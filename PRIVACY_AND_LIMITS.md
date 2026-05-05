# 隐私与平台边界

## 本项目会处理什么

- 用户主动提供的公开链接。
- 用户本机已有权限访问并保存的本地视频、音频、文章或转写。
- 任务包里的元数据、正文、字幕、转写、图片和诊断信息。
- Obsidian Vault 内的入库笔记、索引和 `_resources` 资源目录。

## 本项目不做什么

- 不绕过登录、验证码、机器人校验或付费墙。
- 不承诺抓取用户无权访问的平台内容。
- 不把抓取失败的内容编造成总结。
- 不自动上传你的 Vault、cookies、字幕、转写或原始材料。

## Cookie 与登录态

Bilibili 字幕抓取可以读取 `secrets/bilibili.cookies.txt` 或浏览器登录态。发布到 GitHub 前不要提交 `secrets/` 里的真实 cookie。

YouTube、微信、小红书、抖音等平台如果要求登录、校验或客户端权限，本项目只记录失败状态或使用你本地合法导出的文件，不做绕过。

## 公开测试素材

测试脚本只使用公开可下载、允许测试使用的样例：

- Big Buck Bunny 30s sample：用于本地视频导入测试。
- OpenAI Whisper `jfk.flac`：用于 ASR 转写测试。
- 项目内指定的公开微信公众号文章：用于文章正文和图片本地化回归。

## 发布前注意

- 不提交个人 Vault 路径、真实 cookies、私有任务包或原始材料。
- 推荐用 `config.example.yaml` 作为公开示例。
- 用户首次使用应运行 `scripts/init_config.py` 写入自己的 Vault 路径。
