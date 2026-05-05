from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from v2o_common import ROOT, load_config


SAMPLE_URL = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
SAMPLE_PAGE = "https://peach.blender.org/about/"
SAMPLE_LICENSE = "Creative Commons Attribution 3.0"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a safe YouTube metadata/subtitle smoke test with a CC sample video.")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    cmd = [sys.executable, "scripts/prepare_link.py", SAMPLE_URL]
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    task_dir = Path(output_lines[-1]) if result.returncode == 0 and output_lines else None
    meta = {}
    if task_dir and (task_dir / "meta.json").exists():
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))

    checks = {
        "sample_url": SAMPLE_URL,
        "license_reference": SAMPLE_PAGE,
        "sample_license": SAMPLE_LICENSE,
        "returncode": result.returncode,
        "task_dir": str(task_dir) if task_dir else "",
        "platform": meta.get("platform"),
        "status": meta.get("status"),
        "title": meta.get("title"),
        "passed": result.returncode == 0 and meta.get("platform") == "youtube" and meta.get("status") in {"subtitle_captured", "needs_subtitle_or_asr", "metadata_capture_failed"},
    }
    if not args.keep and task_dir:
        shutil.rmtree(task_dir, ignore_errors=True)
        config = load_config()
        resource_dir = meta.get("resource_dir")
        if resource_dir:
            shutil.rmtree(Path(resource_dir), ignore_errors=True)
        checks["cleaned"] = True
    else:
        checks["cleaned"] = False
    if result.returncode != 0:
        checks["error_tail"] = result.stdout[-1200:]
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    if not checks["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
