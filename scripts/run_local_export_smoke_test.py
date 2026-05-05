from __future__ import annotations

import argparse
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

from v2o_common import ROOT


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local image-text export smoke test.")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    work_dir = ROOT / "tasks" / "_smoke_local_export"
    image_dir = work_dir / "images_in"
    content = work_dir / "note.md"
    image_dir.mkdir(parents=True, exist_ok=True)
    for index in range(1, 3):
        (image_dir / f"image-{index:03d}.png").write_bytes(PNG_1X1)
    content.write_text(
        "# 本地图文导出测试\n\n这是一条用于验证小红书、抖音图文或自有图文材料入库的本地导出内容。\n\n"
        "它应该生成任务包、compact、资源目录，并保留图片文件。\n",
        encoding="utf-8",
    )

    cmd = [
        sys.executable,
        "scripts/import_article_export.py",
        "--platform",
        "xiaohongshu",
        "--content",
        str(content),
        "--image-dir",
        str(image_dir),
        "--source-url",
        "local-export://xiaohongshu/smoke-test",
        "--title",
        "本地图文导出测试",
        "--author",
        "smoke-test",
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    task_dir = Path(output_lines[-2]) if result.returncode == 0 and len(output_lines) >= 2 else None
    meta = {}
    if task_dir and (task_dir / "meta.json").exists():
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    resource_dir = Path(meta["resource_dir"]) if meta.get("resource_dir") else None
    checks = {
        "returncode": result.returncode,
        "task_dir": str(task_dir) if task_dir else "",
        "platform": meta.get("platform"),
        "status": meta.get("status"),
        "image_count": meta.get("image_count"),
        "compact_exists": bool(task_dir and (task_dir / "compact.md").exists()),
        "resource_content_exists": bool(resource_dir and (resource_dir / "content.md").exists()),
        "resource_images": len(list((resource_dir / "images").glob("*"))) if resource_dir and (resource_dir / "images").exists() else 0,
    }
    checks["passed"] = (
        result.returncode == 0
        and meta.get("platform") == "xiaohongshu"
        and meta.get("status") == "article_captured"
        and meta.get("image_count") == 2
        and checks["compact_exists"]
        and checks["resource_content_exists"]
        and checks["resource_images"] == 2
    )
    if not args.keep:
        shutil.rmtree(work_dir, ignore_errors=True)
        if task_dir:
            shutil.rmtree(task_dir, ignore_errors=True)
        if resource_dir:
            shutil.rmtree(resource_dir, ignore_errors=True)
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
