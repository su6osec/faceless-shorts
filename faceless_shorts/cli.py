"""
Command Line Interface for Faceless Shorts.
Author: su6osec (https://github.com/su6osec)
"""

import argparse
import json
import os
import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from faceless_shorts.config import (
    VOICES,
    SUBTITLE_STYLES,
    ART_STYLES,
    ART_STYLE_CATEGORIES,
    TRANSITIONS,
    DEFAULT_TRANSITION,
    LANGUAGES,
    DEFAULT_LANGUAGE,
    QUALITY_PROFILES,
    DEFAULT_QUALITY,
    IMAGE_ENGINES,
    DEFAULT_IMAGE_ENGINE,
)
from faceless_shorts.postfx import PostFX
from faceless_shorts.vfx import VFX_PRESETS
from faceless_shorts.style_processor import StyleProcessor
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

def list_vfx():
    table = Table(title="✨ Open-Source VFX & Animation Suites (Natron, Effekseer, OpenVDB, SVG.js, OpenToonz)", header_style="bold magenta")
    table.add_column("VFX Key", style="bold green", width=14)
    table.add_column("Open-Source Engine / Inspired Stack", style="cyan", width=34)
    table.add_column("Visual Capability & Cinematic Impact")

    table.add_row(
        "hollywood",
        "Natron (github.com/natrongithub/natron)",
        "Node compositing: Anamorphic bloom, chromatic aberration & 35mm halation"
    )
    table.add_row(
        "particles",
        "Effekseer (github.com/effekseer/effekseer)",
        "Procedural floating cosmic stardust, sparks & electric energy arcs"
    )
    table.add_row(
        "smoke_fire",
        "OpenVDB (github.com/academysoftwarefoundation/openvdb)",
        "Volumetric rising fire embers, turbulence & atmospheric smoke dynamics"
    )
    table.add_row(
        "svg_hud",
        "SVG.js (github.com/svgdotjs/svg.js) & Friction",
        "Animated vector sci-fi targeting reticles, corner brackets & HUDs"
    )
    table.add_row(
        "mocap",
        "FreeMoCap (github.com/freemocap/freemocap)",
        "Kinematic telemetry tracking points, wireframes & coordinate radars"
    )
    table.add_row(
        "toon",
        "OpenToonz (github.com/opentoonz) & Pencil2D",
        "2D cel-shaded anime line inking with Sobel edge detection & Ghibli palette"
    )
    table.add_row(
        "theatre",
        "Theatre.js (github.com/theatre-js/theatre)",
        "Non-linear bezier spring easing & elastic momentum for camera motions"
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
    table = Table(
        title="🖌️ Art & Editing Styles (3-stage: AI prompt + PIL transform + FFmpeg grade)",
        header_style="bold yellow"
    )
    table.add_column("Art Style Key", style="bold green", width=18)
    table.add_column("Style Name", style="cyan", width=28)
    table.add_column("Category", style="magenta", width=18)
    table.add_column("PIL Pixel-Op", style="dim", width=16)
    table.add_column("Visual Aesthetics")

    current_cat = None
    for key, a in ART_STYLES.items():
        cat = a.get("category", "cinematic")
        if cat != current_cat:
            table.add_row(
                "", f"[bold white]{ART_STYLE_CATEGORIES.get(cat, cat)}[/bold white]", "", "", ""
            )
            current_cat = cat
        table.add_row(
            key,
            a["name"],
            ART_STYLE_CATEGORIES.get(cat, cat).split(" ", 1)[-1],
            a.get("pixel_op", "—"),
            a["description"]
        )
    console.print(table)

def list_effects():
    table = Table(
        title="🎚️ Premium Post-FX Chain (Natron-grade FFmpeg compositing)",
        header_style="bold magenta"
    )
    table.add_column("Effect / Pack", style="bold green", width=18)
    table.add_column("Kind", style="cyan", width=8)
    table.add_column("Description")
    for effect in PostFX.available():
        table.add_row(effect, "fx", PostFX.describe(effect))
    for pack, members in PostFX.PACKS.items():
        table.add_row(
            f"[bold]{pack}[/bold]", "pack",
            f"Bundle: {', '.join(members) if members else 'clean (no grade)'}"
        )
    console.print(table)

def list_quality():
    table = Table(title="🎯 Render Quality Profiles", header_style="bold blue")
    table.add_column("Profile", style="bold green", width=14)
    table.add_column("Resolution", justify="center", width=14)
    table.add_column("FPS", justify="center", width=6)
    table.add_column("CRF", justify="center", width=6)
    table.add_column("x264 Preset", style="cyan", width=14)
    table.add_column("Audio", width=10)
    table.add_column("Use Case")
    use_cases = {
        "draft": "Fast iteration / previews",
        "social": "Daily posting (default)",
        "hd": "Crisp 1080p master, best balance",
        "cinematic": "60fps buttery motion",
        "ultra": "1440x2560 max-quality master",
    }
    for key, q in QUALITY_PROFILES.items():
        mark = " (default)" if key == DEFAULT_QUALITY else ""
        table.add_row(
            f"[bold]{key}[/bold]{mark}",
            f"{q['width']}x{q['height']}",
            str(q["fps"]), str(q["crf"]),
            q["preset"], q["audio_bitrate"],
            use_cases.get(key, "")
        )
    console.print(table)

def list_style_ops():
    table = Table(title="🧩 Offline PIL Style Transforms", header_style="bold green")
    table.add_column("Pixel Op", style="bold yellow", width=20)
    table.add_column("Description")
    for op in StyleProcessor.available_ops():
        table.add_row(op, StyleProcessor.get_description(op))
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
    profile = QUALITY_PROFILES.get(args.quality, QUALITY_PROFILES[DEFAULT_QUALITY])
    effects_display = args.effects if args.effects not in (None, "none", "nofx", "") else "none"

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
        f"[bold white]Post-FX Grade:[/bold white] [magenta]{effects_display}[/magenta]\n"
        f"[bold white]VFX & Animations:[/bold white] [yellow]{args.vfx or 'none'}[/yellow]\n"
        f"[bold white]Quality:[/bold white] [green]{args.quality} ({profile['width']}x{profile['height']} @ {args.fps or profile['fps']}fps, crf {profile['crf']})[/green]\n"
        f"[bold white]Image Engine:[/bold white] {'Procedural (offline)' if args.offline else IMAGE_ENGINES.get(args.engine, args.engine)}\n"
        f"[bold white]Audio:[/bold white] {'Clean Studio Voice (Zero Background Sound)' if (not args.music or args.music == 'none') else f'{args.music} (Ducked, -14 LUFS)'}",
        title="🎬 Production Brief",
        border_style="green"
    ))

    # Initialize renderer with transitions, VFX, post-FX, quality, engine, audio and language
    output_path = args.output or f"output/{script.niche}_{lang}_short.mp4"
    renderer = VideoRenderer(
        voice=chosen_voice,
        language=lang,
        subtitle_style=args.style,
        art_style=args.art_style,
        transition=args.transition,
        vfx=args.vfx,
        progress_bar=not args.no_progress_bar,
        bg_music_preset=args.music,
        speech_rate=args.rate,
        work_dir=".temp_render",
        quality=args.quality,
        fps=args.fps,
        effects=args.effects,
        engine="procedural" if args.offline else args.engine,
        crf=args.crf,
        encoder_preset=args.encoder_preset,
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

def run_doctor():
    """Diagnose every optional free-tool integration and print a health table."""
    from faceless_shorts.integrations import ToolRegistry, doctor_report

    console.print(Panel(
        "Free & open-source tool integrations (all optional — the core pipeline runs without them)",
        title="🩺 Doctor", border_style="cyan"
    ))
    console.print(doctor_report())

    table = Table(title="Environment", header_style="bold blue")
    table.add_column("Component", style="bold green", width=22)
    table.add_column("Status", style="cyan")
    table.add_column("Notes")

    import shutil as _shutil
    ffmpeg = _shutil.which("ffmpeg")
    if ffmpeg:
        try:
            out = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=10)
            version = out.stdout.splitlines()[0].split(" ")[2] if out.stdout else "?"
        except Exception:
            version = "?"
        table.add_row("ffmpeg", f"[green]✓ v{version}[/green]", "Render core (Ken Burns, xfade, Post-FX, libass)")
    else:
        table.add_row("ffmpeg", "[red]✗ missing[/red]", "brew install ffmpeg-full")

    try:
        import edge_tts  # noqa: F401
        table.add_row("edge-tts", "[green]✓ installed[/green]", "Free neural TTS + word timestamps")
    except Exception:
        table.add_row("edge-tts", "[red]✗ missing[/red]", "pip install edge-tts")

    try:
        import PIL  # noqa: F401
        table.add_row("Pillow", f"[green]✓ v{PIL.__version__}[/green]", "Offline art-style transforms")
    except Exception:
        table.add_row("Pillow", "[red]✗ missing[/red]", "pip install pillow")

    try:
        import faceless_shorts.postfx as _pf
        table.add_row("Post-FX", f"[green]✓ {len(_pf.PostFX.available())} effects[/green]",
                      f"packs: {', '.join(_pf.PostFX.PACKS)}")
    except Exception as e:
        table.add_row("Post-FX", f"[red]✗ {e}[/red]", "")

    console.print(table)

def run_transcribe(args):
    """Local Whisper transcription via FFmpeg's built-in whisper.cpp filter."""
    from faceless_shorts.integrations import WhisperTranscriber

    if not os.path.exists(args.input):
        console.print(f"[red]File not found: {args.input}[/red]")
        sys.exit(1)

    transcriber = WhisperTranscriber()
    if not transcriber.available():
        console.print("[red]FFmpeg whisper filter not available in this build.[/red]")
        console.print("Install a full FFmpeg build (brew install ffmpeg-full) or use openai-whisper.")
        sys.exit(1)

    console.print(f"[cyan]Ensuring local Whisper model ({args.model}) is cached...[/cyan]")
    model_path = transcriber.ensure_model(language=args.language)
    if not model_path:
        console.print("[red]Could not download Whisper model (network offline?).[/red]")
        sys.exit(1)

    console.print(f"[cyan]Transcribing {args.input} with local Whisper ({args.model}, lang={args.language})...[/cyan]")
    fmt = "srt" if (args.output or "").endswith(".srt") else "json"
    result = transcriber.transcribe(
        media_path=args.input,
        language=args.language,
        out_format=fmt,
        model_size=args.model,
    )
    if result is None:
        console.print("[red]Transcription failed.[/red]")
        sys.exit(1)

    out_path = args.output or os.path.splitext(args.input)[0] + f".{fmt}"
    with open(out_path, "w", encoding="utf-8") as f:
        if fmt == "json":
            json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            f.write(str(result))
    console.print(f"[green]✓ Transcription saved to {os.path.abspath(out_path)}[/green]")
    console.print(Panel(str(result)[:1500], title="Transcript Preview", border_style="green"))

def main():
    parser = argparse.ArgumentParser(
        description="Faceless Shorts: 100% Free AI Faceless Video Generator for YouTube Shorts, Reels, and TikTok."
    )
    subparsers = parser.add_subparsers(dest="command")

    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a faceless short video")
    gen_parser.add_argument("-t", "--topic", type=str, help="Custom topic (e.g. 'how to get 6 pack abs' or 'boxing psychology')")
    gen_parser.add_argument("-n", "--niche", type=str, help="Choose pre-built niche or custom niche (fitness, stoicism, dark_psychology, motivation, finance_hustle, ai_tech, horror_mystery, blackhole, etc.)")
    gen_parser.add_argument("-l", "--language", type=str, default="en", help="Language code (en, hi, es, fr, de, pt, ja, ar, ru, it, id)")
    gen_parser.add_argument("-v", "--voice", type=str, default="christopher", help="Edge-TTS voice (e.g. 'christopher', 'guy', 'madhur', 'alvaro', 'henri', 'conrad')")
    gen_parser.add_argument("-tr", "--transition", type=str, default="flash", choices=list(TRANSITIONS.keys()), help="Scene transition (flash, zoom, dissolve, pixelize, blur, circle, ...)")
    gen_parser.add_argument("-x", "--vfx", type=str, default="none", help="Visual effects suite: hollywood, particles, smoke_fire, svg_hud, mocap, toon, theatre (can comma-separate: 'hollywood,particles')")
    gen_parser.add_argument("-fx", "--effects", type=str, default="none", help="Premium Post-FX grade: single effects (bloom, halation, chroma, grain, teal_orange, ...) or packs (cinematic, premium, dreamy, retro). Comma-separable.")
    gen_parser.add_argument("-s", "--style", type=str, default="hormozi", choices=list(SUBTITLE_STYLES.keys()), help="Subtitle style (hormozi, beast_pop, neon_glow, chalk_classic, horror_bleed, ...)")
    gen_parser.add_argument("-a", "--art-style", type=str, default="hyperreal", choices=list(ART_STYLES.keys()), help="Visual art style (hyperreal, pixel_art, chalkboard, glow_sketch, ps2_style, comic_art, flat_vector, minimal_line, cgi_motion, lego, explainer_3d, ...)")
    gen_parser.add_argument("-m", "--music", type=str, default="none", choices=["none", "dark_tension", "curiosity_ambient", "cinematic_pulse", "sub_bass_808"], help="Background music preset (default: 'none' for pristine clean voiceover with zero background sound)")
    gen_parser.add_argument("-r", "--rate", type=str, default="+0%", help="Speech rate adjustment (default: '+0%%' for natural human cadence)")
    gen_parser.add_argument("-q", "--quality", type=str, default=DEFAULT_QUALITY, choices=list(QUALITY_PROFILES.keys()), help="Render quality profile (draft, social, hd, cinematic, ultra)")
    gen_parser.add_argument("--fps", type=int, default=None, help="Override output frame rate (24/30/60)")
    gen_parser.add_argument("--crf", type=int, default=None, help="Override x264 CRF quality (lower = better, 15-28)")
    gen_parser.add_argument("--encoder-preset", type=str, default=None, choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], help="Override x264 encoder speed/quality preset")
    gen_parser.add_argument("--engine", type=str, default=DEFAULT_IMAGE_ENGINE, choices=list(IMAGE_ENGINES.keys()), help="Image generation engine (pollinations, comfyui, procedural)")
    gen_parser.add_argument("-o", "--output", type=str, help="Output MP4 file path")
    gen_parser.add_argument("--script-json", type=str, help="Path to custom JSON script file")
    gen_parser.add_argument("--images-dir", type=str, help="Path to folder containing scene_01.jpg, scene_02.jpg, etc.")
    gen_parser.add_argument("--no-progress-bar", action="store_true", help="Disable the glowing bottom retention progress bar")
    gen_parser.add_argument("--save-preset", action="store_true", help="Save the generated script as a reusable preset JSON file")
    gen_parser.add_argument("--offline", action="store_true", help="Run offline without downloading AI images (forces procedural engine)")

    # listing commands
    subparsers.add_parser("voices", help="List available Edge-TTS voices across languages")
    subparsers.add_parser("languages", help="List supported languages and voice mappings")
    subparsers.add_parser("transitions", help="List scene transitions (flash, zoom, dissolve, pixelize, blur, ...)")
    subparsers.add_parser("vfx", help="List open-source VFX suites (Natron, Effekseer, OpenVDB, SVG.js, OpenToonz, Theatre.js)")
    subparsers.add_parser("effects", help="List premium Post-FX grades & packs (bloom, halation, teal_orange, cinematic, ...)")
    subparsers.add_parser("styles", help="List subtitle styles")
    subparsers.add_parser("art-styles", help="List all art & editing styles by category")
    subparsers.add_parser("style-ops", help="List offline PIL style transforms (pixel art, chalkboard, halftone, ...)")
    subparsers.add_parser("quality", help="List render quality profiles (draft/social/hd/cinematic/ultra)")
    subparsers.add_parser("presets", help="List viral script presets")
    subparsers.add_parser("prompt", help="Print LLM system prompt for Claude/Gemini/OpenCode")
    subparsers.add_parser("doctor", help="Diagnose free tool integrations (ffmpeg, whisper, comfyui, yt-dlp, ollama, ...)")

    # transcribe command (local Whisper via FFmpeg)
    tr_parser = subparsers.add_parser("transcribe", help="Transcribe any audio/video to SRT using local Whisper (FFmpeg built-in, 100%% offline)")
    tr_parser.add_argument("input", type=str, help="Path to audio/video file")
    tr_parser.add_argument("--language", type=str, default="en", help="Language code (en, hi, es, ...)")
    tr_parser.add_argument("--model", type=str, default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
    tr_parser.add_argument("-o", "--output", type=str, help="Output subtitle file path (.srt/.json/.txt)")

    args = parser.parse_args()

    if args.command == "generate":
        run_generate(args)
    elif args.command == "voices":
        list_voices()
    elif args.command == "languages":
        list_languages()
    elif args.command == "transitions":
        list_transitions()
    elif args.command == "vfx":
        list_vfx()
    elif args.command == "effects":
        list_effects()
    elif args.command == "styles":
        list_styles()
    elif args.command == "art-styles":
        list_art_styles()
    elif args.command == "style-ops":
        list_style_ops()
    elif args.command == "quality":
        list_quality()
    elif args.command == "presets":
        list_presets()
    elif args.command == "prompt":
        console.print(Panel(LLM_SYSTEM_PROMPT, title="🤖 System Prompt for LLMs (Claude/Gemini/OpenCode)", border_style="cyan"))
    elif args.command == "doctor":
        run_doctor()
    elif args.command == "transcribe":
        run_transcribe(args)
    else:
        print_banner()
        parser.print_help()

if __name__ == "__main__":
    main()
