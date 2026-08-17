#!/usr/bin/env python3
"""Query Juan Li's public bilingual AI4Science event endpoint."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_URL = "https://juanli.me/ai4science-prototype/api/v1/events.json"


def parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def fetch(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "ai4science-skill/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not read the AI4Science endpoint: {error}") from error


def search_text(event: dict) -> str:
    values = [
        *(event.get("title") or {}).values(),
        *(event.get("summary") or {}).values(),
        *((event.get("field") or {}).values()),
        *(event.get("people") or []),
        *(event.get("organizations") or []),
    ]
    for topic in event.get("topics") or []:
        values.extend(topic.values())
    return "\n".join(str(value) for value in values if value).casefold()


def select_events(
    payload: dict,
    *,
    lang: str,
    days: int,
    limit: int,
    query: str | None,
    field: str | None,
    now: datetime | None = None,
) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days) if days else None
    terms = [term.casefold() for term in (query or "").split() if term]
    field_term = (field or "").casefold().strip()
    selected = []

    for event in payload.get("events", []):
        try:
            published = parse_datetime(str(event["published_at"]))
        except (KeyError, TypeError, ValueError):
            continue
        if cutoff and published < cutoff:
            continue
        field_data = event.get("field") or {}
        field_values = " ".join(str(value) for value in field_data.values()).casefold()
        if field_term and field_term not in field_values:
            continue
        haystack = search_text(event)
        if terms and not all(term in haystack for term in terms):
            continue

        title = event.get("title") or {}
        summary = event.get("summary") or {}
        selected.append(
            {
                "id": event.get("id"),
                "published_at": event.get("published_at"),
                "field": field_data.get(f"name_{lang}") or field_data.get("id"),
                "topics": [
                    topic.get(f"name_{lang}") or topic.get("id")
                    for topic in (event.get("topics") or [])
                ],
                "title": title.get(lang),
                "summary": summary.get(lang),
                "people": event.get("people") or [],
                "organizations": event.get("organizations") or [],
                "source": (event.get("source") or {}).get("name"),
                "links": event.get("links") or {},
            }
        )
        if len(selected) >= limit:
            break
    return selected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=("zh", "en"), default="en")
    parser.add_argument("--days", type=int, default=7, help="0 searches all exposed events")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--q", help="Space-separated terms; every term must match")
    parser.add_argument("--field", help="Field ID or localized field name")
    parser.add_argument("--url", default=DEFAULT_URL, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.days < 0:
        parser.error("--days must be 0 or greater")
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    return args


def main() -> int:
    args = parse_args()
    try:
        payload = fetch(args.url)
        events = select_events(
            payload,
            lang=args.lang,
            days=args.days,
            limit=args.limit,
            query=args.q,
            field=args.field,
        )
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    result = {
        "attribution": payload.get("attribution"),
        "endpoint_generated_at": payload.get("generated_at"),
        "language": args.lang,
        "filters": {
            "days": args.days,
            "query": args.q,
            "field": args.field,
            "limit": args.limit,
        },
        "count": len(events),
        "events": events,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
