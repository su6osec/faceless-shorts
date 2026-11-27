"""
Metadata and SEO Optimization Module for Faceless Shorts.
Generates titles, descriptions and multi-platform hashtag sets for YouTube
Shorts, Instagram Reels and TikTok. The wording follows the script: ghost,
horror and other scary-story scripts get story lines, everything else gets
the general lines.
"""

import os
import re
from typing import Dict, Iterable, List, Optional

from faceless_shorts.script_generator import VideoScript

# Set this to your channel handle to add a "Follow @you" line to the
# Instagram caption. Unset, the caption has no handle line at all.
HANDLE_ENV = "FACELESS_HANDLE"

# A niche or tag containing one of these marks a scary story. Tags are run
# together ("#ghoststory", "#hauntedhouse"), so they match as substrings.
# "mystery" is left out on purpose: fact niches use it too (#cosmicmystery).
STORY_TAG_WORDS = (
    "ghost", "horror", "haunt", "scary", "creepy", "spooky", "paranormal",
    "supernatural", "nosleep", "unsolved", "urbanlegend", "folklore",
)
# Titles are plain English, so only whole words count ("Ghosting" is not one).
STORY_TITLE_WORDS = re.compile(
    r"\b(ghosts?|haunted|haunting|horror|scary|creepy|spooky|paranormal|supernatural)\b",
    re.IGNORECASE,
)

STORY_LINES = {
    "title_variants": (
        "{title} 👻",
        "Don't Watch This Alone: {title} 😨",
        "{title} | Scary Story 🕯️",
        "Wait For The Ending... {title} 😱",
    ),
    "watch": "🕯️ Stay until the end. That's where it gets worse.",
    "comment": "💬 Has something like this ever happened to you or someone you know? Tell us in the comments.",
    "subscribe": "🔔 Subscribe for more scary stories.",
    "tiktok": "😨 Wait for the ending! Tell us your scariest story in the comments 👇",
    "instagram_opener": "🔊 Sound on. Lights off.",
    "follow": "Follow {handle} for more scary stories 👻",
}

GENERAL_LINES = {
    "title_variants": (
        "{title} 🤯",
        "Nobody Tells You This: {title} 👁️",
        "Never Ignore This: {title} ⚠️",
        "Wait Until The End... {title} 🧠",
    ),
    "watch": "🔥 Watch until the end for the most important truth.",
    "comment": "💬 What do you think? Drop a comment below!",
    "subscribe": "🔔 Subscribe for more shorts like this.",
    "tiktok": "🤯 Wait for the end! Drop your thoughts in the comments 👇",
    "instagram_opener": "Save this before it disappears 📌",
    "follow": "Follow {handle} for more like this 🧠",
}

UNIVERSAL_TAGS = ["#shorts", "#viral", "#fyp", "#trending", "#explore"]
YOUTUBE_TAGS = ["#youtubeshorts", "#shortsfeed", "#shortsvideo"]
TIKTOK_TAGS = ["#tiktokviral", "#foryoupage", "#viralvideo"]
INSTAGRAM_TAGS = ["#reels", "#reelsinstagram", "#reelsviral"]

# The TikTok caption opens with this much of the hook.
TIKTOK_HOOK_CHARS = 85


def is_story(script: VideoScript) -> bool:
    """True when the niche, tags or title mark the script as a scary story."""
    words = " ".join([script.niche or "", *(script.tags or [])]).lower()
    if any(word in words for word in STORY_TAG_WORDS):
        return True
    return bool(STORY_TITLE_WORDS.search(script.title or ""))


def _handle(value: Optional[str]) -> str:
    value = (value or "").strip().lstrip("@")
    return f"@{value}" if value else ""


def _hashtags(*groups: Iterable[str]) -> List[str]:
    """Merge tag groups in order. The first spelling of a tag wins and repeats
    are dropped, so the script's own tags lead (YouTube shows the first three
    above the title)."""
    seen, merged = set(), []
    for group in groups:
        for raw in group:
            tag = re.sub(r"\s+", "", str(raw)).lstrip("#")
            if tag and tag.lower() not in seen:
                seen.add(tag.lower())
                merged.append(f"#{tag}")
    return merged


def _shorten(text: str, limit: int) -> str:
    """Fit text into limit characters: as many whole sentences as fit, else
    whole words plus '...'. Never cuts a word in half."""
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    kept = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        candidate = f"{kept} {sentence}".strip()
        if len(candidate) > limit:
            break
        kept = candidate
    if kept:
        return kept
    # One extra character, so a word ending exactly at the limit is kept.
    head = text[:limit + 1]
    words = head.rsplit(" ", 1)[0] if " " in head else text[:limit]
    return words.rstrip(" ,;:-") + "..."


def _paragraphs(*paragraphs: Iterable[str]) -> str:
    """Join paragraphs with a blank line, leaving out empty lines and paragraphs."""
    blocks = ["\n".join(line for line in lines if line) for lines in paragraphs]
    return "\n\n".join(block for block in blocks if block)


class MetadataOptimizer:
    def __init__(self, handle: Optional[str] = None):
        """handle: channel handle for the Instagram follow line. Defaults to
        $FACELESS_HANDLE; with neither set, the caption has no follow line."""
        self.handle = _handle(handle if handle is not None else os.environ.get(HANDLE_ENV))

    def generate_metadata(self, script: VideoScript) -> Dict:
        """
        Generate complete social publishing pack:
        - YouTube Shorts Title, Description, Tags
        - TikTok Captions and Hashtags
        - Instagram Reels Caption and Hashtag Groups
        """
        lines = STORY_LINES if is_story(script) else GENERAL_LINES
        title = " ".join((script.title or "").split())
        hook = " ".join((script.hook or "").split())
        cta = " ".join((script.cta or "").split())

        # 1. Title variations: the whole title in each, so any title reads right
        title_variants = [v.format(title=title) for v in lines["title_variants"]]

        # 2. Hashtags: the script's own tags first, then the platform ones
        niche_tags = script.tags or [f"#{script.niche}"]
        yt_tags = _hashtags(niche_tags, UNIVERSAL_TAGS, YOUTUBE_TAGS)
        tt_tags = _hashtags(niche_tags, UNIVERSAL_TAGS, TIKTOK_TAGS)
        ig_tags = _hashtags(niche_tags, UNIVERSAL_TAGS, INSTAGRAM_TAGS)

        # 3. Descriptions
        yt_description = _paragraphs(
            [hook],
            [lines["watch"], cta],
            [lines["comment"], lines["subscribe"]],
            [" ".join(yt_tags)],
        )

        tt_caption = _paragraphs(
            [" ".join(p for p in (_shorten(hook, TIKTOK_HOOK_CHARS), lines["tiktok"]) if p)],
            [" ".join(tt_tags)],
        )

        follow = lines["follow"].format(handle=self.handle) if self.handle else ""
        ig_caption = _paragraphs(
            [lines["instagram_opener"]],
            [hook],
            [cta, follow],
            [".", ".", ".", " ".join(ig_tags)],
        )

        return {
            "primary_title": title_variants[0],
            "title_variants": title_variants,
            "youtube": {
                "title": title_variants[0],
                "description": yt_description,
                "tags": [t.lstrip("#") for t in yt_tags]
            },
            "tiktok": {
                "caption": tt_caption
            },
            "instagram": {
                "caption": ig_caption
            }
        }
