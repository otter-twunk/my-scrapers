# TheGay.com Scraper

Stash scraper for [TheGay.com](https://www.thegay.com/).

## Supported modes

| Mode | Supported |
|---|---|
| `sceneByURL` | ✅ |
| `sceneByName` | ❌ |
| `sceneByQueryFragment` | ❌ |
| `sceneByFragment` | ❌ |
| `performerByURL` | ❌ |

## Why limited support?

TheGay.com is part of the **TXXX network** and runs as a pure Vue SPA. The server returns
an empty HTML shell for every route — no `<title>`, no og: tags, no JSON-LD. All metadata
is loaded by JavaScript from an internal JSON API. Scene pages can be scraped by extracting
the video ID from the URL and querying that API directly. Search and performer routes have
no server-rendered data and cannot be scraped without a JS-capable headless browser.

## Install

1. Copy `TheGay.yml` and `TheGay.py` into your Stash scrapers directory.
2. Reload scrapers in Stash.

## Usage

- Paste a TheGay.com scene URL into the Stash scrape URL field:
  `https://www.thegay.com/video/{id}/{slug}/`
- Click **Scrape**.

## Requirements

- Python 3.7+
- No external Python packages required (`certifi` is used if available for SSL but is optional)

## Known limitations

- Description may be a comma-separated tag list rather than a prose synopsis on
  user-uploaded clips.
- Studio is always hard-coded to `TheGay.com` — no per-scene channel field in the API.
- Performer and search modes are not supported (SPA-only routes).

## Notes

- An `age_verified=1` cookie is sent automatically by the scraper.
- The internal API endpoint path (`API_ENDPOINT_PATH` in `TheGay.py`) must be confirmed
  against a live browser request before the scraper is considered production-ready.
  See `CODEX_PROMPT.md` for instructions.
