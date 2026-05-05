# Obsidian Inbox README 营销版草稿

> Local-first AI content ingestion for Obsidian, powered by Codex.

`Obsidian Inbox` turns Codex into a local knowledge librarian. Give it a video, article, web page, WeChat post, or local media file, and it prepares a compact task package, writes a structured Obsidian note, preserves raw materials, and rebuilds clickable indexes.

It is designed for people who do not just want another AI summary. It helps you build a long-term personal knowledge base.

## Why This Exists

Most AI summarizers stop at a one-off answer.

`Obsidian Inbox` focuses on the workflow after the summary:

- Where does the note live?
- Can you find it six months later?
- Are raw materials preserved?
- Can deep notes become reusable study material?
- What happens when a platform blocks access or subtitles are missing?

This project solves those problems with a local-first Codex skill and a small set of deterministic Python scripts.

## What It Can Do

| Source | Status | Notes |
|---|---|---|
| Bilibili videos | Stable | Metadata, AI subtitles, standard/deep Obsidian notes |
| WeChat official account articles | Stable | Public article body, Markdown extraction, resource archive |
| YouTube videos | Partial | Subtitle path available; safe failure when access is blocked |
| Generic web pages | Partial | Conservative HTML extraction |
| WeChat Channels | Semi-automatic | Import local captured videos, then transcript or ASR |
| Local video/audio | Supported | Import local files with transcript or ASR |
| Xiaohongshu / Douyin exports | Supported | Local text/image/video import path |

## Core Workflow

```text
Link or local file
-> local capture script
-> task package
-> compact.md for Codex
-> structured Obsidian note
-> raw materials in _resources
-> rebuilt indexes
```

## Standard vs Deep Notes

Standard notes are for fast review:

- one-line summary
- key points
- core content
- timestamps or paragraph clues
- action items
- raw material links

Deep notes are for serious study:

- problem chain
- concept map
- mechanism breakdown
- comparison tables
- common misconceptions
- design tradeoffs
- practice path
- reusable atomic cards

## Local-first by Design

`Obsidian Inbox` does not try to bypass platform access controls.

It does not:

- bypass login, captcha, paywalls, or private content restrictions
- invent summaries when subtitles or article body are missing
- upload your Vault, cookies, transcripts, or raw materials by default

It does:

- keep original materials under `_resources/{entry_id}/`
- write traceable frontmatter
- produce failure states instead of fake notes
- let you inspect every task package locally

## Quickstart

Clone the repository:

```bash
git clone https://github.com/<your-name>/video2obsidian.git
cd video2obsidian
```

Configure your Obsidian Vault:

```bash
python3 scripts/init_config.py --vault-path "/path/to/your/ObsidianVault" --force
```

Check dependencies:

```bash
python3 scripts/doctor.py
```

Run a link ingestion task:

```bash
python3 scripts/prepare_link.py "https://www.bilibili.com/video/BVxxxx" --sync-raw
```

For deep notes:

```bash
python3 scripts/prepare_link.py "https://www.bilibili.com/video/BVxxxx" --sync-raw --mode deep
```

Then ask Codex:

```text
Use the obsidian-inbox skill to finish this task package and write the Obsidian note.
```

Rebuild indexes:

```bash
python3 scripts/rebuild_obsidian_index.py
```

## Recommended Codex Prompt

```text
把这个链接入库：https://...
```

```text
深度入库这个视频：https://...
```

```text
把这个本地视频入库：/path/to/video.mp4，来源是 ...
```

## Obsidian Output

```text
00_Inbox/内容入库/
├── 2026-05-05 Example Note.md
├── 2026-05-05 Example Note 深度.md
├── 内容入库索引.md
├── _topics/
├── _purposes/
└── _resources/
    └── bilibili_xxxxx/
        ├── meta.json
        ├── compact.md
        ├── transcript_timed.md
        └── raw materials...
```

## Run Tests

```bash
python3 scripts/run_all_tests.py --skip-network
```

Full regression:

```bash
python3 scripts/run_all_tests.py
```

## Who Should Use This

Use this if you:

- save many videos and articles but rarely revisit them
- use Obsidian as a second brain
- want local-first AI workflows
- care about source traceability
- need structured notes, not disposable summaries

## Star This Project

If you want Codex-powered local knowledge workflows to become easier for Obsidian users, star the repo and share your use case in Issues.

