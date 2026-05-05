from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path

from obsidian_store import entry_folder_name, note_dir, parse_frontmatter
from v2o_common import load_config


OLD_ROOT_REL = "00_Inbox/内容入库"
OLD_RESOURCE_REL = "00_Inbox/内容入库/_resources"
BIG_EXTS = {".mp4", ".ts", ".mov", ".mkv", ".m4v", ".wav", ".m4a", ".mp3"}
ROOT_INDEX_NAMES = {"内容入库索引.md", "资料库索引.md", "主题索引.md", "用途索引.md"}


def vault_path(config: dict) -> Path:
    return Path(config["obsidian"]["vault_path"]).expanduser()


def old_root(config: dict) -> Path:
    return vault_path(config) / OLD_ROOT_REL


def old_resource_root(config: dict) -> Path:
    return vault_path(config) / OLD_RESOURCE_REL


def note_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.glob("*.md")
        if path.name not in ROOT_INDEX_NAMES and not path.name.startswith("_")
    )


def yaml_quote(value: str) -> str:
    return '"' + str(value or "").replace('"', '\\"') + '"'


def frontmatter_block(meta: dict) -> str:
    lines = ["---"]
    ordered = [
        "title",
        "source",
        "type",
        "platform",
        "author",
        "published_at",
        "created_at",
        "status",
        "entry_id",
        "resource_dir",
        "local_video_path",
        "media_storage",
    ]
    for key in ordered:
        if key in meta and meta[key] not in (None, ""):
            lines.append(f"{key}: {yaml_quote(str(meta[key]))}")
    for key in ["purposes", "tags"]:
        values = meta.get(key)
        if isinstance(values, str):
            values = [values]
        if isinstance(values, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {value}" for value in values)
    lines.append("---")
    return "\n".join(lines)


def replace_frontmatter(text: str, meta: dict) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return frontmatter_block(meta) + text[end + 4 :]
    return frontmatter_block(meta) + "\n\n" + text


def normalize_note_links(text: str, entry_id: str) -> str:
    if entry_id:
        text = text.replace(f"_resources/{entry_id}/", "_resources/")
        text = text.replace(f"../_resources/{entry_id}/", "_resources/")
    text = re.sub(r"\]\([^)]*内容入库索引\.md\)", "](../资料库索引.md)", text)
    return text


def remove_big_resource_links(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("- [") and any(ext in stripped for ext in BIG_EXTS):
            continue
        lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def add_local_video_reference(text: str, meta: dict) -> str:
    local_path = str(meta.get("local_video_path") or "")
    if not local_path or "本地原视频路径" in text:
        return text
    marker = "## 原始材料\n"
    line = f"\n- 本地原视频路径：`{local_path}`\n"
    if marker in text:
        return text.replace(marker, marker + line, 1)
    return text.rstrip() + "\n\n## 原始材料\n" + line


def is_deep(path: Path, meta: dict) -> bool:
    status = str(meta.get("status") or "")
    tags = meta.get("tags") or []
    return "深度" in path.stem or "深度" in status or "深度笔记" in tags


def pick_main(paths: list[Path], metas: dict[Path, dict]) -> tuple[Path, list[Path]]:
    deep = [path for path in paths if is_deep(path, metas[path])]
    main = sorted(deep or paths, key=lambda path: path.name)[-1]
    return main, [path for path in paths if path != main]


def merge_meta(meta: dict, main_path: Path) -> dict:
    updated = dict(meta)
    updated["resource_dir"] = "_resources"
    source = str(updated.get("source") or updated.get("source_url") or "")
    if source.startswith("local:"):
        local_path = source.removeprefix("local:")
        updated["local_video_path"] = local_path
        updated["media_storage"] = "external_local_path"
    elif source.startswith(("http://", "https://")):
        updated["media_storage"] = "remote_link"
    if is_deep(main_path, updated):
        updated["status"] = str(updated.get("status") or "已深度总结")
    return updated


def copy_light_resources(src_dir: Path, dst_dir: Path, delete_candidates: list[Path], apply: bool) -> list[Path]:
    copied: list[Path] = []
    if not src_dir.exists():
        return copied
    for src in sorted(path for path in src_dir.rglob("*") if path.is_file()):
        if src.suffix.lower() in BIG_EXTS:
            delete_candidates.append(src)
            continue
        rel = src.relative_to(src_dir)
        dst = dst_dir / rel
        copied.append(dst)
        if apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return copied


def write_delete_manifest(new_root: Path, delete_candidates: list[Path], tasks_report: list[tuple[Path, int]], apply: bool) -> Path:
    manifest = new_root / "待确认删除大文件清单.md"
    lines = [
        "# 待确认删除大文件清单",
        "",
        "以下文件没有被迁入新资料库。删除前需要用户再次明确确认。",
        "",
        "## Obsidian Vault 旧资源大文件",
        "",
        "| 文件 | 大小 MB |",
        "|---|---:|",
    ]
    total = 0
    for path in sorted(set(delete_candidates)):
        size = path.stat().st_size if path.exists() else 0
        total += size
        lines.append(f"| `{path}` | {size / 1024 / 1024:.1f} |")
    lines.extend(["", f"合计：{total / 1024 / 1024:.1f} MB", "", "## tasks 工作台空间报告", "", "| 文件 | 大小 MB |", "|---|---:|"])
    for path, size in sorted(tasks_report, key=lambda item: item[1], reverse=True):
        lines.append(f"| `{path}` | {size / 1024 / 1024:.1f} |")
    if apply:
        new_root.mkdir(parents=True, exist_ok=True)
        manifest.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return manifest


def tasks_big_files() -> list[tuple[Path, int]]:
    root = Path("tasks")
    if not root.exists():
        return []
    rows = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in BIG_EXTS:
            rows.append((path, path.stat().st_size))
    return rows


def migrate(apply: bool) -> None:
    config = load_config()
    src_root = old_root(config)
    src_resources = old_resource_root(config)
    dst_root = note_dir(config)
    notes = note_files(src_root)
    metas = {path: parse_frontmatter(path) for path in notes}
    by_entry: dict[str, list[Path]] = defaultdict(list)
    for path, meta in metas.items():
        entry = str(meta.get("entry_id") or path.stem)
        by_entry[entry].append(path)

    delete_candidates: list[Path] = []
    print(f"mode={'apply' if apply else 'dry-run'}")
    print(f"old_root={src_root}")
    print(f"new_root={dst_root}")
    for entry, paths in sorted(by_entry.items()):
        main, archives = pick_main(paths, metas)
        meta = merge_meta(metas[main], main)
        folder_name = entry_folder_name(meta)
        dst_dir = dst_root / folder_name
        dst_note = dst_dir / f"{folder_name}.md"
        dst_resources = dst_dir / "_resources"
        src_res = src_resources / entry
        print(f"\nENTRY {entry}")
        print(f"  main: {main.name} -> {dst_note}")
        for archive in archives:
            print(f"  archive: {archive.name} -> {dst_resources / '普通总结归档.md'}")
        copied = copy_light_resources(src_res, dst_resources, delete_candidates, apply)
        for dst in copied:
            print(f"  resource: {dst}")
        if apply:
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(main), str(dst_note))
            text = dst_note.read_text(encoding="utf-8")
            text = normalize_note_links(text, entry)
            text = remove_big_resource_links(text)
            text = add_local_video_reference(text, meta)
            text = replace_frontmatter(text, meta)
            dst_note.write_text(text, encoding="utf-8")
            dst_resources.mkdir(parents=True, exist_ok=True)
            meta_out = dict(meta)
            meta_out["_note_path"] = str(dst_note)
            (dst_resources / "meta.json").write_text(json.dumps(meta_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            for archive in archives:
                dst_resources.mkdir(parents=True, exist_ok=True)
                archive_target = dst_resources / "普通总结归档.md"
                shutil.move(str(archive), str(archive_target))
                archive_text = normalize_note_links(archive_target.read_text(encoding="utf-8"), entry)
                archive_target.write_text(archive_text, encoding="utf-8")

    manifest = write_delete_manifest(dst_root, delete_candidates, tasks_big_files(), apply)
    print(f"\ndelete_manifest={manifest}")
    print("No large files were deleted.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate old Obsidian Inbox content into 00_资料库.")
    parser.add_argument("--apply", action="store_true", help="Perform migration. Default is dry-run only.")
    args = parser.parse_args()
    migrate(args.apply)


if __name__ == "__main__":
    main()
