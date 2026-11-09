# Edge-TTS Free Neural Voice Catalog

Microsoft Edge TTS provides **over 300 studio-grade neural voices across 100+ languages and locales completely free of charge**, with no API keys, no account creation, and zero usage limits.

---

## 1. Top Recommended English Voices

| Voice Shortcut | Full Voice ID | Gender | Tone & Persona | Best Content Niches |
| :--- | :--- | :--- | :--- | :--- |
| **`christopher`** | `en-US-ChristopherNeural` | Male | Deep, authoritative, intense, mysterious | Dark Psychology, Stoicism, True Crime, Thriller |
| **`guy`** | `en-US-GuyNeural` | Male | Energetic, punchy, conversational, modern | Science Facts, Tech News, Life Hacks, Trivia |
| **`aria`** | `en-US-AriaNeural` | Female | Clear, professional, articulate, trustworthy | Documentaries, History, Business, Educational |
| **`jenny`** | `en-US-JennyNeural` | Female | Youthful, natural, friendly, warm | Lifestyle, Storytelling, Motivation, Wholesome |
| **`eric`** | `en-US-EricNeural` | Male | Confident, direct, motivational | Finance, Hustle, Fitness, Discipline |
| **`ryan`** | `en-GB-RyanNeural` | Male | Sophisticated British, cinematic, scholarly | Ancient History, Philosophy, Literature, Space |
| **`sonia`** | `en-GB-SoniaNeural` | Female | Cinematic British female, dramatic | True Crime, Creepypasta, Mystery Narrations |
| **`andrew`** | `en-US-AndrewMultilingualNeural`| Male | Modern, expressive, multilingual | International content, Multi-language dubbing |
| **`brian`** | `en-US-BrianMultilingualNeural` | Male | Resonant, deep, engaging | Narration, Long-form storytelling |

---

## 2. Multi-Language Voice Catalog

### Hindi & Indian English
* `hi-IN-MadhurNeural` (Male): Dynamic, punchy Indian English / Hindi male narration.
* `hi-IN-SwaraNeural` (Female): Smooth, melodic Indian English / Hindi female storytelling.
* `en-IN-PrabhatNeural` (Male): Clear Indian English accent.
* `en-IN-NeerjaNeural` (Female): Professional Indian English speaker.

### Spanish (Español)
* `es-ES-AlvaroNeural` (Male, Spain): Powerful Castilian narration.
* `es-ES-ElviraNeural` (Female, Spain): Articulate Castilian female.
* `es-MX-JorgeNeural` (Male, Mexico): Latin American energetic male.
* `es-MX-DaliaNeural` (Female, Mexico): Latin American natural female.

### French (Français)
* `fr-FR-HenriNeural` (Male): Elegant, cinematic French narration.
* `fr-FR-DeniseNeural` (Female): Clear, sophisticated French female.

### German (Deutsch)
* `de-DE-ConradNeural` (Male): Deep, powerful German tone.
* `de-DE-KatjaNeural` (Female): Articulate German voice.

### Japanese (日本語)
* `ja-JP-KeitaNeural` (Male): Authentic Japanese narrative voice.
* `ja-JP-NanamiNeural` (Female): Friendly, expressive Japanese female.

### Portuguese (Português)
* `pt-BR-AntonioNeural` (Male, Brazil): Warm, expressive Brazilian male.
* `pt-BR-FranciscaNeural` (Female, Brazil): Natural Brazilian female.

---

## 3. Speaking Rate and Pitch Modifiers

You can tune pacing directly in Edge-TTS:

* **Shorts Standard**: `rate="+5%"` to `rate="+10%"` (Eliminates sluggishness, maintains viewer engagement).
* **Urgent / Fast Facts**: `rate="+12%"` or `rate="+15%"`.
* **Deep Mysterious**: `rate="+0%"`, `pitch="-2Hz"`.

---

## 4. Querying All Available Voices on Your Machine

To list all 300+ available voices dynamically:

```bash
python -m edge_tts --list-voices
```
