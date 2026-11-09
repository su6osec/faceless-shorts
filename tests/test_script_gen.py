import unittest
from faceless_shorts.script_generator import (
    VIRAL_TEMPLATES,
    get_template,
    create_or_get_script,
    DynamicScriptBuilder,
    VideoScript
)

class TestScriptGenerator(unittest.TestCase):
    def test_viral_templates_loaded(self):
        self.assertIn("fitness", VIRAL_TEMPLATES)
        self.assertIn("dark_psychology", VIRAL_TEMPLATES)
        self.assertIn("stoicism", VIRAL_TEMPLATES)
        self.assertIn("mind_blowing_facts", VIRAL_TEMPLATES)

    def test_template_structure(self):
        script = get_template("fitness")
        self.assertIsNotNone(script)
        self.assertTrue(len(script.scenes) >= 4)
        self.assertTrue(len(script.hook) > 10)
        self.assertTrue(len(script.tags) > 0)

    def test_dynamic_script_creation(self):
        script = DynamicScriptBuilder.build("boxing psychology")
        self.assertIn("Boxing Psychology", script.title)
        self.assertEqual(len(script.scenes), 5)
        self.assertTrue("boxing psychology" in script.scenes[0].text.lower())

    def test_create_or_get_script(self):
        script_fitness = create_or_get_script("fitness")
        self.assertEqual(script_fitness.niche, "fitness")

        script_custom = create_or_get_script("quantum computing")
        self.assertEqual(len(script_custom.scenes), 5)

    def test_multilingual_script_creation(self):
        script_hi = DynamicScriptBuilder.build("कसरत", language="hi")
        self.assertIn("कसरत", script_hi.title)
        self.assertEqual(len(script_hi.scenes), 5)
        self.assertIn("#hindi", script_hi.tags)

        script_es = DynamicScriptBuilder.build("boxeo", language="es")
        self.assertIn("Boxeo", script_es.title)
        self.assertIn("#parati", script_es.tags)

    def test_to_dict_and_from_dict(self):
        original = get_template("stoicism")
        data = original.to_dict()
        reconstructed = VideoScript.from_dict(data)
        self.assertEqual(original.title, reconstructed.title)
        self.assertEqual(len(original.scenes), len(reconstructed.scenes))

if __name__ == "__main__":
    unittest.main()
