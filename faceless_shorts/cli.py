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

from faceless_shorts.config import (
    VOICES,
    SUBTITLE_STYLES,
    ART_STYLES,
    TRANSITIONS,
    DEFAULT_TRANSITION,
    LANGUAGES,
    DEFAULT_LANGUAGE
)
from faceless_shorts.script_generator import (
    VIRAL_TEMPLATES,
    get_template,
    create_or_get_script,
    VideoScript,
    LLM_SYSTEM_PROMPT
)
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
    table.add_column("Lang", style="magenta", width=6)
    table.add_column("Voice ID", style="yellow")
    table.add_column("Gender", width=8)
    table.add_column("Vibe & Description")
    table.add_column("Best Niches", style="dim")

    for key, v in VOICES.items():
        table.add_row(
            key,
            v.get("language", "en"),
            v["id"],
            v["gender"],
            v["vibe"],
            ", ".join(v["recommended_for"])
        )
    console.print(table)

def list_languages():
    table = Table(title="🌐 Supported Languages & Neural Voice Mapping", header_style="bold blue")
    table.add_column("Code", style="bold green", width=8)
    table.add_column("Language Name", style="yellow", width=24)
    table.add_column("Default Voice", style="cyan", width=16)
    table.add_column("Recommended Font", style="magenta", width=22)
    table.add_column("All Voices", style="dim")

    for code, l in LANGUAGES.items():
        table.add_row(
            code,
            l["name"],
            l["default_voice"],
            l["recommended_font"],
            ", ".join(l["voices"])
        )
    console.print(table)

def list_transitions():
    table = Table(title="🎬 High-Retention Scene Transitions", header_style="bold yellow")
    table.add_column("Transition Key", style="bold green", width=16)
    table.add_column("Transition Name", style="cyan", width=22)
    table.add_column("Duration", justify="center", width=10)
    table.add_column("Retention & Visual Style")

    for key, t in TRANSITIONS.items():
        table.add_row(
            key,
            t["name"],
            f"{t['duration']}s" if t["duration"] > 0 else "0ms",
            t["description"]
        )
    console.print(table)

def list_styles():
    table = Table(title="🎨 Viral Subtitle Styles (With 118% Word Bounce)", header_style="bold magenta")
    table.add_column("Style Name", style="bold green", width=16)
    table.add_column("Font", style="cyan", width=14)
    table.add_column("Description")
    table.add_column("Words/Screen", justify="center", width=14)

    for key, s in SUBTITLE_STYLES.items():
        table.add_row(
            key,
            s["font_name"],
            s["description"],
            str(s["words_per_screen"])
        )
    console.print(table)

def list_art_styles():
    table = Table(title="🖌️ Trendy Video Editing & Art Styles", header_style="bold yellow")
    table.add_column("Art Style Key", style="bold green", width=18)
    table.add_column("Style Name", style="cyan", width=24)
    table.add_column("Visual Aesthetics & Trending Platforms")

    for key, a in ART_STYLES.items():
        table.add_row(
            key,
            a["name"],
            a["description"]
        )
    console.print(table)

def list_presets():
    table = Table(title="📜 Built-in Viral Niche Templates", header_style="bold blue")
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

    script: VideoScript = None
    lang = (args.language or DEFAULT_LANGUAGE).lower()

    if args.script_json and os.path.exists(args.script_json):
        console.print(f"[cyan]Loading script from JSON file: {args.script_json}[/cyan]")
        with open(args.script_json, "r") as f:
            data = json.load(f)
        script = VideoScript.from_dict(data)
    elif args.niche:
        console.print(f"[cyan]Resolving niche: '{args.niche}' (language={lang})...[/cyan]")
        script = create_or_get_script(args.niche, language=lang)
    elif args.topic:
        console.print(f"[cyan]Dynamically building script for custom topic: '{args.topic}' (language={lang})...[/cyan]")
        script = create_or_get_script(args.topic, language=lang)
    else:
        console.print(f"[cyan]No topic/niche specified. Defaulting to 'dark_psychology' (language={lang})...[/cyan]")
        script = create_or_get_script("dark_psychology", language=lang)

    # Resolve voice if user left it as default 'christopher' but specified another language
    chosen_voice = args.voice
    if chosen_voice == "christopher" and lang != "en" and lang in LANGUAGES:
        chosen_voice = LANGUAGES[lang]["default_voice"]

    # Optional: Save preset to presets/ folder
    if args.save_preset:
        preset_out = os.path.join("presets", f"{script.niche}_{lang}.json")
        with open(preset_out, "w") as f:
            json.dump(script.to_dict(), f, indent=2, ensure_ascii=False)
        console.print(f"[green]Saved script template to: {preset_out}[/green]")

    progress_bar_state = "Enabled (Bottom Glowing Line)" if not args.no_progress_bar else "Disabled"
    trans_name = TRANSITIONS.get(args.transition, {}).get("name", args.transition)

    console.print(Panel(
        f"[bold white]Title:[/bold white] {script.title}\n"
        f"[bold white]Language:[/bold white] [cyan]{LANGUAGES.get(lang, {}).get('name', lang)} ({lang})[/cyan]\n"
        f"[bold white]Niche:[/bold white] {script.niche}\n"
        f"[bold white]Scenes:[/bold white] {len(script.scenes)}\n"
        f"[bold white]Opening Hook:[/bold white] [yellow]\"{script.hook}\"[/yellow]\n"
        f"[bold white]Voice:[/bold white] {chosen_voice}\n"
        f"[bold white]Scene Transition:[/bold white] [yellow]{trans_name}[/yellow]\n"
        f"[bold white]Retention Progress Bar:[/bold white] [cyan]{progress_bar_state}[/cyan]\n"
        f"[bold white]Subtitle Style:[/bold white] {args.style}\n"
        f"[bold white]Art & Editing Style:[/bold white] [magenta]{args.art_style}[/magenta]\n"
        f"[bold white]Audio:[/bold white] {'Clean Studio Voice (Zero Background Sound)' if (not args.music or args.music == 'none') else f'{args.music} (Ducked, -14 LUFS)'}\n"
        f"[bold white]AI Visuals:[/bold white] {'Disabled (Offline Procedural)' if args.offline else 'Enabled (Pollinations Flux)'}",
        title="🎬 Production Brief",
        border_style="green"
    ))

    # Initialize renderer with transitions, progress bar, audio base and language
    output_path = args.output or f"output/{script.niche}_{lang}_short.mp4"
    renderer = VideoRenderer(
        voice=chosen_voice,
        language=lang,
        subtitle_style=args.style,
        art_style=args.art_style,
        transition=args.transition,
        progress_bar=not args.no_progress_bar,
        bg_music_preset=args.music,
        speech_rate=args.rate,
        work_dir=".temp_render"
    )

    rendered_file = renderer.render(
        script=script,
        output_mp4_path=output_path,
        custom_images_dir=args.images_dir,
        enable_ai_images=not args.offline
    )

    # Generate companion viral metadata pack
    optimizer = MetadataOptimizer()
    metadata = optimizer.generate_metadata(script)
    meta_path = output_path.replace(".mp4", "_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    console.print(Panel(
        f"[bold green]Video Rendered Successfully with Perfect Frame Sync & Sound Design![/bold green]\n\n"
        f"🎥 [bold]Video File:[/bold] {os.path.abspath(rendered_file)}\n"
        f"📊 [bold]Metadata File:[/bold] {os.path.abspath(meta_path)}\n\n"
        f"[bold yellow]YouTube Title:[/bold yellow] {metadata['youtube']['title']}\n"
        f"[bold yellow]TikTok Caption:[/bold yellow] {metadata['tiktok']['caption'][:80]}...\n"
        f"[bold yellow]Viral Tags:[/bold yellow] {' '.join('#' + t for t in metadata['youtube']['tags'][:8])}",
        title="✨ Ready to Post on YouTube Shorts, TikTok & Reels",
        border_style="bold green"
    ))

def main():
    parser = argparse.ArgumentParser(
        description="Faceless Shorts: 100% Free AI Faceless Video Generator for YouTube Shorts, Reels, and TikTok."
    )
    subparsers = parser.add_subparsers(dest="command")

    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a faceless short video")
    gen_parser.add_argument("-t", "--topic", type=str, help="Custom topic (e.g. 'how to get 6 pack abs' or 'boxing psychology')")
    gen_parser.add_argument("-n", "--niche", type=str, help="Choose pre-built niche or custom niche (fitness, stoicism, dark_psychology, motivation, finance_hustle, ai_tech, horror_mystery, etc.)")
    gen_parser.add_argument("-l", "--language", type=str, default="en", help="Language code (en, hi, es, fr, de, pt, ja, ar, ru, it, id)")
    gen_parser.add_argument("-v", "--voice", type=str, default="christopher", help="Edge-TTS voice (e.g. 'christopher', 'guy', 'madhur', 'alvaro', 'henri', 'conrad')")
    gen_parser.add_argument("-tr", "--transition", type=str, default="flash", choices=list(TRANSITIONS.keys()), help="Scene transition (flash, crossfade, slide, wipe, cut)")
    gen_parser.add_argument("-s", "--style", type=str, default="hormozi", choices=list(SUBTITLE_STYLES.keys()), help="Subtitle style (hormozi, beast_pop, neon_cyberpunk, crimson_alert, sketch_comic, minimalist_gold)")
    gen_parser.add_argument("-a", "--art-style", type=str, default="hyperreal", choices=list(ART_STYLES.keys()), help="Visual editing style (hyperreal, sketch, old_style, paper_craft, cyberpunk_glitch, cinematic_noir)")
    gen_parser.add_argument("-m", "--music", type=str, default="none", choices=["none", "dark_tension", "curiosity_ambient", "cinematic_pulse", "sub_bass_808"], help="Background music preset (default: 'none' for pristine clean voiceover with zero background sound)")
    gen_parser.add_argument("-r", "--rate", type=str, default="+0%", help="Speech rate adjustment (default: '+0%%' for natural human cadence)")
    gen_parser.add_argument("-o", "--output", type=str, help="Output MP4 file path")
    gen_parser.add_argument("--script-json", type=str, help="Path to custom JSON script file")
    gen_parser.add_argument("--images-dir", type=str, help="Path to folder containing scene_01.jpg, scene_02.jpg, etc.")
    gen_parser.add_argument("--no-progress-bar", action="store_true", help="Disable the glowing bottom retention progress bar")
    gen_parser.add_argument("--save-preset", action="store_true", help="Save the generated script as a reusable preset JSON file")
    gen_parser.add_argument("--offline", action="store_true", help="Run offline without downloading AI images")

    # listing commands
    subparsers.add_parser("voices", help="List available Edge-TTS voices across languages")
    subparsers.add_parser("languages", help="List supported languages and voice mappings")
    subparsers.add_parser("transitions", help="List scene transitions (flash cut, crossfade, slide, wipe)")
    subparsers.add_parser("styles", help="List subtitle styles")
    subparsers.add_parser("art-styles", help="List video art & editing styles (sketch, old style, paper craft, etc.)")
    subparsers.add_parser("presets", help="List viral script presets")
    subparsers.add_parser("prompt", help="Print LLM system prompt for Claude/Gemini/OpenCode")

    args = parser.parse_args()

    if args.command == "generate":
        run_generate(args)
    elif args.command == "voices":
        list_voices()
    elif args.command == "languages":
        list_languages()
    elif args.command == "transitions":
        list_transitions()
    elif args.command == "styles":
        list_styles()
    elif args.command == "art-styles":
        list_art_styles()
    elif args.command == "presets":
        list_presets()
    elif args.command == "prompt":
        console.print(Panel(LLM_SYSTEM_PROMPT, title="🤖 System Prompt for LLMs (Claude/Gemini/OpenCode)", border_style="cyan"))
    else:
        print_banner()
        parser.print_help()

if __name__ == "__main__":
    main()
