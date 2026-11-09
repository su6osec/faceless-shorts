import os
import unittest
from faceless_shorts.tts_engine import TTSEngine

class TestTTSEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TTSEngine()
        self.test_audio_path = "tests/temp_test_tts.mp3"

    def tearDown(self):
        if os.path.exists(self.test_audio_path):
            os.remove(self.test_audio_path)

    def test_voice_resolution(self):
        self.assertEqual(self.engine._resolve_voice("christopher"), "en-US-ChristopherNeural")
        self.assertEqual(self.engine._resolve_voice("guy"), "en-US-GuyNeural")
        self.assertEqual(self.engine._resolve_voice("custom-voice"), "custom-voice")

    def test_synthesis_and_words(self):
        res = self.engine.synthesize("Master your mind.", self.test_audio_path, voice="christopher")
        self.assertTrue(os.path.exists(self.test_audio_path))
        self.assertTrue(os.path.getsize(self.test_audio_path) > 1000)
        self.assertTrue(res.duration_sec > 0.5)
        self.assertTrue(len(res.words) >= 3)
        self.assertEqual(res.words[0].word.lower(), "master")

if __name__ == "__main__":
    unittest.main()
