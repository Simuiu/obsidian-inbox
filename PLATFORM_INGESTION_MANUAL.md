# Obsidian Inbox 平台入库操作手册

这份手册说明：你在不同平台看到内容时，应该怎么把材料交给 `obsidian-inbox`，以及当前哪些能力是稳定的、哪些需要额外步骤。

## 总原则

- 能直接给链接的平台，直接发“入库这个链接”或“深度入库这个链接”。
- 需要客户端或下载器的平台，先把原始材料抓到本地，再用导入脚本进入 Obsidian Inbox。
- 没有正文、字幕或转写时，不生成完整总结，只记录材料状态。
- 所有 raw 材料统一进单条资源文件夹下的 `_resources/`，正文只放总结和链接。本地视频原文件和 ASR 临时音频不进入 Obsidian。

## Bilibili 视频

适合：课程、技术讲解、访谈、长视频。

你要做：

```text
入库这个链接：https://www.bilibili.com/video/BV...
```

或：

```text
深度入库这个链接：https://www.bilibili.com/video/BV...
```

系统会做：

- 抓视频元数据。
- 优先用 `secrets/bilibili.cookies.txt` 获取 B 站 AI 字幕。
- 生成 `compact.md`。
- 生成普通或深度 Obsidian 笔记。
- 保存字幕和带时间点转写到 `_resources`。
- 更新总索引、主题索引、用途索引。

注意：

- 如果字幕需要登录，确认 Chrome 已登录 B 站，或维护好 `secrets/bilibili.cookies.txt`。
- 字幕抓不到时不会编造总结。

## YouTube 视频

适合：英文课程、技术演讲、产品发布、访谈。

你要做：

```text
入库这个 YouTube 链接：https://www.youtube.com/watch?v=...
```

系统会尝试：

- 抓视频元数据。
- 获取人工字幕或自动字幕。
- 优先中文字幕；没有中文时可用英文字幕生成中文笔记。

当前状态：

- 代码路径已接入 `yt-dlp`。
- 还需要继续用真实 YouTube 链接做系统测试。

失败时：

- 如果没有字幕，当前不会直接编造总结。
- 如果 YouTube 要求登录或机器人校验，任务会标记为 `metadata_capture_failed`，不会尝试绕过。
- 后续可以接 ASR 兜底。

## 微信公众号文章

适合：长文、技术文章、产品分析、商业评论。

你要做：

```text
入库这篇微信文章：https://mp.weixin.qq.com/s/...
```

系统会做：

- 抓标题。
- 抓公众号名。
- 抓发布时间。
- 抓正文 Markdown。
- 保存原始 HTML 和正文 Markdown 到 `_resources`。
- 生成文章笔记和索引。

注意：

- 当前支持公开可访问文章。
- 图片会尝试本地化保存到任务包和 `_resources/images/`；失败会写入 `article_diagnostics.json`，正文入库不中断。
- 如果只抓到标题或元数据，不生成完整总结。

## 微信视频号

适合：短视频、直播切片、经验分享、产品/商业观察。

视频号不能稳定通过普通 URL 直接下载。当前支持“本地捕获后半自动入库”：Codex 可以协助安装/启动捕获工具、定位新捕获的 `.mp4`、导入任务包并尝试 ASR；用户仍需要在微信客户端里打开并播放目标视频。

推荐 GitHub 工具：

- `https://github.com/putyy/resd-mini`
- `https://github.com/putyy/res-downloader`
- `https://github.com/qiye45/wechatVideoDownload`

半自动流程：

你可以直接对 Codex 说：

```text
帮我半自动入库这个微信视频号。我会在微信里打开并播放它，来源是 ...
```

Codex 可以协助执行：

1. 安装下载器：

```bash
python3 scripts/install_resd_mini.py
```

2. 启动下载器：

```bash
python3 scripts/start_resd_mini.py
```

3. 提示用户在下载器界面启动监听或代理。
4. 提示用户在微信里打开并播放视频号内容。
5. 定位下载器捕获并保存的本地视频文件。
6. 把本地视频导入任务包。
7. 如果有转写则生成笔记；如果没有转写，可尝试 ASR；如果没有可靠转写或 ASR 不可用，只标记材料状态。

如果你已经手动安装了其他下载器，也可以跳过前两步。

原始手动导入流程：

1. 打开下载器。
2. 启动监听或代理。
3. 在微信里打开视频号内容。
4. 等下载器捕获并保存视频文件。
5. 把本地视频导入：

```bash
python3 scripts/import_wechat_video.py \
  --video "/path/to/video.mp4" \
  --source-url "视频号原链接" \
  --title "视频标题" \
  --author "作者"
```

如果你已经有转写：

```bash
python3 scripts/import_wechat_video.py \
  --video "/path/to/video.mp4" \
  --source-url "视频号原链接" \
  --title "视频标题" \
  --author "作者" \
  --transcript "/path/to/transcript.md"
```

如果要自动 ASR：

```bash
python3 scripts/import_media.py \
  --platform wechat_video \
  --video "/path/to/video.mp4" \
  --source-url "视频号原链接" \
  --title "视频标题" \
  --author "作者" \
  --asr
```

注意：

- 自动 ASR 需要本机安装 `ffmpeg`。
- 没有转写时状态是 `needs_asr`，不生成假总结。
- 视频文件最终仍然需要先落到本地，项目才会继续处理；项目不承诺只靠一个视频号 URL 直接下载。

## 本地公开视频或自有视频

适合：公开授权测试素材、你自己录制的视频、已经合法下载到本地的课程或访谈。

你要做：

```bash
python3 scripts/import_media.py \
  --platform local_video \
  --video "/path/to/video.mp4" \
  --source-url "原始公开页面或来源说明" \
  --title "视频标题" \
  --author "作者" \
  --transcript "/path/to/transcript.md"
```

如果没有转写，可以使用本机 ASR：

```bash
python3 scripts/import_media.py \
  --platform local_video \
  --video "/path/to/video.mp4" \
  --source-url "原始公开页面或来源说明" \
  --title "视频标题" \
  --author "作者" \
  --asr \
  --asr-model tiny \
  --language en
```

回归测试：

```bash
python3 scripts/run_public_media_smoke_test.py
```

注意：

- 只导入你有权访问和保存的本地文件。
- 测试脚本使用公开可下载、允许测试的样例视频，默认会清理测试产物。
- ASR 输出过短时会标记为 `needs_asr_review`，不会进入完整总结流程。

## 普通网页文章

适合：博客、新闻、文档、公开网页。

你要做：

```text
入库这个网页：https://...
```

系统会尝试：

- 保守抓取 HTML。
- 转成 Markdown。
- 生成文章任务包。

当前状态：

- 基础 HTML 抽取可用。
- 对复杂 JS 页面、登录页、付费墙不保证。

后续计划：

- 接 Chrome CDP + Readability。
- 支持用户登录后手动确认页面已加载再抓取。

## 小红书

当前支持合规的本地导出导入。

图文导入：

```bash
python3 scripts/import_article_export.py \
  --platform xiaohongshu \
  --content "/path/to/content.md" \
  --image-dir "/path/to/images" \
  --source-url "原始链接或来源说明" \
  --title "标题" \
  --author "作者"
```

视频导入：

```bash
python3 scripts/import_media.py \
  --platform xiaohongshu \
  --video "/path/to/video.mp4" \
  --source-url "原始链接或来源说明" \
  --title "标题" \
  --author "作者" \
  --transcript "/path/to/transcript.md"
```

注意：

- 当前不绕过登录或反爬。
- 优先处理你本地已经合法保存的图文、图片、视频和转写。

## 抖音

当前支持合规的本地导出导入。

图文导入：

```bash
python3 scripts/import_article_export.py \
  --platform douyin \
  --content "/path/to/content.md" \
  --image-dir "/path/to/images" \
  --source-url "原始链接或来源说明" \
  --title "标题" \
  --author "作者"
```

视频导入：

```bash
python3 scripts/import_media.py \
  --platform douyin \
  --video "/path/to/video.mp4" \
  --source-url "原始链接或来源说明" \
  --title "标题" \
  --author "作者" \
  --transcript "/path/to/transcript.md"
```

## 用途分类怎么选

每篇笔记可以有多个用途：

- `学习`：我要理解概念、系统复习、建立框架。
- `实践`：我要照着做、拆路数、落到项目或流程。
- `素材`：我要保存案例、观点、表达、选题或证据。

建议：

- 技术教程：`学习` + `实践`
- 案例分析：`学习` + `素材`
- 方法论文章：`学习` + `实践`
- 选题/观点：`素材`
- 暂时不知道用途：先标 `学习`，后续整理时再改。

## 常用命令

重建索引：

```bash
python3 scripts/rebuild_obsidian_index.py
```

迁移/修复旧笔记结构：

```bash
python3 scripts/migrate_obsidian_inbox.py
```

检查脚本语法：

```bash
python3 -m py_compile scripts/*.py
```

检查运行依赖：

```bash
python3 scripts/doctor.py
```

运行公开视频 smoke test：

```bash
python3 scripts/run_public_media_smoke_test.py
```

运行公开 ASR smoke test：

```bash
python3 scripts/run_public_asr_smoke_test.py
```

运行微信文章 smoke test：

```bash
python3 scripts/run_wechat_article_smoke_test.py
```

运行 YouTube 公开 CC 样例 smoke test：

```bash
python3 scripts/run_youtube_public_smoke_test.py
```

一次性运行完整回归：

```bash
python3 scripts/run_all_tests.py
```
