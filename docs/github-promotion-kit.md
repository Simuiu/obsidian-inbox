# Obsidian Inbox GitHub 宣传资料套件

## 核心定位

中文一句话：

> 把 Codex 变成你的本地知识入库员：链接进来，Obsidian 笔记、原始材料和可点击索引自动生成。

英文一句话：

> Turn Codex into a local knowledge librarian for Obsidian.

更完整的英文描述：

> Obsidian Inbox is a local-first Codex skill that ingests videos, articles, web pages, WeChat posts, and local media into structured Obsidian notes with raw material archives and rebuilt indexes.

## GitHub About 区域

Description:

```text
Local-first Codex skill for turning videos, articles, web pages, and local media into structured Obsidian notes with raw archives and clickable indexes.
```

Website:

```text
留空，或放演示文档 / demo video 链接
```

Topics:

```text
obsidian
codex
ai-notes
knowledge-management
markdown
local-first
bilibili
youtube
wechat
content-ingestion
second-brain
personal-knowledge-management
```

## GitHub Star CTA

短版：

```text
Star this repo if you want better local-first AI workflows for Obsidian.
```

中文短版：

```text
如果你也想把视频、文章和图文稳定沉淀进 Obsidian，欢迎 Star 支持。
```

README 结尾版：

```text
If this saves you from another folder of forgotten links, star the repo and share what platform you want supported next.
```

## README 首屏文案

```md
# Obsidian Inbox

Local-first AI content ingestion for Obsidian, powered by Codex.

Give Codex a video, article, web page, WeChat post, or local media file. Obsidian Inbox prepares a task package, writes a structured Markdown note, preserves raw materials, and rebuilds clickable indexes in your Vault.

It is not just an AI summarizer. It is a repeatable content-to-knowledge workflow.
```

## 产品卖点

- Local-first: Vault、cookies、字幕、转写和原始材料默认留在本地。
- Obsidian-native: 输出 Markdown、frontmatter、Wiki links、总索引、主题索引和用途索引。
- Source-traceable: raw materials 进入 `_resources/{entry_id}/`，笔记只引用不堆全文。
- Failure-safe: 没有字幕、正文或可靠转写时，不编造总结。
- Codex-powered: 让 AI 负责理解与写作，让脚本负责可重复的采集、归档和索引。
- Deep notes: 不止摘要，还能生成问题链、机制拆解、误区、取舍、实践路径和二次加工卡片。

## 适合人群

- Obsidian 重度用户
- AI / 产品 / 技术学习者
- 经常收藏视频和文章但缺少复盘系统的人
- 创作者、研究者、知识工作者
- 偏好本地优先工作流的人

## Launch Tweet / X

英文：

```text
I built Obsidian Inbox: a local-first Codex skill that turns videos, articles, web pages, WeChat posts, and local media into structured Obsidian notes.

It preserves raw materials, writes Markdown notes, and rebuilds clickable indexes.

Not another AI summarizer. A content-to-knowledge workflow.

GitHub: <repo-url>
```

中文：

```text
我做了一个 Codex skill：Obsidian Inbox。

它可以把 B 站视频、微信公众号文章、网页、本地视频/图文材料整理成 Obsidian 笔记，保留原始材料，并自动重建总索引、主题索引和用途索引。

重点不是“总结一次”，而是把内容稳定沉淀进个人知识库。

GitHub: <repo-url>
```

## Hacker News / Reddit 标题

```text
Show HN: Obsidian Inbox - a local-first Codex skill for turning links into Obsidian notes
```

```text
I built a Codex-powered local content ingestion workflow for Obsidian
```

```text
Obsidian Inbox: from videos and articles to structured Markdown notes with raw archives
```

## Product Hunt 标题与副标题

Name:

```text
Obsidian Inbox
```

Tagline:

```text
Turn links and local media into structured Obsidian notes
```

Description:

```text
Obsidian Inbox is a local-first Codex skill for transforming videos, articles, web pages, WeChat posts, and local media into structured Markdown notes. It preserves raw materials, writes traceable frontmatter, and rebuilds clickable Obsidian indexes.
```

## Demo Video 脚本

时长：60-90 秒。

1. 打开 Obsidian，展示空的 `00_Inbox/内容入库`。
2. 在 Codex 输入：`深度入库这个 B 站视频：https://...`
3. 展示终端生成任务包：`meta.json`、`compact.md`、`prompt.md`。
4. 展示 Codex 读取 compact 后生成深度笔记。
5. 打开 Obsidian 新笔记，展示问题链、机制拆解、行动清单。
6. 打开 `_resources/{entry_id}`，展示原始字幕/正文保留在资源目录。
7. 打开 `内容入库索引.md`，展示可点击索引已更新。
8. 结尾字幕：`Not just summaries. A local content-to-knowledge workflow.`

## Demo GIF 分镜

```text
Frame 1: Paste a link into Codex
Frame 2: Task package generated locally
Frame 3: Structured Obsidian note appears
Frame 4: Raw transcript stored under _resources
Frame 5: Index rebuilt and clickable
```

## Release Announcement

```md
## Obsidian Inbox v0.1

Obsidian Inbox is a local-first Codex skill for turning external content into structured Obsidian notes.

Current highlights:

- Bilibili video subtitle ingestion
- WeChat public article ingestion
- local media import with transcript / ASR path
- standard and deep note templates
- raw materials archived under `_resources/{entry_id}`
- rebuilt total, topic, and purpose indexes
- safe failure behavior when content cannot be captured

This first release is for people who want a practical bridge between daily content consumption and long-term personal knowledge management.
```

## Issue 模板建议

Platform support request:

```md
## Platform

## Example URL or material type

## What you expect to capture

## Is login required?

## Can you provide local exported files instead?

## Expected Obsidian note shape
```

Capture failure:

```md
## Command

## Source platform

## Failure status

## diagnostics.json or terminal output

## Did the content require login, captcha, or paid access?
```

## 推广渠道优先级

1. GitHub README + Topics + demo GIF
2. Obsidian Forum：强调 local-first、Markdown、Vault-native
3. X / Twitter：强调 Codex skill 和 second brain
4. Reddit `r/ObsidianMD`：强调本地优先和不上传 Vault
5. Hacker News：强调 AI agent workflow，不要夸大平台抓取
6. Bilibili / 小红书：做中文演示，突出“收藏夹变知识库”

## 不建议使用的宣传话术

- “自动抓取全平台内容”
- “绕过限制下载视频”
- “一键总结任何链接”
- “完全自动化知识库”

这些说法会带来错误预期和平台合规风险。更好的表达是“本地优先、可追溯、失败安全、半自动内容入库”。

