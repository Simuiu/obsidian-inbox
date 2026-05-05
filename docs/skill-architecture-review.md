# Obsidian Inbox Skill 产品架构评估与迭代建议

## 结论

`obsidian-inbox` 已经具备一个优秀 AI skill 的核心形态：它不是单纯的提示词模板，而是把 Codex 操作流程、本地采集脚本、任务包、Obsidian 信息架构、失败边界和回归测试组合成了一个半自动内容入库产品。

从专业 AI 产品架构视角看，它当前最强的资产是“可验证的本地流水线”和“不编造总结”的边界意识；最需要补强的是“配置化发布”“统一任务状态模型”“可观测性”和“面向 GitHub 新用户的 5 分钟成功路径”。

## 当前产品定位

一句话定位：

> 一个面向 Obsidian 用户的本地 AI 内容入库 skill，把视频、文章、图文和本地媒体整理成可检索、可复用、带索引的 Markdown 知识条目。

核心用户：

- 重度 Obsidian 用户
- AI / 产品 / 技术学习者
- 需要长期沉淀视频、文章、图文内容的创作者
- 不希望把全部原始材料上传到第三方 SaaS 的本地优先用户

核心差异：

- 不是“总结一次内容”，而是“把内容稳定纳入个人知识库”
- 不是纯网页应用，而是 Codex + 本地脚本 + Obsidian Vault 的协同工作流
- 明确保留 raw materials，并通过 `_resources/{entry_id}` 形成可追溯结构
- 有普通笔记和深度笔记两种信息密度
- 索引、主题、用途三层组织让内容越积越多时仍可导航

## 架构评价

### 1. Skill 设计

优点：

- `SKILL.md` 的触发语义清晰，覆盖“入库、深度入库、整理到 Obsidian”等自然语言意图。
- 工作流明确规定先生成任务包，再读取 `meta.json`、`compact.md`、`prompt.md`，符合低 token 和渐进披露原则。
- 标准笔记与深度笔记模板区分明显，深度模式强调问题链、机制、误区、取舍和卡片化再加工。
- 明确规定失败时不得编造总结，这是内容入库类 AI 产品的关键质量底线。

问题：

- `SKILL.md` 中固定路径仍偏个人机器，不利于 GitHub 发布和多人复用。
- 支持来源的“Stable / Partial / Planned”存在于 README 和 skill 内，但还没有统一机器可读能力表。
- WeChat Channels 工作流较长，适合拆成 reference 文档，主 `SKILL.md` 只保留决策和入口。

建议：

- 将固定路径改为配置读取优先，个人路径仅作为当前实例示例。
- 新增 `references/platforms.md` 或 `references/source_matrix.md`，保存平台状态、输入要求、失败状态和脚本入口。
- `SKILL.md` 保留核心流程，平台细节按需读取，降低触发后的上下文成本。

### 2. 本地流水线

优点：

- `prepare_link.py`、`import_media.py`、`render_note.py`、`rebuild_obsidian_index.py` 形成了清晰的 ingestion pipeline。
- 任务包结构把 raw、compact、prompt、meta 分开，适合 Codex 只读取压缩上下文。
- 微信文章、本地视频、本地图文、ASR、YouTube 安全路径都有 smoke test，说明项目已经从“脚本集合”进入“可验收产品”阶段。

问题：

- 入口命令仍偏分散，新用户需要理解多个脚本。
- 任务状态虽然存在，但缺少统一枚举文档和状态转移图。
- 失败诊断分散在各平台脚本产物中，不利于 GitHub 用户自助排错。

建议：

- 新增统一 CLI，例如 `python3 scripts/inbox.py ingest <url> --deep`，内部路由到现有脚本。
- 定义 `status` 枚举：`metadata_captured`、`subtitle_captured`、`article_captured`、`transcript_captured`、`needs_subtitle_or_asr`、`needs_asr`、`needs_asr_review`、`metadata_capture_failed`、`capture_failed`。
- 增加 `tasks/<id>/diagnostics.json` 的统一格式，聚合平台、依赖、网络、登录态、正文长度、字幕长度、资源同步结果。

### 3. Obsidian 信息架构

优点：

- 主笔记、资源目录、总索引、主题索引、用途索引的分层合理。
- `entry_id` 放在 frontmatter 和资源目录，不放文件名，兼顾可读性与稳定关联。
- `purposes` 将内容从“收藏”推进到“可学习、可实践、可复用素材”。

问题：

- 主题识别目前依赖 Codex 写笔记时判断，缺少一致性约束。
- 随着内容增多，主题索引可能出现同义词漂移，如“AI 产品”“AI产品”“人工智能产品”。

建议：

- 新增可选 `topics.yaml`，维护规范主题名、别名和合并规则。
- 在 `rebuild_obsidian_index.py` 中加入主题规范化和 orphan note 检查。
- 对用途建立更明确的选择准则：学习、实践、素材可以多选，但默认不要全选。

### 4. 合规与隐私边界

优点：

- 明确不绕过登录、验证码、付费墙，不上传 Vault 和 cookies。
- 对微信视频号、小红书、抖音采用“本地合法材料导入”的稳妥路径。
- 字幕或正文抓取失败时不生成假总结，适合公开发布。

问题：

- GitHub README 需要把这部分前置，否则用户可能误解为“全平台自动爬取器”。
- `secrets/` 目录需要确保永不提交真实 cookie。

建议：

- README 首屏加入 “Local-first, no fake summaries, no bypassing platform access controls”。
- 增加 `scripts/doctor.py --privacy-check` 或发布前检查，扫描真实 cookie、绝对私有路径、tasks raw materials。

## 产品路线建议

### P0：GitHub 发布前必须完成

- 将 README 从个人使用说明改成开源项目首页。
- 确认 `.gitignore` 排除真实 `secrets/*`、`tasks/*`、私有 `_resources`。
- 提供 `config.example.yaml` 和首次初始化命令。
- 跑通 `python3 scripts/run_all_tests.py --skip-network`。
- 用公开样例生成 1-2 个脱敏 demo note，作为 README 展示素材。

### P1：提高新用户成功率

- 做一个统一入口命令：`inbox ingest <url>`、`inbox import-media ...`、`inbox rebuild-index`。
- 新增 `--dry-run`，只生成任务包和诊断，不写 Vault。
- 新增 `doctor` 输出“下一步建议”，而不只是依赖是否存在。
- 在 README 加 5 分钟 quickstart、常见失败、平台能力矩阵。

### P2：增强产品护城河

- 主题规范化与重复内容检测。
- 深度笔记的结构评分器，检查是否真的包含问题链、机制、误区和行动项。
- 多模型 provider 配置，用于不同用户的 LLM 偏好。
- Obsidian Dataview 友好的 frontmatter schema。

### P3：社区增长能力

- 提供 example vault。
- 增加 demo GIF 或短视频。
- 建立 issue templates：平台支持请求、抓取失败、笔记模板建议。
- 加入 GitHub Topics：`obsidian`、`codex`、`ai-notes`、`knowledge-management`、`bilibili`、`wechat`、`youtube`、`markdown`、`local-first`。

## 建议的产品叙事

不要把项目包装成“万能视频总结器”。更准确、更有吸引力的叙事是：

> Obsidian Inbox turns Codex into a local content librarian: it captures links and local media, creates compact task packages, writes structured Obsidian notes, preserves raw materials, and rebuilds clickable knowledge indexes.

中文版本：

> Obsidian Inbox 把 Codex 变成你的本地知识入库员：它读取链接和本地材料，生成任务包，写成结构化 Obsidian 笔记，保留原始材料，并自动维护可点击索引。

这个叙事比“AI 总结视频”更强，因为它强调长期知识资产、可追溯、本地优先和可维护。

