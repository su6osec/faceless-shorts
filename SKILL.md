---
name: faceless-shorts
description: >-
  Use this skill to create 100% free viral vertical faceless shorts/videos for YouTube Shorts, Instagram Reels, and TikTok. Generates viral scripts, realistic voiceovers (Edge-TTS), dynamic AI visuals (Pollinations Flux), Hormozi-style animated karaoke subtitles, audio ducking, and renders 1080x1920 MP4 videos with zero API cost.
---

# Faceless Shorts Generator Skill

This repository provides an autonomous skill and CLI framework for AI agents (Claude, Gemini, Antigravity, OpenCode) and creators to generate vertical 9:16 viral shorts for YouTube Shorts, Instagram Reels, and TikTok completely for free.

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate a viral Fitness short
python -m faceless_shorts generate --niche fitness --voice christopher --style hormozi

# 3. Generate a Sketch/Manga style Dark Psychology short
python -m faceless_shorts generate --niche dark_psychology --art-style sketch --voice christopher --style sketch_comic

# 4. Generate a Vintage 35mm Stoicism short
python -m faceless_shorts generate --niche stoicism --art-style old_style --voice ryan --style minimalist_gold

# 5. Build on ANY arbitrary custom topic (No preset needed!)
python -m faceless_shorts generate --topic "Cold Showers For Dopamine Reset" --art-style paper_craft
```

See [Full Documentation in `.agents/skills/faceless-shorts/SKILL.md`](./.agents/skills/faceless-shorts/SKILL.md) for full references, voice catalogs, subtitle styling, and visual prompt engineering guidelines.
