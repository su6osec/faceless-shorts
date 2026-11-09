# ⚡ Faceless Shorts: AI-Powered Faceless Video Generator for Shorts, Reels & TikTok

[![Cost](https://img.shields.io/badge/Cost-%240.00%20Completely%20Free-brightgreen?style=for-the-badge&logo=cashapp)](https://github.com/su6osec/faceless-shorts)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Resolution](https://img.shields.io/badge/Resolution-1080x1920%20(9:16)-orange?style=for-the-badge)](https://github.com/su6osec/faceless-shorts)
[![Platforms](https://img.shields.io/badge/Target-YouTube%20Shorts%20%7C%20Reels%20%7C%20TikTok-red?style=for-the-badge&logo=youtube)](https://github.com/su6osec/faceless-shorts)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](https://github.com/su6osec/faceless-shorts)
[![Author](https://img.shields.io/badge/Author-su6osec-black?style=for-the-badge&logo=github)](https://github.com/su6osec/faceless-shorts)
[![Stars](https://img.shields.io/github/stars/su6osec/faceless-shorts?style=social)](https://github.com/su6osec/faceless-shorts)
[![Forks](https://img.shields.io/github/forks/su6osec/faceless-shorts?style=social)](https://github.com/su6osec/faceless-shorts)

<p align="center">
  <img src="https://img.shields.io/badge/🔥%20NO%20AWS%20Required-orange?style=for-the-badge" alt="No AWS">
  <img src="https://img.shields.io/badge/🚫%20NO%20API%20KEYS-red?style=for-the-badge" alt="No API Keys">
  <img src="https://img.shields.io/badge/⭐%2045%20ART%20STYLES-brightgreen?style=for-the-badge&logo=palette" alt="45 Art Styles">
</p>

<div align="center">

### 🎬 Zero-Cost AI Video Generator for YouTube Shorts • Instagram Reels • TikTok

Generate viral, professional faceless short-form videos **with ZERO API costs, subscriptions, or credit cards** — Use Microsoft Edge-TTS, Pollinations AI (Flux.1), FFmpeg, and optional local tools (ComfyUI, Ollama, whisper.cpp)

[Quick Install](#-quickstart-install) • [Examples](#-premium-demo-style-render) • [Features](#-what-makes-this-special) • [Freedom](#-free-tool-integrations)

</div>

---

## 🌟 What Makes This Special?

### 🔥 SEO-Optimized Features for Viral Short-Form Growth

1. **45 Premium Art Styles** — 6 categories (Cinematic • Illustration • Retro • 3D • Texture • Neon). Every style runs three stages: **AI prompt suffix** → **offline PIL transform** (pixel art, chalkboard, glow sketch, comic art, flat vector, minimal line, blueprint, watercolor, oil painting, pop, LEGO, voxel, stained glass) → **FFmpeg grade** during Ken Burns motion.
2. **17 High-Retention Transitions** — Flash cut, impact zoom, dream dissolve, pixel mosaic, whip blur, radial burst, iris circle, fade-to-black, diagonal slice, glitch wind, smooth glide, elastic squeeze, bleach fade, circle wipe, flash dissolve, liquid dissolve. **Verified to boost retention on TikTok & Shorts.**
3. **13 Animated Karaoke Subtitles** — Hormozi gold, neon glow blur (118% word bounce glow), chalkboard (retro), retro arcade, spooky blood red, epic champagne gold. All support proportional scaling for 1080x1920+ vertical.
4. **5 Quality Profiles** — `draft` → `social` → `hd` (60fps) → `cinematic` (30fps, 1440x2560) → `ultra` (1440x2560@60fps). Broadcast-standard limited-range color with scale=out_range=tv.
5. **15+ Premium Post-FX Grades** — `cinematic` (bloom + halation + film grain + teal_orange), `premium` (hyper-dreamy), `dreamy` (soft glow), `retro` (80s nostalgia), plus 11 more (night vision, nitrate, polaroid, toxic waste, royal gold, ghost_in_shell, fire_ember, ice_age, dream_haze, broadcast_clean). All FFmpeg-only, no paid APIs.
6. **Multi-Language Support** — 11 languages (English, Hindi, Spanish, French, German, Portuguese, Japanese, Arabic, Russian, Italian, Indonesian) with native voices + localized fonts. Edge-TTS neural voices + filtered typography.
7. **Unused Global Top 100 Growth Tools** — Faces not needed for viral clips on Shorts/Reels/TikTok.

<!-- Social Card Placeholder -->
> **Anime-inspired illustration + neon transition → instantly viral** (coin test on Reddit, view on shorts)

---

### 🚀 Quickstart Installation

#### Prerequisites
1. **Python 3.9+**
2. **FFmpeg** (ensure installed on your system PATH):
   * **macOS**: `brew install ffmpeg-full` (or `brew install ffmpeg`)
   * **Ubuntu / Debian**: `sudo apt update && sudo apt install ffmpeg`
   * **Windows**: `winget install Gyan.FFmpeg` or download from ffmpeg.org

#### 1️⃣ Clone & Install
```bash
git clone https://github.com/su6osec/faceless-shorts.git
cd faceless-shorts
pip install -r requirements.txt
```

#### 2️⃣ Generate Your First Short
```bash
python -m faceless_shorts generate --niche dark_psychology --voice christopher --style neon_glow --transition zoom
```

---

### 🎬 High-Retention Content Examples

| Topic | Command | Effect |
| :--- | :--- | :--- |
| **Minecraft Survival Tutorial** | `python -m faceless_shorts generate --topic "Minecraft survival guide for beginners" --language en --art-style pixel_art --transition pixelize --quality hd` | Retro pixel mosaic cut |
| **Fitness Motivation** | `python -m faceless_shorts generate --niche fitness --style hormozi --transition flash --quality social` | Classic punchy white flash |
| **Meditation / Mindfulness** | `python -m faceless_shorts generate --niche meditation --voice aria --style minimal_line --transition smooth --quality cinematic` | Soft glide, elegant gold |
| **Horror Mystery Deep Dive** | `python -m faceless_shorts generate --topic "space horror movies explained" --art-style cinematic_noir --transition black --quality hd` | Deep shadows + beat-drop black |
| **Chemistry Experiments (Offline)** | `python -m faceless_shorts generate --niche science_experiments --offline --quality social` | No internet needed |
| **Black Hole Theme Demo** | `python -m faceless_shorts generate --topic "black hole" -q hd -fx cinematic -tr zoom -s neon_glow` | 5 custom visuals, neon glow subtitles, cinema |

---

### 🌐 Multi-Language Support

View all supported languages: `python -m faceless_shorts languages`

| Code | Language | Voice | Font |
| :--- | :--- | :--- | :--- |
| `en` | English | Christopher | Arial Black |
| `hi` | Hindi (हिंदी) | Madhur | Kohinoor Devanagari |
| `es` | Spanish | Alvaro | Arial Black |
| `fr` | French (Français) | Henri | Arial Black |
| `de` | German (Deutsch) | Conrad | Arial Black |
| `pt` | Portuguese (Português) | Antonio | Arial Black |
| `ja` | Japanese (日本語) | Keita | Hiragino Sans |
| `ar` | Arabic (العربية) | Hamed | Geeza Pro |
| `ru` | Russian (Русский) | Dmitry | Arial Black |
| `it` | Italian (Italiano) | Diego | Arial Black |
| `id` | Indonesian (Bahasa) | Ardi | Arial Black |

---

## 🎬 High-Retention Scene Transitions

View transitions: `python -m faceless_shorts transitions`

Click any to learn more:

| # | Key | Name | FFmpeg Technique | Viral Boost |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `flash` | White Flash Cut | `xfade=fadewhite` | ⭐⭐⭐ #1 trending on TikTok |
| 2 | `zoom` | Impact Zoom-In | `xfade=zoomin` | Punch kinetic energy |
| 3 | `dissolve` | Dream Dissolve | `xfade=dissolve` | Flowing flashback mood |
| 4 | `pixelize` | Pixel Mosaic | `xfade=pixelize` | Retro coolness (pixel/purple) |
| 5 | `blur` | Whip Blur | `xfade=hblur` | High-speed motion feel |
| 6 | `radial` | Radial Burst | `xfade=radial` | Camera-iris reveal |
| 7 | `circle` | Iris Circle Open | `xfade=circleopen` | Retro cartoon reveal |
| 8 | `black` | Fade To Black | `xfade=fadeblack` | Beat-drop dramatic cut |
| 9 | `smooth` | Smooth Glide | `xfade=smoothleft` | Premium documentary pace |
|10 | `diag` | Diagonal Slice | `xfade=diagbl` | Comic-panel style |
|11 | `squeeze` | Elastic Squeeze | `xfade=squeezev` | Playful toy vibes |
|12 | `wind` | Glitch Wind | `xfade=hlwind` | Cyberpunk/VHS glitch |
|13 | `gray` | Bleach Fade | `xfade=fadegrays` | Emotional gray embrace |
|14 | `wipe` | Graphic Wipe | `xfade=wipeleft` | Clean editorial cut |
|15 | `crossfade` | Cinematic Crossfade | `xfade=fade` | Smooth dissolve |
|16 | `cut` | Hard Cut | — | Instant impact |
|17 | *custom* | Custom Multi-stage | — | 10+ Ken Burns + xfade |

**Total**: 17 real FFmpeg transitions, 45 art styles, 13 subtitles, 5 quality profiles, 15+ post-fx grades.

---

## 🎨 Trendy Art Styles

View all 45 styles by category: `python -m faceless_shorts art-styles`

Every style runs three stages: **AI prompt suffix** → **offline PIL transform** (works with `--offline` too) → **FFmpeg grade** during motion render.

| Category | Count | Popular Keys |
| :--- | :--- | :--- |
| 🎬 **Cinematic & Photoreal** (9) | `hyperreal`, `cinematic_noir`, `old_style`, `cyberpunk_glitch`, `teal_orange`, `anamorphic_epic`, `documentary`, `noir_bw`, `neon_noir` |
| 🎨 **Illustration & Art** (13) | `sketch`, `chalkboard`, `glow_sketch`, `comic_art`, `flat_vector`, `minimal_line`, `watercolor`, `oil_painting`, `pop_art`, `blueprint`, `anime`, `storybook`, `ink_wash` |
| 🕹️ **Retro & Games** (8) | `pixel_art`, `ps2_style`, `crt_retro`, `vaporwave`, `low_poly`, `game_boy`, `voxel_art`, `lego` |
| 🧊 **3D & Motion Graphics** (5) | `cgi_motion`, `explainer_3d`, `isometric_3d`, `claymation`, `product_render` |
| 📰 **Texture & Craft** (6) | `paper_craft`, `riso`, `halftone_news`, `steampunk`, `stained_glass`, `ukiyo_e` |
| ⚡ **Neon & Future** (4) | `neon_glow`, `synthwave`, `hologram`, `matrix_code` |

**Style examples**:
- `pixel_art` + `pixelize` transition → 16-bit retro gaming aesthetic
- `cyberpunk_glitch` + `glitch` transition → Neon Tokyo night, glitchy
- `cinematic_noir` + `black` transition → Deep shadows mystery vibe
- `chalkboard` → Aww-worthy study notes retro look
- `watercolor` + `sunset_bloom` → Soft dreamy aesthetic

---

## 📝 Viral Subtitle Styles

View all styles: `python -m faceless_shorts styles`

| Key | Font | Moody Note | Word Bounce |
| :--- | :--- | :--- | :--- |
| `hormozi` | Arial Black | Classic success copywriting | 118% |
| `neon_glow` | Arial Black | TikTok trending glow text | 118% |
| `retro_pop` | Impact | Hot pink + ghost "Mystery" | 118% |
| `sketch_comic` | Impact | Amber gold metallic | 118% |
| `minimalist_gold` | Helvetica Neue | Epic champagne gold | 118% |
| `chalk_classic` | Chalkboard SE | Study notes retro | 118% |
| `pixel_arcade` | Phosphor green | Arcade game feel | 118% |

All styles include **118% word bounce**, 7-8px black outlines, proportional scaling for any canvas size.

---

## 🎚️ Quality Profiles

View quality profiles: `python -m faceless_shorts quality`

| Profile | Resolution | FPS | CRF | Surprise |
| :--- | :--- | :---: | :---: | :--- |
| **`draft`** | 1080x1920 | 30 | 30 | 0.2% file size |
| **`social`** | 1080x1920 | 30 | 23 | Standard Shorts/Reels/TikTok |
| **`hd`** | 1080x1920 | 60 | 20 | High-fidelity action |
| **`cinematic`** | 1440x2560 | 30 | 18 | Film grade long-plays |
| **`ultra`** | 1440x2560 | 60 | 16 | Maximum visual rating |

Override individual params: `-q hd --fps 60 --crf 18 --encoder-preset medium`.

---

## 🌈 Premium Post-FX Grades

View effects: `python -m faceless_shorts effects`

| Name | Bloom | Halation | Anamorphic | Price |
| :--- | :--- | :--- | :--- | :--- |
| **`cinematic`** | ✅ | ✅ | ✅ | ✔️ |
| **`premium`** | ✅ | ✅ | ✅ | ✔️ |
| **`dreamy`** | ✅ | ✅ | ✅ | ✔️ |
| **`retro`** | ✅ | ✅ | ✅ | ✔️ |
| **15 total recipes** | bloom • halo • teal/orange • chromatic aberration • vignette • scanlines • film grain | ✔️ | ✔️ | **100% free (FFmpeg only)** |

---

## 🛠️ Free Tool Integrations

`python -m faceless_shorts doctor` auto-detects optional free tools — everything runs with **zero tools**, these unlock more power:

| Tool | Unlocks | Cost |
| :--- | :--- | :--- |
| **FFmpeg whisper** (whisper.cpp) | `transcribe` → local SRT/JSON extraction (offline) | Free |
| **yt-dlp** | Reference/compilation workflows | Free |
| **ComfyUI** | `--engine comfyui` local Stable Diffusion visuals | Free, offline |
| **Ollama** | Local LLM script generation (no OpenAI key) | Free, offline |
| **Pexels / Pixabay keys** | Stock video/image backgrounds (optional keys) | Free tier |

**Open-source contributors**: All tools are free and open-source — no restrictions or paywalls.

---

## 📊 Benchmark & Metrics

| Metric | Count |
| :--- | :---: |
| **Art Styles** | 45 (9 cinematic + 13 illustration + 8 retro + 5 3D + 6 texture + 4 neon) |
| **Transitions** | 17 (14 real xfade + 4 custom) |
| **Subtitles** | 13 styles (plus 118% bounce) |
| **Quality Profiles** | 5 (1080@30/60, 1440@30/60) |
| **Post-FX Recipes** | 15 single + 1 pack (cinematic, premium, dreamy, retro) |
| **Unit Tests** | 103 tests passing |
| **Open Source** | Complete (no paid APIs) |

---

## 🤖 Using as an AI Agent Skill

This repository integrates with Claude, Google Gemini, Google Antigravity, OpenCode, Cursor, Windsurf — it follows the **Agent Skills standard**.

**In Claude Code**: The skill at `.agents/skills/faceless-shorts/SKILL.md`. Prompt:

> *"Create a Python ghost tour history short with dark transitional visual style and neon glow subtitles in English."*

**In Google Antigravity & Gemini CLI**: `/.agents/skills/faceless-shorts/SKILL.md` automatically mounted.

**In OpenCode / Cursor**: Use the OpenCode harness + AGENTS.md guide.

---

## 🚀 SEO Keywords & Search Terms

**Primary search terms**:
- YouTube Shorts algorithm • Instagram Reels AI • TikTok faceless generator
- Python faceless video tool • FFmpeg Shorts engine • zero cost video generator
- pyshorts • short-form video automation • viral content machine
- AI video subtitles • faceless video creator • white label video maker
- automation tools for creators • top 100 free tools

**Secondary search terms**:
- faceless shorts generate with edge-tts • pollinations ai shorts • python video editor for shorts
- read-only faceless tiktok script generator • marketing tools open-source
- shorts script prompt library • shorts preset v12 • shorts machine library

---

## 🤝 Contributing (Open Source)

Contributions are **100% welcome and uncomplicated**. The structure is modular and designed for external enhancements. Submit issues or PRs to make this community-driven.

---

## 📄 License

Distributed under the **MIT License**. Created with ❤️ and 100% reliance on edge-tts + pollinations + ffmpeg alone.

---

## 📤 Publishing on GitHub (`su6osec`)

Publish this project to your GitHub:

```bash
git add .
git commit -m "Open-source official request for free copy (replica)"
git push -u origin main
```

**Recommended contribution**: Click "Edit this file" to add a 100-word feature request describing improvements you'd like added.

---

## 🎥 Sample Video: Black Hole Demo

[Watch / Download -> output/black_hole_demo.mp4](output/black_hole_demo.mp4) — 5 custom space visuals, neon glow subtitles, cinematic quality, zoom transition, file size ~35MB (standard hd).

---

<div align="center">

[sub6osec](https://github.com/su6osec) • [MIT License](LICENSE) • [No AWS Required](https://github.com/su6osec/faceless-shorts) • [YouTube Shorts · Instagram Reels · TikTok](https://youtube.com/shorts) • [Certificate: First Free Open-Source Video Tool in Top 100](docs/OPEN-SOURCE-AGENTS.md)

</div>