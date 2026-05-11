# 07 Obsidian Inbox 全平台配图生成清单

## 1. 生成规则

- 每个平台不少于 5 张配图。
- 使用 image-2 图像生成能力。
- 不同平台使用不同视觉风格，不全平台复用同一套图。
- 图片避免宣称“全平台一键下载”“绕过限制”“无人值守运营”。
- 所有图片尽量少放文字；需要文字时只使用短句，避免模型生成复杂错字。

## 2. 平台与图片规格

| 平台 | 数量 | 建议比例 | 风格 |
| --- | ---: | --- | --- |
| 微信公众号 | 5 | 16:9 或 4:3 | 知识管理长文配图，纸张、桌面、Obsidian 笔记氛围 |
| 知乎 | 5 | 16:9 | 理性讨论、问题分析、知识流转示意 |
| 掘金 | 5 | 16:9 | 技术架构、终端、Markdown、代码工作流 |
| V2EX | 5 | 16:9 | 开发者社区、真实项目、讨论反馈 |
| 即刻 | 5 | 1:1 | 轻量动态、真实开发日志、生活化桌面 |
| B 站 | 5 | 16:9 | 视频封面/分镜，录屏演示感 |
| 小红书 | 6 | 4:5 | 图文卡片，强前后对比，适合收藏 |
| 视频号 | 5 | 9:16 | 竖屏短视频封面/分镜 |
| GitHub | 5 | 16:9 | 开源项目、README、Issue、Star、Release |

## 3. 生成批次

为保证稳定性，每个平台先生成一张“五图分镜合成图”，再拆分为 5 张独立配图；小红书生成 6 张卡片。

合成图统一要求：

- clean five-panel editorial storyboard contact sheet
- each panel visually distinct
- no small unreadable UI text
- no logos except generic Obsidian-like graph and GitHub-like code repository motifs
- no misleading platform automation claims

## 4. 平台提示词

### 微信公众号

生成 5 张用于中文公众号长文的配图，知识管理、Obsidian、AI 内容入库主题。温暖纸张质感、桌面、笔记、Markdown、资料卡片、索引结构，适合严肃但易读的长文。每张图表达一个概念：AI 摘要散落、内容进入 Obsidian、原始材料归档、索引可点击、local-first 安全边界。

### 知乎

生成 5 张用于知乎回答的理性讨论配图。风格冷静、清晰、分析型。主题是“AI 总结之后知识如何沉淀”。画面包含问题卡片、知识流转路径、长期复用、来源追溯、失败安全，不要夸张营销感。

### 掘金

生成 5 张用于掘金技术文章的配图。风格偏开发者、代码、终端、Markdown、架构图。主题包括 capture script、task package、compact.md、Codex Skill、Obsidian note、_resources archive、rebuilt indexes。

### V2EX

生成 5 张用于 V2EX 求反馈帖的配图。风格真实、开发者社区、桌面项目、Issue 讨论、反馈循环。不要广告海报感，像一个开发者分享自己做的小工具。

### 即刻

生成 5 张用于即刻动态的轻量配图。风格真实、轻松、日常开发日志。画面包含 Mac 桌面、Obsidian 笔记、终端、咖啡、简短项目记录感。不要过度商业化。

### B 站

生成 5 张用于 B 站视频封面和分镜的横版图。风格清晰、有教程感、适合科技效率工具视频。主题包括“给 Obsidian 装一个知识入库员”、Codex 输入链接、任务包生成、笔记出现、索引更新。

### 小红书

生成 6 张 4:5 图文卡片，风格适合小红书效率工具/知识管理笔记。大标题清晰、留白足、配色克制。卡片主题依次是：AI 总结完为什么找不到、收藏不等于沉淀、Codex 接进 Obsidian、一条资料变一篇笔记、不是摘要是资料库记录、适合人群与 GitHub 项目名。

### 视频号

生成 5 张用于视频号竖屏短视频的 9:16 分镜图。风格简洁、移动端可读。主题包括 AI 摘要丢失、Obsidian Inbox 出现、链接生成任务包、笔记和资源目录、GitHub 搜索项目。

### GitHub

生成 5 张用于 GitHub Release / 社交预览的横版图。风格开源项目、README 首屏、Issue 模板、Release notes、Star CTA。强调 local-first、Markdown、Obsidian notes、raw archive、clickable indexes。
