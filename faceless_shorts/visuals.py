"""
Visuals Module for Faceless Shorts.
Handles free AI image generation via Pollinations (Flux/SDXL), Pexels stock video fetching,
offline procedural background generation, and Ken Burns motion video synthesis.
"""

import math
import os
import random
import subprocess
import time
import urllib.parse
import urllib.request
from typing import Dict, List, Optional
from PIL import Image, ImageDraw, ImageFilter

from faceless_shorts.config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FPS

class VisualManager:
    def __init__(self, cache_dir: str = ".cache_visuals"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def generate_ai_image(
        self,
        prompt: str,
        output_path: str,
        model: str = "flux",
        seed: Optional[int] = None
    ) -> str:
        """
        Generate 1080x1920 AI image using Pollinations API (100% Free, no API key).
        Falls back to procedural generation if network is unavailable.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        chosen_seed = seed if seed is not None else random.randint(1000, 999999)
        
        # Optimize prompt for vertical 9:16 cinematic aesthetic
        enhanced_prompt = f"{prompt}, 9:16 vertical orientation, cinematic aesthetic, dramatic lighting, photorealistic, 8k wallpaper"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width={CANVAS_WIDTH}&height={CANVAS_HEIGHT}"
            f"&model={model}&seed={chosen_seed}&nologo=true"
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=40) as response:
                    with open(output_path, "wb") as f:
                        f.write(response.read())

                # Validate image
                with Image.open(output_path) as img:
                    img.verify()

                return output_path
            except Exception as e:
                time.sleep(2)
                if attempt == max_retries - 1:
                    print(f"[!] Warning: Pollinations generation failed ({e}). Falling back to procedural background.")
                    return self.generate_procedural_background(output_path, prompt)

        return self.generate_procedural_background(output_path, prompt)

    def generate_procedural_background(
        self,
        output_path: str,
        topic: str = "general"
    ) -> str:
        """
        Generate an elegant, moody abstract dark gradient background offline using Pillow.
        Zero dependencies on external APIs, ensuring offline reliability.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), color=(15, 15, 22))
        draw = ImageDraw.Draw(img)

        # Draw a deep moody vertical gradient
        color_top = (10, 10, 18)
        color_bottom = (24, 20, 36)
        
        for y in range(CANVAS_HEIGHT):
            ratio = y / CANVAS_HEIGHT
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b))

        # Add subtle ambient glowing circle in the center/upper third
        glow = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse(
            [(CANVAS_WIDTH // 4, CANVAS_HEIGHT // 3), (CANVAS_WIDTH * 3 // 4, CANVAS_HEIGHT * 2 // 3)],
            fill=(60, 40, 90, 80)
        )
        glow = glow.filter(ImageFilter.GaussianBlur(120))
        img.paste(glow, (0, 0), glow)

        img.save(output_path, quality=95)
        return output_path

    def render_ken_burns_clip(
        self,
        image_path: str,
        output_video_path: str,
        duration: float,
        motion: str = "center_zoom_in",
        fps: int = DEFAULT_FPS
    ) -> str:
        """
        Convert static image into a cinematic vertical video clip with Ken Burns motion.
        Uses FFmpeg's zoompan filter with heavy pre-scaling to prevent stutter/jitter.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        total_frames = max(int(duration * fps), 30)

        # Select motion mathematical formula
        if motion == "center_zoom_out":
            # Start at 1.25x and smoothly zoom out towards 1.0x
            z_expr = "if(eq(on,1),1.25,max(zoom-0.0012,1.0))"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion == "pan_up":
            z_expr = "1.15"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = f"min(ih/2-(ih/zoom/2)+({total_frames}-on)*1.2,ih-(ih/zoom))"
        elif motion == "pan_down":
            z_expr = "1.15"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "max(0,on*1.2)"
        elif motion == "subtle_drift":
            z_expr = "min(zoom+0.0006,1.15)"
            x_expr = "iw/2-(iw/zoom/2)+sin(on*0.03)*25"
            y_expr = "ih/2-(ih/zoom/2)"
        else: # center_zoom_in default
            z_expr = "min(zoom+0.0012,1.25)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"

        filter_chain = (
            f"scale=2160:-1,"
            f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':"
            f"d={total_frames}:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:fps={fps},"
            f"format=yuv420p"
        )

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", filter_chain,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "faster",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_video_path
