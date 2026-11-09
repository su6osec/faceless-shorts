"""
Viral Script Generator for Faceless Shorts.
Generates structured scene-by-scene scripts optimized for high retention on YouTube Shorts, Instagram Reels, and TikTok.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class Scene:
    index: int
    text: str
    visual_prompt: str
    motion: str = "center_zoom_in"
    duration_estimate: float = 5.0

@dataclass
class VideoScript:
    title: str
    niche: str
    target_duration: int
    hook: str
    scenes: List[Scene]
    cta: str
    tags: List[str]

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "niche": self.niche,
            "target_duration": self.target_duration,
            "hook": self.hook,
            "scenes": [asdict(s) for s in self.scenes],
            "cta": self.cta,
            "tags": self.tags,
            "full_text": " ".join(s.text for s in self.scenes)
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoScript':
        scenes = [Scene(**s) for s in data.get("scenes", [])]
        return cls(
            title=data.get("title", "Untitled Short"),
            niche=data.get("niche", "general"),
            target_duration=data.get("target_duration", 45),
            hook=data.get("hook", ""),
            scenes=scenes,
            cta=data.get("cta", ""),
            tags=data.get("tags", [])
        )

# Built-in High-Retention Viral Presets (100% Offline, Ready to Produce Immediately)
VIRAL_TEMPLATES = {
    "dark_psychology": VideoScript(
        title="3 Dark Psychology Tricks People Use On You",
        niche="dark_psychology",
        target_duration=45,
        hook="If someone stares at your forehead while you speak, they are doing this on purpose.",
        scenes=[
            Scene(
                index=1,
                text="If someone stares at your forehead while you speak, they are doing this on purpose.",
                visual_prompt="cinematic close up of mysterious shadowy eyes in dark room, intense gaze, dramatic rim lighting, photorealistic 8k vertical wallpaper",
                motion="center_zoom_in"
            ),
            Scene(
                index=2,
                text="It makes you feel deeply insecure and completely shatters your train of thought.",
                visual_prompt="silhouette of a stressed person holding their head in hands, dark moody neon lighting, psychological thriller atmosphere, vertical composition",
                motion="pan_down"
            ),
            Scene(
                index=3,
                text="Second is the silent pause. When they want you to over-explain a lie, they simply stay quiet and keep looking at you.",
                visual_prompt="two shadowy figures across an interrogation table, dramatic smoky lighting, cinema noir style, ultra sharp 8k vertical",
                motion="center_zoom_out"
            ),
            Scene(
                index=4,
                text="Humans naturally hate silence, so they rush to fill the gap with confessions.",
                visual_prompt="hourglass with glowing dark sand running out, ominous clockwork background, macro photorealistic vertical shot",
                motion="center_zoom_in"
            ),
            Scene(
                index=5,
                text="And the most dangerous one? Artificial scarcity of affection. They pull away to make you obsess.",
                visual_prompt="a golden glowing marionette puppet with severed strings in dark void, mystical hyperrealistic lighting, 8k vertical wallpaper",
                motion="subtle_drift"
            ),
            Scene(
                index=6,
                text="Remember, aware minds are impossible to control. Drop a follow if you refuse to be manipulated.",
                visual_prompt="ancient glowing marble statue of stoic philosopher, dark stormy lightning background, cinematic epic lighting, 8k vertical",
                motion="center_zoom_in"
            )
        ],
        cta="Drop a follow if you refuse to be manipulated.",
        tags=["#darkpsychology", "#mindtricks", "#psychologyfacts", "#manipulation", "#shorts"]
    ),

    "stoicism": VideoScript(
        title="Marcus Aurelius' Rule To Never Get Angry",
        niche="stoicism",
        target_duration=40,
        hook="Whenever you are offended by someone's lack of respect, ask yourself this one question.",
        scenes=[
            Scene(
                index=1,
                text="Whenever you are offended by someone's lack of respect, ask yourself this one question.",
                visual_prompt="majestic roman emperor marcus aurelius marble bust, cinematic moody lighting, ancient pillars and storm clouds, 8k vertical masterpiece",
                motion="center_zoom_in"
            ),
            Scene(
                index=2,
                text="Is it possible for shameless people not to exist in this world? Absolutely not.",
                visual_prompt="ancient roman colosseum during turbulent thunderstorm, dramatic cinematic lighting, hyperrealistic vertical composition",
                motion="pan_up"
            ),
            Scene(
                index=3,
                text="So why do you expect the impossible? You have encountered one of those inevitable fools.",
                visual_prompt="lone stoic warrior standing on a mountain cliff, violent wind, calm face, dramatic sunset lighting, photorealistic vertical",
                motion="center_zoom_out"
            ),
            Scene(
                index=4,
                text="You cannot control the storm outside, but you have absolute power over your inner stillness.",
                visual_prompt="calm glowing bonsai tree inside a raging glass sphere amidst tempest, surreal hyperrealistic lighting, 8k vertical",
                motion="subtle_drift"
            ),
            Scene(
                index=5,
                text="Do not hand over the steering wheel of your emotions to people who cannot even control themselves.",
                visual_prompt="bronze ancient compass resting on old leather map, golden warm cinematic glow, photorealistic vertical macro shot",
                motion="center_zoom_in"
            )
        ],
        cta="Subscribe to master your mind.",
        tags=["#stoicism", "#marcusaurelius", "#philosophy", "#mindset", "#discipline", "#shorts"]
    ),

    "mind_blowing_facts": VideoScript(
        title="3 Terrifying Space Facts That Keep Scientists Awake",
        niche="mind_blowing_facts",
        target_duration=45,
        hook="There are rogue planets hurtling through pitch-black space right now with no star.",
        scenes=[
            Scene(
                index=1,
                text="There are rogue planets hurtling through pitch-black space right now with no star.",
                visual_prompt="lone frozen dark rogue planet wandering through deep interstellar abyss, faint distant starlight, cinematic photorealistic 8k vertical",
                motion="center_zoom_in"
            ),
            Scene(
                index=2,
                text="Billions of these celestial phantoms drift freely, completely undetected until they enter a solar system.",
                visual_prompt="vast majestic galaxy spiral with ominous dark nebulae, cosmic dust clouds, deep space photography 8k vertical wallpaper",
                motion="pan_down"
            ),
            Scene(
                index=3,
                text="Even stranger, the Boötes Void is a 330 million light-year expanse of almost complete emptiness.",
                visual_prompt="a colossal terrifying cosmic void surrounded by glittering web of galaxies, James Webb style space telescope vertical image",
                motion="center_zoom_out"
            ),
            Scene(
                index=4,
                text="Scientists still cannot explain why such a massive region of the universe has virtually no galaxies.",
                visual_prompt="futuristic astronaut looking out of spacecraft window into deep dark cosmos, visor reflection of stars, cinematic 8k vertical",
                motion="subtle_drift"
            ),
            Scene(
                index=5,
                text="If humanity disappeared tomorrow, the universe would not even blink. Which cosmic secret scares you the most?",
                visual_prompt="earth floating in silent infinite darkness, tiny blue dot, cinematic epic NASA style photorealistic vertical shot",
                motion="center_zoom_in"
            )
        ],
        cta="Which cosmic secret scares you the most?",
        tags=["#spacefacts", "#universe", "#cosmicmystery", "#astronomy", "#didyouknow", "#shorts"]
    )
}

LLM_SYSTEM_PROMPT = """You are an elite short-form video scriptwriter who crafts viral YouTube Shorts, Instagram Reels, and TikTok scripts with over 70% average percentage viewed (APV).

RULES:
1. Pacing: Total spoken words must be between 90 and 140 words (~40-55 seconds).
2. The Hook (0-3s): Must trigger intense curiosity, fear of missing out, or a pattern interrupt. Never start with "Hello" or "Today we will discuss".
3. Scene Breakdown: Split the script into 4-7 punchy scenes.
4. Visual Prompts: For each scene, create a hyper-descriptive prompt for AI image generation (vertical 9:16, photorealistic, dramatic lighting, 8k).
5. Seamless Ending: End with an open-ended engagement question or a seamless loop phrase.

Output ONLY valid JSON formatted as follows:
{
  "title": "Viral Click-Worthy Title",
  "niche": "niche_name",
  "target_duration": 45,
  "hook": "Opening hook sentence",
  "scenes": [
    {
      "index": 1,
      "text": "First punchy spoken sentence.",
      "visual_prompt": "Cinematic visual prompt for image generator, photorealistic 8k vertical wallpaper",
      "motion": "center_zoom_in"
    }
  ],
  "cta": "Final call to action or question",
  "tags": ["#shorts", "#viral", "#niche"]
}
"""

def get_template(niche: str) -> Optional[VideoScript]:
    """Retrieve a pre-built viral script template by niche."""
    return VIRAL_TEMPLATES.get(niche)

def create_custom_script(title: str, niche: str, scenes_data: List[Dict]) -> VideoScript:
    """Build a VideoScript object from custom scene definitions."""
    scenes = [
        Scene(
            index=i + 1,
            text=s["text"],
            visual_prompt=s.get("visual_prompt", f"cinematic scene depicting {s['text'][:50]}, 8k vertical wallpaper"),
            motion=s.get("motion", "center_zoom_in")
        )
        for i, s in enumerate(scenes_data)
    ]
    hook = scenes[0].text if scenes else ""
    return VideoScript(
        title=title,
        niche=niche,
        target_duration=len(scenes) * 7,
        hook=hook,
        scenes=scenes,
        cta=scenes[-1].text if scenes else "",
        tags=[f"#{niche.replace('_', '')}", "#shorts", "#viral", "#fyp"]
    )
