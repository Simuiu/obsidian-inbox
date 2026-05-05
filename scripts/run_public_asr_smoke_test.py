from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from v2o_common import ROOT


SAMPLE_PAGE_URL = "https://github.com/openai/whisper/blob/main/tests/jfk.flac"
SAMPLE_FILE_URL = "https://raw.githubusercontent.com/openai/whisper/main/tests/jfk.flac"
SAMPLE_LICENSE = "OpenAI Whisper repository test fixture"


def download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "video2obsidian-public-asr-smoke-test/1.0"})
    with urlopen(req, timeout=60) as response, output.open("wb") as fh:
        shutil.copyfileobj(response, fh)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ASR smoke test with a public downloadable audio fixture.")
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--model", default="tiny")
    parser.add_argument("--language", default="en")
    args = parser.parse_args()

    work_dir = ROOT / "tasks" / "_smoke_public_asr"
    audio = work_dir / "jfk.flac"
    output = work_dir / "asr_transcript.md"
    if not audio.exists():
        download(SAMPLE_FILE_URL, audio)

    cmd = [
        sys.executable,
        "scripts/transcribe_task.py",
        str(audio),
        "--output",
        str(output),
        "--model",
        args.model,
        "--language",
        args.language,
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    transcript = output.read_text(encoding="utf-8") if output.exists() else ""
    checks = {
        "sample_page": SAMPLE_PAGE_URL,
        "sample_license": SAMPLE_LICENSE,
        "model": args.model,
        "language": args.language,
        "returncode": result.returncode,
        "output_exists": output.exists(),
        "transcript_chars": len(transcript),
        "contains_expected_phrase": "my fellow americans" in transcript.lower() or "fellow americans" in transcript.lower(),
    }
    checks["passed"] = (
        result.returncode == 0
        and checks["output_exists"]
        and checks["transcript_chars"] > 80
        and checks["contains_expected_phrase"]
    )
    if not args.keep:
        shutil.rmtree(work_dir, ignore_errors=True)
        checks["cleaned"] = True
    else:
        checks["cleaned"] = False
        checks["work_dir"] = str(work_dir)
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    if not checks["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
