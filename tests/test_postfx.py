"""
Tests for faceless_shorts.postfx — the composable FFmpeg FX builder.

Run with:  python -m unittest tests.test_postfx -v
"""

import shutil
import subprocess
import unittest

from faceless_shorts.postfx import PostFX

# The full effect roster, mirrored here so a dropped effect fails loudly.
ALL_EFFECTS = [
    "bloom",
    "halation",
    "chroma",
    "grain",
    "vignette",
    "sharpen",
    "punch",
    "teal_orange",
    "dreamy",
    "motion_blur",
    "vhs",
    "vivid",
    "anamorphic",
    "noir",
    "night",
]

ALL_PACKS = ["clean", "cinematic", "premium", "dreamy", "retro", "nofx"]

FFMPEG = shutil.which("ffmpeg")

# Small vertical source so every validation run is fast (270x480, 1s @30fps).
TEST_SRC = "testsrc2=size=270x480:rate=30:duration=1"


class TestPostFXAPI(unittest.TestCase):
    """(a) available() / describe() / ValueError / null / packs / dedupe."""

    def test_available_lists_every_effect(self):
        available = PostFX.available()
        self.assertIsInstance(available, list)
        for name in ALL_EFFECTS:
            self.assertIn(name, available)
        self.assertEqual(len(available), len(set(available)), "duplicates in available()")
        self.assertGreaterEqual(len(available), 15)

    def test_describe_is_non_empty_for_all_names(self):
        for name in PostFX.available() + list(PostFX.PACKS) + ["none", "nofx"]:
            with self.subTest(name=name):
                text = PostFX.describe(name)
                self.assertIsInstance(text, str)
                self.assertTrue(text.strip(), f"empty description for {name!r}")

    def test_unknown_effect_raises_value_error_listing_valid_names(self):
        with self.assertRaises(ValueError) as ctx:
            PostFX.build("bloom,definitely_not_a_real_effect")
        message = str(ctx.exception)
        self.assertIn("definitely_not_a_real_effect", message)
        # The message must list valid names (effects and packs alike).
        self.assertIn("halation", message)
        self.assertIn("cinematic", message)

    def test_unknown_effect_in_describe_raises(self):
        with self.assertRaises(ValueError) as ctx:
            PostFX.describe("nope_not_here")
        self.assertIn("nope_not_here", str(ctx.exception))

    def test_empty_and_none_build_null_passthrough(self):
        for effects in ("", "   ", [], "none", ["none"], "nofx", "none,none", ["clean"], "clean,nofx"):
            with self.subTest(effects=effects):
                self.assertEqual(PostFX.build(effects), "[0:v]null[vout]")

    def test_pack_expansion_order(self):
        cases = {
            "cinematic": ["bloom", "halation", "teal_orange", "grain", "vignette"],
            "premium": ["bloom", "chroma", "punch", "sharpen", "grain", "vignette"],
            "retro": ["vhs", "grain", "chroma", "vignette"],
        }
        for pack, members in cases.items():
            with self.subTest(pack=pack):
                self.assertEqual(PostFX.build(pack), PostFX.build(members))

        # The 'dreamy' pack name is ambiguous with the effect of the same
        # name and resolves to the effect (asserted separately); its member
        # list must still build as the full bundle.
        self.assertEqual(
            PostFX.build(PostFX.PACKS["dreamy"]),
            PostFX.build(["dreamy", "bloom", "vignette"]),
        )

    def test_all_packs_declare_valid_effect_names(self):
        valid = set(PostFX.available())
        for pack, members in PostFX.PACKS.items():
            with self.subTest(pack=pack):
                self.assertIsInstance(members, list)
                for member in members:
                    self.assertIn(member, valid)

    def test_dedupe_preserves_order(self):
        body = PostFX.build("vignette,vignette")
        self.assertEqual(body.count("vignette="), 1)

        # "bloom" appears both directly and inside the "premium" pack.
        body = PostFX.build(["bloom", "premium"])
        self.assertEqual(body.count("split=2"), 1)
        self.assertEqual(body.count("vignette="), 1)
        self.assertLess(body.index("gblur=sigma=18"), body.index("rgbashift=rh=3"))

    def test_pack_and_effects_mix_order(self):
        # vignette first, retro expands after it, trailing vignette deduped.
        body = PostFX.build(["vignette", "retro", "vignette"])
        self.assertEqual(body.count("vignette="), 1)
        self.assertLess(body.index("vignette="), body.index("rgbashift=rh=4"))
        self.assertLess(body.index("rgbashift=rh=4"), body.index("noise=alls=7"))
        self.assertLess(body.index("noise=alls=7"), body.index("rgbashift=rh=3"))

    def test_dreamy_name_resolves_to_effect_not_pack(self):
        effect_body = PostFX.build("dreamy")
        self.assertIn("gblur=sigma=9", effect_body)
        self.assertNotIn("gblur=sigma=18", effect_body)
        # ...while the pack is still reachable as an explicit member list.
        pack_body = PostFX.build(PostFX.PACKS["dreamy"])
        self.assertIn("gblur=sigma=18", pack_body)
        self.assertIn("vignette=", pack_body)

    def test_custom_labels(self):
        body = PostFX.build("bloom", input_label="0:v", output_label="final")
        self.assertTrue(body.startswith("[0:v]"))
        self.assertTrue(body.endswith("[final]"))
        self.assertNotIn("[vout]", body)

        # Brackets around labels are tolerated.
        self.assertEqual(
            PostFX.build("punch", input_label="[0:v]", output_label="[vout]"),
            PostFX.build("punch"),
        )

        with self.assertRaises(ValueError):
            PostFX.build("punch", output_label="")

    def test_geometry_and_duration_validation(self):
        with self.assertRaises(ValueError):
            PostFX.build("bloom", width=-5)
        with self.assertRaises(ValueError):
            PostFX.build("bloom", height="1080")
        with self.assertRaises(ValueError):
            PostFX.build("bloom", duration=0)

        # width feeds the anamorphic streak length.
        self.assertIn("gblur=sigma=70", PostFX.build("anamorphic"))
        self.assertIn("gblur=sigma=125", PostFX.build("anamorphic", width=1920))

    def test_build_accepts_comma_string_and_sequence_alike(self):
        self.assertEqual(PostFX.build("bloom,grain"), PostFX.build(["bloom", "grain"]))


class TestPostFXGraphStructure(unittest.TestCase):
    """(c) build() output shape: labels, segments, no double semicolons."""

    @staticmethod
    def _sample_bodies():
        yield "empty", PostFX.build("")
        for name in PostFX.available():
            yield name, PostFX.build([name])
        for pack in PostFX.PACKS:
            yield f"pack:{pack}", PostFX.build(PostFX.PACKS[pack])
        yield "all-effects", PostFX.build(PostFX.available())
        yield "mixed", PostFX.build("retro,punch,none")
        yield "geometry", PostFX.build("anamorphic,bloom", width=1080, height=1920, duration=5.0)

    def test_output_label_and_segment_well_formedness(self):
        for label, body in self._sample_bodies():
            with self.subTest(body=label):
                self.assertIsInstance(body, str)
                # Output label present as the final label.
                self.assertIn("[vout]", body)
                self.assertTrue(body.endswith("[vout]"), body)
                self.assertTrue(body.startswith("[0:v]"), body)
                # No empty segments, no double/leading/trailing semicolons.
                self.assertNotIn(";;", body)
                self.assertFalse(body.startswith(";"))
                self.assertFalse(body.endswith(";"))
                segments = body.split(";")
                for segment in segments:
                    self.assertTrue(segment.strip(), f"empty segment in {body}")
                    self.assertTrue(segment.startswith("["), f"bad segment {segment!r}")
                    self.assertTrue(segment.endswith("]"), f"bad segment {segment!r}")

    def test_every_effect_body_emits_its_key_filter(self):
        keys = {
            "bloom": "gblur=sigma=18",
            "halation": "lutyuv",
            "chroma": "rgbashift=rh=3",
            "grain": "noise=alls=7",
            "vignette": "vignette=PI/4.6",
            "sharpen": "unsharp=",
            "punch": "eq=contrast=1.12",
            "teal_orange": "colorbalance=",
            "dreamy": "gblur=sigma=9",
            "motion_blur": "tmix=frames=4",
            "vhs": "rgbashift=rh=4",
            "vivid": "eq=gamma=1.07",
            "anamorphic": "sigmaV=0",
            "noir": "contrast=1.35",
            "night": "colorchannelmixer=gg=1.35",
        }
        self.assertEqual(sorted(keys), sorted(PostFX.available()))
        for name, needle in keys.items():
            with self.subTest(effect=name):
                self.assertIn(needle, PostFX.build([name]))


@unittest.skipUnless(FFMPEG, "ffmpeg executable not found on PATH")
class TestPostFXFFmpegValidation(unittest.TestCase):
    """(b) Run every body through real FFmpeg and require exit code 0."""

    def _assert_valid(self, body: str, label: str) -> None:
        proc = subprocess.run(
            [
                FFMPEG,
                "-hide_banner",
                "-v", "error",
                "-f", "lavfi",
                "-i", TEST_SRC,
                "-filter_complex", body,
                "-map", "[vout]",
                "-frames:v", "10",
                "-f", "null",
                "-",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"ffmpeg rejected {label} (rc={proc.returncode})\n"
            f"body: {body}\nstderr: {proc.stderr}",
        )

    def test_every_effect_validates(self):
        for name in PostFX.available():
            with self.subTest(effect=name):
                self._assert_valid(PostFX.build([name]), f"effect {name}")

    def test_every_pack_validates(self):
        for pack in PostFX.PACKS:
            with self.subTest(pack=pack):
                # Built from the member list: the "dreamy" pack name itself
                # resolves to the same-named effect (documented precedence).
                self._assert_valid(PostFX.build(PostFX.PACKS[pack]), f"pack {pack}")

    def test_pack_names_resolve_through_build(self):
        for pack in ALL_PACKS:
            if pack == "dreamy":
                continue  # ambiguous with the effect of the same name
            with self.subTest(pack=pack):
                self.assertEqual(PostFX.build(pack), PostFX.build(PostFX.PACKS[pack]))
                self._assert_valid(PostFX.build(pack), f"pack name {pack}")

    def test_all_effects_chain_validates(self):
        body = PostFX.build(PostFX.available())
        self._assert_valid(body, "all-effects chain")

    def test_mixed_pack_and_effects_chain_validates(self):
        body = PostFX.build("retro,punch,none", width=1080, height=1920, duration=1.0)
        self._assert_valid(body, "mixed retro+punch chain")


if __name__ == "__main__":
    unittest.main()
