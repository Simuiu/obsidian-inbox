from __future__ import annotations

import argparse
import html
import json
import re
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)


def fetch_bytes(url: str, timeout: int = 30, referer: str = "") -> tuple[bytes, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            **({"Referer": referer} if referer else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(), response.headers.get("Content-Type", "")


def fetch_html(url: str, timeout: int = 30) -> str:
    try:
        data, _ = fetch_bytes(url, timeout=timeout)
        return data.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:300]}") from exc


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def meta_content(source: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, source, flags=re.S | re.I)
        if match:
            return html.unescape(match.group(1)).strip()
    return ""


class ElementExtractor(HTMLParser):
    def __init__(self, target_id: str):
        super().__init__(convert_charrefs=False)
        self.target_id = target_id
        self.capturing = False
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if not self.capturing and attrs_dict.get("id") == self.target_id:
            self.capturing = True
            self.depth = 1
            self.parts.append(self.get_starttag_text() or "")
            return
        if self.capturing:
            self.depth += 1
            self.parts.append(self.get_starttag_text() or "")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.capturing:
            self.parts.append(self.get_starttag_text() or "")

    def handle_endtag(self, tag: str) -> None:
        if not self.capturing:
            return
        self.parts.append(f"</{tag}>")
        self.depth -= 1
        if self.depth <= 0:
            self.capturing = False

    def handle_data(self, data: str) -> None:
        if self.capturing:
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.capturing:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.capturing:
            self.parts.append(f"&#{name};")


class MarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []
        self.skip_depth = 0
        self.list_depth = 0

    def emit(self, value: str) -> None:
        if self.skip_depth == 0:
            self.parts.append(value)

    def newline(self, count: int = 1) -> None:
        self.emit("\n" * count)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k: v or "" for k, v in attrs}
        if tag in {"script", "style", "svg", "iframe", "video"}:
            self.skip_depth += 1
            return
        if tag in {"p", "div", "section", "article"}:
            self.newline(2)
        elif tag in {"br"}:
            self.newline()
        elif tag in {"h1", "h2", "h3"}:
            level = {"h1": "#", "h2": "##", "h3": "###"}[tag]
            self.newline(2)
            self.emit(f"{level} ")
        elif tag in {"strong", "b"}:
            self.emit("**")
        elif tag in {"em", "i"}:
            self.emit("*")
        elif tag == "blockquote":
            self.newline(2)
            self.emit("> ")
        elif tag in {"ul", "ol"}:
            self.list_depth += 1
            self.newline()
        elif tag == "li":
            self.newline()
            self.emit("- ")
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self.links.append(href)
            self.emit("[")
        elif tag == "img":
            src = attrs_dict.get("data-src") or attrs_dict.get("src") or attrs_dict.get("data-original")
            alt = attrs_dict.get("alt") or "image"
            if src:
                self.newline(2)
                self.emit(f"![{alt}]({src})")
                self.newline(2)
        elif tag == "pre":
            self.newline(2)
            self.emit("```text\n")
        elif tag == "code":
            self.emit("`")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "iframe", "video"}:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag in {"p", "div", "section", "article", "blockquote", "h1", "h2", "h3"}:
            self.newline(2)
        elif tag in {"strong", "b"}:
            self.emit("**")
        elif tag in {"em", "i"}:
            self.emit("*")
        elif tag in {"ul", "ol"}:
            self.list_depth = max(0, self.list_depth - 1)
            self.newline()
        elif tag == "a":
            href = self.links.pop() if self.links else ""
            self.emit(f"]({href})" if href else "]")
        elif tag == "pre":
            self.emit("\n```")
            self.newline(2)
        elif tag == "code":
            self.emit("`")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = re.sub(r"\s+", " ", data)
        if text.strip():
            self.emit(text)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = html.unescape(text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" +", " ", text)
        return text.strip() + "\n"


def extract_element_html(source: str, element_id: str) -> str:
    parser = ElementExtractor(element_id)
    parser.feed(source)
    return "".join(parser.parts)


def html_to_markdown(source: str) -> str:
    converter = MarkdownConverter()
    converter.feed(source)
    return converter.markdown()


def extension_from_content_type(content_type: str, url: str) -> str:
    lowered = content_type.lower()
    if "jpeg" in lowered or "jpg" in lowered:
        return ".jpg"
    if "png" in lowered:
        return ".png"
    if "gif" in lowered:
        return ".gif"
    if "webp" in lowered:
        return ".webp"
    suffix = Path(urlparse(url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp"} else ".jpg"


def localize_markdown_images(markdown: str, task_dir: Path, source_url: str, limit: int = 40) -> tuple[str, dict[str, Any]]:
    image_dir = task_dir / "images"
    if image_dir.exists():
        import shutil

        shutil.rmtree(image_dir)
    diagnostics: dict[str, Any] = {
        "image_refs": 0,
        "localized_images": 0,
        "image_failures": [],
    }
    pattern = re.compile(r"!\[([^\]]*)\]\((https?://[^)]+)\)")

    def replace(match: re.Match[str]) -> str:
        diagnostics["image_refs"] += 1
        alt = match.group(1) or "image"
        url = html.unescape(match.group(2))
        if diagnostics["localized_images"] >= limit:
            diagnostics["image_failures"].append({"url": url, "reason": "image localization limit reached"})
            return match.group(0)
        try:
            data, content_type = fetch_bytes(url, timeout=20, referer=source_url)
            ext = extension_from_content_type(content_type, url)
            image_dir.mkdir(parents=True, exist_ok=True)
            filename = f"image-{diagnostics['localized_images'] + 1:03d}{ext}"
            (image_dir / filename).write_bytes(data)
            diagnostics["localized_images"] += 1
            return f"![{alt}](images/{filename})"
        except Exception as exc:
            diagnostics["image_failures"].append({"url": url, "reason": str(exc)[:240]})
            return match.group(0)

    return pattern.sub(replace, markdown), diagnostics


def extract_wechat(url: str, source: str) -> dict[str, Any]:
    title = meta_content(
        source,
        [
            r'id=["\']activity-name["\'][^>]*>(.*?)</',
            r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']',
            r'<title[^>]*>(.*?)</title>',
        ],
    )
    author = meta_content(
        source,
        [
            r'id=["\']js_name["\'][^>]*>(.*?)</',
            r'id=["\']profileBt["\'][\s\S]*?class=["\'][^"\']*profile_nickname[^"\']*["\'][^>]*>(.*?)</',
            r'<meta\s+name=["\']author["\']\s+content=["\'](.*?)["\']',
        ],
    )
    published = meta_content(source, [r'var\s+ct\s*=\s*["\'](\d+)["\']'])
    if published:
        try:
            from datetime import datetime

            published = datetime.fromtimestamp(int(published)).date().isoformat()
        except Exception:
            pass
    content_html = extract_element_html(source, "js_content")
    markdown = html_to_markdown(content_html)
    plain_length = len(re.sub(r"\s+", "", re.sub(r"!\[[^\]]*\]\([^)]+\)", "", markdown)))
    if plain_length < 120:
        raise RuntimeError("WeChat article body extraction produced too little text; page may require login or anti-bot verification.")
    return {
        "title": strip_tags(title) or "微信文章",
        "author": strip_tags(author),
        "published_at": published,
        "source_url": url,
        "content": markdown,
    }


def fetch_article(url: str, task_dir: Path) -> dict[str, Any]:
    source = fetch_html(url)
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "article_raw.html").write_text(source, encoding="utf-8")
    if "mp.weixin.qq.com" in url.lower():
        data = extract_wechat(url, source)
    else:
        # Conservative generic fallback: use body text conversion when no source-specific extractor exists.
        body = extract_element_html(source, "content") or source
        markdown = html_to_markdown(body)
        title = meta_content(source, [r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', r"<title[^>]*>(.*?)</title>"])
        data = {"title": strip_tags(title) or "网页文章", "author": "", "published_at": "", "source_url": url, "content": markdown}
    content, image_diagnostics = localize_markdown_images(data["content"], task_dir, url)
    data["content"] = content
    (task_dir / "content.md").write_text(data["content"], encoding="utf-8")
    metadata = {k: v for k, v in data.items() if k != "content"}
    (task_dir / "article_meta.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text_length = len(re.sub(r"\s+", "", re.sub(r"!\[[^\]]*\]\([^)]+\)", "", data["content"])))
    diagnostics = {
        "source_url": url,
        "text_length": text_length,
        "title_captured": bool(metadata.get("title")),
        "author_captured": bool(metadata.get("author")),
        "published_at_captured": bool(metadata.get("published_at")),
        **image_diagnostics,
    }
    (task_dir / "article_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a web or WeChat article into Markdown.")
    parser.add_argument("url")
    parser.add_argument("--task-dir", type=Path, required=True)
    args = parser.parse_args()
    meta = fetch_article(args.url, args.task_dir)
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
