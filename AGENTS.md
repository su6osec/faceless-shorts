# AGENTS.md - Faceless Shorts Autonomous Production Guide

This file instructs AI coding assistants (Google Antigravity, Gemini CLI, Claude Code, OpenCode, Cursor, Windsurf) on operating the `faceless-shorts` pipeline.

## Project Scope
This project is an open-source, 100% free automated faceless video generation system designed by **su6osec** for YouTube Shorts, Instagram Reels, and TikTok.

## Zero-Cost Stack Requirements
- **LLM / Scripts**: Free prompts / Built-in viral templates (`presets/`).
- **TTS**: Microsoft Edge-TTS (`edge-tts`), zero API key, includes native word timestamps.
- **Visuals**: Pollinations.ai (Flux.1 vertical 1080x1920) or procedural fallback.
- **Captions**: Word-level ASS karaoke styling (Alex Hormozi, Beast, Neon, Crimson styles).
- **Audio Mixing**: FFmpeg `sidechaincompress` audio ducking with procedural ambient synthesis.
- **Rendering**: FFmpeg with Ken Burns subpixel motion.

## Quick Commands for Agents
```bash
# Generate using preset
python -m faceless_shorts generate --niche dark_psychology --voice christopher --style hormozi

# Generate using custom JSON script
python -m faceless_shorts generate --script-json presets/stoicism.json --output output/stoic.mp4

# Offline test (superfast procedural background)
python -m faceless_shorts generate --niche stoicism --offline --output output/offline.mp4
```

## Relevant Skill Documentation
- Main Skill: `.agents/skills/faceless-shorts/SKILL.md`
- References: `.agents/skills/faceless-shorts/references/`
