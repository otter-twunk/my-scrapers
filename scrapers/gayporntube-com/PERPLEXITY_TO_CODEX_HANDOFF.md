# Perplexity to Codex Handoff — GayPornTube

Create a working Stash scraper for https://www.gayporntube.com/ in this repository.

## Repository

- Repo name: `otter-twunk/my-scrapers`
- Structure: one scraper per folder under `scrapers/<site-folder>/`
- This scraper lives in: `scrapers/gayporntube-com/`

## Your Job

- Read the research in `SCRAPER_SPEC.json` and use it as the implementation contract
- Create `GayPornTube.py` and `GayPornTube.yml` inside this folder
- Keep `SCRAPER_SPEC.json`, `PERPLEXITY_TO_CODEX_HANDOFF.md`, and `CODEX_PROMPT.md` as-is
- Update `TODO.md` as you complete tasks
- Follow official Stash scraper conventions
- Preserve all other scrapers in the repo
- Update the root `README.md` to add `scrapers/gayporntube-com` to the current scrapers list

## Implementation Requirements

- Use Python 3 for the script scraper
- Use the same pattern as `scrapers/justthegays-tv/JustTheGays.py` (stdlib-only, urllib + curl subprocess fallback, JSON-LD parsing)
- Support **sceneByURL**, **sceneByName**, **sceneByQueryFragment**, and **sceneByFragment**
- **performerByURL is NOT supported** — this site has no performer/model pages
- Handle missing metadata gracefully — return empty string or empty list, not an error
- No third-party dependencies beyond Python stdlib and optional `certifi`

## Site Research Summary

### Platform

Custom tube site. Not WordPress. **No Cloudflare protection** — all pages respond cleanly to a standard Firefox UA with the `age_verified=1` cookie.

### URL Patterns

- Scene pages: `https://www.gayporntube.com/video/{id}/{slug}`
- Search pages: `https://www.gayporntube.com/search/videos/?q={query}` — **accessible, returns HTML results**
- Performer pages: **None** — site has no model/performer section

### Access Requirements

- Set `Cookie: age_verified=1` on all requests
- Use a realistic Firefox/Linux User-Agent
- Standard `Accept: text/html` and `Accept-Language: en-US,en;q=0.5` headers
- Python urllib and curl subprocess both work fine

### Metadata — Scene Page

All key scene metadata is in the `application/ld+json` block of type `VideoObject`:

| Stash field | Source |
|---|---|
| title | `VideoObject.name` |
| date | `VideoObject.uploadDate` (ISO-8601, strip to `YYYY-MM-DD`) |
| details | `VideoObject.description` — **sanitise**: often just `⭐⭐⭐⭐⭐`; return empty string if no real text |
| image | `VideoObject.thumbnailUrl` (plain string, CDN URL) |
| performers | **Not available** — return empty list |
| tags | CSS `div.video-info-tags > a` anchor text |
| studio | Constant: `GayPornTube` |

Additionally, CSS `div.video-info-categories > a` anchor text gives channel/category labels (e.g. `Ass Play`, `Muscle Boys`). Merge these into the tags list for richer tagging.

Fallbacks:
- title: `og:title` meta → `<h1 class="title">` inner text
- image: `og:image` meta

### Search — sceneByName / sceneByQueryFragment / sceneByFragment

- Endpoint: `https://www.gayporntube.com/search/videos/?q={query}`
- Results page contains `<a href="/video/{id}/{slug}">` links
- Use `difflib.SequenceMatcher` (already used in `JustTheGays.py`) to pick the best title match
- For `sceneByFragment`: use the scene title from the fragment as the search query
- For `sceneByQueryFragment`: use available title/filename fields as the search query

### No Performer Scraping

This site does not have model or performer profile pages. Do not implement `performerByURL`. The `.yml` should omit the `performerByURL` section entirely.

## Known Limitations

- `description` is frequently star-rating emoji — sanitise by stripping if no real text remains
- Performer metadata is unavailable
- Tags are sparse (0–2 per scene is typical)
- Category links (`/channels/{id}/{slug}/`) are merged into tags as the best available enrichment
- Title matching for fragment modes is best-effort

## Test URLs

```
https://www.gayporntube.com/video/2041527/ass-addiction
https://www.gayporntube.com/video/2041520/help-cumming-00
https://www.gayporntube.com/video/2041464/a-perfect-cock2
```

Search test:
```
https://www.gayporntube.com/search/videos/?q=bareback
```
