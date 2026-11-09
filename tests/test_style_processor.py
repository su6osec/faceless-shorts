"""Unit tests for the offline PIL style processor (faceless_shorts.style_processor)."""

import os
import random
import shutil
import tempfile
import unittest

from PIL import Image, ImageDraw, ImageStat

from faceless_shorts.style_processor import StyleProcessor

# Every style documented in the public API must be registered.
EXPECTED_OPS = {
    "pixel_art",
    "ps2_style",
    "chalkboard",
    "glow_sketch",
    "comic_halftone",
    "flat_vector",
    "minimal_line",
    "lego_studs",
    "blueprint",
    "pop_art",
    "watercolor",
    "oil_painting",
    "synthwave_duotone",
}


def _build_source(path, size=(270, 480)):
    """Create a reproducible RGB still: gradient plus seeded circles/rectangles."""
    w, h = size
    rows = []
    for y in range(h):
        gy = y / (h - 1)
        row = bytearray()
        for x in range(w):
            gx = x / (w - 1)
            row += bytes(
                (
                    int(255 * gx),
                    int(255 * gy),
                    int(255 * max(0.0, 1.0 - 0.5 * gx - 0.5 * gy)),
                )
            )
        rows.append(bytes(row))
    img = Image.frombytes("RGB", size, b"".join(rows))

    draw = ImageDraw.Draw(img)
    rng = random.Random(20240617)
    for _ in range(12):
        cx, cy = rng.randrange(w), rng.randrange(h)
        r = rng.randrange(8, 42)
        color = (rng.randrange(256), rng.randrange(256), rng.randrange(256))
        if rng.random() < 0.5:
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
        else:
            draw.rectangle((cx - r, cy - r, cx + r, cy + r), fill=color)
    img.save(path)
    return path


class StyleProcessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_root = tempfile.mkdtemp(prefix="style_processor_")
        cls.src_path = os.path.join(cls.tmp_root, "source.png")
        _build_source(cls.src_path)
        with Image.open(cls.src_path) as img:
            cls.src_size = img.size

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_root, ignore_errors=True)

    def setUp(self):
        self.case_dir = tempfile.mkdtemp(prefix="case_", dir=self.tmp_root)

    # -- helpers -----------------------------------------------------------

    def _apply(self, op, name, src_path=None, params=None):
        out_path = os.path.join(self.case_dir, f"{name}.png")
        result = StyleProcessor.apply(src_path or self.src_path, out_path, op, params)
        return result, out_path

    def _assert_valid(self, result, expected_path, check_variance=True):
        self.assertEqual(result, expected_path)
        self.assertTrue(os.path.isfile(result), f"missing output: {result}")
        with Image.open(result) as out:
            out.load()
            self.assertEqual(out.size, self.src_size)
            self.assertEqual(out.mode, "RGB")
            if check_variance:
                self.assertGreater(
                    sum(ImageStat.Stat(out).var),
                    0.0,
                    "output is a solid color (no visual content)",
                )

    # -- API shape ---------------------------------------------------------

    def test_available_ops_contains_all_documented_styles(self):
        ops = StyleProcessor.available_ops()
        self.assertIsInstance(ops, list)
        self.assertTrue(all(isinstance(op, str) for op in ops))
        self.assertEqual(len(ops), len(set(ops)), "duplicate op registration")
        self.assertTrue(
            EXPECTED_OPS.issubset(set(ops)),
            f"missing ops: {EXPECTED_OPS - set(ops)}",
        )

    def test_descriptions_are_non_empty_for_every_op(self):
        for op in StyleProcessor.available_ops():
            with self.subTest(op=op):
                desc = StyleProcessor.get_description(op)
                self.assertIsInstance(desc, str)
                self.assertTrue(desc.strip(), f"empty description for {op}")

    def test_unknown_description_returns_empty_string(self):
        self.assertEqual(StyleProcessor.get_description("definitely_not_a_style"), "")

    # -- core behaviour ----------------------------------------------------

    def test_apply_every_op(self):
        for op in StyleProcessor.available_ops():
            with self.subTest(op=op):
                result, expected = self._apply(op, op)
                self._assert_valid(result, expected)

    def test_apply_unknown_op_saves_unchanged_copy(self):
        result, expected = self._apply("definitely_not_a_style", "unknown")
        self._assert_valid(result, expected)
        with Image.open(self.src_path) as src, Image.open(result) as out:
            self.assertEqual(src.tobytes(), out.tobytes())

    def test_apply_creates_missing_output_directories(self):
        nested = os.path.join(self.case_dir, "deep", "nested", "style.png")
        result = StyleProcessor.apply(self.src_path, nested, "blueprint")
        self.assertEqual(result, nested)
        self.assertTrue(os.path.isfile(nested))

    def test_apply_is_deterministic(self):
        # chalkboard is seeded-noise heavy: same input must give identical bytes.
        first = os.path.join(self.case_dir, "det_a.png")
        second = os.path.join(self.case_dir, "det_b.png")
        StyleProcessor.apply(self.src_path, first, "chalkboard")
        StyleProcessor.apply(self.src_path, second, "chalkboard")
        with open(first, "rb") as fa, open(second, "rb") as fb:
            self.assertEqual(fa.read(), fb.read())

    def test_params_are_honoured(self):
        default_out = os.path.join(self.case_dir, "px_default.png")
        coarse_out = os.path.join(self.case_dir, "px_coarse.png")
        StyleProcessor.apply(self.src_path, default_out, "pixel_art")
        StyleProcessor.apply(self.src_path, coarse_out, "pixel_art", {"factor": 14})
        with open(default_out, "rb") as fa, open(coarse_out, "rb") as fb:
            self.assertNotEqual(fa.read(), fb.read())

    # -- robustness --------------------------------------------------------

    def test_apply_black_and_white_images(self):
        for name, color in (("black", (0, 0, 0)), ("white", (255, 255, 255))):
            flat_path = os.path.join(self.case_dir, f"{name}.png")
            Image.new("RGB", self.src_size, color).save(flat_path)
            for op in StyleProcessor.available_ops():
                with self.subTest(image=name, op=op):
                    out_path = os.path.join(self.case_dir, f"{name}_{op}.png")
                    result = StyleProcessor.apply(flat_path, out_path, op)
                    self.assertTrue(os.path.isfile(result))
                    with Image.open(result) as out:
                        out.load()
                        self.assertEqual(out.size, self.src_size)
                        self.assertEqual(out.mode, "RGB")

    def test_non_rgb_input_modes_are_normalized(self):
        variants = {
            "rgba": Image.new("RGBA", self.src_size, (200, 40, 90, 128)),
            "palette": Image.open(self.src_path).convert("P"),
            "gray": Image.open(self.src_path).convert("L"),
        }
        for tag, image in variants.items():
            in_path = os.path.join(self.case_dir, f"input_{tag}.png")
            image.save(in_path)
            for op in StyleProcessor.available_ops():
                with self.subTest(input=tag, op=op):
                    out_path = os.path.join(self.case_dir, f"{tag}_{op}.png")
                    result = StyleProcessor.apply(in_path, out_path, op)
                    self.assertTrue(os.path.isfile(result))
                    with Image.open(result) as out:
                        out.load()
                        self.assertEqual(out.size, self.src_size)
                        self.assertEqual(out.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
