#!/usr/bin/env bash
set -euo pipefail

cd "/Users/longhuadmin/obsidian-inbox"
exec /usr/bin/python3 scripts/ingest_ai_news_daily.py
