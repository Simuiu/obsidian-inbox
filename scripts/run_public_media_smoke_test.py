from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from v2o_common import ROOT, find_tool


SAMPLE_PAGE_URL = "https://github.com/bower-media-samples/big-buck-bunny-480p-30s"
SAMPLE_FILE_URL = "https://raw.githubusercontent.com/bower-media-samples/big-buck-bunny-480p-30s/master/video.mp4"
SAMPLE_LICENSE = "Creative Commons Attribution 3.0"


def download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "video2obsidian-public-smoke-test/1.0"})
    with urlopen(req, timeout=60) as response, output.open("wb") as fh:
        shutil.copyfileobj(response, fh)


def trim_video(input_path: Path, output_path: Path, seconds: int) -> None:
    ffmpeg = find_tool("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found; run scripts/doctor.py first.")
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(input_path),
        "-t",
        str(seconds),
        "-c",
        "copy",
        str(output_path),
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout[-1200:])


def run_import(video: Path, transcript: Path, asr: bool) -> Path:
    cmd = [
        sys.executable,
        "scripts/import_media.py",
        "--platform",
        "local_video",
        "--video",
        str(video),
        "--source-url",
        SAMPLE_PAGE_URL,
        "--title",
        "Big Buck Bunny 公开测试片段",
        "--author",
        "Blender Foundation",
        "--published-at",
        "2008-06-07",
    ]
    if asr:
        cmd.extend(["--asr", "--asr-model", "tiny", "--language", "en"])
    else:
        cmd.extend(["--transcript", str(transcript)])

    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout)
    first_line = result.stdout.splitlines()[0].strip()
    return Path(first_line)


def make_transcript(path: Path) -> None:
    text = """# 转写全文

[00:00 - 00:12] This is a public downloadable sample video used only to verify local media import.

[00:12 - 00:24] The smoke test checks task metadata, resource copying, transcript capture, and compact context generation.

[00:24 - 00:35] It does not access login-only platforms, private content, or copyrighted platform media.
"""
    path.write_text(text, encoding="utf-8")


def verify(task_dir: Path) -> dict[str, object]:
    meta_path = task_dir / "meta.json"
    compact_path = task_dir / "compact.md"
    transcript_path = task_dir / "transcript_timed.md"
    if not meta_path.exists():
        raise RuntimeError(f"missing meta.json: {meta_path}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    resource_dir = Path(meta["resource_dir"])
    media_file = meta.get("media_file")
    checks = {
        "task_dir": str(task_dir),
        "resource_dir": str(resource_dir),
        "platform": meta.get("platform"),
        "status": meta.get("status"),
        "compact_exists": compact_path.exists(),
        "transcript_exists": transcript_path.exists(),
        "resource_dir_exists": resource_dir.exists(),
        "media_file": media_file,
        "local_video_path": meta.get("local_video_path"),
        "resource_media_exists": bool(media_file and (resource_dir / media_file).exists()),
        "resource_audio_exists": (resource_dir / "audio.wav").exists(),
    }
    failures = []
    if meta.get("platform") != "local_video":
        failures.append("platform is not local_video")
    if meta.get("status") != "transcript_captured":
        failures.append(f"status is {meta.get('status')}")
    if not compact_path.exists():
        failures.append("compact.md missing")
    if not transcript_path.exists():
        failures.append("transcript_timed.md missing")
    if not resource_dir.exists():
        failures.append("resource dir missing")
    if not meta.get("local_video_path"):
        failures.append("local_video_path missing")
    if media_file and (resource_dir / media_file).exists():
        failures.append("local video was copied into Obsidian resources")
    if (resource_dir / "audio.wav").exists():
        failures.append("audio.wav was copied into Obsidian resources")
    checks["passed"] = not failures
    checks["failures"] = failures
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a smoke test with a public, downloadable sample video.")
    parser.add_argument("--keep", action="store_true", help="Keep generated task/resource files.")
    parser.add_argument("--asr", action="store_true", help="Use local ASR instead of the fixture transcript.")
    parser.add_argument("--seconds", type=int, default=35, help="Trim sample video to this many seconds before import.")
    args = parser.parse_args()

    work_dir = ROOT / "tasks" / "_smoke_public_media"
    source_video = work_dir / "big-buck-bunny-30s.mp4"
    clipped_video = work_dir / f"big-buck-bunny-{args.seconds}s.mp4"
    transcript = work_dir / "fixture_transcript.md"

    if not source_video.exists():
        download(SAMPLE_FILE_URL, source_video)
    trim_video(source_video, clipped_video, args.seconds)
    make_transcript(transcript)

    task_dir = run_import(clipped_video, transcript, args.asr)
    result = verify(task_dir)
    result["sample_page"] = SAMPLE_PAGE_URL
    result["sample_license"] = SAMPLE_LICENSE

    if not args.keep:
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
        resource_dir = Path(meta["resource_dir"])
        shutil.rmtree(task_dir, ignore_errors=True)
        shutil.rmtree(resource_dir, ignore_errors=True)
        try:
            resource_dir.parent.rmdir()
        except OSError:
            pass
        shutil.rmtree(work_dir, ignore_errors=True)
        result["cleaned"] = True
    else:
        result["cleaned"] = False

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
