"""
Configuration and Presets for Faceless Shorts Generator.
"""

from typing import Dict, List, Optional

# Video Canvas Defaults (Vertical 9:16)
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
DEFAULT_FPS = 30

# Curated High-Fidelity Edge-TTS Voices (100% Free, No API Key Required)
VOICES = {
    "christopher": {
        "id": "en-US-ChristopherNeural",
        "gender": "male",
        "vibe": "Deep, mysterious, authoritative",
        "recommended_for": ["dark_psychology", "stoicism", "mystery", "horror", "fitness"]
    },
    "guy": {
        "id": "en-US-GuyNeural",
        "gender": "male",
        "vibe": "Energetic, engaging, conversational",
        "recommended_for": ["facts", "tech", "lifehacks", "science", "motivation"]
    },
    "aria": {
        "id": "en-US-AriaNeural",
        "gender": "female",
        "vibe": "Clear, professional, articulate",
        "recommended_for": ["documentary", "history", "educational", "storytelling"]
    },
    "jenny": {
        "id": "en-US-JennyNeural",
        "gender": "female",
        "vibe": "Natural, youthful, friendly",
        "recommended_for": ["lifestyle", "social", "relationships", "wholesome"]
    },
    "eric": {
        "id": "en-US-EricNeural",
        "gender": "male",
        "vibe": "Confident, direct, punchy",
        "recommended_for": ["motivation", "finance", "business", "hustle", "fitness"]
    },
    "ryan": {
        "id": "en-GB-RyanNeural",
        "gender": "male",
        "vibe": "Sophisticated British accent, cinematic",
        "recommended_for": ["history", "nature", "mythology", "philosophy"]
    },
    "sonia": {
        "id": "en-GB-SoniaNeural",
        "gender": "female",
        "vibe": "Refined British female, storytelling",
        "recommended_for": ["true_crime", "drama", "literature"]
    },
    "madhur": {
        "id": "hi-IN-MadhurNeural",
        "gender": "male",
        "vibe": "Indian English / Hindi expressive tone",
        "recommended_for": ["facts", "motivation", "desi_trivia"]
    },
    "swara": {
        "id": "hi-IN-SwaraNeural",
        "gender": "female",
        "vibe": "Indian English / Hindi smooth storytelling",
        "recommended_for": ["stories", "mythology", "educational"]
    },
    "alvaro": {
        "id": "es-ES-AlvaroNeural",
        "gender": "male",
        "vibe": "Spanish native, expressive",
        "recommended_for": ["spanish_shorts", "curiosidades"]
    }
}

DEFAULT_VOICE = "en-US-ChristopherNeural"

# Premium Subtitle Styling with Scale Bounce Animation & Heavy Stroke
# Colors in ASS format are &HAABBGGRR in hex
SUBTITLE_STYLES = {
    "hormozi": {
        "name": "Hormozi Classic",
        "description": "Bold Arial Black, bright neon yellow highlight, heavy 7px black outline with active bounce",
        "font_name": "Arial Black",
        "font_size": 90,
        "primary_color": "&H00FFFFFF",      # Crisp White
        "highlight_color": "&H002BF7&",    # Neon Yellow/Gold (&H00BBGGRR -> BB=00, GG=F7, RR=2B)
        "outline_color": "&H00000000",      # Solid Black Outline
        "back_color": "&H90000000",         # Deep Shadow
        "bold": -1,
        "outline": 7,
        "shadow": 4,
        "alignment": 2,                     # Bottom Center
        "margin_v": 700,                    # Centered in lower middle third
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 118                 # 118% pop scale on active word
    },
    "beast_pop": {
        "name": "Beast Pop",
        "description": "Electric Impact font, neon lime green highlight with vibrant contrast",
        "font_name": "Impact",
        "font_size": 94,
        "primary_color": "&H0000FFFF",      # Bright Yellow base
        "highlight_color": "&H0000FF00&",   # Lime Green highlight
        "outline_color": "&H00000000",
        "back_color": "&H90000000",
        "bold": -1,
        "outline": 8,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 120
    },
    "neon_cyberpunk": {
        "name": "Cyberpunk Neon",
        "description": "Electric cyan active words over crisp white with purple shadow glow",
        "font_name": "Arial Black",
        "font_size": 88,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H00FFFF00&",   # Electric Cyan (&H00BBGGRR -> BB=FF, GG=FF, RR=00)
        "outline_color": "&H00220011",
        "back_color": "&HB0000000",
        "bold": -1,
        "outline": 6,
        "shadow": 5,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 115
    },
    "crimson_alert": {
        "name": "Crimson Alert",
        "description": "Vivid blood-red highlight for horror, thriller, crime, and psychology",
        "font_name": "Arial Black",
        "font_size": 92,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H001111FF&",   # Blood Red (&H00BBGGRR -> BB=11, GG=11, RR=FF)
        "outline_color": "&H00000000",
        "back_color": "&H95000000",
        "bold": -1,
        "outline": 7,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 2,
        "scale_bounce": 120
    },
    "sketch_comic": {
        "name": "Sketch Comic",
        "description": "Inked graphic novel subtitle with high-contrast comic stroke",
        "font_name": "Impact",
        "font_size": 92,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H0000D4FF&",   # Warm Amber Yellow
        "outline_color": "&H00000000",
        "back_color": "&H99000000",
        "bold": -1,
        "outline": 8,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 115
    },
    "minimalist_gold": {
        "name": "Minimalist Gold",
        "description": "Clean, elegant luxury aesthetic with warm gold accent",
        "font_name": "Helvetica Neue",
        "font_size": 82,
        "primary_color": "&H00E0E0E0",
        "highlight_color": "&H0050C8E8&",   # Soft Gold
        "outline_color": "&H00151515",
        "back_color": "&H60000000",
        "bold": -1,
        "outline": 4,
        "shadow": 3,
        "alignment": 2,
        "margin_v": 680,
        "uppercase": False,
        "words_per_screen": 4,
        "scale_bounce": 110
    }
}

# Artistic Video Editing Styles for High-Retention Social Media Trends
ART_STYLES = {
    "hyperreal": {
        "name": "Hyperrealistic Cinematic",
        "description": "Photorealistic 8k octane render with dramatic volumetric lighting",
        "prompt_suffix": "cinematic photorealistic, dramatic studio lighting, 8k vertical wallpaper, octane render, shallow depth of field, 9:16 vertical orientation",
        "ffmpeg_filter": "eq=contrast=1.08:saturation=1.06"
    },
    "sketch": {
        "name": "Manga / Inked Pencil Sketch",
        "description": "Detailed black & white manga graphic novel sketch with heavy ink hatching",
        "prompt_suffix": "detailed inked manga sketch, black and white graphite line art, dark cross-hatching, dramatic comic aesthetic, graphic novel style, 8k vertical wallpaper",
        "ffmpeg_filter": "format=gray,curves=increase_contrast,unsharp=luma_msize_x=7:luma_msize_y=7:luma_amount=2.2,noise=alls=12:allf=t+u"
    },
    "old_style": {
        "name": "Vintage 35mm / 80s Retro Film",
        "description": "Nostalgic 1970s/1980s Kodachrome analog film look with grain and warm vignette",
        "prompt_suffix": "vintage 1970s 35mm film photograph, Kodak Portra 400, analog film grain, retro cinema, nostalgic Kodachrome warm palette, cinematic still, 8k vertical",
        "ffmpeg_filter": "curves=vintage,vignette=PI/3.5,noise=alls=15:allf=t+u,eq=saturation=0.85:contrast=1.15"
    },
    "paper_craft": {
        "name": "Torn Paper Collage Scrapbook",
        "description": "Viral Vox/MagnatesMedia style textured papercraft collage with raw torn edges",
        "prompt_suffix": "torn paper collage artwork, textured vintage papercraft, mixed media scrapbook cutout, rough torn edges, handmade layered paper collage, 8k vertical",
        "ffmpeg_filter": "eq=saturation=0.75:contrast=1.25,noise=alls=22:allf=u"
    },
    "cyberpunk_glitch": {
        "name": "Cyberpunk Neon Glitch",
        "description": "Dark futuristic aesthetic with electric cyan/magenta rim glow and high contrast",
        "prompt_suffix": "dark cyberpunk noir, neon cyan and magenta volumetric rim lighting, dystopian sci-fi aesthetic, Unreal Engine 5 render, 8k vertical wallpaper",
        "ffmpeg_filter": "eq=saturation=1.4:contrast=1.25,unsharp=5:5:1.2,vignette=PI/4"
    },
    "cinematic_noir": {
        "name": "Moody Film Noir",
        "description": "Extreme chiaroscuro shadows with warm amber rim light (David Fincher style)",
        "prompt_suffix": "cinematic film noir, deep dramatic shadows, intense chiaroscuro lighting, moody amber rim highlights, 35mm anamorphic lens, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.35:brightness=-0.04:saturation=0.9,vignette=PI/3"
    }
}

# Auto-Emoji keyword triggers
EMOJI_KEYWORDS = {
    "brain": "🧠", "mind": "🧠", "think": "🧠", "psychology": "🧠", "memory": "🧠",
    "dead": "💀", "death": "💀", "kill": "💀", "danger": "⚠️", "warning": "⚠️",
    "money": "💰", "cash": "💵", "rich": "🤑", "wealth": "💎", "crypto": "🪙",
    "fire": "🔥", "hot": "🔥", "burn": "🔥", "insane": "🤯", "shocking": "😱",
    "time": "⏳", "second": "⏱️", "hour": "⏰", "clock": "⌛", "history": "📜",
    "dark": "🌑", "secret": "🤫", "mystery": "🕵️", "lie": "🤥", "truth": "👁️",
    "space": "🚀", "earth": "🌍", "universe": "🌌", "star": "✨", "future": "⚡",
    "heart": "❤️", "love": "❤️", "fear": "😨", "demon": "😈", "ghost": "👻",
    "stop": "🛑", "rule": "📜", "winner": "🏆", "target": "🎯", "power": "👑",
    "muscle": "💪", "gym": "🏋️", "workout": "💪", "strong": "⚡", "weight": "🏋️"
}

# Punchy Ken Burns Dynamic Motions
KEN_BURNS_PRESETS = [
    "punch_zoom_in",
    "dramatic_zoom_out",
    "pan_left",
    "pan_right",
    "vertigo_shake"
]
