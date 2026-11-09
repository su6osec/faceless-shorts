"""
Subtitle Generation Module for Faceless Shorts.
Generates viral, word-synced ASS (Advanced SubStation Alpha) subtitles with:
- Word chunking (2-3 words per screen for high retention)
- Dynamic popping scale bounce (118%) on each spoken word
- Premium typography (Arial Black, Impact, Helvetica Neue)
- High-contrast thick black outline and drop shadow
"""

import math
import os
import re
from typing import List, Dict, Optional, Tuple
from faceless_shorts.config import SUBTITLE_STYLES, CANVAS_WIDTH, CANVAS_HEIGHT
from faceless_shorts.tts_engine import WordTimestamp

def format_ass_time(seconds: float) -> str:
    """Format float seconds to ASS timestamp format: H:MM:SS.cc"""
    if seconds < 0:
        seconds = 0.0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int(round((seconds - int(seconds)) * 100))
    if centisecs >= 100:
        centisecs = 99
    return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

class SubtitleGenerator:
    def __init__(self, style_name: str = "hormozi"):
        self.style_config = SUBTITLE_STYLES.get(style_name, SUBTITLE_STYLES["hormozi"])
        self.words_per_screen = self.style_config.get("words_per_screen", 3)
        self.uppercase = self.style_config.get("uppercase", True)
        self.scale_bounce = self.style_config.get("scale_bounce", 118)

    def generate_ass_script(
        self,
        words: List[WordTimestamp],
        output_ass_path: str,
        start_offset: float = 0.0
    ) -> str:
        """
        Generate ASS file with word-by-word karaoke highlights and active-word scale bounce.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
        
        cfg = self.style_config
        font_name = cfg["font_name"]
        font_size = cfg["font_size"]
        primary_color = cfg["primary_color"]
        highlight_color = cfg["highlight_color"]
        outline_color = cfg["outline_color"]
        back_color = cfg["back_color"]
        bold = cfg["bold"]
        outline = cfg["outline"]
        shadow = cfg["shadow"]
        alignment = cfg["alignment"]
        margin_v = cfg["margin_v"]
        bounce = self.scale_bounce

        header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {CANVAS_WIDTH}
PlayResY: {CANVAS_HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{font_name},{font_size},{primary_color},&H000000FF,{outline_color},{back_color},{bold},0,0,0,100,100,1,0,1,{outline},{shadow},{alignment},50,50,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        dialogue_lines: List[str] = []
        if not words:
            with open(output_ass_path, "w", encoding="utf-8-sig") as f:
                f.write(header)
            return output_ass_path

        # Split words into chunks of N words (2-3 words per screen)
        chunk_size = self.words_per_screen
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

        for chunk in chunks:
            # Create an event for each word within the chunk where that word is highlighted & popped
            for active_idx, active_word in enumerate(chunk):
                w_start = active_word.start_sec + start_offset
                w_end = active_word.end_sec + start_offset
                
                # Expand slightly to prevent tiny gaps between consecutive words
                if active_idx < len(chunk) - 1:
                    next_start = chunk[active_idx + 1].start_sec + start_offset
                    if next_start > w_end and (next_start - w_end) < 0.18:
                        w_end = next_start

                start_str = format_ass_time(w_start)
                end_str = format_ass_time(w_end)

                # Assemble chunk text with active word scaled up and highlighted
                parts = []
                for idx, w in enumerate(chunk):
                    # Clean punctuation from display while maintaining readability
                    cleaned_word = re.sub(r"[\*\_#\[\]]", "", w.word).strip()
                    display_text = cleaned_word.upper() if self.uppercase else cleaned_word
                    
                    if idx == active_idx:
                        # Active popping word with scale bounce and highlight color
                        parts.append(
                            f"{{\\fscx{bounce}\\fscy{bounce}\\c{highlight_color}}}"
                            f"{display_text}"
                            f"{{\\fscx100\\fscy100\\c{primary_color}}}"
                        )
                    else:
                        parts.append(display_text)

                line_payload = " ".join(parts)
                line = f"Dialogue: 0,{start_str},{end_str},Main,,0,0,0,,{line_payload}"
                dialogue_lines.append(line)

        with open(output_ass_path, "w", encoding="utf-8-sig") as f:
            f.write(header + "\n".join(dialogue_lines) + "\n")

        return output_ass_path
