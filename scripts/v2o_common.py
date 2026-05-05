from __future__ import annotations

import json
import re
import hashlib
import subprocess
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import shutil

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.yaml"


def load_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def local_bin() -> Path:
    return ROOT / "tools" / "bin"


def find_tool(name: str) -> str | None:
    local = local_bin() / name
    if local.exists():
        return str(local)
    return shutil.which(name)


def safe_filename(value: str, max_len: int = 80) -> str:
    value = re.sub(r'[\\/:\*\?"<>\|]', "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.strip(". ")
    return value[:max_len].rstrip() or "untitled"


def detect_platform(url: str) -> str:
    lowered = url.lower()
    if "bilibili.com" in lowered or "b23.tv" in lowered:
        return "bilibili"
    if "youtube.com" in lowered or "youtu.be" in lowered:
        return "youtube"
    if "channels.weixin.qq.com" in lowered or "finder.video.qq.com" in lowered:
        return "wechat_video"
    if "mp.weixin.qq.com" in lowered:
        return "wechat"
    return "web"


def link_id(url: str) -> str:
    parsed = urlparse(url)
    match = re.search(r"/s/([^/?#]+)", parsed.path)
    if match:
        return safe_filename(match.group(1), max_len=32)
    host = parsed.netloc.replace("www.", "") or "web"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return safe_filename(f"{host}-{digest}", max_len=48)


def today() -> str:
    return date.today().isoformat()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
