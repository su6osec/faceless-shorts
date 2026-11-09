import os
import unittest
from faceless_shorts.subtitles import SubtitleGenerator, format_ass_time
from faceless_shorts.tts_engine import WordTimestamp

class TestSubtitles(unittest.TestCase):
    def setUp(self):
        self.sub_gen = SubtitleGenerator(style_name="hormozi")
        self.test_ass_path = "tests/temp_test.ass"

    def tearDown(self):
        if os.path.exists(self.test_ass_path):
            os.remove(self.test_ass_path)

    def test_format_ass_time(self):
        self.assertEqual(format_ass_time(0.0), "0:00:00.00")
        self.assertEqual(format_ass_time(65.45), "0:01:05.45")
        self.assertEqual(format_ass_time(3600.0), "1:00:00.00")

    def test_ass_script_generation(self):
        words = [
            WordTimestamp(word="Your", start_sec=0.1, end_sec=0.4, duration_sec=0.3),
            WordTimestamp(word="brain", start_sec=0.4, end_sec=0.9, duration_sec=0.5),
            WordTimestamp(word="decides", start_sec=0.9, end_sec=1.4, duration_sec=0.5),
        ]
        self.sub_gen.generate_ass_script(words, self.test_ass_path)
        self.assertTrue(os.path.exists(self.test_ass_path))
        
        with open(self.test_ass_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        self.assertIn("[Script Info]", content)
        self.assertIn("[V4+ Styles]", content)
        self.assertIn("Style: Main", content)
        self.assertIn("BRAIN", content)
        # Check scale bounce popping tag
        self.assertIn("\\fscx118\\fscy118", content)

    def test_hindi_language_font(self):
        hi_gen = SubtitleGenerator(style_name="hormozi", language="hi")
        self.assertEqual(hi_gen.style_config["font_name"], "Kohinoor Devanagari")
        self.assertFalse(hi_gen.uppercase)

if __name__ == "__main__":
    unittest.main()
