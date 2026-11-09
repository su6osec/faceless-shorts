"""
SVG.js, Friction & FreeMoCap Vector Motion Graphics Engine.
Procedurally generates animated vector motion graphics, sci-fi HUDs, and kinematic overlays:
- Futuristic targeting crosshairs & reticles
- Animated corner brackets & framing HUDs
- Circular rotating telemetry gauges
- FreeMoCap-style kinematic tracking markers
Inspired by https://github.com/svgdotjs/svg.js, https://github.com/friction2d/friction, and https://github.com/freemocap/freemocap
"""

import math
import os
import subprocess
from typing import Dict, List, Optional
from PIL import Image, ImageDraw

from faceless_shorts.config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FPS

class SVGVectorHUD:
    def __init__(self, width: int = CANVAS_WIDTH, height: int = CANVAS_HEIGHT, fps: int = DEFAULT_FPS):
        self.width = width
        self.height = height
        self.fps = fps
        self.sim_w = 540
        self.sim_h = 960

    def generate_hud_overlay(
        self,
        output_video_path: str,
        duration: float,
        preset: str = "sci_fi_reticle",
        color_rgb: tuple = (0, 240, 255)  # Electric cyan default
    ) -> str:
        """
        Synthesizes an animated vector motion graphics HUD overlay video.
        Composited over video with FFmpeg blend=all_mode=screen.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        total_frames = max(int(duration * self.fps), 15)
        temp_dir = output_video_path + "_hud_frames"
        os.makedirs(temp_dir, exist_ok=True)

        cx, cy = self.sim_w // 2, self.sim_h // 2
        r, g, b = color_rgb

        for frame_idx in range(total_frames):
            frame = Image.new("RGBA", (self.sim_w, self.sim_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            time_sec = frame_idx / self.fps
            angle = (time_sec * 45) % 360  # Rotating 45 deg/sec

            # 1. Sci-Fi Tech Corner Brackets
            margin = 35
            b_len = 40
            w_box, h_box = self.sim_w - margin, self.sim_h - margin
            alpha_hud = 180

            # Top-Left Bracket
            draw.line([(margin, margin), (margin + b_len, margin)], fill=(r, g, b, alpha_hud), width=2)
            draw.line([(margin, margin), (margin, margin + b_len)], fill=(r, g, b, alpha_hud), width=2)
            # Top-Right Bracket
            draw.line([(w_box, margin), (w_box - b_len, margin)], fill=(r, g, b, alpha_hud), width=2)
            draw.line([(w_box, margin), (w_box, margin + b_len)], fill=(r, g, b, alpha_hud), width=2)
            # Bottom-Left Bracket
            draw.line([(margin, h_box), (margin + b_len, h_box)], fill=(r, g, b, alpha_hud), width=2)
            draw.line([(margin, h_box), (margin, h_box - b_len)], fill=(r, g, b, alpha_hud), width=2)
            # Bottom-Right Bracket
            draw.line([(w_box, h_box), (w_box - b_len, h_box)], fill=(r, g, b, alpha_hud), width=2)
            draw.line([(w_box, h_box), (w_box, h_box - b_len)], fill=(r, g, b, alpha_hud), width=2)

            # 2. Central Targeting Reticle & Rotating Rings
            radius = 120
            # Inner rotating dashed arc
            for seg in range(4):
                start_deg = angle + seg * 90
                end_deg = start_deg + 45
                draw.arc(
                    [cx - radius, cy - radius, cx + radius, cy + radius],
                    start=start_deg,
                    end=end_deg,
                    fill=(r, g, b, 200),
                    width=2
                )

            # Small target center crosshair
            cross_r = 14
            draw.line([(cx - cross_r, cy), (cx + cross_r, cy)], fill=(r, g, b, 230), width=1)
            draw.line([(cx, cy - cross_r), (cx, cy + cross_r)], fill=(r, g, b, 230), width=1)
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(r, g, b, 255), width=1)

            # FreeMoCap / Kinematic telemetry tracking ticks
            pulse_rad = radius + int(15 * math.sin(time_sec * 3.0))
            draw.arc(
                [cx - pulse_rad, cy - pulse_rad, cx + pulse_rad, cy + pulse_rad],
                start=0,
                end=360,
                fill=(r, g, b, 50),
                width=1
            )

            frame_path = os.path.join(temp_dir, f"hud_{frame_idx:04d}.png")
            frame.save(frame_path)

        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(self.fps),
            "-i", os.path.join(temp_dir, "hud_%04d.png"),
            "-vf", f"scale={self.width}:{self.height}:flags=bilinear",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)

        return output_video_path
