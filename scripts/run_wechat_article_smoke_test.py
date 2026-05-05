from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from v2o_common import ROOT


SAMPLE_URL = "https://mp.weixin.qq.com/s/9d5DWg7YdMHPvVl-2KLH2w"
SAMPLE_DESCRIPTION = "Public WeChat article used by the project as an extraction regression sample."


def main() -> None:
    parser = argparse.ArgumentParser(description="Run public WeChat article extraction smoke test.")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    cmd = [sys.executable, "scripts/prepare_link.py", SAMPLE_URL, "--sync-raw"]
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    task_dir = Path(output_lines[-1]) if result.returncode == 0 and output_lines else None
    meta = {}
    diagnostics = {}
    if task_dir and (task_dir / "meta.json").exists():
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    if task_dir and (task_dir / "article_diagnostics.json").exists():
        diagnostics = json.loads((task_dir / "article_diagnostics.json").read_text(encoding="utf-8"))

    checks = {
        "sample_url": SAMPLE_URL,
        "sample_description": SAMPLE_DESCRIPTION,
        "returncode": result.returncode,
        "task_dir": str(task_dir) if task_dir else "",
        "platform": meta.get("platform"),
        "status": meta.get("status"),
        "title": meta.get("title"),
        "text_length": diagnostics.get("text_length"),
        "image_refs": diagnostics.get("image_refs"),
        "localized_images": diagnostics.get("localized_images"),
        "image_failures": diagnostics.get("image_failures"),
    }
    checks["passed"] = (
        result.returncode == 0
        and meta.get("platform") == "wechat"
        and meta.get("status") == "article_captured"
        and int(diagnostics.get("text_length") or 0) > 1000
        and int(diagnostics.get("localized_images") or 0) == int(diagnostics.get("image_refs") or 0)
        and not diagnostics.get("image_failures")
    )
    if not args.keep and task_dir:
        shutil.rmtree(task_dir, ignore_errors=True)
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
