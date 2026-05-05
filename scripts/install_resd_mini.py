from __future__ import annotations

import json
import platform
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from v2o_common import local_bin


REPO = "putyy/resd-mini"


def arch_suffix() -> str:
    machine = platform.machine().lower()
    system = platform.system().lower()
    if system != "darwin":
        raise SystemExit("This installer currently targets macOS only. Download resd-mini manually for other platforms.")
    arch = "arm64" if machine in {"arm64", "aarch64"} else "amd64"
    return f"mac_{arch}"


def latest_asset() -> tuple[str, str]:
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    with urllib.request.urlopen(url, timeout=30) as response:
        release = json.load(response)
    suffix = arch_suffix()
    for asset in release.get("assets", []):
        name = asset.get("name", "")
        if suffix in name and not name.endswith(".dmg"):
            return name, asset["browser_download_url"]
    raise RuntimeError(f"No resd-mini release asset found for {suffix}")


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout)


def main() -> None:
    name, url = latest_asset()
    target = local_bin() / "resd-mini"
    local_bin().mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        download = Path(tmp) / name
        print(f"Downloading {name}")
        run(["curl", "-L", "--fail", "-o", str(download), url])
        shutil.copy2(download, target)
        target.chmod(0o755)
    print(f"installed resd-mini: {target}")
    print("")
    print("Start it with:")
    print("  python3 scripts/start_resd_mini.py")


if __name__ == "__main__":
    main()
