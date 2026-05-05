# Obsidian Inbox 后续开发计划

## 产品目标

把分散在视频、文章、图文、短视频里的内容，稳定沉淀到 Obsidian，形成一个可搜索、可回看、可分类、可实践的个人知识库。

核心体验保持简单：

```text
给链接或本地文件 -> 生成任务包 -> 产出 Obsidian 笔记 -> 自动更新索引
```

## 当前已具备能力

| 内容来源 | 当前状态 | 适合用途 |
|---|---|---|
| Bilibili | 稳定，依赖可获取字幕 | 学习、实践 |
| 微信公众号公开文章 | 稳定，支持正文 Markdown | 学习、素材 |
| 普通网页文章 | 可用，复杂 JS 页面待增强 | 学习、素材 |
| 微信视频号 | 可导入本地捕获视频，支持转写或 ASR | 实践、素材 |
| 本地视频 | 可导入本地公开样例或自有视频 | 测试、学习 |
| YouTube | 基础路径已有，待系统测试 | 学习 |
| 小红书 | 支持本地图文/视频导入 | 素材、实践 |
| 抖音 | 支持本地图文/视频导入 | 素材、实践 |

## 下一阶段优先级

1. 稳定本地回归测试

   每次发布前跑公开公开视频 smoke test、微信公众号公开文章回归、索引重建和脚本语法检查。先保证核心入库链路不会退化。

2. 增强微信文章入库

   继续提升正文抽取质量，增加图片本地化、封面保存、引用来源标记和失败诊断。目标是公开可访问微信文章尽量做到标题、作者、时间、正文都完整。

3. 视频号真实流程验证

   在用户本机微信客户端授权环境下，用 `resd-mini` 或同类工具捕获用户自己可访问的视频号内容，再进入本地视频导入链路。系统不绕过登录、不抓无权限内容。

4. YouTube 系统测试

   用官方或 Creative Commons 视频测试字幕抓取、英文转中文笔记、无字幕时的 ASR 兜底。

5. 图文平台扩展

   小红书、抖音先采用“用户本地提供导出材料或本地视频文件”的合规路径，再评估公开链接可抓取能力。图文重点是正文、图片、发布时间和作者归档。

6. 发布到 GitHub 前整理

   把个人绝对路径改为初始化配置，提供示例 Vault 结构、示例命令、公开测试素材说明和常见失败处理。

## 本地测试流程

推荐顺序：

```bash
python3 -m py_compile scripts/*.py
python3 scripts/doctor.py
python3 scripts/run_public_media_smoke_test.py
python3 scripts/run_public_asr_smoke_test.py
python3 scripts/run_wechat_article_smoke_test.py
python3 scripts/run_youtube_public_smoke_test.py
python3 scripts/run_local_export_smoke_test.py
python3 scripts/rebuild_obsidian_index.py
```

也可以一次性运行：

```bash
python3 scripts/run_all_tests.py
```

公开媒体 smoke test 使用 GitHub 上的 Big Buck Bunny 30 秒测试样例，项目 README 标注其用于视频测试，且 Big Buck Bunny 使用 Creative Commons Attribution 3.0 许可。脚本默认下载样例、截取短片、生成测试任务、验证 `meta.json` / `compact.md` / 转写 / 资源目录，然后清理测试产物。

保留测试产物：

```bash
python3 scripts/run_public_media_smoke_test.py --keep
```

公开视频样例主要验证“本地文件导入 + 转写入库 + 资源归档”。ASR 另用带清晰人声、授权明确的素材单独测试，避免把无对白视频误判为转写失败。

YouTube 测试使用公开 CC 样例，只验证元数据、字幕状态和失败安全，不下载视频文件。

## 发布前检查清单

- README 不包含只能在个人机器上成立的假设。
- `config.yaml` 支持用户初始化自己的 Vault 路径。
- 所有入库失败都能给出明确状态，不生成假总结。
- 测试素材来自公开可下载、允许测试使用的来源。
- 微信、抖音、小红书等平台只处理用户有权访问并本地提供的内容。
