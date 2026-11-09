import unittest
from faceless_shorts.vfx import (
    VFXManager,
    VFX_PRESETS,
    NatronCompositor,
    ToonShader,
    get_theatre_motion_expr
)

class TestVFXSuite(unittest.TestCase):
    def test_vfx_presets_loaded(self):
        self.assertIn("hollywood", VFX_PRESETS)
        self.assertIn("particles", VFX_PRESETS)
        self.assertIn("smoke_fire", VFX_PRESETS)
        self.assertIn("svg_hud", VFX_PRESETS)
        self.assertIn("toon", VFX_PRESETS)
        self.assertIn("theatre", VFX_PRESETS)

    def test_natron_filtergraph(self):
        fg = NatronCompositor.get_filtergraph("in_v", "out_v")
        self.assertIn("rgbashift", fg)
        self.assertIn("gblur", fg)
        self.assertIn("blend", fg)
        self.assertIn("format=gbrp", fg)
        self.assertIn("format=yuv420p", fg)

    def test_toon_shader_filtergraph(self):
        fg = ToonShader.get_filtergraph("in_v", "out_v")
        self.assertIn("edgedetect", fg)
        self.assertIn("blend=all_mode=multiply", fg)
        self.assertIn("format=gbrp", fg)

    def test_theatre_motion_expressions(self):
        z, x, y = get_theatre_motion_expr("theatre_spring_zoom", 90)
        self.assertIn("cos", z)
        self.assertIn("exp", z)

        z2, x2, y2 = get_theatre_motion_expr("theatre_whip_pan", 90)
        self.assertIn("pow", x2)

if __name__ == "__main__":
    unittest.main()
