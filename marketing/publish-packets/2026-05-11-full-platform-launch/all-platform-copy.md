# 05 Obsidian Inbox 全平台首轮发布物料包

## 1. 使用说明

本发布包用于 `Obsidian Inbox` 第一轮外部引流。所有平台统一导向：

https://github.com/Simuiu/obsidian-inbox

统一口径：

> 把 Codex 变成你的本地知识入库员：链接进来，Obsidian 笔记、原始材料和可点击索引自动生成。

发布边界：

- 不宣传“全平台一键下载”。
- 不宣传“绕过登录、验证码、付费墙”。
- 不宣传“无人值守自动运营”。
- 强调 local-first、可追溯、失败安全、人工确认边界。

配图使用：

- 每个平台至少使用 5 张配图。
- 长文平台按正文中的“插图位”插入。
- 小红书按卡片顺序上传。
- B 站和视频号优先上传视频文件，再上传封面/首帧图。
- HTML 发布助手会显示每张图的推荐位置、复制路径、打开图片、尝试复制图片。

## 2. 微信公众号

### 标题

我把 Codex 接进了 Obsidian

### 摘要

AI 总结不难，难的是总结之后能不能回到自己的知识库。我做了一个 local-first 的 Obsidian 入库工作流，让链接、本地文件、字幕和原始材料变成可追溯、可索引、可复用的 Markdown 笔记。

### 正文

#### 开头：我真正卡住的不是总结

过去一年，我越来越频繁地用 AI 总结文章、视频、课程和会议材料。

一开始很爽：几十分钟的视频，几秒钟就能得到重点；一篇长文章，马上能变成要点列表。

但用久之后，我发现真正麻烦的不是“AI 会不会总结”，而是：

> 总结完之后，它到底去哪了？

很多摘要最后停在聊天窗口里。过几天想找，要么翻聊天记录，要么重新找链接，要么重新让 AI 总结一遍。

这不是知识管理，只是把临时理解变快了。

【插图 1：痛点图。放在这里，用 `images/wechat/cards/wechat-01.png`】

#### 问题：收藏越来越多，知识却没有沉淀

我的资料来源很杂：

- B 站课程和长视频。
- 微信公众号文章。
- YouTube、网页、本地视频和音频。
- 临时看到但来不及处理的资料链接。

如果每条都手动整理，成本太高；如果只交给 AI 总结，结果又很难沉淀。

我真正想要的是一条更完整的链路：

```text
链接或本地文件
-> 提取正文/字幕/转写
-> 生成结构化笔记
-> 保存原始材料
-> 写入 Obsidian
-> 自动重建索引
-> 半年后还能找回来
```

所以我做了一个小工具：`Obsidian Inbox`。

【插图 2：工作流图。放在这里，用 `images/wechat/cards/wechat-02.png`】

#### 它不是摘要工具，而是入库工作流

`Obsidian Inbox` 的定位很简单：

> 把 Codex 变成你的本地知识入库员。

它做的不是生成一段更漂亮的摘要，而是把外部内容变成 Obsidian 里可追溯、可索引、可复用的 Markdown 笔记。

目前的主流程是：

```text
链接 -> 本地脚本抓字幕/正文 -> 生成 compact.md -> Codex 生成 Obsidian 笔记 -> 重建索引
```

每条资料会有一个主笔记，也会有 `_resources` 目录保存原始正文、字幕、转写或本地文件路径。

这样做的好处是：你以后看到的不只是一段摘要，而是一条带来源、带上下文、带索引入口的知识资产。

【插图 3：Obsidian 结构图。放在这里，用 `images/wechat/cards/wechat-03.png`】

#### 我刻意做了几个限制

我没有把它包装成“全平台一键导入”。

原因很简单：很多平台有登录、权限、验证码、版权和付费内容边界。一个个人知识管理工具，不应该宣传自己能绕过这些限制。

所以它的原则是：

- 能正常抓到公开正文或字幕，才总结。
- 抓不到正文、字幕或可靠转写时，不编造内容。
- Vault、Markdown、原始材料默认留在本机。
- 涉及账号权限和高风险自动化时，保留人工确认。

这也是我最看重的地方：失败要透明，来源要可追溯。

【插图 4：失败安全/边界图。放在这里，用 `images/wechat/cards/wechat-04.png`】

#### 适合哪些人

我觉得它适合这些人：

- 已经用 Obsidian，但资料库越来越乱。
- 经常让 AI 总结内容，但总结散落在聊天记录里。
- 看课程、长视频、会议材料，需要复盘和二次加工。
- 希望 Codex 不只是问答，而是参与稳定工作流。
- 关心 Markdown、本地优先、来源归档和可迁移。

如果你只是偶尔总结一篇文章，它可能有点重。

但如果你已经在维护自己的知识库，或者经常收藏很多资料却来不及整理，它解决的是一个很具体的问题：

> 让内容从“看过/收藏过”，变成“以后真的能找回和复用”。

【插图 5：结果图。放在这里，用 `images/wechat/cards/wechat-05.png`】

#### 项目地址

项目已经放在 GitHub：

https://github.com/Simuiu/obsidian-inbox

如果这个方向对你有用，欢迎 Star。也欢迎在 Issue 里告诉我：

- 你最想入库哪类资料？
- 你希望 Obsidian 笔记长什么样？
- 你现在整理视频、文章、课程时最卡在哪一步？

我的答案很朴素：

> AI 总结之后，知识应该回到你自己的知识库里，带着来源，带着索引，带着以后还能复用的结构。

## 3. 知乎

### 标题候选

1. AI 总结工具最大的问题：总结完之后没人管
2. 用 AI 做知识管理，关键不是总结
3. 为什么我把 Codex 接进了 Obsidian？

### 正文

先说结论：AI 总结有用，但它不是知识管理的终点。

很多人现在的流程是：

```text
看到文章/视频 -> 扔给 AI -> 得到摘要 -> 摘要留在聊天记录里
```

这条链路解决了“当下理解”，但没有解决“长期沉淀”。

我自己真正需要的是另一条链路：

```text
资料进入 -> 提取正文/字幕/转写 -> AI 生成结构化笔记 -> 保存原始材料 -> 写入 Obsidian -> 建立索引
```

所以我做了一个开源小工具：`Obsidian Inbox`。

它不是为了再做一个摘要工具，而是让 Codex 参与 Obsidian 入库流程。

核心设计有 5 点：

1. local-first：Vault、正文、字幕和转写默认在本地处理。
2. Obsidian-native：输出 Markdown、frontmatter、Wiki links 和索引。
3. 可追溯：原始材料进入 `_resources`。
4. 失败安全：抓不到正文/字幕/可靠转写时，不硬编总结。
5. 分层总结：普通总结用于快速入库，深度总结用于课程和系统学习。

我觉得它适合的人不是“偶尔总结一篇文章”的用户，而是长期维护资料库的人：

- 收藏很多，但复盘很少。
- 经常看课程、长视频、技术文章。
- 希望 AI 输出能进入自己的知识系统。
- 关心本地文件、Markdown 和可迁移。

它也有边界：不会绕过登录、验证码、付费墙，也不是全平台一键导入。

项目地址：

https://github.com/Simuiu/obsidian-inbox

我的观点是：不要只追求让 AI 总结得更快，而要让 AI 生成的东西有地方沉淀。

### 配图位置

- 图 1：开头痛点后，`images/zhihu/cards/zhihu-01.png`
- 图 2：两条链路对比后，`images/zhihu/cards/zhihu-02.png`
- 图 3：5 点设计原则前，`images/zhihu/cards/zhihu-03.png`
- 图 4：适用人群前，`images/zhihu/cards/zhihu-04.png`
- 图 5：项目链接前，`images/zhihu/cards/zhihu-05.png`

## 4. 掘金

### 标题候选

1. 我做了一个 local-first 的 Codex + Obsidian 入库工作流
2. 如何把 AI 摘要变成可追溯的 Obsidian 笔记
3. Obsidian Inbox：用 Codex 自动整理外部资料

### 正文

项目地址：

https://github.com/Simuiu/obsidian-inbox

`Obsidian Inbox` 解决的不是“如何总结一篇文章”，而是：

> 如何把外部内容稳定地变成 Obsidian 里可追溯、可索引、可复用的 Markdown 笔记？

#### 1. 背景

普通 AI 摘要工具的问题是结果太脆弱：

- 摘要停留在聊天窗口。
- 没有统一 frontmatter。
- 没有来源归档。
- 没有索引。
- 失败时容易产生“看起来完整”的幻觉内容。

对长期知识管理来说，这些都很致命。

#### 2. 总体流程

```text
source
-> capture script
-> task package
-> compact.md
-> Codex Skill
-> Obsidian note
-> _resources archive
-> rebuilt indexes
```

任务包通常包含：

- `meta.json`：平台、标题、作者、来源 URL、状态等元数据。
- `compact.md`：给 Codex 读取的低 token 摘要材料。
- `prompt.md`：当前任务的写作要求。
- 原始正文、字幕或转写材料。

Codex 默认只读取 `meta.json`、`compact.md`、`prompt.md`，避免把完整字幕或正文塞进上下文。

#### 3. Obsidian 输出结构

```text
00_资料库/YYMMDD 短标题/YYMMDD 短标题.md
00_资料库/YYMMDD 短标题/_resources
```

索引层面维护：

- 总索引。
- 主题索引。
- 用途索引。

笔记正文保留总结、重点、时间点、行动清单和资源链接；原始材料留在 `_resources`，避免主笔记变成材料垃圾场。

#### 4. 关键取舍

我没有追求“全平台一键抓取”。

项目更强调：

- local-first：本地 Vault 和原始材料优先。
- 失败安全：没有正文/字幕/可靠转写时不生成完整总结。
- 低 token：Codex 读 compact 材料，不直接吞完整 SRT。
- 可回溯：source ID、原始材料、资源目录都保留。
- 人工边界：账号权限、平台限制、版权边界不做危险自动化。

#### 5. 适用场景

适合：

- Obsidian 用户。
- AI Agent / Codex 工作流用户。
- 课程、长视频、文章资料整理。
- 需要来源追溯和长期复盘的个人知识库。

不适合：

- 想要所有平台一键下载的人。
- 想绕过登录、验证码、付费墙的人。
- 只想临时总结一段文本的人。

欢迎 Star 或提 Issue：

https://github.com/Simuiu/obsidian-inbox

### 配图位置

- 图 1：背景痛点后，`images/juejin/cards/juejin-01.png`
- 图 2：总体流程后，`images/juejin/cards/juejin-02.png`
- 图 3：输出结构后，`images/juejin/cards/juejin-03.png`
- 图 4：关键取舍后，`images/juejin/cards/juejin-04.png`
- 图 5：适用场景前，`images/juejin/cards/juejin-05.png`

## 5. V2EX

### 节点建议

优先：`分享创造`。如果你判断更像推广，就发 `推广`。

### 标题候选

1. 分享一个把 Codex 接进 Obsidian 的本地入库工具
2. 做了个 Obsidian Inbox：让 AI 摘要不要死在聊天记录里
3. 开源自荐：用 Codex 半自动整理视频/文章到 Obsidian

### 正文

大家好，分享一个我最近在做的小工具：`Obsidian Inbox`。

GitHub：
https://github.com/Simuiu/obsidian-inbox

它解决的问题不是“AI 怎么总结得更好”，而是“总结完之后怎么进入自己的知识库”。

现在的主流程是：

```text
链接 -> 本地脚本抓正文/字幕 -> 生成任务包 -> Codex 写 Obsidian 笔记 -> 重建索引
```

我自己遇到的痛点是：视频、公众号文章、本地课程资料越来越多，AI 摘要也越来越多，但最后都散落在聊天记录或临时文档里，长期找不到。

所以这个项目更关注：

- Markdown 和 Obsidian Vault。
- 原始材料归档到 `_resources`。
- 总索引、主题索引、用途索引。
- 抓不到正文/字幕时不编造总结。
- 能本地处理就本地处理。

它现在还是早期项目，不是“全平台一键导入”，也不会绕过登录、验证码、付费墙。

想听听大家的反馈：

- 你们会把 AI 总结结果放到哪里？
- 如果是 Obsidian 用户，你希望笔记结构长什么样？
- 这种半自动 Agent 工作流，对你有没有实际价值？

### 配图位置

V2EX 不强依赖图片，但这次素材包已准备 5 张，可按需要上传或在评论补充：

- `images/v2ex/cards/v2ex-01.png`
- `images/v2ex/cards/v2ex-02.png`
- `images/v2ex/cards/v2ex-03.png`
- `images/v2ex/cards/v2ex-04.png`
- `images/v2ex/cards/v2ex-05.png`

## 6. 即刻

### 正文

我最近把“AI 总结”往前推了一步。

以前是：看到文章/视频 -> 扔给 AI -> 得到摘要 -> 摘要躺在聊天记录里。

现在我想要的是：摘要直接回到 Obsidian，带来源、带原始材料、带索引，以后还能找回来。

所以做了个开源小工具：`Obsidian Inbox`。

它的大概流程：

```text
链接/本地文件 -> 抓正文/字幕/转写 -> Codex 写成 Obsidian 笔记 -> 归档 _resources -> 重建索引
```

我比较在意几个点：

- 本地优先，不默认上传 Vault。
- 抓不到材料就失败，不硬编。
- 输出是 Markdown，能被 Obsidian 长期管理。
- 不追求绕过平台限制。

项目在这里：
https://github.com/Simuiu/obsidian-inbox

很好奇大家：你们现在让 AI 总结完的内容，最后都放哪？

### 配图位置

- 图 1：动态首图，`images/jike/cards/jike-01.png`
- 图 2：流程图，`images/jike/cards/jike-02.png`
- 图 3：Obsidian 结构，`images/jike/cards/jike-03.png`
- 图 4：边界说明，`images/jike/cards/jike-04.png`
- 图 5：GitHub CTA，`images/jike/cards/jike-05.png`

## 7. 小红书

### 标题候选

1. AI 总结完别再丢聊天框了
2. Obsidian 用户真的需要这个流程
3. 我让 Codex 自动整理资料库了

### 正文

我之前用 AI 总结文章和视频，最大的问题不是总结不够快，而是总结完之后找不到。

后来我做了一个本地工作流：`Obsidian Inbox`。

它会把链接/本地文件整理成 Obsidian 笔记，保留原始材料，并自动重建索引。

适合：

- Obsidian 用户
- 收藏很多资料但没时间整理的人
- 经常看课程/长视频/技术文章的人
- 想把 Codex 变成固定工作流的人

它不是全平台一键下载，也不会绕过登录和付费墙。

但如果你想让 AI 摘要真正回到自己的知识库里，这个方向可以试试。

GitHub：Simuiu/obsidian-inbox

#Obsidian #AI工具 #知识管理 #Codex #效率工具 #开源项目

### 图片上传顺序

1. `images/xiaohongshu/final-cards/xiaohongshu-final-01.png`：首图，讲痛点。
2. `images/xiaohongshu/final-cards/xiaohongshu-final-02.png`：旧流程为什么不够。
3. `images/xiaohongshu/final-cards/xiaohongshu-final-03.png`：新工作流。
4. `images/xiaohongshu/final-cards/xiaohongshu-final-04.png`：Obsidian 输出结构。
5. `images/xiaohongshu/final-cards/xiaohongshu-final-05.png`：适用人群。
6. `images/xiaohongshu/final-cards/xiaohongshu-final-06.png`：边界和 GitHub。

## 8. B 站

### 标题候选

1. AI 总结完别丢了：我把 Codex 接进 Obsidian
2. Obsidian + Codex：自动整理视频和文章资料
3. 我做了个本地知识入库工具 Obsidian Inbox

### 简介

很多 AI 总结最后都留在聊天记录里。这个视频演示我做的开源项目 `Obsidian Inbox`：把链接、本地视频、文章资料整理成 Obsidian Markdown 笔记，并保留原始材料和索引。

GitHub：
https://github.com/Simuiu/obsidian-inbox

章节：

00:00 AI 总结之后的问题
00:18 Obsidian Inbox 是什么
00:42 本地入库流程
01:10 原始材料和索引
01:35 适用场景和边界
01:55 GitHub 项目地址

标签：
Obsidian, AI工具, Codex, 知识管理, 开源项目, Markdown

### 置顶评论

项目地址：https://github.com/Simuiu/obsidian-inbox

如果你也有“AI 总结完不知道放哪”的问题，可以试试这个方向。欢迎 Star，也欢迎提 Issue 说说你想入库哪类资料。

### 素材

- 视频：`video-assets/bilibili-slideshow.mp4`
- 推荐封面：`images/bilibili/final-covers/bilibili-cover-01.png`
- 备选封面：`images/bilibili/final-covers/bilibili-cover-02.png` 至 `bilibili-cover-05.png`
- 辅助配图：`images/bilibili/cards/bilibili-01.png` 至 `bilibili-05.png`

## 9. 视频号

### 标题候选

1. AI 总结完，别丢聊天框
2. 我把 Codex 接进 Obsidian
3. 资料自动入库到 Obsidian

### 文案

AI 总结之后，知识应该去哪？

我做了一个本地工作流：`Obsidian Inbox`。

链接或本地文件进来，Codex 帮我整理成 Obsidian 笔记，原始材料进 `_resources`，索引自动重建。

它不是全平台一键下载，也不会绕过登录、验证码和付费墙。

它解决的是一个更朴素的问题：让 AI 摘要回到自己的知识库里。

GitHub：Simuiu/obsidian-inbox

#Obsidian #AI工具 #Codex #知识管理 #开源项目

### 素材

- 视频：`video-assets/wechat-video-slideshow.mp4`
- 首帧/封面建议：`images/wechat-video/cards/wechat-video-01.png`
- 过程配图：`images/wechat-video/cards/wechat-video-02.png` 至 `wechat-video-05.png`

## 10. GitHub

### About

Local-first Codex workflow for turning videos, articles, and local media into traceable Obsidian notes with archived resources and rebuilt indexes.

### Topics

`obsidian`, `codex`, `ai-agents`, `knowledge-management`, `markdown`, `local-first`, `personal-knowledge-management`, `automation`

### README 引导语

`Obsidian Inbox` turns Codex into a local knowledge ingestion assistant: links and local files become structured Obsidian notes, raw materials are archived, and indexes are rebuilt for future retrieval.

### 配图

- `images/github/cards/github-01.png`
- `images/github/cards/github-02.png`
- `images/github/cards/github-03.png`
- `images/github/cards/github-04.png`
- `images/github/cards/github-05.png`
