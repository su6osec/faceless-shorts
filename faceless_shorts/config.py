"""
Configuration and Presets for Faceless Shorts Generator.
"""

from dataclasses import dataclass, field
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
        "recommended_for": ["dark_psychology", "stoicism", "mystery", "horror", "crime"]
    },
    "guy": {
        "id": "en-US-GuyNeural",
        "gender": "male",
        "vibe": "Energetic, engaging, conversational",
        "recommended_for": ["facts", "tech", "lifehacks", "science", "curiosity"]
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
        "recommended_for": ["lifestyle", "social", "motivation", "wholesome"]
    },
    "eric": {
        "id": "en-US-EricNeural",
        "gender": "male",
        "vibe": "Confident, direct, punchy",
        "recommended_for": ["motivation", "finance", "business", "hustle"]
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

# Subtitle Styling Configurations (ASS format colors are &HAABBGGRR in hex)
SUBTITLE_STYLES = {
    "hormozi": {
        "name": "Hormozi Classic",
        "description": "Bold white letters with bright neon yellow highlight and heavy black stroke",
        "font_name": "Arial",
        "font_size": 84,
        "primary_color": "&H00FFFFFF",      # White (Inactive)
        "highlight_color": "&H002BF7&",    # Neon Yellow/Gold (&H00BBGGRR -> BB=00, GG=F7, RR=2B)
        "outline_color": "&H00000000",      # Solid Black Outline
        "back_color": "&H80000000",         # Semi-transparent shadow
        "bold": -1,
        "outline": 6,
        "shadow": 3,
        "alignment": 2,                     # Bottom Center (Alignment 2)
        "margin_v": 680,                    # Centered in lower middle third
        "uppercase": True,
        "words_per_screen": 3
    },
    "neon_cyberpunk": {
        "name": "Cyberpunk Neon",
        "description": "Electric cyan active words over lime green/white text",
        "font_name": "Arial",
        "font_size": 82,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H00FFFF00&",   # Electric Cyan (&H00BBGGRR -> BB=FF, GG=FF, RR=00)
        "outline_color": "&H00220011",
        "back_color": "&HA0000000",
        "bold": -1,
        "outline": 5,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 680,
        "uppercase": True,
        "words_per_screen": 3
    },
    "crimson_alert": {
        "name": "Crimson Alert",
        "description": "Vivid blood-red highlight for horror, thriller, crime, and psychology",
        "font_name": "Arial",
        "font_size": 86,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H001111FF&",   # Blood Red (&H00BBGGRR -> BB=11, GG=11, RR=FF)
        "outline_color": "&H00000000",
        "back_color": "&H90000000",
        "bold": -1,
        "outline": 6,
        "shadow": 3,
        "alignment": 2,
        "margin_v": 680,
        "uppercase": True,
        "words_per_screen": 2
    },
    "beast_pop": {
        "name": "Beast Pop",
        "description": "Electric lime green highlight with vibrant contrast",
        "font_name": "Arial",
        "font_size": 85,
        "primary_color": "&H0000FFFF",      # Bright Yellow base
        "highlight_color": "&H0000FF00&",   # Lime Green highlight
        "outline_color": "&H00000000",
        "back_color": "&H80000000",
        "bold": -1,
        "outline": 7,
        "shadow": 3,
        "alignment": 2,
        "margin_v": 680,
        "uppercase": True,
        "words_per_screen": 3
    },
    "minimalist_gold": {
        "name": "Minimalist Gold",
        "description": "Clean, elegant luxury aesthetic with warm gold accent",
        "font_name": "Arial",
        "font_size": 76,
        "primary_color": "&H00E0E0E0",
        "highlight_color": "&H0050C8E8&",   # Soft Gold
        "outline_color": "&H00151515",
        "back_color": "&H50000000",
        "bold": -1,
        "outline": 4,
        "shadow": 2,
        "alignment": 2,
        "margin_v": 650,
        "uppercase": False,
        "words_per_screen": 4
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
    "stop": "🛑", "rule": "📜", "winner": "🏆", "target": "🎯", "power": "👑"
}

# Ken Burns Motion Effects
KEN_BURNS_PRESETS = [
    "center_zoom_in",
    "center_zoom_out",
    "pan_up",
    "pan_down",
    "subtle_drift"
]
