#!/usr/bin/env python3
"""Fetch RSS feed items from Readwise Reader API for the past 24 hours."""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone


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


def main():
    token = os.environ.get("READWISE_TOKEN")
    if not token:
        print("Error: READWISE_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    items = fetch_rss_items(token)
    print(json.dumps(items, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
