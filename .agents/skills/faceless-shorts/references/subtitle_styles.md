# Viral Subtitle Styles & Animation Cheatsheet

Subtitles are not just accessibility tools in short-form content—they are the **primary visual anchor** that keeps the viewer's eyes fixated on screen. Over 70% of viewers scroll social feeds with sound muted or low.

---

## 1. Supported Style Presets

### 1. `hormozi` (The Alex Hormozi Classic)
* **Font**: Arial Bold / Montserrat Black (All Uppercase)
* **Colors**:
  * Inactive Text: Pure White (`#FFFFFF`, ASS: `&H00FFFFFF`)
  * Active Word Highlight: Vibrant Neon Yellow (`#F72B00` in BGR -> `#00F72B`, ASS: `&H002BF7&`)
  * Outline: Solid Black 6px stroke (`&H00000000`)
  * Shadow: 3px semi-transparent
* **Chunks**: 3 words per screen
* **Best For**: Motivation, Business, Psychology, Life Lessons

### 2. `neon_cyberpunk`
* **Font**: Arial Bold / Impact (All Uppercase)
* **Colors**:
  * Inactive Text: Crisp Off-White / Lime
  * Active Word Highlight: Electric Cyan (`#00FFFF`, ASS: `&H00FFFF00&`)
  * Outline: Dark Deep Purple/Black 5px stroke (`&H00220011`)
* **Chunks**: 3 words per screen
* **Best For**: Tech, AI Breakthroughs, Sci-Fi, Space Facts

### 3. `crimson_alert`
* **Font**: Arial Black / Futura Bold (All Uppercase)
* **Colors**:
  * Inactive Text: Stark White
  * Active Word Highlight: Blood Crimson Red (`#FF1111`, ASS: `&H001111FF&`)
  * Outline: Pure Black 6px
* **Chunks**: 2 words per screen (Ultra-punchy rapid focus)
* **Best For**: True Crime, Horror, Dark Secrets, Warnings

### 4. `beast_pop` (MrBeast Style)
* **Font**: Arial Bold / Komika Axis (All Uppercase)
* **Colors**:
  * Inactive Text: Bright Electric Yellow (`#00FFFF`)
  * Active Word Highlight: Toxic Lime Green (`#00FF00`, ASS: `&H0000FF00&`)
  * Outline: Heavy Black 7px
* **Chunks**: 3 words per screen
* **Best For**: Crazy Facts, Entertainment, High-Energy Trivia

### 5. `minimalist_gold`
* **Font**: Arial Medium / Helvetica Neue
* **Colors**:
  * Inactive Text: Soft Silver Gray (`#E0E0E0`)
  * Active Word Highlight: Warm Champagne Gold (`#E8C850`, ASS: `&H0050C8E8&`)
  * Outline: Subtle 4px dark border
* **Chunks**: 4 words per screen
* **Best For**: Luxury, Stoicism, Meditative Philosophy, Poetry

---

## 2. Advanced SubStation Alpha (.ASS) Color Format

ASS subtitle files use **BGR (Blue-Green-Red)** hexadecimal notation with an optional Alpha prefix:

$$\text{Format: } \&\text{H}[AA][BB][GG][RR]\&$$

* White: `&H00FFFFFF&` (BB=FF, GG=FF, RR=FF)
* Yellow: `&H0000FFFF&` (BB=00, GG=FF, RR=FF)
* Bright Gold: `&H002BF7&` (BB=00, GG=F7, RR=2B)
* Cyan: `&H00FFFF00&` (BB=FF, GG=FF, RR=00)
* Pure Red: `&H000000FF&` (BB=00, GG=00, RR=FF)
* Pure Green: `&H0000FF00&` (BB=00, GG=FF, RR=00)
* Black: `&H00000000&` (BB=00, GG=00, RR=00)

---

## 3. Positioning and Safe Zones for Shorts

In vertical 9:16 (1080x1920):

* **Top 250px**: Header / Search bar UI (Avoid)
* **Bottom 450px**: Caption text, channel avatar, subscribe button, audio title (Avoid)
* **Right 150px**: Like, Dislike, Comment, Share buttons (Avoid)
* **The Golden Safe Zone**: $Y = 1100$ to $Y = 1350$ (Centered in the lower middle third, right above the channel handle).
  In our ASS configuration, `MarginV: 680` positions the subtitles squarely in this high-retention golden zone.
