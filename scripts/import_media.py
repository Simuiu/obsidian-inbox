from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SUPPORTED_PLATFORMS = {"wechat_video", "douyin", "xiaohongshu", "local_video"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Import locally captured media into Obsidian Inbox.")
    parser.add_argument("--platform", required=True, choices=sorted(SUPPORTED_PLATFORMS))
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--published-at", default="")
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--asr", action="store_true")
    parser.add_argument("--asr-model", default="small")
    parser.add_argument("--language", default="zh")
    args = parser.parse_args()

    if args.platform not in {"wechat_video", "local_video", "douyin", "xiaohongshu"}:
        raise SystemExit(
            f"{args.platform} import is not implemented yet. "
            "Use this command shape later; currently local video imports are wired for wechat_video, local_video, douyin, and xiaohongshu."
        )

    cmd = [
        sys.executable,
        "scripts/import_wechat_video.py",
        "--platform",
        args.platform,
        "--video",
        str(args.video),
        "--source-url",
        args.source_url,
        "--title",
        args.title,
        "--author",
        args.author,
    ]
    if args.published_at:
        cmd.extend(["--published-at", args.published_at])
    if args.transcript:
        cmd.extend(["--transcript", str(args.transcript)])
    if args.asr:
        cmd.extend(["--asr", "--asr-model", args.asr_model, "--language", args.language])

    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
