---
name: faceless-shorts
description: >-
  Use this skill to create 100% free viral vertical faceless shorts/videos for YouTube Shorts, Instagram Reels, and TikTok. Generates viral scripts, realistic voiceovers (Edge-TTS), dynamic AI visuals (Pollinations Flux), Hormozi-style animated karaoke subtitles, audio ducking, and renders 1080x1920 MP4 videos with zero API cost.
---

# Faceless Shorts Generator Skill

This skill guides you (Claude, Gemini, Antigravity, OpenCode, or any AI assistant) in orchestrating the complete end-to-end production of publication-ready, vertical 9:16 faceless videos **completely for free**.

---

## 1. Capabilities Overview

* **Zero-Cost Stack**: Microsoft Edge-TTS (multilingual neural voices + word boundaries) + Pollinations AI (Flux.1 9:16 visuals) + FFmpeg.
* **Target Platforms**: YouTube Shorts, Instagram Reels, TikTok (1080x1920, 30/60 FPS).
* **Open-Source VFX & Animation Suite (`--vfx` / `-x`)**:
  * **`hollywood`** (Inspired by Natron `github.com/natrongithub/natron`): Multi-pass node compositing with anamorphic bloom/glow diffusion, optical chromatic aberration (RGB shift), and 35mm grain.
  * **`particles`** (Inspired by Effekseer `github.com/effekseer/effekseer`): Procedural floating cosmic stardust, sparks, and electric arcs.
  * **`smoke_fire`** (Inspired by OpenVDB `github.com/academysoftwarefoundation/openvdb`): Volumetric rising fire embers, turbulence, and atmospheric smoke dynamics.
  * **`svg_hud`** (Inspired by SVG.js `github.com/svgdotjs/svg.js` & Friction `github.com/friction2d/friction`): Animated vector sci-fi targeting reticles, rotating telemetry gauges, and corner tech HUD brackets.
  * **`mocap`** (Inspired by FreeMoCap `github.com/freemocap/freemocap`): Kinematic telemetry tracking points and coordinate radar overlays.
  * **`toon`** (Inspired by OpenToonz `github.com/opentoonz` & Pencil2D `github.com/pencil2d`): Traditional 2D anime cel-shading with Sobel contour inking and Ghibli palette grading.
  * **`theatre`** (Inspired by Theatre.js `github.com/theatre-js/theatre`): Non-linear bezier spring easing and elastic momentum for camera motions.
* **Audio Engineering**:
  * **Clean Studio Voiceover**: Default is 100% clean human voiceover with **zero background sound, hum, or drone**, mastered to -14 LUFS.
  * Optional Sub-Bass & Ambient Presets (`--music`): `sub_bass_808`, `dark_tension`, `cinematic_pulse`, `curiosity_ambient`.
* **Multi-Language Support (`--language` / `-l`)**:
  * English (`en`), Hindi (`hi`), Spanish (`es`), French (`fr`), German (`de`), Portuguese (`pt`), Japanese (`ja`), Arabic (`ar`), Russian (`ru`), Italian (`it`), Indonesian (`id`).
  * Continuous human prosody without unnatural 1.2s dead stops.
  * Automatic neural voice selection and native font resolution (`Kohinoor Devanagari`, `Hiragino Sans`, `Geeza Pro`, `Arial Black`).
* **High-Retention Scene Transitions (`--transition` / `-tr`)**:
  * `flash`: 0.22s White Flash Cut (#1 viral retention cut on TikTok & Shorts).
  * `crossfade`: 0.25s Smooth cinematic dissolve between scenes.
  * `slide`: 0.22s Fast kinetic whip slide transition.
  * `wipe`: 0.22s Graphic wipe across the screen.
  * `cut`: Instant direct cut.
* **Motion Graphics & Animations**:
  * Glowing animated **Retention Progress Bar** at the bottom (keeps viewers watching until the loop).
  * Active-word 118% scale-bounce karaoke animation in ASS subtitles.

---

## 2. Interactive Agent Workflow

When the user requests a short video, follow these steps:

### Step 1: Script & Niche Selection
1. Choose a pre-built niche (`fitness`, `dark_psychology`, `stoicism`, etc.) or pass ANY custom topic directly via `--topic "your topic"`.
2. Specify the language with `--language` (e.g. `--language hi` for Hindi, `--language es` for Spanish).

### Step 2: Configure Aesthetics & VFX
* **VFX Suite**: `--vfx hollywood,particles,svg_hud` (or `--vfx toon`, `--vfx smoke_fire`).
* **Voice**: Automatically selected for the language, or specify via `-v` / `--voice` (`christopher`, `guy`, `madhur`, `alvaro`, `henri`, `conrad`, `keita`, `hamed`).
* **Scene Transition**: `--transition flash` (default white flash cut), `crossfade`, `slide`, `wipe`, `cut`.
* **Audio**: Defaults to clean voiceover with zero background sound (`--music none`). To add sub-bass drone, specify `--music sub_bass_808`.
* **Subtitle Style**: `--style hormozi`, `beast_pop`, `neon_cyberpunk`, `crimson_alert`, `sketch_comic`, `minimalist_gold`.

### Step 3: Visual Generation Options
* **Option A (Autonomous Agent / Nano Banana)**: In Antigravity or Gemini, invoke the built-in `image-generator` subagent (Nano Banana) for each scene prompt to create custom 9:16 high-res visuals in `images/<niche>/`, then pass `--images-dir images/<niche>`.
* **Option B (Pollinations AI Free REST)**: The engine automatically queries Pollinations Flux for 100% zero-cost keyless generation.
* **Option C (Custom User Images)**: Place images (`scene_01.jpg`, `scene_02.jpg`, etc.) into `images/<niche>/` or pass `--images-dir`.

### Step 4: Execute the Python CLI

#### Example 1: Hollywood VFX Black Hole Short (Clean Voiceover + Zero Background Sound)
```bash
python -m faceless_shorts generate --niche blackhole --transition flash --vfx hollywood,particles,svg_hud --music none --style hormozi
```

#### Example 2: Continuous Hindi Short with Native Devanagari & Zero Background Sound
```bash
python -m faceless_shorts generate --topic "ब्लैक होल" --language hi --transition flash --music none --style hormozi
```

#### Example 3: OpenToonz / Manga Anime Cel-Shaded Short
```bash
python -m faceless_shorts generate --topic "cyberpunk boxing" --art-style sketch --vfx toon --transition slide
```

### Step 5: Present Companion Metadata Pack
After rendering finishes, report the video path and present the viral metadata (`output/*_metadata.json`):
* YouTube Title, Description, Timestamps & Viral Hashtags
* TikTok Caption & Hashtags
* Instagram Reels Caption & Tags
