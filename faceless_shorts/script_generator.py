"""
Viral Script Generator & Dynamic Script Builder for Faceless Shorts.
Generates structured scene-by-scene scripts optimized for high retention on YouTube Shorts, Instagram Reels, and TikTok.
Includes 12+ pre-built viral niche templates and a Dynamic AI Script Generator for ANY custom topic.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class Scene:
    index: int
    text: str
    visual_prompt: str
    motion: str = "punch_zoom_in"
    duration_estimate: float = 5.0

@dataclass
class VideoScript:
    title: str
    niche: str
    target_duration: int
    hook: str
    scenes: List[Scene]
    cta: str
    tags: List[str]

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "niche": self.niche,
            "target_duration": self.target_duration,
            "hook": self.hook,
            "scenes": [asdict(s) for s in self.scenes],
            "cta": self.cta,
            "tags": self.tags,
            "full_text": " ".join(s.text for s in self.scenes)
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoScript':
        scenes = [Scene(**s) for s in data.get("scenes", [])]
        return cls(
            title=data.get("title", "Untitled Short"),
            niche=data.get("niche", "general"),
            target_duration=data.get("target_duration", 45),
            hook=data.get("hook", ""),
            scenes=scenes,
            cta=data.get("cta", ""),
            tags=data.get("tags", [])
        )

# Pre-built High-Retention Viral Presets (Ready out-of-the-box)
VIRAL_TEMPLATES = {
    "fitness": VideoScript(
        title="Stop Lifting Weights Like An Amateur",
        niche="fitness",
        target_duration=45,
        hook="Stop lifting weights like an amateur if you want real muscle growth.",
        scenes=[
            Scene(
                index=1,
                text="Stop lifting weights like an amateur if you want real muscle growth.",
                visual_prompt="intense muscular athlete chalking hands before a heavy deadlift, dark gritty gym, cinematic volumetric rim lighting",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="Most people fail because they change their workout routine every single week chasing soreness.",
                visual_prompt="stacks of rusted heavy iron dumbbell plates in dimly lit underground weight room, dramatic shadows",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=3,
                text="Your muscles do not care about variety. They respond strictly to mechanical tension and progressive overload.",
                visual_prompt="anatomical muscular human physique glowing with red electric power and energy, hyperrealistic medical 3d render",
                motion="pan_left"
            ),
            Scene(
                index=4,
                text="Pick three compound movements, master perfect form, and force your body to lift heavier every single month.",
                visual_prompt="loaded heavy Olympic barbell bending under extreme weight on squat rack, spotlight reflection",
                motion="punch_zoom_in"
            ),
            Scene(
                index=5,
                text="Discipline will build ten times more muscle than temporary motivation ever could. What is your current bench press?",
                visual_prompt="lone disciplined warrior standing in pouring rain, calm focused facial expression, cinematic epic shot",
                motion="pan_right"
            )
        ],
        cta="What is your current bench press? Comment below.",
        tags=["#fitness", "#gymmotivation", "#workouttips", "#bodybuilding", "#discipline", "#shorts"]
    ),

    "dark_psychology": VideoScript(
        title="3 Dark Psychology Tricks People Use On You",
        niche="dark_psychology",
        target_duration=45,
        hook="If someone stares at your forehead while you speak, they are doing this on purpose.",
        scenes=[
            Scene(
                index=1,
                text="If someone stares at your forehead while you speak, they are doing this on purpose.",
                visual_prompt="cinematic close up of mysterious shadowy eyes in dark room, intense gaze, dramatic rim lighting",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="It makes you feel deeply insecure and completely shatters your train of thought.",
                visual_prompt="silhouette of a stressed person holding their head in hands, dark moody neon lighting, psychological thriller atmosphere",
                motion="pan_left"
            ),
            Scene(
                index=3,
                text="Second is the silent pause. When they want you to over-explain a lie, they simply stay quiet and keep looking at you.",
                visual_prompt="two shadowy figures across an interrogation table, dramatic smoky lighting, cinema noir style",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=4,
                text="Humans naturally hate silence, so they rush to fill the gap with confessions.",
                visual_prompt="hourglass with glowing dark sand running out, ominous clockwork background, macro photorealistic shot",
                motion="punch_zoom_in"
            ),
            Scene(
                index=5,
                text="And the most dangerous one? Artificial scarcity of affection. They pull away to make you obsess.",
                visual_prompt="a golden glowing marionette puppet with severed strings in dark void, mystical hyperrealistic lighting",
                motion="pan_right"
            ),
            Scene(
                index=6,
                text="Remember, aware minds are impossible to control. Drop a follow if you refuse to be manipulated.",
                visual_prompt="ancient glowing marble statue of stoic philosopher, dark stormy lightning background, cinematic epic lighting",
                motion="punch_zoom_in"
            )
        ],
        cta="Drop a follow if you refuse to be manipulated.",
        tags=["#darkpsychology", "#mindtricks", "#psychologyfacts", "#manipulation", "#shorts"]
    ),

    "stoicism": VideoScript(
        title="Marcus Aurelius' Rule To Never Get Angry",
        niche="stoicism",
        target_duration=40,
        hook="Whenever you are offended by someone's lack of respect, ask yourself this one question.",
        scenes=[
            Scene(
                index=1,
                text="Whenever you are offended by someone's lack of respect, ask yourself this one question.",
                visual_prompt="majestic roman emperor marcus aurelius marble bust, cinematic moody lighting, ancient pillars and storm clouds",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="Is it possible for shameless people not to exist in this world? Absolutely not.",
                visual_prompt="ancient roman colosseum during turbulent thunderstorm, dramatic cinematic lighting",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=3,
                text="So why do you expect the impossible? You have encountered one of those inevitable fools.",
                visual_prompt="lone stoic warrior standing on a mountain cliff, violent wind, calm face, dramatic sunset lighting",
                motion="pan_left"
            ),
            Scene(
                index=4,
                text="You cannot control the storm outside, but you have absolute power over your inner stillness.",
                visual_prompt="calm glowing bonsai tree inside a raging glass sphere amidst tempest, surreal hyperrealistic lighting",
                motion="pan_right"
            ),
            Scene(
                index=5,
                text="Do not hand over the steering wheel of your emotions to people who cannot even control themselves.",
                visual_prompt="bronze ancient compass resting on old leather map, golden warm cinematic glow, macro shot",
                motion="punch_zoom_in"
            )
        ],
        cta="Subscribe to master your mind.",
        tags=["#stoicism", "#marcusaurelius", "#philosophy", "#mindset", "#discipline", "#shorts"]
    ),

    "mind_blowing_facts": VideoScript(
        title="3 Terrifying Space Facts That Keep Scientists Awake",
        niche="mind_blowing_facts",
        target_duration=45,
        hook="There are rogue planets hurtling through pitch-black space right now with no star.",
        scenes=[
            Scene(
                index=1,
                text="There are rogue planets hurtling through pitch-black space right now with no star.",
                visual_prompt="lone frozen dark rogue planet wandering through deep interstellar abyss, faint distant starlight",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="Billions of these celestial phantoms drift freely, completely undetected until they enter a solar system.",
                visual_prompt="vast majestic galaxy spiral with ominous dark nebulae, cosmic dust clouds, deep space photography",
                motion="pan_left"
            ),
            Scene(
                index=3,
                text="Even stranger, the Boötes Void is a 330 million light-year expanse of almost complete emptiness.",
                visual_prompt="a colossal terrifying cosmic void surrounded by glittering web of galaxies, James Webb style space telescope image",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=4,
                text="Scientists still cannot explain why such a massive region of the universe has virtually no galaxies.",
                visual_prompt="futuristic astronaut looking out of spacecraft window into deep dark cosmos, visor reflection of stars",
                motion="pan_right"
            ),
            Scene(
                index=5,
                text="If humanity disappeared tomorrow, the universe would not even blink. Which cosmic secret scares you the most?",
                visual_prompt="earth floating in silent infinite darkness, tiny blue dot, cinematic epic NASA style photorealistic shot",
                motion="punch_zoom_in"
            )
        ],
        cta="Which cosmic secret scares you the most?",
        tags=["#spacefacts", "#universe", "#cosmicmystery", "#astronomy", "#didyouknow", "#shorts"]
    ),

    "motivation": VideoScript(
        title="Monk Mode Will Change Your Life In 90 Days",
        niche="motivation",
        target_duration=42,
        hook="If you want to become unrecognizable in six months, you must disappear for ninety days.",
        scenes=[
            Scene(
                index=1,
                text="If you want to become unrecognizable in six months, you must disappear for ninety days.",
                visual_prompt="solitary silhouette of a man meditating on foggy mountain peak at dawn, golden sunrise rim light",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="Cut out cheap dopamine, toxic friendships, and endless mindless scrolling.",
                visual_prompt="shattered glowing smartphone screen lying on dark cold stone pavement, sparks and smoke",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=3,
                text="When you isolate yourself to master one high-income skill and train your body daily, magic happens.",
                visual_prompt="intense scholar writing notes in ancient candlelit library surrounded by towering bookshelves",
                motion="pan_left"
            ),
            Scene(
                index=4,
                text="People will wonder where you went, but you will re-emerge with unshakeable confidence and focus.",
                visual_prompt="sharp dressed confident man walking out of shadowy dark corridor into bright modern daylight",
                motion="pan_right"
            ),
            Scene(
                index=5,
                text="Are you willing to sacrifice short-term comfort for lifelong freedom? Comment YES if you are locked in.",
                visual_prompt="majestic lion looking straight into camera with fierce golden eyes, hyperrealistic cinematic portrait",
                motion="punch_zoom_in"
            )
        ],
        cta="Comment YES if you are locked in.",
        tags=["#motivation", "#monkmode", "#selfimprovement", "#discipline", "#success", "#shorts"]
    ),

    "finance_hustle": VideoScript(
        title="The Brutal Rule Wealthy People Never Break",
        niche="finance_hustle",
        target_duration=40,
        hook="Poor people trade their time for money. The wealthy buy other people's time.",
        scenes=[
            Scene(
                index=1,
                text="Poor people trade their time for money. The wealthy buy other people's time.",
                visual_prompt="luxury modern penthouse office overlooking skyline at night, glowing glass desk, sleek dark billionaire aesthetic",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="If you are the only engine generating your income, you are one illness away from absolute zero.",
                visual_prompt="golden mechanical clock gears spinning amidst dark smoke, dramatic luxury lighting, macro shot",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=3,
                text="Every single dollar you save should not sit in a bank. It must act as an employee deployed to capture more dollars.",
                visual_prompt="stacks of crisp currency neatly arranged next to glowing stock charts on dark screen, cinematic lighting",
                motion="pan_left"
            ),
            Scene(
                index=4,
                text="Build assets that print cash while you sleep, or you will work until the day you die.",
                visual_prompt="golden bullion bars gleaming under focused spotlight in high-security bank vault, hyperrealistic wallpaper",
                motion="pan_right"
            ),
            Scene(
                index=5,
                text="Drop a follow if you choose financial freedom over comfort.",
                visual_prompt="sleek black sports car driving into dark neon futuristic city sunset, cinematic reflections",
                motion="punch_zoom_in"
            )
        ],
        cta="Drop a follow if you choose financial freedom over comfort.",
        tags=["#wealthmindset", "#financialfreedom", "#moneyrules", "#investing", "#discipline", "#shorts"]
    ),

    "ai_tech": VideoScript(
        title="Humanoid Robots Are About To Replace Everyone",
        niche="ai_tech",
        target_duration=45,
        hook="In less than five years, humanoid robots will walk among us in public.",
        scenes=[
            Scene(
                index=1,
                text="In less than five years, humanoid robots will walk among us in public.",
                visual_prompt="futuristic sleek white humanoid robot standing among humans in bustling modern city street, photorealistic",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="Major tech titans are already deploying bipedal androids in factories that never tire or complain.",
                visual_prompt="automated gigafactory assembly line with robotic arms and humanoid workers under neon lights",
                motion="pan_left"
            ),
            Scene(
                index=3,
                text="Equipped with advanced multimodal neural networks, they learn physical tasks simply by watching human video.",
                visual_prompt="close up of glowing robotic android face with synthetic blue eyes and intricate micro-circuitry",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=4,
                text="The jobs of repetitive labor will vanish overnight. The only safe humans are those who know how to command the machines.",
                visual_prompt="human programmer interacting with holographic 3d AI neural code in dark cybersecurity center",
                motion="pan_right"
            ),
            Scene(
                index=5,
                text="Are you preparing for the AGI era or will you be caught off guard? Drop your thoughts below.",
                visual_prompt="cyberpunk silhouette of human and robot shaking hands against glowing skyline, dramatic concept art",
                motion="punch_zoom_in"
            )
        ],
        cta="Are you preparing for the AGI era or will you be caught off guard?",
        tags=["#aitech", "#robotics", "#futuretech", "#artificialintelligence", "#technews", "#shorts"]
    ),

    "horror_mystery": VideoScript(
        title="The Creepiest Incident In Naval History",
        niche="horror_mystery",
        target_duration=45,
        hook="In 1947, ships across the Straits of Malacca picked up a chilling Morse code SOS.",
        scenes=[
            Scene(
                index=1,
                text="In 1947, ships across the Straits of Malacca picked up a chilling Morse code SOS.",
                visual_prompt="vintage 1940s naval radio operator listening in dimly lit radio room, static green glow, cinematic dark horror aesthetic",
                motion="punch_zoom_in"
            ),
            Scene(
                index=2,
                text="The message simply read: All officers including captain are dead. I die.",
                visual_prompt="vintage typewriter printing eerie morse code on aged parchment, macro shallow depth of field, dramatic dark shadows",
                motion="pan_left"
            ),
            Scene(
                index=3,
                text="When rescue teams boarded the SS Ourang Medan, they found the entire crew deceased, eyes wide open, staring at the sky.",
                visual_prompt="ghost ship floating in silent eerie foggy ocean under moonlight, cold blue mist, chilling cinematic thriller composition",
                motion="dramatic_zoom_out"
            ),
            Scene(
                index=4,
                text="There was not a single scratch or sign of violence on any body.",
                visual_prompt="creepy abandoned ship bridge with wheel spinning slowly in wind, flickering emergency lights",
                motion="pan_right"
            ),
            Scene(
                index=5,
                text="Before investigators could search the lower deck, an unexplained fire forced them off, and the vessel sank forever.",
                visual_prompt="burning silhouette of an old cargo ship sinking into stormy dark waves, fiery orange sparks, epic atmospheric lighting",
                motion="punch_zoom_in"
            )
        ],
        cta="What do you think killed the crew?",
        tags=["#unsolvedmystery", "#ghostship", "#truehorror", "#creepyfacts", "#shorts"]
    )
}

LLM_SYSTEM_PROMPT = """You are an elite short-form video scriptwriter who crafts viral YouTube Shorts, Instagram Reels, and TikTok scripts with over 70% average percentage viewed (APV).

RULES:
1. Pacing: Total spoken words must be between 90 and 140 words (~40-55 seconds).
2. The Hook (0-3s): Must trigger intense curiosity, fear of missing out, or a pattern interrupt. Never start with "Hello" or "Today we will discuss".
3. Scene Breakdown: Split the script into 4-7 punchy scenes.
4. Visual Prompts: For each scene, create a hyper-descriptive prompt for AI image generation (vertical 9:16, photorealistic, dramatic lighting, 8k).
5. Seamless Ending: End with an open-ended engagement question or a seamless loop phrase.

Output ONLY valid JSON formatted as follows:
{
  "title": "Viral Click-Worthy Title",
  "niche": "niche_name",
  "target_duration": 45,
  "hook": "Opening hook sentence",
  "scenes": [
    {
      "index": 1,
      "text": "First punchy spoken sentence.",
      "visual_prompt": "Cinematic visual prompt for image generator, photorealistic 8k vertical wallpaper",
      "motion": "punch_zoom_in"
    }
  ],
  "cta": "Final call to action or question",
  "tags": ["#shorts", "#viral", "#niche"]
}
"""

class DynamicScriptBuilder:
    """
    Intelligent Builder that constructs viral, publication-ready scripts
    for ANY custom topic or niche across multiple languages without requiring pre-stored templates.
    """
    @staticmethod
    def build(topic: str, niche: Optional[str] = None, language: str = "en") -> VideoScript:
        clean_topic = topic.strip()
        niche_key = (niche or re.sub(r"[^\w\s]", "", clean_topic).replace(" ", "_")).lower()
        lang = (language or "en").lower()

        # Localized script lines based on selected language
        if lang == "hi":
            title = f"{clean_topic} का कड़वा सच"
            hook = f"{clean_topic} के बारे में कोई आपको कड़वा सच नहीं बताता, लेकिन यह रहा।"
            scene_1_text = f"{clean_topic} के बारे में कोई आपको कड़वा सच नहीं बताता, लेकिन यह रहा।"
            scene_2_text = f"निन्यानवे प्रतिशत लोग {clean_topic} को गलत तरीके से करते हैं और सोचते हैं कि वे असफल क्यों हुए।"
            scene_3_text = f"असली रहस्य किसी भी जटिल तरीके को जोड़ने से पहले बुनियादी बातों में महारत हासिल करना है।"
            scene_4_text = f"एक बार जब आप भटकाव हटाकर हर दिन अभ्यास करते हैं, तो सफलता निश्चित हो जाती है।"
            scene_5_text = f"इस वीडियो को भूलने से पहले अभी सेव करें और अपने कौशल को निखारने के लिए फॉलो करें।"
            cta = "इस वीडियो को सेव करें और कमेंट में अपनी राय बताएं।"
            tags = [f"#{niche_key}", "#shorts", "#hindi", "#viral", "#foryou", "#mindset"]
        elif lang == "es":
            title = f"La Verdad Sobre {clean_topic.title()}"
            hook = f"Nadie te dice la verdad sobre {clean_topic}, pero aquí está."
            scene_1_text = f"Nadie te dice la verdad sobre {clean_topic}, pero aquí está."
            scene_2_text = f"El noventa y nueve por ciento de las personas abordan {clean_topic} al revés y se preguntan por qué fallan."
            scene_3_text = f"El verdadero secreto es dominar los fundamentos antes de añadir tácticas complicadas."
            scene_4_text = f"Una vez que eliminas el ruido y eres constante todos los días, los resultados son inevitables."
            scene_5_text = f"Guarda este video antes de que lo olvides y síguenos para dominar esta habilidad."
            cta = "Guarda este video y comparte tu opinión en los comentarios."
            tags = [f"#{niche_key}", "#shorts", "#viral", "#parati", "#motivacion"]
        elif lang == "fr":
            title = f"La Vérité Sur {clean_topic.title()}"
            hook = f"Personne ne vous dit la vérité sur {clean_topic}, mais la voici."
            scene_1_text = f"Personne ne vous dit la vérité sur {clean_topic}, mais la voici."
            scene_2_text = f"Quatre-vingt-dix-neuf pour cent des gens abordent {clean_topic} à l'envers et s'étonnent d'échouer."
            scene_3_text = f"Le secret réside dans la maîtrise des principes fondamentaux avant toute tactique compliquée."
            scene_4_text = f"Une fois le bruit éliminé et une exécution quotidienne, les résultats deviennent inévitables."
            scene_5_text = f"Enregistrez cette vidéo avant de l'oublier et abonnez-vous pour progresser."
            cta = "Enregistrez cette vidéo et donnez votre avis en commentaire."
            tags = [f"#{niche_key}", "#shorts", "#viral", "#pourtoi", "#developpement"]
        else: # Default English
            title = f"The Brutal Truth About {clean_topic.title()}"
            hook = f"Nobody tells you the brutal truth about {clean_topic}, but here it is."
            scene_1_text = f"Nobody tells you the brutal truth about {clean_topic}, but here it is."
            scene_2_text = f"Most people chase flashy tricks in {clean_topic} and wonder why nothing sticks after one week."
            scene_3_text = f"The ones who actually win at {clean_topic} obsess over one boring fundamental that everybody else skips."
            scene_4_text = f"Stack that one fundamental every single day for ninety days and {clean_topic} starts compounding like interest."
            scene_5_text = f"Save this before it disappears, and drop a follow if you truly want to win at {clean_topic}."
            cta = "Save this video right now and drop a follow to master your craft."
            tags = [f"#{niche_key}", "#shorts", "#viral", "#foryou", "#mindset"]

        # High-impact visual prompts kept in English for peak image synthesis quality
        scene_1_prompt = f"dramatic cinematic opening shot representing {clean_topic}, intense atmosphere, volumetric lighting, photorealistic 8k"
        scene_2_prompt = f"chaotic scattered attempts and frustration around {clean_topic}, high contrast shadows, moody cinematic"
        scene_3_prompt = f"glowing blueprint and precise mechanism representing the core fundamental of {clean_topic}, macro lens"
        scene_4_prompt = f"disciplined figure executing daily practice of {clean_topic} in sleek modern environment, cinematic golden hour lighting"
        scene_5_prompt = f"triumphant silhouette mastering {clean_topic} at sunrise overlooking vast landscape, cinematic masterpiece"

        scenes = [
            Scene(1, scene_1_text, scene_1_prompt, "punch_zoom_in"),
            Scene(2, scene_2_text, scene_2_prompt, "dramatic_zoom_out"),
            Scene(3, scene_3_text, scene_3_prompt, "pan_left"),
            Scene(4, scene_4_text, scene_4_prompt, "whip_zoom"),
            Scene(5, scene_5_text, scene_5_prompt, "pan_right")
        ]

        return VideoScript(
            title=title,
            niche=niche_key,
            target_duration=42,
            hook=hook,
            scenes=scenes,
            cta=cta,
            tags=tags
        )

def get_template(niche: str, language: str = "en") -> Optional[VideoScript]:
    """Retrieve a pre-built viral script template by niche, or check presets folder.
    Checks language-suffixed presets first (e.g. presets/blackhole_en.json), then
    the plain preset file (e.g. presets/stoicism.json)."""
    lang = (language or "en").lower()
    if niche in VIRAL_TEMPLATES and lang == "en":
        return VIRAL_TEMPLATES[niche]

    # Language-suffixed preset first (blackhole_en.json / blackhole_hi.json);
    # the plain preset only applies to English so non-English voices never get
    # handed an English script. Also try the underscore-stripped key so that
    # `--topic "Black Hole"` (key: black_hole) resolves presets/blackhole_en.json.
    variants = [niche]
    stripped = niche.replace("_", "")
    if stripped != niche:
        variants.append(stripped)

    candidates = []
    for variant in variants:
        candidates.append(os.path.join("presets", f"{variant}_{lang}.json"))
    if lang == "en":
        for variant in variants:
            candidates.append(os.path.join("presets", f"{variant}.json"))

    for candidate in candidates:
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                data = json.load(f)
            return VideoScript.from_dict(data)

    return None

# --------------------------------------------------------------------------- #
# Curated topic knowledge packs: factual, high-retention scene scripts for
# popular custom topics. Matched by keyword against --topic / --niche.
# --------------------------------------------------------------------------- #
TOPIC_KNOWLEDGE = {
    "human_brain": {
        "match": ["human brain", "brain", "neuroscience", "memory", "mind"],
        "title": "Your Brain Is Lying To You Every Single Day",
        "hook": "Your brain deletes ninety-nine percent of what you see and shows you a comfortable fiction.",
        "scenes": [
            {
                "text": "Your brain deletes ninety-nine percent of what you see and shows you a comfortable fiction.",
                "visual_prompt": "glowing translucent human brain floating in dark laboratory, synapses firing electric blue and gold, cinematic macro lighting, 8k vertical",
                "motion": "punch_zoom_in"
            },
            {
                "text": "It fills gaps with prediction, so you are literally seeing the past roughly half a second before it arrives.",
                "visual_prompt": "human eye extreme close up reflecting a cascade of glowing data streams, deep cinematic reflections, 8k vertical",
                "motion": "dramatic_zoom_out"
            },
            {
                "text": "Every time you remember something, your brain rewrites it. Memory is editing, not playback.",
                "visual_prompt": "old cassette tape unwinding into glowing neural fibers being rewritten, surreal dark studio lighting, 8k vertical",
                "motion": "pan_left"
            },
            {
                "text": "That is why eyewitnesses disagree and why your happiest days feel different each time you recall them.",
                "visual_prompt": "three silhouetted witnesses seeing three different glowing versions of the same event, dramatic noir lighting, 8k vertical",
                "motion": "whip_zoom"
            },
            {
                "text": "But the same glitch is a feature: focus on one skill for sixty days and your brain physically rewires around it.",
                "visual_prompt": "neural pathways restructuring into a bright golden highway of myelin, hyperreal microscopic render, 8k vertical",
                "motion": "pan_right"
            },
            {
                "text": "Your software can be updated. What will you choose to install?",
                "visual_prompt": "silhouette of a person with glowing upgrade interface hologram emerging from their mind, dark cinematic, 8k vertical",
                "motion": "pulse_heartbeat"
            }
        ],
        "cta": "What will you choose to install? Comment below.",
        "tags": ["#neuroscience", "#brainfacts", "#psychology", "#memory", "#mindset", "#shorts"]
    },
    "sleep": {
        "match": ["sleep", "insomnia", "rest", "circadian"],
        "title": "What Happens If You Stop Sleeping For 7 Days",
        "hook": "After just three sleepless nights, your brain starts seeing things that are not there.",
        "scenes": [
            {
                "text": "After just three sleepless nights, your brain starts seeing things that are not there.",
                "visual_prompt": "exhausted person staring at glowing clock at 3am in pitch dark room, cold blue light, cinematic horror lighting, 8k vertical",
                "motion": "punch_zoom_in"
            },
            {
                "text": "During sleep your brain flushes toxic waste through a cleansing system that only opens at night.",
                "visual_prompt": "glowing cerebrospinal fluid waves washing through translucent brain channels, scientific macro render, 8k vertical",
                "motion": "dramatic_zoom_out"
            },
            {
                "text": "Skip that wash and proteins pile up exactly where Alzheimer's disease begins.",
                "visual_prompt": "dark plaque proteins accumulating between glowing neurons, ominous medical visualization, 8k vertical",
                "motion": "pan_left"
            },
            {
                "text": "One all-nighter cuts your daytime focus by forty percent, worse than being legally drunk.",
                "visual_prompt": "blurry office worker with double vision ghosting, motion blur portraits, cold clinical light, 8k vertical",
                "motion": "whip_zoom"
            },
            {
                "text": "Protect the eight hours. It is the only upgrade your body cannot buy or skip.",
                "visual_prompt": "peaceful silhouette sleeping under a glowing protective dome of stars, serene cinematic night, 8k vertical",
                "motion": "orbit_sway"
            }
        ],
        "cta": "Are you getting eight hours? Be honest below.",
        "tags": ["#sleep", "#healthfacts", "#brainhealth", "#insomnia", "#science", "#shorts"]
    },
    "deep_ocean": {
        "match": ["ocean", "sea", "deep sea", "mariana", "underwater"],
        "title": "The Deep Ocean Hides Something Terrifying",
        "hook": "Ninety-five percent of our ocean has never been seen by human eyes.",
        "scenes": [
            {
                "text": "Ninety-five percent of our ocean has never been seen by human eyes.",
                "visual_prompt": "deep dark ocean abyss with a lone submarine light beam vanishing into blackness, cinematic scale, 8k vertical",
                "motion": "punch_zoom_in"
            },
            {
                "text": "Below one thousand meters there is zero sunlight, crushing pressure, and temperatures near freezing.",
                "visual_prompt": "deep sea trench walls under immense pressure, single bioluminescent glow, photorealistic, 8k vertical",
                "motion": "dramatic_zoom_out"
            },
            {
                "text": "Yet creatures here generate their own light, hunt with living lasers, and survive being frozen solid.",
                "visual_prompt": "bioluminescent anglerfish glowing electric blue in absolute darkness, macro deep sea photography, 8k vertical",
                "motion": "pan_left"
            },
            {
                "text": "We have mapped Mars in more detail than our own seafloor.",
                "visual_prompt": "split composition: red Mars surface above, dark unexplored ocean trench below, epic concept art, 8k vertical",
                "motion": "whip_zoom"
            },
            {
                "text": "The next giant discovery will not come from the stars. It will come from the deep.",
                "visual_prompt": "massive unknown glowing silhouette beneath deep ocean surface, awe and dread, cinematic, 8k vertical",
                "motion": "rise_up"
            }
        ],
        "cta": "Would you dive into the unknown? Comment below.",
        "tags": ["#deepocean", "#oceanfacts", "#scifi", "#nature", "#didyouknow", "#shorts"]
    },
    "mars": {
        "match": ["mars", "red planet", "space colonization"],
        "title": "Why Mars Will Kill The First Colonists",
        "hook": "The first people to live on Mars will die in ways nobody on Earth is ready for.",
        "scenes": [
            {
                "text": "The first people to live on Mars will die in ways nobody on Earth is ready for.",
                "visual_prompt": "lone astronaut standing before a giant rust-red Martian dust storm approaching a habitat dome, cinematic epic, 8k vertical",
                "motion": "punch_zoom_in"
            },
            {
                "text": "Martian dust is like ground glass. It poisons your lungs, jams your suits, and it gets everywhere.",
                "visual_prompt": "extreme macro of jagged red Martian dust particles under microscope light, scientific render, 8k vertical",
                "motion": "dramatic_zoom_out"
            },
            {
                "text": "There is no magnetic field, so solar radiation silently shreds your DNA every single day.",
                "visual_prompt": "glowing radiation waves striking a small red planet surface, dangerous violet glow, 8k vertical",
                "motion": "pan_left"
            },
            {
                "text": "And the soil is laced with toxic perchlorates that would poison any crop you try to grow.",
                "visual_prompt": "astronaut hands in toxic red Martian soil with wilting green sprout, shallow depth of field, 8k vertical",
                "motion": "pan_right"
            },
            {
                "text": "Mars does not want us. And that is exactly why some people will go anyway.",
                "visual_prompt": "rocket lifting off from red Martian surface toward a distant blue Earth in the sky, epic cinematic, 8k vertical",
                "motion": "shockwave_out"
            }
        ],
        "cta": "Would you risk it? Comment below.",
        "tags": ["#mars", "#space", "#astronomy", "#spacex", "#science", "#shorts"]
    }
}

def _knowledge_lookup(topic: str) -> Optional[VideoScript]:
    """Find a curated knowledge pack matching this topic, if any."""
    clean = topic.strip().lower()
    for pack in TOPIC_KNOWLEDGE.values():
        if any(keyword in clean for keyword in pack["match"]):
            scenes = [
                Scene(index=i + 1, text=s["text"], visual_prompt=s["visual_prompt"], motion=s["motion"])
                for i, s in enumerate(pack["scenes"])
            ]
            return VideoScript(
                title=pack["title"],
                niche=re.sub(r"[^\w\s]", "", topic).replace(" ", "_").lower(),
                target_duration=45,
                hook=pack["hook"],
                scenes=scenes,
                cta=pack["cta"],
                tags=pack["tags"],
            )
    return None

def _llm_lookup(topic: str, language: str) -> Optional[VideoScript]:
    """Ask a free local LLM (Ollama / OpenAI-compatible) for a fresh script.
    Returns None instantly when no LLM is reachable."""
    try:
        from faceless_shorts.integrations import LLMScriptWriter
        writer = LLMScriptWriter()
        if not writer.available():
            return None
        data = writer.write_script(
            topic=topic,
            language=language,
            system_prompt=LLM_SYSTEM_PROMPT,
        )
        if not data or not data.get("scenes"):
            return None
        scenes = [
            Scene(
                index=s.get("index", i + 1),
                text=s.get("text", ""),
                visual_prompt=s.get("visual_prompt", ""),
                motion=s.get("motion", "punch_zoom_in"),
            )
            for i, s in enumerate(data["scenes"])
            if s.get("text")
        ]
        if len(scenes) < 3:
            return None
        key = re.sub(r"[^\w\s]", "", topic).replace(" ", "_").lower()
        return VideoScript(
            title=data.get("title", f"The Truth About {topic.title()}"),
            niche=key,
            target_duration=int(data.get("target_duration", 45)),
            hook=data.get("hook", scenes[0].text),
            scenes=scenes,
            cta=data.get("cta", ""),
            tags=data.get("tags", [f"#{key}", "#shorts"]),
        )
    except Exception:
        return None

def create_or_get_script(niche_or_topic: str, language: str = "en", use_llm: bool = True) -> VideoScript:
    """
    Unified resolver:
      1. Pre-built template / language-suffixed preset (presets/<niche>_<lang>.json)
      2. Curated topic knowledge pack (factual scene scripts for popular topics)
      3. Free local LLM (Ollama / OpenAI-compatible) when reachable
      4. Dynamic viral script builder for any topic (all 11 languages)
    """
    key = niche_or_topic.lower().replace(" ", "_")
    lang = (language or "en").lower()

    # 1. Templates & presets (language aware)
    template = get_template(key, language=lang)
    if template:
        return template

    # 2. Curated knowledge packs
    knowledge = _knowledge_lookup(niche_or_topic)
    if knowledge:
        return knowledge

    # 3. Optional free LLM (returns instantly when unreachable)
    if use_llm:
        llm_script = _llm_lookup(niche_or_topic, lang)
        if llm_script:
            return llm_script

    # 4. Dynamic viral script builder
    return DynamicScriptBuilder.build(topic=niche_or_topic, niche=key, language=lang)
