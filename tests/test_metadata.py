"""
Tests for the post metadata pack: story scripts get story wording, other
scripts the general wording, and nothing in it is template filler that
never matches the video (fixed timestamps, a placeholder handle).
"""

import json
import os
import unittest

from faceless_shorts.metadata import HANDLE_ENV, MetadataOptimizer, is_story
from faceless_shorts.script_generator import VIRAL_TEMPLATES, Scene, VideoScript


def ghost_story(**overrides) -> VideoScript:
    fields = dict(
        title="The House in Avondale That Cleans Itself",
        niche="avondale_ghost",
        target_duration=170,
        hook="There's a house in Avondale that you will never find dirty. "
             "Not the yard. Not the kitchen. Not one plate.",
        scenes=[Scene(index=1, text="There's a house in Avondale...", visual_prompt="house at night")],
        cta="Would you have stayed a second night in that house?",
        tags=["#zambia", "#ghoststory", "#hauntedhouse", "#shorts"],
    )
    fields.update(overrides)
    return VideoScript(**fields)


def everything(metadata) -> str:
    return json.dumps(metadata, ensure_ascii=False)


class MetadataTestCase(unittest.TestCase):
    def setUp(self):
        self._saved_handle = os.environ.pop(HANDLE_ENV, None)

    def tearDown(self):
        os.environ.pop(HANDLE_ENV, None)
        if self._saved_handle is not None:
            os.environ[HANDLE_ENV] = self._saved_handle

    def assertNoFiller(self, metadata):
        text = everything(metadata)
        for filler in ("TIMESTAMPS", "0:15", "0:35", "How To Protect Yourself",
                       "@yourchannel", "mind mastery", "mind-bending", "psychological secrets"):
            self.assertNotIn(filler, text)

    def assertTitlesKeepWholeTitle(self, metadata, title):
        self.assertEqual(len(metadata["title_variants"]), 4)
        for variant in metadata["title_variants"]:
            self.assertIn(title, variant)
        self.assertEqual(metadata["primary_title"], metadata["title_variants"][0])
        self.assertEqual(metadata["youtube"]["title"], metadata["primary_title"])


class TestStoryMetadata(MetadataTestCase):
    def test_ghost_story_gets_story_lines(self):
        script = ghost_story()
        meta = MetadataOptimizer().generate_metadata(script)

        self.assertNoFiller(meta)
        self.assertTitlesKeepWholeTitle(meta, script.title)
        self.assertNotIn("About Itself", everything(meta))
        description = meta["youtube"]["description"]
        self.assertTrue(description.startswith(script.hook))
        self.assertIn(script.cta, description)
        self.assertIn("Subscribe for more scary stories", description)
        self.assertIn("Wait for the ending", meta["tiktok"]["caption"])
        self.assertTrue(meta["instagram"]["caption"].startswith("🔊 Sound on. Lights off."))

    def test_output_keeps_its_keys(self):
        meta = MetadataOptimizer().generate_metadata(ghost_story())
        self.assertEqual(set(meta), {"primary_title", "title_variants", "youtube", "tiktok", "instagram"})
        self.assertEqual(set(meta["youtube"]), {"title", "description", "tags"})
        self.assertEqual(set(meta["tiktok"]), {"caption"})
        self.assertEqual(set(meta["instagram"]), {"caption"})

    def test_script_tags_lead_and_never_repeat(self):
        script = ghost_story(tags=["#zambia", "ghoststory", "#Shorts", "#viral"])
        meta = MetadataOptimizer().generate_metadata(script)
        tags = meta["youtube"]["tags"]
        self.assertEqual(tags[:4], ["zambia", "ghoststory", "Shorts", "viral"])
        lowered = [t.lower() for t in tags]
        self.assertEqual(len(lowered), len(set(lowered)))
        self.assertIn("youtubeshorts", tags)
        hashtag_line = meta["youtube"]["description"].splitlines()[-1]
        self.assertTrue(hashtag_line.startswith("#zambia #ghoststory #Shorts #viral "))
        # Same script, same order: the old set() shuffled them on every run.
        self.assertEqual(meta, MetadataOptimizer().generate_metadata(script))

    def test_tiktok_caption_keeps_whole_sentences(self):
        meta = MetadataOptimizer().generate_metadata(ghost_story())
        self.assertTrue(meta["tiktok"]["caption"].startswith(
            "There's a house in Avondale that you will never find dirty. Not the yard. 😨"))

    def test_tiktok_caption_cuts_a_long_sentence_between_words(self):
        hook = ("Every night at two in the morning somebody sweeps the yard of the old house "
                "on the corner where nobody has lived since the grandmother died")
        caption = MetadataOptimizer().generate_metadata(ghost_story(hook=hook))["tiktok"]["caption"]
        opening = caption.split("...", 1)[0]
        self.assertTrue(hook.startswith(opening))
        self.assertEqual(hook[len(opening)], " ")
        self.assertLessEqual(len(opening), 85)

    def test_missing_cta_leaves_no_empty_lines(self):
        meta = MetadataOptimizer().generate_metadata(ghost_story(cta=""))
        for text in (meta["youtube"]["description"], meta["instagram"]["caption"]):
            self.assertNotIn("\n\n\n", text)


class TestGeneralMetadata(MetadataTestCase):
    def test_self_help_script_gets_general_lines(self):
        script = VIRAL_TEMPLATES["dark_psychology"]
        meta = MetadataOptimizer().generate_metadata(script)

        self.assertFalse(is_story(script))
        self.assertNoFiller(meta)
        self.assertTitlesKeepWholeTitle(meta, script.title)
        description = meta["youtube"]["description"]
        self.assertIn("Watch until the end", description)
        self.assertNotIn("scary stories", everything(meta))
        self.assertTrue(meta["instagram"]["caption"].startswith("Save this before it disappears"))

    def test_only_the_horror_template_is_a_story(self):
        stories = sorted(key for key, script in VIRAL_TEMPLATES.items() if is_story(script))
        self.assertEqual(stories, ["horror_mystery"])

    def test_story_detection(self):
        self.assertTrue(is_story(ghost_story(tags=[])))  # niche avondale_ghost
        self.assertTrue(is_story(ghost_story(niche="zambia", tags=["#hauntedhouse"])))
        self.assertTrue(is_story(ghost_story(niche="zambia", tags=[], title="The Haunted Well")))
        # Fact niches say "mystery" and "terrifying" too; that's no ghost story.
        self.assertFalse(is_story(ghost_story(
            niche="mind_blowing_facts", tags=["#cosmicmystery", "#spacefacts"],
            title="3 Terrifying Space Facts That Keep Scientists Awake")))
        self.assertFalse(is_story(ghost_story(
            niche="dark_psychology", tags=["#darkpsychology"],
            title="Ghosting Is A Dark Psychology Trick")))


class TestHandle(MetadataTestCase):
    def test_no_follow_line_without_a_handle(self):
        meta = MetadataOptimizer().generate_metadata(ghost_story())
        self.assertNotIn("Follow", meta["instagram"]["caption"])
        self.assertNotIn("@", everything(meta))

    def test_handle_argument_adds_follow_line(self):
        meta = MetadataOptimizer(handle="mychannel").generate_metadata(ghost_story())
        self.assertIn("Follow @mychannel for more scary stories", meta["instagram"]["caption"])

    def test_handle_from_environment(self):
        os.environ[HANDLE_ENV] = "@envchannel"
        meta = MetadataOptimizer().generate_metadata(VIRAL_TEMPLATES["stoicism"])
        caption = meta["instagram"]["caption"]
        self.assertIn("Follow @envchannel for more like this", caption)
        self.assertNotIn("@@", caption)


if __name__ == "__main__":
    unittest.main()
