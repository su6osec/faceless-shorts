# AGENTS.md - Faceless Shorts Autonomous Production Guide

This file instructs AI coding assistants (Google Antigravity, Gemini CLI, Claude Code, OpenCode, Cursor, Windsurf) on operating the `faceless-shorts` pipeline.

## Project Scope
This project is an open-source, 100% free automated faceless video generation system designed by **su6osec** for YouTube Shorts, Instagram Reels, and TikTok.

## Zero-Cost Stack Requirements
- **LLM / Scripts**: Free prompts / Built-in viral templates (`presets/`), curated knowledge packs, optional free local LLM (Ollama).
- **TTS**: Microsoft Edge-TTS (`edge-tts`), zero API key, includes native word timestamps.
- **Visuals**: Pollinations.ai (Flux.1 vertical 1080x1920), local ComfyUI (`--engine comfyui`), or procedural fallback (`--offline`).
- **Art Styles**: 45 three-stage styles (AI prompt → offline PIL transform → FFmpeg grade): pixel art, chalkboard, glow sketch, PS2, comic, flat vector, minimal line, CGI, LEGO, explainer 3D, watercolor, blueprint, vaporwave, synthwave...
- **Post-FX**: 15 premium FFmpeg grades + 6 packs (`--effects cinematic|premium|dreamy|retro`): bloom, halation, chromatic aberration, teal-orange, film grain, anamorphic streaks.
- **Captions**: Word-level ASS karaoke styling (13 styles with 118% word bounce and neon glow).
- **Audio Mixing**: FFmpeg `sidechaincompress` audio ducking with procedural ambient synthesis.
- **Rendering**: FFmpeg with 10 Ken Burns motions, 17 xfade transitions, 5 quality profiles (draft → ultra 1440x2560@60fps), broadcast-standard limited-range color.
- **Free Tools** (optional, auto-detected via `doctor`): whisper.cpp (FFmpeg built-in STT), yt-dlp, ComfyUI, Ollama, Pexels/Pixabay.

## Quick Commands for Agents
```bash
# Generate using preset
python -m faceless_shorts generate --niche dark_psychology --voice christopher --style hormozi

# Premium demo-style render (cinematic grade + zoom cuts + hd quality)
python -m faceless_shorts generate --topic "black hole" -q hd -fx cinematic -tr zoom -s neon_glow

# Retro pixel-art short with pixel mosaic transitions
python -m faceless_shorts generate --niche mind_blowing_facts -a pixel_art -tr pixelize -fx retro

# Generate using custom JSON script
python -m faceless_shorts generate --script-json presets/stoicism.json --output output/stoic.mp4

# Offline test (superfast procedural background)
python -m faceless_shorts generate --niche stoicism --offline --output output/offline.mp4

# Inspect the toolkit
python -m faceless_shorts art-styles   # 45 styles by category
python -m faceless_shorts effects      # Post-FX effects & packs
python -m faceless_shorts quality      # quality profiles
python -m faceless_shorts doctor       # free tool health check
python -m faceless_shorts transcribe clip.mp4   # local Whisper SRT
```

## Relevant Skill Documentation
- Main Skill: `.agents/skills/faceless-shorts/SKILL.md`
- References: `.agents/skills/faceless-shorts/references/`
