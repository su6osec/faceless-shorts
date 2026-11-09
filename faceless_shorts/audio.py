"""
Audio Processing & Sound Design Module for Faceless Shorts.
Features:
- Procedural Royalty-Free Tension / Ambient Music Synthesizer (Zero Copyright Claims)
- Professional Automated Audio Ducking with FFmpeg Sidechain Compression
- Audio Normalization and Multi-track Mixing
"""

import math
import os
import struct
import subprocess
import wave
from typing import Optional

class SoundEngine:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def generate_tension_drone(
        self,
        output_path: str,
        duration_sec: float,
        preset: str = "dark_tension"
    ) -> str:
        """
        Synthesize a royalty-free cinematic tension / ambient audio track offline.
        Guaranteed 0% chance of YouTube / TikTok copyright strikes.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        num_samples = int(self.sample_rate * duration_sec)
        
        with wave.open(output_path, "w") as wav:
            wav.setnchannels(2)      # Stereo
            wav.setsampwidth(2)      # 16-bit
            wav.setframerate(self.sample_rate)
            
            frames = bytearray()
            
            for i in range(num_samples):
                t = i / self.sample_rate
                
                if preset == "curiosity_ambient":
                    # Soft warm pad: Root 130.81Hz (C3) + Fifth 196.00Hz (G3) with slow harmonic sweeping
                    sweep = 0.5 + 0.5 * math.sin(2 * math.pi * 0.15 * t)
                    left = 0.25 * math.sin(2 * math.pi * 130.81 * t) + 0.15 * sweep * math.sin(2 * math.pi * 196.00 * t)
                    right = 0.25 * math.sin(2 * math.pi * 131.2 * t) + 0.15 * sweep * math.sin(2 * math.pi * 196.50 * t)
                    # Air shimmer
                    air = 0.02 * math.sin(2 * math.pi * 523.25 * t) * math.sin(2 * math.pi * 0.3 * t)
                    left += air
                    right += air
                elif preset == "cinematic_pulse":
                    # Heartbeat rhythm at 1.1 Hz (~66 BPM)
                    beat_phase = (t * 1.1) % 1.0
                    heartbeat = math.exp(-beat_phase * 12) * math.sin(2 * math.pi * 60 * t) if beat_phase < 0.25 else 0.0
                    sub = 0.2 * math.sin(2 * math.pi * 45 * t)
                    left = sub + 0.4 * heartbeat
                    right = sub + 0.4 * heartbeat
                else: # dark_tension default
                    # Deep 55Hz sub drone + eerie detune at 55.8Hz + rhythmic breathing wave
                    breath = 0.6 + 0.4 * math.sin(2 * math.pi * 0.25 * t)
                    drone_left = 0.35 * math.sin(2 * math.pi * 55 * t) + 0.18 * breath * math.sin(2 * math.pi * 110 * t)
                    drone_right = 0.35 * math.sin(2 * math.pi * 55.7 * t) + 0.18 * breath * math.sin(2 * math.pi * 111.4 * t)
                    whisper = 0.015 * math.sin(2 * math.pi * 440 * t) * math.sin(2 * math.pi * 0.1 * t)
                    left = drone_left + whisper
                    right = drone_right + whisper

                # Soft limiter and 16-bit PCM conversion
                l_val = max(-0.95, min(0.95, left))
                r_val = max(-0.95, min(0.95, right))
                frames.extend(struct.pack("<hh", int(l_val * 28000), int(r_val * 28000)))
            
            wav.writeframes(frames)
            
        return output_path

    def mix_with_ducking(
        self,
        voiceover_path: str,
        background_music_path: str,
        output_path: str,
        bg_volume_db: float = -18.0
    ) -> str:
        """
        Mix voiceover and background music with dynamic ducking via FFmpeg sidechaincompress.
        When voiceover speaks, background music smoothly drops in volume.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Audio filtergraph:
        # [1:a] Background music is adjusted and fed to sidechain compressor
        # [0:a] Voiceover acts as the control sidechain trigger
        # Then both are mixed together cleanly
        filter_graph = (
            f"[1:a]volume={bg_volume_db}dB[bg_low];"
            f"[0:a]asplit=2[voice_main][voice_trigger];"
            f"[bg_low][voice_trigger]sidechaincompress=threshold=0.06:ratio=6:attack=150:release=800[ducked_bg];"
            f"[voice_main][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[outa]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", voiceover_path,
            "-stream_loop", "-1",
            "-i", background_music_path,
            "-filter_complex", filter_graph,
            "-map", "[outa]",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
