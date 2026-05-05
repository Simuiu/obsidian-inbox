from __future__ import annotations

import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from v2o_common import ROOT, local_bin


URLS = {
    "ffmpeg": "https://evermeet.cx/ffmpeg/getrelease/zip",
    "ffprobe": "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip",
}


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout)


def install_one(name: str, url: str) -> Path:
    target_dir = local_bin()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / name
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / f"{name}.zip"
        run(["curl", "-L", "--fail", "-o", str(archive), url])
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(tmp_path)
        candidates = [path for path in tmp_path.rglob(name) if path.is_file()]
        if not candidates:
            raise RuntimeError(f"{name} not found in downloaded archive")
        shutil.copy2(candidates[0], target)
        target.chmod(0o755)
    return target


def main() -> None:
    print(f"Installing ffmpeg tools into {local_bin()}")
    for name, url in URLS.items():
        path = install_one(name, url)
        print(f"installed {name}: {path}")
    print("")
    run([str(local_bin() / "ffmpeg"), "-version"])
    run([str(local_bin() / "ffprobe"), "-version"])
    print("ffmpeg and ffprobe are ready.")


if __name__ == "__main__":
    main()
