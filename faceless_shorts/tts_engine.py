"""
Text-to-Speech Engine utilizing Microsoft Edge-TTS.
100% Free, zero API key required, neural quality, with word-boundary timestamp extraction.
"""

import asyncio
import os
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import edge_tts
from faceless_shorts.config import VOICES, DEFAULT_VOICE

@dataclass
class WordTimestamp:
    word: str
    start_sec: float
    end_sec: float
    duration_sec: float

    def to_dict(self) -> Dict:
        return {
            "word": self.word,
            "start": round(self.start_sec, 3),
            "end": round(self.end_sec, 3),
            "duration": round(self.duration_sec, 3)
        }

@dataclass
class AudioResult:
    audio_path: str
    duration_sec: float
    words: List[WordTimestamp]
    text: str

class TTSEngine:
    def __init__(self, default_voice: str = DEFAULT_VOICE):
        self.default_voice = self._resolve_voice(default_voice)

    def _resolve_voice(self, voice_name_or_id: str) -> str:
        """Resolve short name (e.g. 'christopher') to full Edge-TTS voice ID."""
        if voice_name_or_id in VOICES:
            return VOICES[voice_name_or_id]["id"]
        # If it's already a full ID or unknown string, pass through
        return voice_name_or_id

    async def _synthesize_async(
        self,
        text: str,
        voice: str,
        output_path: str,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ) -> AudioResult:
        """Asynchronously synthesize speech and extract word boundaries."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Strip markdown or special characters that confuse TTS
        cleaned_text = re.sub(r"[\*\_#\[\]\(\)]", "", text).strip()
        
        # For Hindi / Indic languages: normalize '।' and '?' to ',' so Edge-TTS neural voices
        # flow smoothly and continuously like a real human without inserting 1.2s dead stops
        if "hi-" in voice or any("\u0900" <= c <= "\u097F" for c in cleaned_text):
            cleaned_text = re.sub(r"[।\?]+", ", ", cleaned_text)
            cleaned_text = re.sub(r",\s*,+", ", ", cleaned_text)
        
        communicate = edge_tts.Communicate(
            text=cleaned_text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch,
            boundary="WordBoundary"
        )

        words: List[WordTimestamp] = []
        raw_audio = bytearray()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                raw_audio.extend(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # offset and duration in 100-nanosecond units (ticks)
                # 1 tick = 0.0000001 seconds = 0.1 microseconds
                start_sec = chunk["offset"] / 10_000_000.0
                duration_sec = chunk["duration"] / 10_000_000.0
                end_sec = start_sec + duration_sec
                word_text = chunk["text"].strip()
                
                if word_text:
                    words.append(WordTimestamp(
                        word=word_text,
                        start_sec=start_sec,
                        end_sec=end_sec,
                        duration_sec=duration_sec
                    ))

        with open(output_path, "wb") as f:
            f.write(raw_audio)

        # Estimate duration from last word timestamp or audio file
        total_duration = words[-1].end_sec + 0.3 if words else 1.0

        return AudioResult(
            audio_path=output_path,
            duration_sec=total_duration,
            words=words,
            text=cleaned_text
        )

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        rate: str = "+0%"
    ) -> AudioResult:
        """Synchronous wrapper for speech synthesis."""
        selected_voice = self._resolve_voice(voice or self.default_voice)
        return asyncio.run(self._synthesize_async(
            text=text,
            voice=selected_voice,
            output_path=output_path,
            rate=rate
        ))

    def synthesize_scenes(
        self,
        scenes: List[Dict],
        output_dir: str,
        voice: Optional[str] = None,
        rate: str = "+5%"
    ) -> List[Tuple[Dict, AudioResult]]:
        """
        Synthesize individual audio clips for a list of scenes.
        Returns list of tuples (scene_data, audio_result).
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        selected_voice = self._resolve_voice(voice or self.default_voice)

        for i, scene in enumerate(scenes):
            audio_filename = f"scene_{i + 1:02d}.mp3"
            audio_path = os.path.join(output_dir, audio_filename)
            res = self.synthesize(
                text=scene["text"],
                output_path=audio_path,
                voice=selected_voice,
                rate=rate
            )
            results.append((scene, res))

        return results
