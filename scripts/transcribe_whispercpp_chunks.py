from __future__ import annotations

import argparse
from pathlib import Path

from whispercpp import Whisper


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe WAV chunks with whispercpp.")
    parser.add_argument("chunks_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="tiny")
    parser.add_argument("--model-dir", default="models/whispercpp")
    args = parser.parse_args()

    chunks = sorted(args.chunks_dir.glob("chunk_*.wav"))
    if not chunks:
        raise SystemExit(f"No chunk_*.wav files found in {args.chunks_dir}")

    model = Whisper.from_pretrained(args.model, basedir=args.model_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("# 转写全文\n\n", encoding="utf-8")

    for index, chunk in enumerate(chunks, start=1):
        text = model.transcribe_from_file(str(chunk)).strip()
        with args.output.open("a", encoding="utf-8") as handle:
            handle.write(f"## Chunk {index:02d}\n\n{text}\n\n")
        print(f"chunk {index}/{len(chunks)} done: {chunk.name}, chars={len(text)}", flush=True)


if __name__ == "__main__":
    main()
