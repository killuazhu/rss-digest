#!/usr/bin/env python3
"""Fetch RSS feed items from Readwise Reader API and group into categories."""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

TECH_FEED_KEYWORDS = {
    "tech",
    "technology",
    "ai",
    "artificial intelligence",
    "software",
    "programming",
    "developer",
    "engineering",
    "startup",
    "cybersecurity",
    "cloud",
    "data",
    "open source",
}

NON_TECH_NEWS_KEYWORDS = {
    "news",
    "politics",
    "economy",
    "economic",
    "business",
    "finance",
    "markets",
    "world",
    "policy",
    "government",
}

TECH_DOMAINS = {
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "arstechnica.com",
    "hackernews",
    "venturebeat.com",
    "engadget.com",
    "thenextweb.com",
    "github.blog",
}


def fetch_rss_items(token: str, hours: int = 24) -> list[dict]:
    updated_after = (
        datetime.now(timezone.utc) - timedelta(hours=hours)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    base_url = "https://readwise.io/api/v3/list/"
    all_results = []
    page_cursor = None

    while True:
        params = {"location": "feed", "updatedAfter": updated_after}
        if page_cursor:
            params["pageCursor"] = page_cursor

        url = base_url + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(
            url, headers={"Authorization": f"Token {token}"}
        )

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())

        all_results.extend(data.get("results", []))

        page_cursor = data.get("nextPageCursor")
        if not page_cursor:
            break
        time.sleep(1)  # respect rate limit

    return all_results


def _item_text(item: dict) -> str:
    text_parts = [
        item.get("title", ""),
        item.get("site_name", ""),
        item.get("summary", ""),
        item.get("category", ""),
        item.get("source_url", ""),
    ]
    return " ".join(part for part in text_parts if isinstance(part, str)).lower()


def _is_tech_item(item: dict) -> bool:
    text = _item_text(item)
    if any(keyword in text for keyword in TECH_FEED_KEYWORDS):
        return True
    return any(domain in text for domain in TECH_DOMAINS)


def _is_non_tech_news_item(item: dict) -> bool:
    text = _item_text(item)
    return any(keyword in text for keyword in NON_TECH_NEWS_KEYWORDS)


def categorize_items(items: list[dict]) -> dict[str, list[dict]]:
    categorized = {"tech_news": [], "non_tech_news": []}

    for item in items:
        if _is_tech_item(item):
            categorized["tech_news"].append(item)
        elif _is_non_tech_news_item(item):
            categorized["non_tech_news"].append(item)
        else:
            categorized["non_tech_news"].append(item)

    return categorized


def main():
    token = os.environ.get("READWISE_TOKEN")
    if not token:
        print("Error: READWISE_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    items = fetch_rss_items(token)
    categorized_items = categorize_items(items)
    print(json.dumps(categorized_items, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
