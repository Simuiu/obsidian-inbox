from __future__ import annotations

import argparse
from pathlib import Path

from faster_whisper import WhisperModel


def format_ts(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe a task audio file with faster-whisper.")
    parser.add_argument("audio", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="zh")
    args = parser.parse_args()

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(args.audio),
        language=args.language,
        vad_filter=True,
        beam_size=5,
    )

    lines = [
        "# 转写全文",
        "",
        f"- language: {info.language}",
        f"- language_probability: {info.language_probability:.4f}",
        f"- duration: {format_ts(info.duration)}",
        "",
    ]

    for segment in segments:
        text = segment.text.strip()
        if not text:
            continue
        lines.append(f"[{format_ts(segment.start)} - {format_ts(segment.end)}] {text}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
