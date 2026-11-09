---
name: faceless-shorts
description: >-
  Use this skill to create 100% free viral vertical faceless shorts/videos for YouTube Shorts, Instagram Reels, and TikTok. Generates viral scripts, realistic voiceovers (Edge-TTS), dynamic AI visuals (Pollinations Flux), Hormozi-style animated karaoke subtitles, audio ducking, and renders 1080x1920 MP4 videos with zero API cost.
---

# Faceless Shorts Generator Skill

This skill guides you (Claude, Gemini, Antigravity, OpenCode, or any AI assistant) in orchestrating the complete end-to-end production of publication-ready, vertical 9:16 faceless videos **completely for free**.

---

## 1. Capabilities Overview

* **Zero-Cost Stack**: Microsoft Edge-TTS (voices + word boundaries) + Pollinations AI (Flux.1 9:16 visuals) + FFmpeg (Punchy Ken Burns + ASS subtitle burning + dynamic ducking).
* **Target Platforms**: YouTube Shorts, Instagram Reels, TikTok (1080x1920, 30/60 FPS).
* **Universal Niche Support**: Supports pre-built presets (`fitness`, `dark_psychology`, `stoicism`, `mind_blowing_facts`, `motivation`, `finance_hustle`, `ai_tech`, `horror_mystery`) **OR any custom topic dynamically generated on the fly**!
* **Trendy Video Editing Styles**:
  * **`sketch`**: Detailed black & white manga / inked graphic novel look.
  * **`old_style`**: Vintage 1970s/80s analog 35mm film with grain, Kodachrome warm palette & vignette.
  * **`paper_craft`**: Textured torn-paper collage scrapbook aesthetic (Vox / MagnatesMedia style).
  * **`cyberpunk_glitch`**: Dark neon cyan/magenta rim lighting & futuristic atmosphere.
  * **`cinematic_noir`**: Deep chiaroscuro shadows with warm amber rim light.
  * **`hyperreal`**: Photorealistic 8k octane render.
* **Premium Typography & 118% Word Bounce**:
  * Heavy fonts (`Arial Black`, `Impact`, `Helvetica Neue`).
  * Words pop with dynamic scale bounce (118%) exactly as they are spoken.
* **Frame-Accurate Synchronization**:
  * Continuous stream speech synthesis prevents MP3 padding drift. Visual cuts and subtitles are aligned down to the millisecond.

---

## 2. Interactive Agent Workflow

When the user requests a short video (e.g., *"Make a fitness short about building muscle"*, *"Create a sketch-style short about stoicism"*, or *"Create a 50-second short on quantum computing"*), follow these steps:

### Step 1: Script & Niche Selection
1. You can use any of the built-in niches (`fitness`, `dark_psychology`, `stoicism`, `mind_blowing_facts`, `motivation`, `finance_hustle`, `ai_tech`, `horror_mystery`) or pass ANY custom topic directly via `--topic "your topic"`.
2. The dynamic builder will automatically construct a 5-scene high-retention script with a 3-second pattern interrupt hook, high-density beats, and an infinite loop CTA.

### Step 2: Choose Voice, Subtitle Style & Art Style
* **Voice Selection**:
  * Deep/Authoritative: `christopher` (`en-US-ChristopherNeural`)
  * Energetic/Facts: `guy` (`en-US-GuyNeural`)
  * British Scholarly: `ryan` (`en-GB-RyanNeural`)
  * Articulate Documentary: `aria` (`en-US-AriaNeural`)
  * Confident Hustle: `eric` (`en-US-EricNeural`)
  * Indian/Desi: `madhur` (`hi-IN-MadhurNeural`)
* **Subtitle Styles**:
  * `hormozi` (Arial Black, bright neon yellow highlight, heavy black outline, 118% word bounce)
  * `beast_pop` (Impact font, toxic lime green highlight over yellow)
  * `neon_cyberpunk` (Electric cyan active word over crisp white)
  * `crimson_alert` (Blood-red highlight for horror/crime/psychology)
  * `sketch_comic` (Inked graphic novel style)
  * `minimalist_gold` (Clean Helvetica Neue with warm gold)
* **Video Art & Editing Styles**:
  * `--art-style sketch` (Manga / comic sketch)
  * `--art-style old_style` (Vintage 35mm / 80s film)
  * `--art-style paper_craft` (Torn paper collage scrapbook)
  * `--art-style cyberpunk_glitch` (Dark neon futuristic)
  * `--art-style cinematic_noir` (Moody chiaroscuro)
  * `--art-style hyperreal` (Cinematic 8k photorealistic)

### Step 3: Execute the Python Engine

#### Example 1: Generate Fitness Short (Hormozi style)
```bash
python -m faceless_shorts generate --niche fitness --voice christopher --style hormozi
```

#### Example 2: Generate Manga / Sketch Style Short
```bash
python -m faceless_shorts generate --niche dark_psychology --art-style sketch --voice christopher --style sketch_comic
```

#### Example 3: Generate Vintage 35mm Film Stoicism Short
```bash
python -m faceless_shorts generate --niche stoicism --art-style old_style --voice ryan --style minimalist_gold
```

#### Example 4: Build From Scratch on ANY Custom Topic (No Preset Needed)
```bash
python -m faceless_shorts generate --topic "Cold Showers For Dopamine Reset" --art-style paper_craft --save-preset
```

#### Example 5: Instant Offline Test (Render in ~4 seconds)
```bash
python -m faceless_shorts generate --niche fitness --offline --output output/offline_fitness.mp4
```

### Step 4: Present Metadata Pack
After rendering finishes, report the video location to the user and present the auto-generated metadata file (`output/*_metadata.json`):
* YouTube Title & Description with Timestamps & Tags
* TikTok Caption & Hashtags
* Instagram Reels Caption & Tags

---

## 3. Reference Files & Deep Dives

* [Viral Hooks & Script Blueprint](./references/viral_hooks_blueprint.md)
* [Voice Catalog & Language Codes](./references/voice_catalog.md)
* [Subtitle Styles & ASS Configs](./references/subtitle_styles.md)
* [Visual Prompt Engineering Guide](./references/prompt_engineering_visuals.md)
* [100% Free Resources & API Catalog](./references/free_resources.md)
