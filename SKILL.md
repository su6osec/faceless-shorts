---
name: faceless-shorts
description: >-
  Use this skill to create 100% free viral vertical faceless shorts/videos for YouTube Shorts, Instagram Reels, and TikTok. Generates viral scripts, realistic voiceovers (Edge-TTS), dynamic AI visuals (Pollinations Flux), Hormozi-style animated karaoke subtitles, audio ducking, and renders 1080x1920 MP4 videos with zero API cost.
---

# Faceless Shorts Generator Skill

This skill guides you (Claude, Gemini, Antigravity, OpenCode, or any AI assistant) in orchestrating the complete end-to-end production of publication-ready, vertical 9:16 faceless videos **completely for free**.

---

## 1. Capabilities Overview

* **Zero-Cost Stack**: Microsoft Edge-TTS (multilingual neural voices + word boundaries) + Pollinations AI (Flux.1 9:16 visuals) + FFmpeg (Punchy Ken Burns + ASS subtitle burning + dynamic ducking).
* **Target Platforms**: YouTube Shorts, Instagram Reels, TikTok (1080x1920, 30/60 FPS).
* **Multi-Language Support (`--language` / `-l`)**:
  * English (`en`), Hindi (`hi`), Spanish (`es`), French (`fr`), German (`de`), Portuguese (`pt`), Japanese (`ja`), Arabic (`ar`), Russian (`ru`), Italian (`it`), Indonesian (`id`).
  * Automatic neural voice selection and native font resolution (`Kohinoor Devanagari`, `Hiragino Sans`, `Geeza Pro`, `Arial Black`).
* **High-Retention Scene Transitions (`--transition` / `-tr`)**:
  * `flash`: 0.22s White Flash Cut (#1 viral retention cut on TikTok & Shorts).
  * `crossfade`: 0.25s Smooth cinematic dissolve between scenes.
  * `slide`: 0.22s Fast kinetic whip slide transition.
  * `wipe`: 0.22s Graphic wipe across the screen.
  * `cut`: Instant direct cut.
* **Motion Graphics & Animations**:
  * Glowing animated **Retention Progress Bar** at the bottom (keeps viewers watching until the loop).
  * Dynamic camera motion presets: `punch_zoom_in`, `dramatic_zoom_out`, `pan_left`, `pan_right`, `vertigo_shake`, `whip_zoom`.
  * Active-word 118% scale-bounce karaoke animation in ASS subtitles.
* **Studio Audio Base & Sound Design**:
  * Deep sub-bass presets: `sub_bass_808` (45Hz punch), `dark_tension`, `cinematic_pulse`, `curiosity_ambient`.
  * Procedural Scene Transition Whoosh SFX: Synthesized noise sweep & sub swoosh automatically synced to every scene cut.
  * Vocal presence EQ (75Hz rumble cut + 3.5kHz clarity boost).
  * Dynamic sidechain ducking of background music under speech.
  * Master loudness normalized to -14 LUFS (EBU R128 social media standard).
* **Universal Niche Support**:
  * Built-in presets (`fitness`, `dark_psychology`, `stoicism`, `mind_blowing_facts`, `motivation`, `finance_hustle`, `ai_tech`, `horror_mystery`).
  * **Dynamic AI Script Generator for ANY custom topic or language on the fly**!
* **Trendy Video Editing Styles (`--art-style`)**:
  * `sketch`: Detailed black & white manga / inked graphic novel look.
  * `old_style`: Vintage 1970s/80s analog 35mm film with Kodachrome palette & grain.
  * `paper_craft`: Textured torn-paper collage scrapbook aesthetic (Vox / MagnatesMedia style).
  * `cyberpunk_glitch`: Dark neon cyan/magenta rim lighting.
  * `cinematic_noir`: Deep chiaroscuro shadows with warm amber rim light.
  * `hyperreal`: Photorealistic 8k octane render.

---

## 2. Interactive Agent Workflow

When the user requests a short video, follow these steps:

### Step 1: Script & Niche Selection
1. You can choose a pre-built niche (`fitness`, `dark_psychology`, `stoicism`, etc.) or pass ANY custom topic directly via `--topic "your topic"`.
2. Specify the language with `--language` (e.g. `--language hi` for Hindi, `--language es` for Spanish).
3. The dynamic builder constructs a 5-scene high-retention script with a pattern-interrupt hook and loop CTA.

### Step 2: Configure Aesthetics & Audio
* **Voice**: Automatically selected for the language, or specify via `-v` / `--voice` (`christopher`, `guy`, `madhur`, `alvaro`, `henri`, `conrad`, `keita`, `hamed`).
* **Scene Transition**: `--transition flash` (default white flash cut), `crossfade`, `slide`, `wipe`, `cut`.
* **Audio Preset**: `--music sub_bass_808`, `dark_tension`, `cinematic_pulse`, `curiosity_ambient`.
* **Subtitle Style**: `--style hormozi`, `beast_pop`, `neon_cyberpunk`, `crimson_alert`, `sketch_comic`, `minimalist_gold`.
* **Art Style**: `--art-style hyperreal`, `sketch`, `old_style`, `paper_craft`, `cyberpunk_glitch`, `cinematic_noir`.
* **Progress Bar**: Enabled by default; disable with `--no-progress-bar`.

### Step 3: Visual Generation Options
* **Option A (Autonomous Agent / Nano Banana)**: In Antigravity or Gemini, invoke the built-in `image-generator` subagent (Nano Banana) for each scene prompt to create custom 9:16 high-res visuals in `images/<niche>/`, then pass `--images-dir images/<niche>`.
* **Option B (Pollinations AI Free REST)**: The engine automatically queries Pollinations Flux for 100% zero-cost keyless generation.
* **Option C (Custom User Images)**: Place images (`scene_01.jpg`, `scene_02.jpg`, etc.) into `images/<niche>/` or pass `--images-dir`.

### Step 4: Execute the Python CLI

#### Example 1: High-Retention Fitness Short (White Flash + Sub-Bass 808)
```bash
python -m faceless_shorts generate --niche fitness --transition flash --music sub_bass_808 --style hormozi
```

#### Example 2: Hindi Short with Native Devanagari Subtitles & Voice
```bash
python -m faceless_shorts generate --topic "कसरत" --language hi --transition flash --style hormozi
```

#### Example 3: Spanish Dark Psychology Short (Manga Sketch Style)
```bash
python -m faceless_shorts generate --topic "trucos psicologicos" --language es --art-style sketch --transition slide
```

#### Example 4: Vintage 35mm Film Stoicism Short
```bash
python -m faceless_shorts generate --niche stoicism --art-style old_style --transition crossfade --style minimalist_gold
```

#### Example 5: Instant Offline Test (Render in ~4 seconds)
```bash
python -m faceless_shorts generate --niche stoicism --offline --output output/offline_stoic.mp4
```

### Step 5: Present Companion Metadata Pack
After rendering finishes, report the video path and present the viral metadata (`output/*_metadata.json`):
* YouTube Title, Description, Timestamps & Viral Hashtags
* TikTok Caption & Hashtags
* Instagram Reels Caption & Tags
