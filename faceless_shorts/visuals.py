"""
Visuals Module for Faceless Shorts.
Handles free AI image generation via Pollinations (Flux/SDXL),
artistic video styles (sketch, old style 35mm, papercraft, cyberpunk),
and punchy dynamic Ken Burns motion video synthesis.
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

from faceless_shorts.config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FPS, ART_STYLES

class VisualManager:
    def __init__(self, cache_dir: str = ".cache_visuals", art_style: str = "hyperreal"):
        self.cache_dir = cache_dir
        self.art_style = art_style
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
        Injects artistic style modifiers (sketch, old style, papercraft, cyberpunk).
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        chosen_seed = seed if seed is not None else random.randint(1000, 999999)
        
        style_config = ART_STYLES.get(self.art_style, ART_STYLES["hyperreal"])
        style_suffix = style_config["prompt_suffix"]

        # Formulate full enriched prompt
        enhanced_prompt = f"{prompt}, {style_suffix}"
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
                with urllib.request.urlopen(req, timeout=35) as response:
                    with open(output_path, "wb") as f:
                        f.write(response.read())

                # Validate image file integrity
                with Image.open(output_path) as img:
                    img.verify()

                return output_path
            except Exception as e:
                time.sleep(2)
                if attempt == max_retries - 1:
                    print(f"    [!] Warning: Visual generation failed ({e}). Using sleek procedural canvas.")
                    return self.generate_procedural_background(output_path, prompt)

        return self.generate_procedural_background(output_path, prompt)

    def generate_procedural_background(
        self,
        output_path: str,
        topic: str = "general"
    ) -> str:
        """
        Generate a moody abstract dark gradient background offline using Pillow.
        Zero dependencies on external APIs, ensuring 100% offline reliability.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), color=(12, 12, 18))
        draw = ImageDraw.Draw(img)

        # Draw deep moody vertical gradient
        color_top = (8, 8, 14)
        color_bottom = (26, 20, 38)
        
        for y in range(CANVAS_HEIGHT):
            ratio = y / CANVAS_HEIGHT
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b))

        # Add ambient glowing sphere
        glow = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse(
            [(CANVAS_WIDTH // 4, CANVAS_HEIGHT // 3), (CANVAS_WIDTH * 3 // 4, CANVAS_HEIGHT * 2 // 3)],
            fill=(65, 45, 95, 90)
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
        motion: str = "punch_zoom_in",
        fps: int = DEFAULT_FPS
    ) -> str:
        """
        Convert static image into a dynamic vertical video clip with punchy Ken Burns motion
        and artistic video post-processing filters (sketch, vintage film, papercraft, cyberpunk).
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        total_frames = max(int(duration * fps), 30)

        # Dynamic high-impact camera motion formulas
        if motion == "dramatic_zoom_out":
            # Starts close (1.38x) and smoothly reveals out to 1.02x
            z_expr = "if(eq(on,1),1.38,max(zoom-0.0035,1.02))"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion == "pan_left":
            # Smooth cinematic left tracking pan
            z_expr = "1.25"
            x_expr = f"min((iw-iw/zoom)*(on/{total_frames}),iw-iw/zoom)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion == "pan_right":
            # Smooth cinematic right tracking pan
            z_expr = "1.25"
            x_expr = f"max((iw-iw/zoom)*(1-on/{total_frames}),0)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion == "vertigo_shake":
            # Organic handheld camera float
            z_expr = "min(zoom+0.002,1.3)"
            x_expr = "iw/2-(iw/zoom/2)+sin(on*0.06)*20"
            y_expr = "ih/2-(ih/zoom/2)+cos(on*0.05)*15"
        else: # punch_zoom_in default
            # Fast, punchy camera push-in (1.0x -> 1.38x)
            z_expr = "min(zoom+0.0035,1.38)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"

        # Pre-scale and crop to exact 9:16 to prevent distortion on any input image
        base_prep = "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840"
        
        # Ken Burns motion filter
        motion_filter = f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':d={total_frames}:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:fps={fps}"

        # Artistic style filter chain
        style_config = ART_STYLES.get(self.art_style, ART_STYLES["hyperreal"])
        art_filter = style_config.get("ffmpeg_filter", "eq=contrast=1.05:saturation=1.05")

        full_filter_chain = f"{base_prep},{motion_filter},{art_filter},format=yuv420p"

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", full_filter_chain,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "faster",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_video_path
