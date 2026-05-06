# AGENTS.md

## 项目目标

本项目用于把外部视频 / 文章 / 图文链接整理进 Obsidian Vault `bling` 的资料库。

当前主流程是 Codex 半自动：

```text
链接 -> 本地脚本抓字幕/正文 -> 生成 compact.md -> Codex 生成 Obsidian 笔记 -> 重建索引
```

## 固定路径

- 项目目录：`/Users/longhuadmin/obsidian-inbox`
- Obsidian Vault：`/Users/longhuadmin/Library/Mobile Documents/iCloud~md~obsidian/Documents/bling`
- 资料库目录：`00_资料库`
- 总索引：`00_资料库/000 资料库索引/000 资料库索引.md`
- 主题索引：`00_资料库/001 主题索引/001 主题索引.md`
- 用途索引：`00_资料库/002 用途索引/002 用途索引.md`
- 单条资源结构：`00_资料库/YYMMDD 短标题/YYMMDD 短标题.md`
- 单条辅助材料：`00_资料库/YYMMDD 短标题/_resources`

## 低 Token 规则

1. 用户要求“入库链接 / 深度入库 / 整理到 Obsidian”时，优先使用 `.agents/skills/obsidian-inbox/SKILL.md`。
2. 普通模式先运行 `python3 scripts/prepare_link.py "<URL>" --sync-raw`。
3. 深度模式先运行 `python3 scripts/prepare_link.py "<URL>" --sync-raw --mode deep`。
4. 默认只读取任务包里的 `meta.json`、`compact.md`、`prompt.md`。
5. 不要读取完整 SRT、`transcript_timed.md` 或文章 `content.md`，除非 `compact.md` 明显不足。
6. 不要把完整字幕贴进对话。
7. 主笔记只保留总结、重点、时间点、行动清单和资源链接。
8. 写完笔记后运行 `python3 scripts/rebuild_obsidian_index.py`。
9. 如果字幕或正文抓取失败，不要编造总结。
10. ASR 只有在转写质量可检查且可用时才作为兜底。

## 微信文章规则

- `mp.weixin.qq.com` 公开文章走本地文章采集器。
- 必须抓到正文后才能总结；只抓到标题或元数据时不得生成完整总结。
- 原始 HTML 和正文 Markdown 存入单条资源文件夹下的 `_resources/`。
- 图片默认保留远程链接，后续再做本地化下载。

## 微信视频号规则

- 识别 `channels.weixin.qq.com` 和 `finder.video.qq.com` 为微信视频号。
- 使用外部 GitHub 下载器捕获视频文件：`resd-mini` / `res-downloader` / `wechatVideoDownload`。
- 本地视频文件优先用统一入口 `python3 scripts/import_media.py --platform wechat_video --video ... --source-url ... --title ...` 导入。
- 也可以直接用底层脚本 `python3 scripts/import_wechat_video.py --video ... --source-url ... --title ...`。
- 没有转写时状态为 `needs_asr`，不得生成总结。
- 只有提供转写或 ASR 结果后，才能生成普通/深度笔记。

## 命名和结构

- 资源文件夹和主总结文件名：`YYMMDD 短标题`。
- 每个资源默认只有一篇主总结；视频主总结默认使用深度总结内容。
- 普通总结用于快速入库；深度总结用于课程、教学、系统整理、本地视频和明确要求“深度”的内容。
- frontmatter 必须写 `summary_mode: "普通"` 或 `summary_mode: "深度"`，正文 `索引与主题` 中也要显示 `总结模式：普通/深度`。
- source ID 不放文件名，保存在 frontmatter。
- 普通总结如需保留，归档到 `_resources/普通总结归档.md`。
- 本地视频原文件和 `audio.wav` 不进入 Obsidian，只在主总结中记录本地路径。
- 正文要链接资料库索引和主题索引，索引要能直接点到主总结。
- 正文和 frontmatter 要标明用途：学习、实践、素材，或后续新增用途。

## B 站规则

- 默认优先读取 `secrets/bilibili.cookies.txt`。
- 如果 Cookie 文件不存在，再回退读取 Chrome 登录 Cookie。
- 如果提示字幕需要登录，先确认 Chrome 是否已登录 B 站。
- Safari Cookie 不一定能读到有效 B 站登录态。

## 输出要求

完成后只简短说明：

- 是否成功；
- 生成的 Obsidian 笔记路径；
- 资源目录路径；
- 索引是否更新；
- 是否有失败或限制。
