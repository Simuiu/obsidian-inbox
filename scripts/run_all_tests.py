from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from v2o_common import ROOT


def run_step(name: str, cmd: list[str]) -> dict[str, object]:
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return {
        "name": name,
        "cmd": " ".join(cmd),
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "output_tail": result.stdout[-1600:],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local regression suite.")
    parser.add_argument("--skip-network", action="store_true", help="Skip tests that download or query public internet resources.")
    args = parser.parse_args()

    steps = [
        ("py_compile", [sys.executable, "-m", "py_compile", *[str(path) for path in sorted((ROOT / "scripts").glob("*.py"))]]),
        ("doctor", [sys.executable, "scripts/doctor.py"]),
        ("init_config", [sys.executable, "scripts/init_config.py", "--vault-path", "/tmp/video2obsidian-vault", "--output", "/tmp/video2obsidian-test-config.yaml", "--force"]),
        ("render_note", [sys.executable, "scripts/render_note.py", "tasks/2026-05-04-wechat-9d5DWg7YdMHPvVl-2KLH2w", "--output", "/tmp/video2obsidian-render-test.md", "--force"]),
        ("local_export", [sys.executable, "scripts/run_local_export_smoke_test.py"]),
    ]
    if not args.skip_network:
        steps.extend(
            [
                ("public_media", [sys.executable, "scripts/run_public_media_smoke_test.py"]),
                ("public_asr", [sys.executable, "scripts/run_public_asr_smoke_test.py"]),
                ("wechat_article", [sys.executable, "scripts/run_wechat_article_smoke_test.py"]),
                ("youtube_public", [sys.executable, "scripts/run_youtube_public_smoke_test.py"]),
            ]
        )
    steps.append(("rebuild_index", [sys.executable, "scripts/rebuild_obsidian_index.py"]))

    results = [run_step(name, cmd) for name, cmd in steps]
    for temp in [Path("/tmp/video2obsidian-test-config.yaml"), Path("/tmp/video2obsidian-test-config.yaml.bak")]:
        temp.unlink(missing_ok=True)
    Path("/tmp/video2obsidian-render-test.md").unlink(missing_ok=True)
    summary = {
        "passed": all(item["passed"] for item in results),
        "total": len(results),
        "failed": [item["name"] for item in results if not item["passed"]],
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
