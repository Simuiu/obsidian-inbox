# 11 Obsidian Inbox 平台草稿包与授权清单

## 1. 当前完成状态

已完成：

- 全平台文案。
- 每个平台不少于 5 张配图。
- B 站横版 MP4 素材。
- 视频号竖版 MP4 素材。
- 小红书 6 张最终图文卡片。
- B 站 5 张最终封面候选。
- HTML 复制助手。
- GitHub README、Issue 模板、Topics 等承接页优化。

未完成的线上动作：

- 未登录你的内容平台账号。
- 未在公众号、知乎、掘金、V2EX、即刻、B 站、小红书、视频号创建线上草稿。
- 未正式发布任何内容。

原因：这些动作需要平台账号授权、扫码登录或你确认账号风险边界。

## 2. 本地发布助手

打开：

```bash
open marketing/publish-packets/2026-05-11-full-platform-launch/index.html
```

可用功能：

- 复制单字段：标题、摘要、正文、标签、脚本。
- 复制本平台全部文案。
- 查看本平台配图。
- 复制图片路径。

## 3. 平台草稿包

### 3.1 微信公众号

文案：

- `05 Obsidian Inbox 全平台首轮发布物料包` 的微信公众号部分。
- HTML 助手里选择“微信公众号”。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/wechat/cards/
```

需要你配合：

- 公众号后台扫码登录，或提供开发者权限配置方式。
- 如果走草稿箱 API，需要 AppID、AppSecret、安全 IP、素材上传权限。不要直接发在对话里，建议写入本地安全配置。

我能继续做：

- 在你授权后，把标题、摘要、正文和图片上传到公众号草稿箱。

### 3.2 知乎

文案：

- `05` 的知乎部分。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/zhihu/cards/
```

需要你配合：

- 确认发布到哪个问题下。
- 如果要我辅助进草稿，需要知乎网页登录状态或浏览器自动化授权。

我能继续做：

- 你给问题链接后，我整理成该问题下的最终回答版本。
- 如果允许浏览器辅助，我可尝试填入草稿，不直接点发布。

### 3.3 掘金

文案：

- `05` 的掘金部分。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/juejin/cards/
```

需要你配合：

- 掘金登录状态或后台入口。

我能继续做：

- 辅助粘贴 Markdown 和上传图片到草稿，不直接发布。

### 3.4 V2EX

文案：

- `05` 的 V2EX 部分。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/v2ex/cards/
```

建议节点：

- `create`
- `share`
- `programmer`

需要你配合：

- V2EX 发帖通常更适合你手动确认发布，避免账号风控。

我能继续做：

- 根据你选的节点，进一步压缩正文或调整口吻。

### 3.5 即刻

文案：

- `05` 的即刻部分。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/jike/cards/
```

需要你配合：

- 即刻账号登录或手动发布。

我能继续做：

- 按“更轻松/更技术/更求反馈”三个口吻生成备选。

### 3.6 B 站

文案：

- `05` 的 B 站部分。
- `06` 的 B 站分镜脚本。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/bilibili/final-covers/
```

已生成视频素材：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/video-assets/bilibili-slideshow.mp4
```

需要你配合：

- 如果要正式投稿，需要 B 站账号登录。
- 如果要更正式的视频，需要你确认是否用真实录屏替换当前 slideshow MP4。

我能继续做：

- 在你提供录屏或允许我录制本地演示后，生成更正式的演示视频。
- 有登录授权后，辅助填写投稿信息，不直接发布。

### 3.7 小红书

文案：

- `05` 的小红书部分。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/xiaohongshu/final-cards/
```

需要你配合：

- 小红书登录或手动上传。

我能继续做：

- 当前已生成可直接发布的 6 张最终图文卡片；如果你想更贴近某个账号风格，可以继续重生成。

### 3.8 视频号

文案：

- `05` 的视频号部分。
- `06` 的视频号 60 秒脚本。

配图：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/images/wechat-video/cards/
```

已生成视频素材：

```text
marketing/publish-packets/2026-05-11-full-platform-launch/video-assets/wechat-video-slideshow.mp4
```

需要你配合：

- 视频号账号登录。
- 是否关联公众号文章。

我能继续做：

- 在你确认后，辅助填写视频标题、描述、封面，不直接发布。

## 4. 你最少需要配合什么

第一批如果只想快速启动，建议你只做这 4 件事：

1. 确认先发哪些平台：建议即刻、V2EX、知乎。
2. 对需要登录的平台，打开网页登录状态或扫码。
3. 决定 B 站/视频号是否接受当前 slideshow MP4 作为首版素材。
4. 确认公众号是否有开发者权限；没有的话先走手动草稿。

## 5. Codex 自评结论

现在本地发布准备已经完整。真正卡点不在物料，而在平台账号授权和最终发布确认。建议下一步先从即刻/V2EX/知乎这三个低成本平台开始。
