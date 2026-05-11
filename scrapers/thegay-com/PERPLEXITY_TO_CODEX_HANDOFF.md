# Perplexity → Codex Handoff: TheGay.com

Create a working Stash scraper for **https://www.thegay.com/** in this repository.

## Repository

- Repo: `otter-twunk/my-scrapers`
- Scraper folder: `scrapers/thegay-com/`

## Your job

- Read the research below and `SCRAPER_SPEC.json` as the primary implementation guide
- Complete the scraper in `scrapers/thegay-com/`
- Files to produce / complete:
  - `TheGay.py` — the backing Python script (stub is present; implement it fully)
  - `TheGay.yml` — the Stash scraper descriptor (stub is present; adjust if hook set changes)
  - `README.md` — short site-specific notes
  - Keep `SCRAPER_SPEC.json`, `PERPLEXITY_TO_CODEX_HANDOFF.md`, `CODEX_PROMPT.md`, `TODO.md` in the folder
- Follow official Stash scraper conventions
- Preserve all existing scrapers and repo structure
- Update the root `README.md` with the new scraper folder entry

## Implementation requirements

- Prefer Python (no heavy dependencies)
- Support `sceneByURL` as the primary and likely only reliable hook mode
- Keep the scraper scoped to thegay.com
- Handle missing or null metadata fields gracefully — return partial results, never crash
- The `age_verified=1` cookie is mandatory on all requests

## Site overview

TheGay.com is part of the **TXXX network** — the same Vue SPA codebase used by HClips, HDZog,
HotMovs, Upornia, TXXX, and ~10 other tube sites. Every page route is rendered entirely in
JavaScript. The HTML shell the server returns for any URL is essentially empty: blank `<title>`,
no og: tags, no JSON-LD. All video metadata is fetched by the Vue app from an internal JSON API
after the page loads.

## Critical first step for Codex

Before writing a single line of scraper logic, **open a scene page in a browser and inspect
the Network tab (XHR/Fetch filter)** to find the exact API endpoint the Vue app calls to load
video data. The expected pattern based on TXXX network analysis is:

```
GET https://www.thegay.com/api/json/video/{id}
Headers:
  User-Agent: Firefox UA
  Referer: https://www.thegay.com/video/{id}/{slug}/
  Cookie: age_verified=1
  Accept: application/json
```

The video ID is the first numeric segment in the URL: `/video/748987/slug/` → ID = `748987`.

The stub at `TheGay.py` already implements the URL-to-ID extraction and the fetch/parse scaffold.
Replace `API_ENDPOINT_PATH` with the confirmed path and implement the JSON field mapping
using the field names in `SCRAPER_SPEC.json`.

## URL patterns

| Type | Pattern |
|---|---|
| Scene page | `https://www.thegay.com/video/{id}/{slug}/` |
| Performer page | `https://www.thegay.com/pornstar/{slug}/` |
| Search | `https://www.thegay.com/search/{query}/` |

Performer pages and search routes are SPA-only — no server-rendered data. Only `sceneByURL` is
practical without a JS-capable headless browser.

## Expected API response fields

| Stash field | API key(s) to try |
|---|---|
| title | `title`, `name` |
| date | `post_date`, `added`, `date` |
| details | `description`, `text` |
| image | `thumbs[0].src`, `thumb_url`, `preview_url` |
| performers | `models[].title` or `models[].name`, also `pornstars[]` |
| tags | `categories[].title`, `tags[].title` |
| studio | Hard-code to `"TheGay.com"` |

## Known limitations

- `sceneByName`, `sceneByQueryFragment`, `sceneByFragment` — not supported (SPA search routes)
- `performerByURL` — not supported (SPA performer routes, no server-rendered data)
- Description may be a tag list rather than prose on user-uploaded clips
- Studio is always `TheGay.com` — no per-scene channel field in the API

## Validation

Test `sceneByURL` against:
```
https://www.thegay.com/video/748987/bareback-gay-sex-with-jerk/
```

Expect: title, date, image, performers, and tags to be populated.

## Research date

2026-05-11
