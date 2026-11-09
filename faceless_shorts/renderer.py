"""
Master Video Rendering Engine for Faceless Shorts.
Features:
- Continuous Stream Voice Synthesis (Zero MP3 Concatenation Desync)
- Frame-Accurate Speech, Visual Cut & Subtitle Synchronization
- High-Retention Scene Transitions (White Flash Cut, Crossfade, Slide, Wipe, Cut)
- Dynamic Retention Progress Bar (Glowing animated bottom bar for maximum completion rate)
- Punchy Ken Burns Dynamic Motion (Punch Zoom In, Zoom Out, Tracking Pans, Whip Zoom)
- Artistic Video Style Post-Processing (Sketch, Vintage 35mm, Papercraft, Cyberpunk)
- ASS Karaoke Subtitles with Dynamic 118% Word Bounce Popping
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
    DEFAULT_LANGUAGE
)
from faceless_shorts.script_generator import VideoScript
from faceless_shorts.tts_engine import TTSEngine, WordTimestamp
from faceless_shorts.visuals import VisualManager
from faceless_shorts.subtitles import SubtitleGenerator
from faceless_shorts.audio import SoundEngine
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
        work_dir: str = ".temp_render"
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
        self.art_style = art_style
        self.bg_music_preset = bg_music_preset
        self.speech_rate = speech_rate
        self.work_dir = work_dir

        # Parse VFX modes
        if isinstance(vfx, str):
            self.vfx_modes = [m.strip().lower() for m in vfx.split(",") if m.strip()]
        elif isinstance(vfx, list):
            self.vfx_modes = [m.lower() for m in vfx]
        else:
            self.vfx_modes = []

        self.tts = TTSEngine(default_voice=self.voice)
        self.visuals = VisualManager(cache_dir=os.path.join(work_dir, "cache"), art_style=art_style)
        self.subtitles = SubtitleGenerator(style_name=subtitle_style, language=self.language)
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
        use_xfade = bool(trans_name and trans_dur > 0 and len(script.scenes) > 1)

        print(f"\n🎨 [2/5] Producing visuals with style '{self.art_style}' & dynamic motion...")
        scene_video_clips = []
        
        # Rotating motion patterns so camera is constantly dynamic and engaging
        motion_rotation = ["punch_zoom_in", "dramatic_zoom_out", "pan_left", "whip_zoom", "pan_right", "vertigo_shake"]

        for i, scene in enumerate(script.scenes):
            dur = scene_timings[i][2]
            # When xfade is used, non-final clips have extra duration to provide overlap
            clip_dur = dur + trans_dur if (use_xfade and i < len(script.scenes) - 1) else dur
            motion = scene.motion or motion_rotation[i % len(motion_rotation)]
            
            img_path = os.path.join(self.work_dir, f"image_scene_{i+1:02d}.jpg")
            clip_path = os.path.join(self.work_dir, f"clip_scene_{i+1:02d}.mp4")

            # Check if custom image exists (e.g. from Nano Banana or user folder)
            custom_candidate = None
            if custom_images_dir and os.path.exists(custom_images_dir):
                for ext in [".jpg", ".png", ".jpeg", ".webp"]:
                    c1 = os.path.join(custom_images_dir, f"scene_{i+1:02d}{ext}")
                    c2 = os.path.join(custom_images_dir, f"scene_{i+1}{ext}")
                    if os.path.exists(c1):
                        custom_candidate = c1
                        break
                    elif os.path.exists(c2):
                        custom_candidate = c2
                        break

            # Also check default workspace images/<niche>/
            if not custom_candidate:
                default_niche_dir = os.path.join("images", script.niche)
                if os.path.exists(default_niche_dir):
                    for ext in [".jpg", ".png", ".jpeg", ".webp"]:
                        c1 = os.path.join(default_niche_dir, f"scene_{i+1:02d}{ext}")
                        c2 = os.path.join(default_niche_dir, f"scene_{i+1}{ext}")
                        if os.path.exists(c1):
                            custom_candidate = c1
                            break
                        elif os.path.exists(c2):
                            custom_candidate = c2
                            break

            if custom_candidate:
                print(f"    → Scene {i+1}: Using high-res custom visual from {custom_candidate}...")
                shutil.copy(custom_candidate, img_path)
            elif enable_ai_images:
                print(f"    → Scene {i+1}: Generating visual ('{scene.visual_prompt[:40]}...')...")
                self.visuals.generate_ai_image(prompt=scene.visual_prompt, output_path=img_path)
            else:
                self.visuals.generate_procedural_background(output_path=img_path, topic=scene.text)

            print(f"    → Scene {i+1}: Rendering motion ({clip_dur:.2f}s, {motion})...")
            self.visuals.render_ken_burns_clip(
                image_path=img_path,
                output_video_path=clip_path,
                duration=clip_dur,
                motion=motion
            )
            scene_video_clips.append(clip_path)

        # Assemble video scenes with transition
        raw_video_path = os.path.join(self.work_dir, "raw_video.mp4")
        if use_xfade:
            print(f"    → Applying '{trans_cfg['name']}' ({trans_dur}s) across {len(scene_video_clips)} scene cuts...")
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
                    "-preset", "faster",
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

        print(f"\n🎬 [5/5] Final FFmpeg assembly, Retention progress bar & Subtitle burning...")
        # Build video filter chain: ASS subtitles + Retention Progress Bar
        video_filters = [f"ass={ass_path}"]
        if self.progress_bar:
            bar_color = PROGRESS_BAR_CONFIG["colors_by_style"].get(
                self.subtitle_style,
                PROGRESS_BAR_CONFIG["default_color"]
            )
            y_pos = PROGRESS_BAR_CONFIG["y"]
            h_val = PROGRESS_BAR_CONFIG["height"]
            bar_filter = f"drawbox=x=0:y={y_pos}:w='iw*(t/{total_duration:.3f})':h={h_val}:color={bar_color}:t=fill"
            video_filters.append(bar_filter)

        final_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video_path,
            "-i", master_audio_path,
            "-vf", ",".join(video_filters),
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "19",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_mp4_path
        ]

        subprocess.run(final_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elapsed = time.time() - start_time
        print(f"\n✨ Video successfully rendered in {elapsed:.1f}s!")
        print(f"📦 Output path: {output_mp4_path}")

        return output_mp4_path
