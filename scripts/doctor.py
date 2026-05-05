from __future__ import annotations

import importlib.util

from v2o_common import find_tool


CHECKS = [
    ("python module", "yt_dlp", "Bilibili/YouTube metadata and subtitles"),
    ("python module", "faster_whisper", "ASR transcription"),
    ("python module", "whispercpp", "Experimental whisper.cpp transcription"),
    ("command", "ffmpeg", "Extract audio from local video files"),
    ("command", "ffprobe", "Inspect local media metadata"),
    ("command", "resd-mini", "Capture WeChat Channels media through local proxy/listening"),
]


def module_exists(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_exists(name: str) -> bool:
    return find_tool(name) is not None


def main() -> None:
    print("# Obsidian Inbox Doctor")
    print("")
    missing: list[tuple[str, str]] = []
    for kind, name, purpose in CHECKS:
        ok = module_exists(name) if kind == "python module" else command_exists(name)
        mark = "OK" if ok else "MISSING"
        print(f"- {mark}: {kind} `{name}` - {purpose}")
        if not ok:
            missing.append((name, purpose))

    print("")
    if missing:
        print("## Missing")
        for name, purpose in missing:
            print(f"- `{name}`: {purpose}")
        print("")
        print("Install `ffmpeg` before using automatic ASR for WeChat Channels, Douyin, Xiaohongshu, or local videos.")
    else:
        print("All required runtime dependencies are available.")


if __name__ == "__main__":
    main()
