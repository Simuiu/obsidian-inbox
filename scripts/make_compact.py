from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


KEYWORDS = [
    "Transformer",
    "GPT",
    "提示词",
    "微调",
    "RAG",
    "Function",
    "MCP",
    "agent",
    "Agent",
    "上下文",
    "skill",
    "Skill",
    "Open",
    "Harness",
    "驾驭",
]


def read_meta(task_dir: Path) -> dict:
    return json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))


def parse_timed(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = re.match(r"\[(\d\d:\d\d:\d\d|\d\d:\d\d)\.\d+\]\s*(.+)", line.strip())
        if match:
            rows.append((match.group(1), match.group(2)))
    return rows


def minute_value(ts: str) -> int:
    parts = [int(p) for p in ts.split(":")]
    if len(parts) == 2:
        return parts[0]
    return parts[0] * 60 + parts[1]


def build_segments(rows: list[tuple[str, str]], window_minutes: int = 5) -> list[tuple[str, str, str]]:
    buckets: dict[int, list[str]] = {}
    for ts, line in rows:
        bucket = minute_value(ts) // window_minutes
        buckets.setdefault(bucket, []).append(line)
    segments: list[tuple[str, str, str]] = []
    for bucket in sorted(buckets):
        start = bucket * window_minutes
        end = start + window_minutes
        text = "".join(buckets[bucket])
        excerpt = text[:700]
        segments.append((f"{start:02d}:00-{end:02d}:00", excerpt, text))
    return segments


def keyword_hits(rows: list[tuple[str, str]], limit: int = 80) -> list[str]:
    hits: list[str] = []
    for ts, line in rows:
        if any(k.lower() in line.lower() for k in KEYWORDS):
            hits.append(f"[{ts}] {line}")
        if len(hits) >= limit:
            break
    return hits


def article_segments(text: str, window_chars: int = 900) -> list[tuple[str, str]]:
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    segments: list[tuple[str, str]] = []
    current: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        if current and current_len + len(paragraph) > window_chars:
            segments.append((f"片段 {len(segments) + 1}", "\n\n".join(current)))
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += len(paragraph)
    if current:
        segments.append((f"片段 {len(segments) + 1}", "\n\n".join(current)))
    return segments


def standard_output_requirements() -> list[str]:
    return [
        "- 基于 compact 内容生成 Obsidian 笔记。",
        "- 不要读取完整字幕，除非 compact 信息明显不足。",
        "- 不要编造字幕没有的信息。",
        "- 主笔记保留摘要、重点、时间点、可实践行动和后续可追问问题。",
        "- 原始材料只链接到 _resources 文件，不要把完整转写或原文塞入主笔记。",
    ]


def deep_output_requirements() -> list[str]:
    return [
        "- 基于 compact 内容生成深度 Obsidian Markdown 笔记。",
        "- 深度模式不能只是普通笔记的加长版，必须产出可复习、可迁移、可追问的教学型笔记。",
        "- 目标是教学重构，不是字幕流水账：按“问题链 -> 方案演化 -> 机制拆解 -> 设计取舍 -> 实践路径”组织。",
        "- 必须显式写出：这个内容在解决什么问题、为什么旧方案不够、每一层新抽象解决了什么、代价是什么。",
        "- 必须包含“概念地图”“问题链推导”“关键机制拆解”“对比表”“常见误区”“设计取舍”“实践路径”“二次加工卡片”。",
        "- 对比表要用于区分容易混淆的概念、方案、协议或实现路径。",
        "- 二次加工卡片要写成可直接沉淀进 Obsidian 的原子化知识卡片，不是简单摘抄。",
        "- 优先保留视频中的真实概念、论证、术语、案例、代码、公式、限制和实践建议，并把它们放进上述结构。",
        "- 可以比普通入库明显更长，但不要把完整转写塞入主笔记。",
        "- 不要编造 compact 或原始材料中没有的信息；如果 compact 不足以支撑深度总结，明确写出信息限制。",
        "- 原始材料只链接到 _resources 文件。",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build compact context for Codex.")
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--mode", choices=["standard", "deep"], default="standard")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    task_dir = args.task_dir
    meta = read_meta(task_dir)
    timed_path = task_dir / "transcript_timed.md"
    content_path = task_dir / "content.md"
    rows: list[tuple[str, str]] = []
    article_text = ""
    if timed_path.exists():
        rows = parse_timed(timed_path.read_text(encoding="utf-8"))
        segments = build_segments(rows)
        hits = keyword_hits(rows)
        section_title = "主题分段候选"
    elif content_path.exists():
        article_text = content_path.read_text(encoding="utf-8")
        segments = [(label, excerpt, excerpt) for label, excerpt in article_segments(article_text)]
        hits = [line for line in article_text.splitlines() if any(k.lower() in line.lower() for k in KEYWORDS)][:80]
        section_title = "正文分段候选"
    else:
        segments = []
        hits = []
        section_title = "内容分段候选"

    lines = [
        "# Compact Context",
        "",
        "## 元信息",
        "",
        f"- 标题：{meta.get('title', '')}",
        f"- 平台：{meta.get('platform', '')}",
        f"- 作者：{meta.get('author', '')}",
        f"- 发布时间：{meta.get('published_at', '')}",
        f"- 时长：{meta.get('duration', '')}",
        f"- 链接：{meta.get('source_url', '')}",
        "",
        f"## {section_title}",
        "",
    ]
    for label, excerpt, _ in segments:
        lines.append(f"### {label}")
        lines.append("")
        lines.append(excerpt)
        lines.append("")

    lines.extend(["## 关键词命中摘录", ""])
    lines.extend(hits)
    lines.extend(["", "## 给 Codex 的输出要求", ""])
    if args.mode == "deep":
        lines.extend(deep_output_requirements())
    else:
        lines.extend(standard_output_requirements())

    output = args.output or task_dir / "compact.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
