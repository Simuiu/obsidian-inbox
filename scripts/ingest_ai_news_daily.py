#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v2o_common import load_config, safe_filename


ROOT = Path(__file__).resolve().parents[1]
FEED_BASE = "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main"
FEEDS = {
    "x": f"{FEED_BASE}/feed-x.json",
    "blogs": f"{FEED_BASE}/feed-blogs.json",
    "podcasts": f"{FEED_BASE}/feed-podcasts.json",
    "sources": f"{FEED_BASE}/config/default-sources.json",
}


@dataclass
class NewsItem:
    category: str
    source_name: str
    title: str
    url: str
    published_at: str
    excerpt: str
    score: int = 0


def fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "obsidian-inbox-ai-news/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def now_local() -> datetime:
    return datetime.now().astimezone()


def compact_date(dt: datetime) -> str:
    return dt.strftime("%y%m%d")


def today_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def vault_note_root() -> Path:
    config = load_config()
    return Path(config["obsidian"]["vault_path"]).expanduser() / config["obsidian"]["note_folder"]


def clean_text(value: str, max_len: int = 420) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def parse_datetime(value: str) -> str:
    if not value:
        return ""
    raw = str(value)
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return parsed.astimezone().strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return raw


def flatten_x(feed: dict[str, Any], limit: int) -> list[NewsItem]:
    relevance_terms = [
        "ai",
        "agent",
        "agents",
        "model",
        "models",
        "llm",
        "claude",
        "openai",
        "anthropic",
        "codex",
        "inference",
        "compute",
        "eval",
        "evals",
        "context",
        "workflow",
        "automation",
        "mcp",
        "reasoning",
        "token",
        "tokens",
        "prompt",
        "gpu",
        "cursor",
        "devin",
        "software",
        "coding",
        "developer",
        "knowledge work",
    ]
    low_signal_terms = [
        "what if we name",
        "happy mother",
        "mother's day",
        "calisthenics",
        "sign up for free",
        "newsletter",
    ]
    items: list[NewsItem] = []
    for account in feed.get("x", []):
        name = account.get("name") or account.get("handle") or "X"
        handle = account.get("handle") or ""
        for tweet in account.get("tweets", []):
            text = clean_text(tweet.get("text") or "")
            if not text:
                continue
            lowered = text.lower()
            tokens = set(re.findall(r"[a-z0-9]+", lowered))
            phrase_matches = {"knowledge work"}
            exact_terms = set(relevance_terms) - phrase_matches
            if not (tokens.intersection(exact_terms) or any(term in lowered for term in phrase_matches)):
                continue
            if any(term in lowered for term in low_signal_terms):
                continue
            score = int(tweet.get("likes") or 0) + int(tweet.get("retweets") or 0) * 2 + int(tweet.get("replies") or 0)
            items.append(
                NewsItem(
                    category="X / Builders",
                    source_name=f"{name} (@{handle})" if handle else name,
                    title=text[:72],
                    url=tweet.get("url") or "",
                    published_at=parse_datetime(tweet.get("createdAt") or ""),
                    excerpt=text,
                    score=score,
                )
            )
    return sorted(items, key=lambda item: item.score, reverse=True)[:limit]


def flatten_blogs(feed: dict[str, Any], limit: int) -> list[NewsItem]:
    items: list[NewsItem] = []
    for post in feed.get("blogs", []):
        title = clean_text(post.get("title") or "Untitled", 140)
        excerpt = clean_text(post.get("description") or post.get("content") or "", 520)
        items.append(
            NewsItem(
                category="Official / Engineering Blogs",
                source_name=post.get("name") or post.get("author") or "Blog",
                title=title,
                url=post.get("url") or "",
                published_at=parse_datetime(post.get("publishedAt") or ""),
                excerpt=excerpt,
            )
        )
    return items[:limit]


def flatten_podcasts(feed: dict[str, Any], limit: int) -> list[NewsItem]:
    items: list[NewsItem] = []
    for episode in feed.get("podcasts", []):
        title = clean_text(episode.get("title") or "Untitled", 140)
        excerpt = clean_text(episode.get("transcript") or episode.get("description") or "", 520)
        items.append(
            NewsItem(
                category="Podcasts / Long-form",
                source_name=episode.get("name") or "Podcast",
                title=title,
                url=episode.get("url") or "",
                published_at=parse_datetime(episode.get("publishedAt") or ""),
                excerpt=excerpt,
            )
        )
    return items[:limit]


def render_item(item: NewsItem) -> list[str]:
    lines = [f"### {item.title}", ""]
    meta = [f"来源：{item.source_name}"]
    if item.published_at:
        meta.append(f"时间：{item.published_at}")
    if item.score:
        meta.append(f"热度分：{item.score}")
    lines.extend([f"- {'；'.join(meta)}"])
    if item.url:
        lines.append(f"- 链接：{item.url}")
    if item.excerpt:
        lines.extend(["", item.excerpt])
    lines.append("")
    return lines


def render_note(
    generated_at: str,
    x_items: list[NewsItem],
    blog_items: list[NewsItem],
    podcast_items: list[NewsItem],
    resource_rel: str,
    now: datetime,
) -> str:
    title = f"{today_iso(now)} AI 一手信息日报"
    all_items = x_items + blog_items + podcast_items
    lines = [
        "---",
        f'title: "{title}"',
        f'source: "{FEED_BASE}"',
        'type: "daily_news"',
        'platform: "github"',
        'author: "zarazhangrui/follow-builders"',
        f'published_at: "{generated_at}"',
        f'created_at: "{today_iso(now)}"',
        'status: "已入库"',
        'summary_mode: "普通"',
        f'entry_id: "{compact_date(now)}-ai-news-follow-builders"',
        f'resource_dir: "{resource_rel}"',
        "purposes:",
        "  - 学习",
        "  - 素材",
        "tags:",
        "  - AI新闻",
        "  - 一手信息",
        "  - follow-builders",
        "---",
        "",
        f"# {title}",
        "",
        "## 索引与主题",
        "",
        "- 总结模式：普通",
        "- 总索引：[[00_资料库/000 资料库索引/000 资料库索引|总索引]]",
        "- 主题：[[AI新闻]]、[[AI工具]]、[[AI Agent]]",
        "- 用途：[[00_资料库/002 用途索引/002 用途索引#学习|学习]]、[[00_资料库/002 用途索引/002 用途索引#素材|素材]]",
        "",
        "## 今日概览",
        "",
        f"- 数据源：`zarazhangrui/follow-builders` central feeds",
        f"- Feed 生成时间：{generated_at or '未知'}",
        f"- 入库时间：{now.strftime('%Y-%m-%d %H:%M %Z')}",
        f"- 条目数量：X {len(x_items)} 条；官方/工程博客 {len(blog_items)} 条；播客 {len(podcast_items)} 条。",
        "",
        "## 快速判断",
        "",
    ]
    if all_items:
        lines.extend(
            [
                "- 这份日报偏“一手来源摘录”，不是二手新闻摘要。",
                "- 优先看官方工程博客和高热度 builder 动态，再决定是否深读原文。",
                "- 如果某条内容值得深入，再单独用 Obsidian Inbox 对原文或视频做深度入库。",
            ]
        )
    else:
        lines.append("- 今天没有成功抓到新条目；请查看 `_resources` 里的原始 feed 或错误日志。")

    sections = [
        ("X / Builders", x_items),
        ("Official / Engineering Blogs", blog_items),
        ("Podcasts / Long-form", podcast_items),
    ]
    for heading, items in sections:
        lines.extend(["", f"## {heading}", ""])
        if not items:
            lines.append("- 今日未抓到可记录条目。")
            continue
        for item in items:
            lines.extend(render_item(item))

    lines.extend(
        [
            "## 原始材料",
            "",
            f"- 资源目录：`{resource_rel}`",
            "- `feed-x.json`",
            "- `feed-blogs.json`",
            "- `feed-podcasts.json`",
            "- `default-sources.json`",
            "",
            "## 后续动作",
            "",
            "- 挑 1-3 条值得深读的官方博客或视频，单独入库。",
            "- 如果连续几天某个主题反复出现，可整理成主题笔记。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch zarazhangrui/follow-builders feeds into Obsidian.")
    parser.add_argument("--x-limit", type=int, default=12)
    parser.add_argument("--blog-limit", type=int, default=8)
    parser.add_argument("--podcast-limit", type=int, default=5)
    parser.add_argument("--no-rebuild-index", action="store_true")
    args = parser.parse_args()

    now = now_local()
    folder_name = f"{compact_date(now)} AI 一手信息日报"
    note_root = vault_note_root()
    entry_dir = note_root / folder_name
    resource_dir = entry_dir / "_resources"
    entry_dir.mkdir(parents=True, exist_ok=True)
    resource_dir.mkdir(parents=True, exist_ok=True)

    fetched: dict[str, dict[str, Any]] = {}
    errors: dict[str, str] = {}
    for key, url in FEEDS.items():
        try:
            fetched[key] = fetch_json(url)
            write_json(resource_dir / f"{key}.json", fetched[key])
        except Exception as exc:  # noqa: BLE001
            errors[key] = str(exc)

    if "x" in fetched:
        shutil.copy2(resource_dir / "x.json", resource_dir / "feed-x.json")
    if "blogs" in fetched:
        shutil.copy2(resource_dir / "blogs.json", resource_dir / "feed-blogs.json")
    if "podcasts" in fetched:
        shutil.copy2(resource_dir / "podcasts.json", resource_dir / "feed-podcasts.json")
    if "sources" in fetched:
        shutil.copy2(resource_dir / "sources.json", resource_dir / "default-sources.json")
    if errors:
        write_json(resource_dir / "fetch-errors.json", errors)

    generated_at = (
        fetched.get("x", {}).get("generatedAt")
        or fetched.get("blogs", {}).get("generatedAt")
        or fetched.get("podcasts", {}).get("generatedAt")
        or ""
    )
    x_items = flatten_x(fetched.get("x", {}), args.x_limit)
    blog_items = flatten_blogs(fetched.get("blogs", {}), args.blog_limit)
    podcast_items = flatten_podcasts(fetched.get("podcasts", {}), args.podcast_limit)
    resource_rel = str(resource_dir.relative_to(note_root.parent))
    note_text = render_note(generated_at, x_items, blog_items, podcast_items, resource_rel, now)
    note_path = entry_dir / f"{folder_name}.md"
    note_path.write_text(note_text, encoding="utf-8")

    if not args.no_rebuild_index:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/rebuild_obsidian_index.py")],
            cwd=str(ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if result.returncode != 0:
            print(result.stdout, file=sys.stderr)
            return result.returncode

    print(note_path)
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
