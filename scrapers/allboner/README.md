# allboner.com Stash Scraper

Files:

- `AllBonerScraper.yml`
- `AllBonerScraper.py`
- `SCRAPER_SPEC.json`
- `PERPLEXITY_TO_CODEX_HANDOFF.md`
- `CODEX_PROMPT.md`
- `TODO.md`

Install:

1. Copy `AllBonerScraper.yml` and `AllBonerScraper.py` into your Stash `scrapers` directory.
2. In Stash, reload scrapers or restart the app.

What it supports:

- `sceneByURL`
- `sceneByName`

Platform: KVS (Kernel Video Sharing)

Notes:

- Scraper implementation pending — this folder contains Perplexity research handoff files for Codex.
- Adult content source: keep scraping metadata-only.
- Cloudflare present; set age-gate cookies (`age_verified=1; kt_tc=1`).

Known limitations:

- Model/performer links not visible on sampled scene pages — may not be populated for all content.
- Cloudflare may tighten; implement fallback for 403/challenge responses.
- Adult content — keep scraper metadata-only.
