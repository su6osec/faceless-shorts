"""
postfx.py — Composable premium post-processing FX builder (zero-cost).

Turns a list of named effects and/or curated packs into a complete
``-filter_complex`` filtergraph BODY (segments joined by ``;``), ready to
embed directly::

    ffmpeg -i in.mp4 -filter_complex "<body>" -map "[vout]" out.mp4

Public API
----------
``PostFX.available()``      -> list of every supported effect name
``PostFX.describe(name)``   -> one-line description (effects and packs)
``PostFX.build(...)``       -> filtergraph body string
``PostFX.PACKS``            -> curated bundles of effect names

Design
------
* **Linear** effects are plain comma-joined filter chains. They are
  buffered and flushed into a single filtergraph segment whenever a
  **graph** effect (one that splits/blends with its own internal labels)
  appears, which keeps the emitted filtergraph minimal but always valid.
* RGB-sensitive blends run in ``format=gbrp`` (planar RGB) to avoid the
  YUV chroma "pink shift" this project already ran into; every graph
  effect converts back with ``format=yuv420p``, and a trailing linear
  flush is closed with ``format=yuv420p`` as well.
* Names resolve **effect first, pack second**, so ``dreamy`` builds the
  standalone effect; pass ``PostFX.PACKS["dreamy"]`` as a list to request
  that pack explicitly.
* ``width``/``height``/``duration`` are validated and handed to effects
  through the graph context (currently ``anamorphic`` scales its streak
  length from ``width``).

Validation notes (FFmpeg 9.0.2, homebrew ``ffmpeg-full``)
----------------------------------------------------------
* ``tmix`` weights must be single-quoted: literal double quotes are kept
  inside the option value and make tmix fail with "Invalid syntax for
  weights". ``weights='1 1 1 1'`` parses everywhere.
* ``gblur`` exposes ``sigma`` (horizontal) + ``sigmaV`` (vertical) only —
  ``sigmaX``/``sigmaY`` do not exist in FFmpeg 9. Horizontal-only blur is
  ``gblur=sigma=N:sigmaV=0`` (confirmed via PSNR: columns 16->34 dB while
  rows stay near baseline, vs 51 dB for a full 2-D blur).
* ``huesaturation`` exists but has no ``s`` option; saturation changes use
  ``saturation=<delta>`` (range -1..1), so the VHS look uses +0.05.
* ``boxblur`` is strictly 2-D (no separate X/Y radii), so the anamorphic
  streak uses ``gblur`` instead.

No external dependencies — output is plain FFmpeg filtergraph text.
"""

from __future__ import annotations

import itertools
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

__all__ = ["PostFX"]

# Internal helpers -------------------------------------------------------------

EffectsInput = Union[str, Sequence[str]]
GraphFn = Callable[[str, str, Dict], str]


def _label(text: str, arg: str) -> str:
    """Normalize a user-supplied filtergraph label (brackets optional)."""
    if not isinstance(text, str):
        raise ValueError(f"{arg} must be a string, got {type(text).__name__}")
    value = text.strip()
    if value.startswith("[") and value.endswith("]") and len(value) >= 2:
        value = value[1:-1].strip()
    if not value or any(ch in value for ch in "[];,"):
        raise ValueError(f"{arg} must be a plain filtergraph label, got {text!r}")
    return value


def _opt_positive_int(value, arg: str):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{arg} must be a positive integer or None, got {value!r}")
    return value


def _opt_positive_number(value, arg: str):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{arg} must be a positive number or None, got {value!r}")
    return value


def _tokenize(effects: EffectsInput) -> List[str]:
    """Split the flexible ``effects`` argument into raw name tokens."""
    if effects is None:
        return []
    if isinstance(effects, str):
        raw = effects.split(",")
    elif isinstance(effects, (list, tuple)):
        raw = []
        for item in effects:
            if not isinstance(item, str):
                raise ValueError(
                    "effects must contain only names (str); "
                    f"got {type(item).__name__} ({item!r})"
                )
            raw.extend(item.split(","))
    else:
        raise ValueError(
            "effects must be a comma-separated string or a list of names, "
            f"got {type(effects).__name__}"
        )
    return [token.strip() for token in raw if token.strip()]


# Graph effect payloads --------------------------------------------------------
# Signature: (input_label, output_label, ctx) -> one or more ';' joined segments.
# Internal labels are namespaced with a per-build tag so repeated graph effects
# never collide.


def _graph_bloom(fin: str, fout: str, ctx: Dict) -> str:
    t = ctx["tag"]()
    base, src, glow = f"{t}base", f"{t}src", f"{t}glow"
    return (
        f"[{fin}]format=gbrp,split=2[{base}][{src}];"
        f"[{src}]gblur=sigma=18:steps=1,"
        f"colorchannelmixer=rr=0.28:gg=0.24:bb=0.30[{glow}];"
        f"[{base}][{glow}]blend=all_mode=screen,format=yuv420p[{fout}]"
    )


def _graph_halation(fin: str, fout: str, ctx: Dict) -> str:
    t = ctx["tag"]()
    base, src, glow = f"{t}base", f"{t}src", f"{t}glow"
    return (
        f"[{fin}]format=gbrp,split=2[{base}][{src}];"
        f"[{src}]format=yuv420p,"
        f"lutyuv=y='if(gt(val,170),val,0)':u=128:v=128,"
        f"gblur=sigma=10,format=gbrp,"
        f"colorchannelmixer=rr=1.10:gg=0.50:bb=0.22[{glow}];"
        f"[{base}][{glow}]blend=all_mode=screen:all_opacity=0.7,"
        f"format=yuv420p[{fout}]"
    )


def _graph_dreamy(fin: str, fout: str, ctx: Dict) -> str:
    t = ctx["tag"]()
    base, src, soft = f"{t}base", f"{t}src", f"{t}soft"
    return (
        f"[{fin}]format=gbrp,split=2[{base}][{src}];"
        f"[{src}]gblur=sigma=9[{soft}];"
        f"[{base}][{soft}]blend=all_mode=screen,eq=brightness=-0.02,"
        f"format=yuv420p[{fout}]"
    )


def _graph_anamorphic(fin: str, fout: str, ctx: Dict) -> str:
    t = ctx["tag"]()
    base, src, glow = f"{t}base", f"{t}src", f"{t}glow"
    width = ctx.get("width")
    sigma = max(20, int(round(width * 0.065))) if width else 70
    return (
        f"[{fin}]format=gbrp,split=2[{base}][{src}];"
        f"[{src}]gblur=sigma={sigma}:sigmaV=0,"
        f"colorchannelmixer=rr=0.45:gg=0.65:bb=1.40[{glow}];"
        f"[{base}][{glow}]blend=all_mode=screen,format=yuv420p[{fout}]"
    )


# Effect table -----------------------------------------------------------------
# kind "linear": payload is a comma-joined chain fragment (no labels).
# kind "graph":  payload is a callable(in, out, ctx) -> segment string(s).

_EFFECTS: Dict[str, Tuple[str, Union[str, GraphFn]]] = {
    # 1
    "bloom": ("graph", _graph_bloom),
    # 2
    "halation": ("graph", _graph_halation),
    # 3
    "chroma": ("linear", "rgbashift=rh=3:bh=-3"),
    # 4
    "grain": ("linear", "noise=alls=7:allf=t+u"),
    # 5
    "vignette": ("linear", "vignette=PI/4.6"),
    # 6
    "sharpen": (
        "linear",
        "unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.9:chroma_amount=0.4",
    ),
    # 7
    "punch": ("linear", "eq=contrast=1.12:saturation=1.12:brightness=0.01"),
    # 8
    "teal_orange": (
        "linear",
        "colorbalance=rs=0.05:gs=-0.01:bs=-0.06:rm=0.03:bm=-0.05:rh=0.04:bh=-0.03,"
        "eq=saturation=1.08:contrast=1.06",
    ),
    # 9
    "dreamy": ("graph", _graph_dreamy),
    # 10
    "motion_blur": ("linear", "tmix=frames=4:weights='1 1 1 1'"),
    # 11
    "vhs": (
        "linear",
        "rgbashift=rh=4:bh=-4,noise=alls=10:allf=t+u,"
        "eq=contrast=0.96:saturation=1.15,huesaturation=saturation=0.05",
    ),
    # 12
    "vivid": (
        "linear",
        "eq=gamma=1.07:saturation=1.25:contrast=1.1,"
        "colorchannelmixer=rr=1.02:bb=1.02",
    ),
    # 13
    "anamorphic": ("graph", _graph_anamorphic),
    # 14
    "noir": (
        "linear",
        "hue=s=0,eq=contrast=1.35:brightness=-0.02:gamma=0.98,noise=alls=6:allf=t+u",
    ),
    # 15
    "night": (
        "linear",
        "hue=s=0,eq=brightness=-0.05:contrast=1.25,"
        "colorchannelmixer=gg=1.35:rr=0.45:bb=0.55,vignette=PI/3.5,"
        "noise=alls=9:allf=t+u",
    ),
}

_DESCRIPTIONS: Dict[str, str] = {
    "bloom": "Soft highlight bloom (gaussian glow screened in RGB space)",
    "halation": "Warm film halation — highlights bleed orange across the frame",
    "chroma": "Optical chromatic aberration (red/blue horizontal shift)",
    "grain": "35mm film grain (temporal full-range noise)",
    "vignette": "Gentle lens vignette (angle PI/4.6)",
    "sharpen": "Unsharp-mask detail boost (luma 0.9 / chroma 0.4)",
    "punch": "Punchy grade: +12% contrast, +12% saturation, tiny lift",
    "teal_orange": "Blockbuster teal-and-orange color grade",
    "dreamy": "Soft-focus diffusion glow (screen-blended gaussian diffusion)",
    "motion_blur": "Temporal motion blur (tmix over 4 frames, static frames safe)",
    "vhs": "Retro VHS look: chroma shift, tape grain, washed-out contrast",
    "vivid": "Vivid punch: gamma 1.07, saturation 1.25, subtle RGB gain",
    "anamorphic": "Horizontal anamorphic lens streaks (blue flare)",
    "noir": "High-contrast black & white film-noir grade",
    "night": "Night-vision green: desaturated, green-boosted, vignetted",
}

_PASSTHROUGH = frozenset({"none", "nofx"})


def _valid_names_message(unknown: Sequence[str]) -> str:
    listed = ", ".join(repr(name) for name in unknown)
    return (
        f"Unknown effect name(s): {listed}. "
        f"Valid effect names: {', '.join(_EFFECTS)}. "
        f"Valid pack names: {', '.join(_PACK_ORDER)}. "
        f"Passthrough names: none, nofx."
    )


# Pack expansion ---------------------------------------------------------------


def _expand(tokens: Sequence[str]) -> List[str]:
    """Resolve tokens (effects, packs, passthrough) -> deduped effect names."""
    unknown: List[str] = []
    expanded: List[str] = []
    for token in tokens:
        key = token.strip().lower()
        if not key or key in _PASSTHROUGH:
            continue
        if key in _EFFECTS:
            expanded.append(key)
        elif key in _PACK_ORDER:
            expanded.extend(_PACKS[key])
        else:
            unknown.append(token)
    if unknown:
        raise ValueError(_valid_names_message(unknown))
    # Guard against mutated packs that smuggle in non-effect names.
    invalid = [name for name in expanded if name not in _EFFECTS]
    if invalid:
        raise ValueError(_valid_names_message(invalid))
    # Dedupe while preserving first occurrence order.
    seen = set()
    return [name for name in expanded if not (name in seen or seen.add(name))]


# The pack manifest lives at module level so ``_expand`` can use it before the
# class body finishes executing; ``PostFX.PACKS`` re-exports the same dict.
_PACKS: Dict[str, List[str]] = {
    "clean": [],
    "cinematic": ["bloom", "halation", "teal_orange", "grain", "vignette"],
    "premium": ["bloom", "chroma", "punch", "sharpen", "grain", "vignette"],
    "dreamy": ["dreamy", "bloom", "vignette"],
    "retro": ["vhs", "grain", "chroma", "vignette"],
    "nofx": [],
}
_PACK_ORDER = tuple(_PACKS)


class PostFX:
    """Builds FFmpeg ``-filter_complex`` bodies from effects and packs."""

    PACKS: Dict[str, List[str]] = _PACKS

    # -- API ------------------------------------------------------------------

    @staticmethod
    def available() -> List[str]:
        """All supported effect names (definition order)."""
        return list(_EFFECTS)

    @staticmethod
    def describe(effect: str) -> str:
        """One-line description of an effect, a pack, or the 'none' passthrough."""
        if not isinstance(effect, str):
            raise ValueError(f"effect must be a string, got {type(effect).__name__}")
        key = effect.strip().lower()
        if key in _PASSTHROUGH:
            return "Null passthrough (no processing applied)."
        if key in _DESCRIPTIONS:
            return _DESCRIPTIONS[key]
        if key in _PACKS:
            members = _PACKS[key]
            if not members:
                return f"Pack '{key}': no effects (null passthrough)."
            return f"Pack '{key}': {' + '.join(members)} ({len(members)} effects)."
        raise ValueError(_valid_names_message([effect]))

    @staticmethod
    def build(
        effects: EffectsInput,
        input_label: str = "0:v",
        output_label: str = "vout",
        duration: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> str:
        """Return a complete filter_complex BODY (segments joined by ';').

        ``effects`` is a comma-separated string or a list of names and may
        include pack names; packs expand into their effect list, names are
        deduped while preserving order, and unknown names raise
        ``ValueError`` listing every valid name.

        ``duration``/``width``/``height`` are validated and passed to
        effects through the graph context (``anamorphic`` scales its
        streak length from ``width``).

        Embed as::

            ffmpeg -i in -filter_complex "<body>" -map "[vout]" out
        """
        in_lbl = _label(input_label, "input_label")
        out_lbl = _label(output_label, "output_label")
        width = _opt_positive_int(width, "width")
        height = _opt_positive_int(height, "height")
        duration = _opt_positive_number(duration, "duration")

        names = _expand(_tokenize(effects))
        if not names:
            return f"[{in_lbl}]null[{out_lbl}]"

        seg_ids = itertools.count(1)
        tag_ids = itertools.count(1)
        ctx: Dict = {
            "width": width,
            "height": height,
            "duration": duration,
            "tag": lambda: f"p{next(tag_ids)}",
        }

        segments: List[str] = []
        pending: List[str] = []
        current = in_lbl

        def fresh_segment_label() -> str:
            return f"fx{next(seg_ids)}"

        for name in names:
            kind, payload = _EFFECTS[name]
            if kind == "linear":
                pending.append(payload)  # type: ignore[arg-type]
                continue
            # Flush buffered linear filters before entering a graph effect.
            if pending:
                nxt = fresh_segment_label()
                segments.append(f"[{current}]{','.join(pending)}[{nxt}]")
                current = nxt
                pending = []
            nxt = fresh_segment_label()
            segments.append(payload(current, nxt, ctx))  # type: ignore[operator]
            current = nxt

        if pending:
            # Trailing linear chain: guarantee a yuv420p output for the
            # renderer regardless of the source pixel format.
            segments.append(f"[{current}]{','.join(pending)},format=yuv420p[{out_lbl}]")
        elif segments:
            # Last segment is a graph effect; retarget its output label.
            tail = f"[{current}]"
            last = segments[-1]
            if not last.endswith(tail):  # pragma: no cover - internal invariant
                raise RuntimeError(f"postfx: segment does not end with {tail}")
            segments[-1] = last[: -len(tail)] + f"[{out_lbl}]"
        else:  # pragma: no cover - names is non-empty, so a segment exists
            return f"[{in_lbl}]null[{out_lbl}]"

        return ";".join(segments)
