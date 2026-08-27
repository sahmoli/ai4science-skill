import importlib.util
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "ai4science/scripts/query_ai4science.py"
SPEC = importlib.util.spec_from_file_location("query_ai4science", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class QueryAI4ScienceTest(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "events": [
                {
                    "id": "new-biology",
                    "published_at": "2026-08-15T00:00:00Z",
                    "field": {
                        "id": "biology",
                        "name_zh": "生物与医学",
                        "name_en": "Biology & Medicine",
                    },
                    "topics": [
                        {
                            "id": "verification",
                            "name_zh": "验证与证据",
                            "name_en": "Verification & Evidence",
                        }
                    ],
                    "title": {"zh": "蛋白质模型", "en": "Protein model"},
                    "summary": {"zh": "包含实验验证。", "en": "Includes experimental validation."},
                    "summary_type": {"zh": "ai_guide", "en": "ai_guide"},
                    "people": [],
                    "organizations": ["Example Lab"],
                    "source": {"name": "Example Journal"},
                    "links": {"ai4science": "https://example.org/event", "original": "https://example.org/paper"},
                },
                {
                    "id": "old-math",
                    "published_at": "2026-01-01T00:00:00Z",
                    "field": {"id": "math", "name_zh": "数学", "name_en": "Mathematics"},
                    "topics": [],
                    "title": {"zh": "旧数学事件", "en": "Old math event"},
                    "summary": {"zh": "旧事件。", "en": "An old event."},
                    "people": [],
                    "organizations": [],
                    "source": {"name": "Archive"},
                    "links": {},
                },
            ]
        }

    def test_filters_and_localizes(self):
        events = MODULE.select_events(
            self.payload,
            lang="zh",
            days=7,
            limit=10,
            query="蛋白质 验证",
            field="biology",
            now=datetime(2026, 8, 16, tzinfo=timezone.utc),
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "蛋白质模型")
        self.assertEqual(events[0]["field"], "生物与医学")
        self.assertEqual(events[0]["summary_type"], "ai_guide")

    def test_fields_array_without_singular_field_still_filters(self):
        payload = {
            "events": [
                {
                    "id": "fields-only",
                    "published_at": "2026-08-15T00:00:00Z",
                    "fields": [
                        {
                            "id": "biology",
                            "name_zh": "生物与医学",
                            "name_en": "Biology & Medicine",
                        }
                    ],
                    "topics": [],
                    "title": {"zh": "仅 fields", "en": "Fields only"},
                    "summary": {"zh": "摘要", "en": "Summary"},
                    "people": [],
                    "organizations": [],
                    "source": {"name": "Lab"},
                    "links": {
                        "permalink": {
                            "zh": "https://juanli.me/ai4science/zh/events/fields-only/",
                            "en": "https://juanli.me/ai4science/en/events/fields-only/",
                        }
                    },
                }
            ]
        }
        events = MODULE.select_events(
            payload,
            lang="en",
            days=7,
            limit=10,
            query=None,
            field="biology",
            now=datetime(2026, 8, 16, tzinfo=timezone.utc),
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0]["event_url"],
            "https://juanli.me/ai4science/en/events/fields-only/",
        )
        self.assertNotIn("ai4science", events[0]["links"])

    def test_days_zero_includes_archive(self):
        events = MODULE.select_events(
            self.payload,
            lang="en",
            days=0,
            limit=10,
            query=None,
            field=None,
        )
        self.assertEqual([event["id"] for event in events], ["new-biology", "old-math"])


if __name__ == "__main__":
    unittest.main()
