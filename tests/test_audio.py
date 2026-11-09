import os
import unittest
import wave
from faceless_shorts.audio import SoundEngine

class TestAudio(unittest.TestCase):
    def setUp(self):
        self.engine = SoundEngine()
        self.test_wav_path = "tests/temp_test_audio.wav"

    def tearDown(self):
        if os.path.exists(self.test_wav_path):
            os.remove(self.test_wav_path)

    def test_drone_synthesis(self):
        out = self.engine.generate_tension_drone(
            output_path=self.test_wav_path,
            duration_sec=2.0,
            preset="dark_tension"
        )
        self.assertTrue(os.path.exists(out))
        with wave.open(out, "r") as wav:
            self.assertEqual(wav.getnchannels(), 2)
            self.assertEqual(wav.getsampwidth(), 2)
            self.assertEqual(wav.getframerate(), 44100)
            self.assertEqual(wav.getnframes(), 44100 * 2)

if __name__ == "__main__":
    unittest.main()
