"""
Visuals Module for Faceless Shorts.
Handles free AI image generation (Pollinations Flux / local ComfyUI / offline procedural),
offline PIL art-style transforms (pixel art, chalkboard, glow sketch, halftone, ...),
artistic FFmpeg grading, and punchy dynamic Ken Burns motion video synthesis.
"""

import math
import os
import random
import subprocess
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
from PIL import Image, ImageDraw, ImageFilter

from faceless_shorts.config import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    DEFAULT_FPS,
    ART_STYLES,
    DEFAULT_IMAGE_ENGINE,
)
from faceless_shorts.style_processor import StyleProcessor
from faceless_shorts.vfx.theatre_easing import get_theatre_motion_expr

class VisualManager:
    def __init__(
        self,
        cache_dir: str = ".cache_visuals",
        art_style: str = "hyperreal",
        engine: str = DEFAULT_IMAGE_ENGINE,
        width: int = CANVAS_WIDTH,
        height: int = CANVAS_HEIGHT,
        fps: int = DEFAULT_FPS,
    ):
        self.cache_dir = cache_dir
        self.art_style = art_style
        self.engine = engine or DEFAULT_IMAGE_ENGINE
        self.width = width
        self.height = height
        self.fps = fps
        os.makedirs(self.cache_dir, exist_ok=True)

    # ------------------------------------------------------------------ IMAGES
    def _pollinations_url(self, prompt: str, model: str, seed: int) -> str:
        style_config = ART_STYLES.get(self.art_style, ART_STYLES["hyperreal"])
        enhanced_prompt = f"{prompt}, {style_config['prompt_suffix']}"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        return (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width={self.width}&height={self.height}"
            f"&model={model}&seed={seed}&nologo=true"
        )

    def generate_ai_image(
        self,
        prompt: str,
        output_path: str,
        model: str = "flux",
        seed: Optional[int] = None
    ) -> str:
        """
        Generate a vertical AI image using the selected free engine:
          - pollinations: keyless cloud Flux generation
          - comfyui: local ComfyUI instance (private, GPU, free)
          - procedural: offline Pillow canvas (zero network)
        Always degrades to the procedural canvas so rendering never fails.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        chosen_seed = seed if seed is not None else random.randint(1000, 999999)

        if self.engine == "comfyui":
            try:
                from faceless_shorts.integrations import ComfyUIClient
                client = ComfyUIClient()
                path = client.generate(
                    prompt=prompt,
                    output_path=output_path,
                    width=self.width,
                    height=self.height,
                    seed=chosen_seed,
                )
                if path and os.path.exists(path):
                    with Image.open(path) as img:
                        img.verify()
                    return path
                print("    [!] ComfyUI unavailable, falling back to Pollinations Flux.")
            except Exception as e:
                print(f"    [!] ComfyUI engine failed ({e}), falling back to Pollinations Flux.")

        if self.engine != "procedural":
            style_config = ART_STYLES.get(self.art_style, ART_STYLES["hyperreal"])
            url = self._pollinations_url(prompt, model, chosen_seed)
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

    def generate_ai_images_parallel(
        self,
        jobs: List[Dict],
        max_workers: int = 4
    ) -> Dict[str, str]:
        """
        Generate several AI images concurrently (network-bound -> big wall-clock win).
        jobs: [{"prompt": str, "output_path": str}, ...] in scene order.
        Returns {output_path: path} (failed jobs fall back to procedural canvases).
        """
        def _one(job: Dict) -> Dict[str, str]:
            try:
                return {job["output_path"]: self.generate_ai_image(
                    prompt=job["prompt"], output_path=job["output_path"])}
            except Exception:
                return {job["output_path"]: self.generate_procedural_background(
                    output_path=job["output_path"], topic=job.get("prompt", ""))}

        results: Dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for partial in pool.map(_one, jobs):
                results.update(partial)
        return results

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
        img = Image.new("RGB", (self.width, self.height), color=(12, 12, 18))
        draw = ImageDraw.Draw(img)

        # Draw deep moody vertical gradient
        color_top = (8, 8, 14)
        color_bottom = (26, 20, 38)

        for y in range(self.height):
            ratio = y / self.height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Add ambient glowing sphere
        glow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse(
            [(self.width // 4, self.height // 3), (self.width * 3 // 4, self.height * 2 // 3)],
            fill=(65, 45, 95, 90)
        )
        glow = glow.filter(ImageFilter.GaussianBlur(120))
        img.paste(glow, (0, 0), glow)

        img.save(output_path, quality=95)
        return output_path

    def apply_art_style(self, image_path: str, output_path: str) -> str:
        """
        Apply the offline PIL pixel-op stage of the current art style
        (pixel art, chalkboard, glow sketch, halftone, flat vector, ...).
        Styles without a pixel_op pass through untouched.
        """
        style_config = ART_STYLES.get(self.art_style, ART_STYLES["hyperreal"])
        pixel_op = style_config.get("pixel_op")
        if not pixel_op:
            return image_path
        try:
            return StyleProcessor.apply(
                image_path=image_path,
                output_path=output_path,
                op=pixel_op,
                params=style_config.get("pixel_op_params"),
            )
        except Exception as e:
            print(f"    [!] Style transform '{pixel_op}' failed ({e}). Using raw visual.")
            return image_path

    # -------------------------------------------------------------- KEN BURNS
    def render_ken_burns_clip(
        self,
        image_path: str,
        output_video_path: str,
        duration: float,
        motion: str = "punch_zoom_in",
        fps: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> str:
        """
        Convert static image into a dynamic vertical video clip with punchy Ken Burns motion
        and artistic video post-processing filters (sketch, vintage film, papercraft, cyberpunk).
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        fps = fps or self.fps
        width = width or self.width
        height = height or self.height
        total_frames = max(int(duration * fps), 30)

        # Dynamic high-impact camera motion formulas
        if motion.startswith("theatre_"):
            z_expr, x_expr, y_expr = get_theatre_motion_expr(motion, total_frames)
        elif motion == "dramatic_zoom_out":
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
        elif motion == "whip_zoom":
            # High-impact dynamic whip zoom surge
            z_expr = f"min(1.0+0.45*pow(on/{total_frames},1.6),1.48)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion == "rise_up":
            # Slow vertical crane rise (reveals the scene upward)
            z_expr = "1.22"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = f"max((ih-ih/zoom)*(1-on/{total_frames}),0)"
        elif motion == "orbit_sway":
            # Gentle floating orbital drift (documentary hover)
            z_expr = "1.18+0.04*sin(on*0.08)"
            x_expr = "iw/2-(iw/zoom/2)+sin(on*0.045)*38"
            y_expr = "ih/2-(ih/zoom/2)+cos(on*0.037)*26"
        elif motion == "pulse_heartbeat":
            # Double-thump zoom pulse synced to audio tension
            z_expr = f"1.06+0.10*abs(sin(on*0.45))+0.03*sin(on*0.11)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion == "shockwave_out":
            # Explosive pull-back with decaying micro-shake (impact reveal)
            z_expr = f"if(lte(on,6),1.0+0.06*on,max(1.36-0.005*(on-6),1.04))"
            x_expr = "iw/2-(iw/zoom/2)+sin(on*0.9)*12*exp(-on/14)"
            y_expr = "ih/2-(ih/zoom/2)+cos(on*1.1)*9*exp(-on/14)"
        else: # punch_zoom_in default
            # Fast, punchy camera push-in (1.0x -> 1.38x)
            z_expr = "min(zoom+0.0035,1.38)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"

        # Pre-scale and supersample to prevent distortion & zoompan jitter on any input
        base_prep = "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840"

        # Ken Burns motion filter
        motion_filter = f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':d={total_frames}:s={width}x{height}:fps={fps}"

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
