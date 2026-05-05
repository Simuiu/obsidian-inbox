from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from obsidian_store import GENERIC_TAGS, index_path, note_dir, parse_frontmatter
from v2o_common import load_config


INDEX_FILE_REL = Path("000 资料库索引/000 资料库索引.md")
TOPIC_INDEX_FILE_REL = Path("001 主题索引/001 主题索引.md")
PURPOSE_INDEX_FILE_REL = Path("002 用途索引/002 用途索引.md")
ROOT_INDEX_RELS = {
    INDEX_FILE_REL,
    TOPIC_INDEX_FILE_REL,
    PURPOSE_INDEX_FILE_REL,
    Path("00 资料库索引.md"),
    Path("01 主题索引.md"),
    Path("02 用途索引.md"),
    Path("资料库索引.md"),
    Path("主题索引.md"),
    Path("用途索引.md"),
}


@lru_cache(maxsize=1)
def vault_root() -> Path:
    config = load_config()
    return Path(config["obsidian"]["vault_path"]).expanduser()


def note_files(root: Path) -> list[Path]:
    notes: list[Path] = []
    for path in root.glob("*/*.md"):
        if "_resources" in path.parts:
            continue
        if path.relative_to(root) in ROOT_INDEX_RELS:
            continue
        if path.parent.name.startswith("_"):
            continue
        notes.append(path)
    return sorted(notes)


def display_title(path: Path, meta: dict) -> str:
    return str(meta.get("title") or path.stem)


def note_status(meta: dict) -> str:
    return str(meta.get("status") or "未标记")


def summary_mode(meta: dict) -> str:
    explicit = str(meta.get("summary_mode") or "").strip()
    if explicit:
        return explicit
    mode = str(meta.get("mode") or "").strip()
    if mode == "deep":
        return "深度"
    status = str(meta.get("status") or "")
    tags = meta.get("tags") or []
    if "深度" in status or (isinstance(tags, list) and "深度笔记" in tags):
        return "深度"
    return "普通"


def content_type(meta: dict) -> str:
    platform = str(meta.get("platform") or "web")
    ctype = str(meta.get("type") or meta.get("content_type") or "")
    if ctype:
        return ctype
    if platform in {"bilibili", "youtube", "douyin", "wechat_video", "local_video"}:
        return "video"
    if platform in {"wechat", "xiaohongshu", "web"}:
        return "article"
    return "content"


def topic_tags(meta: dict) -> list[str]:
    tags = meta.get("tags") or []
    if not isinstance(tags, list):
        return []
    return [tag for tag in tags if tag and tag not in GENERIC_TAGS]


def purposes(meta: dict) -> list[str]:
    values = meta.get("purposes") or []
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, list):
        return []
    return [str(value) for value in values if str(value).strip()]


def source_line(meta: dict) -> str:
    local_path = str(meta.get("local_video_path") or "")
    source = str(meta.get("source") or meta.get("source_url") or "")
    if local_path:
        return f"原视频：`{local_path}`"
    if source.startswith(("http://", "https://")):
        return f"来源：[打开链接]({source})"
    if source:
        return f"来源：`{source}`"
    return ""


def transcript_link(path: Path) -> str:
    resource_dir = path.parent / "_resources"
    for name in ["转写.md", "带时间点转写.md", "content.md"]:
        target = resource_dir / name
        if target.exists():
            return wiki_link(name.removesuffix(".md"), target)
    return ""


def wiki_link(label: str, target: Path) -> str:
    try:
        rel = target.relative_to(vault_root())
    except ValueError:
        rel = target
    rel_no_ext = rel.with_suffix("") if rel.suffix == ".md" else rel
    return f"[[{rel_no_ext.as_posix()}|{label}]]"


def note_item(path: Path, meta: dict) -> list[str]:
    title = wiki_link(display_title(path, meta), path)
    details = [
        f"日期：{meta.get('created_at', '')}",
        f"平台：{meta.get('platform', '')}",
        f"总结模式：{summary_mode(meta)}",
        f"状态：{note_status(meta)}",
    ]
    transcript = transcript_link(path)
    if transcript:
        details.append(f"转写/正文：{transcript}")
    source = source_line(meta)
    if source:
        details.append(source)
    return [f"- {title}", f"  - {'；'.join(details)}"]


def sorted_notes(paths: list[Path], metas: dict[Path, dict]) -> list[Path]:
    return sorted(paths, key=lambda item: (str(metas[item].get("created_at") or ""), item.parent.name), reverse=True)


def render_note_list(paths: list[Path], metas: dict[Path, dict]) -> list[str]:
    lines: list[str] = []
    for path in sorted_notes(paths, metas):
        lines.extend(note_item(path, metas[path]))
    return lines


def render_index(notes: list[Path], metas: dict[Path, dict], output: Path, topic_file: Path, purpose_file: Path) -> str:
    by_type: dict[str, list[Path]] = defaultdict(list)
    for path in notes:
        by_type[content_type(metas[path])].append(path)

    lines = [
        "# 资料库索引",
        "",
        "这里是资料库总入口。每一行对应一个资源，优先进入主总结；需要复核时再打开转写、正文或来源。",
        "",
        "## 快速入口",
        "",
        f"- {wiki_link('主题索引', topic_file)}",
        f"- {wiki_link('用途索引', purpose_file)}",
        "",
        "## 最近入库",
        "",
        *render_note_list(notes, metas),
        "",
        "## 按类型",
        "",
    ]
    for ctype in sorted(by_type):
        lines.extend([f"### {ctype}", "", *render_note_list(by_type[ctype], metas), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_topic_index(notes: list[Path], metas: dict[Path, dict], output: Path, idx: Path) -> str:
    by_topic: dict[str, list[Path]] = defaultdict(list)
    for path, meta in metas.items():
        for tag in topic_tags(meta):
            by_topic[tag].append(path)
    lines = ["# 主题索引", "", f"- 返回：{wiki_link('资料库索引', idx)}", ""]
    for topic in sorted(by_topic):
        lines.extend([f"## {topic}", "", *render_note_list(by_topic[topic], metas), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_purpose_index(notes: list[Path], metas: dict[Path, dict], output: Path, idx: Path) -> str:
    by_purpose: dict[str, list[Path]] = defaultdict(list)
    for path, meta in metas.items():
        for purpose in purposes(meta):
            by_purpose[purpose].append(path)
    lines = ["# 用途索引", "", f"- 返回：{wiki_link('资料库索引', idx)}", ""]
    for purpose in sorted(by_purpose):
        lines.extend([f"## {purpose}", "", *render_note_list(by_purpose[purpose], metas), ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    config = load_config()
    root = note_dir(config)
    root.mkdir(parents=True, exist_ok=True)
    idx = index_path(config)
    topic_file = root / TOPIC_INDEX_FILE_REL
    purpose_file = root / PURPOSE_INDEX_FILE_REL
    notes = note_files(root)
    metas = {path: parse_frontmatter(path) for path in notes}

    idx.parent.mkdir(parents=True, exist_ok=True)
    topic_file.parent.mkdir(parents=True, exist_ok=True)
    purpose_file.parent.mkdir(parents=True, exist_ok=True)

    idx.write_text(render_index(notes, metas, idx, topic_file, purpose_file), encoding="utf-8")
    topic_file.write_text(render_topic_index(notes, metas, topic_file, idx), encoding="utf-8")
    purpose_file.write_text(render_purpose_index(notes, metas, purpose_file, idx), encoding="utf-8")

    print(idx)
    print(topic_file)
    print(purpose_file)


if __name__ == "__main__":
    main()
