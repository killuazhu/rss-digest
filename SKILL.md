---
name: rss-digest
description: Fetch and summarize RSS news from the past 24 hours grouped into tech and non-tech sections, with top 5 items per section.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["READWISE_TOKEN"]},"emoji":"📰"}}
---

# RSS Daily Digest

Fetch and summarize RSS news from the past 24 hours using the Readwise Reader API.

## Steps

1. **Fetch RSS documents**: Run the bundled fetch script:

   ```bash
   python3 {baseDir}/fetch_rss.py
   ```

   This calls the Readwise Reader API (`GET https://readwise.io/api/v3/list/?location=feed&updatedAfter=<24h-ago-ISO8601>`) using the `READWISE_TOKEN` environment variable. It handles pagination automatically and outputs categorized JSON to stdout with:
   - `tech_news`: tech-focused RSS items
   - `non_tech_news`: general/non-tech RSS items (e.g., economy, politics, business)

2. **Pick top items in each section**:
   - Select the **top 5** items from `tech_news`
   - Select the **top 5** items from `non_tech_news`

   Prioritize by:
   - Recency (prefer newer items)
   - Diversity of sources (avoid clustering from a single feed)
   - Significance of the topic (major events, breaking news, high-impact stories)

3. **Generate the digest**:
   - Provide a 2-3 sentence overall **TL;DR** at the top.
   - Then provide two sections: **Tech News (Top 5)** and **Non-Tech News (Top 5)**.
   - For each item, output:

   ```
   ### <number>. <title>
   **Source:** <site_name or author>  |  **Published:** <published_date>
   **Link:** <url>

   <2-3 sentence summary based on the `summary` field and any available content>
   ```

## Output Format

```
# Daily RSS Digest — <today's date>

## TL;DR
<Overall synthesis of today's key themes across both sections>

---

## Tech News (Top 5)

### 1. <Title>
**Source:** ...  |  **Published:** ...
**Link:** ...

<Summary>

...

## Non-Tech News (Top 5)

### 1. <Title>
**Source:** ...  |  **Published:** ...
**Link:** ...

<Summary>

...
```

## Important Notes

- If a section has fewer than 5 items, summarize all available items and note the total count for that section.
- If one section is empty, explicitly state that no qualifying items were found in the last 24 hours.
- If the fetch script returns an error about `READWISE_TOKEN`, stop and ask the user to set it (tokens are available at https://readwise.io/access_token).
