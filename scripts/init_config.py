from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import yaml

from v2o_common import CONFIG_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize config.yaml for a local Obsidian vault.")
    parser.add_argument("--vault-path", required=True, help="Absolute path to the user's Obsidian vault.")
    parser.add_argument("--output", type=Path, default=CONFIG_PATH, help="Config file to write. Defaults to project config.yaml.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing config.yaml after creating a backup.")
    args = parser.parse_args()

    vault = Path(args.vault_path).expanduser()
    output = args.output.expanduser()
    if output.exists() and not args.force:
        raise SystemExit(f"{output} already exists. Use --force to update it after backup.")
    if output.exists():
        backup = output.with_suffix(output.suffix + ".bak")
        shutil.copy2(output, backup)

    config = {
        "obsidian": {
            "vault_path": str(vault),
            "note_folder": "00_资料库",
            "raw_folder": "00_资料库/_raw",
            "attachment_folder": "00_资料库/_attachments",
            "resource_folder": "00_资料库",
            "topic_folder": "00_资料库",
            "purpose_folder": "00_资料库",
            "index_file": "00_资料库/000 资料库索引/000 资料库索引.md",
            "filename_rule": "date_short_title",
        },
        "tasks": {"task_dir": "tasks"},
        "capture": {"prefer_subtitle": True, "require_api_key": False, "mode": "codex_manual"},
        "bilibili": {"cookies_file": "secrets/bilibili.cookies.txt", "fallback_cookies_from_browser": "chrome"},
        "codex": {"summary_mode": "manual"},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
