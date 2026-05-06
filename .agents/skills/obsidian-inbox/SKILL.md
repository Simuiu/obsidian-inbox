---
name: obsidian-inbox
description: Use when the user asks to ingest, summarize, save, 入库, 深度入库, or organize links into an Obsidian Inbox. Handles Bilibili/YouTube video notes today, with a product structure intended for articles, web pages, WeChat, Xiaohongshu, Douyin, audio, and image-text content.
---

# Obsidian Inbox

Use this skill when the user says things like:

- "把这个链接入库"
- "深度入库这个视频"
- "整理到 Obsidian"
- "用 obsidian-inbox 处理 ..."

## Goal

Turn external content into clean Obsidian Inbox notes that remain navigable after many items accumulate.

## Fixed Paths

- Project root: `/Users/longhuadmin/obsidian-inbox`
- Obsidian vault: `/Users/longhuadmin/Library/Mobile Documents/iCloud~md~obsidian/Documents/bling`
- Library folder: `00_资料库`
- Index file: `00_资料库/000 资料库索引/000 资料库索引.md`
- Topic index: `00_资料库/001 主题索引/001 主题索引.md`
- Purpose index: `00_资料库/002 用途索引/002 用途索引.md`
- Entry structure: `00_资料库/YYMMDD 短标题/YYMMDD 短标题.md`
- Entry resources: `00_资料库/YYMMDD 短标题/_resources`

## Supported Sources

- Stable now: Bilibili videos with available AI subtitles.
- Stable now: public WeChat official account articles (`mp.weixin.qq.com`) with accessible article body.
- Partial: YouTube videos through `yt-dlp` subtitles.
- Partial: generic web pages through conservative HTML extraction.
- WeChat Channels / 微信视频号: supported through external downloader import. Use `resd-mini` / `res-downloader` or `wechatVideoDownload` to capture the local video first, then run `scripts/import_wechat_video.py`.
- Planned: Xiaohongshu, Douyin, richer image-text content, and stable ASR fallback.

If a source is not supported or content capture fails, do not invent a summary. Write only the captured metadata and the limitation.

## Workflow

1. Run the local prepare script:

   ```bash
   python3 scripts/prepare_link.py "<URL>" --sync-raw
   ```

   For explicit deep requests such as "深度入库", "深度总结", "课程讲义", or "教学笔记":

   ```bash
   python3 scripts/prepare_link.py "<URL>" --sync-raw --mode deep
   ```

2. Read only these files from the newest task directory:

   - `meta.json`
   - `compact.md`
   - `prompt.md`

3. Do not read full `transcript_timed.md` or full `.srt` unless `compact.md` is clearly insufficient.
   For articles, do not read full `content.md` unless `compact.md` is clearly insufficient.

4. Write the final note to the suggested path in `meta.json`:

   - standard mode: `standard_note_path`
   - deep mode: `deep_note_path`

   If the user asks for a quick draft or wants a script-generated starting point, run:

   ```bash
   python3 scripts/render_note.py "<TASK_DIR>" --write
   ```

   For a deep draft:

   ```bash
   python3 scripts/render_note.py "<TASK_DIR>" --mode deep --write
   ```

   Treat generated drafts as editable scaffolding, not final AI summaries.

5. Link raw/source materials from the entry `_resources` folder. For local videos, do not copy original video or `audio.wav` into Obsidian; keep only transcript/light materials and record the original local path in the main note.

6. Run the index rebuild after writing the note:

   ```bash
   python3 scripts/rebuild_obsidian_index.py
   ```

## WeChat Channels Workflow

GitHub implementations to use as capture layer:

- `https://github.com/putyy/resd-mini`
- `https://github.com/putyy/res-downloader`
- `https://github.com/qiye45/wechatVideoDownload`

These tools capture WeChat Channels media through local proxy/listening; they are not simple URL-to-video libraries. After the video file is captured locally, import it into this workflow:

```bash
python3 scripts/import_wechat_video.py \
  --video "/path/to/video.mp4" \
  --source-url "<WECHAT_CHANNELS_URL>" \
  --title "<TITLE>" \
  --author "<AUTHOR>"
```

If a transcript is available:

```bash
python3 scripts/import_wechat_video.py \
  --video "/path/to/video.mp4" \
  --source-url "<WECHAT_CHANNELS_URL>" \
  --title "<TITLE>" \
  --author "<AUTHOR>" \
  --transcript "/path/to/transcript.md"
```

Without transcript/ASR, do not generate a summary. The task should remain `needs_asr`.

## Naming Rules

- Note file names should use date + short title.
- Do not put the source ID in the note filename.
- Store the stable source ID in frontmatter.
- Each resource should have one main note by default:
  - `YYMMDD short title/YYMMDD short title.md`
- For videos, the main note should use deep-summary structure by default; standard notes, if any, should be archived under `_resources/普通总结归档.md`.
- Standard mode is for quick ingestion and first-pass understanding.
- Deep mode is for reusable learning notes. Use it when the user says "深度入库", "深度总结", "课程", "教学", "系统整理", or when importing local/course videos.
- Frontmatter must include `summary_mode: "普通"` or `summary_mode: "深度"`.
- The `索引与主题` section must include a visible `总结模式：普通/深度` line so users can tell which mode they are reading.

## Standard Note Template

```md
---
title: "{{title}}"
source: "{{source_url}}"
type: "{{content_type}}"
platform: "{{platform}}"
author: "{{author}}"
published_at: "{{published_at}}"
created_at: "{{created_at}}"
status: "已总结"
summary_mode: "普通"
entry_id: "{{entry_key}}"
resource_dir: "{{resource_dir_relative}}"
purposes:
  - 学习
  - 实践
tags:
  - 内容入库
  - AI总结
---

## 索引与主题

- 总结模式：普通
- 总索引：[[00_资料库/000 资料库索引/000 资料库索引|总索引]]
- 主题：[[主题名]]
- 用途：[[00_资料库/002 用途索引/002 用途索引#学习|学习]]、[[00_资料库/002 用途索引/002 用途索引#实践|实践]]

## 一句话总结

## 重点速览

## 核心内容

## 关键时间点

## 值得实践的部分

## 行动清单

## 后续可追问的问题

## 原始材料
```

## Deep Note Template

Deep mode must not be only a longer version of the default note. It should reconstruct the teaching logic and produce reusable study material.

```md
---
title: "{{title}}"
source: "{{source_url}}"
type: "{{content_type}}"
platform: "{{platform}}"
author: "{{author}}"
published_at: "{{published_at}}"
created_at: "{{created_at}}"
status: "已深度总结"
summary_mode: "深度"
entry_id: "{{entry_key}}"
resource_dir: "{{resource_dir_relative}}"
purposes:
  - 学习
  - 实践
tags:
  - 内容入库
  - AI总结
  - 深度笔记
---

## 索引与主题

- 总结模式：深度
- 总索引：[[00_资料库/000 资料库索引/000 资料库索引|总索引]]
- 主题：[[主题名]]
- 用途：[[00_资料库/002 用途索引/002 用途索引#学习|学习]]、[[00_资料库/002 用途索引/002 用途索引#实践|实践]]

## 核心结论

## 这篇内容在解决什么问题

## 概念地图

## 问题链推导

## 关键机制拆解

## 对比表

## 常见误区

## 设计取舍

## 实践路径

## 关键时间点

## 二次加工卡片

## 行动清单

## 后续可追问的问题

## 原始材料
```

## Quality Bar

- The note must be useful as a second-brain entry, not just metadata.
- Keep raw transcripts out of the main note; link to `_resources/...` instead.
- For WeChat articles, the note must be based on captured article正文 from `compact.md`; if正文 capture fails, do not summarize from title alone.
- For WeChat Channels, summarize only after a transcript is available; a captured video file alone is not enough for a reliable note.
- The index must be clickable and rebuilt after note creation.
- Assign `purposes` deliberately: `学习` for understanding/review, `实践` for things worth trying, `素材` for reusable material.
- Never claim a full summary was produced if only metadata was captured.
- For deep mode, include problem chains, mechanisms, comparisons, misconceptions, tradeoffs, and atomic cards.
