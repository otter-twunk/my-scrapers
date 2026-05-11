# xvideos.com Stash Scraper

Files:

- `XVideosScraper.yml`
- `XVideosScraper.py`
- `SCRAPER_SPEC.json`
- `PERPLEXITY_TO_CODEX_HANDOFF.md`
- `CODEX_PROMPT.md`
- `TODO.md`

Install:

1. Copy `XVideosScraper.yml` and `XVideosScraper.py` into your Stash `scrapers` directory.
2. In Stash, reload scrapers or restart the app.

What it supports:

- `sceneByURL`
- `sceneByName`
- `performerByURL`

Platform: Custom/proprietary (XVideos in-house platform)

Notes:

- Scraper implementation pending — this folder contains Perplexity research handoff files for Codex.
- Adult content source: keep scraping metadata-only.

Known limitations:

- video_models array is frequently empty on amateur/upload pages.
- Performer pages use /profiles/ not a dedicated pornstar path for user-uploaded content.
- Signed CDN media URLs expire; do not store raw stream URLs.
- Content URLs include signed tokens and should not be followed for download.
