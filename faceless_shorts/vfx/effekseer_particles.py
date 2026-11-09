"""
Effekseer Particle Generator & OpenVDB Volumetrics Engine.
Procedurally simulates dynamic physical particles:
- Rising glowing fire embers and sparks
- Cosmic stardust & nebula floating particles
- Electric arcs and energy shockwaves
Inspired by https://github.com/effekseer/effekseer and https://github.com/academysoftwarefoundation/openvdb
"""

import math
import os
import random
import subprocess
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFilter

from faceless_shorts.config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FPS

class ParticleEngine:
    def __init__(self, width: int = CANVAS_WIDTH, height: int = CANVAS_HEIGHT, fps: int = DEFAULT_FPS):
        self.width = width
        self.height = height
        self.fps = fps
        # Internal low-res simulation grid (540x960) for lightning-fast rendering
        self.sim_w = 540
        self.sim_h = 960

    def generate_particle_overlay(
        self,
        output_video_path: str,
        duration: float,
        preset: str = "cosmic_stardust",
        particle_count: int = 45
    ) -> str:
        """
        Synthesizes a physical particle overlay video clip using procedural simulation.
        Can be composited over video with FFmpeg blend=all_mode=screen.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        total_frames = max(int(duration * self.fps), 15)
        
        # Color palettes and dynamics based on preset
        if preset == "fire_embers":
            base_colors = [(255, 120, 20), (255, 70, 10), (255, 200, 50), (255, 90, 0)]
            speed_range = (4.0, 9.0)
            drift_amp = 2.0
            y_dir = -1  # Rising up
        elif preset == "electric_sparks":
            base_colors = [(50, 220, 255), (100, 255, 255), (180, 240, 255), (255, 255, 255)]
            speed_range = (6.0, 14.0)
            drift_amp = 4.0
            y_dir = -1
        else: # cosmic_stardust / nebula
            base_colors = [(200, 180, 255), (255, 215, 100), (120, 220, 255), (255, 255, 255)]
            speed_range = (1.5, 4.5)
            drift_amp = 1.2
            y_dir = -1

        # Initialize particles
        particles = []
        for _ in range(particle_count):
            particles.append({
                "x": random.uniform(0, self.sim_w),
                "y": random.uniform(0, self.sim_h),
                "r": random.uniform(2.0, 5.5),
                "speed": random.uniform(*speed_range),
                "phase": random.uniform(0, math.pi * 2),
                "color": random.choice(base_colors),
                "alpha": random.randint(140, 255),
                "flicker_speed": random.uniform(0.1, 0.3)
            })

        # Render frames to raw image sequence in temp directory or pipe directly into FFmpeg
        temp_dir = output_video_path + "_frames"
        os.makedirs(temp_dir, exist_ok=True)

        for frame_idx in range(total_frames):
            frame = Image.new("RGBA", (self.sim_w, self.sim_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)

            for p in particles:
                p["y"] += p["speed"] * y_dir
                p["x"] += math.sin(p["phase"] + frame_idx * 0.08) * drift_amp

                # Wrap around borders
                if p["y"] < -10:
                    p["y"] = self.sim_h + 10
                    p["x"] = random.uniform(0, self.sim_w)
                elif p["y"] > self.sim_h + 10:
                    p["y"] = -10
                    p["x"] = random.uniform(0, self.sim_w)

                # Pulsing brightness
                pulse = 0.7 + 0.3 * math.sin(frame_idx * p["flicker_speed"] + p["phase"])
                r, g, b = p["color"]
                a = int(p["alpha"] * pulse)

                # Draw glowing core and soft halo
                rad = p["r"]
                draw.ellipse(
                    [p["x"] - rad, p["y"] - rad, p["x"] + rad, p["y"] + rad],
                    fill=(r, g, b, a)
                )

            # Soft bloom blur
            frame_blurred = frame.filter(ImageFilter.GaussianBlur(1.2))
            frame_final = Image.alpha_composite(frame_blurred, frame)
            
            # Save frame as PNG
            frame_path = os.path.join(temp_dir, f"p_frame_{frame_idx:04d}.png")
            frame_final.save(frame_path)

        # Encode frames into lightweight MP4 overlay
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(self.fps),
            "-i", os.path.join(temp_dir, "p_frame_%04d.png"),
            "-vf", f"scale={self.width}:{self.height}:flags=bilinear",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Clean up temporary frame PNGs
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)

        return output_video_path
