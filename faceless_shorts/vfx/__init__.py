"""
VFX & Animation Suite for Faceless Shorts.
Integrates techniques from:
- OpenToonz / Pencil2D (2D Animation & Cel Shading)
- Natron (Hollywood Node-based Compositing & Bloom)
- Effekseer (Game Particle Simulations & Energy Sparks)
- OpenVDB (Volumetric Smoke, Fire & Embers)
- SVG.js & Friction & Synfig (Vector Motion Graphics & Kinetic HUDs)
- FreeMoCap (Kinematic Tracking & Telemetry Overlays)
- Theatre.js (Cinematic Bezier Keyframing & Spring Physics)
"""

from faceless_shorts.vfx.manager import VFXManager, VFX_PRESETS
from faceless_shorts.vfx.theatre_easing import get_theatre_motion_expr
from faceless_shorts.vfx.natron_compositor import NatronCompositor
from faceless_shorts.vfx.effekseer_particles import ParticleEngine
from faceless_shorts.vfx.svg_motion import SVGVectorHUD
from faceless_shorts.vfx.toon_shader import ToonShader

__all__ = [
    "VFXManager",
    "VFX_PRESETS",
    "get_theatre_motion_expr",
    "NatronCompositor",
    "ParticleEngine",
    "SVGVectorHUD",
    "ToonShader"
]
