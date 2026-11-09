"""
Style Processor for Faceless Shorts
===================================

A 100% offline art-style image transformer built on Pillow only (no numpy, no
opencv, no network). It converts a source still (typically 1080x1920 RGB) into
a stylized frame BEFORE it enters the FFmpeg Ken Burns motion stage, powering
viral reel looks: pixel art, PS2, chalkboard, glow sketch, comic halftone,
flat vector, minimal line, lego, blueprint, pop art, watercolor, oil painting
and synthwave duotone.

Design rules:

* Pure stdlib + PIL (``math``, ``random``, ``os`` + ``PIL``).
* Deterministic: every noise layer is generated from a fixed seed, so repeated
  renders of the same input are byte-identical.
* Robust: any input mode (RGBA/P/L/...) is normalized to RGB, unknown ops fall
  back to an unchanged copy instead of raising, and output directories are
  created automatically.
* Fast: each op runs well under 1.5s on a 1080x1920 image.

Public API::

    from faceless_shorts.style_processor import StyleProcessor

    StyleProcessor.available_ops()                # -> list[str]
    StyleProcessor.get_description("pixel_art")   # -> str
    StyleProcessor.apply(src, dst, "blueprint")   # -> dst path
"""

import math
import os
import random
from collections.abc import Callable

from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageMath,
    ImageOps,
    ImageStat,
)

__all__ = ["StyleProcessor"]

# Fixed seeds keep every noise layer deterministic across runs.
_SEED_PS2 = 1001
_SEED_CHALK_DUST = 1002
_SEED_CHALK_STREAK = 1003
_SEED_BLUEPRINT = 1004
_SEED_WATERCOLOR = 1005
_SEED_OIL = 1006

# Color-dodge evaluated in C by PIL.ImageMath: min(255, a * 255 / max(255 - b, 1)).
_DODGE_EXPR = "convert(min(a * 255 / max(255 - b, 1), 255), 'L')"

# cos(45 deg): the Benday lattice is rotated 45 degrees.
_DIAG = math.cos(math.radians(45))


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _solid(size: tuple[int, int], color: tuple[int, int, int]) -> Image.Image:
    """Flat RGB layer of ``color`` at ``size``."""
    return Image.new("RGB", size, color)


def _noise(size: tuple[int, int], sigma: float, seed: int) -> Image.Image:
    """Deterministic gaussian-ish noise (mode ``L``, mean ~128, stdev ~sigma).

    ``Image.effect_noise`` cannot be seeded, so four uniform ``random``
    streams are averaged (central limit theorem) and shaped with a point
    curve to reach the requested spread.
    """
    w, h = size
    n = w * h
    rng = random.Random(seed)
    layers = [Image.frombytes("L", size, rng.randbytes(n)) for _ in range(4)]
    # Two levels of C-speed halving: mean 128, stdev ~36.8 before shaping.
    avg = ImageChops.add(
        ImageChops.add(layers[0], layers[1], 2),
        ImageChops.add(layers[2], layers[3], 2),
        2,
    )
    gain = sigma / 36.8
    if abs(gain - 1.0) > 0.02:
        avg = avg.point(lambda v: max(0, min(255, int(round(128 + (v - 128) * gain)))))
    return avg


def _color_dodge(base: Image.Image, blend: Image.Image) -> Image.Image:
    """Photoshop color-dodge of two ``L`` bands: min(255, base / (1 - blend)).

    Pillow >= 10 removed ``ImageChops.dodge``, so the exact per-pixel math is
    evaluated through ``PIL.ImageMath`` (C inner loop, ~6ms on 1080x1920).
    """
    return ImageMath.unsafe_eval(_DODGE_EXPR, a=base, b=blend)


def _kill_border(mask: Image.Image, width: int = 2) -> Image.Image:
    """Zero a ``width`` px frame so FIND_EDGES border artifacts vanish."""
    w, h = mask.size
    if width > 0 and w > 2 * width and h > 2 * width:
        # outline (not fill!) + width draws only the frame
        ImageDraw.Draw(mask).rectangle((0, 0, w - 1, h - 1), outline=0, width=width)
    return mask


def _edge_mask(img: Image.Image, blur: float = 0.0, border: int = 2) -> Image.Image:
    """Bright-where-lines edge mask (mode ``L``) with borders suppressed."""
    edges = img.filter(ImageFilter.FIND_EDGES)
    if edges.mode != "L":
        edges = edges.convert("L")
    if blur > 0:
        edges = edges.filter(ImageFilter.GaussianBlur(blur))
    return _kill_border(edges, border)


def _vignette(img: Image.Image, amount: float = 0.5) -> Image.Image:
    """Radial corner darkening: edges dimmed by ``amount`` (0..1)."""
    if amount <= 0:
        return img
    w, h = img.size
    sw, sh = max(8, w // 4), max(8, h // 4)
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, sw - 1, sh - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(2.0, min(sw, sh) * 0.15)))
    mask = mask.resize((w, h), Image.Resampling.BILINEAR)
    dark = img.point(lambda v: int(v * (1.0 - amount)))
    return Image.composite(img, dark, mask)


def _screen_tint(
    base: Image.Image,
    color: tuple[int, int, int],
    mask: Image.Image,
    gain: float = 1.0,
) -> Image.Image:
    """Screen ``color`` onto ``base`` wherever ``mask`` (scaled by ``gain``) is set."""
    if gain != 1.0:
        mask = mask.point(lambda v: min(255, int(v * gain)))
    if mask.getbbox() is None:
        return base
    layer = _solid(base.size, color)
    return Image.composite(ImageChops.screen(base, layer), base, mask)


def _ramp_lut(positions: list[int], values: list[int]) -> list[int]:
    """256-entry LUT with piecewise-linear interpolation between stops."""
    lut: list[int] = []
    for v in range(256):
        if v <= positions[0]:
            lut.append(values[0])
        elif v >= positions[-1]:
            lut.append(values[-1])
        else:
            for i in range(len(positions) - 1):
                if positions[i] <= v <= positions[i + 1]:
                    span = positions[i + 1] - positions[i]
                    t = (v - positions[i]) / span if span else 0.0
                    val = values[i] + (values[i + 1] - values[i]) * t
                    lut.append(max(0, min(255, int(round(val)))))
                    break
    return lut


def _halftone_overlay(gray: Image.Image, spacing: int) -> Image.Image:
    """White RGB overlay carrying black Benday dots on a 45-degree lattice.

    Dot radius follows local darkness sampled from a heavily downscaled
    luminance map, so light cells stay dot-free.
    """
    w, h = gray.size
    step = spacing * _DIAG  # nearest-neighbour distance stays == spacing
    cells_w = max(1, w // spacing)
    cells_h = max(1, h // spacing)
    cell_px = gray.resize((cells_w, cells_h), Image.Resampling.BILINEAR).load()
    max_r = spacing * 0.46

    overlay = _solid((w, h), (255, 255, 255))
    draw = ImageDraw.Draw(overlay)
    uw = int(w / step) + 1
    vh = int(h / step) + 1
    for u in range(uw + 1):
        cx = u * step
        sx = min(cells_w - 1, int(cx * cells_w / w))
        for v in range(vh + 1):
            if (u + v) & 1:  # every other lattice node == spacing density
                continue
            cy = v * step
            lum = cell_px[sx, min(cells_h - 1, int(cy * cells_h / h))]
            radius = (1.0 - lum / 255.0) * max_r
            if radius >= 0.8:
                draw.ellipse(
                    (cx - radius, cy - radius, cx + radius, cy + radius),
                    fill=(0, 0, 0),
                )
    return overlay


def _brighten(color: tuple[int, ...], amount: int) -> tuple[int, ...]:
    """Nudge every channel toward white without clipping."""
    return tuple(min(255, int(c) + amount) for c in color)


# ---------------------------------------------------------------------------
# Style ops: each takes (RGB image, params dict) and returns an RGB image
# ---------------------------------------------------------------------------

def _op_pixel_art(img: Image.Image, params: dict) -> Image.Image:
    """Hard-edged chunky pixels: NEAREST downscale -> 16-color palette -> NEAREST upscale."""
    factor = max(1, int(params.get("factor", 6)))
    w, h = img.size
    small = img.resize((max(1, w // factor), max(1, h // factor)), Image.Resampling.NEAREST)
    small = small.quantize(
        colors=16, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
    ).convert("RGB")
    up = small.resize((w, h), Image.Resampling.NEAREST)
    return up.filter(ImageFilter.UnsharpMask(radius=1, percent=60))


def _op_ps2_style(img: Image.Image, params: dict) -> Image.Image:
    """Sixth-gen console look: soft low-res bloom, 64 colors, sensor noise, slight saturation pop."""
    w, h = img.size
    small = img.resize((max(8, int(w / 2.5)), max(8, int(h / 2.5))), Image.Resampling.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(0.7))
    small = small.quantize(
        colors=64, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE
    ).convert("RGB")
    out = small.resize((w, h), Image.Resampling.BILINEAR)  # soft, slightly bloomy upscale
    grain = _noise((w, h), 40, _SEED_PS2).convert("RGB")
    out = Image.blend(out, grain, 0.06)
    return ImageEnhance.Color(out).enhance(1.15)


def _op_chalkboard(img: Image.Image, params: dict) -> Image.Image:
    """Dark green slate board with white chalk linework, dust grain and wipe streaks."""
    w, h = img.size
    board = ImageEnhance.Color(img).enhance(0.35)
    board = ImageChops.multiply(board, _solid((w, h), (24, 42, 34)))  # chalkboard green tint

    # fine chalk-dust grain
    dust = _noise((w, h), 22, _SEED_CHALK_DUST).convert("RGB")
    board = Image.blend(board, dust, 0.18)

    # subtle horizontal chalk wipe streaks (lighter, low opacity)
    streaks = _noise((w, max(6, h // 14)), 55, _SEED_CHALK_STREAK)
    streaks = streaks.resize((w, h), Image.Resampling.BILINEAR)
    streaks = streaks.filter(ImageFilter.GaussianBlur(2.5))
    lift = streaks.point(lambda v: min(90, max(0, (v - 150) * 2)))
    board = Image.composite(_solid((w, h), (226, 233, 221)), board, lift)

    # white chalk line work traced from the image edges
    edges = _edge_mask(img, blur=0.6)
    edges = edges.point(lambda v: min(255, v * 2))  # lift faint contours
    chalk_mask = edges.point(lambda v: min(255, int(v * 0.7)))  # white chalk opacity
    board = Image.composite(_solid((w, h), (247, 245, 236)), board, chalk_mask)

    return _vignette(board, amount=0.55)


def _op_glow_sketch(img: Image.Image, params: dict) -> Image.Image:
    """Pencil-sketch lines on near-black with a two-tone neon glow halo."""
    glow = tuple(int(c) for c in params.get("glow_color", (0, 220, 255)))
    secondary = tuple(int(c) for c in params.get("secondary_color", (255, 60, 200)))

    gray = img.convert("L")
    blurred_inv = ImageOps.invert(gray).filter(ImageFilter.GaussianBlur(4))
    sketch = _color_dodge(gray, blurred_inv)  # white paper, dark pencil lines

    edges = _edge_mask(sketch)
    edges = edges.point(lambda v: min(255, v * 2))  # lift faint pencil strokes
    core = edges.filter(ImageFilter.GaussianBlur(1.6))  # crisp linework
    halo = edges.filter(ImageFilter.GaussianBlur(3.0))  # inner glow
    wide = edges.filter(ImageFilter.GaussianBlur(9.0))  # outer halo

    # near-black version of the sketch: dim inverted linework on a black field
    base = ImageOps.invert(sketch).point(lambda v: int(v * 0.16)).convert("RGB")
    base = _screen_tint(base, _brighten(glow, 70), core, gain=1.0)
    base = _screen_tint(base, glow, halo, gain=1.0)
    # the wide halo is much weaker than the inner one: boost so the magenta
    # fringe (and the whole outer bloom) actually shows on the dark side
    outer = ImageChops.subtract(wide, halo).point(lambda v: min(255, v * 6))
    base = _screen_tint(base, secondary, outer, gain=1.0)
    return base


def _op_comic_halftone(img: Image.Image, params: dict) -> Image.Image:
    """Saturated posterized comic print with 45-degree Benday dots and inked edges."""
    spacing = max(3, int(params.get("dot_size", 6)))
    out = ImageEnhance.Color(img).enhance(1.6)
    out = ImageOps.posterize(out, 4)

    # Benday dot layer, multiply-blended at 25% (dot-free on light cells)
    overlay = _halftone_overlay(img.convert("L"), spacing)
    out = Image.blend(out, ImageChops.multiply(out, overlay), 0.25)

    # ink outline: darkened edge lines multiplied at 40%
    edges = _edge_mask(img, blur=0.5)
    boosted = edges.point(lambda v: min(255, v * 3))
    ink = ImageOps.invert(boosted).convert("RGB")
    out = Image.blend(out, ImageChops.multiply(out, ink), 0.40)
    return out


def _op_flat_vector(img: Image.Image, params: dict) -> Image.Image:
    """Clean flat-vector/infographic look: smoothed regions posterized into flat color fields."""
    out = img.filter(ImageFilter.MedianFilter(size=13))  # flatten regions
    out = ImageOps.posterize(out, 6)
    out = ImageEnhance.Color(out).enhance(1.25)
    out = ImageEnhance.Contrast(out).enhance(1.1)
    out = out.filter(ImageFilter.GaussianBlur(0.4))
    return ImageOps.posterize(out, 7)  # re-posterize kills gradient banding


def _op_minimal_line(img: Image.Image, params: dict) -> Image.Image:
    """Minimal single-weight black line art on a pure white background."""
    threshold = int(params.get("threshold", 70))
    gray = ImageOps.autocontrast(img.convert("L"))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    _kill_border(edges, 2)
    bw = edges.point(lambda v: 255 if v >= threshold else 0)
    if ImageStat.Stat(bw).mean[0] < 128:  # invert-safe: background must be white
        bw = ImageOps.invert(bw)
    return bw.filter(ImageFilter.MinFilter(3)).convert("RGB")  # slightly thicker lines


def _op_lego_studs(img: Image.Image, params: dict) -> Image.Image:
    """Toy brick look: flat plastic colors under a regular grid of shaded studs."""
    w, h = img.size
    spacing = max(24, int(params.get("stud_spacing", 96)))
    radius = max(4, spacing // 4)

    out = img.quantize(
        colors=18, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE
    ).convert("RGB")
    out = ImageEnhance.Color(out).enhance(1.3)

    # four masks: drop shadow, stud body, dark ring, top-left highlight arc
    shadow = Image.new("L", (w, h), 0)
    body = Image.new("L", (w, h), 0)
    ring = Image.new("L", (w, h), 0)
    highlight = Image.new("L", (w, h), 0)
    d_shadow = ImageDraw.Draw(shadow)
    d_body = ImageDraw.Draw(body)
    d_ring = ImageDraw.Draw(ring)
    d_high = ImageDraw.Draw(highlight)

    for cy in range(spacing // 2, h, spacing):
        for cx in range(spacing // 2, w, spacing):
            bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
            d_shadow.ellipse(
                (cx - radius + 2, cy - radius + 2, cx + radius + 2, cy + radius + 2),
                fill=255,
            )
            d_body.ellipse(bbox, fill=255)
            d_ring.ellipse(bbox, outline=255, width=2)
            d_high.arc(
                (cx - radius + 2, cy - radius + 2, cx + radius - 2, cy + radius - 2),
                165,
                285,
                fill=255,
                width=2,
            )

    # faint drop shadow first, then the stud overlay blended at 35%
    out = Image.composite(_solid((w, h), (0, 0, 0)), out, shadow.point(lambda v: int(v * 0.15)))
    shaded = out.point(lambda v: int(v * 0.86))
    out = Image.composite(shaded, out, body.point(lambda v: int(v * 0.35)))
    out = Image.composite(_solid((w, h), (12, 12, 16)), out, ring.point(lambda v: int(v * 0.6)))
    out = Image.composite(
        _solid((w, h), (255, 255, 255)), out, highlight.point(lambda v: int(v * 0.4))
    )
    return out


def _op_blueprint(img: Image.Image, params: dict) -> Image.Image:
    """Cyanotype engineering blueprint: duotone map, fine grid, paper grain, vignette."""
    w, h = img.size
    gray = ImageOps.invert(ImageOps.autocontrast(img.convert("L")))
    deep, pale = (10, 42, 88), (210, 235, 255)
    bands = tuple(gray.point(_ramp_lut([0, 255], [deep[i], pale[i]])) for i in range(3))
    out = Image.merge("RGB", bands)

    # engineering grid every 60px (thin, light blue, alpha ~50)
    grid = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(grid)
    for x in range(0, w, 60):
        draw.line((x, 0, x, h - 1), fill=50)
    for y in range(0, h, 60):
        draw.line((0, y, w - 1, y), fill=50)
    out = Image.composite(_solid((w, h), (170, 210, 240)), out, grid)

    # slight paper noise, then vignette
    grain = _noise((w, h), 26, _SEED_BLUEPRINT).convert("RGB")
    out = Image.blend(out, ImageChops.multiply(out, grain), 0.10)
    return _vignette(out, amount=0.35)


def _op_pop_art(img: Image.Image, params: dict) -> Image.Image:
    """Lichtenstein pop art: bold colors, big halftone dots, thick ink, high contrast."""
    spacing = max(4, int(params.get("dot_size", 10)))
    out = ImageEnhance.Color(img).enhance(1.9)
    out = ImageOps.posterize(out, 3)

    # big black halftone dots, multiply at 35%
    overlay = _halftone_overlay(img.convert("L"), spacing)
    out = Image.blend(out, ImageChops.multiply(out, overlay), 0.35)

    # thick black edge lines, multiply at 55%
    edges = _edge_mask(img, blur=0.4)
    ink_mask = edges.point(lambda v: 255 if v >= 24 else 0)
    ink_mask = ink_mask.filter(ImageFilter.MaxFilter(3))  # thicken
    ink = ImageOps.invert(ink_mask).convert("RGB")
    out = Image.blend(out, ImageChops.multiply(out, ink), 0.55)
    return ImageEnhance.Contrast(out).enhance(1.25)


def _op_watercolor(img: Image.Image, params: dict) -> Image.Image:
    """Gentle painterly watercolor: posterized washes, paper grain, edge pooling."""
    w, h = img.size
    out = img.filter(ImageFilter.MedianFilter(size=7))
    out = ImageOps.posterize(out, 6)

    # paper texture: fine grain multiply + warm paper tint multiply
    grain = _noise((w, h), 12, _SEED_WATERCOLOR).convert("RGB")
    out = Image.blend(out, ImageChops.multiply(out, grain), 0.10)
    warm = _solid((w, h), (255, 252, 245))
    out = Image.blend(out, ImageChops.multiply(out, warm), 0.12)

    # edge darkening: pigment pools along edges (darkened copy at 30%)
    edges = _edge_mask(out, blur=1.2)
    pooled = Image.composite(out.point(lambda v: int(v * 0.55)), out, edges)
    out = Image.blend(out, pooled, 0.30)

    out = ImageEnhance.Color(out).enhance(0.9)
    return ImageEnhance.Brightness(out).enhance(1.06)


def _op_oil_painting(img: Image.Image, params: dict) -> Image.Image:
    """Painterly oil-brush look: Kuwahara-like mode flattening with crisp impasto edges."""
    w, h = img.size
    # pass 1 on a half-scale copy (cheap strong flattening), pass 2 at full res
    # (size 7 keeps the full-res pass inside the 1.5s budget on 1080x1920)
    half = img.resize((max(1, w // 2), max(1, h // 2)), Image.Resampling.BILINEAR)
    flat = half.filter(ImageFilter.ModeFilter(size=9)).resize((w, h), Image.Resampling.BILINEAR)
    out = flat.filter(ImageFilter.ModeFilter(size=7))
    out = out.filter(ImageFilter.UnsharpMask(radius=3, percent=120, threshold=2))
    out = ImageEnhance.Color(out).enhance(1.2)
    grain = _noise((w, h), 30, _SEED_OIL).convert("RGB")
    return Image.blend(out, ImageChops.multiply(out, grain), 0.08)


def _op_synthwave_duotone(img: Image.Image, params: dict) -> Image.Image:
    """Purple-magenta-cyan gradient-map duotone with retro scanlines."""
    w, h = img.size
    gray = img.convert("L")
    lut_r = _ramp_lut([0, 128, 255], [26, 255, 60])
    lut_g = _ramp_lut([0, 128, 255], [2, 45, 240])
    lut_b = _ramp_lut([0, 128, 255], [46, 140, 255])
    out = Image.merge(
        "RGB", (gray.point(lut_r), gray.point(lut_g), gray.point(lut_b))
    )

    # scanline darkening every 3px at 10%
    scan = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(scan)
    for y in range(0, h, 3):
        draw.line((0, y, w - 1, y), fill=255)
    dark = out.point(lambda v: int(v * 0.9))
    out = Image.composite(dark, out, scan)

    return ImageEnhance.Color(out).enhance(1.15)  # slight chroma push


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

OPS: dict[str, Callable[[Image.Image, dict], Image.Image]] = {
    "pixel_art": _op_pixel_art,
    "ps2_style": _op_ps2_style,
    "chalkboard": _op_chalkboard,
    "glow_sketch": _op_glow_sketch,
    "comic_halftone": _op_comic_halftone,
    "flat_vector": _op_flat_vector,
    "minimal_line": _op_minimal_line,
    "lego_studs": _op_lego_studs,
    "blueprint": _op_blueprint,
    "pop_art": _op_pop_art,
    "watercolor": _op_watercolor,
    "oil_painting": _op_oil_painting,
    "synthwave_duotone": _op_synthwave_duotone,
}

DESCRIPTIONS: dict[str, str] = {
    "pixel_art": "Chunky 16-color pixel art with hard NEAREST-neighbor edges.",
    "ps2_style": "Sixth-gen console look: soft low-res bloom, 64 colors and sensor noise.",
    "chalkboard": "Dark slate board with white chalk linework, dust grain and wipe streaks.",
    "glow_sketch": "Pencil sketch linework glowing with a cyan/magenta neon halo on near-black.",
    "comic_halftone": "Saturated posterized comic print with 45-degree Benday dots and ink.",
    "flat_vector": "Clean flat-vector/infographic color fields with zero noise.",
    "minimal_line": "Single-weight black line art on a pure white background.",
    "lego_studs": "Flat plastic brick colors under a regular grid of shaded toy studs.",
    "blueprint": "Cyanotype engineering blueprint with pale grid lines and paper grain.",
    "pop_art": "Lichtenstein pop art: bold color, big halftone dots and thick ink.",
    "watercolor": "Gentle painterly watercolor with paper grain and edge pigment pooling.",
    "oil_painting": "Painterly oil-brush flattening with crisp impasto edges.",
    "synthwave_duotone": "Purple-magenta-cyan gradient map with retro scanlines.",
}


class StyleProcessor:
    """Offline PIL art-style transformer for pre-Ken Burns stills.

    Stateless static API: nothing is cached, every call reads the source,
    stylizes it deterministically and writes the result to disk.
    """

    @staticmethod
    def available_ops() -> list[str]:
        """Return every supported style op name, in stable registration order."""
        return list(OPS)

    @staticmethod
    def get_description(op: str) -> str:
        """Return the one-line description of ``op`` (empty string if unknown)."""
        return DESCRIPTIONS.get(op, "")

    @staticmethod
    def apply(image_path: str, output_path: str, op: str, params: dict | None = None) -> str:
        """Load image, apply op, save to output_path (create dirs), return output_path.

        Any input mode is normalized to RGB. An unknown ``op`` never raises:
        an unchanged copy is saved instead, so callers may pass raw user
        input without guarding.
        """
        with Image.open(image_path) as source:
            img = source.convert("RGB")

        func = OPS.get(op)
        result = func(img, dict(params or {})) if func is not None else img.copy()

        # Defensive invariants: RGB, original size, real image object.
        if not isinstance(result, Image.Image):
            result = img
        if result.mode != "RGB":
            result = result.convert("RGB")
        if result.size != img.size:
            result = result.resize(img.size, Image.Resampling.NEAREST)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fmt = Image.registered_extensions().get(os.path.splitext(output_path)[1].lower())
        result.save(output_path, format=fmt or "PNG")
        return output_path
