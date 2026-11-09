import os
import unittest
from faceless_shorts.config import TRANSITIONS, LANGUAGES, PROGRESS_BAR_CONFIG
from faceless_shorts.renderer import VideoRenderer
from faceless_shorts.script_generator import get_template

class TestRendererConfig(unittest.TestCase):
    def test_renderer_initialization_defaults(self):
        renderer = VideoRenderer()
        self.assertEqual(renderer.voice, "christopher")
        self.assertEqual(renderer.language, "en")
        self.assertEqual(renderer.transition, "flash")
        self.assertTrue(renderer.progress_bar)

    def test_renderer_hindi_voice_routing(self):
        renderer = VideoRenderer(language="hi")
        self.assertEqual(renderer.voice, "madhur")
        self.assertEqual(renderer.language, "hi")

    def test_renderer_spanish_voice_routing(self):
        renderer = VideoRenderer(language="es")
        self.assertEqual(renderer.voice, "alvaro")
        self.assertEqual(renderer.language, "es")

    def test_transition_configs(self):
        self.assertIn("flash", TRANSITIONS)
        self.assertIn("crossfade", TRANSITIONS)
        self.assertIn("slide", TRANSITIONS)
        self.assertIn("wipe", TRANSITIONS)
        self.assertIn("cut", TRANSITIONS)

    def test_progress_bar_colors(self):
        self.assertIn("hormozi", PROGRESS_BAR_CONFIG["colors_by_style"])
        self.assertIn("beast_pop", PROGRESS_BAR_CONFIG["colors_by_style"])
        self.assertIn("crimson_alert", PROGRESS_BAR_CONFIG["colors_by_style"])

if __name__ == "__main__":
    unittest.main()
