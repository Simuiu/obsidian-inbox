# 14 AI 最新新闻知识库自动入库说明

## 目标

每天从 `zarazhangrui/follow-builders` 的公开 central feeds 抓取 AI 一手信息，生成一篇 Obsidian 日报笔记，并保存原始 JSON。

数据源：

- `feed-x.json`
- `feed-blogs.json`
- `feed-podcasts.json`
- `config/default-sources.json`

项目链接：

https://github.com/zarazhangrui/follow-builders

## 入库位置

每天生成一篇：

```text
00_资料库/YYMMDD AI 一手信息日报/YYMMDD AI 一手信息日报.md
```

原始材料：

```text
00_资料库/YYMMDD AI 一手信息日报/_resources/
```

## 手动运行

```bash
cd /Users/longhuadmin/obsidian-inbox
python3 scripts/ingest_ai_news_daily.py
```

运行后会自动重建 Obsidian 索引。

## 定时任务

已准备 launchd 配置：

```text
marketing/automation/com.longhu.obsidian-ai-news.plist
```

计划时间：

```text
每天 08:30
```

日志：

```text
logs/ai-news-daily.out.log
logs/ai-news-daily.err.log
```

## 设计边界

- 只记录公开 feed 中已经生成的信息。
- 不编造新闻，不把抓取失败当成空新闻。
- 默认覆盖当天日报，保证重复运行不会产生多篇重复笔记。
- 如果某条内容值得深入，再单独对原文、视频或播客做深度入库。
