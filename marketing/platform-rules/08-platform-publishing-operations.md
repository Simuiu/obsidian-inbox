# 08 Obsidian Inbox 平台发布操作辅助

## 1. 使用说明

本文件用于把 `05 全平台首轮发布物料包` 和图片资产落到各平台发布操作中。默认目标是减少你的手工工作量：能自动进入草稿就自动，不能自动就提供复制清单和图片路径。

安全边界：

- 不在对话中展示 token、cookie、session、auth 文件。
- 未确认授权前，不直接登录或代发内容。
- 默认只做到草稿、待发布或可检查状态。

## 2. 平台操作清单

| 平台 | 发布方式 | 文案来源 | 图片来源 | 你需要做 |
| --- | --- | --- | --- | --- |
| 微信公众号 | 半自动；有开发者权限后可尝试草稿箱 API | `05` 公众号段落 / HTML 助手 | `images/wechat/cards/` | 复制标题、摘要、富文本正文，上传 5 张配图 |
| 知乎 | 半自动 | `05` 知乎段落 / HTML 助手 | `images/zhihu/cards/` | 选择问题，粘贴回答，插入配图 |
| 掘金 | 半自动 | `05` 掘金段落 / HTML 助手 | `images/juejin/cards/` | 粘贴 Markdown，上传配图，检查代码块 |
| V2EX | 人工确认发布 | `05` V2EX 段落 / HTML 助手 | `images/v2ex/cards/` | 选节点，粘贴正文，必要时不放图或放 1-2 张 |
| 即刻 | 人工确认发布 | `05` 即刻段落 / HTML 助手 | `images/jike/cards/` | 粘贴正文，选择 1-5 张配图 |
| B 站 | 半自动 | `05` B 站段落，`06` 分镜脚本 | `images/bilibili/cards/` | 上传视频，复制标题/简介/标签/置顶评论 |
| 小红书 | 半自动 | `05` 小红书段落，`06` 卡片内容 | `images/xiaohongshu/cards/` | 上传 6 张图，复制标题/正文/话题 |
| 视频号 | 半自动 | `05` 视频号段落，`06` 60 秒脚本 | `images/wechat-video/cards/` | 上传视频或分镜图，复制标题/描述 |
| GitHub | 已具备 CLI 能力，但推送受网络影响 | `03`、`04`、`05` GitHub 段落 | `images/github/cards/` | 等 GitHub push 恢复后检查 Issue 模板和 Release 草稿 |

## 3. 微信公众号复制流程

1. 打开本地发布助手：

```bash
open marketing/publish-packets/2026-05-11-full-platform-launch/index.html
```

2. 切换到“微信公众号”。
3. 依次复制：
   - 标题
   - 摘要
   - 正文
4. 上传配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/wechat/cards/
```

5. 发布前检查：
   - 是否保留 GitHub 链接。
   - 是否没有“绕过限制”等高风险表达。
   - 图片是否显示正常。

## 4. 小红书复制流程

1. 上传图片：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/xiaohongshu/cards/
```

2. 复制标题、正文、话题。
3. 检查首图是否足够清晰。
4. 如果平台压缩导致字太小，优先重新生成小红书卡片。

## 5. B 站发布流程

1. 先按 `06` 的分镜录屏或制作视频。
2. 上传视频后，复制：
   - 标题
   - 简介
   - 标签
   - 置顶评论
3. 封面优先选：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/bilibili/cards/bilibili-01.png
```

## 6. 自动化待验证

| 平台 | 待验证点 |
| --- | --- |
| 微信公众号 | 是否有可用公众号开发者权限，能否通过草稿箱 API 创建草稿 |
| 掘金 | 是否有稳定草稿 API/CLI 或可接受浏览器辅助 |
| B 站 | 是否有可靠上传工具，是否支持待发布草稿 |
| 小红书 | 不建议 cookie 自动发帖，最多做低频浏览器辅助 |
| 视频号 | 默认人工发布，后续再看是否能走微信生态接口 |

## 7. Codex 自评结论

本文件已经能支持你按平台逐个发布。当前最省事的路线是：先用 HTML 助手复制文案，再手动上传对应平台的配图。等第一轮验证有反馈后，再决定是否接平台草稿 API。

