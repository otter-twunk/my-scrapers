# everydayporn.co Stash Scraper

Files:

- `EverydayPornScraper.yml`
- `EverydayPornScraper.py`
- `SCRAPER_SPEC.json`
- `PERPLEXITY_TO_CODEX_HANDOFF.md`
- `CODEX_PROMPT.md`
- `TODO.md`

Install:

1. Copy `EverydayPornScraper.yml` and `EverydayPornScraper.py` into your Stash `scrapers` directory.
2. In Stash, reload scrapers or restart the app.

What it supports:

- `sceneByURL`
- `sceneByName`

Platform: KVS-like tube platform

Notes:

- Scraper implementation pending — this folder contains Perplexity research handoff files for Codex.
- Adult content source: keep scraping metadata-only.
- JSON-LD VideoObject present on scene pages — prefer it over OG tags.

Known limitations:

- Performer/model links not present on sampled scene pages.
- Studio/source links not confirmed — may not be populated for all content.
- Platform appears KVS-like but exact CMS unconfirmed — avoid hardcoding KVS-specific assumptions.
