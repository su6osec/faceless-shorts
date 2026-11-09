"""
Validation tests: every art-style FFmpeg grade, every transition, and every
subtitle style must actually execute on the installed FFmpeg build.
This guarantees the CLI never ships a broken style/transition choice.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from faceless_shorts.config import ART_STYLES, TRANSITIONS, SUBTITLE_STYLES, QUALITY_PROFILES
from faceless_shorts.subtitles import SubtitleGenerator
from faceless_shorts.tts_engine import WordTimestamp

HAS_FFMPEG = bool(shutil.which("ffmpeg"))


def run_ffmpeg(args, timeout=60):
    cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-y", *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class TestArtStyleFilters(unittest.TestCase):
    """Each art style's ffmpeg_filter must chain cleanly after zoompan."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fs_style_")
        self.src = os.path.join(self.tmp, "src.png")
        run_ffmpeg([
            "-f", "lavfi", "-i", "testsrc2=size=144x256:rate=15:duration=0.5",
            "-frames:v", "1", self.src,
        ])

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_every_art_style_filter_runs(self):
        failures = []
        for key, style in ART_STYLES.items():
            grade = style.get("ffmpeg_filter", "null")
            out = os.path.join(self.tmp, f"{key}.mp4")
            # Mirror the production chain: upscale -> zoompan -> grade -> yuv420p
            vf = (
                "scale=288:512:force_original_aspect_ratio=increase,crop=288:512,"
                "zoompan=z='min(zoom+0.01,1.1)':d=8:s=144x256:fps=15,"
                f"{grade},format=yuv420p"
            )
            res = run_ffmpeg(["-loop", "1", "-i", self.src, "-vf", vf,
                              "-t", "0.5", "-c:v", "libx264", "-preset", "ultrafast", out])
            if res.returncode != 0:
                failures.append(f"{key}: {res.stderr.strip()[:300]}")
        self.assertEqual(failures, [], "Broken art-style filters:\n" + "\n".join(failures))

    def test_every_pixel_op_exists(self):
        from faceless_shorts.style_processor import StyleProcessor
        ops = set(StyleProcessor.available_ops())
        for key, style in ART_STYLES.items():
            op = style.get("pixel_op")
            if op:
                self.assertIn(op, ops, f"art style '{key}' references unknown pixel_op '{op}'")

    def test_art_styles_have_required_fields_and_categories(self):
        from faceless_shorts.config import ART_STYLE_CATEGORIES
        seen_categories = set()
        for key, style in ART_STYLES.items():
            for field in ("name", "description", "prompt_suffix", "ffmpeg_filter", "category"):
                self.assertIn(field, style, f"art style '{key}' missing '{field}'")
            self.assertIn(style["category"], ART_STYLE_CATEGORIES,
                          f"art style '{key}' has unknown category '{style['category']}'")
            seen_categories.add(style["category"])
        # Every registered category must be populated
        self.assertEqual(seen_categories, set(ART_STYLE_CATEGORIES))


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class TestTransitions(unittest.TestCase):
    """Every transition's xfade name must exist in this FFmpeg build."""

    def test_every_transition_xfade_runs(self):
        tmp = tempfile.mkdtemp(prefix="fs_xfade_")
        try:
            a = os.path.join(tmp, "a.mp4")
            b = os.path.join(tmp, "b.mp4")
            for p in (a, b):
                run_ffmpeg(["-f", "lavfi", "-i", "testsrc2=size=144x256:rate=15:duration=1",
                            "-c:v", "libx264", "-preset", "ultrafast", p])
            failures = []
            for key, t in TRANSITIONS.items():
                xname = t.get("xfade_name")
                if not xname:
                    continue  # 'cut' has no xfade
                out = os.path.join(tmp, f"{key}.mp4")
                res = run_ffmpeg([
                    "-i", a, "-i", b,
                    "-filter_complex",
                    f"[0:v][1:v]xfade=transition={xname}:duration=0.2:offset=0.6[v]",
                    "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast", out,
                ])
                if res.returncode != 0:
                    failures.append(f"{key} ({xname}): {res.stderr.strip()[:300]}")
            self.assertEqual(failures, [], "Broken transitions:\n" + "\n".join(failures))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_transition_durations_are_sane(self):
        for key, t in TRANSITIONS.items():
            self.assertGreaterEqual(t["duration"], 0, key)
            self.assertLessEqual(t["duration"], 1.0, f"{key} transition too long for Shorts")
            self.assertTrue(t["name"] and t["description"], key)


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class TestSubtitleStyles(unittest.TestCase):
    """Every subtitle style must generate a valid ASS file burnable by libass."""

    def test_every_subtitle_style_burns(self):
        tmp = tempfile.mkdtemp(prefix="fs_ass_")
        try:
            bg = os.path.join(tmp, "bg.mp4")
            res = run_ffmpeg(["-f", "lavfi", "-i", "color=c=0x101018:size=144x256:rate=15:duration=1",
                              "-c:v", "libx264", "-preset", "ultrafast", bg])
            self.assertEqual(res.returncode, 0, f"bg clip creation failed: {res.stderr[:200]}")
            words = [
                WordTimestamp("black", 0.1, 0.4, 0.3),
                WordTimestamp("hole", 0.4, 0.7, 0.3),
                WordTimestamp("devours", 0.7, 1.1, 0.4),
                WordTimestamp("light", 1.1, 1.5, 0.4),
            ]
            failures = []
            for key in SUBTITLE_STYLES:
                ass = os.path.join(tmp, f"{key}.ass")
                SubtitleGenerator(style_name=key, language="en").generate_ass_script(
                    words=words, output_ass_path=ass)
                self.assertTrue(os.path.exists(ass), f"{key}: ASS file not written")
                out = os.path.join(tmp, f"{key}.mp4")
                res = run_ffmpeg(["-i", bg, "-vf", f"ass={ass}", "-c:v", "libx264",
                                  "-preset", "ultrafast", out])
                if res.returncode != 0:
                    failures.append(f"{key}: {res.stderr.strip()[:300]}")
            self.assertEqual(failures, [], "Broken subtitle styles:\n" + "\n".join(failures))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_glow_styles_declare_numeric_blur(self):
        for key, style in SUBTITLE_STYLES.items():
            if "glow_blur" in style:
                self.assertIsInstance(style["glow_blur"], int, key)
                self.assertGreater(style["glow_blur"], 0, key)


class TestQualityProfiles(unittest.TestCase):
    def test_quality_profiles_complete(self):
        for key, q in QUALITY_PROFILES.items():
            for field in ("fps", "crf", "preset", "audio_bitrate", "width", "height"):
                self.assertIn(field, q, f"quality '{key}' missing '{field}'")
            self.assertIn(q["fps"], (24, 30, 60), key)
            self.assertTrue(0 < q["crf"] < 51, key)
            self.assertEqual(q["width"] % 2, 0, key)
            self.assertEqual(q["height"] % 2, 0, key)


if __name__ == "__main__":
    unittest.main()
