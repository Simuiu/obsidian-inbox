# Obsidian Inbox

![Obsidian Inbox hero](docs/assets/hero.svg)

Codex 半自动内容入库工具：把外部链接和本地材料整理成 Obsidian 资料库里的 Markdown 笔记，并维护可点击的资料库索引、主题索引和用途索引。

当前稳定场景是 Bilibili 视频字幕入库和微信公众号公开文章入库；项目结构已经面向更多文章、图文、小红书、抖音和音频内容扩展。

## 它解决什么问题

多数 AI 总结工具只给一次性答案。`Obsidian Inbox` 更关注总结之后的知识库工作流：

- 资料应该放在哪里；
- 以后能不能通过总索引、主题索引、用途索引找回来；
- 原始转写、正文和来源能不能追溯；
- 普通总结和深度总结是否能让用户一眼区分；
- 本地视频、音频和 cookies 是否避免进入 GitHub 或 iCloud。

![Workflow](docs/assets/workflow.svg)

## 资料库结构

Obsidian Vault 中的资料库目录：

```text
00_资料库
```

索引使用 Folder Notes 友好的结构，能排在资源文件夹前面：

```text
00_资料库/000 资料库索引/000 资料库索引.md
00_资料库/001 主题索引/001 主题索引.md
00_资料库/002 用途索引/002 用途索引.md
```

单条资源结构：

```text
00_资料库/YYMMDD 短标题/YYMMDD 短标题.md
00_资料库/YYMMDD 短标题/_resources
```

![Vault structure](docs/assets/vault-structure.svg)

## 推荐用法

以后直接对 Codex 说：

```text
把这个链接入库：https://...
```

或者：

```text
深度入库这个视频：https://...
```

Codex 应按 `.agents/skills/obsidian-inbox/SKILL.md` 的流程执行。旧的 `video2obsidian` skill 仍保留为兼容入口。

不同平台的具体操作见：

```text
PLATFORM_INGESTION_MANUAL.md
```

隐私与平台边界见：

```text
PRIVACY_AND_LIMITS.md
```

面向用户的完整说明见：

```text
用户手册.md
```

验收步骤见：

```text
验收路径.md
```

后续开发计划和本地测试流程见：

```text
DEVELOPMENT_PLAN.md
```

首次在新机器使用时可以初始化 Vault 路径：

```bash
python3 scripts/init_config.py --vault-path "/path/to/your/ObsidianVault" --force
```

也可以先复制示例配置：

```bash
cp config.example.yaml config.yaml
```

## 手动准备任务包

普通入库：

```bash
python3 scripts/prepare_link.py "https://www.bilibili.com/video/BVxxxx" --sync-raw
```

深度入库：

```bash
python3 scripts/prepare_link.py "https://www.bilibili.com/video/BVxxxx" --sync-raw --mode deep
```

脚本会生成：

```text
tasks/YYYY-MM-DD-platform-id/
├── meta.json
├── compact.md
├── prompt.md
├── transcript_clean.txt
├── transcript_timed.md
└── subtitle*.srt
```

`meta.json` 会给出建议笔记路径和资源目录。字幕、转写、正文等轻量材料保存在单条资源文件夹的 `_resources/`，主笔记只链接，不内嵌全文。本地视频原文件和 ASR 临时音频不进入 Obsidian。

写完笔记后重建索引：

```bash
python3 scripts/rebuild_obsidian_index.py
```

生成可编辑 Obsidian 草稿：

```bash
python3 scripts/render_note.py "tasks/YYYY-MM-DD-platform-id" --write
```

深度草稿：

```bash
python3 scripts/render_note.py "tasks/YYYY-MM-DD-platform-id" --mode deep --write
```

默认不会覆盖已有笔记；确认覆盖时加 `--force`。

## 文件命名

资源文件夹和主总结文件名使用短日期：

```text
YYMMDD 短标题/
└── YYMMDD 短标题.md
```

source ID 不放入文件名；它保存在 frontmatter 里，用于去重和关联原始材料。

## 能力状态

| 来源 | 状态 |
|---|---|
| Bilibili 视频 | 稳定：元数据、AI 字幕、普通/深度笔记 |
| 微信公众号 | 稳定：公开文章标题、公众号、发布时间、正文 Markdown |
| YouTube 视频 | 部分支持：依赖字幕可得性，需继续系统测试 |
| 普通网页 | 部分支持：保守 HTML 正文抽取 |
| 微信视频号 | 支持外部下载器导入：先用 resd-mini / res-downloader / wechatVideoDownload 捕获视频，再导入任务包 |
| 本地公开视频/自有视频 | 支持：本地文件导入、转写文件导入、可选 ASR |
| 小红书 | 支持本地图文/视频导入 |
| 抖音 | 支持本地图文/视频导入 |
| 音频 ASR | 实验脚本可用，尚未作为稳定默认兜底 |

## 原则

- 先入 Inbox，再通过索引和主题页组织。
- 索引必须能点到正文，正文也要能回到索引。
- 每篇笔记要标记用途：学习、实践、素材，后续可继续扩展。
- raw 材料按条目折叠到单条资源文件夹下的 `_resources`，不再堆在扁平 `_raw`。
- 本地视频原文件和 `audio.wav` 不进入 Obsidian/iCloud；主总结只记录本地原路径。
- 字幕或正文抓取失败时，不编造总结。
- 普通总结用于快速入库和第一遍理解；深度总结用于课程、教学、系统整理、本地视频和明确要求“深度”的内容。
- 每篇主笔记必须在 frontmatter 写 `summary_mode: "普通"` 或 `summary_mode: "深度"`，并在 `索引与主题` 中显示 `总结模式：普通/深度`。
- 深度笔记必须明显区别于普通总结，包含问题链、机制拆解、对比表、误区、设计取舍和二次加工卡片。

## 微信视频号

视频号不能稳定通过普通 URL 直接下载。当前集成方式是复用 GitHub 上成熟的本地监听/代理下载器：

- `https://github.com/putyy/resd-mini`
- `https://github.com/putyy/res-downloader`
- `https://github.com/qiye45/wechatVideoDownload`

安装推荐下载器：

```bash
python3 scripts/install_resd_mini.py
```

启动：

```bash
python3 scripts/start_resd_mini.py
```

使用流程：

1. 打开下载器并启动监听/代理。
2. 在微信里打开视频号内容，让下载器捕获视频文件。
3. 将本地视频导入 Obsidian Inbox 任务包：

```bash
python3 scripts/import_wechat_video.py \
  --video "/path/to/video.mp4" \
  --source-url "<WECHAT_CHANNELS_URL>" \
  --title "视频标题" \
  --author "作者"
```

如果已有转写：

```bash
python3 scripts/import_wechat_video.py \
  --video "/path/to/video.mp4" \
  --source-url "<WECHAT_CHANNELS_URL>" \
  --title "视频标题" \
  --author "作者" \
  --transcript "/path/to/transcript.md"
```

没有转写时，任务状态会保持为 `needs_asr`，不会生成假总结。

也可以使用未来兼容更多平台的统一入口：

```bash
python3 scripts/import_media.py \
  --platform wechat_video \
  --video "/path/to/video.mp4" \
  --source-url "<WECHAT_CHANNELS_URL>" \
  --title "视频标题" \
  --author "作者" \
  --asr
```

检查依赖：

```bash
python3 scripts/doctor.py
```

## 本地公开视频测试

使用公开可下载、允许测试使用的 Big Buck Bunny 样例视频跑 smoke test：

```bash
python3 scripts/run_public_media_smoke_test.py
```

脚本默认下载样例、截取短片、导入为 `local_video`、验证任务包与 `_resources`，并清理测试产物。需要保留产物时加：

```bash
python3 scripts/run_public_media_smoke_test.py --keep
```

ASR 单独使用公开音频样例测试：

```bash
python3 scripts/run_public_asr_smoke_test.py
```

微信文章使用公开文章样例测试正文抽取和图片本地化：

```bash
python3 scripts/run_wechat_article_smoke_test.py
```

YouTube 只跑公开 CC 样例的元数据/字幕链路测试，不下载视频正文：

```bash
python3 scripts/run_youtube_public_smoke_test.py
```

一次性跑完整回归：

```bash
python3 scripts/run_all_tests.py
```
