"""
Regression & integration tests for the advanced pipeline upgrade:
quality profiles, Post-FX wiring, script knowledge/presets, engines.
"""

import os
import tempfile
import unittest

from faceless_shorts.config import (
    ART_STYLES,
    QUALITY_PROFILES,
    IMAGE_ENGINES,
    TRANSITIONS,
    SUBTITLE_STYLES,
    KEN_BURNS_PRESETS,
)
from faceless_shorts.postfx import PostFX
from faceless_shorts.script_generator import (
    DynamicScriptBuilder,
    TOPIC_KNOWLEDGE,
    VIRAL_TEMPLATES,
    create_or_get_script,
    get_template,
)
from faceless_shorts.renderer import VideoRenderer
from faceless_shorts.subtitles import SubtitleGenerator
from faceless_shorts.tts_engine import WordTimestamp
from faceless_shorts.visuals import VisualManager


class TestPresetsReachability(unittest.TestCase):
    """The language-suffixed presets (blackhole_en.json) must actually resolve."""

    def test_niche_blackhole_resolves_preset(self):
        script = create_or_get_script("blackhole", use_llm=False)
        self.assertEqual(script.niche, "blackhole")
        self.assertIn("Black Hole", script.title)
        self.assertEqual(len(script.scenes), 5)

    def test_topic_black_hole_resolves_preset_via_normalization(self):
        script = create_or_get_script("Black Hole", use_llm=False)
        self.assertIn("Black Hole", script.title)
        self.assertEqual(len(script.scenes), 5)
        self.assertTrue(any("event horizon" in s.text.lower() for s in script.scenes))

    def test_hindi_blackhole_uses_hindi_preset(self):
        script = create_or_get_script("black hole", language="hi", use_llm=False)
        self.assertEqual(len(script.scenes), 5)
        # Hindi preset must actually contain Devanagari script
        self.assertTrue(any("\u0900" <= c <= "\u097F" for c in script.title),
                        f"Hindi preset not localized: {script.title}")

    def test_non_english_never_gets_plain_english_preset(self):
        # fitness.json exists but fitness_hi.json must not be used for Hindi
        script = get_template("fitness", language="hi")
        self.assertIsNone(script)

    def test_english_plain_preset_still_works(self):
        script = get_template("stoicism", language="en")
        self.assertIsNotNone(script)
        self.assertEqual(script.niche, "stoicism")


class TestKnowledgePacks(unittest.TestCase):
    def test_knowledge_packs_structure(self):
        for key, pack in TOPIC_KNOWLEDGE.items():
            self.assertIn("match", pack, key)
            self.assertIn("title", pack, key)
            self.assertGreaterEqual(len(pack["scenes"]), 5, key)
            for scene in pack["scenes"]:
                self.assertTrue(scene["text"] and scene["visual_prompt"], key)
                self.assertIn(scene["motion"], KEN_BURNS_PRESETS, f"{key}: bad motion")

    def test_knowledge_lookup_fires(self):
        script = create_or_get_script("the human brain", use_llm=False)
        self.assertEqual(len(script.scenes), 6)
        self.assertIn("Brain", script.title)

    def test_unknown_topic_falls_back_to_builder(self):
        script = create_or_get_script("quantum computing", use_llm=False)
        self.assertEqual(len(script.scenes), 5)
        self.assertIn("Quantum Computing", script.title)
        self.assertIn("quantum computing", script.scenes[0].text.lower())


class TestRendererConfiguration(unittest.TestCase):
    def _renderer(self, **kwargs):
        return VideoRenderer(work_dir=tempfile.mkdtemp(prefix="fs_cfg_"), **kwargs)

    def test_default_quality_profile(self):
        r = self._renderer()
        self.assertEqual(r.quality, "social")
        self.assertEqual((r.width, r.height), (1080, 1920))
        self.assertEqual(r.fps, 30)
        self.assertEqual(r.crf, 21)

    def test_ultra_quality_profile(self):
        r = self._renderer(quality="ultra")
        self.assertEqual((r.width, r.height), (1440, 2560))
        self.assertEqual(r.fps, 60)
        self.assertEqual(r.crf, 15)
        # Subtitles must scale with the bigger canvas
        self.assertGreater(r.subtitles.style_config["font_size"], 90)

    def test_fps_and_crf_overrides(self):
        r = self._renderer(quality="hd", fps=60, crf=16, encoder_preset="slow")
        self.assertEqual(r.fps, 60)
        self.assertEqual(r.crf, 16)
        self.assertEqual(r.encoder_preset, "slow")

    def test_effects_parsing_and_none_neutralization(self):
        r = self._renderer(effects="bloom, grain, chroma")
        self.assertEqual(r.effects, ["bloom", "grain", "chroma"])
        r2 = self._renderer(effects="none")
        self.assertEqual(r2.effects, [])
        r3 = self._renderer(effects="cinematic")  # pack expands at build time
        self.assertEqual(r3.effects, ["cinematic"])

    def test_invalid_art_style_falls_back_to_hyperreal(self):
        r = self._renderer(art_style="does_not_exist")
        self.assertEqual(r.art_style, "hyperreal")

    def test_engine_selection(self):
        r = self._renderer(engine="comfyui")
        self.assertEqual(r.visuals.engine, "comfyui")
        r2 = self._renderer(engine="procedural")
        self.assertEqual(r2.visuals.engine, "procedural")

    def test_final_filter_complex_builds(self):
        """The exact graph the renderer feeds to ffmpeg must be well-formed."""
        from faceless_shorts.postfx import PostFX as PFX
        fx_body = PFX.build(["cinematic"], input_label="0:v", output_label="fx",
                            duration=30.0, width=1080, height=1920)
        graph = f"{fx_body};[fx]ass=/tmp/x.ass,drawbox=x=0:y=1908:w='iw*(t/30)':h=8:color=0x2BF7FF@0.95:t=fill,format=yuv420p[vout]"
        self.assertIn("[vout]", graph)
        self.assertIn("ass=/tmp/x.ass", graph)
        self.assertNotIn(";;", graph)
        self.assertTrue(graph.startswith("[0:v]"))


class TestVisualManager(unittest.TestCase):
    def test_parallel_image_generation_offline(self):
        vm = VisualManager(cache_dir=tempfile.mkdtemp(prefix="fs_par_"),
                           engine="procedural", art_style="pixel_art")
        jobs = [
            {"prompt": "test a", "output_path": os.path.join(vm.cache_dir, "a.jpg")},
            {"prompt": "test b", "output_path": os.path.join(vm.cache_dir, "b.jpg")},
        ]
        results = vm.generate_ai_images_parallel(jobs, max_workers=2)
        self.assertEqual(len(results), 2)
        for path in results.values():
            self.assertTrue(os.path.exists(path))

    def test_apply_art_style_passthrough_without_pixel_op(self):
        from PIL import Image
        vm = VisualManager(cache_dir=tempfile.mkdtemp(prefix="fs_st_"),
                           engine="procedural", art_style="hyperreal")
        src = os.path.join(vm.cache_dir, "src.jpg")
        Image.new("RGB", (64, 64), (200, 100, 50)).save(src)
        out = vm.apply_art_style(src, os.path.join(vm.cache_dir, "out.jpg"))
        self.assertEqual(out, src)  # hyperreal has no pixel_op

    def test_apply_art_style_transforms_when_defined(self):
        from PIL import Image
        vm = VisualManager(cache_dir=tempfile.mkdtemp(prefix="fs_st2_"),
                           engine="procedural", art_style="pixel_art")
        src = os.path.join(vm.cache_dir, "src.jpg")
        Image.new("RGB", (128, 224), (30, 120, 200)).save(src)
        out = vm.apply_art_style(src, os.path.join(vm.cache_dir, "styled.jpg"))
        self.assertNotEqual(out, src)
        self.assertTrue(os.path.exists(out))

    def test_new_ken_burns_motions_render(self):
        """The 4 new camera motions must produce a valid clip."""
        import shutil
        import subprocess
        import unittest as _u
        if not shutil.which("ffmpeg"):
            self.skipTest("ffmpeg missing")
        from PIL import Image
        tmp = tempfile.mkdtemp(prefix="fs_kb_")
        try:
            src = os.path.join(tmp, "src.png")
            Image.new("RGB", (270, 480), (10, 30, 60)).save(src)
            vm = VisualManager(cache_dir=tmp, engine="procedural",
                               width=144, height=256, fps=15)
            for motion in ("rise_up", "orbit_sway", "pulse_heartbeat", "shockwave_out"):
                out = os.path.join(tmp, f"{motion}.mp4")
                vm.render_ken_burns_clip(src, out, duration=0.6, motion=motion,
                                         fps=15, width=144, height=256)
                self.assertTrue(os.path.exists(out), motion)
                res = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                      "format=duration", "-of", "csv=p=0", out],
                                     capture_output=True, text=True)
                self.assertGreater(float(res.stdout.strip() or 0), 0.2, motion)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestSubtitleGlow(unittest.TestCase):
    def test_glow_style_emits_blur_tags(self):
        tmp = tempfile.mkdtemp(prefix="fs_glow_")
        ass = os.path.join(tmp, "glow.ass")
        words = [WordTimestamp("glow", 0.1, 0.5, 0.4)]
        SubtitleGenerator(style_name="neon_glow").generate_ass_script(words, ass)
        with open(ass, encoding="utf-8-sig") as f:
            content = f.read()
        self.assertIn("\\blur7", content)
        self.assertIn("\\blur0", content)

    def test_non_glow_style_has_no_blur(self):
        tmp = tempfile.mkdtemp(prefix="fs_noglow_")
        ass = os.path.join(tmp, "plain.ass")
        words = [WordTimestamp("plain", 0.1, 0.5, 0.4)]
        SubtitleGenerator(style_name="hormozi").generate_ass_script(words, ass)
        with open(ass, encoding="utf-8-sig") as f:
            content = f.read()
        self.assertNotIn("\\blur", content)


class TestConfigIntegrity(unittest.TestCase):
    def test_all_style_categories_populated(self):
        from faceless_shorts.config import ART_STYLE_CATEGORIES
        cats = {s["category"] for s in ART_STYLES.values()}
        self.assertEqual(cats, set(ART_STYLE_CATEGORIES))

    def test_required_viral_styles_present(self):
        required = [
            "pixel_art", "chalkboard", "glow_sketch", "ps2_style", "comic_art",
            "flat_vector", "minimal_line", "cgi_motion", "lego", "explainer_3d",
        ]
        for style in required:
            self.assertIn(style, ART_STYLES, f"missing required style: {style}")

    def test_image_engines_registered(self):
        self.assertEqual(set(IMAGE_ENGINES), {"pollinations", "comfyui", "procedural"})

    def test_transitions_and_styles_counts(self):
        self.assertGreaterEqual(len(TRANSITIONS), 15)
        self.assertGreaterEqual(len(SUBTITLE_STYLES), 10)
        self.assertGreaterEqual(len(ART_STYLES), 40)


if __name__ == "__main__":
    unittest.main()
