#!/usr/bin/env python3
"""Prepare or create a WeChat Official Account draft for Obsidian Inbox.

Default mode is local preview only. Network API calls require explicit flags.
Secrets are read from environment variables or a local env file passed with
--env-file. Do not commit real env files.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

import requests


ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "marketing/publish-packets/2026-05-11-full-platform-launch"
PREVIEW_DIR = ROOT / "marketing/automation/previews"

TITLE = "我把 Codex 接进了 Obsidian"
DIGEST = (
    "我以前最大的问题不是不会用 AI 总结，而是总结完以后根本找不回来。"
    "于是我把 Codex 接进 Obsidian，做了一个把文章、视频和本地资料整理进自己知识库的小工具。"
)
GITHUB_URL = "https://github.com/Simuiu/obsidian-inbox"
COVER = PACKET_DIR / "images/wechat/cover-wechat-flow.png"
BODY_IMAGES = [
    PACKET_DIR / "images/wechat/cards/wechat-01.png",
    PACKET_DIR / "images/wechat/cards/wechat-02.png",
    PACKET_DIR / "images/wechat/cards/wechat-03.png",
    PACKET_DIR / "images/wechat/cards/wechat-04.png",
    PACKET_DIR / "images/wechat/cards/wechat-05.png",
]

SECTIONS: List[Tuple[str, str]] = [
    (
        "我真正受不了的是反复整理",
        "我以前很爱让 AI 总结东西。\n"
        "看到一篇长文，丢进去；看到一个视频，丢进去；买了课、听了分享，也丢进去。\n"
        "当时确实省时间。\n"
        "但过几天我想找某个观点，经常会卡住：它到底在哪个聊天窗口里？原链接是哪一个？当时那段字幕或原文还在不在？\n"
        "最烦的是，有些内容我明明总结过，最后还是要重新找链接、重新发给 AI、重新整理一遍。\n"
        "这件事让我意识到：我缺的不是又一个摘要，而是一个能把资料放回知识库里的入口。",
    ),
    (
        "我想要的是少做一次重复劳动",
        "我的资料来源很杂：B 站视频、公众号文章、网页、本地课程、会议录音，还有一些临时收藏的链接。\n"
        "以前我会先收藏，等有空再整理。结果你也知道，基本没有那个“有空”。\n"
        "所以我想要的其实很简单：我把链接或本地文件丢进去，它先把正文、字幕或转写准备好，再让 Codex 写成一篇 Obsidian 笔记，同时把原始材料也留下。\n"
        "下次我再找这条资料，不用翻聊天记录，也不用猜关键词，直接从 Obsidian 的索引里进。",
    ),
    (
        "我把 Codex 接进 Obsidian 后发生了什么",
        "这个小工具叫 Obsidian Inbox。\n"
        "它现在做的事情不复杂：先在本地准备资料包，再让 Codex 按固定结构写 Obsidian 笔记。\n"
        "一条资料进来后，最后不只是得到一段“本文主要讲了什么”。它会变成一个文件夹：里面有主笔记，也有 _resources，用来放原始正文、字幕、转写或本地文件路径。\n"
        "我最需要的就是这个结果。\n"
        "因为一篇笔记如果没有来源、没有原始材料、没有索引入口，过一段时间还是会变成孤岛。",
    ),
    (
        "有些事我故意不让它做",
        "我没有把它包装成“全平台一键导入”。\n"
        "听起来很厉害，但不真实，也不安全。\n"
        "很多平台有登录、验证码、付费墙和版权边界。这个工具不会宣传自己能绕过这些限制。\n"
        "它的原则反而比较保守：能拿到公开正文或字幕，才继续整理；拿不到可靠材料，就保留失败状态，不硬编一篇看起来很完整的笔记；Obsidian Vault、Markdown 和原始材料默认都在本地。\n"
        "对我来说，知识库工具最重要的不是显得自动化，而是别把不确定的东西伪装成确定。",
    ),
    (
        "它适合的不是所有人",
        "如果你只是偶尔总结一篇文章，它可能有点重。\n"
        "但如果你已经在用 Obsidian，或者经常看长视频、课程、技术文章、会议材料，又总觉得“收藏很多，真正沉淀很少”，它会比较适合你。\n"
        "我做它的目的不是替我思考，而是替我完成那部分最容易拖延的整理动作：建文件、归档材料、写初稿、补索引。\n"
        "真正有价值的地方，是它把“我看过”往前推了一步，变成“我以后还能找回来”。",
    ),
]


def load_env_file(path: Path | None) -> None:
    if not path:
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required env var: {name}")
    return value


def wx_get(url: str, **params: str) -> Dict:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    if data.get("errcode"):
        raise SystemExit(f"WeChat API error: {data}")
    return data


def wx_post_json(url: str, payload: Dict, **params: str) -> Dict:
    response = requests.post(
        url,
        params=params,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("errcode"):
        raise SystemExit(f"WeChat API error: {data}")
    return data


def get_access_token(appid: str, secret: str) -> str:
    data = wx_get(
        "https://api.weixin.qq.com/cgi-bin/token",
        grant_type="client_credential",
        appid=appid,
        secret=secret,
    )
    return data["access_token"]


def upload_thumb(access_token: str, path: Path) -> str:
    with path.open("rb") as fh:
        response = requests.post(
            "https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={"access_token": access_token, "type": "thumb"},
            files={"media": (path.name, fh, "image/png")},
            timeout=60,
        )
    response.raise_for_status()
    data = response.json()
    if data.get("errcode"):
        raise SystemExit(f"WeChat thumb upload error: {data}")
    return data["media_id"]


def upload_content_image(access_token: str, path: Path) -> str:
    with path.open("rb") as fh:
        response = requests.post(
            "https://api.weixin.qq.com/cgi-bin/media/uploadimg",
            params={"access_token": access_token},
            files={"media": (path.name, fh, "image/png")},
            timeout=60,
        )
    response.raise_for_status()
    data = response.json()
    if data.get("errcode"):
        raise SystemExit(f"WeChat image upload error: {data}")
    return data["url"]


def html_content(image_urls: List[str] | None = None) -> str:
    image_urls = image_urls or [str(path.relative_to(PACKET_DIR)) for path in BODY_IMAGES]
    chunks: List[str] = []
    for index, (heading, body) in enumerate(SECTIONS):
        chunks.append(f'<h2 style="font-size:20px;line-height:1.5;margin:24px 0 12px;">{heading}</h2>')
        for paragraph in body.split("\n"):
            chunks.append(f'<p style="font-size:16px;line-height:1.8;margin:0 0 12px;">{paragraph}</p>')
        if index < len(image_urls):
            chunks.append(f'<p style="margin:18px 0;"><img src="{image_urls[index]}" style="max-width:100%;" /></p>')
    chunks.append(f'<p style="font-size:16px;line-height:1.8;margin:24px 0 12px;">项目地址：{GITHUB_URL}</p>')
    return "\n".join(chunks)


def build_payload(thumb_media_id: str, image_urls: List[str] | None = None) -> Dict:
    return {
        "articles": [
            {
                "title": TITLE,
                "author": os.environ.get("WECHAT_OFFICIAL_AUTHOR", ""),
                "digest": DIGEST,
                "content": html_content(image_urls),
                "content_source_url": os.environ.get("WECHAT_OFFICIAL_CONTENT_SOURCE_URL", GITHUB_URL),
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
            }
        ]
    }


def write_preview(payload: Dict) -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    (PREVIEW_DIR / "wechat-draft-payload.preview.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    preview_content = payload["articles"][0]["content"].replace(
        'src="images/',
        'src="../../publish-packets/2026-05-11-full-platform-launch/images/',
    )
    html = f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>{TITLE}</title></head>
<body style="max-width:760px;margin:40px auto;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;color:#222;">
<h1>{TITLE}</h1>
<p style="color:#666;">{DIGEST}</p>
<img src="../../publish-packets/2026-05-11-full-platform-launch/images/wechat/cover-wechat-flow.png" style="width:100%;max-width:900px;" />
{preview_content}
</body></html>
"""
    (PREVIEW_DIR / "wechat-draft-preview.html").write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="Local env file with WeChat credentials.")
    parser.add_argument("--upload-assets", action="store_true", help="Upload cover/body images to WeChat and use returned media/url values.")
    parser.add_argument("--create-draft", action="store_true", help="Create WeChat draft. Requires credentials and uploaded/available thumb media.")
    args = parser.parse_args()

    load_env_file(args.env_file)

    thumb_media_id = os.environ.get("WECHAT_OFFICIAL_THUMB_MEDIA_ID", "PREVIEW_THUMB_MEDIA_ID")
    image_urls: List[str] | None = None
    access_token = None

    if args.upload_assets or args.create_draft:
        access_token = get_access_token(require_env("WECHAT_OFFICIAL_APPID"), require_env("WECHAT_OFFICIAL_SECRET"))

    if args.upload_assets:
        thumb_media_id = upload_thumb(access_token, COVER)
        image_urls = [upload_content_image(access_token, path) for path in BODY_IMAGES]

    if args.create_draft and thumb_media_id == "PREVIEW_THUMB_MEDIA_ID":
        raise SystemExit("Creating a draft requires --upload-assets or WECHAT_OFFICIAL_THUMB_MEDIA_ID.")

    payload = build_payload(thumb_media_id, image_urls)
    write_preview(payload)

    if args.create_draft:
        result = wx_post_json(
            "https://api.weixin.qq.com/cgi-bin/draft/add",
            payload,
            access_token=access_token,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Preview written: {PREVIEW_DIR / 'wechat-draft-preview.html'}")
        print(f"Payload written: {PREVIEW_DIR / 'wechat-draft-payload.preview.json'}")


if __name__ == "__main__":
    main()
