# Video2Obsidian 自动化实现方案

> 目标：让 Codex 读取本 Markdown 文档后，能够基于成熟开源项目或轻量二次开发，帮我实现「输入 YouTube / 哔哩哔哩视频链接 → 自动总结 → 生成 Markdown → 保存到 Obsidian 仓库」的本地自动化工具。

---

## 0. 给 Codex 的总指令

Codex，请先完整阅读本文档，不要立即改代码。你的任务是帮我实现一个本地自动化工具 **Video2Obsidian**。

核心目标：

1. 支持输入 YouTube 视频链接。
2. 支持输入哔哩哔哩视频链接。
3. 优先读取平台已有字幕；没有字幕时，再走音频下载 + ASR 转写。
4. 调用大模型对字幕 / 转写文本进行总结。
5. 按固定模板生成 Markdown 笔记。
6. 将 Markdown 自动保存到我的 Obsidian Vault 指定目录。
7. 支持单条链接处理，也支持批量链接处理。
8. 支持失败记录、成功记录、日志记录，方便后续排查。

你需要优先复用成熟开源项目，不要从 0 重复造轮子。优先评估和复用 BiliNote，其次参考 AI-Video-Transcriber、TubeSage、BiliSummary 等项目。

---

## 1. 我的真实需求重新梳理

我想解决的问题不是单纯“总结一个视频”，而是建立一套可以长期使用的个人知识库自动化流程。

我平时会看到很多 YouTube 和哔哩哔哩视频，里面可能有产品、AI、技术、教程、行业分析等内容。我希望把这些视频内容沉淀到 Obsidian 中，形成可检索、可复用、可回顾的 Markdown 笔记。

理想状态是：

```text
复制一个视频链接
→ 执行一个命令
→ 自动获取字幕或转写音频
→ 自动总结
→ 自动生成 Markdown
→ 自动保存到 Obsidian 指定文件夹
→ 后续我可以直接在 Obsidian 里搜索和整理
```

我不是专业程序员，所以实现方案需要尽量简单、稳定、可维护。Codex 的作用是作为本地开发助手，帮我读代码、改代码、写脚本、补 README、处理报错。

---

## 2. 最终使用效果

### 2.1 单个视频

希望最终可以这样运行：

```bash
video2obsidian "https://www.bilibili.com/video/BVxxxx"
```

或者：

```bash
video2obsidian "https://www.youtube.com/watch?v=xxxx"
```

运行后自动生成：

```text
ObsidianVault/
└── 视频笔记/
    └── 2026-05-01-bilibili-视频标题.md
```

### 2.2 批量处理

希望可以维护一个 `inbox.txt`：

```txt
https://www.bilibili.com/video/BVxxxx
https://www.youtube.com/watch?v=xxxx
```

然后运行：

```bash
video2obsidian batch
```

系统自动逐条处理。

处理成功的链接进入：

```text
processed.txt
```

处理失败的链接进入：

```text
failed.txt
```

同时记录错误原因，方便后续重试。

---

## 3. 推荐实现路线

### 3.1 首选路线：基于 BiliNote 二次改造

优先使用 BiliNote 作为底座。

BiliNote GitHub：

```text
https://github.com/JefferyHcool/BiliNote
```

选择它的原因：

1. 已经支持哔哩哔哩、YouTube、抖音等视频链接。
2. 已经支持自动生成结构化 Markdown 笔记。
3. 已经支持截图、原片跳转、AI 问答等视频笔记能力。
4. 已经支持多种大模型配置。
5. 已经有 Docker / 桌面端 / 源码部署等形态。
6. 比从 0 写视频解析、字幕提取、转写、总结更稳。

Codex 需要先分析 BiliNote 当前代码结构，判断下面这些能力是否已有：

- 视频链接解析；
- 平台识别；
- 字幕获取；
- 无字幕 ASR 转写；
- LLM 总结；
- Markdown 生成；
- 文件导出；
- CLI / API 调用方式；
- 配置文件；
- 任务状态记录。

如果 BiliNote 已经有对应能力，优先复用；如果没有，再做补充。

### 3.2 备选路线：基于 AI-Video-Transcriber 做后端能力

AI-Video-Transcriber GitHub：

```text
https://github.com/wendy7756/AI-Video-Transcriber
```

它适合作为备选底座，尤其适合做“视频 / 音频 → 转写 → 总结”的通用后端能力。

需要重点评估：

1. 是否能稳定支持 YouTube 和 Bilibili。
2. 是否支持字幕优先。
3. 是否支持无字幕时 Whisper / faster-whisper 转写。
4. 是否支持 OpenAI-compatible API。
5. 是否方便输出 Markdown 到指定目录。

### 3.3 不建议作为主底座，但可参考的项目

#### TubeSage

```text
https://github.com/rmccorkl/tubesage
```

优点：Obsidian 插件形态，适合 YouTube 到 Obsidian。  
缺点：主要面向 YouTube，不适合作为同时支持 B 站和 YouTube 的主方案。

#### BiliSummary

```text
https://github.com/jackwener/bilibili-summary
```

优点：偏 B 站总结，支持 Markdown 输出和收藏夹工作流。  
缺点：主要面向 B 站，不适合作为 YouTube + B 站统一入口。

#### BiliSummary iOS

```text
https://github.com/jackwener/bilibili-summary-swift
```

优点：可以参考 B 站批量总结、收藏夹总结的产品思路。  
缺点：iOS 客户端方向，不适合作为本地 Obsidian 自动化主底座。

#### Bilibili Video Summary Agent

```text
https://github.com/Cansiny0320/bilibili-video-summary-agent
```

优点：CLI 形态，输入 B 站 BV 号或链接，生成摘要和关键要点。  
缺点：偏 B 站，不覆盖 YouTube。

#### bilibili-subtitle

```text
https://github.com/HamsteRider-m/bilibili-subtitle
```

优点：可以参考 B 站字幕提取、AI 字幕、无字幕 ASR 兜底逻辑。  
缺点：更像子能力，不是完整 Obsidian 笔记工具。

---

## 4. Codex 应该怎么介入

Codex 不是视频总结工具本身，而是本地自动化开发助手。

Codex 官方文档：

```text
https://developers.openai.com/codex/cli
https://developers.openai.com/codex/noninteractive
https://developers.openai.com/codex/cli/reference
```

Codex 需要做的事：

1. 阅读项目代码。
2. 理清现有能力。
3. 判断最佳改造点。
4. 新增 Obsidian 输出层。
5. 新增批量处理脚本。
6. 新增配置文件。
7. 新增错误日志。
8. 新增 README。
9. 帮我以小白能理解的方式说明如何安装、配置、运行。

---

## 5. 项目命名

建议新工具命名为：

```text
Video2Obsidian
```

命令名建议为：

```bash
video2obsidian
```

---

## 6. 最小可行版本范围

### 6.1 MVP 必须实现

第一版只做这些：

1. 输入单个视频链接。
2. 自动识别 YouTube 或 Bilibili。
3. 获取字幕。
4. 无字幕时给出明确错误，或者走 ASR 兜底。
5. 调用大模型生成总结。
6. 生成 Markdown。
7. 保存到 Obsidian 指定目录。
8. 文件名自动清洗非法字符。
9. 笔记中保留原视频链接。

### 6.2 第一版可以不做

这些先不要做，避免过度复杂：

1. 图形界面。
2. Obsidian 插件。
3. 手机端同步。
4. 自动监听剪贴板。
5. 自动登录 B 站。
6. 自动下载完整视频。
7. 很复杂的标签体系。
8. 多用户系统。
9. Web 服务部署。

---

## 7. 后续增强版本

### 7.1 V0.2：批量处理

增加：

1. `inbox.txt` 批量读取。
2. `processed.txt` 成功记录。
3. `failed.txt` 失败记录。
4. `logs/` 运行日志。
5. 失败任务可重试。

### 7.2 V0.3：知识库增强

增加：

1. 自动标签。
2. 自动分类。
3. 时间戳跳转。
4. 视频截图。
5. 原文转写折叠。
6. 总结风格模板。
7. 按领域生成不同笔记模板，例如 AI、产品、投资、技术教程。

### 7.3 V0.4：半自动工作流

增加：

1. 监听某个 `inbox.md` 文件。
2. 我把视频链接粘进去后，手动运行一次命令即可全部处理。
3. 后续可以考虑加 macOS 快捷指令或 Alfred / Raycast 快捷入口。

---

## 8. 推荐工作流

### 8.1 手动轻量工作流

```text
复制视频链接
→ 打开终端
→ 运行 video2obsidian "视频链接"
→ 打开 Obsidian 查看笔记
```

### 8.2 批量工作流

```text
把多个链接放到 inbox.txt
→ 运行 video2obsidian batch
→ 成功链接进入 processed.txt
→ 失败链接进入 failed.txt
→ Obsidian 中自动出现多篇视频笔记
```

---

## 9. 配置文件设计

建议新建配置文件：

```text
config.yaml
```

示例：

```yaml
obsidian:
  vault_path: "/Users/你的用户名/Documents/ObsidianVault"
  note_folder: "视频笔记"
  asset_folder: "附件/视频截图"
  filename_rule: "{date}-{platform}-{title}.md"

llm:
  provider: "openai_compatible"
  api_base: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"
  model: "gpt-5.5"
  temperature: 0.2

transcription:
  prefer_platform_subtitle: true
  fallback_to_asr: true
  asr_engine: "faster-whisper"
  language: "zh"

summary:
  output_language: "zh-CN"
  style: "产品经理知识库笔记"
  include_transcript: true
  include_timestamps: true
  max_summary_tokens: 3000

batch:
  inbox_file: "inbox.txt"
  processed_file: "processed.txt"
  failed_file: "failed.txt"
  log_dir: "logs"
```

注意：

1. `vault_path` 必须由我自己改成真实的 Obsidian 仓库路径。
2. API Key 不要直接写进配置文件，优先使用环境变量。
3. 如果我使用百炼 / DeepSeek / OpenRouter 等 OpenAI-compatible 服务，需要支持 `api_base` 自定义。

---

## 10. Obsidian Markdown 输出模板

生成的 Markdown 笔记建议使用这个结构：

```md
---
title: "{{title}}"
source: "{{url}}"
platform: "{{platform}}"
author: "{{author}}"
published_at: "{{published_at}}"
created_at: "{{created_at}}"
tags:
  - 视频笔记
  - AI总结
  - "{{platform}}"
---

# {{title}}

## 一句话总结

{{one_sentence_summary}}

## 核心观点

{{key_points}}

## 关键时间点

{{timeline}}

## 可复用内容

{{reusable_insights}}

## 我的思考

> 这里先留空，方便我后续自己补充。

## 原视频信息

- 平台：{{platform}}
- 作者：{{author}}
- 链接：{{url}}
- 发布时间：{{published_at}}
- 总结时间：{{created_at}}

## 原文转写

<details>
<summary>展开查看转写全文</summary>

{{transcript}}

</details>
```

---

## 11. 文件命名规则

为了避免文件名报错，需要对视频标题做清洗。

规则：

1. 去掉 `/ \ : * ? " < > |` 等非法字符。
2. 连续空格替换为一个空格。
3. 文件名太长时截断到 80 个字符左右。
4. 默认命名：

```text
{date}-{platform}-{title}.md
```

示例：

```text
2026-05-01-bilibili-一个产品经理如何使用AI工具.md
2026-05-01-youtube-How to Build AI Agents.md
```

---

## 12. 建议项目目录

如果是新建包装项目，建议目录如下：

```text
Video2Obsidian/
├── README.md
├── AGENTS.md
├── VIDEO2OBSIDIAN_SPEC.md
├── config.example.yaml
├── config.yaml
├── inbox.txt
├── processed.txt
├── failed.txt
├── logs/
├── video2obsidian/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── platform_detect.py
│   ├── transcript.py
│   ├── summarizer.py
│   ├── obsidian_writer.py
│   ├── batch.py
│   └── utils.py
└── tests/
    ├── test_filename.py
    ├── test_platform_detect.py
    └── test_markdown_render.py
```

如果是直接改造 BiliNote，则 Codex 需要先判断 BiliNote 的真实目录结构，再把上述能力合并到合适位置，不要硬套目录。

---

## 13. CLI 命令设计

### 13.1 初始化配置

```bash
video2obsidian init
```

生成：

```text
config.yaml
inbox.txt
processed.txt
failed.txt
logs/
```

### 13.2 单链接处理

```bash
video2obsidian run "https://www.bilibili.com/video/BVxxxx"
```

或简写：

```bash
video2obsidian "https://www.youtube.com/watch?v=xxxx"
```

### 13.3 批量处理

```bash
video2obsidian batch
```

### 13.4 检查配置

```bash
video2obsidian doctor
```

检查：

1. Obsidian Vault 路径是否存在。
2. `note_folder` 是否存在，不存在则创建。
3. ffmpeg 是否安装。
4. API Key 是否存在。
5. 模型配置是否可用。
6. BiliNote / 依赖服务是否可调用。

---

## 14. 大模型总结 Prompt 模板

建议使用如下 Prompt：

```text
你是一个专业的视频内容整理助手，擅长把视频字幕整理成适合 Obsidian 知识库保存的 Markdown 笔记。

请基于下面的视频信息和字幕内容，生成结构化中文笔记。

要求：
1. 不要编造字幕中没有的信息。
2. 重点提炼观点、结论、方法和可复用经验。
3. 如果字幕中有明显时间线，请生成关键时间点。
4. 如果内容适合产品经理、AI 工具使用、个人知识管理，请额外提炼“可复用内容”。
5. 输出必须是 Markdown。
6. 不要输出无关寒暄。

视频信息：
标题：{{title}}
平台：{{platform}}
作者：{{author}}
链接：{{url}}

字幕内容：
{{transcript}}

请按以下结构输出：

## 一句话总结

## 核心观点

## 关键时间点

## 可复用内容

## 我的思考
> 留空，等待用户补充。
```

---

## 15. Codex 第一阶段任务

Codex 先做“分析”，不要急着写代码。

请 Codex 执行：

```text
请你先阅读当前目录和相关项目代码，不要修改任何文件。

请输出一份分析报告，回答：

1. 当前项目是否已经具备视频链接解析能力？
2. 当前项目是否支持 YouTube？
3. 当前项目是否支持 Bilibili？
4. 当前项目是否支持字幕优先？
5. 当前项目是否支持无字幕 ASR？
6. 当前项目是否已经能生成 Markdown？
7. 当前项目是否支持命令行调用？
8. 当前项目是否支持自定义输出目录？
9. 最适合新增 Obsidian 输出层的位置在哪里？
10. 最适合新增 batch 批处理的位置在哪里？
11. 你计划修改哪些文件？为什么？
12. 你认为第一版最小改动方案是什么？

先给我修改计划，等我确认后再开始改。
```

---

## 16. Codex 第二阶段任务：实现 MVP

确认修改计划后，让 Codex 执行：

```text
请按刚才确认的计划实现 MVP：

1. 新增或完善配置文件 config.yaml。
2. 支持配置 Obsidian Vault 路径。
3. 支持配置笔记保存目录。
4. 支持输入单个 YouTube / Bilibili 链接。
5. 复用现有字幕 / 转写 / 总结能力。
6. 按模板生成 Markdown。
7. 写入 Obsidian 指定目录。
8. 文件名自动清洗非法字符。
9. 提供命令行入口。
10. 更新 README，给出小白可复制运行的步骤。

实现后请运行最小测试，并告诉我：
- 改了哪些文件；
- 新增了哪些命令；
- 如何配置；
- 如何运行；
- 还存在哪些限制。
```

---

## 17. Codex 第三阶段任务：批量处理

MVP 跑通后，再让 Codex 做批量：

```text
请在 MVP 基础上新增 batch 模式：

1. 从 inbox.txt 读取视频链接。
2. 忽略空行和 # 开头的注释行。
3. 逐条处理链接。
4. 成功后写入 processed.txt。
5. 失败后写入 failed.txt，记录失败原因。
6. 每次运行生成日志文件。
7. 避免重复处理 processed.txt 中已有链接。
8. README 中补充批量处理教程。

请先给修改计划，确认后再动代码。
```

---

## 18. 验收标准

### 18.1 功能验收

必须满足：

- [ ] 输入一个 B 站链接，可以生成 Markdown。
- [ ] 输入一个 YouTube 链接，可以生成 Markdown。
- [ ] Markdown 能保存到 Obsidian Vault 指定目录。
- [ ] Markdown 中包含原视频链接。
- [ ] Markdown 中包含标题、平台、总结时间、标签。
- [ ] 文件名不包含非法字符。
- [ ] 没有字幕时有明确提示或 ASR 兜底。
- [ ] 配置文件可修改 Vault 路径。
- [ ] README 能让小白照着跑通。

### 18.2 批量验收

- [ ] `inbox.txt` 中多个链接可以逐个处理。
- [ ] 成功任务写入 `processed.txt`。
- [ ] 失败任务写入 `failed.txt`。
- [ ] 失败原因可读。
- [ ] 重复运行不会重复生成同一篇笔记，或至少有明确去重策略。

---

## 19. 风险和注意事项

### 19.1 B 站风险

1. 部分 B 站视频没有字幕。
2. 部分视频需要登录或 Cookie。
3. B 站页面结构可能变化，导致解析失败。
4. 分 P 视频需要额外处理。

### 19.2 YouTube 风险

1. 部分视频没有字幕。
2. 部分视频字幕不可下载。
3. 部分地区网络访问受限。
4. 公开视频、会员视频、年龄限制视频处理方式不同。

### 19.3 ASR 风险

1. 无字幕视频如果走 ASR，需要 ffmpeg。
2. Whisper / faster-whisper 对电脑性能有要求。
3. 长视频处理时间较长。
4. 本地模型会占用磁盘和内存。

### 19.4 API Key 风险

1. 不要把 API Key 写进 Git 仓库。
2. 配置文件中只写环境变量名。
3. README 中要说明如何设置环境变量。
4. 如果使用百炼、DeepSeek、OpenRouter，需要支持 OpenAI-compatible API Base URL。

### 19.5 Obsidian 路径风险

1. Vault 路径不能写错。
2. 文件夹不存在时应自动创建。
3. macOS 路径中可能有空格。
4. iCloud 同步目录可能存在延迟。
5. 文件名必须清洗非法字符。

---

## 20. 给我的小白使用步骤

最终 README 需要提供类似步骤：

### 20.1 安装依赖

```bash
git clone https://github.com/JefferyHcool/BiliNote.git
cd BiliNote
```

然后按照项目实际说明安装依赖。

### 20.2 放入本规格文档

把本文档放到项目根目录：

```text
VIDEO2OBSIDIAN_SPEC.md
```

### 20.3 启动 Codex

```bash
codex
```

### 20.4 给 Codex 的第一句话

```text
请先阅读 VIDEO2OBSIDIAN_SPEC.md 和当前项目代码。不要修改文件。先输出一份实现方案和修改计划。
```

### 20.5 确认后再让 Codex 改

```text
同意你的 MVP 方案。请开始实现，但每完成一个阶段都要告诉我改了哪些文件、如何测试。
```

---

## 21. 建议额外创建 AGENTS.md

为了让 Codex 每次进入项目都知道规则，建议创建：

```text
AGENTS.md
```

内容如下：

```md
# AGENTS.md

## 项目目标

本项目目标是实现 Video2Obsidian：将 YouTube / Bilibili 视频自动总结成 Markdown，并保存到 Obsidian Vault。

## 开发规则

1. 不要从 0 重复造轮子，优先复用现有项目能力。
2. 修改前先说明计划。
3. 不要把 API Key 写入代码或配置文件。
4. 所有路径都要支持 macOS。
5. 所有输出 Markdown 必须兼容 Obsidian。
6. 文件名必须清洗非法字符。
7. README 必须给出小白可复制执行的步骤。
8. 优先实现 MVP，再做批量能力。
9. 如果遇到 B 站或 YouTube 限制，要给出明确错误提示。
10. 每次改完代码，说明改了哪些文件、如何测试。
```

---

## 22. 给 Codex 的可复制总 Prompt

下面这段可以直接复制给 Codex：

```text
请先阅读当前目录下的 VIDEO2OBSIDIAN_SPEC.md。

我的目标是实现一个 Video2Obsidian 工具：输入 YouTube 或哔哩哔哩视频链接，自动获取字幕或转写音频，调用大模型总结，生成 Markdown，并保存到我的 Obsidian Vault 指定目录。

请你先不要修改文件。先完成以下分析：

1. 当前项目有哪些能力可以复用？
2. 是否支持 YouTube 和 Bilibili？
3. 是否支持字幕优先？
4. 是否支持无字幕时 ASR 兜底？
5. 是否能生成 Markdown？
6. 是否有 CLI 或 API 可以直接调用？
7. 最小改造路径是什么？
8. 你计划新增 / 修改哪些文件？
9. MVP 版本预计实现哪些功能？
10. 有哪些风险和依赖？

请先输出修改计划，等我确认后再开始改代码。
```

---

## 23. 我当前的方案选择

当前建议：

```text
主方案：BiliNote + Codex 二次改造
备选方案：AI-Video-Transcriber + 自定义 Obsidian 输出层
不推荐主方案：单独使用 TubeSage，因为它主要适合 YouTube，不覆盖 B 站
```

原因：

```text
BiliNote 已经覆盖视频解析、字幕 / 转写、AI 总结、Markdown 生成等核心能力。
Codex 只需要重点补齐 Obsidian 输出、批量处理、配置文件、README 和命令行体验。
这样开发成本最低，成功率最高。
```

---

## 24. 需要我手动确认 / 修改的参数

开始实现前，我需要根据自己的电脑改这些内容：

```yaml
obsidian:
  vault_path: "/Users/你的用户名/Documents/ObsidianVault"
  note_folder: "视频笔记"
  asset_folder: "附件/视频截图"
```

如果我不知道自己的 Obsidian Vault 路径，可以打开 Obsidian：

```text
设置 → 文件与链接 / 或管理仓库 → 查看仓库所在路径
```

也可以在 Finder 中找到 Vault 文件夹后，右键复制路径。

---

## 25. 最终一句话

不要把这个项目做复杂。第一目标是跑通：

```text
一个视频链接 → 一篇 Obsidian Markdown 笔记
```

跑通后，再做批量、截图、标签、时间戳、自动分类等增强能力。
