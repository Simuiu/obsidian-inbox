from __future__ import annotations

raise SystemExit("migrate_obsidian_inbox.py is deprecated. Use scripts/migrate_obsidian_library.py for the 00_资料库 structure.")

import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

from obsidian_store import (
    GENERIC_TAGS,
    entry_key,
    note_dir,
    note_filename,
    parse_frontmatter,
    resource_dir_for,
)
from v2o_common import load_config


def source_id_from_url(source: str) -> str:
    match = re.search(r"(BV[0-9A-Za-z]+)", source)
    if match:
        return match.group(1)
    parsed = urlparse(source)
    if "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:
        query_match = re.search(r"[?&]v=([^&]+)", source)
        if query_match:
            return query_match.group(1)
        return parsed.path.strip("/").split("/")[-1]
    return ""


def meta_from_note(path: Path) -> dict:
    meta = parse_frontmatter(path)
    source = str(meta.get("source") or "")
    video_id = source_id_from_url(source)
    if video_id:
        meta["video_id"] = video_id
    meta.setdefault("platform", "web")
    meta.setdefault("created_at", path.name[:10])
    meta.setdefault("title", path.stem[11:])
    return meta


def mode_from_note(path: Path, meta: dict) -> str:
    status = str(meta.get("status") or "")
    if "深度" in status or "深度" in path.stem:
        return "deep"
    return "standard"


def add_frontmatter_field(text: str, key: str, value: str) -> str:
    if re.search(rf"(?m)^{re.escape(key)}:", text):
        return re.sub(rf"(?m)^{re.escape(key)}:.*$", f'{key}: "{value}"', text)
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    return text[:end] + f'\n{key}: "{value}"' + text[end:]


def add_frontmatter_list(text: str, key: str, values: list[str]) -> str:
    block = "\n".join([f"{key}:"] + [f"  - {value}" for value in values])
    if re.search(rf"(?m)^{re.escape(key)}:", text):
        return re.sub(rf"(?ms)^{re.escape(key)}:\n(?:  - .+\n?)*", block + "\n", text)
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    return text[:end] + "\n" + block + text[end:]


def note_topics(meta: dict) -> list[str]:
    tags = meta.get("tags") or []
    if not isinstance(tags, list):
        return []
    return [tag for tag in tags if tag and tag not in GENERIC_TAGS]


def upsert_index_section(text: str, meta: dict, topics: list[str], purposes: list[str]) -> str:
    topic_links = "、".join(f"[[_topics/{topic}|{topic}]]" for topic in topics) or "待分类"
    purpose_links = "、".join(f"[[_purposes/{purpose}|{purpose}]]" for purpose in purposes) or "待定"
    section = "\n".join(
        [
            "## 索引与主题",
            "",
            "- 总索引：[[内容入库索引]]",
            f"- 主题：{topic_links}",
            f"- 用途：{purpose_links}",
            "",
        ]
    )
    text = re.sub(r"\n## 索引与主题\n.*?(?=\n## |\Z)", "\n" + section, text, flags=re.S)
    if "## 索引与主题" in text:
        return text
    match = re.search(r"(?m)^# .+\n", text)
    if not match:
        return section + "\n" + text
    return text[: match.end()] + "\n" + section + text[match.end() :]


def migrate_raw(config: dict, meta: dict, old_raw: Path) -> None:
    rid = str(meta.get("video_id") or "")
    if not rid:
        return
    created = str(meta.get("created_at"))
    platform = str(meta.get("platform"))
    prefix = f"{created}-{platform}-{rid}-"
    target_dir = resource_dir_for(config, meta)
    target_dir.mkdir(parents=True, exist_ok=True)
    if not old_raw.exists():
        return
    for src in old_raw.glob(prefix + "*"):
        dst = target_dir / src.name.removeprefix(prefix)
        if dst.exists():
            src.unlink()
        else:
            shutil.move(str(src), str(dst))


def update_resource_links(text: str, meta: dict) -> str:
    rid = str(meta.get("video_id") or "")
    if not rid:
        return text
    created = str(meta.get("created_at"))
    platform = str(meta.get("platform"))
    key = entry_key(meta)
    prefix = f"{created}-{platform}-{rid}-"
    text = text.replace(f"./_raw/{prefix}", f"./_resources/{key}/")
    text = text.replace(f"_raw/{prefix}", f"_resources/{key}/")
    return text


def unique_target(target: Path, current: Path) -> Path:
    if target == current or not target.exists():
        return target
    index = 2
    while True:
        candidate = target.with_name(f"{target.stem} {index}{target.suffix}")
        if candidate == current or not candidate.exists():
            return candidate
        index += 1


def main() -> None:
    config = load_config()
    root = note_dir(config)
    old_raw = root / "_raw"
    note_paths = [path for path in sorted(root.glob("*.md")) if path.name != "内容入库索引.md"]
    metas = {path: meta_from_note(path) for path in note_paths}
    topics_by_entry: dict[str, list[str]] = {}
    for meta in metas.values():
        if not meta.get("source"):
            continue
        key = entry_key(meta)
        topics_by_entry.setdefault(key, [])
        for topic in note_topics(meta):
            if topic not in topics_by_entry[key]:
                topics_by_entry[key].append(topic)

    for path in note_paths:
        text = path.read_text(encoding="utf-8")
        meta = metas[path]
        if not meta.get("source"):
            continue
        key = entry_key(meta)
        migrate_raw(config, meta, old_raw)
        text = add_frontmatter_field(text, "entry_id", key)
        text = add_frontmatter_field(text, "resource_dir", f"_resources/{key}")
        if "purposes:" not in text:
            text = add_frontmatter_list(text, "purposes", ["学习", "实践"])
        text = update_resource_links(text, meta)
        text = upsert_index_section(text, meta, topics_by_entry.get(key) or note_topics(meta), ["学习", "实践"])
        path.write_text(text, encoding="utf-8")

        mode = mode_from_note(path, meta)
        target = unique_target(root / note_filename(meta, mode), path)
        if target != path:
            path.rename(target)
            print(f"{path.name} -> {target.name}")
        else:
            print(f"kept {path.name}")


if __name__ == "__main__":
    main()
