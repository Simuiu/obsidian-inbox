from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_srt(text: str) -> list[tuple[str, str]]:
    blocks = re.split(r"\n\s*\n", text.strip())
    rows: list[tuple[str, str]] = []
    for block in blocks:
        parts = [p.strip() for p in block.splitlines() if p.strip()]
        if len(parts) < 3 or "-->" not in parts[1]:
            continue
        start = parts[1].split(" --> ", 1)[0].replace(",", ".")
        content = "".join(parts[2:]).strip()
        if content:
            rows.append((start, content))
    return rows


def clean_srt(srt_path: Path, output_dir: Path) -> None:
    rows = parse_srt(srt_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "transcript_clean.txt").write_text(
        "\n".join(text for _, text in rows) + "\n",
        encoding="utf-8",
    )
    (output_dir / "transcript_timed.md").write_text(
        "# 带时间点转写\n\n" + "\n\n".join(f"[{start}] {text}" for start, text in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean SRT into transcript files.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    clean_srt(args.srt, args.output_dir)


if __name__ == "__main__":
    main()
