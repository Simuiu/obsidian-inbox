from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from obsidian_store import entry_key, note_path_for, resource_dir_for
from v2o_common import find_tool, link_id, load_config, safe_filename, today, write_json


MEDIA_PLATFORMS = ["wechat_video", "local_video", "douyin", "xiaohongshu"]


def read_text_if_present(path: Path | None) -> str:
    if not path:
        return ""
    return path.read_text(encoding="utf-8")


def normalize_transcript(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "# 转写全文\n\n" + "\n\n".join(lines) + "\n"


def transcript_body_length(text: str) -> int:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("- language") or stripped.startswith("- duration"):
            continue
        lines.append(stripped)
    return len("".join(lines))


def build_compact(task_dir: Path, meta: dict, transcript_text: str) -> None:
    excerpt = transcript_text.replace("\n", " ")[:3000]
    lines = [
        "# Compact Context",
        "",
        "## 元信息",
        "",
        f"- 标题：{meta.get('title', '')}",
        f"- 平台：{meta.get('platform', '')}",
        f"- 作者：{meta.get('author', '')}",
        f"- 发布时间：{meta.get('published_at', '')}",
        f"- 链接：{meta.get('source_url', '')}",
        "",
        "## 转写摘录",
        "",
        excerpt,
        "",
        "## 给 Codex 的输出要求",
        "",
        "- 基于 compact 内容生成 Obsidian 笔记。",
        "- 不要编造转写或视频中没有的信息。",
        "- 主笔记保留摘要、重点、可实践行动和后续可追问问题。",
        "- 原始材料只链接到 _resources 文件。",
    ]
    (task_dir / "compact.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_audio(video: Path, output: Path) -> None:
    ffmpeg = find_tool("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found. Install ffmpeg or provide --transcript.")
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output),
    ]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout[-1000:])


def transcribe_audio(audio: Path, output: Path, model: str, language: str) -> None:
    cmd = ["python3", "scripts/transcribe_task.py", str(audio), "--output", str(output), "--model", model, "--language", language]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout[-1000:])


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a locally captured video into Obsidian Inbox task structure.")
    parser.add_argument("--platform", default="wechat_video", choices=MEDIA_PLATFORMS, help="Source platform recorded in metadata.")
    parser.add_argument("--video", type=Path, required=True, help="Local video file captured by resd-mini, res-downloader, or another downloader.")
    parser.add_argument("--source-url", required=True, help="Original source URL or share URL.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--published-at", default="")
    parser.add_argument("--transcript", type=Path, help="Optional transcript text/markdown file. If omitted, the task is marked as needing ASR.")
    parser.add_argument("--asr", action="store_true", help="Extract audio with ffmpeg and transcribe with faster-whisper.")
    parser.add_argument("--asr-model", default="small")
    parser.add_argument("--language", default="zh")
    args = parser.parse_args()

    if not args.video.exists():
        raise SystemExit(f"Video not found: {args.video}")

    config = load_config()
    source = link_id(args.source_url)
    capture_tools = []
    capture_source = "local_file"
    if args.platform == "wechat_video":
        capture_source = "external_downloader"
        capture_tools = [
            "https://github.com/putyy/resd-mini",
            "https://github.com/putyy/res-downloader",
            "https://github.com/qiye45/wechatVideoDownload",
        ]

    meta = {
        "task_id": f"{today()}-{args.platform}-{source}",
        "status": "media_captured",
        "platform": args.platform,
        "content_type": "video",
        "mode": "deep" if args.platform in {"local_video", "wechat_video"} else "standard",
        "created_at": today(),
        "video_id": source,
        "title": args.title,
        "author": args.author,
        "duration": "",
        "published_at": args.published_at,
        "source_url": args.source_url,
        "capture_source": capture_source,
        "capture_tools": capture_tools,
        "local_video_path": str(args.video.resolve()),
        "media_storage": "external_local_path" if args.platform == "local_video" else "external_downloader",
    }
    meta["entry_key"] = entry_key(meta)
    meta["resource_dir"] = str(resource_dir_for(config, meta))
    meta["standard_note_path"] = str(note_path_for(config, meta, "standard"))
    meta["deep_note_path"] = str(note_path_for(config, meta, "deep"))

    task_dir = Path(config["tasks"]["task_dir"]) / meta["task_id"]
    task_dir.mkdir(parents=True, exist_ok=True)
    resource_dir = resource_dir_for(config, meta)
    resource_dir.mkdir(parents=True, exist_ok=True)

    video_name = safe_filename(args.video.stem, max_len=60) + args.video.suffix.lower()
    meta["media_file"] = video_name

    transcript_text = read_text_if_present(args.transcript)
    if not transcript_text and args.asr:
        try:
            audio_path = task_dir / "audio.wav"
            transcript_path = task_dir / "asr_transcript.md"
            extract_audio(args.video, audio_path)
            transcribe_audio(audio_path, transcript_path, args.asr_model, args.language)
            transcript_text = transcript_path.read_text(encoding="utf-8")
            meta["asr_model"] = args.asr_model
            meta["asr_language"] = args.language
            if audio_path.exists():
                audio_path.unlink()
        except Exception as exc:
            meta["asr_error"] = str(exc)

    if transcript_text:
        normalized = normalize_transcript(transcript_text)
        if transcript_body_length(transcript_text) < 20:
            meta["status"] = "needs_asr_review"
            meta["failure_reason"] = "ASR completed but produced too little usable transcript text; review audio/transcript before summarizing."
            (task_dir / "asr_transcript.md").write_text(normalized, encoding="utf-8")
            (resource_dir / "转写待复核.md").write_text(normalized, encoding="utf-8")
        else:
            (task_dir / "transcript_timed.md").write_text(normalized, encoding="utf-8")
            (resource_dir / "转写.md").write_text(normalized, encoding="utf-8")
            meta["status"] = "transcript_captured"
            build_compact(task_dir, meta, transcript_text)
    else:
        meta["status"] = "needs_asr"
        meta["failure_reason"] = "视频文件已导入，但未提供转写；需要 ASR 后才能生成可靠总结。"

    write_json(task_dir / "meta.json", meta)
    prompt = [
        "# Obsidian Inbox Video Task",
        "",
        "请基于本任务包生成 Obsidian 笔记。",
        "",
        "如果没有 compact.md 或转写内容，不要编造视频总结；只说明已收集视频且需要 ASR。",
    ]
    (task_dir / "prompt.md").write_text("\n".join(prompt) + "\n", encoding="utf-8")
    print(task_dir.resolve())
    print(resource_dir)


if __name__ == "__main__":
    main()
