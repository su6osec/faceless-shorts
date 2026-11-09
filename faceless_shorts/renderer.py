"""
Master Video Rendering Engine for Faceless Shorts.
Features:
- Continuous Stream Voice Synthesis (Zero MP3 Concatenation Desync)
- Frame-Accurate Speech, Visual Cut & Subtitle Synchronization
- Punchy Ken Burns Dynamic Motion (Punch Zoom In, Zoom Out, Tracking Pans)
- Artistic Video Style Post-Processing (Sketch, Vintage 35mm, Papercraft, Cyberpunk)
- ASS Karaoke Subtitles with Dynamic 118% Word Bounce Popping
- Automated Dynamic Audio Ducking with FFmpeg Sidechain Compression
"""

import os
import shutil
import subprocess
import time
from typing import Dict, List, Optional, Tuple
from faceless_shorts.config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FPS, ART_STYLES
from faceless_shorts.script_generator import VideoScript
from faceless_shorts.tts_engine import TTSEngine, WordTimestamp
from faceless_shorts.visuals import VisualManager
from faceless_shorts.subtitles import SubtitleGenerator
from faceless_shorts.audio import SoundEngine

class VideoRenderer:
    def __init__(
        self,
        voice: str = "christopher",
        subtitle_style: str = "hormozi",
        art_style: str = "hyperreal",
        bg_music_preset: str = "dark_tension",
        speech_rate: str = "+5%",
        work_dir: str = ".temp_render"
    ):
        self.tts = TTSEngine(default_voice=voice)
        self.visuals = VisualManager(cache_dir=os.path.join(work_dir, "cache"), art_style=art_style)
        self.subtitles = SubtitleGenerator(style_name=subtitle_style)
        self.audio = SoundEngine()
        self.voice = voice
        self.subtitle_style = subtitle_style
        self.art_style = art_style
        self.bg_music_preset = bg_music_preset
        self.speech_rate = speech_rate
        self.work_dir = work_dir

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

        print(f"\n🚀 [1/5] Synthesizing continuous neural voiceover ({self.voice})...")
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

        print(f"\n🎨 [2/5] Producing visuals with style '{self.art_style}' & dynamic motion...")
        scene_video_clips = []
        
        # Rotating motion patterns so camera is constantly dynamic and engaging
        motion_rotation = ["punch_zoom_in", "dramatic_zoom_out", "pan_left", "pan_right", "punch_zoom_in"]

        for i, scene in enumerate(script.scenes):
            dur = scene_timings[i][2]
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

            print(f"    → Scene {i+1}: Rendering motion ({dur:.2f}s, {motion})...")
            self.visuals.render_ken_burns_clip(
                image_path=img_path,
                output_video_path=clip_path,
                duration=dur,
                motion=motion
            )
            scene_video_clips.append(clip_path)

        print(f"\n📝 [3/5] Generating synchronized bouncing subtitles ({self.subtitle_style})...")
        ass_path = os.path.join(self.work_dir, "master_subtitles.ass")
        self.subtitles.generate_ass_script(
            words=all_words,
            output_ass_path=ass_path
        )
        print(f"    ✓ Burned subtitles mapped to millisecond speech events")

        print(f"\n🎵 [4/5] Sound design & Sidechain audio ducking...")
        # Prepare background music (procedural or custom)
        if custom_bg_music and os.path.exists(custom_bg_music):
            bg_music_path = custom_bg_music
        else:
            bg_music_path = os.path.join(self.work_dir, "procedural_music.wav")
            self.audio.generate_tension_drone(
                output_path=bg_music_path,
                duration_sec=total_duration + 3.0,
                preset=self.bg_music_preset
            )

        # Mix with dynamic sidechain compression
        master_audio_path = os.path.join(self.work_dir, "master_audio.m4a")
        self.audio.mix_with_ducking(
            voiceover_path=master_voice_path,
            background_music_path=bg_music_path,
            output_path=master_audio_path
        )
        print("    ✓ Dynamic ducking complete")

        print(f"\n🎬 [5/5] Final FFmpeg assembly & Subtitle burning...")
        # Concatenate video clips
        video_concat_list = os.path.join(self.work_dir, "video_concat.txt")
        with open(video_concat_list, "w") as f:
            for v_file in scene_video_clips:
                f.write(f"file '{os.path.abspath(v_file)}'\n")

        raw_video_path = os.path.join(self.work_dir, "raw_video.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", video_concat_list,
            "-c", "copy",
            raw_video_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Final pass: Burn ASS subtitles and mux final mixed audio
        final_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video_path,
            "-i", master_audio_path,
            "-vf", f"ass={ass_path}",
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
