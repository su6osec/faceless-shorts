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
    # English Voices
    "christopher": {
        "id": "en-US-ChristopherNeural",
        "gender": "male",
        "vibe": "Deep, mysterious, authoritative",
        "language": "en",
        "recommended_for": ["dark_psychology", "stoicism", "mystery", "horror", "fitness"]
    },
    "guy": {
        "id": "en-US-GuyNeural",
        "gender": "male",
        "vibe": "Energetic, engaging, conversational",
        "language": "en",
        "recommended_for": ["facts", "tech", "lifehacks", "science", "motivation"]
    },
    "aria": {
        "id": "en-US-AriaNeural",
        "gender": "female",
        "vibe": "Clear, professional, articulate",
        "language": "en",
        "recommended_for": ["documentary", "history", "educational", "storytelling"]
    },
    "jenny": {
        "id": "en-US-JennyNeural",
        "gender": "female",
        "vibe": "Natural, youthful, friendly",
        "language": "en",
        "recommended_for": ["lifestyle", "social", "relationships", "wholesome"]
    },
    "eric": {
        "id": "en-US-EricNeural",
        "gender": "male",
        "vibe": "Confident, direct, punchy",
        "language": "en",
        "recommended_for": ["motivation", "finance", "business", "hustle", "fitness"]
    },
    "ryan": {
        "id": "en-GB-RyanNeural",
        "gender": "male",
        "vibe": "Sophisticated British accent, cinematic",
        "language": "en",
        "recommended_for": ["history", "nature", "mythology", "philosophy"]
    },
    "sonia": {
        "id": "en-GB-SoniaNeural",
        "gender": "female",
        "vibe": "Refined British female, storytelling",
        "language": "en",
        "recommended_for": ["true_crime", "drama", "literature"]
    },
    # Hindi Voices
    "madhur": {
        "id": "hi-IN-MadhurNeural",
        "gender": "male",
        "vibe": "Hindi native expressive, motivational & authoritative tone",
        "language": "hi",
        "recommended_for": ["facts", "motivation", "desi_trivia", "fitness", "stoicism"]
    },
    "swara": {
        "id": "hi-IN-SwaraNeural",
        "gender": "female",
        "vibe": "Hindi native smooth storytelling & educational tone",
        "language": "hi",
        "recommended_for": ["stories", "mythology", "educational", "relationships"]
    },
    # Spanish Voices
    "alvaro": {
        "id": "es-ES-AlvaroNeural",
        "gender": "male",
        "vibe": "Spanish (Spain) expressive, punchy energetic",
        "language": "es",
        "recommended_for": ["curiosidades", "psicologia", "motivacion", "fitness"]
    },
    "elvira": {
        "id": "es-ES-ElviraNeural",
        "gender": "female",
        "vibe": "Spanish (Spain) clear, engaging narrator",
        "language": "es",
        "recommended_for": ["historias", "documental", "educacion"]
    },
    "jorge": {
        "id": "es-MX-JorgeNeural",
        "gender": "male",
        "vibe": "Spanish (Latin America / Mexico) warm & captivating",
        "language": "es",
        "recommended_for": ["shorts_latam", "historias", "misterio"]
    },
    # French Voices
    "henri": {
        "id": "fr-FR-HenriNeural",
        "gender": "male",
        "vibe": "French authoritative & cinematic narrator",
        "language": "fr",
        "recommended_for": ["philosophie", "faits", "motivation"]
    },
    "denise": {
        "id": "fr-FR-DeniseNeural",
        "gender": "female",
        "vibe": "French warm, elegant storytelling",
        "language": "fr",
        "recommended_for": ["culture", "histoire", "developpement"]
    },
    # German Voices
    "conrad": {
        "id": "de-DE-ConradNeural",
        "gender": "male",
        "vibe": "German deep, focused, disciplined tone",
        "language": "de",
        "recommended_for": ["psychologie", "fitness", "wissen"]
    },
    "katja": {
        "id": "de-DE-KatjaNeural",
        "gender": "female",
        "vibe": "German articulate & confident speaker",
        "language": "de",
        "recommended_for": ["fakten", "business", "lifestyle"]
    },
    # Portuguese Voices
    "antonio": {
        "id": "pt-BR-AntonioNeural",
        "gender": "male",
        "vibe": "Brazilian Portuguese engaging & motivational",
        "language": "pt",
        "recommended_for": ["motivacao", "curiosidades", "treino"]
    },
    "francisca": {
        "id": "pt-BR-FranciscaNeural",
        "gender": "female",
        "vibe": "Brazilian Portuguese natural & friendly",
        "language": "pt",
        "recommended_for": ["historias", "saude", "dicas"]
    },
    # Japanese Voices
    "keita": {
        "id": "ja-JP-KeitaNeural",
        "gender": "male",
        "vibe": "Japanese dramatic anime / cinematic narrator",
        "language": "ja",
        "recommended_for": ["anime", "facts", "mystery", "philosophy"]
    },
    "nanami": {
        "id": "ja-JP-NanamiNeural",
        "gender": "female",
        "vibe": "Japanese calm, crystal clear narration",
        "language": "ja",
        "recommended_for": ["storytelling", "mindfulness", "history"]
    },
    # Arabic Voices
    "hamed": {
        "id": "ar-SA-HamedNeural",
        "gender": "male",
        "vibe": "Arabic authoritative, resonant classical tone",
        "language": "ar",
        "recommended_for": ["facts", "history", "motivation", "wisdom"]
    },
    "zariyah": {
        "id": "ar-SA-ZariyahNeural",
        "gender": "female",
        "vibe": "Arabic expressive & articulate narrator",
        "language": "ar",
        "recommended_for": ["culture", "stories", "education"]
    },
    # Russian Voices
    "dmitry": {
        "id": "ru-RU-DmitryNeural",
        "gender": "male",
        "vibe": "Russian deep, intense, cinematic",
        "language": "ru",
        "recommended_for": ["psychology", "facts", "strength"]
    },
    "svetlana": {
        "id": "ru-RU-SvetlanaNeural",
        "gender": "female",
        "vibe": "Russian clear, engaging storytelling",
        "language": "ru",
        "recommended_for": ["history", "science", "lifestyle"]
    },
    # Italian Voices
    "diego": {
        "id": "it-IT-DiegoNeural",
        "gender": "male",
        "vibe": "Italian passionate, engaging speaker",
        "language": "it",
        "recommended_for": ["storia", "curiosita", "crescita"]
    },
    "elsa": {
        "id": "it-IT-ElsaNeural",
        "gender": "female",
        "vibe": "Italian smooth, elegant narrator",
        "language": "it",
        "recommended_for": ["documentario", "arte", "benessere"]
    },
    # Indonesian Voices
    "ardi": {
        "id": "id-ID-ArdiNeural",
        "gender": "male",
        "vibe": "Indonesian punchy, energetic creator tone",
        "language": "id",
        "recommended_for": ["fakta", "motivasi", "horor"]
    },
    "gadis": {
        "id": "id-ID-GadisNeural",
        "gender": "female",
        "vibe": "Indonesian natural, friendly narration",
        "language": "id",
        "recommended_for": ["cerita", "edukasi", "hiburan"]
    }
}

DEFAULT_VOICE = "en-US-ChristopherNeural"

# Multi-Language Catalog with Native Fonts and Voice Defaults
LANGUAGES = {
    "en": {
        "name": "English",
        "default_voice": "christopher",
        "voices": ["christopher", "guy", "aria", "eric", "ryan", "jenny", "sonia"],
        "recommended_font": "Arial Black"
    },
    "hi": {
        "name": "Hindi (हिंदी)",
        "default_voice": "madhur",
        "voices": ["madhur", "swara"],
        "recommended_font": "Kohinoor Devanagari"
    },
    "es": {
        "name": "Spanish (Español)",
        "default_voice": "alvaro",
        "voices": ["alvaro", "elvira", "jorge"],
        "recommended_font": "Arial Black"
    },
    "fr": {
        "name": "French (Français)",
        "default_voice": "henri",
        "voices": ["henri", "denise"],
        "recommended_font": "Arial Black"
    },
    "de": {
        "name": "German (Deutsch)",
        "default_voice": "conrad",
        "voices": ["conrad", "katja"],
        "recommended_font": "Arial Black"
    },
    "pt": {
        "name": "Portuguese (Português)",
        "default_voice": "antonio",
        "voices": ["antonio", "francisca"],
        "recommended_font": "Arial Black"
    },
    "ja": {
        "name": "Japanese (日本語)",
        "default_voice": "keita",
        "voices": ["keita", "nanami"],
        "recommended_font": "Hiragino Sans"
    },
    "ar": {
        "name": "Arabic (العربية)",
        "default_voice": "hamed",
        "voices": ["hamed", "zariyah"],
        "recommended_font": "Geeza Pro"
    },
    "ru": {
        "name": "Russian (Русский)",
        "default_voice": "dmitry",
        "voices": ["dmitry", "svetlana"],
        "recommended_font": "Arial Black"
    },
    "it": {
        "name": "Italian (Italiano)",
        "default_voice": "diego",
        "voices": ["diego", "elsa"],
        "recommended_font": "Arial Black"
    },
    "id": {
        "name": "Indonesian (Bahasa Indonesia)",
        "default_voice": "ardi",
        "voices": ["ardi", "gadis"],
        "recommended_font": "Arial Black"
    }
}
DEFAULT_LANGUAGE = "en"

# High-Retention Visual Scene Transitions
TRANSITIONS = {
    "flash": {
        "name": "White Flash Cut",
        "description": "High-retention 0.22s white flash cut (#1 viral effect on TikTok & Shorts)",
        "xfade_name": "fadewhite",
        "duration": 0.22
    },
    "crossfade": {
        "name": "Cinematic Crossfade",
        "description": "Smooth 0.25s cinematic dissolve between scenes",
        "xfade_name": "fade",
        "duration": 0.25
    },
    "slide": {
        "name": "Dynamic Slide Left",
        "description": "Fast kinetic whip slide left transition",
        "xfade_name": "slideleft",
        "duration": 0.22
    },
    "wipe": {
        "name": "Graphic Wipe Left",
        "description": "Clean graphic wipe transition",
        "xfade_name": "wipeleft",
        "duration": 0.22
    },
    "cut": {
        "name": "Hard Cut",
        "description": "Instant 0ms cut between scenes without transition overlap",
        "xfade_name": None,
        "duration": 0.0
    },
    "zoom": {
        "name": "Impact Zoom-In",
        "description": "Hard punch zoom-in cut (MrBeast style scene impact)",
        "xfade_name": "zoomin",
        "duration": 0.30
    },
    "dissolve": {
        "name": "Dream Dissolve",
        "description": "Frame-scrambling dissolve for flashback & mind-bend moments",
        "xfade_name": "dissolve",
        "duration": 0.28
    },
    "pixelize": {
        "name": "Pixel Mosaic",
        "description": "8-bit pixel mosaic transition (pairs with pixel_art / PS2 styles)",
        "xfade_name": "pixelize",
        "duration": 0.28
    },
    "radial": {
        "name": "Radial Burst",
        "description": "Circular radial reveal sweeping from center",
        "xfade_name": "radial",
        "duration": 0.25
    },
    "circle": {
        "name": "Iris Circle Open",
        "description": "Camera-iris circle open (retro cartoon reveal)",
        "xfade_name": "circleopen",
        "duration": 0.25
    },
    "blur": {
        "name": "Whip Blur",
        "description": "Directional motion-blur whip (high-speed camera pan feel)",
        "xfade_name": "hblur",
        "duration": 0.32
    },
    "black": {
        "name": "Fade To Black",
        "description": "Dramatic fade to black beat-drop cut",
        "xfade_name": "fadeblack",
        "duration": 0.30
    },
    "smooth": {
        "name": "Smooth Glide",
        "description": "Eased smooth slide for premium documentary pacing",
        "xfade_name": "smoothleft",
        "duration": 0.30
    },
    "diag": {
        "name": "Diagonal Slice",
        "description": "Diagonal comic-panel slice (pairs with comic_art style)",
        "xfade_name": "diagbl",
        "duration": 0.22
    },
    "squeeze": {
        "name": "Elastic Squeeze",
        "description": "Vertical elastic squeeze (playful / toy styles)",
        "xfade_name": "squeezev",
        "duration": 0.28
    },
    "wind": {
        "name": "Glitch Wind",
        "description": "Horizontal wind-shear glitch wipe (cyberpunk & VHS looks)",
        "xfade_name": "hlwind",
        "duration": 0.26
    },
    "gray": {
        "name": "Bleach Fade",
        "description": "Desaturating fade-to-gray emotional transition",
        "xfade_name": "fadegrays",
        "duration": 0.30
    }
}
DEFAULT_TRANSITION = "flash"

# Motion Graphics & Retention Progress Bar Defaults
PROGRESS_BAR_CONFIG = {
    "enabled": True,
    "height": 8,
    "y": 1912,
    "default_color": "0x2BF7FF@0.95",  # Electric cyan glow
    "colors_by_style": {
        "hormozi": "0x2BF7FF@0.95",        # Cyan on yellow
        "beast_pop": "0x00FF00@0.95",      # Neon lime
        "neon_cyberpunk": "0xFF00FF@0.95", # Electric magenta
        "crimson_alert": "0x2222FF@0.95",  # Deep crimson red
        "sketch_comic": "0x00D4FF@0.95",   # Amber gold
        "minimalist_gold": "0x50C8E8@0.95",# Champagne gold
        "neon_glow": "0x00FFFF@0.95",      # Pure neon cyan
        "chalk_classic": "0xFFE9B3@0.95",  # Chalk yellow
        "retro_pop": "0xFF66CC@0.95",      # Hot pink
        "pixel_arcade": "0x40FF00@0.95",   # Phosphor green
        "luxury_cinema": "0x7AC8E8@0.95",  # Champagne gold
        "horror_bleed": "0x3333FF@0.95",   # Blood red
        "glow_blur": "0x00FFFF@0.95"       # Glow neon cyan
    }
}

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
    },
    "neon_glow": {
        "name": "Neon Glow",
        "description": "Electric cyan neon tubes with soft bloom blur on the active word",
        "font_name": "Arial Black",
        "font_size": 90,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H00FFFF00&",   # Electric cyan (&H00BBGGRR)
        "outline_color": "&H003B1E00",      # Deep indigo outline
        "back_color": "&H99000000",
        "bold": -1,
        "outline": 6,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 118,
        "glow_blur": 7,
        "glow_color": "&H00FFFF00&"
    },
    "chalk_classic": {
        "name": "Chalk Classic",
        "description": "Hand-written chalkboard lettering (pairs with the chalkboard art style)",
        "font_name": "Chalkboard SE",
        "font_size": 86,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H0055E0FF&",   # Chalk yellow (&H00BBGGRR -> BB=55 GG=E0 RR=FF)
        "outline_color": "&H00202020",
        "back_color": "&H88000000",
        "bold": -1,
        "outline": 4,
        "shadow": 3,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": False,
        "words_per_screen": 3,
        "scale_bounce": 112,
        "glow_blur": 2
    },
    "retro_pop": {
        "name": "Retro Pop",
        "description": "Bubbly rounded lettering with hot-pink pop highlight (toy & fun styles)",
        "font_name": "Arial Rounded MT Bold",
        "font_size": 92,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H0066CCFF&",   # Hot pink (&H00BBGGRR -> BB=66 GG=CC RR=FF)
        "outline_color": "&H00330011",
        "back_color": "&H99000000",
        "bold": -1,
        "outline": 7,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 122
    },
    "pixel_arcade": {
        "name": "Pixel Arcade",
        "description": "Monospaced arcade-cabinet typography with phosphor-green highlight",
        "font_name": "Courier New",
        "font_size": 84,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H0000FF40&",   # Phosphor green
        "outline_color": "&H00000000",
        "back_color": "&HAA000000",
        "bold": -1,
        "outline": 5,
        "shadow": 3,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 110,
        "glow_blur": 5,
        "glow_color": "&H0000FF40&"
    },
    "luxury_cinema": {
        "name": "Luxury Cinema",
        "description": "Refined serif title-card typography with champagne highlight",
        "font_name": "Georgia",
        "font_size": 84,
        "primary_color": "&H00F5F0E8",
        "highlight_color": "&H007AC8E8&",   # Champagne gold
        "outline_color": "&H00101010",
        "back_color": "&H70000000",
        "bold": -1,
        "outline": 3,
        "shadow": 4,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": False,
        "words_per_screen": 4,
        "scale_bounce": 108
    },
    "horror_bleed": {
        "name": "Horror Bleed",
        "description": "Distressed blood-red warning type for true-crime & horror",
        "font_name": "American Typewriter",
        "font_size": 90,
        "primary_color": "&H00E8E8E8",
        "highlight_color": "&H001111FF&",   # Blood red
        "outline_color": "&H00000000",
        "back_color": "&HA0000000",
        "bold": -1,
        "outline": 6,
        "shadow": 6,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 2,
        "scale_bounce": 116,
        "glow_blur": 4,
        "glow_color": "&H001111FF&"
    },
    "glow_blur": {
        "name": "Neon Glow Blur",
        "description": "Soft-blurred neon halo on active words (TikTok glow-text trend)",
        "font_name": "Arial Black",
        "font_size": 88,
        "primary_color": "&H00FFFFFF",
        "highlight_color": "&H00FFFF00&",   # Electric cyan highlight
        "outline_color": "&H00201000",
        "back_color": "&H90000000",
        "bold": -1,
        "outline": 5,
        "shadow": 5,
        "alignment": 2,
        "margin_v": 700,
        "uppercase": True,
        "words_per_screen": 3,
        "scale_bounce": 118,
        "glow_blur": 8,
        "glow_color": "&H00FFFF00&"
    }
}

# Artistic Video Editing Styles for High-Retention Social Media Trends.
# Three-stage styling engine:
#   1. prompt_suffix -> injected into the AI image prompt (Pollinations Flux / ComfyUI)
#   2. pixel_op      -> offline PIL transformation (faceless_shorts.style_processor)
#   3. ffmpeg_filter -> linear FFmpeg grade applied during Ken Burns motion render
# Categories drive the `art-styles` CLI listing.
ART_STYLES = {
    # ---------------------------------------------------------------- CINEMATIC
    "hyperreal": {
        "name": "Hyperrealistic Cinematic",
        "category": "cinematic",
        "description": "Photorealistic 8k octane render with dramatic volumetric lighting",
        "prompt_suffix": "cinematic photorealistic, dramatic studio lighting, 8k vertical wallpaper, octane render, shallow depth of field, 9:16 vertical orientation",
        "ffmpeg_filter": "eq=contrast=1.08:saturation=1.06"
    },
    "cinematic_noir": {
        "name": "Moody Film Noir",
        "category": "cinematic",
        "description": "Extreme chiaroscuro shadows with warm amber rim light (David Fincher style)",
        "prompt_suffix": "cinematic film noir, deep dramatic shadows, intense chiaroscuro lighting, moody amber rim highlights, 35mm anamorphic lens, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.35:brightness=-0.04:saturation=0.9,vignette=PI/3"
    },
    "old_style": {
        "name": "Vintage 35mm / 80s Retro Film",
        "category": "cinematic",
        "description": "Nostalgic 1970s/1980s Kodachrome analog film look with grain and warm vignette",
        "prompt_suffix": "vintage 1970s 35mm film photograph, Kodak Portra 400, analog film grain, retro cinema, nostalgic Kodachrome warm palette, cinematic still, 8k vertical",
        "ffmpeg_filter": "curves=vintage,vignette=PI/3.5,noise=alls=15:allf=t+u,eq=saturation=0.85:contrast=1.15"
    },
    "cyberpunk_glitch": {
        "name": "Cyberpunk Neon Glitch",
        "category": "cinematic",
        "description": "Dark futuristic aesthetic with electric cyan/magenta rim glow and high contrast",
        "prompt_suffix": "dark cyberpunk noir, neon cyan and magenta volumetric rim lighting, dystopian sci-fi aesthetic, Unreal Engine 5 render, 8k vertical wallpaper",
        "ffmpeg_filter": "eq=saturation=1.4:contrast=1.25,unsharp=5:5:1.2,vignette=PI/4"
    },
    "teal_orange": {
        "name": "Blockbuster Teal & Orange",
        "category": "cinematic",
        "description": "Hollywood action-movie grade: crushed teal shadows and warm skin-tone highlights",
        "prompt_suffix": "cinematic blockbuster movie still, teal and orange color grade, dramatic rim lighting, 35mm anamorphic, 8k vertical",
        "ffmpeg_filter": "curves=preset=medium_contrast,colorbalance=rs=0.05:bs=-0.06:rm=0.03:bm=-0.05,eq=saturation=1.12"
    },
    "anamorphic_epic": {
        "name": "Anamorphic Epic",
        "category": "cinematic",
        "description": "Wide-lens IMAX feel with strong contrast, subtle flare and vignette",
        "prompt_suffix": "epic IMAX anamorphic film still, horizontal lens flare, immense scale, deep contrast, atmospheric haze, 8k vertical",
        "ffmpeg_filter": "curves=preset=strong_contrast,eq=saturation=1.05:contrast=1.08,vignette=PI/6,noise=alls=5:allf=t+u"
    },
    "documentary": {
        "name": "Clean Documentary",
        "category": "cinematic",
        "description": "Natural National Geographic grade: honest color, gentle contrast",
        "prompt_suffix": "award-winning documentary photography, natural available light, honest realistic color, 8k vertical",
        "ffmpeg_filter": "curves=preset=linear_contrast,eq=saturation=0.96:brightness=0.01,unsharp=5:5:0.5"
    },
    "noir_bw": {
        "name": "Monochrome Noir",
        "category": "cinematic",
        "description": "High-contrast black & white with heavy grain and hard vignette",
        "prompt_suffix": "high contrast black and white photograph, hard shadows, film noir lighting, 35mm grain, 8k vertical",
        "ffmpeg_filter": "format=gray,curves=preset=strong_contrast,noise=alls=8:allf=t+u,vignette=PI/3"
    },
    "neon_noir": {
        "name": "Neon Noir",
        "category": "cinematic",
        "description": "Rain-slicked night city: magenta/cyan neon through deep black shadows",
        "prompt_suffix": "neon noir night scene, rain-slicked streets, magenta and cyan neon reflections, deep black shadows, cinematic 8k vertical",
        "ffmpeg_filter": "curves=preset=strong_contrast,rgbashift=rh=3:bh=-3,eq=saturation=1.3,vignette=PI/4"
    },

    # ----------------------------------------------------------- ILLUSTRATION
    "sketch": {
        "name": "Manga / Inked Pencil Sketch",
        "category": "illustration",
        "description": "Detailed black & white manga graphic novel sketch with heavy ink hatching",
        "prompt_suffix": "detailed inked manga sketch, black and white graphite line art, dark cross-hatching, dramatic comic aesthetic, graphic novel style, 8k vertical wallpaper",
        "ffmpeg_filter": "format=gray,curves=increase_contrast,unsharp=luma_msize_x=7:luma_msize_y=7:luma_amount=2.2,noise=alls=12:allf=t+u"
    },
    "chalkboard": {
        "name": "Chalkboard Doodle",
        "category": "illustration",
        "description": "White & yellow chalk drawing on a dusty dark slate blackboard",
        "prompt_suffix": "chalk drawing on black chalkboard, white and yellow chalk strokes, dusty texture, hand-lettered doodle, dark slate background, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.12:saturation=0.9,noise=alls=6:allf=t+u,boxblur=1:1",
        "pixel_op": "chalkboard"
    },
    "glow_sketch": {
        "name": "Glow Sketch",
        "category": "illustration",
        "description": "Electric neon doodle linework glowing on near-black canvas",
        "prompt_suffix": "glowing neon line sketch, luminous hand-drawn strokes on dark background, electric blue and magenta glow, hand-drawn doodle, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.1:saturation=1.2,unsharp=5:5:0.7,noise=alls=4:allf=t+u",
        "pixel_op": "glow_sketch"
    },
    "comic_art": {
        "name": "Comic Book Art",
        "category": "illustration",
        "description": "Bold ink outlines, flat colors and halftone dot print texture",
        "prompt_suffix": "comic book panel, bold ink outlines, halftone dots, flat saturated colors, pop art, graphic novel style, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.15:contrast=1.1,unsharp=5:5:0.7",
        "pixel_op": "comic_halftone"
    },
    "flat_vector": {
        "name": "Flat Vector / Infographic",
        "category": "illustration",
        "description": "Clean geometric flat-vector illustration (corporate memphis explainer look)",
        "prompt_suffix": "flat vector illustration, clean geometric shapes, solid fills, minimal shading, corporate memphis style, 2D, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.15:contrast=1.06",
        "pixel_op": "flat_vector"
    },
    "minimal_line": {
        "name": "Minimal Line Art",
        "category": "illustration",
        "description": "Single-weight continuous line drawing with generous negative space",
        "prompt_suffix": "single continuous line art, minimal line drawing, black lines on white, elegant line illustration, lots of negative space, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.05",
        "pixel_op": "minimal_line"
    },
    "watercolor": {
        "name": "Watercolor Painting",
        "category": "illustration",
        "description": "Wet-on-wet watercolor bleed on textured paper",
        "prompt_suffix": "watercolor painting, wet-on-wet pigment bleed, paper texture, soft edges, artistic, vibrant washes, 8k vertical",
        "ffmpeg_filter": "gblur=sigma=2,eq=saturation=1.15",
        "pixel_op": "watercolor"
    },
    "oil_painting": {
        "name": "Oil Painting",
        "category": "illustration",
        "description": "Thick impasto oil brushwork with painterly flattening",
        "prompt_suffix": "oil painting on canvas, thick impasto brush strokes, visible palette knife texture, museum masterpiece, 8k vertical",
        "ffmpeg_filter": "unsharp=5:5:0.5,eq=saturation=1.1",
        "pixel_op": "oil_painting"
    },
    "pop_art": {
        "name": "Pop Art (Lichtenstein)",
        "category": "illustration",
        "description": "Ben-Day dots, screaming primary colors and heavy ink lines",
        "prompt_suffix": "pop art in the style of Roy Lichtenstein, ben-day dots, bold primary colors, heavy black outlines, comic panel, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.25:contrast=1.15",
        "pixel_op": "pop_art"
    },
    "blueprint": {
        "name": "Engineering Blueprint",
        "category": "illustration",
        "description": "Cyanotype technical drawing: white line work on deep blueprint blue",
        "prompt_suffix": "engineering blueprint drawing, white technical line work on deep blue cyanotype paper, precise schematic, grid, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.08",
        "pixel_op": "blueprint"
    },
    "anime": {
        "name": "Anime Cel Shading",
        "category": "illustration",
        "description": "Vibrant studio-anime key visual with crisp cel shading",
        "prompt_suffix": "anime artwork, key visual, cel shading, vibrant anime coloring, clean line art, studio quality, 8k vertical",
        "ffmpeg_filter": "unsharp=5:5:0.9:5:5:0.0,eq=saturation=1.3:contrast=1.1,noise=alls=3:allf=u"
    },
    "storybook": {
        "name": "Storybook Illustration",
        "category": "illustration",
        "description": "Warm hand-painted children's storybook page",
        "prompt_suffix": "children's storybook illustration, warm hand-painted gouache, soft rounded shapes, charming whimsical, 8k vertical",
        "ffmpeg_filter": "curves=preset=lighter,eq=saturation=1.1:brightness=0.015,noise=alls=4:allf=u"
    },
    "ink_wash": {
        "name": "Sumi-e Ink Wash",
        "category": "illustration",
        "description": "Traditional Japanese sumi-e brush painting with flowing ink gradients",
        "prompt_suffix": "traditional japanese sumi-e ink wash painting, flowing black ink brush strokes, rice paper texture, minimalist zen, 8k vertical",
        "ffmpeg_filter": "eq=saturation=0.6:contrast=1.2,curves=preset=medium_contrast,noise=alls=5:allf=u"
    },

    # --------------------------------------------------------- RETRO / GAMES
    "pixel_art": {
        "name": "Pixel Art (16-bit)",
        "category": "retro",
        "description": "Chunky 16-bit sprites with a locked limited palette",
        "prompt_suffix": "pixel art, 16-bit, blocky, limited palette, crisp pixels, dithering, retro game sprite, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.2:contrast=1.1,unsharp=5:5:0.6",
        "pixel_op": "pixel_art"
    },
    "ps2_style": {
        "name": "PS2 Console Era",
        "category": "retro",
        "description": "Sixth-gen console look: low-res textures, soft aliasing, 2002 bloom",
        "prompt_suffix": "playstation 2 era render, low poly, low resolution textures, vertex colors, aliased edges, 2002 console graphics, 8k vertical",
        "ffmpeg_filter": "eq=saturation=0.98:contrast=1.1,noise=alls=7:allf=t",
        "pixel_op": "ps2_style"
    },
    "crt_retro": {
        "name": "CRT Found Footage",
        "category": "retro",
        "description": "VHS camcorder tape with chroma bleed, scanlines and tape noise",
        "prompt_suffix": "1990s VHS camcorder footage, analog tape degradation, chroma bleed, camcorder viewfinder, found footage, 8k vertical",
        "ffmpeg_filter": "rgbashift=rh=2:bh=-2,noise=alls=10:allf=t,vignette=PI/4,curves=preset=increase_contrast"
    },
    "vaporwave": {
        "name": "Vaporwave / Synthwave",
        "category": "retro",
        "description": "80s retrowave: chrome, grid horizons and pastel teal-pink gradient",
        "prompt_suffix": "vaporwave aesthetic, 80s retro-futurism, synthwave grid horizon, chrome typography, pastel pink and teal, sunset, 8k vertical",
        "ffmpeg_filter": "colortemperature=temperature=8500:mix=0.4,eq=saturation=1.3,rgbashift=rh=4:bh=-4"
    },
    "low_poly": {
        "name": "Low-Poly 3D",
        "category": "retro",
        "description": "Faceted polygon mesh with flat shading",
        "prompt_suffix": "low-poly style, polygon mesh, jagged facets, flat shading, triangulated 3d render, 8k vertical",
        "ffmpeg_filter": "curves=preset=medium_contrast,eq=contrast=1.15:saturation=1.18,unsharp=5:5:0.4"
    },
    "game_boy": {
        "name": "Handheld Retro (Game Boy)",
        "category": "retro",
        "description": "4-shade portable-console green LCD look",
        "prompt_suffix": "retro handheld game console screen, 4 shade green LCD palette, dot matrix display, 8-bit game, 8k vertical",
        "ffmpeg_filter": "hue=s=0.35,eq=contrast=1.25:brightness=0.04,colorchannelmixer=gg=1.2:rr=0.75:bb=0.75",
        "pixel_op": "pixel_art"
    },
    "voxel_art": {
        "name": "Voxel Craft",
        "category": "retro",
        "description": "Blocky cube-world voxel build with chunky isometric lighting",
        "prompt_suffix": "voxel art, blocky cube world, minecraft-inspired chunky geometry, bright saturated colors, isometric 3d render, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.25:contrast=1.12,unsharp=5:5:0.6"
    },
    "lego": {
        "name": "LEGO Brick Build",
        "category": "retro",
        "description": "Glossy ABS plastic brick sculpture with studded surfaces",
        "prompt_suffix": "lego brick sculpture, plastic studs, glossy ABS plastic toy photography, bright primary colors, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.3:contrast=1.1,unsharp=5:5:0.6",
        "pixel_op": "lego_studs"
    },

    # ------------------------------------------------------ 3D / MOTION GRAPHICS
    "cgi_motion": {
        "name": "CGI Motion Graphics",
        "category": "motion_3d",
        "description": "Octane-grade 3D motion-graphics render with glossy materials",
        "prompt_suffix": "octane render, 3d motion graphics, glossy materials, studio lighting, soft shadows, depth of field, highly detailed, 8k vertical",
        "ffmpeg_filter": "curves=preset=medium_contrast,eq=saturation=1.22:contrast=1.05,unsharp=5:5:0.5,vignette=PI/6"
    },
    "explainer_3d": {
        "name": "Explainer 3D",
        "category": "motion_3d",
        "description": "Friendly soft-clay explainer video aesthetic with pastel palette",
        "prompt_suffix": "claymation 3d characters, soft rounded shapes, pastel palette, isometric friendly explainer video style, soft global illumination, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.2:brightness=0.025,unsharp=5:5:0.4"
    },
    "isometric_3d": {
        "name": "Isometric Diorama",
        "category": "motion_3d",
        "description": "Tiny 3/4-view diorama world with tilt-shift focus",
        "prompt_suffix": "isometric style, tiny detailed diorama, 3/4 view, crisp details, centered composition, tilt-shift photography, 8k vertical",
        "ffmpeg_filter": "curves=preset=medium_contrast,eq=saturation=1.18,vignette=PI/5"
    },
    "claymation": {
        "name": "Claymation Stop-Motion",
        "category": "motion_3d",
        "description": "Handmade plasticine stop-motion with visible fingerprint texture",
        "prompt_suffix": "claymation stop motion, handmade plasticine characters, visible clay texture, fingerprint details, aardman style, 8k vertical",
        "ffmpeg_filter": "gblur=sigma=1,eq=saturation=1.2:contrast=1.05,noise=alls=5:allf=u"
    },
    "product_render": {
        "name": "Luxury Product Render",
        "category": "motion_3d",
        "description": "Premium studio product shot with softbox falloff and deep vignette",
        "prompt_suffix": "luxury product render, studio softbox lighting, seamless backdrop, premium commercial photography, glossy reflections, 8k vertical",
        "ffmpeg_filter": "curves=preset=medium_contrast,eq=contrast=1.1:saturation=1.06,vignette=PI/5,unsharp=5:5:0.6"
    },

    # ------------------------------------------------------- TEXTURE / CRAFT
    "paper_craft": {
        "name": "Torn Paper Collage Scrapbook",
        "category": "texture",
        "description": "Viral Vox/MagnatesMedia style textured papercraft collage with raw torn edges",
        "prompt_suffix": "torn paper collage artwork, textured vintage papercraft, mixed media scrapbook cutout, rough torn edges, handmade layered paper collage, 8k vertical",
        "ffmpeg_filter": "eq=saturation=0.75:contrast=1.25,noise=alls=22:allf=u"
    },
    "riso": {
        "name": "Risograph Print",
        "category": "texture",
        "description": "Two-color riso poster with misregistration and grainy ink",
        "prompt_suffix": "risograph print, two spot colors, visible ink grain, slight misregistration, zine poster, 8k vertical",
        "ffmpeg_filter": "noise=alls=14:allf=u,eq=saturation=1.25:contrast=1.1"
    },
    "halftone_news": {
        "name": "Newspaper Halftone",
        "category": "texture",
        "description": "Retro newsprint: coarse black halftone dots on aged paper",
        "prompt_suffix": "vintage newspaper photograph, coarse halftone dot print, aged newsprint, front page exposure, 8k vertical",
        "ffmpeg_filter": "format=gray,eq=contrast=1.25:brightness=0.03,noise=alls=8:allf=u",
        "pixel_op": "comic_halftone"
    },
    "steampunk": {
        "name": "Steampunk Victorian",
        "category": "texture",
        "description": "Brass gears, leather and steam-era machinery in warm sepia",
        "prompt_suffix": "steampunk victorian machinery, brass gears, copper pipes, leather, warm sepia light, detailed, 8k vertical",
        "ffmpeg_filter": "curves=preset=vintage,eq=saturation=1.12:contrast=1.1,unsharp=5:5:0.5"
    },
    "stained_glass": {
        "name": "Stained Glass Window",
        "category": "texture",
        "description": "Backlit cathedral stained glass with leaded black cames",
        "prompt_suffix": "stained glass window artwork, leaded black outlines, backlit saturated jewel colors, cathedral rose window, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.3:contrast=1.15,unsharp=5:5:0.5"
    },
    "ukiyo_e": {
        "name": "Ukiyo-e Woodblock",
        "category": "texture",
        "description": "Edo-period Japanese woodblock print with flat color and paper grain",
        "prompt_suffix": "ukiyo-e japanese woodblock print, edo period, flat color areas, wood grain texture, hokusai style, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.12:contrast=1.05,noise=alls=6:allf=u"
    },

    # --------------------------------------------------------- NEON / FUTURE
    "neon_glow": {
        "name": "Neon Glow",
        "category": "neon_future",
        "description": "Tube-light neon signage blooming against dark brick",
        "prompt_suffix": "bright neon glow signage, volumetric light bloom, dark background, electric magenta and cyan, night photography, 8k vertical",
        "ffmpeg_filter": "eq=contrast=1.2:saturation=1.3,rgbashift=rh=2:bh=-2,noise=alls=4:allf=t"
    },
    "synthwave": {
        "name": "Synthwave Duotone",
        "category": "neon_future",
        "description": "Magenta-to-cyan gradient map with CRT scanlines",
        "prompt_suffix": "synthwave retro future, neon grid, chrome sports car, sunset gradient, 80s arcade poster, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.2:contrast=1.1,noise=alls=5:allf=t+u",
        "pixel_op": "synthwave_duotone"
    },
    "hologram": {
        "name": "Hologram / Sci-Fi HUD",
        "category": "neon_future",
        "description": "Flickering cyan holographic projection with data scanlines",
        "prompt_suffix": "glowing cyan hologram projection, sci-fi holographic interface, scan lines, floating volumetric light, dark room, 8k vertical",
        "ffmpeg_filter": "eq=saturation=1.25:contrast=1.15,rgbashift=rh=2:gh=0:bh=-2,vignette=PI/4,noise=alls=6:allf=t"
    },
    "matrix_code": {
        "name": "Digital Rain Matrix",
        "category": "neon_future",
        "description": "Terminal-green cascading code with CRT glow",
        "prompt_suffix": "cascading digital rain code, matrix green terminal text, dark cyberpunk server room, crt glow, 8k vertical",
        "ffmpeg_filter": "hue=s=0.5,eq=contrast=1.25:brightness=-0.02,colorchannelmixer=gg=1.25:rr=0.5:bb=0.6,noise=alls=5:allf=t"
    }
}

# Ordered category registry for CLI listings
ART_STYLE_CATEGORIES = {
    "cinematic": "🎬 Cinematic & Photoreal",
    "illustration": "🎨 Illustration & Art",
    "retro": "🕹️ Retro & Games",
    "motion_3d": "🧊 3D & Motion Graphics",
    "texture": "📰 Texture & Craft",
    "neon_future": "⚡ Neon & Future"
}

# Render-quality profiles: fps / x264 CRF / encoder preset / audio bitrate / canvas
QUALITY_PROFILES = {
    "draft": {
        "fps": 24, "crf": 26, "preset": "ultrafast",
        "audio_bitrate": "128k", "width": 1080, "height": 1920
    },
    "social": {
        "fps": 30, "crf": 21, "preset": "faster",
        "audio_bitrate": "160k", "width": 1080, "height": 1920
    },
    "hd": {
        "fps": 30, "crf": 18, "preset": "medium",
        "audio_bitrate": "192k", "width": 1080, "height": 1920
    },
    "cinematic": {
        "fps": 60, "crf": 17, "preset": "medium",
        "audio_bitrate": "192k", "width": 1080, "height": 1920
    },
    "ultra": {
        "fps": 60, "crf": 15, "preset": "slow",
        "audio_bitrate": "256k", "width": 1440, "height": 2560
    }
}
DEFAULT_QUALITY = "social"

# Image generation engines (all 100% free). `procedural` is the offline fallback.
IMAGE_ENGINES = {
    "pollinations": "Pollinations.ai Flux (free, keyless cloud)",
    "comfyui": "Local ComfyUI (github.com/comfyanonymous/ComfyUI, free & private)",
    "procedural": "Offline procedural Pillow canvas (zero network)"
}
DEFAULT_IMAGE_ENGINE = "pollinations"

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
    "vertigo_shake",
    "whip_zoom",
    "rise_up",
    "orbit_sway",
    "pulse_heartbeat",
    "shockwave_out"
]
