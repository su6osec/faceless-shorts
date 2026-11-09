import unittest
from faceless_shorts.script_generator import (
    VIRAL_TEMPLATES,
    get_template,
    create_custom_script,
    VideoScript
)

class TestScriptGenerator(unittest.TestCase):
    def test_viral_templates_loaded(self):
        self.assertIn("dark_psychology", VIRAL_TEMPLATES)
        self.assertIn("stoicism", VIRAL_TEMPLATES)
        self.assertIn("mind_blowing_facts", VIRAL_TEMPLATES)

    def test_template_structure(self):
        script = get_template("dark_psychology")
        self.assertIsNotNone(script)
        self.assertTrue(len(script.scenes) >= 4)
        self.assertTrue(len(script.hook) > 10)
        self.assertTrue(len(script.tags) > 0)

    def test_custom_script_creation(self):
        scenes_data = [
            {"text": "Hook sentence here.", "visual_prompt": "Prompt 1"},
            {"text": "Second sentence here.", "visual_prompt": "Prompt 2"}
        ]
        script = create_custom_script("Custom Title", "custom_niche", scenes_data)
        self.assertEqual(script.title, "Custom Title")
        self.assertEqual(len(script.scenes), 2)
        self.assertEqual(script.scenes[0].text, "Hook sentence here.")

    def test_to_dict_and_from_dict(self):
        original = get_template("stoicism")
        data = original.to_dict()
        reconstructed = VideoScript.from_dict(data)
        self.assertEqual(original.title, reconstructed.title)
        self.assertEqual(len(original.scenes), len(reconstructed.scenes))

if __name__ == "__main__":
    unittest.main()
