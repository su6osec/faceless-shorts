"""
Offline tests for faceless_shorts.integrations (unittest, no pytest).

Every test here MUST pass with no network access: no model downloads, no
stock API calls, no LLM calls, no yt-dlp runs against real URLs.
"""

import contextlib
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from unittest import mock

from faceless_shorts import integrations
from faceless_shorts.integrations import (
    ComfyUIClient,
    LLMScriptWriter,
    StockBRoll,
    ToolRegistry,
    WhisperTranscriber,
    YtDlpHelper,
    doctor,
    doctor_report,
)

# The exact tool keys the registry must report.
EXPECTED_TOOLS = ("whisper", "comfyui", "ytdlp", "llm", "stock")
# Every doctor() entry must carry these keys.
INFO_KEYS = ("available", "version", "kind", "install", "hint")
# Env vars that could leak real credentials / endpoints into the tests.
LEAKY_ENV = (
    "PEXELS_API_KEY",
    "PIXABAY_API_KEY",
    "OLLAMA_HOST",
    "LLM_BASE_URL",
    "LLM_API_KEY",
    "LLM_MODEL",
    "FACELESS_COMFY_URL",
    "FACELESS_MODELS_DIR",
    "FACELESS_STOCK_DIR",
    "FACELESS_WHISPER_MODEL",
)


@contextlib.contextmanager
def clean_env():
    """Temporarily remove leaky env vars (restored automatically)."""
    with mock.patch.dict(os.environ, {}, clear=False):
        for key in LEAKY_ENV:
            os.environ.pop(key, None)
        yield


def ffmpeg_has_whisper_filter():
    """Independent check: does the local ffmpeg ship the `whisper` filter?"""
    exe = shutil.which("ffmpeg")
    if not exe:
        return False
    try:
        proc = subprocess.run(
            [exe, "-hide_banner", "-filters"],
            capture_output=True,
            text=True,
            timeout=3,
        )
    except Exception:
        return False
    blob = (proc.stdout or "") + (proc.stderr or "")
    for line in blob.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "whisper":
            return True
    return False


class ToolRegistryTests(unittest.TestCase):
    def test_doctor_shape_and_keys(self):
        with clean_env():
            started = time.monotonic()
            report = doctor()
            elapsed = time.monotonic() - started
        self.assertLess(elapsed, 6.0, "doctor() must stay fast")
        self.assertIsInstance(report, dict)
        self.assertEqual(set(report.keys()), set(EXPECTED_TOOLS))
        for key in EXPECTED_TOOLS:
            info = report[key]
            self.assertIsInstance(info, dict)
            for required in INFO_KEYS:
                self.assertIn(required, info, f"{key} missing {required}")
            self.assertIsInstance(info["available"], bool)
            self.assertTrue(info["version"] is None or isinstance(info["version"], str))
            self.assertIsInstance(info["kind"], str)
            self.assertTrue(info["kind"])
            self.assertIsInstance(info["install"], str)
            self.assertTrue(info["install"])
            self.assertIsInstance(info["hint"], str)
            self.assertTrue(info["hint"])

    def test_available_returns_bool_for_known_tools(self):
        for key in EXPECTED_TOOLS:
            with self.subTest(tool=key):
                self.assertIsInstance(ToolRegistry.available(key), bool)

    def test_available_unknown_tool_is_false_and_safe(self):
        self.assertIs(ToolRegistry.available("definitely_not_a_tool"), False)
        self.assertIs(ToolRegistry.available(""), False)
        self.assertIs(ToolRegistry.available(None), False)
        self.assertIs(ToolRegistry.available(123), False)


class WhisperTranscriberTests(unittest.TestCase):
    def test_available_is_bool_and_matches_ffmpeg_whisper_filter(self):
        expected = ffmpeg_has_whisper_filter()
        with clean_env():
            started = time.monotonic()
            result = WhisperTranscriber.available()
            elapsed = time.monotonic() - started
        self.assertLess(elapsed, 6.0)
        self.assertIsInstance(result, bool)
        self.assertEqual(result, expected)

    def test_transcribe_nonexistent_file_returns_none_without_raising(self):
        with clean_env():
            started = time.monotonic()
            result = WhisperTranscriber().transcribe("/nonexistent/faceless_clip.mp4")
            elapsed = time.monotonic() - started
        self.assertLess(elapsed, 6.0)
        self.assertIsNone(result)

    def test_transcribe_never_auto_downloads_the_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            models_dir = os.path.join(tmp, "models")
            os.makedirs(models_dir)
            media = os.path.join(tmp, "clip.mp4")
            with open(media, "wb") as handle:
                handle.write(b"not a real video")
            with clean_env():
                os.environ["FACELESS_MODELS_DIR"] = models_dir
                with mock.patch.object(WhisperTranscriber, "ensure_model") as ensure:
                    started = time.monotonic()
                    result = WhisperTranscriber().transcribe(media)
                    elapsed = time.monotonic() - started
            # ensure_model must NEVER be invoked automatically...
            ensure.assert_not_called()
            # ...so with no cached model the result is None and nothing was written.
            self.assertIsNone(result)
            self.assertEqual(os.listdir(models_dir), [])
            self.assertLess(elapsed, 6.0)

    def test_ensure_model_returns_cached_path_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            cached = os.path.join(tmp, "ggml-base.en.bin")
            with open(cached, "wb") as handle:
                handle.write(b"fake-model-bytes")
            with clean_env():
                os.environ["FACELESS_MODELS_DIR"] = tmp
                with mock.patch.object(integrations, "_download") as download:
                    result = WhisperTranscriber.ensure_model("en")
            self.assertEqual(result, cached)
            download.assert_not_called()
            self.assertFalse(os.path.exists(cached + ".part"))


class ComfyUIClientTests(unittest.TestCase):
    def test_available_false_fast_when_nothing_listens(self):
        with clean_env():
            client = ComfyUIClient()
            started = time.monotonic()
            result = client.available()
            elapsed = time.monotonic() - started
        self.assertIs(result, False)
        self.assertLess(elapsed, 3.0, "availability probe must be fast")

    def test_generate_on_unavailable_client_returns_none_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "render.png")
            with clean_env():
                client = ComfyUIClient()
                started = time.monotonic()
                result = client.generate("a serene mountain lake at dawn", target)
                elapsed = time.monotonic() - started
            self.assertIsNone(result)
            self.assertFalse(os.path.exists(target))
            self.assertLess(elapsed, 6.0)


class YtDlpHelperTests(unittest.TestCase):
    def test_available_returns_bool_quickly(self):
        with clean_env():
            started = time.monotonic()
            result = YtDlpHelper.available()
            elapsed = time.monotonic() - started
        self.assertIsInstance(result, bool)
        self.assertLess(elapsed, 6.0)

    def test_download_returns_none_when_unavailable(self):
        if YtDlpHelper.available():
            self.skipTest("yt-dlp is installed here; download() would hit the network")
        with tempfile.TemporaryDirectory() as tmp:
            with clean_env():
                started = time.monotonic()
                result = YtDlpHelper.download(
                    "https://example.com/reference.mp4", out_dir=tmp
                )
                elapsed = time.monotonic() - started
            self.assertIsNone(result)
            self.assertEqual(os.listdir(tmp), [])
            self.assertLess(elapsed, 6.0)


class LLMScriptWriterTests(unittest.TestCase):
    def test_available_returns_bool_quickly(self):
        with clean_env():
            started = time.monotonic()
            result = LLMScriptWriter.available()
            elapsed = time.monotonic() - started
        self.assertIsInstance(result, bool)
        self.assertLess(elapsed, 6.0)

    def test_write_script_returns_none_offline(self):
        with clean_env():
            # Point Ollama at a dead local port and remove every LLM env var
            # so no backend can possibly be reached.
            os.environ["OLLAMA_HOST"] = "http://127.0.0.1:9"
            writer = LLMScriptWriter()
            started = time.monotonic()
            self.assertFalse(writer.available())
            result = writer.write_script("stoic discipline", language="en")
            elapsed = time.monotonic() - started
        self.assertIsNone(result)
        self.assertLess(elapsed, 6.0)


class StockBRollTests(unittest.TestCase):
    def test_unavailable_without_keys_and_search_returns_none(self):
        with clean_env():
            self.assertFalse(StockBRoll.available())
            started = time.monotonic()
            result = StockBRoll.search_clip("ocean waves", orientation="portrait")
            elapsed = time.monotonic() - started
        self.assertIsNone(result)
        self.assertLess(elapsed, 6.0)


class DoctorReportTests(unittest.TestCase):
    def test_doctor_report_contains_every_tool_key(self):
        with clean_env():
            started = time.monotonic()
            text = doctor_report()
            elapsed = time.monotonic() - started
        self.assertLess(elapsed, 6.0)
        self.assertIsInstance(text, str)
        self.assertTrue(text.strip())
        for key in EXPECTED_TOOLS:
            self.assertIn(key, text)

    def test_all_exports(self):
        expected = {
            "ToolRegistry",
            "WhisperTranscriber",
            "ComfyUIClient",
            "YtDlpHelper",
            "LLMScriptWriter",
            "StockBRoll",
            "doctor",
            "doctor_report",
        }
        self.assertEqual(set(integrations.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(integrations, name), f"missing export {name}")


if __name__ == "__main__":
    unittest.main()
