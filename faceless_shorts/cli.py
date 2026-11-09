"""
Command Line Interface for Faceless Shorts.
Author: su6osec (https://github.com/su6osec)
"""

import argparse
import json
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from faceless_shorts.config import VOICES, SUBTITLE_STYLES
from faceless_shorts.script_generator import VIRAL_TEMPLATES, get_template, VideoScript, LLM_SYSTEM_PROMPT
from faceless_shorts.renderer import VideoRenderer
from faceless_shorts.metadata import MetadataOptimizer

console = Console()

def print_banner():
    console.print("""[bold magenta]
  ███████╗ █████╗  ██████╗███████╗██╗     ███████╗███████╗███████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝██║     ██╔════╝██╔════╝██╔════╝
  █████╗  ███████║██║     █████╗  ██║     █████╗  ███████╗███████╗
  ██╔══╝  ██╔══██║██║     ██╔══╝  ██║     ██╔══╝  ╚════██║╚════██║
  ██║     ██║  ██║╚██████╗███████╗███████╗███████╗███████║███████║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝
    [bold yellow]⚡ 100% Free AI Faceless Video Generator for Shorts, Reels & TikTok ⚡[/bold yellow]
    [dim cyan]Maintained by su6osec • https://github.com/su6osec/faceless-shorts[/dim cyan]
[/bold magenta]""")

def list_voices():
    table = Table(title="🎙️ Supported Free Edge-TTS Voices", header_style="bold cyan")
    table.add_column("Shortcut", style="bold green", width=12)
    table.add_column("Voice ID", style="yellow")
    table.add_column("Gender", width=8)
    table.add_column("Vibe & Description")
    table.add_column("Best Niches", style="dim")

    for key, v in VOICES.items():
        table.add_row(
            key,
            v["id"],
            v["gender"],
            v["vibe"],
            ", ".join(v["recommended_for"])
        )
    console.print(table)

def list_styles():
    table = Table(title="🎨 Viral Subtitle Styles", header_style="bold magenta")
    table.add_column("Style Name", style="bold green", width=16)
    table.add_column("Title", style="yellow")
    table.add_column("Description")
    table.add_column("Words/Screen", justify="center", width=14)

    for key, s in SUBTITLE_STYLES.items():
        table.add_row(
            key,
            s["name"],
            s["description"],
            str(s["words_per_screen"])
        )
    console.print(table)

def list_presets():
    table = Table(title="📜 Pre-built Viral Templates", header_style="bold blue")
    table.add_column("Niche / Key", style="bold green", width=20)
    table.add_column("Video Title", style="yellow")
    table.add_column("Scenes", justify="center", width=8)
    table.add_column("Opening Hook")

    for key, t in VIRAL_TEMPLATES.items():
        table.add_row(
            key,
            t.title,
            str(len(t.scenes)),
            t.hook[:60] + "..."
        )
    console.print(table)

def run_generate(args):
    print_banner()

    # Determine the script
    script: VideoScript = None

    if args.script_json and os.path.exists(args.script_json):
        console.print(f"[cyan]Loading script from JSON file: {args.script_json}[/cyan]")
        with open(args.script_json, "r") as f:
            data = json.load(f)
        script = VideoScript.from_dict(data)
    elif args.niche and args.niche in VIRAL_TEMPLATES:
        console.print(f"[cyan]Using viral preset template: '{args.niche}'[/cyan]")
        script = get_template(args.niche)
    else:
        # Check if topic matches a preset
        matched = None
        if args.topic:
            topic_lower = args.topic.lower()
            if "psychology" in topic_lower or "manipulat" in topic_lower or "trick" in topic_lower:
                matched = "dark_psychology"
            elif "stoic" in topic_lower or "aurelius" in topic_lower or "anger" in topic_lower:
                matched = "stoicism"
            elif "space" in topic_lower or "science" in topic_lower or "fact" in topic_lower:
                matched = "mind_blowing_facts"

        if matched:
            console.print(f"[cyan]Auto-detected best viral preset: '{matched}'[/cyan]")
            script = get_template(matched)
        else:
            # Fallback to dark_psychology template if no topic given
            console.print("[cyan]Defaulting to viral 'dark_psychology' template...[/cyan]")
            script = get_template("dark_psychology")

    console.print(Panel(
        f"[bold white]Title:[/bold white] {script.title}\n"
        f"[bold white]Niche:[/bold white] {script.niche}\n"
        f"[bold white]Scenes:[/bold white] {len(script.scenes)}\n"
        f"[bold white]Opening Hook:[/bold white] [yellow]\"{script.hook}\"[/yellow]\n"
        f"[bold white]Voice:[/bold white] {args.voice}\n"
        f"[bold white]Subtitle Style:[/bold white] {args.style}\n"
        f"[bold white]AI Images:[/bold white] {'Disabled (Offline Mode)' if args.offline else 'Enabled (Pollinations Flux)'}",
        title="🎬 Production Brief",
        border_style="green"
    ))

    # Initialize renderer
    output_path = args.output or f"output/{script.niche}_short.mp4"
    renderer = VideoRenderer(
        voice=args.voice,
        subtitle_style=args.style,
        bg_music_preset=args.music,
        speech_rate=args.rate,
        work_dir=".temp_render"
    )

    rendered_file = renderer.render(
        script=script,
        output_mp4_path=output_path,
        enable_ai_images=not args.offline
    )

    # Generate metadata
    optimizer = MetadataOptimizer()
    metadata = optimizer.generate_metadata(script)
    meta_path = output_path.replace(".mp4", "_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    console.print(Panel(
        f"[bold green]Video Rendered Successfully![/bold green]\n\n"
        f"🎥 [bold]Video Path:[/bold] {os.path.abspath(rendered_file)}\n"
        f"📊 [bold]Metadata Path:[/bold] {os.path.abspath(meta_path)}\n\n"
        f"[bold yellow]YouTube Title:[/bold yellow] {metadata['youtube']['title']}\n"
        f"[bold yellow]TikTok Caption:[/bold yellow] {metadata['tiktok']['caption'][:80]}...\n"
        f"[bold yellow]Tags:[/bold yellow] {' '.join('#' + t for t in metadata['youtube']['tags'][:8])}",
        title="✨ Output Ready for Social Media",
        border_style="bold green"
    ))

def main():
    parser = argparse.ArgumentParser(
        description="Faceless Shorts: 100% Free AI Faceless Video Generator for YouTube Shorts, Reels, and TikTok."
    )
    subparsers = parser.add_subparsers(dest="command")

    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a faceless short video")
    gen_parser.add_argument("-t", "--topic", type=str, help="Topic for the video (e.g. 'dark psychology tricks')")
    gen_parser.add_argument("-n", "--niche", type=str, choices=list(VIRAL_TEMPLATES.keys()), help="Choose a pre-built viral template")
    gen_parser.add_argument("-v", "--voice", type=str, default="christopher", help="Edge-TTS voice (e.g. 'christopher', 'guy', 'aria', 'eric')")
    gen_parser.add_argument("-s", "--style", type=str, default="hormozi", choices=list(SUBTITLE_STYLES.keys()), help="Subtitle style")
    gen_parser.add_argument("-m", "--music", type=str, default="dark_tension", choices=["dark_tension", "curiosity_ambient", "cinematic_pulse"], help="Background music preset")
    gen_parser.add_argument("-r", "--rate", type=str, default="+5%", help="Speech rate adjustment (e.g. '+5%%', '+10%%')")
    gen_parser.add_argument("-o", "--output", type=str, help="Output MP4 file path")
    gen_parser.add_argument("--script-json", type=str, help="Path to custom JSON script file")
    gen_parser.add_argument("--offline", action="store_true", help="Run offline without downloading AI images")

    # list commands
    subparsers.add_parser("voices", help="List available Edge-TTS voices")
    subparsers.add_parser("styles", help="List subtitle styles")
    subparsers.add_parser("presets", help="List viral script presets")
    subparsers.add_parser("prompt", help="Print LLM system prompt for Claude/Gemini/OpenCode")

    args = parser.parse_args()

    if args.command == "generate":
        run_generate(args)
    elif args.command == "voices":
        list_voices()
    elif args.command == "styles":
        list_styles()
    elif args.command == "presets":
        list_presets()
    elif args.command == "prompt":
        console.print(Panel(LLM_SYSTEM_PROMPT, title="🤖 System Prompt for LLMs (Claude/Gemini/OpenCode)", border_style="cyan"))
    else:
        print_banner()
        parser.print_help()

if __name__ == "__main__":
    main()
