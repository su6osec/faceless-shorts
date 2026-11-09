"""
Master Video Rendering Engine for Faceless Shorts.
Features:
- Continuous Stream Voice Synthesis (Zero MP3 Concatenation Desync)
- Frame-Accurate Speech, Visual Cut & Subtitle Synchronization
- High-Retention Scene Transitions (17 xfade cuts: flash, zoom, dissolve, pixelize, ...)
- Dynamic Retention Progress Bar (Glowing animated bottom bar for maximum completion rate)
- Punchy Ken Burns Dynamic Motion (10 camera moves incl. orbit sway, pulse, shockwave)
- Three-Stage Art Styling: AI prompt suffix -> offline PIL pixel-op -> FFmpeg grade
- Premium Post-FX Chain (bloom, halation, chromatic aberration, film grain, teal-orange, ...)
- Quality Profiles (draft/social/hd/cinematic/ultra: fps, CRF, encoder preset, resolution)
- Parallel AI image generation (network-bound scenes synthesized concurrently)
- Free image engines: Pollinations Flux / local ComfyUI / offline procedural
- ASS Karaoke Subtitles with Dynamic 118% Word Bounce & neon glow
- Studio Sound Design: Sub-Bass Drones, Transition Whoosh SFX & -14 LUFS Audio Ducking
"""

import os
import shutil
import subprocess
import time
from typing import Dict, List, Optional, Tuple

from faceless_shorts.config import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    DEFAULT_FPS,
    ART_STYLES,
    TRANSITIONS,
    DEFAULT_TRANSITION,
    PROGRESS_BAR_CONFIG,
    LANGUAGES,
    DEFAULT_LANGUAGE,
    QUALITY_PROFILES,
    DEFAULT_QUALITY,
    DEFAULT_IMAGE_ENGINE,
)
from faceless_shorts.script_generator import VideoScript
from faceless_shorts.tts_engine import TTSEngine, WordTimestamp
from faceless_shorts.visuals import VisualManager
from faceless_shorts.subtitles import SubtitleGenerator
from faceless_shorts.audio import SoundEngine
from faceless_shorts.postfx import PostFX
from faceless_shorts.vfx import VFXManager, VFX_PRESETS

class VideoRenderer:
    def __init__(
        self,
        voice: Optional[str] = None,
        language: str = DEFAULT_LANGUAGE,
        subtitle_style: str = "hormozi",
        art_style: str = "hyperreal",
        transition: str = DEFAULT_TRANSITION,
        vfx: Optional[str] = None,
        progress_bar: bool = True,
        bg_music_preset: Optional[str] = "none",
        speech_rate: str = "+0%",
        work_dir: str = ".temp_render",
        quality: str = DEFAULT_QUALITY,
        fps: Optional[int] = None,
        effects: Optional[str] = None,
        engine: str = DEFAULT_IMAGE_ENGINE,
        crf: Optional[int] = None,
        encoder_preset: Optional[str] = None,
    ):
        self.language = (language or DEFAULT_LANGUAGE).lower()

        # Resolve voice according to language if not explicitly provided
        if not voice:
            if self.language in LANGUAGES:
                self.voice = LANGUAGES[self.language]["default_voice"]
            else:
                self.voice = "christopher"
        else:
            self.voice = voice

        self.transition = transition if transition in TRANSITIONS else DEFAULT_TRANSITION
        self.progress_bar = progress_bar
        self.subtitle_style = subtitle_style
        self.art_style = art_style if art_style in ART_STYLES else "hyperreal"
        self.bg_music_preset = bg_music_preset
        self.speech_rate = speech_rate
        self.work_dir = work_dir
        self.engine = engine or DEFAULT_IMAGE_ENGINE

        # Quality profile: fps / CRF / x264 preset / audio bitrate / canvas size
        profile = QUALITY_PROFILES.get(quality, QUALITY_PROFILES[DEFAULT_QUALITY])
        self.quality = quality if quality in QUALITY_PROFILES else DEFAULT_QUALITY
        self.width = int(profile["width"])
        self.height = int(profile["height"])
        self.fps = int(fps or profile["fps"])
        self.crf = int(crf if crf is not None else profile["crf"])
        self.encoder_preset = encoder_preset or profile["preset"]
        self.audio_bitrate = profile["audio_bitrate"]

        # Premium post-FX chain (effect names and/or packs from PostFX)
        if isinstance(effects, str):
            self.effects = [e.strip() for e in effects.split(",") if e.strip()]
        elif isinstance(effects, list):
            self.effects = [str(e).strip() for e in effects if str(e).strip()]
        else:
            self.effects = []
        if "none" in self.effects or "nofx" in self.effects:
            self.effects = []

        # Parse VFX modes (overlay/particle pass)
        if isinstance(vfx, str):
            self.vfx_modes = [m.strip().lower() for m in vfx.split(",") if m.strip()]
        elif isinstance(vfx, list):
            self.vfx_modes = [m.lower() for m in vfx]
        else:
            self.vfx_modes = []

        self.tts = TTSEngine(default_voice=self.voice)
        self.visuals = VisualManager(
            cache_dir=os.path.join(work_dir, "cache"),
            art_style=self.art_style,
            engine=self.engine,
            width=self.width,
            height=self.height,
            fps=self.fps,
        )
        self.subtitles = SubtitleGenerator(
            style_name=subtitle_style,
            language=self.language,
            width=self.width,
            height=self.height,
        )
        self.audio = SoundEngine()
        self.vfx_mgr = VFXManager(work_dir=work_dir)

    def _map_words_to_scenes(
        self,
        scenes: List,
        all_words: List[WordTimestamp],
        total_duration: float
    ) -> List[Tuple[float, float, float]]:
        """
        Map continuous word stream to individual scenes to establish exact
        start, end, and duration boundaries for each visual clip.
        Returns list of (start_time, end_time, duration).
        """
        scene_boundaries = []
        word_cursor = 0
        total_words_count = len(all_words)

        for i, scene in enumerate(scenes):
            scene_word_tokens = scene.text.split()
            count = len(scene_word_tokens)

            # Words for this scene
            scene_words = all_words[word_cursor : min(word_cursor + count, total_words_count)]
            word_cursor += count

            if i == 0:
                scene_start = 0.0
            else:
                scene_start = scene_boundaries[-1][1]

            if i == len(scenes) - 1:
                scene_end = total_duration
            else:
                # Find start of next scene's first word or extend past current scene's last word
                next_word_idx = word_cursor
                if next_word_idx < total_words_count:
                    scene_end = all_words[next_word_idx].start_sec
                elif scene_words:
                    scene_end = scene_words[-1].end_sec + 0.3
                else:
                    scene_end = scene_start + 5.0

            # Ensure minimum duration
            if scene_end <= scene_start:
                scene_end = scene_start + 4.0

            duration = scene_end - scene_start
            scene_boundaries.append((scene_start, scene_end, duration))

        return scene_boundaries

    def _fallback_concat(self, video_clips: List[str], output_path: str):
        """Standard lossless FFmpeg concat demuxer fallback."""
        video_concat_list = os.path.join(self.work_dir, "video_concat.txt")
        with open(video_concat_list, "w") as f:
            for v_file in video_clips:
                f.write(f"file '{os.path.abspath(v_file)}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", video_concat_list,
            "-c", "copy",
            output_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _resolve_scene_image(
        self,
        script: VideoScript,
        scene_index: int,
        dest_path: str,
        enable_ai_images: bool,
        custom_images_dir: Optional[str]
    ) -> Tuple[str, str]:
        """
        Resolve the source visual for a scene in priority order:
        custom folder -> workspace images/<niche>/ -> AI engine -> procedural.
        Returns (resolved_image_path, source_label).
        """
        candidates = []
        if custom_images_dir and os.path.exists(custom_images_dir):
            candidates.append(custom_images_dir)
        default_niche_dir = os.path.join("images", script.niche)
        if os.path.exists(default_niche_dir):
            candidates.append(default_niche_dir)

        for base in candidates:
            for ext in [".jpg", ".png", ".jpeg", ".webp"]:
                c1 = os.path.join(base, f"scene_{scene_index+1:02d}{ext}")
                c2 = os.path.join(base, f"scene_{scene_index+1}{ext}")
                if os.path.exists(c1):
                    shutil.copy(c1, dest_path)
                    return dest_path, f"custom:{c1}"
                if os.path.exists(c2):
                    shutil.copy(c2, dest_path)
                    return dest_path, f"custom:{c2}"

        if enable_ai_images:
            return dest_path, "ai"

        return self.visuals.generate_procedural_background(
            output_path=dest_path, topic=script.scenes[scene_index].text
        ), "procedural"

    def render(
        self,
        script: VideoScript,
        output_mp4_path: str,
        custom_bg_music: Optional[str] = None,
        custom_images_dir: Optional[str] = None,
        enable_ai_images: bool = True
    ) -> str:
        """
        Execute full end-to-end automated production pipeline.
        Returns path to final rendered MP4 video.
        """
        start_time = time.time()
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4_path)), exist_ok=True)

        n_scenes = len(script.scenes)
        print(f"\n🚀 [1/5] Synthesizing continuous neural voiceover ({self.voice}, language={self.language})...")
        full_text = " ".join(scene.text for scene in script.scenes)
        master_voice_path = os.path.join(self.work_dir, "master_voice.mp3")

        audio_res = self.tts.synthesize(
            text=full_text,
            output_path=master_voice_path,
            voice=self.voice,
            rate=self.speech_rate
        )

        all_words = audio_res.words
        total_duration = audio_res.duration_sec
        print(f"    ✓ Spoken duration: {total_duration:.2f}s | Extracted words: {len(all_words)}")

        # Calculate exact visual clip timings to match speech sentences
        scene_timings = self._map_words_to_scenes(script.scenes, all_words, total_duration)

        # Transition configuration
        trans_cfg = TRANSITIONS.get(self.transition, TRANSITIONS["flash"])
        trans_name = trans_cfg.get("xfade_name")
        trans_dur = trans_cfg.get("duration", 0.0)
        use_xfade = bool(trans_name and trans_dur > 0 and n_scenes > 1)

        print(
            f"\n🎨 [2/5] Producing visuals | style='{self.art_style}' | engine='{self.engine}' | "
            f"{self.width}x{self.height}@{self.fps}fps (quality={self.quality})..."
        )

        # Rotating motion patterns so camera is constantly dynamic and engaging
        motion_rotation = [
            "punch_zoom_in", "dramatic_zoom_out", "pan_left", "whip_zoom",
            "pan_right", "vertigo_shake", "rise_up", "orbit_sway",
            "shockwave_out", "pulse_heartbeat",
        ]

        # ---------------------------------------------------- resolve raw images
        raw_image_paths: List[str] = []
        ai_job_queue: List[Dict] = []
        for i, scene in enumerate(script.scenes):
            img_path = os.path.join(self.work_dir, f"image_scene_{i+1:02d}.jpg")
            resolved, source = self._resolve_scene_image(
                script, i, img_path, enable_ai_images, custom_images_dir
            )
            if source == "ai":
                print(f"    → Scene {i+1}: Queued AI visual ('{scene.visual_prompt[:40]}...')")
                ai_job_queue.append({"prompt": scene.visual_prompt, "output_path": img_path})
                raw_image_paths.append(img_path)
            elif source.startswith("custom:"):
                print(f"    → Scene {i+1}: Using high-res custom visual ({source.split(':', 1)[1]})")
                raw_image_paths.append(resolved)
            else:
                print(f"    → Scene {i+1}: Offline procedural canvas")
                raw_image_paths.append(resolved)

        # Parallel network-bound AI generation (4 concurrent Flux requests)
        if ai_job_queue:
            print(f"    → Generating {len(ai_job_queue)} AI visuals in parallel...")
            self.visuals.generate_ai_images_parallel(ai_job_queue, max_workers=4)

        # ------------------------------------------- style transform + Ken Burns
        scene_video_clips: List[str] = []
        for i, scene in enumerate(script.scenes):
            dur = scene_timings[i][2]
            # When xfade is used, non-final clips have extra duration to provide overlap
            clip_dur = dur + trans_dur if (use_xfade and i < n_scenes - 1) else dur
            motion = scene.motion or motion_rotation[i % len(motion_rotation)]

            src_image = raw_image_paths[i]
            if not os.path.exists(src_image):  # safety net: AI job failed
                src_image = self.visuals.generate_procedural_background(
                    output_path=src_image, topic=scene.text)

            # Stage 2 of styling: offline PIL pixel-op (pixel art, chalkboard, ...)
            style_cfg = ART_STYLES.get(self.art_style, ART_STYLES["hyperreal"])
            if style_cfg.get("pixel_op"):
                styled_path = os.path.join(self.work_dir, f"styled_scene_{i+1:02d}.jpg")
                src_image = self.visuals.apply_art_style(src_image, styled_path)

            clip_path = os.path.join(self.work_dir, f"clip_scene_{i+1:02d}.mp4")
            print(f"    → Scene {i+1}: Rendering motion ({clip_dur:.2f}s, {motion})...")
            self.visuals.render_ken_burns_clip(
                image_path=src_image,
                output_video_path=clip_path,
                duration=clip_dur,
                motion=motion,
                fps=self.fps,
                width=self.width,
                height=self.height,
            )
            scene_video_clips.append(clip_path)

        # Assemble video scenes with transition
        raw_video_path = os.path.join(self.work_dir, "raw_video.mp4")
        if use_xfade:
            print(f"    → Applying '{trans_cfg['name']}' ({trans_dur}s) across {n_scenes} scene cuts...")
            try:
                filters = []
                current_input = "0:v"
                current_offset = 0.0
                inputs = []
                for clip in scene_video_clips:
                    inputs.extend(["-i", clip])
                for i in range(1, len(scene_video_clips)):
                    current_offset += scene_timings[i - 1][2]
                    next_input = f"{i}:v"
                    out_label = f"v0{i}" if i < len(scene_video_clips) - 1 else "outv"
                    filters.append(
                        f"[{current_input}][{next_input}]xfade=transition={trans_name}:duration={trans_dur}:offset={current_offset:.3f}[{out_label}]"
                    )
                    current_input = out_label
                filter_complex = ";".join(filters)

                xfade_cmd = [
                    "ffmpeg", "-y",
                    *inputs,
                    "-filter_complex", filter_complex,
                    "-map", f"[{current_input}]",
                    "-c:v", "libx264",
                    "-preset", self.encoder_preset,
                    "-crf", str(self.crf),
                    "-pix_fmt", "yuv420p",
                    raw_video_path
                ]
                subprocess.run(xfade_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("    ✓ Scene transitions rendered with frame-accurate timing")
            except Exception as e:
                print(f"    [!] xfade failed ({e}). Falling back to clean direct cuts.")
                self._fallback_concat(scene_video_clips, raw_video_path)
        else:
            self._fallback_concat(scene_video_clips, raw_video_path)

        # Hollywood & Open-Source VFX Compositing Pass (Natron, Effekseer, OpenVDB, SVG.js, OpenToonz)
        if self.vfx_modes and "none" not in self.vfx_modes:
            print(f"\n✨ [2.5/5] Compositing VFX & Animation Suite ({', '.join(self.vfx_modes)})...")
            raw_video_path = self.vfx_mgr.apply_vfx_pipeline(
                base_video_path=raw_video_path,
                output_video_path=os.path.join(self.work_dir, "vfx_composite.mp4"),
                duration=total_duration,
                vfx_modes=self.vfx_modes
            )
            print("    ✓ VFX compositing, particle simulation & vector graphics applied")

        print(f"\n📝 [3/5] Generating synchronized bouncing subtitles ({self.subtitle_style}, lang={self.language})...")
        ass_path = os.path.join(self.work_dir, "master_subtitles.ass")
        self.subtitles.generate_ass_script(
            words=all_words,
            output_ass_path=ass_path
        )
        print(f"    ✓ Burned subtitles mapped to millisecond speech events")

        # Prepare audio: Clean studio voiceover or optional background music
        has_custom_music = bool(custom_bg_music and os.path.exists(custom_bg_music))
        has_preset_music = bool(
            self.bg_music_preset and self.bg_music_preset.lower() not in ["none", "off", "disable", "disabled", "false", ""]
        )
        has_music = has_custom_music or has_preset_music

        master_audio_path = os.path.join(self.work_dir, "master_audio.m4a")

        if has_music:
            print(f"\n🎵 [4/5] Audio mixing & sidechain ducking ({self.bg_music_preset or 'custom'})...")
            if has_custom_music:
                bg_music_path = custom_bg_music
            else:
                bg_music_path = os.path.join(self.work_dir, "procedural_music.wav")
                self.audio.generate_tension_drone(
                    output_path=bg_music_path,
                    duration_sec=total_duration + 3.0,
                    preset=self.bg_music_preset
                )

            # Generate transition whooshes at scene boundaries
            cut_times = [scene_timings[i][1] for i in range(len(scene_timings) - 1)]
            sfx_path = os.path.join(self.work_dir, "transition_whooshes.wav")
            transition_sfx = self.audio.generate_transition_track(
                output_path=sfx_path,
                total_duration=total_duration,
                transition_times=cut_times
            )

            # Mix with dynamic sidechain compression and -14 LUFS mastering
            self.audio.mix_with_ducking(
                voiceover_path=master_voice_path,
                background_music_path=bg_music_path,
                output_path=master_audio_path,
                transition_sfx_path=transition_sfx
            )
            print("    ✓ Mixed with background music and mastered to -14 LUFS")
        else:
            print("\n🎙️ [4/5] Mastering clean studio voiceover (Zero background sound)...")
            self.audio.master_clean_voice(
                voiceover_path=master_voice_path,
                output_path=master_audio_path
            )
            print("    ✓ Pristine studio voiceover mastered to -14 LUFS (100% clean, no background sound)")

        print(f"\n🎬 [5/5] Final assembly: Post-FX grade → subtitles → retention bar → {self.quality} encode...")
        # Video graph: PostFX premium grade FIRST, then crisp subtitles on top, then progress bar
        fx_body = PostFX.build(
            self.effects,
            input_label="0:v",
            output_label="fx",
            duration=total_duration,
            width=self.width,
            height=self.height,
        )

        burn_filters = [f"ass={ass_path}"]
        if self.progress_bar:
            bar_color = PROGRESS_BAR_CONFIG["colors_by_style"].get(
                self.subtitle_style,
                PROGRESS_BAR_CONFIG["default_color"]
            )
            bar_h = PROGRESS_BAR_CONFIG["height"]
            y_pos = self.height - bar_h - 4
            burn_filters.append(
                f"drawbox=x=0:y={y_pos}:w='iw*(t/{total_duration:.3f})':h={bar_h}:color={bar_color}:t=fill"
            )
        # Normalize to broadcast-standard limited range (TV) before encoding so
        # platforms never mis-read full-range (yuvj420p) luma.
        burn_filters.append("scale=out_range=tv")
        burn_filters.append("format=yuv420p")
        video_filters = ",".join(burn_filters)

        filter_complex = f"{fx_body};[fx]{video_filters}[vout]"

        final_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video_path,
            "-i", master_audio_path,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", self.encoder_preset,
            "-crf", str(self.crf),
            "-pix_fmt", "yuv420p",
            "-color_range", "tv",
            "-colorspace", "bt709",
            "-color_primaries", "bt709",
            "-color_trc", "bt709",
            "-c:a", "aac",
            "-b:a", self.audio_bitrate,
            "-ar", "48000",
            "-movflags", "+faststart",
            "-shortest",
            output_mp4_path
        ]

        subprocess.run(final_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elapsed = time.time() - start_time
        print(f"\n✨ Video successfully rendered in {elapsed:.1f}s!")
        print(f"📦 Output path: {output_mp4_path}")

        return output_mp4_path
