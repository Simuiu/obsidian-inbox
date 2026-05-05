from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from obsidian_store import index_path, note_path_for, resource_dir_for
from v2o_common import load_config


def yaml_scalar(value: Any) -> str:
    text = str(value or "").replace('"', '\\"')
    return f'"{text}"'


def list_block(values: list[str]) -> list[str]:
    if not values:
        return []
    return [f"  - {value}" for value in values]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compact_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def excerpt_from_section(section: str, max_items: int = 6) -> list[str]:
    lines = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line or line.startswith("### "):
            continue
        if line.startswith("!["):
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        if len(line) > 220:
            line = line[:220].rstrip() + "..."
        if line:
            lines.append(line)
        if len(lines) >= max_items:
            break
    return lines


def relative_link(from_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target, from_file.parent)).as_posix()


def resource_links(note_path: Path, resource_dir: Path) -> list[str]:
    if not resource_dir.exists():
        return []
    links = []
    for path in sorted(resource_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = relative_link(note_path, path)
        label = path.relative_to(resource_dir).as_posix()
        links.append(f"- [{label}]({rel})")
    return links


def wiki_path_from_vault(config: dict[str, Any], path: Path) -> str:
    vault = Path(config["obsidian"]["vault_path"]).expanduser()
    try:
        rel = path.relative_to(vault)
    except ValueError:
        rel = path
    return rel.with_suffix("").as_posix() if rel.suffix == ".md" else rel.as_posix()


def summary_mode_label(mode: str) -> str:
    return "深度" if mode == "deep" else "普通"


def infer_tags(meta: dict[str, Any], mode: str) -> list[str]:
    tags = ["内容入库", "AI总结"]
    platform = str(meta.get("platform") or "")
    if meta.get("content_type") == "video" or platform in {"bilibili", "youtube", "wechat_video", "local_video"}:
        tags.append("视频笔记")
    if mode == "deep":
        tags.append("深度笔记")
    return tags


def frontmatter(meta: dict[str, Any], resource_rel: str, status: str, mode: str) -> str:
    purposes = meta.get("purposes") if isinstance(meta.get("purposes"), list) else ["学习"]
    tags = infer_tags(meta, mode)
    lines = [
        "---",
        f"title: {yaml_scalar(meta.get('title'))}",
        f"source: {yaml_scalar(meta.get('source_url'))}",
        f"type: {yaml_scalar(meta.get('content_type') or meta.get('type'))}",
        f"platform: {yaml_scalar(meta.get('platform'))}",
        f"author: {yaml_scalar(meta.get('author'))}",
        f"published_at: {yaml_scalar(meta.get('published_at'))}",
        f"created_at: {yaml_scalar(meta.get('created_at'))}",
        f"status: {yaml_scalar(status)}",
        f"summary_mode: {yaml_scalar(summary_mode_label(mode))}",
        f"entry_id: {yaml_scalar(meta.get('entry_key'))}",
        f"resource_dir: {yaml_scalar(resource_rel)}",
        "purposes:",
        *list_block([str(item) for item in purposes]),
        "tags:",
        *list_block(tags),
        "---",
    ]
    return "\n".join(lines)


def render_standard(meta: dict[str, Any], compact: dict[str, str], note_path: Path, resource_dir: Path, config: dict[str, Any]) -> str:
    segment_items = excerpt_from_section(compact.get("正文分段候选") or compact.get("主题分段候选") or "", max_items=8)
    keyword_items = excerpt_from_section(compact.get("关键词命中摘录", ""), max_items=8)
    resource_rel = relative_link(note_path, resource_dir)
    idx = index_path(config)
    lines = [
        frontmatter(meta, resource_rel, "待润色", "standard"),
        "",
        "## 索引与主题",
        "",
        "- 总结模式：普通",
        f"- 总索引：[[{wiki_path_from_vault(config, idx)}|总索引]]",
        "- 用途：[[00_资料库/002 用途索引/002 用途索引#学习|学习]]",
        "",
        "## 一句话总结",
        "",
        "> 自动草稿：请基于 compact 内容继续润色，不要把这句话当作最终总结。",
        "",
        "## 重点速览",
        "",
    ]
    lines.extend([f"- {item}" for item in segment_items[:5]] or ["- 待根据正文或转写补充。"])
    lines.extend(["", "## 核心内容", ""])
    lines.extend([f"- {item}" for item in segment_items] or ["- 当前任务包没有足够 compact 片段。"])
    lines.extend(["", "## 关键时间点 / 段落线索", ""])
    lines.extend([f"- {item}" for item in keyword_items] or ["- 暂无关键词命中。"])
    lines.extend(["", "## 值得实践的部分", "", "- 待从内容中提炼可操作步骤。"])
    lines.extend(["", "## 行动清单", "", "- 复核自动草稿。", "- 补充个人判断和实践计划。"])
    lines.extend(["", "## 后续可追问的问题", "", "- 这篇内容最值得迁移到哪个项目或流程？"])
    lines.extend(["", "## 原始材料", ""])
    lines.extend(resource_links(note_path, resource_dir) or [f"- 资源目录：`{resource_rel}`"])
    return "\n".join(lines).rstrip() + "\n"


def render_deep(meta: dict[str, Any], compact: dict[str, str], note_path: Path, resource_dir: Path, config: dict[str, Any]) -> str:
    base = render_standard(meta, compact, note_path, resource_dir, config)
    segment_items = excerpt_from_section(compact.get("正文分段候选") or compact.get("主题分段候选") or "", max_items=10)
    resource_rel = relative_link(note_path, resource_dir)
    idx = index_path(config)
    lines = [
        frontmatter(meta, resource_rel, "待深度润色", "deep"),
        "",
        "## 索引与主题",
        "",
        "- 总结模式：深度",
        f"- 总索引：[[{wiki_path_from_vault(config, idx)}|总索引]]",
        "- 用途：[[00_资料库/002 用途索引/002 用途索引#学习|学习]]、[[00_资料库/002 用途索引/002 用途索引#实践|实践]]",
        "",
        "## 核心结论",
        "",
        "> 自动深度草稿：这里先搭好深度笔记结构，最终结论需要继续由 Codex 或人工复核。",
        "",
        "## 这篇内容在解决什么问题",
        "",
        *[f"- {item}" for item in segment_items[:3]],
        "",
        "## 概念地图",
        "",
        "- 核心对象：待补充",
        "- 关键机制：待补充",
        "- 应用场景：待补充",
        "",
        "## 问题链推导",
        "",
        "- 原问题是什么？",
        "- 旧方案为什么不够？",
        "- 新方案解决了哪一层问题？",
        "",
        "## 关键机制拆解",
        "",
        *[f"- {item}" for item in segment_items[3:8]],
        "",
        "## 对比表",
        "",
        "| 对象 | 解决的问题 | 代价 | 适用场景 |",
        "|---|---|---|---|",
        "| 待补充 | 待补充 | 待补充 | 待补充 |",
        "",
        "## 常见误区",
        "",
        "- 待根据原文补充。",
        "",
        "## 设计取舍",
        "",
        "- 待根据原文补充。",
        "",
        "## 实践路径",
        "",
        "- 把原文中的步骤转成可复现流程。",
        "",
        "## 二次加工卡片",
        "",
        "- 卡片 1：待提炼。",
        "",
        "## 行动清单",
        "",
        "- 复核自动深度草稿。",
        "- 补充对比表、误区和实践路径。",
        "",
        "## 后续可追问的问题",
        "",
        "- 哪些部分可以迁移为自己的 SOP？",
        "",
        "## 原始材料",
        "",
        *(resource_links(note_path, resource_dir) or [f"- 资源目录：`{resource_rel}`"]),
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an editable Obsidian note draft from a task package.")
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--mode", choices=["standard", "deep"])
    parser.add_argument("--write", action="store_true", help="Write to the suggested Obsidian note path.")
    parser.add_argument("--output", type=Path, help="Write draft to a custom path.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing draft/note.")
    args = parser.parse_args()

    config = load_config()
    meta = read_json(args.task_dir / "meta.json")
    mode = args.mode or str(meta.get("mode") or "standard")
    compact_path = args.task_dir / "compact.md"
    if not compact_path.exists():
        raise SystemExit(f"compact.md not found: {compact_path}")
    compact = compact_sections(compact_path.read_text(encoding="utf-8"))
    note_path = args.output or note_path_for(config, meta, mode)
    resource_dir = resource_dir_for(config, meta)
    text = render_deep(meta, compact, note_path, resource_dir, config) if mode == "deep" else render_standard(meta, compact, note_path, resource_dir, config)

    if args.write or args.output:
        if note_path.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite existing note: {note_path}. Use --force to overwrite.")
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(text, encoding="utf-8")
        print(note_path)
    else:
        print(text)


if __name__ == "__main__":
    main()
