# 04 Obsidian Inbox v0.1 发布草稿

## 标题

Obsidian Inbox v0.1：把视频、文章和本地资料整理进 Obsidian

## GitHub Release 正文

`Obsidian Inbox` 是一个 local-first 的 Codex Skill，用来把外部内容整理成结构化 Obsidian 笔记。

它不是一次性 AI 摘要工具，而是一套内容入库工作流：本地脚本负责采集、归档和索引，Codex 负责理解内容并生成普通总结或深度总结。

### 当前能力

- Bilibili 视频字幕入库。
- 微信公众号公开文章正文入库。
- 本地视频/音频导入，支持转写或 ASR 路径。
- 普通总结和深度总结两种笔记模式。
- 原始材料归档到 `_resources/`。
- 自动重建资料库索引、主题索引和用途索引。
- 抓不到字幕、正文或可靠转写时保留失败状态，不编造总结。

### 适合谁

- Obsidian 重度用户。
- 经常收藏视频和文章但很少复盘的人。
- 想把 Codex 变成本地工作流的人。
- 关心 local-first、Markdown、可追溯材料的知识管理用户。

### 试用入口

项目地址：

https://github.com/Simuiu/obsidian-inbox

如果你也想把视频、文章和本地资料稳定沉淀进 Obsidian，欢迎 Star 项目，并在 Issue 里告诉我你最想支持哪类资料。

## Codex 自评

这版 Release 适合作为 v0.1 首发说明，重点放在能力边界和目标用户，没有夸大自动化或平台抓取能力。

发布前需要确认：

1. 当前是否已经准备好打 `v0.1` tag。
2. 是否要先补一段 60-90 秒 demo 视频链接。
3. 是否要把 README 里的中文快速开始再压缩一版，放进 Release。
