#!/usr/bin/env python3
"""
Batch Video Producer for Faceless Shorts.
Generates an entire week or month of content across multiple niches automatically.
Usage: python scripts/batch_generate.py --count 3 --output-dir batch_output
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faceless_shorts.script_generator import VIRAL_TEMPLATES
from faceless_shorts.renderer import VideoRenderer
from faceless_shorts.metadata import MetadataOptimizer

def main():
    parser = argparse.ArgumentParser(description="Batch generate vertical faceless videos.")
    parser.add_argument("-c", "--count", type=int, default=3, help="Number of videos to generate")
    parser.add_argument("-o", "--output-dir", type=str, default="batch_output", help="Directory for output videos")
    parser.add_argument("--offline", action="store_true", help="Use procedural backgrounds for ultra-fast generation")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    niches = list(VIRAL_TEMPLATES.keys())
    optimizer = MetadataOptimizer()

    print(f"🎬 Starting batch production of {args.count} videos...\n")
    start_total = time.time()

    for idx in range(args.count):
        niche = niches[idx % len(niches)]
        script = VIRAL_TEMPLATES[niche]
        out_video = os.path.join(args.output_dir, f"short_{idx+1:02d}_{niche}.mp4")
        
        print(f"==================================================")
        print(f"▶️ [{idx+1}/{args.count}] Producing Short: '{script.title}' ({niche})")
        print(f"==================================================")

        voice = "christopher" if "dark" in niche or "stoic" in niche else "guy"
        style = "hormozi" if "psychology" in niche else "minimalist_gold"

        renderer = VideoRenderer(
            voice=voice,
            subtitle_style=style,
            work_dir=f".batch_render_temp_{idx+1}"
        )

        renderer.render(
            script=script,
            output_mp4_path=out_video,
            enable_ai_images=not args.offline
        )

        metadata = optimizer.generate_metadata(script)
        meta_file = out_video.replace(".mp4", "_metadata.json")
        with open(meta_file, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ Video {idx+1} complete: {out_video}\n")

    total_time = time.time() - start_total
    print(f"🎉 Batch generation finished! {args.count} videos produced in {total_time:.1f}s.")
    print(f"📁 Check '{args.output_dir}' for your ready-to-post videos and metadata.")

if __name__ == "__main__":
    main()
