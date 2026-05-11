# Codex Prompt — IceGayTube Scraper

Create a working Stash scraper for https://www.icegaytube.tv/ in this repository.

## Start

All research is already done. Use the files in `scrapers/icegaytube-tv/` to build the scraper:

1. Read `SCRAPER_SPEC.json` — this is the implementation contract
2. Read `PERPLEXITY_TO_CODEX_HANDOFF.md` — this has full site notes and field mapping
3. Use `scrapers/justthegays-tv/JustTheGays.py` as the reference implementation pattern
4. Create `IceGayTube.py` and `IceGayTube.yml` in `scrapers/icegaytube-tv/`
5. Update `TODO.md` as tasks are completed
6. Update the root `README.md` to add `scrapers/icegaytube-tv` to the current scrapers list

## Requirements

- Python 3, stdlib only (+ optional certifi for SSL)
- urllib request + curl subprocess fallback (same as justthegays-tv pattern)
- Supported hooks: `sceneByURL`, `sceneByName`, `performerByURL`
- `sceneByFragment` and `sceneByQueryFragment` — do NOT implement unless explicitly asked
- Parse scene metadata primarily from `og:*` meta tags; use JSON-LD `VideoObject` as secondary source if confirmed present
- Set `age_verified=1` cookie in all HTTP requests
- Realistic browser User-Agent and Accept headers required
- Handle missing or empty fields gracefully (return empty string, not error)
- One scraper per site — do not modify other scraper folders

## Key Facts

- Scene URL pattern: `https://www.icegaytube.tv/movies/{id}/{slug}`
- Performer URL pattern: `https://www.icegaytube.tv/pornstars/{slug}`
- Search URL pattern: `https://www.icegaytube.tv/search/scenes?q={query}`
- No Cloudflare challenge detected — standard urllib/curl should work for all routes
- Primary metadata source: `og:title`, `og:description`, `og:image` meta tags
- Performer links on scene pages: `a[href*='/pornstars/']`
- Tag links on scene pages: `a[href*='/category/']`
- Studio: `a[href*='/channel/']` or constant fallback `IceGayTube`
- Validated scenes:
  - `https://www.icegaytube.tv/movies/2493331/machine-fuck-him-danny-wolfe-maxence-angel`
  - `https://www.icegaytube.tv/movies/1116728/ultimate-str8-redneck-has-sex-with-chap-and-says-it-s-all-for-the-cash-data-max`
