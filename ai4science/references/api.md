# Public interface reference

## Endpoints

- JSON v1: `https://juanli.me/ai4science/api/v1/events.json`
- Chinese daily brief RSS: `https://juanli.me/ai4science/feed/daily.zh.xml`
- English daily brief RSS: `https://juanli.me/ai4science/feed/daily.en.xml`
- Chinese full updates RSS: `https://juanli.me/ai4science/feed.zh.xml`
- English full updates RSS: `https://juanli.me/ai4science/feed.en.xml`
- Human-readable access page: `https://juanli.me/ai4science/agent/`

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
- `fields[]`: zero or more field objects with `id`, `name_zh`, and `name_en`. Prefer this array.
- `field`: first field object, kept for compatibility when at least one field exists
- `topics`: zero or more localized topic objects
- `title`: `zh` and `en`
- `summary`: `zh` and `en`
- `summary_type`: `zh` and `en`, one of:
  - `ai_guide`: site-written or editorially reviewed guide
  - `source_abstract`: mechanically cleaned source abstract; not an AI4Science original guide
  - `summary`: public summary whose type is not further determined
- `people`, `organizations`
- `source.name`
- `links.permalink.zh` and `links.permalink.en`: bilingual permanent event pages
- `links.interactive`: hash URL for the interactive app (`#item/{id}`)
- `links.ai4science`: deprecated alias of the hash URL; still present, still a hash. Do not treat it as the current permalink.
- `links.original`: primary source

The public schema intentionally excludes ingestion configuration, relevance scores, candidate state, localization state, secrets, and editorial rules.

`published_at` is the event timestamp exposed by the reading layer. It can reflect a revision or a newly indexed event and must not automatically be described as the source's first-publication date. Events are ordered by this timestamp, not by importance.

## Direct examples

```bash
curl -fsSL https://juanli.me/ai4science/api/v1/events.json
```

```bash
python3 scripts/query_ai4science.py --lang zh --days 7 --field 生物 --limit 8
```

Field IDs currently include `math`, `biology`, `materials`, `physics`, `climate`, `astronomy`, `ecology`, `agents`, `infrastructure`, and `policy`. Prefer field IDs in automated calls because they are language-independent.

## Use and verification

Link back to `links.permalink[lang]` or the query script's `event_url` when presenting an item. For scientific numbers, methods, results, or quotations, open `links.original` and verify the claim against the primary source. When `summary_type` is `source_abstract`, say so; do not describe it as an edited guide.
