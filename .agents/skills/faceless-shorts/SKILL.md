---
name: faceless-shorts
description: >-
  Use this skill to create 100% free viral vertical faceless shorts/videos for YouTube Shorts, Instagram Reels, and TikTok. Generates viral scripts, realistic voiceovers (Edge-TTS), dynamic AI visuals (Pollinations Flux), Hormozi-style animated karaoke subtitles, audio ducking, and renders 1080x1920 MP4 videos with zero API cost.
---

# Faceless Shorts Generator Skill

This skill guides you (Claude, Gemini, Antigravity, OpenCode, or any AI assistant) in orchestrating the complete end-to-end production of publication-ready, vertical 9:16 faceless videos **completely for free**.

---

## 1. Quick Capabilities Overview

* **Zero-Cost Stack**: Microsoft Edge-TTS (voices + word boundaries) + Pollinations AI (Flux.1 9:16 visuals) + FFmpeg (Ken Burns motion + ASS subtitle burning + dynamic ducking).
* **Target Platforms**: YouTube Shorts, Instagram Reels, TikTok (1080x1920, 30/60 FPS).
* **Viral Formatting**: 2-4 word screen chunking, Alex Hormozi / Beast style active word highlighting, context emoji insertion, and seamless loop hooks.

---

## 2. Interactive Agent Workflow

When the user requests a short video (e.g., *"Make a dark psychology short about ghosting"* or *"Create a 50-second Stoic short"*), follow these 5 steps:

### Step 1: Script & Niche Selection
1. Identify the viral niche:
   * **`dark_psychology`**: Manipulation, body language, covert influence, subconscious mind.
   * **`stoicism`**: Marcus Aurelius, emotional mastery, discipline, ego control.
   * **`mind_blowing_facts`**: Space exploration, quantum physics, bizarre animal facts.
   * **`horror_mystery`**: Creepypastas, unsolved disappearances, dark history.
   * **`finance_hustle`**: Money rules, compounding habits, investor mindset.
2. Structure the script into **4 to 7 scenes** (~40-55 seconds total, 95-120 words).
3. Ensure Scene 1 is a **Pattern Interrupt Hook** (0-3s).
4. Review [Viral Hooks Blueprint](./references/viral_hooks_blueprint.md) for proven formulas and loop endings.

### Step 2: Choose Voice & Subtitle Style
* **Voice Selection** (from [Voice Catalog](./references/voice_catalog.md)):
  * Deep/Mysterious: `christopher` (`en-US-ChristopherNeural`)
  * Energetic/Facts: `guy` (`en-US-GuyNeural`)
  * Articulate/Documentary: `aria` (`en-US-AriaNeural`)
  * Friendly/Youthful: `jenny` (`en-US-JennyNeural`)
  * British Cinematic: `ryan` (`en-GB-RyanNeural`)
  * Hindi/Desi: `madhur` (`hi-IN-MadhurNeural`)
* **Subtitle Style** (from [Subtitle Styles](./references/subtitle_styles.md)):
  * `hormozi` (Yellow highlight, bold white, black border) — *Recommended default*
  * `neon_cyberpunk` (Cyan highlight over green/white)
  * `crimson_alert` (Blood-red highlight, ideal for horror/thriller)
  * `beast_pop` (Lime green highlight over yellow)
  * `minimalist_gold` (Subtle elegant warm gold)

### Step 3: Formulate Visual Prompts
For each scene, craft an 8k cinematic visual prompt following the [Prompt Engineering Guide](./references/prompt_engineering_visuals.md):
```text
cinematic [subject/action], [environment], [dramatic lighting/chiaroscuro], 9:16 vertical composition, photorealistic, 8k wallpaper
```

### Step 4: Execute the Python Engine
Run the generator CLI or script from the repository root:

#### Option A: One-Shot Generation using Niche Presets
```bash
python -m faceless_shorts generate --niche dark_psychology --voice christopher --style hormozi
```

#### Option B: Custom Script via JSON
Save a custom script to `.temp_script.json`:
```json
{
  "title": "3 Signs Someone Is Secretly Jealous",
  "niche": "dark_psychology",
  "target_duration": 45,
  "hook": "Notice how they always downplay your biggest achievements?",
  "scenes": [
    {
      "index": 1,
      "text": "Notice how they always downplay your biggest achievements?",
      "visual_prompt": "mysterious shadowy silhouette of a two-faced figure in dark room, dramatic noir lighting, photorealistic 8k vertical wallpaper",
      "motion": "center_zoom_in"
    },
    {
      "index": 2,
      "text": "When you share good news, pay close attention to their micro-expressions.",
      "visual_prompt": "macro close-up of human eye showing cold envious reflection, intense cinematic rim lighting, 8k vertical",
      "motion": "center_zoom_out"
    }
  ],
  "cta": "Follow to master human behavior.",
  "tags": ["#psychology", "#jealousy", "#mindset", "#shorts"]
}
```
Then execute:
```bash
python -m faceless_shorts generate --script-json .temp_script.json --output output/custom_short.mp4
```

#### Option C: Offline Fast Mode (Zero Internet Needed)
```bash
python -m faceless_shorts generate --niche stoicism --offline --output output/offline_stoic.mp4
```

### Step 5: Review & Present Metadata Pack
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
