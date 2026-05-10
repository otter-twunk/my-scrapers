# Perplexity Research Input

Use this prompt before asking Codex to build a new scraper:

```text
Research how to build a Stash scraper for SITE_URL.

I want practical implementation research, not a generic overview.

Please do all of the following:

1. Review the official Stash scraper documentation and summarize only the parts relevant to building a script scraper for this site.
2. Inspect SITE_URL and determine:
   - whether the site is custom, WordPress, or another known platform
   - the structure of scene pages
   - the structure of performer pages
   - whether the site has search that can support title lookup
   - whether filename or fragment matching is likely to work
3. Identify how the following metadata appears on the site:
   - scene title
   - date
   - description
   - cover image
   - performers
   - tags or categories
   - studio or site name
4. Provide likely selectors, page patterns, or parsing strategies for extracting that metadata.
5. Note any blockers, anti-bot issues, missing metadata, inconsistent page layouts, or weak areas where scrape quality may be limited.
6. Recommend which Stash hook modes are realistic for this site:
   - sceneByURL
   - sceneByName
   - sceneByQueryFragment
   - sceneByFragment
   - performerByURL
7. Suggest a short URL-safe folder name for adding this scraper to the repo `otter-twunk/my-scrapers` under `scrapers/<folder-name>/`.

Output format:
- Short implementation summary
- Recommended supported hook modes
- Metadata field mapping
- Suggested selectors or parsing approach
- Known limitations
- Suggested folder name
- Source links
```
