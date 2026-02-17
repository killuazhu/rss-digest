---
name: rss-digest
description: Fetch and summarize the top 5 RSS news items from the past 24 hours using the Readwise Reader API. Use when the user wants a daily news digest or RSS summary.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["READWISE_TOKEN"]},"emoji":"📰"}}
---

# RSS Daily Digest

Fetch and summarize the top 5 RSS news items from the past 24 hours using the Readwise Reader API.

## Steps

1. **Fetch RSS documents**: Run the bundled fetch script:

   ```bash
   python3 {baseDir}/fetch_rss.py
   ```

   This calls the Readwise Reader API (`GET https://readwise.io/api/v3/list/?location=feed&updatedAfter=<24h-ago-ISO8601>`) using the `READWISE_TOKEN` environment variable. It handles pagination automatically and outputs JSON to stdout.

2. **Select the top 5**: From all fetched RSS items, pick the 5 most interesting/important articles. Prioritize by:
   - Recency (prefer newer items)
   - Diversity of sources (avoid clustering from a single feed)
   - Significance of the topic (major events, breaking news, high-impact stories)

3. **Generate the digest**: For each of the top 5, output:

   ```
   ### <number>. <title>
   **Source:** <site_name or author>  |  **Published:** <published_date>
   **Link:** <url>

   <2-3 sentence summary of the article based on the `summary` field and any available content>
   ```

   Then add an overall **TL;DR** section at the top with a 2-3 sentence synthesis of the day's key themes.

## Output Format

```
# Daily RSS Digest — <today's date>

## TL;DR
<Overall synthesis of today's key themes across all articles>

---

### 1. <Title>
**Source:** ...  |  **Published:** ...
**Link:** ...

<Summary>

### 2. <Title>
...
```

## Important Notes

- If fewer than 5 RSS items exist for the past day, summarize all available items and note the total count.
- If the fetch script returns an error about `READWISE_TOKEN`, stop and ask the user to set it (tokens are available at https://readwise.io/access_token).
