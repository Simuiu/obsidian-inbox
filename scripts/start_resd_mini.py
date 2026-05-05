from __future__ import annotations

import os
import subprocess
from pathlib import Path

from v2o_common import find_tool


def main() -> None:
    tool = find_tool("resd-mini")
    if not tool:
        raise SystemExit("resd-mini not found. Run: python3 scripts/install_resd_mini.py")
    print("Starting resd-mini. Follow its browser UI to start proxy/listening.")
    print("If macOS blocks it, allow it in System Settings > Privacy & Security.")
    print("")
    subprocess.run([tool], cwd=str(Path.cwd()), env=os.environ.copy(), check=False)


if __name__ == "__main__":
    main()
