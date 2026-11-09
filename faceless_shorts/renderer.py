"""
Master Video Rendering Engine for Faceless Shorts.
Orchestrates TTS, Visual AI, Ken Burns motion synthesis, ASS subtitle burning,
and sidechain audio mixing into publication-ready 1080x1920 MP4 shorts.
"""

import os
import shutil
import subprocess
import time
from typing import Dict, List, Optional
from faceless_shorts.config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FPS
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
        bg_music_preset: str = "dark_tension",
        speech_rate: str = "+5%",
        work_dir: str = ".temp_render"
    ):
        self.tts = TTSEngine(default_voice=voice)
        self.visuals = VisualManager(cache_dir=os.path.join(work_dir, "cache"))
        self.subtitles = SubtitleGenerator(style_name=subtitle_style)
        self.audio = SoundEngine()
        self.voice = voice
        self.subtitle_style = subtitle_style
        self.bg_music_preset = bg_music_preset
        self.speech_rate = speech_rate
        self.work_dir = work_dir

    def render(
        self,
        script: VideoScript,
        output_mp4_path: str,
        custom_bg_music: Optional[str] = None,
        enable_ai_images: bool = True
    ) -> str:
        """
        Execute full end-to-end automated production pipeline.
        Returns path to final rendered MP4 video.
        """
        start_time = time.time()
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4_path)), exist_ok=True)
        
        print(f"\n🚀 [1/5] Synthesizing speech for {len(script.scenes)} scenes...")
        scene_audio_files = []
        all_words: List[WordTimestamp] = []
        scene_durations = []
        cumulative_offset = 0.0

        for i, scene in enumerate(script.scenes):
            scene_audio_path = os.path.join(self.work_dir, f"audio_scene_{i+1:02d}.mp3")
            audio_res = self.tts.synthesize(
                text=scene.text,
                output_path=scene_audio_path,
                voice=self.voice,
                rate=self.speech_rate
            )
            scene_audio_files.append(scene_audio_path)
            scene_durations.append(audio_res.duration_sec)

            # Accumulate word timestamps with scene offset
            for w in audio_res.words:
                all_words.append(WordTimestamp(
                    word=w.word,
                    start_sec=w.start_sec + cumulative_offset,
                    end_sec=w.end_sec + cumulative_offset,
                    duration_sec=w.duration_sec
                ))
            cumulative_offset += audio_res.duration_sec

        total_duration = cumulative_offset
        print(f"    ✓ Total video duration: {total_duration:.1f} seconds")

        print(f"\n🎨 [2/5] Generating visuals and Ken Burns motion...")
        scene_video_clips = []
        for i, scene in enumerate(script.scenes):
            dur = scene_durations[i]
            img_path = os.path.join(self.work_dir, f"image_scene_{i+1:02d}.jpg")
            clip_path = os.path.join(self.work_dir, f"clip_scene_{i+1:02d}.mp4")

            if enable_ai_images:
                print(f"    → Scene {i+1}: Generating AI visual ('{scene.visual_prompt[:45]}...')...")
                self.visuals.generate_ai_image(prompt=scene.visual_prompt, output_path=img_path)
            else:
                self.visuals.generate_procedural_background(output_path=img_path, topic=scene.text)

            print(f"    → Scene {i+1}: Rendering Ken Burns motion ({dur:.1f}s, {scene.motion})...")
            self.visuals.render_ken_burns_clip(
                image_path=img_path,
                output_video_path=clip_path,
                duration=dur,
                motion=scene.motion
            )
            scene_video_clips.append(clip_path)

        print(f"\n📝 [3/5] Generating karaoke ASS subtitles ({self.subtitle_style} style)...")
        ass_path = os.path.join(self.work_dir, "master_subtitles.ass")
        self.subtitles.generate_ass_script(
            words=all_words,
            output_ass_path=ass_path,
            enable_emojis=True
        )
        print(f"    ✓ Subtitles mapped: {len(all_words)} words")

        print(f"\n🎵 [4/5] Sound design & Sidechain audio ducking...")
        # 1. Concatenate speech audio
        speech_concat_list = os.path.join(self.work_dir, "speech_concat.txt")
        with open(speech_concat_list, "w") as f:
            for s_file in scene_audio_files:
                f.write(f"file '{os.path.abspath(s_file)}'\n")
        
        master_voice_path = os.path.join(self.work_dir, "master_voice.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", speech_concat_list,
            "-c", "copy",
            master_voice_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2. Prepare background music (custom or procedural)
        if custom_bg_music and os.path.exists(custom_bg_music):
            bg_music_path = custom_bg_music
        else:
            bg_music_path = os.path.join(self.work_dir, "procedural_music.wav")
            self.audio.generate_tension_drone(
                output_path=bg_music_path,
                duration_sec=total_duration + 3.0,
                preset=self.bg_music_preset
            )

        # 3. Mix with dynamic sidechain ducking
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

        # Final pass: Burn subtitles and merge final audio
        escaped_ass = os.path.abspath(ass_path).replace("\\", "/")
        if ":" in escaped_ass:
            # Handle Windows colon in path if needed
            escaped_ass = escaped_ass[0] + "\\:" + escaped_ass[2:]

        final_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video_path,
            "-i", master_audio_path,
            "-vf", f"ass={ass_path}",
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "20",
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
