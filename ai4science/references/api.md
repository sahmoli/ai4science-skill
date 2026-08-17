# Public interface reference

## Endpoints

- JSON v1: `https://juanli.me/ai4science-prototype/api/v1/events.json`
- Chinese daily brief RSS: `https://juanli.me/ai4science-prototype/feed/daily.zh.xml`
- English daily brief RSS: `https://juanli.me/ai4science-prototype/feed/daily.en.xml`
- Chinese full updates RSS: `https://juanli.me/ai4science-prototype/feed.zh.xml`
- English full updates RSS: `https://juanli.me/ai4science-prototype/feed.en.xml`
- Human-readable access page: `https://juanli.me/ai4science-prototype/agent/`

All endpoints are anonymous, read-only HTTPS resources. They do not accept API keys, cookies, writes, or user data.

The daily feeds publish one curated brief per day and retain the latest 30 editions. The full updates feeds publish one RSS item per research event.

## JSON v1 shape

The top-level object contains:

- `version`: schema version, currently `1`
- `generated_at`: source dataset generation timestamp
- `timezone`: editorial timezone
- `attribution`: dataset name and canonical URL
- `feeds`: localized RSS URLs
- `events`: public, publication-ready events ordered newest first

Each event contains:

- `id`, `published_at`
- `field`: `id`, `name_zh`, and `name_en`
- `topics`: zero or more localized topic objects
- `title`: `zh` and `en`
- `summary`: `zh` and `en`
- `people`, `organizations`
- `source.name`
- `links.ai4science` and `links.original`

The public schema intentionally excludes ingestion configuration, relevance scores, candidate state, localization state, secrets, and editorial rules.

`published_at` is the event timestamp exposed by the reading layer. It can reflect a revision or a newly indexed event and must not automatically be described as the source's first-publication date. Events are ordered by this timestamp, not by importance.

## Direct examples

```bash
curl -fsSL https://juanli.me/ai4science-prototype/api/v1/events.json
```

```bash
python3 scripts/query_ai4science.py --lang zh --days 7 --field 生物 --limit 8
```

Field IDs currently include `math`, `biology`, `materials`, `physics`, `climate`, `astronomy`, `ecology`, `agents`, `infrastructure`, and `policy`. Prefer field IDs in automated calls because they are language-independent.

## Use and verification

Link back to the AI4Science event page when presenting an item. For scientific numbers, methods, results, or quotations, open `links.original` and verify the claim against the primary source.
