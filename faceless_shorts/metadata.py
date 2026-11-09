"""
Metadata and SEO Optimization Module for Faceless Shorts.
Generates viral titles, high-retention descriptions, and multi-platform hashtag sets
optimized for YouTube Shorts, Instagram Reels, and TikTok algorithms.
"""

from typing import Dict, List
from faceless_shorts.script_generator import VideoScript

class MetadataOptimizer:
    def __init__(self):
        pass

    def generate_metadata(self, script: VideoScript) -> Dict:
        """
        Generate complete social publishing pack:
        - YouTube Shorts Title, Description, Tags
        - TikTok Captions and Hashtags
        - Instagram Reels Caption and Hashtag Groups
        """
        # 1. High CTR Title Variations
        base_title = script.title
        title_variants = [
            f"{base_title} 🤯",
            f"The Secret Nobody Tells You About {base_title.split()[-1]}... 👁️",
            f"Never Ignore This: {base_title} ⚠️",
            f"Wait Until The End... {base_title} 🧠"
        ]

        # 2. Viral Hashtags
        universal_tags = ["#shorts", "#viral", "#fyp", "#trending", "#explore"]
        yt_tags = ["#youtubeshorts", "#shortsfeed", "#shortsvideo"]
        tt_tags = ["#tiktokviral", "#foryoupage", "#viralvideo"]
        ig_tags = ["#reels", "#reelsinstagram", "#reelsviral"]
        
        niche_tags = script.tags or [f"#{script.niche}"]

        # 3. Descriptions
        yt_description = f"""{script.hook}

🔥 Watch until the end for the most important truth.
{script.cta}

⏰ TIMESTAMPS:
0:00 - The Hook
0:15 - The Untold Truth
0:35 - How To Protect Yourself

💬 Drop a comment below if you have ever experienced this!
🔔 Subscribe for more mind-bending wisdom and psychological secrets.

{' '.join(set(universal_tags + yt_tags + niche_tags))}
"""

        tt_caption = f"""{script.hook[:85]}... 🤯 Wait for the end! Drop your thoughts in the comments 👇

{' '.join(set(universal_tags + tt_tags + niche_tags))}
"""

        ig_caption = f"""Save this before it disappears 📌

{script.hook}

{script.cta}
Follow @yourchannel for daily mind mastery 🧠

.
.
.
{' '.join(set(universal_tags + ig_tags + niche_tags))}
"""

        return {
            "primary_title": title_variants[0],
            "title_variants": title_variants,
            "youtube": {
                "title": title_variants[0],
                "description": yt_description.strip(),
                "tags": [t.replace("#", "") for t in (universal_tags + yt_tags + niche_tags)]
            },
            "tiktok": {
                "caption": tt_caption.strip()
            },
            "instagram": {
                "caption": ig_caption.strip()
            }
        }
