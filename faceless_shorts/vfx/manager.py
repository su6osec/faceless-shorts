"""
Master VFX & Animation Suite Manager.
Orchestrates open-source visual effects and animation pipelines:
- OpenToonz & Pencil2D: 2D Cel Animation & Line Inking
- Natron: Hollywood Node Compositing (Bloom, Chromatic Aberration, Halation)
- Effekseer: Game & Particle VFX (Sparks, Embers, Cosmic Dust)
- OpenVDB: Volumetric Smoke & Fire Dynamics
- SVG.js, Friction & Synfig: Kinetic Vector Graphics & Animated HUDs
- FreeMoCap: Kinematic Motion Tracking & Telemetry Overlays
- Theatre.js: Non-Linear Easing & Cinematic Spring Physics
"""

import os
import subprocess
from typing import List, Optional

from faceless_shorts.vfx.natron_compositor import NatronCompositor
from faceless_shorts.vfx.effekseer_particles import ParticleEngine
from faceless_shorts.vfx.svg_motion import SVGVectorHUD
from faceless_shorts.vfx.toon_shader import ToonShader
from faceless_shorts.vfx.theatre_easing import get_theatre_motion_expr

VFX_PRESETS = {
    "hollywood": "Natron-style multi-pass node compositing (Anamorphic bloom, chromatic aberration, 35mm grain)",
    "particles": "Effekseer-style procedural floating cosmic stardust & energy sparks",
    "smoke_fire": "OpenVDB-style rising volumetric fire embers & smoke dynamics",
    "svg_hud": "SVG.js & Friction & FreeMoCap animated sci-fi targeting HUD & vector telemetry",
    "toon": "OpenToonz & Pencil2D cel-shaded anime line art with Sobel inking",
    "theatre": "Theatre.js non-linear bezier spring easing curves for dynamic camera motion",
    "none": "Clean standard render without heavy VFX overlays"
}

class VFXManager:
    def __init__(self, work_dir: str = ".temp_render"):
        self.work_dir = work_dir
        self.particle_engine = ParticleEngine()
        self.svg_hud = SVGVectorHUD()

    def apply_vfx_pipeline(
        self,
        base_video_path: str,
        output_video_path: str,
        duration: float,
        vfx_modes: List[str]
    ) -> str:
        """
        Applies requested VFX pipelines (Hollywood Natron compositing, Effekseer particles,
        OpenVDB smoke/embers, SVG.js HUDs, and OpenToonz cel-shading) to the input video.
        """
        if not vfx_modes or "none" in vfx_modes or vfx_modes == ["none"]:
            # If no VFX requested, copy through
            return base_video_path

        current_video = base_video_path
        os.makedirs(self.work_dir, exist_ok=True)

        # 1. Overlay Pass: Effekseer Particles or OpenVDB Embers
        if "particles" in vfx_modes or "smoke_fire" in vfx_modes:
            preset = "fire_embers" if "smoke_fire" in vfx_modes else "cosmic_stardust"
            p_clip = os.path.join(self.work_dir, f"vfx_particles_{preset}.mp4")
            self.particle_engine.generate_particle_overlay(
                output_video_path=p_clip,
                duration=duration,
                preset=preset
            )
            # Blend particle overlay with base video
            blended_particles = os.path.join(self.work_dir, "vfx_p_blended.mp4")
            cmd = [
                "ffmpeg", "-y",
                "-i", current_video,
                "-i", p_clip,
                "-filter_complex", "[0:v][1:v]blend=all_mode=screen[outv]",
                "-map", "[outv]",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                blended_particles
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            current_video = blended_particles

        # 2. Overlay Pass: SVG.js & Friction & FreeMoCap HUD
        if "svg_hud" in vfx_modes:
            hud_clip = os.path.join(self.work_dir, "vfx_svg_hud.mp4")
            self.svg_hud.generate_hud_overlay(
                output_video_path=hud_clip,
                duration=duration
            )
            blended_hud = os.path.join(self.work_dir, "vfx_hud_blended.mp4")
            cmd = [
                "ffmpeg", "-y",
                "-i", current_video,
                "-i", hud_clip,
                "-filter_complex", "[0:v][1:v]blend=all_mode=screen[outv]",
                "-map", "[outv]",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                blended_hud
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            current_video = blended_hud

        # 3. Grading Pass: OpenToonz Cel Animation Shader
        if "toon" in vfx_modes:
            toon_video = os.path.join(self.work_dir, "vfx_toon.mp4")
            fg = ToonShader.get_filtergraph("0:v", "outv")
            cmd = [
                "ffmpeg", "-y",
                "-i", current_video,
                "-filter_complex", fg,
                "-map", "[outv]",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                toon_video
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            current_video = toon_video

        # 4. Grading Pass: Natron Hollywood Node Compositing (Bloom, Chromatic Aberration)
        if "hollywood" in vfx_modes:
            natron_video = os.path.join(self.work_dir, "vfx_natron.mp4")
            fg = NatronCompositor.get_filtergraph("0:v", "outv")
            cmd = [
                "ffmpeg", "-y",
                "-i", current_video,
                "-filter_complex", fg,
                "-map", "[outv]",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                natron_video
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            current_video = natron_video

        return current_video
