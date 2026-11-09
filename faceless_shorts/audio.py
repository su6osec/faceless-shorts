"""
Audio Processing & Sound Design Module for Faceless Shorts.
Features:
- Procedural Royalty-Free Tension / Ambient / 808 Sub-Bass Synthesizer (Zero Copyright Claims)
- Procedural Scene Transition Whoosh SFX Engine
- Professional Automated Audio Ducking with FFmpeg Sidechain Compression
- Vocal Presence EQ & Master Loudness Normalization (-14 LUFS EBU R128 Standard)
"""

import math
import os
import random
import struct
import subprocess
import wave
from typing import List, Optional

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
                    sub = 0.28 * math.sin(2 * math.pi * 48 * t)
                    left = sub + 0.42 * heartbeat
                    right = sub + 0.42 * heartbeat
                elif preset == "sub_bass_808":
                    # Deep 808 sub-bass rumble (45Hz root + 90Hz second harmonic + 2-second dynamic drop)
                    drop_phase = (t * 0.5) % 1.0
                    drop_freq = 45.0 + 35.0 * math.exp(-drop_phase * 8)
                    drop_amp = 0.45 * math.exp(-drop_phase * 3.5)
                    sub = drop_amp * math.sin(2 * math.pi * drop_freq * t)
                    warmth = 0.12 * math.sin(2 * math.pi * 90 * t)
                    left = sub + warmth
                    right = sub + warmth
                else: # dark_tension default
                    # Deep 50Hz sub drone + eerie detune at 50.8Hz + rhythmic breathing wave
                    breath = 0.6 + 0.4 * math.sin(2 * math.pi * 0.25 * t)
                    drone_left = 0.38 * math.sin(2 * math.pi * 50 * t) + 0.18 * breath * math.sin(2 * math.pi * 100 * t)
                    drone_right = 0.38 * math.sin(2 * math.pi * 50.8 * t) + 0.18 * breath * math.sin(2 * math.pi * 101.6 * t)
                    whisper = 0.015 * math.sin(2 * math.pi * 440 * t) * math.sin(2 * math.pi * 0.1 * t)
                    left = drone_left + whisper
                    right = drone_right + whisper

                # Soft limiter and 16-bit PCM conversion
                l_val = max(-0.95, min(0.95, left))
                r_val = max(-0.95, min(0.95, right))
                frames.extend(struct.pack("<hh", int(l_val * 28000), int(r_val * 28000)))
            
            wav.writeframes(frames)
            
        return output_path

    def generate_whoosh(
        self,
        output_path: str,
        duration_sec: float = 0.45
    ) -> str:
        """
        Synthesize a crisp, cinematic transition whoosh SFX offline.
        Uses resonant frequency sweep white noise + exponential envelope + sub-bass swoosh.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        num_samples = int(self.sample_rate * duration_sec)
        
        with wave.open(output_path, "w") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            
            frames = bytearray()
            bp_y1 = bp_y2 = 0.0
            
            for i in range(num_samples):
                t = i / self.sample_rate
                p = t / duration_sec
                # Exponential bell envelope peaking at 55%
                envelope = math.exp(-((p - 0.55) ** 2) / 0.05)
                noise = (random.random() * 2.0 - 1.0)
                
                # Resonant bandpass filter sweeping from 250Hz to 2000Hz and back
                center_freq = 250 + 1750 * math.sin(math.pi * p)
                w0 = 2 * math.pi * center_freq / self.sample_rate
                alpha = math.sin(w0) * 0.45
                b0 = alpha
                b2 = -alpha
                a0 = 1 + alpha
                a1 = -2 * math.cos(w0)
                a2 = 1 - alpha
                
                filtered = (b0 / a0) * noise + bp_y1
                bp_y1 = (b2 / a0) * noise - (a1 / a0) * filtered + bp_y2
                bp_y2 = -(a2 / a0) * filtered
                
                # Dynamic sub-bass swoosh (45Hz to 90Hz sweep)
                sub_freq = 45 + 45 * math.sin(math.pi * p)
                sub = 0.4 * math.sin(2 * math.pi * sub_freq * t) * envelope
                
                combined = (filtered * 0.65 + sub) * envelope
                clamped = max(-0.95, min(0.95, combined))
                
                # Cinematic left-to-right stereo panning
                l_val = clamped * (1.0 - p * 0.5)
                r_val = clamped * (0.5 + p * 0.5)
                
                frames.extend(struct.pack("<hh", int(l_val * 24000), int(r_val * 24000)))
                
            wav.writeframes(frames)
            
        return output_path

    def generate_transition_track(
        self,
        output_path: str,
        total_duration: float,
        transition_times: List[float]
    ) -> Optional[str]:
        """
        Synthesize a master stereo sound effects track containing whoosh impacts
        at every scene transition timestamp.
        """
        if not transition_times or total_duration <= 0:
            return None
            
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        whoosh_dur = 0.45
        whoosh_samples = int(self.sample_rate * whoosh_dur)
        
        # Pre-synthesize whoosh sample buffers
        whoosh_left = []
        whoosh_right = []
        bp_y1 = bp_y2 = 0.0
        
        for i in range(whoosh_samples):
            t = i / self.sample_rate
            p = t / whoosh_dur
            envelope = math.exp(-((p - 0.55) ** 2) / 0.05)
            noise = (random.random() * 2.0 - 1.0)
            center_freq = 250 + 1750 * math.sin(math.pi * p)
            w0 = 2 * math.pi * center_freq / self.sample_rate
            alpha = math.sin(w0) * 0.45
            b0 = alpha; b2 = -alpha; a0 = 1 + alpha; a1 = -2 * math.cos(w0); a2 = 1 - alpha
            filtered = (b0 / a0) * noise + bp_y1
            bp_y1 = (b2 / a0) * noise - (a1 / a0) * filtered + bp_y2
            bp_y2 = -(a2 / a0) * filtered
            sub = 0.4 * math.sin(2 * math.pi * (45 + 45 * math.sin(math.pi * p)) * t) * envelope
            combined = (filtered * 0.65 + sub) * envelope
            clamped = max(-0.95, min(0.95, combined))
            whoosh_left.append(int(clamped * (1.0 - p * 0.5) * 24000))
            whoosh_right.append(int(clamped * (0.5 + p * 0.5) * 24000))

        total_samples = int(self.sample_rate * total_duration)
        track_left = [0] * total_samples
        track_right = [0] * total_samples

        # Stamp whoosh at each transition timestamp (whoosh peaks right at transition)
        for t_cut in transition_times:
            # Start whoosh ~0.22s before the cut point
            start_idx = max(0, int((t_cut - 0.22) * self.sample_rate))
            for k in range(whoosh_samples):
                pos = start_idx + k
                if pos < total_samples:
                    track_left[pos] = max(-32000, min(32000, track_left[pos] + whoosh_left[k]))
                    track_right[pos] = max(-32000, min(32000, track_right[pos] + whoosh_right[k]))

        with wave.open(output_path, "w") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            frames = bytearray()
            for i in range(total_samples):
                frames.extend(struct.pack("<hh", track_left[i], track_right[i]))
            wav.writeframes(frames)

        return output_path

    def mix_with_ducking(
        self,
        voiceover_path: str,
        background_music_path: str,
        output_path: str,
        bg_volume_db: float = -18.0,
        transition_sfx_path: Optional[str] = None
    ) -> str:
        """
        Mix voiceover, background music, and transition SFX with:
        - Vocal presence EQ (high-pass at 75Hz + 3.5kHz vocal boost)
        - Dynamic audio ducking via FFmpeg sidechaincompress
        - Transition whoosh sound effects integration
        - Master loudness normalization (-14 LUFS standard)
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        has_sfx = transition_sfx_path and os.path.exists(transition_sfx_path)
        
        # Audio filtergraph:
        # [0:a] Voiceover -> Highpass (75Hz) + Presence Boost (3500Hz)
        #                 -> Split into [voice_eq] and [voice_trigger]
        # [1:a] Background music -> low volume -> sidechaincompress triggered by voice
        # [2:a] Transition whoosh SFX (if provided)
        # Final mix -> loudnorm to -14 LUFS standard
        if has_sfx:
            filter_graph = (
                f"[0:a]highpass=f=75,equalizer=f=3500:t=q:w=1.2:g=2.5,asplit=2[voice_eq][voice_trigger];"
                f"[1:a]volume={bg_volume_db}dB[bg_low];"
                f"[bg_low][voice_trigger]sidechaincompress=threshold=0.06:ratio=6:attack=150:release=800[ducked_bg];"
                f"[2:a]volume=-2dB[sfx_vol];"
                f"[voice_eq][ducked_bg][sfx_vol]amix=inputs=3:duration=first:dropout_transition=2,"
                f"loudnorm=I=-14:LRA=7:TP=-1.5[outa]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-i", voiceover_path,
                "-stream_loop", "-1",
                "-i", background_music_path,
                "-i", transition_sfx_path,
                "-filter_complex", filter_graph,
                "-map", "[outa]",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_path
            ]
        else:
            filter_graph = (
                f"[0:a]highpass=f=75,equalizer=f=3500:t=q:w=1.2:g=2.5,asplit=2[voice_eq][voice_trigger];"
                f"[1:a]volume={bg_volume_db}dB[bg_low];"
                f"[bg_low][voice_trigger]sidechaincompress=threshold=0.06:ratio=6:attack=150:release=800[ducked_bg];"
                f"[voice_eq][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2,"
                f"loudnorm=I=-14:LRA=7:TP=-1.5[outa]"
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
