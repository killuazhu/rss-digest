---
name: rss-digest
description: Fetch and summarize RSS news from the past 24 hours grouped into tech and non-tech sections, with top 5 items per section, and generate a 10-minute podcast script.
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

3. **Generate the written digest**:
   - Provide a 2-3 sentence overall **TL;DR** at the top.
   - Then provide two sections: **Tech News (Top 5)** and **Non-Tech News (Top 5)**.
   - For each item, output:

   ```
   ### <number>. <title>
   **Source:** <site_name or author>  |  **Published:** <published_date>
   **Link:** <url>

   <2-3 sentence summary based on the `summary` field and any available content>
   ```

4. **Generate a 10-minute podcast package from today's RSS digest**:
   - Create a spoken-word script targeting **~10 minutes** (roughly **1,250-1,500 words** at normal speaking pace).
   - Keep tone conversational, concise, and neutral.
   - Structure into:
     - Intro (30-45 sec): show opening + key themes
     - Tech segment (4-5 min): top 5 stories
     - Non-tech segment (4-5 min): top 5 stories
     - Outro (30-45 sec): key takeaways + sign-off
   - Add timestamps for each segment.
   - For each story in the podcast script, mention source and summarize in 2-4 spoken sentences.
   - End with a short “What to watch tomorrow” section with 3 bullets.

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

---

## 10-Minute Podcast Script

**Estimated Duration:** ~10 minutes
**Target Word Count:** 1,250-1,500 words

### [00:00-00:45] Intro
<Host script>

### [00:45-05:00] Tech News Segment
<Host script covering top 5 tech items>

### [05:00-09:15] Non-Tech News Segment
<Host script covering top 5 non-tech items>

### [09:15-10:00] Outro + What to Watch Tomorrow
<Host script>

**What to Watch Tomorrow**
- <signal 1>
- <signal 2>
- <signal 3>
```

## Important Notes

- If a section has fewer than 5 items, summarize all available items and note the total count for that section.
- If one section is empty, explicitly state that no qualifying items were found in the last 24 hours and rebalance podcast timing toward the available section.
- If the fetch script returns an error about `READWISE_TOKEN`, stop and ask the user to set it (tokens are available at https://readwise.io/access_token).
- If summaries are sparse, clearly mark assumptions and avoid fabricating facts.
