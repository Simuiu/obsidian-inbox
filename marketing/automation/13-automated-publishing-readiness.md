# 13 Obsidian Inbox 全自动发布可行性盘点与准备清单

## 1. 结论

按“官方接口或成熟 CLI、账号风险可控、能先生成预览或草稿、发布前可人工确认”的标准，当前真正可以纳入全自动或准全自动发布准备的平台只有 3 类：

| 平台 | 可自动化动作 | 当前状态 | 是否进入准备 |
| --- | --- | --- | --- |
| GitHub | Release、Issue、仓库内容、Topics 检查、提交推送 | `gh` 已登录 `Simuiu`，可执行 | 是 |
| 飞书 | Markdown 文档同步为云文档 | `md2feishu` 已授权并多次成功同步 | 是 |
| 微信公众号 | 上传素材、创建草稿；正式发布可通过接口但发布前必须人工确认 | 官方有草稿箱和发布接口；需要公众号开发者权限、AppID/Secret、安全 IP、素材权限 | 是，先准备草稿预览和本地脚本 |

不纳入全自动承诺的平台：

| 平台 | 原因 | 当前策略 |
| --- | --- | --- |
| 知乎 | 未确认稳定公开发文接口，浏览器自动化有账号风控 | 半自动发布包 |
| 掘金 | 未确认稳定官方草稿/发布接口 | 半自动 Markdown 发布包 |
| V2EX | 官方 API 主要偏读取，不把自动发帖作为可控路径 | 人工确认发帖 |
| 即刻 | 未接入稳定发布接口 | 人工确认发布 |
| 小红书 | 不建议 cookie 自动发帖，账号风控较高 | 半自动图文包 |
| B 站 | 官方/开放平台视频上传权限不适合直接承诺，第三方上传工具多为非官方路径 | 半自动投稿包 |
| 视频号 | 未确认稳定可用的普通账号发布接口 | 半自动视频包 |

## 2. 已完成准备

### GitHub

- 已确认 `gh` 登录账号：`Simuiu`。
- 之前已经完成 README、Issue 模板、Topics、发布物料提交和推送。
- 后续可由 Codex 自动准备 Release 草稿，但正式 Release 发布前需要你确认标题、tag、正文。

### 飞书

- `md2feishu` 已可用。
- `00-13` 相关 Markdown 可同步到飞书。
- 后续文档修改后可以继续自动覆盖同一飞书云文档。

### 微信公众号

已新增准备文件：

- 配置模板：`marketing/automation/wechat-official-account.env.example`
- 草稿脚本：`scripts/wechat_official_account_draft.py`
- 本地预览输出目录：`marketing/automation/previews/`

默认先生成本地预览，不访问微信接口：

```bash
python3 scripts/wechat_official_account_draft.py
```

生成：

- `marketing/automation/previews/wechat-draft-preview.html`
- `marketing/automation/previews/wechat-draft-payload.preview.json`

如果你提供安全授权配置，后续可尝试：

```bash
python3 scripts/wechat_official_account_draft.py \
  --env-file secrets/wechat-official-account.env \
  --upload-assets \
  --create-draft
```

这一步的目标是创建公众号草稿，不直接正式发布。

## 3. 微信公众号需要你确认/提供

需要确认：

- 公众号是否具备开发者权限。
- 是否允许配置安全 IP。
- 是否允许使用草稿箱接口。
- 是否只允许我创建草稿，不允许直接发布。

需要本地安全配置，不要发在对话里：

```text
WECHAT_OFFICIAL_APPID=
WECHAT_OFFICIAL_SECRET=
WECHAT_OFFICIAL_AUTHOR=
WECHAT_OFFICIAL_CONTENT_SOURCE_URL=https://github.com/Simuiu/obsidian-inbox
```

建议保存到：

```text
secrets/wechat-official-account.env
```

## 4. 发布前确认流程

后续对可自动化平台统一采用这个流程：

1. Codex 生成本地预览。
2. 你确认预览效果。
3. Codex 创建草稿或 Release 草稿。
4. 你检查线上草稿。
5. 你确认后，才正式发布。

## 5. 当前下一步

建议先做微信公众号自动草稿验证：

1. 你确认公众号是否能提供开发者权限。
2. 我运行本地预览脚本，给你预览路径。
3. 你确认预览。
4. 你配置本地 `.secrets/wechat-official-account.env`。
5. 我尝试上传素材并创建公众号草稿。

## 6. 参考链接

- GitHub CLI Release 文档：https://cli.github.com/manual/gh_release_create
- GitHub REST Releases 文档：https://docs.github.com/en/rest/releases/releases
- 微信公众号草稿箱接口：https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
- 微信公众号发布接口：https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html
- 微信公众号素材管理接口：https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html
