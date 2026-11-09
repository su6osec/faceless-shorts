import os
import unittest
import wave
from faceless_shorts.audio import SoundEngine

class TestAudio(unittest.TestCase):
    def setUp(self):
        self.engine = SoundEngine()
        self.test_wav_path = "tests/temp_test_audio.wav"
        self.test_whoosh_path = "tests/temp_whoosh.wav"
        self.test_trans_path = "tests/temp_trans.wav"

    def tearDown(self):
        for p in [self.test_wav_path, self.test_whoosh_path, self.test_trans_path]:
            if os.path.exists(p):
                os.remove(p)

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

    def test_sub_bass_808(self):
        out = self.engine.generate_tension_drone(
            output_path=self.test_wav_path,
            duration_sec=1.5,
            preset="sub_bass_808"
        )
        self.assertTrue(os.path.exists(out))
        with wave.open(out, "r") as wav:
            self.assertEqual(wav.getnchannels(), 2)
            self.assertEqual(wav.getnframes(), int(44100 * 1.5))

    def test_whoosh_synthesis(self):
        out = self.engine.generate_whoosh(
            output_path=self.test_whoosh_path,
            duration_sec=0.45
        )
        self.assertTrue(os.path.exists(out))
        with wave.open(out, "r") as wav:
            self.assertEqual(wav.getnchannels(), 2)
            self.assertEqual(wav.getnframes(), int(44100 * 0.45))

    def test_transition_track(self):
        out = self.engine.generate_transition_track(
            output_path=self.test_trans_path,
            total_duration=5.0,
            transition_times=[2.0, 4.0]
        )
        self.assertTrue(os.path.exists(out))
        with wave.open(out, "r") as wav:
            self.assertEqual(wav.getnchannels(), 2)
            self.assertEqual(wav.getnframes(), 44100 * 5)

if __name__ == "__main__":
    unittest.main()
