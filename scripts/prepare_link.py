from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from clean_srt import clean_srt
from fetch_article import fetch_article
from obsidian_store import entry_key, note_path_for, resource_dir_for
from v2o_common import ROOT, detect_platform, link_id, load_config, run, today, write_json


def yt_dlp_metadata(url: str) -> dict[str, str]:
    fields = ["%(id)s", "%(title)s", "%(uploader)s", "%(duration_string)s", "%(upload_date>%Y-%m-%d)s", "%(webpage_url)s"]
    cmd = ["python3", "-m", "yt_dlp", "--skip-download"]
    for field in fields:
        cmd.extend(["--print", field])
    cmd.append(url)
    result = run(cmd)
    if result.returncode != 0:
        raise RuntimeError(result.stdout)
    values = [line.strip() for line in result.stdout.splitlines() if line.strip() and not line.startswith("Deprecated Feature")]
    values = values[-6:]
    return {
        "video_id": values[0],
        "title": values[1],
        "author": values[2],
        "duration": values[3],
        "published_at": values[4],
        "source_url": values[5],
    }


def bilibili_cookie_args(config: dict) -> list[str]:
    bilibili = config.get("bilibili", {})
    cookies_file = bilibili.get("cookies_file")
    if cookies_file:
        cookie_path = (ROOT / cookies_file).expanduser()
        if cookie_path.exists():
            return ["--cookies", str(cookie_path)]

    browser = bilibili.get("fallback_cookies_from_browser", "chrome")
    if browser:
        return ["--cookies-from-browser", browser]
    return []


def download_subtitle(url: str, task_dir: Path, platform: str, config: dict) -> Path | None:
    output_template = str(task_dir / "subtitle.%(ext)s")
    cmd = ["python3", "-m", "yt_dlp", "--skip-download", "--write-subs", "--sub-format", "srt", "-o", output_template]
    if platform == "bilibili":
        cmd.extend(bilibili_cookie_args(config))
        cmd.extend(["--sub-langs", "ai-zh"])
    elif platform == "youtube":
        cmd.extend(["--write-auto-subs", "--sub-langs", "zh.*,en.*"])
    else:
        return None
    cmd.append(url)
    result = run(cmd)
    (task_dir / "yt-dlp.log").write_text(result.stdout, encoding="utf-8")
    if result.returncode != 0:
        return None
    subtitles = sorted(task_dir.glob("subtitle*.srt"))
    return subtitles[0] if subtitles else None


def prepare(url: str, mode: str = "standard") -> Path:
    config = load_config()
    platform = detect_platform(url)
    metadata_error = ""
    if platform in {"bilibili", "youtube"}:
        try:
            metadata = yt_dlp_metadata(url)
        except Exception as exc:
            metadata_error = str(exc)
            metadata = {
                "video_id": link_id(url),
                "title": f"{platform} 视频待抓取",
                "author": "",
                "duration": "",
                "published_at": "",
                "source_url": url,
            }
    else:
        metadata = {
            "video_id": link_id(url),
            "title": "待抓取文章",
            "author": "",
            "duration": "",
            "published_at": "",
            "source_url": url,
        }
    task_id = f"{today()}-{platform}-{metadata['video_id']}"
    task_dir = ROOT / config["tasks"]["task_dir"] / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "task_id": task_id,
        "status": "metadata_captured",
        "platform": platform,
        "content_type": "video" if platform in {"bilibili", "youtube"} else "article",
        "mode": mode,
        "created_at": today(),
        **metadata,
    }
    if platform not in {"bilibili", "youtube"}:
        meta["content_type"] = "article"
    meta["entry_key"] = entry_key(meta)
    meta["resource_dir"] = str(resource_dir_for(config, meta))
    meta["standard_note_path"] = str(note_path_for(config, meta, "standard"))
    meta["deep_note_path"] = str(note_path_for(config, meta, "deep"))
    write_json(task_dir / "meta.json", meta)

    if platform in {"bilibili", "youtube"}:
        if metadata_error:
            meta["status"] = "metadata_capture_failed"
            meta["failure_reason"] = metadata_error[-1200:]
            write_json(task_dir / "meta.json", meta)
        else:
            subtitle = download_subtitle(url, task_dir, platform, config)
            if subtitle:
                clean_srt(subtitle, task_dir)
                meta["status"] = "subtitle_captured"
                meta["subtitle_file"] = subtitle.name
                write_json(task_dir / "meta.json", meta)
                compact_cmd = ["python3", "scripts/make_compact.py", str(task_dir)]
                if mode == "deep":
                    compact_cmd.extend(["--mode", "deep"])
                run(compact_cmd)
            else:
                meta["status"] = "needs_subtitle_or_asr"
                write_json(task_dir / "meta.json", meta)
    elif platform == "wechat_video":
        meta["status"] = "needs_wechat_video_capture"
        meta["failure_reason"] = "微信视频号需要接入桌面监听/下载器后才能稳定获取视频正文、音频或字幕；当前已识别来源但不生成总结。"
        meta["content_type"] = "video"
        write_json(task_dir / "meta.json", meta)
    else:
        try:
            article_meta = fetch_article(url, task_dir)
            meta.update(
                {
                    "status": "article_captured",
                    "title": article_meta.get("title") or meta["title"],
                    "author": article_meta.get("author") or meta.get("author", ""),
                    "published_at": article_meta.get("published_at") or meta.get("published_at", ""),
                    "source_url": article_meta.get("source_url") or url,
                }
            )
            meta["entry_key"] = entry_key(meta)
            meta["resource_dir"] = str(resource_dir_for(config, meta))
            meta["standard_note_path"] = str(note_path_for(config, meta, "standard"))
            meta["deep_note_path"] = str(note_path_for(config, meta, "deep"))
            write_json(task_dir / "meta.json", meta)
            compact_cmd = ["python3", "scripts/make_compact.py", str(task_dir)]
            if mode == "deep":
                compact_cmd.extend(["--mode", "deep"])
            run(compact_cmd)
        except Exception as exc:
            meta["status"] = "article_capture_failed"
            meta["failure_reason"] = str(exc)
            write_json(task_dir / "meta.json", meta)

    if (task_dir / "meta.json").exists():
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
        meta["resource_dir"] = str(resource_dir_for(config, meta))
        meta["standard_note_path"] = str(note_path_for(config, meta, "standard"))
        meta["deep_note_path"] = str(note_path_for(config, meta, "deep"))
        write_json(task_dir / "meta.json", meta)

    prompt = [
        "# Video2Obsidian Task",
        "",
        "请基于本任务包生成 Obsidian 笔记。",
        "",
        f"模式：{mode}",
        "",
        "优先读取 compact.md；不要读取完整字幕，除非 compact 信息明显不足。",
    ]
    if mode == "deep":
        prompt.extend(
            [
                "",
                "深度模式要求：重构教学逻辑，输出更完整的 Markdown 笔记；如果 compact 信息不足以支撑深度总结，明确说明限制，再按可得内容总结。",
            ]
        )
    (task_dir / "prompt.md").write_text("\n".join(prompt) + "\n", encoding="utf-8")

    return task_dir


def sync_raw_to_obsidian(task_dir: Path) -> None:
    config = load_config()
    meta = __import__("json").loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    raw_dir = resource_dir_for(config, meta)
    raw_dir.mkdir(parents=True, exist_ok=True)
    for name in ["transcript_timed.md", meta.get("subtitle_file", ""), "content.md", "article_raw.html", "article_meta.json", "article_diagnostics.json"]:
        if not name:
            continue
        src = task_dir / name
        if src.exists():
            suffix = "带时间点转写.md" if name == "transcript_timed.md" else name
            shutil.copy2(src, raw_dir / suffix)
    image_dir = task_dir / "images"
    if image_dir.exists():
        target = raw_dir / "images"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(image_dir, target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a Video2Obsidian task package.")
    parser.add_argument("url")
    parser.add_argument(
        "--mode",
        choices=["standard", "deep"],
        default="standard",
        help="Use standard low-token notes or deeper teaching-note prompts.",
    )
    parser.add_argument("--sync-raw", action="store_true", help="Copy raw transcript files into the Obsidian per-entry resource folder.")
    args = parser.parse_args()

    task_dir = prepare(args.url, args.mode)
    if args.sync_raw:
        sync_raw_to_obsidian(task_dir)
    print(task_dir)


if __name__ == "__main__":
    main()
