# Local Tools

This directory is for local runtime tools that should not be committed to Git.

Installed by helper scripts:

- `scripts/install_ffmpeg_local.py` -> `tools/bin/ffmpeg`, `tools/bin/ffprobe`
- `scripts/install_resd_mini.py` -> `tools/bin/resd-mini`

Check current tool availability:

```bash
python3 scripts/doctor.py
```
