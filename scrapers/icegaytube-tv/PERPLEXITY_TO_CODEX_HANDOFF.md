# Perplexity to Codex Handoff — IceGayTube

Create a working Stash scraper for https://www.icegaytube.tv/ in this repository.

## Repository

- Repo name: `otter-twunk/my-scrapers`
- Structure: one scraper per folder under `scrapers/<site-folder>/`
- This scraper lives in: `scrapers/icegaytube-tv/`

## Your Job

- Read the research in `SCRAPER_SPEC.json` and use it as the implementation contract
- Create `IceGayTube.py` and `IceGayTube.yml` inside this folder
- Keep `SCRAPER_SPEC.json`, `PERPLEXITY_TO_CODEX_HANDOFF.md`, and `CODEX_PROMPT.md` as-is
- Update `TODO.md` as you complete tasks
- Follow official Stash scraper conventions
- Preserve all other scrapers in the repo
- Update the root `README.md` to add `scrapers/icegaytube-tv` to the current scrapers list

## Implementation Requirements

- Use Python 3 for the script scraper
- Use the same pattern as `scrapers/justthegays-tv/JustTheGays.py` (stdlib-only, urllib + curl subprocess fallback, JSON-LD parsing)
- Support **sceneByURL**, **sceneByName**, and **performerByURL**
- Handle missing metadata gracefully — return empty string, not an error
- No third-party dependencies beyond Python stdlib and optional `certifi`

## Site Research Summary

### Platform

Custom tube site. Not WordPress. No Cloudflare challenge detected on public-facing pages during research. Age gate cookie should be sent defensively.

### URL Patterns

- Scene pages: `https://www.icegaytube.tv/movies/{id}/{slug}`
- Performer pages: `https://www.icegaytube.tv/pornstars/{slug}`
- Search: `https://www.icegaytube.tv/search/scenes?q={query}`

### Access Notes

- No Cloudflare challenge observed — standard urllib or curl should work.
- Set `age_verified=1` cookie defensively in all requests.
- Use a realistic Firefox/Linux User-Agent and `Accept: text/html`, `Accept-Language: en-US,en;q=0.5` headers.

### Metadata — Scene Page

Primary source is `og:*` meta tags. JSON-LD `VideoObject` may also be present (confirm on live page).

| Stash field | Source |
|---|---|
| title | `og:title` meta tag — strip ' at Ice Gay Tube' suffix |
| date | JSON-LD `VideoObject.uploadDate` (ISO-8601, strip to YYYY-MM-DD); fallback: `meta[name='date']` or visible date text |
| details | `og:description` meta tag; fallback: JSON-LD `VideoObject.description` |
| image | `og:image` meta tag; fallback: JSON-LD `VideoObject.thumbnailUrl[0]` |
| performers | `a[href*='/pornstars/']` anchor text in page HTML |
| tags | `a[href*='/category/']` or `a[href*='/search/']` anchor text in tag block |
| studio | `a[href*='/channel/']` anchor text; fallback constant: `IceGayTube` |

### Metadata — Performer Page

Performer pages at `/pornstars/{slug}` appear publicly accessible. Extract:
- Name: `og:title` or `<h1>` heading
- Photo: `og:image`
- Gender: hardcode `Male`
- Bio fields (birthdate, country, aliases): look for structured data or visible text labels on the page — structure TBD until live page is inspected

### Search — sceneByName

Search endpoint: `https://www.icegaytube.tv/search/scenes?q={title}`

- Fetch search results page
- Parse scene cards: extract scene URL from `a[href*='/movies/']` and title from card heading or `og:title`
- Return first matching result or a list of candidates
- No Cloudflare block expected on search pages

### Validated Example URLs

- Scene: `https://www.icegaytube.tv/movies/2493331/machine-fuck-him-danny-wolfe-maxence-angel`
  - Expected title: `Machine fuck Him - Danny Wolfe & Maxence angel`
  - Expected performers: Danny Wolfe, Maxence Angel
- Scene: `https://www.icegaytube.tv/movies/1116728/ultimate-str8-redneck-has-sex-with-chap-and-says-it-s-all-for-the-cash-data-max`

## Known Limitations

1. JSON-LD `VideoObject` presence is inferred — confirm it exists on a live scene page before relying on it as primary source.
2. Date field may be a relative string ('X days ago') — implement a parser or regex fallback.
3. Studio/channel may be absent on some scenes — always fall back to constant `IceGayTube`.
4. Performer list may be empty on amateur/untagged clips.
5. `sceneByFragment` and `sceneByQueryFragment` are not prioritised — implement only if search quality proves reliable.

## Validation Requirements

- Test `sceneByURL` against: `https://www.icegaytube.tv/movies/2493331/machine-fuck-him-danny-wolfe-maxence-angel`
  - Confirm: title, image, performers (Danny Wolfe, Maxence Angel), tags populated
- Test `sceneByName` with query `machine fuck him danny wolfe`
  - Confirm: first result returns the correct scene URL
- Test `performerByURL` against a performer page from `https://www.icegaytube.tv/pornstars`
  - Confirm: name and image populated; document any missing bio fields

## Repo Helpers

- Reference implementation: `scrapers/justthegays-tv/JustTheGays.py` (same stdlib pattern)
- Template: `templates/site-template/SiteScraper.py` and `SiteScraper.yml`
- Checklist: `workflow/NEW_SCRAPER_CHECKLIST.md`
