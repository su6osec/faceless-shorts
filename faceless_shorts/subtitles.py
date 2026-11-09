"""
Subtitle Generation Module for Faceless Shorts.
Generates viral, word-synced ASS (Advanced SubStation Alpha) subtitles with:
- Chunking (2-4 words per screen)
- Karaoke active-word color highlights (Hormozi, Cyberpunk, Crimson, Beast, Minimalist)
- Automatic context emoji injection
- Uppercase bold high-contrast styling
"""

import math
import os
import re
from typing import List, Dict, Optional, Tuple
from faceless_shorts.config import SUBTITLE_STYLES, EMOJI_KEYWORDS, CANVAS_WIDTH, CANVAS_HEIGHT
from faceless_shorts.tts_engine import WordTimestamp

def format_ass_time(seconds: float) -> str:
    """Format float seconds to ASS timestamp format: H:MM:SS.cc"""
    if seconds < 0:
        seconds = 0
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

    def _get_emoji_for_word(self, word: str) -> Optional[str]:
        """Find matching emoji based on keyword lookup."""
        cleaned = re.sub(r"[^\w]", "", word).lower()
        return EMOJI_KEYWORDS.get(cleaned)

    def generate_ass_script(
        self,
        words: List[WordTimestamp],
        output_ass_path: str,
        start_offset: float = 0.0,
        enable_emojis: bool = True
    ) -> str:
        """
        Generate ASS file with word-by-word karaoke highlights across chunks.
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

        # Split words into chunks of N words
        chunk_size = self.words_per_screen
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

        for chunk in chunks:
            # Check for emoji inside chunk
            chunk_emoji = ""
            if enable_emojis:
                for w in chunk:
                    em = self._get_emoji_for_word(w.word)
                    if em:
                        chunk_emoji = f" {em}"
                        break

            # Create an event for each word within the chunk where that word is highlighted
            for active_idx, active_word in enumerate(chunk):
                w_start = active_word.start_sec + start_offset
                w_end = active_word.end_sec + start_offset
                
                # Expand slightly to prevent tiny gaps between words
                if active_idx < len(chunk) - 1:
                    next_start = chunk[active_idx + 1].start_sec + start_offset
                    if next_start > w_end and (next_start - w_end) < 0.15:
                        w_end = next_start

                start_str = format_ass_time(w_start)
                end_str = format_ass_time(w_end)

                # Assemble chunk text with active word highlighted
                parts = []
                for idx, w in enumerate(chunk):
                    display_text = w.word.upper() if self.uppercase else w.word
                    if idx == active_idx:
                        # Highlighted word with color override tag
                        parts.append(f"{{\\c{highlight_color}}}{display_text}{{\\c{primary_color}}}")
                    else:
                        parts.append(display_text)

                line_payload = " ".join(parts) + chunk_emoji
                line = f"Dialogue: 0,{start_str},{end_str},Main,,0,0,0,,{line_payload}"
                dialogue_lines.append(line)

        with open(output_ass_path, "w", encoding="utf-8-sig") as f:
            f.write(header + "\n".join(dialogue_lines) + "\n")

        return output_ass_path

    def generate_srt(
        self,
        words: List[WordTimestamp],
        output_srt_path: str,
        start_offset: float = 0.0
    ) -> str:
        """Fallback SRT generator for standard players and captions."""
        os.makedirs(os.path.dirname(os.path.abspath(output_srt_path)), exist_ok=True)
        chunks = [words[i:i + self.words_per_screen] for i in range(0, len(words), self.words_per_screen)]
        srt_lines = []

        for idx, chunk in enumerate(chunks):
            start_sec = chunk[0].start_sec + start_offset
            end_sec = chunk[-1].end_sec + start_offset
            
            s_h = int(start_sec // 3600)
            s_m = int((start_sec % 3600) // 60)
            s_s = int(start_sec % 60)
            s_ms = int(round((start_sec - int(start_sec)) * 1000))

            e_h = int(end_sec // 3600)
            e_m = int((end_sec % 3600) // 60)
            e_s = int(end_sec % 60)
            e_ms = int(round((end_sec - int(end_sec)) * 1000))

            time_header = f"{s_h:02d}:{s_m:02d}:{s_s:02d},{s_ms:03d} --> {e_h:02d}:{e_m:02d}:{e_s:02d},{e_ms:03d}"
            text = " ".join(w.word for w in chunk)
            if self.uppercase:
                text = text.upper()

            srt_lines.append(f"{idx + 1}\n{time_header}\n{text}\n")

        with open(output_srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))

        return output_srt_path
