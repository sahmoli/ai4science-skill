# AI4Science Skill

A bilingual, source-grounded AI for Science feed for agents.

This repository exposes the **public reading layer** of [Juan Li · AI4Science](https://juanli.me/ai4science-prototype/): publication-ready events with Chinese and English titles, edited summaries, classifications, and links to original sources. It does **not** expose the private collection, scoring, translation, review, or publishing pipeline.

[中文说明](README.zh-CN.md) · [Agent access page](https://juanli.me/ai4science-prototype/agent/)

## Install

Ask a Skills-compatible agent:

> Install the AI4Science Skill from https://github.com/sahmoli/ai4science-skill. Install the `ai4science/` directory, start a new session, then verify it by asking: “What were the most important AI4Science developments in the past seven days?”

Or copy the `ai4science/` directory into the skills directory used by your agent.

## What it can do

- Summarize recent AI4Science developments in Chinese or English
- Filter by time, scientific field, researcher, organization, or keyword
- Produce daily and weekly briefs with traceable event and original-source links
- Query the public endpoint with a dependency-free Python script

Example:

```bash
python3 ai4science/scripts/query_ai4science.py --lang en --days 7 --field biology --limit 10
```

## Public interfaces

- JSON: `https://juanli.me/ai4science-prototype/api/v1/events.json`
- Chinese RSS: `https://juanli.me/ai4science-prototype/feed.zh.xml`
- English RSS: `https://juanli.me/ai4science-prototype/feed.en.xml`

No API key is required. See [`ai4science/references/api.md`](ai4science/references/api.md) for the public schema and trust boundary.

## License

The Skill code and documentation are available under the [MIT License](LICENSE). Linked source materials remain subject to their respective owners' terms.
