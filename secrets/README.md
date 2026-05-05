# Secrets

把 B 站 Cookie 文件放在这里：

```text
secrets/bilibili.cookies.txt
```

脚本会优先使用这个文件：

```bash
yt-dlp --cookies secrets/bilibili.cookies.txt
```

如果文件不存在，才会回退到：

```bash
yt-dlp --cookies-from-browser chrome
```

注意：`bilibili.cookies.txt` 等同于登录凭证，不要分享，不要提交到 Git。
