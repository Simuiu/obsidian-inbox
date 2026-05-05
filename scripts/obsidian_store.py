from __future__ import annotations

import re
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from v2o_common import safe_filename


GENERIC_TAGS = {"内容入库", "资料库", "AI总结", "视频笔记", "深度笔记", "第二大脑"}
RESOURCE_FOLDER_NAME = "_resources"


def vault_path(config: dict[str, Any]) -> Path:
    return Path(config["obsidian"]["vault_path"]).expanduser()


def note_dir(config: dict[str, Any]) -> Path:
    return vault_path(config) / config["obsidian"]["note_folder"]


def resource_root(config: dict[str, Any]) -> Path:
    folder = config["obsidian"].get("resource_folder") or config["obsidian"].get("raw_folder")
    return vault_path(config) / folder


def topic_dir(config: dict[str, Any]) -> Path:
    return note_dir(config)


def purpose_dir(config: dict[str, Any]) -> Path:
    return note_dir(config)


def index_path(config: dict[str, Any]) -> Path:
    return vault_path(config) / config["obsidian"].get("index_file", "00_资料库/资料库索引.md")


def source_id(meta: dict[str, Any]) -> str:
    value = str(meta.get("video_id") or meta.get("id") or "").strip()
    if value:
        return safe_filename(value, max_len=80)
    parsed = urlparse(str(meta.get("source_url") or ""))
    host = parsed.netloc.replace("www.", "") or "web"
    slug = re.sub(r"[^a-zA-Z0-9]+", "", parsed.path)[-8:] or "link"
    return safe_filename(f"{host}-{slug}", max_len=80)


def entry_key(meta: dict[str, Any]) -> str:
    return "-".join(
        [
            str(meta.get("created_at") or ""),
            str(meta.get("platform") or "web"),
            source_id(meta),
        ]
    )


def short_title(title: str, max_len: int = 48) -> str:
    title = re.sub(r"https?://\S+", "", title)
    parts = [part.strip() for part in re.split(r"[｜|]", title) if part.strip()]
    if parts and len(parts[0]) >= 8:
        title = parts[0]
    title = title.replace("｜", " ").replace("|", " ")
    title = re.sub(r"[#*_`~\[\]\(\){}]", "", title)
    title = safe_filename(title, max_len=max_len)
    title = re.sub(r"\s+", " ", title).strip()
    return title or "未命名内容"


def compact_date(value: str) -> str:
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) >= 8:
        return digits[2:8]
    if len(digits) == 6:
        return digits
    return digits or "000000"


def entry_folder_name(meta: dict[str, Any]) -> str:
    return f"{compact_date(str(meta.get('created_at') or ''))} {short_title(str(meta.get('title') or '未命名内容'))}"


def note_filename(meta: dict[str, Any], mode: str = "standard") -> str:
    return f"{entry_folder_name(meta)}.md"


def note_path_for(config: dict[str, Any], meta: dict[str, Any], mode: str = "standard") -> Path:
    folder = note_dir(config) / entry_folder_name(meta)
    return folder / note_filename(meta, mode)


def resource_dir_for(config: dict[str, Any], meta: dict[str, Any]) -> Path:
    return note_path_for(config, meta).parent / RESOURCE_FOLDER_NAME


def obsidian_rel_link(from_file: Path, target: Path) -> str:
    rel = target.relative_to(from_file.parent) if target.is_relative_to(from_file.parent) else target
    return rel.as_posix()


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    front = text[4:end].splitlines()
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in front:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip().strip('"'))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            if value == "":
                data[current_key] = []
            else:
                data[current_key] = value.strip('"')
    return data


def markdown_link(label: str, target: Path, from_file: Path) -> str:
    rel = Path(os.path.relpath(target, from_file.parent))
    return f"[{label}]({rel.as_posix()})"
