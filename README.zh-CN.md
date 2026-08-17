# AI4Science Skill

一个面向 Agent 的双语、来源可追溯 AI for Science 信息接口。

这个仓库开放的是 [Juan Li · AI4Science](https://juanli.me/ai4science-prototype/) 的**公开阅读层**：已经达到发布标准的事件、中英文标题与编辑摘要、分类，以及原始来源链接。它**不包含**私有的采集、评分、翻译、审校和发布管线。

[English](README.md) · [Agent 接入页](https://juanli.me/ai4science-prototype/agent/)

## 安装

把下面这句话交给支持 Skills 的 Agent：

> 请从 https://github.com/sahmoli/ai4science-skill 安装 AI4Science Skill。安装仓库中的 `ai4science/` 目录，完成后开启新会话，并用“过去 7 天最值得关注的 AI4Science 进展是什么？”验证。

也可以直接把 `ai4science/` 目录复制到你的 Agent 实际读取的 skills 目录。

## 能做什么

- 用中文或英文总结最近的 AI4Science 动态
- 按时间、科学领域、研究者、机构或关键词筛选
- 生成带事件页和原始来源链接的日报或周报
- 通过一个不依赖第三方库的 Python 脚本查询公开接口

示例：

```bash
python3 ai4science/scripts/query_ai4science.py --lang zh --days 7 --field biology --limit 10
```

## 公开接口

- JSON：`https://juanli.me/ai4science-prototype/api/v1/events.json`
- 中文每日简报 RSS（推荐）：`https://juanli.me/ai4science-prototype/feed/daily.zh.xml`
- 英文每日简报 RSS（推荐）：`https://juanli.me/ai4science-prototype/feed/daily.en.xml`
- 中文完整动态 RSS：`https://juanli.me/ai4science-prototype/feed.zh.xml`
- 英文完整动态 RSS：`https://juanli.me/ai4science-prototype/feed.en.xml`

不需要 API Key。公开字段与边界见 [`ai4science/references/api.md`](ai4science/references/api.md)。

## 许可

Skill 代码与文档采用 [MIT License](LICENSE)。所链接的原始资料仍遵循各自权利人的条款。
