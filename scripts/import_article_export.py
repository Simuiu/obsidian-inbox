from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from obsidian_store import entry_key, note_path_for, resource_dir_for
from v2o_common import link_id, load_config, safe_filename, today, write_json


ARTICLE_PLATFORMS = ["local_export", "xiaohongshu", "douyin", "web", "wechat"]


def copy_images(image_dir: Path, target: Path) -> int:
    count = 0
    if not image_dir.exists():
        return 0
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(image_dir.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            continue
        name = safe_filename(path.stem, max_len=50) + path.suffix.lower()
        shutil.copy2(path, target / name)
        count += 1
    return count


def rewrite_image_links(content: str, image_count: int) -> str:
    if image_count <= 0:
        return content
    lines = [content.rstrip(), "", "## 本地图片", ""]
    for index in range(1, image_count + 1):
        lines.append(f"- images/image-{index:03d}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a local article/image-text export into Obsidian Inbox.")
    parser.add_argument("--platform", required=True, choices=ARTICLE_PLATFORMS)
    parser.add_argument("--content", type=Path, required=True, help="Markdown or text file exported by the user.")
    parser.add_argument("--source-url", required=True, help="Original link or source description.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--published-at", default="")
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument("--content-type", choices=["article", "image_text"], default="image_text")
    args = parser.parse_args()

    if not args.content.exists():
        raise SystemExit(f"Content file not found: {args.content}")
    if args.image_dir and not args.image_dir.exists():
        raise SystemExit(f"Image directory not found: {args.image_dir}")

    config = load_config()
    source = link_id(args.source_url)
    meta = {
        "task_id": f"{today()}-{args.platform}-{source}",
        "status": "article_captured",
        "platform": args.platform,
        "content_type": args.content_type,
        "mode": "standard",
        "created_at": today(),
        "video_id": source,
        "title": args.title,
        "author": args.author,
        "duration": "",
        "published_at": args.published_at,
        "source_url": args.source_url,
        "capture_source": "local_export",
    }
    meta["entry_key"] = entry_key(meta)
    meta["resource_dir"] = str(resource_dir_for(config, meta))
    meta["standard_note_path"] = str(note_path_for(config, meta, "standard"))
    meta["deep_note_path"] = str(note_path_for(config, meta, "deep"))

    task_dir = Path(config["tasks"]["task_dir"]) / meta["task_id"]
    task_dir.mkdir(parents=True, exist_ok=True)
    resource_dir = resource_dir_for(config, meta)
    resource_dir.mkdir(parents=True, exist_ok=True)

    content = args.content.read_text(encoding="utf-8")
    task_images = task_dir / "images"
    resource_images = resource_dir / "images"
    if task_images.exists():
        shutil.rmtree(task_images)
    if resource_images.exists():
        shutil.rmtree(resource_images)
    image_count = copy_images(args.image_dir, task_images) if args.image_dir else 0
    if task_images.exists():
        resource_images.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(task_images, resource_images)

    content = rewrite_image_links(content, image_count)
    (task_dir / "content.md").write_text(content, encoding="utf-8")
    shutil.copy2(task_dir / "content.md", resource_dir / "content.md")
    meta["image_count"] = image_count
    write_json(task_dir / "meta.json", meta)
    write_json(resource_dir / "meta.json", meta)

    compact_cmd = [sys.executable, "scripts/make_compact.py", str(task_dir)]
    compact_result = subprocess.run(compact_cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if compact_result.returncode != 0:
        meta["status"] = "compact_failed"
        meta["failure_reason"] = compact_result.stdout[-1200:]
        write_json(task_dir / "meta.json", meta)
        write_json(resource_dir / "meta.json", meta)

    prompt = [
        "# Obsidian Inbox Local Export Task",
        "",
        "请基于本任务包生成 Obsidian 笔记。",
        "",
        "- 优先读取 compact.md。",
        "- 本地导出的图片和正文只链接到 _resources，不要把原始材料完整塞进主笔记。",
        "- 不要编造本地导出材料中没有的信息。",
    ]
    (task_dir / "prompt.md").write_text("\n".join(prompt) + "\n", encoding="utf-8")
    print(task_dir.resolve())
    print(resource_dir)


if __name__ == "__main__":
    main()
