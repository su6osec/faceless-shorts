"""
Optional adapters for the best free / open-source tools on GitHub.

Every integration in this module is OPTIONAL. Detection is FAST (subprocess
probes are capped at 3s, HTTP probes at 1.0s), nothing is ever downloaded
unless you explicitly ask for it, and every failure degrades to ``None`` /
``False`` instead of raising, so the core pipeline never crashes when a tool
is missing.

Projects credited (all free / open source):

- whisper.cpp — local speech-to-text, used through FFmpeg's built-in
  ``whisper`` filter (no pip install needed)
  https://github.com/ggerganov/whisper.cpp
- ComfyUI — local Stable Diffusion txt2img node UI
  https://github.com/comfyanonymous/ComfyUI
- yt-dlp — feature-rich media downloader (B-roll / reference footage)
  https://github.com/yt-dlp/yt-dlp
- Ollama — local LLM runtime for script writing
  https://github.com/ollama/ollama
- Pexels API — free stock video clips
  https://www.pexels.com/api/
- Pixabay API — free stock video clips (fallback)
  https://pixabay.com/api/docs/

Author: su6osec (https://github.com/su6osec)
"""

from __future__ import annotations

import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple
from urllib import error as urlerror
from urllib.parse import urlencode
from urllib import request as urlrequest

__all__ = [
    "ToolRegistry",
    "WhisperTranscriber",
    "ComfyUIClient",
    "YtDlpHelper",
    "LLMScriptWriter",
    "StockBRoll",
    "doctor",
    "doctor_report",
]

# --------------------------------------------------------------------------- #
# Tunables: detection must be FAST, transfers may be slow, nothing crashes.
# --------------------------------------------------------------------------- #
SUBPROCESS_TIMEOUT = 3.0        # hard cap for any `ffmpeg` / `yt-dlp` probe
HTTP_TIMEOUT = 1.0              # hard cap for availability probes
HTTP_INFO_TIMEOUT = 5.0         # ComfyUI /object_info (local, can be large)
HTTP_SEARCH_TIMEOUT = 10.0      # stock API searches
HTTP_SUBMIT_TIMEOUT = 10.0      # ComfyUI POST /prompt
HTTP_POLL_TIMEOUT = 2.0         # ComfyUI /history polling
HTTP_IO_TIMEOUT = 30.0          # streaming downloads (urllib socket timeout)
COMFY_POLL_INTERVAL = 0.5       # seconds between /history polls
COMFY_POLL_TIMEOUT = 120.0      # total seconds to wait for a ComfyUI render
YTDLP_TIMEOUT = 300.0           # cap for a single yt-dlp download
TRANSCRIBE_TIMEOUT = 600.0      # cap for an ffmpeg whisper transcription

DEFAULT_COMFY_URL = "http://127.0.0.1:8188"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_CHECKPOINT = "v1-5-pruned-emaonly.safetensors"
DEFAULT_NEGATIVE_PROMPT = "lowres, blurry, watermark, text"
HF_WHISPER_BASE = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main"
DEFAULT_LLM_MODEL = "gpt-4o-mini"

# Tool keys reported by doctor() / doctor_report().
TOOL_KEYS: Tuple[str, ...] = ("whisper", "comfyui", "ytdlp", "llm", "stock")

# rich is an optional dependency; plain aligned text is the fallback.
try:  # pragma: no cover - exercised implicitly when rich is installed
    from rich.console import Console as _RichConsole
    from rich.table import Table as _RichTable
except Exception:  # pragma: no cover
    _RichConsole = None
    _RichTable = None


# --------------------------------------------------------------------------- #
# Tiny helpers (never raise, never hang)
# --------------------------------------------------------------------------- #
def _env(name: str, default: str = "") -> str:
    """Read an env var, treating missing/blank as unset."""
    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip()
    return value or default


def _http_request(
    url: str,
    data: Any = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = HTTP_TIMEOUT,
) -> Optional[Tuple[int, bytes]]:
    """Perform a GET/POST and return ``(status, body_bytes)`` or ``None``.

    Never raises: network errors, DNS failures and timeouts all return None,
    HTTP error statuses are returned as-is so callers can inspect them.
    """
    try:
        payload = None
        if data is not None:
            payload = data if isinstance(data, bytes) else json.dumps(data).encode("utf-8")
        request = urlrequest.Request(url, data=payload)
        for key, value in (headers or {}).items():
            request.add_header(key, value)
        if payload is not None and not any(k.lower() == "content-type" for k in (headers or {})):
            request.add_header("Content-Type", "application/json")
        with urlrequest.urlopen(request, timeout=timeout) as response:
            return int(response.getcode() or 200), response.read()
    except urlerror.HTTPError as exc:  # HTTPError is a subclass of URLError
        try:
            body = exc.read()
        except Exception:
            body = b""
        return int(exc.code), body
    except Exception:
        return None


def _http_json(
    url: str,
    data: Any = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = HTTP_TIMEOUT,
) -> Any:
    """GET/POST and parse the body as JSON. Returns parsed JSON or ``None``."""
    result = _http_request(url, data=data, headers=headers, timeout=timeout)
    if result is None:
        return None
    status, body = result
    if status != 200 or not body:
        return None
    try:
        return json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return None


def _http_ok(url: str, timeout: float = HTTP_TIMEOUT, headers: Optional[Dict[str, str]] = None) -> bool:
    """True when *url* answers with a 2xx status within *timeout* seconds."""
    result = _http_request(url, headers=headers, timeout=timeout)
    return bool(result and 200 <= result[0] < 300)


def _download(url: str, dest_path: str, timeout: float = HTTP_IO_TIMEOUT,
              headers: Optional[Dict[str, str]] = None) -> Optional[str]:
    """Stream *url* to *dest_path* atomically (``.part`` then rename).

    Returns the destination path on success, ``None`` on any failure.
    """
    part_path = dest_path + ".part"
    try:
        os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
        request = urlrequest.Request(url, headers=headers or {})
        with urlrequest.urlopen(request, timeout=timeout) as response:
            with open(part_path, "wb") as handle:
                while True:
                    chunk = response.read(1 << 16)
                    if not chunk:
                        break
                    handle.write(chunk)
        os.replace(part_path, dest_path)
        return dest_path
    except Exception:
        try:
            os.unlink(part_path)
        except OSError:
            pass
        return None


def _ffmpeg_path() -> Optional[str]:
    return shutil.which("ffmpeg")


def _ffmpeg_version() -> Optional[str]:
    exe = _ffmpeg_path()
    if not exe:
        return None
    try:
        proc = subprocess.run(
            [exe, "-version"],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    first = (proc.stdout or "").splitlines()
    first = first[0] if first else ""
    match = re.search(r"ffmpeg version (\S+)", first)
    if match:
        return match.group(1)
    return first.replace("ffmpeg version", "").strip() or None


def _ffmpeg_has_whisper_filter() -> bool:
    """True when the local ffmpeg build ships the ``whisper`` filter."""
    exe = _ffmpeg_path()
    if not exe:
        return False
    try:
        proc = subprocess.run(
            [exe, "-hide_banner", "-filters"],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
    except Exception:
        return False
    blob = (proc.stdout or "") + (proc.stderr or "")
    for line in blob.splitlines():
        parts = line.split()
        # Filter listing lines look like:  ".. whisper    A->A   description"
        if len(parts) >= 2 and parts[1] == "whisper":
            return True
    return False


def model_cache_dir() -> str:
    """Where whisper.cpp ggml models live (override: FACELESS_MODELS_DIR)."""
    custom = _env("FACELESS_MODELS_DIR")
    if custom:
        return custom
    return os.path.join(os.path.expanduser("~"), ".cache", "faceless-shorts", "models")


def _extract_json(text: Any) -> Optional[Dict[str, Any]]:
    """Pull the first JSON object out of possibly fenced / prose-wrapped text."""
    if not isinstance(text, str) or not text.strip():
        return None
    stripped = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", stripped, re.S)
    candidates = []
    if fence:
        candidates.append(fence.group(1).strip())
    candidates.append(stripped)
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
    # Fall back to the first balanced {...} block in the raw text.
    start = stripped.find("{")
    while start != -1:
        depth = 0
        end = None
        for index in range(start, len(stripped)):
            char = stripped[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index
                    break
        if end is not None:
            try:
                parsed = json.loads(stripped[start:end + 1])
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
        start = stripped.find("{", start + 1)
    return None


# --------------------------------------------------------------------------- #
# Tool registry / doctor
# --------------------------------------------------------------------------- #
class ToolRegistry:
    """Fast availability probing for every optional tool."""

    @staticmethod
    def doctor() -> Dict[str, Dict[str, Any]]:
        """Return ``{tool_key: {available, version, kind, install, hint}}``."""
        report: Dict[str, Dict[str, Any]] = {}

        # --- whisper: local STT via FFmpeg's whisper.cpp filter -------------
        report["whisper"] = {
            "available": bool(WhisperTranscriber.available()),
            "version": _ffmpeg_version(),
            "kind": "local STT (ffmpeg whisper filter)",
            "install": "brew install ffmpeg (built with libwhisper)",
            "hint": "https://github.com/ggerganov/whisper.cpp - models via ensure_model()",
        }

        # --- comfyui: local txt2img ----------------------------------------
        comfy = ComfyUIClient()
        comfy_ok = comfy.available()
        comfy_version = None
        if comfy_ok:
            stats = _http_json(f"{comfy.base_url}/system_stats", timeout=HTTP_TIMEOUT)
            if isinstance(stats, dict):
                comfy_version = str(((stats.get("system") or {}).get("comfyui_version")) or "") or None
        report["comfyui"] = {
            "available": bool(comfy_ok),
            "version": comfy_version,
            "kind": "local text-to-image",
            "install": "git clone https://github.com/comfyanonymous/ComfyUI",
            "hint": "run it on :8188 or set FACELESS_COMFY_URL",
        }

        # --- yt-dlp: media downloader ---------------------------------------
        ytdlp_version = YtDlpHelper.version()
        report["ytdlp"] = {
            "available": bool(YtDlpHelper.available()),
            "version": ytdlp_version,
            "kind": "B-roll media downloader",
            "install": "python -m pip install -U yt-dlp",
            "hint": "https://github.com/yt-dlp/yt-dlp",
        }

        # --- llm: Ollama or any OpenAI-compatible endpoint -------------------
        llm_backend = LLMScriptWriter._backend()
        llm_version = None
        if llm_backend is not None:
            if llm_backend[0] == "ollama":
                info = _http_json(f"{llm_backend[1]}/api/version", timeout=HTTP_TIMEOUT)
                if isinstance(info, dict) and info.get("version"):
                    llm_version = str(info["version"])
            else:
                llm_version = "openai-compatible"
        report["llm"] = {
            "available": llm_backend is not None,
            "version": llm_version,
            "kind": "free script-writing LLM",
            "install": "https://github.com/ollama/ollama -> ollama serve",
            "hint": "OLLAMA_HOST, or LLM_BASE_URL + LLM_API_KEY",
        }

        # --- stock: free-tier stock footage ---------------------------------
        pexels = bool(_env("PEXELS_API_KEY"))
        pixabay = bool(_env("PIXABAY_API_KEY"))
        providers = "+".join(
            name for name, present in (("pexels", pexels), ("pixabay", pixabay)) if present
        )
        report["stock"] = {
            "available": bool(pexels or pixabay),
            "version": providers or None,
            "kind": "free stock B-roll",
            "install": "free keys: pexels.com/api + pixabay.com/api/docs",
            "hint": "export PEXELS_API_KEY=... or PIXABAY_API_KEY=...",
        }

        return report

    @staticmethod
    def available(tool: str) -> bool:
        """Return whether *tool* (a doctor() key) is usable. Unknown -> False."""
        if not isinstance(tool, str):
            return False
        handlers = {
            "whisper": WhisperTranscriber.available,
            "comfyui": ComfyUIClient().available,
            "ytdlp": YtDlpHelper.available,
            "llm": LLMScriptWriter.available,
            "stock": StockBRoll.available,
        }
        handler = handlers.get(tool)
        if handler is None:
            return False
        try:
            return bool(handler())
        except Exception:
            return False


def doctor() -> Dict[str, Dict[str, Any]]:
    """Module-level convenience wrapper around ``ToolRegistry.doctor()``."""
    return ToolRegistry.doctor()


# --------------------------------------------------------------------------- #
# whisper.cpp via FFmpeg's built-in `whisper` filter (no pip install needed)
# --------------------------------------------------------------------------- #
class WhisperTranscriber:
    """Local speech-to-text through ``ffmpeg -af whisper=...``."""

    SIZES: Tuple[str, ...] = ("tiny", "base", "small")

    @staticmethod
    def available() -> bool:
        """True when ffmpeg is present AND ships the ``whisper`` filter."""
        return _ffmpeg_has_whisper_filter()

    @staticmethod
    def _model_filename(size: str, language: Optional[str]) -> str:
        lang = (language or "").strip().lower()
        if lang == "en" or lang.startswith("en-"):
            return f"ggml-{size}.en.bin"
        return f"ggml-{size}.bin"

    @classmethod
    def _model_url(cls, size: str, language: Optional[str]) -> str:
        return f"{HF_WHISPER_BASE}/{cls._model_filename(size, language)}"

    @classmethod
    def ensure_model(cls, language: str = "en") -> Optional[str]:
        """Explicitly download the ggml model (huggingface, free).

        Called ONLY on demand - never automatically by ``transcribe()``.
        Streams to ``<cache>/*.part`` then renames atomically. Returns the
        absolute model path, or ``None`` on any failure.
        """
        size = _env("FACELESS_WHISPER_MODEL", "base")
        directory = model_cache_dir()
        destination = os.path.join(directory, cls._model_filename(size, language))
        if os.path.isfile(destination) and os.path.getsize(destination) > 0:
            return destination  # already cached: no network access
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception:
            return None
        return _download(cls._model_url(size, language), destination, timeout=HTTP_IO_TIMEOUT)

    @classmethod
    def _find_model(cls, model_size: str, language: Optional[str]) -> Optional[str]:
        """Locate a cached model for (size, language) without downloading."""
        directory = model_cache_dir()
        names: List[str] = []
        if language:
            names.append(cls._model_filename(model_size, language))
        plain = f"ggml-{model_size}.bin"
        english = f"ggml-{model_size}.en.bin"
        for name in (plain, english):
            if name not in names:
                names.append(name)
        for name in names:
            path = os.path.join(directory, name)
            if os.path.isfile(path) and os.path.getsize(path) > 0:
                return path
        return None

    @classmethod
    def transcribe(
        cls,
        media_path: Any,
        language: Optional[str] = None,
        out_format: str = "json",
        model_size: str = "base",
    ) -> Optional[Any]:
        """Run the ffmpeg ``whisper`` filter on *media_path*.

        Returns the parsed JSON dict (``out_format="json"``), a list of lines
        (text/srt), or ``None`` on any failure. NEVER downloads a model: when
        the model file is absent it simply returns ``None``.
        """
        try:
            if not media_path or not os.path.isfile(str(media_path)):
                return None
            if out_format not in ("json", "text", "srt"):
                return None  # unsupported by the whisper filter
            model_path = cls._find_model(model_size, language)
            if not model_path:
                return None  # no model cached -> do NOT auto-download
            exe = _ffmpeg_path()
            if not exe or not cls.available():
                return None
            destination = os.path.join(
                tempfile.gettempdir(), f"faceless_whisper_{uuid.uuid4().hex}.json"
            )
            filter_expr = (
                f"whisper=model={model_path}:format={out_format}:destination={destination}"
            )
            if language:
                filter_expr += f":language={language}"
            cmd = [
                exe,
                "-hide_banner",
                "-loglevel", "error",
                "-i", str(media_path),
                "-map", "0:a",
                "-af", filter_expr,
                "-f", "null", "-",
            ]
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=TRANSCRIBE_TIMEOUT,
                )
                if proc.returncode != 0:
                    return None
                if not os.path.isfile(destination):
                    return None
                try:
                    with open(destination, encoding="utf-8") as handle:
                        payload = handle.read()
                finally:
                    try:
                        os.unlink(destination)
                    except OSError:
                        pass
                if not payload.strip():
                    return None
                if out_format == "json":
                    parsed = json.loads(payload)
                    return parsed if isinstance(parsed, (dict, list)) else None
                return [line for line in payload.splitlines() if line.strip()]
            finally:
                if os.path.exists(destination):
                    try:
                        os.unlink(destination)
                    except OSError:
                        pass
        except Exception:
            return None


# --------------------------------------------------------------------------- #
# ComfyUI (local Stable Diffusion txt2img)
# --------------------------------------------------------------------------- #
class ComfyUIClient:
    """Minimal client for a stock local ComfyUI install."""

    def __init__(self, base_url: Optional[str] = None) -> None:
        self._base_url = (base_url or "").strip().rstrip("/") or None

    @property
    def base_url(self) -> str:
        """ComfyUI root: explicit arg > FACELESS_COMFY_URL > 127.0.0.1:8188."""
        if self._base_url:
            return self._base_url
        return _env("FACELESS_COMFY_URL").rstrip("/") or DEFAULT_COMFY_URL

    @staticmethod
    def available() -> bool:
        """True when a ComfyUI server answers on its /system_stats endpoint."""
        return _http_ok(f"{ComfyUIClient().base_url}/system_stats", timeout=HTTP_TIMEOUT)

    def _pick_checkpoint(self) -> Optional[str]:
        """Ask the server which checkpoints exist; prefer the v1.5 default."""
        names: List[str] = []
        for path in ("/object_info", "/object_info/CheckpointLoaderSimple"):
            info = _http_json(f"{self.base_url}{path}", timeout=HTTP_INFO_TIMEOUT)
            if not isinstance(info, dict):
                continue
            try:
                if path == "/object_info":
                    spec = info["CheckpointLoaderSimple"]
                else:
                    spec = info
                names = [str(name) for name in spec["input"]["required"]["checkpoint"][0]]
            except Exception:
                names = []
            if names:
                break
        if not names:
            return DEFAULT_CHECKPOINT
        if DEFAULT_CHECKPOINT in names:
            return DEFAULT_CHECKPOINT
        return names[0]

    @staticmethod
    def _first_image(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        outputs = entry.get("outputs") or {}
        for node_output in outputs.values():
            if not isinstance(node_output, dict):
                continue
            for image in node_output.get("images") or []:
                if isinstance(image, dict) and image.get("filename"):
                    return image
        return None

    def _wait_for_history(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        deadline = time.monotonic() + COMFY_POLL_TIMEOUT
        while time.monotonic() < deadline:
            history = _http_json(
                f"{self.base_url}/history/{prompt_id}", timeout=HTTP_POLL_TIMEOUT
            )
            if isinstance(history, dict) and history:
                entry = history.get(prompt_id)
                if not isinstance(entry, dict):
                    entry = next(iter(history.values()), None)
                if isinstance(entry, dict):
                    status = entry.get("status") or {}
                    if status.get("status_str") == "error":
                        return None
                    return entry
            time.sleep(COMFY_POLL_INTERVAL)
        return None

    def generate(
        self,
        prompt: str,
        output_path: str,
        width: int = 1080,
        height: int = 1920,
        seed: Optional[int] = None,
        negative: str = DEFAULT_NEGATIVE_PROMPT,
        steps: int = 20,
        cfg: float = 6.5,
    ) -> Optional[str]:
        """Run a stock txt2img workflow and save the PNG to *output_path*.

        Returns ``output_path`` on success, ``None`` on any error (including
        an unreachable server). All HTTP goes through urllib with timeouts.
        """
        try:
            if not prompt or not output_path:
                return None
            if not self.available():
                return None
            checkpoint = self._pick_checkpoint()
            if not checkpoint:
                return None
            if seed is None:
                seed = random.randrange(0, 2 ** 32)
            workflow: Dict[str, Any] = {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": checkpoint},
                },
                "2": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": str(prompt), "clip": ["1", 1]},
                },
                "3": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": str(negative or ""), "clip": ["1", 1]},
                },
                "4": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {
                        "width": int(width),
                        "height": int(height),
                        "batch_size": 1,
                    },
                },
                "5": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": int(seed),
                        "steps": int(steps),
                        "cfg": float(cfg),
                        "sampler_name": "euler",
                        "scheduler": "karras",
                        "denoise": 1.0,
                        "model": ["1", 0],
                        "positive": ["2", 0],
                        "negative": ["3", 0],
                        "latent_image": ["4", 0],
                    },
                },
                "6": {
                    "class_type": "VAEDecode",
                    "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
                },
                "7": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "images": ["6", 0],
                        "filename_prefix": "faceless_shorts",
                    },
                },
            }
            response = _http_json(
                f"{self.base_url}/prompt",
                data={"prompt": workflow},
                timeout=HTTP_SUBMIT_TIMEOUT,
            )
            if not isinstance(response, dict):
                return None
            prompt_id = response.get("prompt_id")
            if not prompt_id or response.get("error"):
                return None
            entry = self._wait_for_history(str(prompt_id))
            if not entry:
                return None
            image = self._first_image(entry)
            if not image:
                return None
            query = urlencode(
                {
                    "filename": image.get("filename", ""),
                    "subfolder": image.get("subfolder", ""),
                    "type": image.get("type", ""),
                }
            )
            return _download(
                f"{self.base_url}/view?{query}",
                str(output_path),
                timeout=HTTP_IO_TIMEOUT,
            )
        except Exception:
            return None


# --------------------------------------------------------------------------- #
# yt-dlp (B-roll / reference media sourcing)
# --------------------------------------------------------------------------- #
class YtDlpHelper:
    """Thin wrapper around the yt-dlp CLI (or ``python -m yt_dlp``)."""

    @staticmethod
    def _cmd() -> Optional[List[str]]:
        exe = shutil.which("yt-dlp")
        if exe:
            return [exe]
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "yt_dlp", "--version"],
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
        except Exception:
            return None
        if proc.returncode == 0:
            return [sys.executable, "-m", "yt_dlp"]
        return None

    @classmethod
    def available(cls) -> bool:
        """True when a working yt-dlp is on PATH or importable."""
        return cls._cmd() is not None

    @classmethod
    def version(cls) -> Optional[str]:
        cmd = cls._cmd()
        if not cmd:
            return None
        try:
            proc = subprocess.run(
                cmd + ["--version"],
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
        except Exception:
            return None
        if proc.returncode != 0:
            return None
        return (proc.stdout or "").strip().splitlines()[0] or None

    @classmethod
    def download(
        cls,
        url: str,
        out_dir: str = ".",
        audio_only: bool = False,
        max_seconds: Optional[int] = None,
    ) -> Optional[str]:
        """Download *url* into *out_dir*; returns the file path or ``None``."""
        try:
            if not url or not cls.available():
                return None
            cmd = cls._cmd()
            if not cmd:
                return None
            out_dir = str(out_dir)
            os.makedirs(out_dir, exist_ok=True)
            template = os.path.join(out_dir, "%(title).80s_%(id)s.%(ext)s")
            full = cmd + [
                "--no-playlist",
                "--no-warnings",
                "-o", template,
                "--print", "after_move:filepath",
            ]
            if audio_only:
                full += ["-x", "--audio-format", "m4a"]
            if max_seconds:
                full += ["--download-sections", f"*0-{int(max_seconds)}"]
            full.append(url)
            started = time.time()
            proc = subprocess.run(
                full,
                capture_output=True,
                text=True,
                timeout=YTDLP_TIMEOUT,
            )
            if proc.returncode != 0:
                return None
            # yt-dlp prints the final path thanks to --print after_move:filepath
            for line in reversed((proc.stdout or "").splitlines()):
                candidate = line.strip().strip('"')
                if candidate and os.path.isfile(candidate):
                    return candidate
            # Fallback: newest file created by this run.
            newest, newest_mtime = None, started - 1.0
            for name in os.listdir(out_dir):
                path = os.path.join(out_dir, name)
                if os.path.isfile(path):
                    mtime = os.path.getmtime(path)
                    if mtime > newest_mtime:
                        newest, newest_mtime = path, mtime
            return newest
        except Exception:
            return None


# --------------------------------------------------------------------------- #
# Optional FREE LLM: Ollama or any OpenAI-compatible endpoint
# --------------------------------------------------------------------------- #
class LLMScriptWriter:
    """Generate script JSON via a local Ollama model or an OpenAI-compatible API."""

    DEFAULT_SYSTEM = (
        "You are a scriptwriter for short-form faceless videos "
        "(YouTube Shorts / Reels / TikTok). Reply with ONLY a JSON object."
    )

    @staticmethod
    def _ollama_base() -> str:
        host = _env("OLLAMA_HOST") or DEFAULT_OLLAMA_URL
        if "://" not in host:
            host = "http://" + host
        return host.rstrip("/")

    @classmethod
    def _backend(cls) -> Optional[Tuple[str, str]]:
        """Return ``("ollama", base)`` / ``("openai", base)`` or ``None``."""
        base = cls._ollama_base()
        if _http_ok(f"{base}/api/tags", timeout=HTTP_TIMEOUT):
            return ("ollama", base)
        openai_base = _env("LLM_BASE_URL")
        if openai_base and _env("LLM_API_KEY"):
            return ("openai", openai_base.rstrip("/"))
        return None

    @classmethod
    def available(cls) -> bool:
        """True when Ollama answers, or LLM_BASE_URL + LLM_API_KEY are set."""
        return cls._backend() is not None

    @staticmethod
    def _build_prompt(topic: str, language: str, system_prompt: str) -> str:
        return (
            f"Write a viral short-form video script about: {topic}\n"
            f"Language: {language or 'en'}\n"
            "Return a JSON object with keys: title, hook, scenes (array of strings), "
            "cta. Keep it under 60 seconds of narration."
            + (f"\nExtra instructions: {system_prompt}" if system_prompt else "")
        )

    @classmethod
    def _via_ollama(cls, base: str, prompt: str, system: str, model: Optional[str]) -> Optional[Dict[str, Any]]:
        chosen = model
        if not chosen:
            tags = _http_json(f"{base}/api/tags", timeout=HTTP_TIMEOUT)
            if isinstance(tags, dict):
                models = tags.get("models") or []
                if models and isinstance(models[0], dict):
                    chosen = str(models[0].get("name") or "") or None
        if not chosen:
            return None
        response = _http_json(
            f"{base}/api/generate",
            data={
                "model": chosen,
                "prompt": prompt,
                "system": system,
                "stream": False,
                "format": "json",
            },
            timeout=HTTP_IO_TIMEOUT,
        )
        if not isinstance(response, dict) or not response.get("response"):
            return None
        return _extract_json(response.get("response"))

    @classmethod
    def _via_openai(cls, base: str, prompt: str, system: str, model: Optional[str]) -> Optional[Dict[str, Any]]:
        response = _http_json(
            f"{base}/chat/completions",
            data={
                "model": model or _env("LLM_MODEL") or DEFAULT_LLM_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
            },
            headers={"Authorization": f"Bearer {_env('LLM_API_KEY')}"},
            timeout=HTTP_IO_TIMEOUT,
        )
        if not isinstance(response, dict):
            return None
        try:
            content = response["choices"][0]["message"]["content"]
        except Exception:
            return None
        return _extract_json(content)

    @classmethod
    def write_script(
        cls,
        topic: str,
        language: str = "en",
        system_prompt: str = "",
        model: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Ask the first reachable free LLM for script JSON (dict or None)."""
        try:
            if not topic:
                return None
            backend = cls._backend()
            if backend is None:
                return None
            kind, base = backend
            system = (system_prompt or "").strip() or cls.DEFAULT_SYSTEM
            prompt = cls._build_prompt(topic, language, system_prompt or "")
            if kind == "ollama":
                return cls._via_ollama(base, prompt, system, model)
            return cls._via_openai(base, prompt, system, model)
        except Exception:
            return None


# --------------------------------------------------------------------------- #
# Free-tier stock footage (Pexels + Pixabay)
# --------------------------------------------------------------------------- #
class StockBRoll:
    """Download free portrait stock clips for B-roll."""

    @staticmethod
    def available() -> bool:
        """True when a free Pexels or Pixabay API key is configured."""
        return bool(_env("PEXELS_API_KEY") or _env("PIXABAY_API_KEY"))

    @staticmethod
    def _out_dir() -> str:
        custom = _env("FACELESS_STOCK_DIR")
        if custom:
            return custom
        return os.path.join(os.path.expanduser("~"), ".cache", "faceless-shorts", "stock")

    @classmethod
    def _search_pexels(cls, query: str, orientation: str) -> Optional[str]:
        key = _env("PEXELS_API_KEY")
        if not key:
            return None
        params = urlencode(
            {"query": query, "orientation": orientation or "portrait", "per_page": 5}
        )
        data = _http_json(
            f"https://api.pexels.com/videos/search?{params}",
            headers={"Authorization": key},
            timeout=HTTP_SEARCH_TIMEOUT,
        )
        if not isinstance(data, dict):
            return None
        for video in data.get("videos") or []:
            if not isinstance(video, dict):
                continue
            files = [f for f in (video.get("video_files") or []) if isinstance(f, dict) and f.get("link")]
            hd = [f for f in files if (f.get("height") or 0) >= 1280]
            pick = hd[0] if hd else (files[0] if files else None)
            if pick:
                return str(pick["link"])
        return None

    @classmethod
    def _search_pixabay(cls, query: str) -> Optional[str]:
        key = _env("PIXABAY_API_KEY")
        if not key:
            return None
        params = urlencode({"key": key, "q": query, "per_page": 5})
        data = _http_json(
            f"https://pixabay.com/api/videos/?{params}",
            timeout=HTTP_SEARCH_TIMEOUT,
        )
        if not isinstance(data, dict):
            return None
        for hit in data.get("hits") or []:
            if not isinstance(hit, dict):
                continue
            videos = hit.get("videos") or {}
            for size in ("large", "medium", "small", "tiny"):
                url = (videos.get(size) or {}).get("url")
                if url:
                    return str(url)
        return None

    @classmethod
    def search_clip(cls, query: str, orientation: str = "portrait") -> Optional[str]:
        """Search Pexels (then Pixabay) and download the first clip.

        Returns the local ``.mp4`` path, or ``None`` when no key is set or
        anything fails. Never raises.
        """
        try:
            if not query or not cls.available():
                return None
            link = cls._search_pexels(str(query), orientation) or cls._search_pixabay(str(query))
            if not link:
                return None
            out_dir = cls._out_dir()
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception:
                return None
            slug = re.sub(r"[^a-z0-9]+", "_", str(query).lower()).strip("_")[:40] or "clip"
            destination = os.path.join(out_dir, f"{slug}_{uuid.uuid4().hex[:8]}.mp4")
            return _download(link, destination, timeout=HTTP_IO_TIMEOUT)
        except Exception:
            return None


# --------------------------------------------------------------------------- #
# Doctor report
# --------------------------------------------------------------------------- #
def _plain_table(headers: Tuple[str, ...], rows: List[Tuple[str, ...]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(str(cell)))

    def fmt(row: Tuple[str, ...]) -> str:
        return "  ".join(str(cell).ljust(widths[index]) for index, cell in enumerate(row)).rstrip()

    lines = [fmt(headers), "  ".join("-" * width for width in widths)]
    lines.extend(fmt(row) for row in rows)
    return "\n".join(lines)


def doctor_report() -> str:
    """Build a readable plain-text table of :func:`doctor` results."""
    data = doctor()
    headers = ("tool", "status", "version", "kind", "install", "hint")
    rows: List[Tuple[str, ...]] = []
    for key in TOOL_KEYS:
        info = data.get(key) or {}
        rows.append(
            (
                key,
                "OK" if info.get("available") else "MISSING",
                str(info.get("version") or "-"),
                str(info.get("kind") or "-"),
                str(info.get("install") or "-"),
                str(info.get("hint") or "-"),
            )
        )
    title = "faceless-shorts - optional tool doctor"
    if _RichTable is not None and _RichConsole is not None:
        try:
            table = _RichTable(title=title, show_header=True, show_lines=False)
            table.add_column("tool", style="cyan", no_wrap=True)
            table.add_column("status", no_wrap=True)
            table.add_column("version", no_wrap=True)
            table.add_column("kind")
            table.add_column("install", overflow="fold")
            table.add_column("hint", overflow="fold")
            for row in rows:
                style = "green" if row[1] == "OK" else "red"
                table.add_row(row[0], f"[{style}]{row[1]}[/]", *row[2:])
            buffer = io.StringIO()
            console = _RichConsole(
                file=buffer,
                width=120,
                force_terminal=False,
                color_system=None,
                highlight=False,
            )
            console.print(table)
            rendered = buffer.getvalue().strip()
            if rendered:
                return rendered
        except Exception:
            pass  # fall back to plain text
    return title + "\n" + _plain_table(headers, rows)
