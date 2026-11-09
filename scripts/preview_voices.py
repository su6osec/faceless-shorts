#!/usr/bin/env python3
"""
Voice Sample Previewer for Faceless Shorts.
Generates 3-second sample audio files for all popular Edge-TTS voices so you can audition them.
Usage: python scripts/preview_voices.py --output-dir voice_previews
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faceless_shorts.config import VOICES
from faceless_shorts.tts_engine import TTSEngine

SAMPLE_PHRASE = "Did you know your brain makes decisions seven seconds before you realize it?"

def main():
    parser = argparse.ArgumentParser(description="Audition Edge-TTS voices.")
    parser.add_argument("-o", "--output-dir", type=str, default="voice_previews", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    engine = TTSEngine()

    print(f"🎙️ Generating voice previews in '{args.output_dir}'...\n")

    for key, info in VOICES.items():
        out_file = os.path.join(args.output_dir, f"{key}_{info['id']}.mp3")
        print(f"  → Synthesizing '{key}' ({info['vibe']})...")
        engine.synthesize(
            text=SAMPLE_PHRASE,
            output_path=out_file,
            voice=info["id"],
            rate="+5%"
        )

    print(f"\n✨ Audition files ready in '{args.output_dir}'! Play them to choose your favorite voice.")

if __name__ == "__main__":
    main()
