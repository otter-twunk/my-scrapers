# Codex Prompt — GayPornTube

Create a working Stash scraper for https://www.gayporntube.com/ in this repository.

## Requirements

- Follow the existing repo structure: one scraper per folder under `scrapers/gayporntube-com/`
- Create `GayPornTube.py` and `GayPornTube.yml` inside this folder
- Keep folder-local workflow notes: `SCRAPER_SPEC.json`, `PERPLEXITY_TO_CODEX_HANDOFF.md`, `CODEX_PROMPT.md`, `TODO.md`
- Follow official Stash scraper conventions
- Prefer Python 3 stdlib-only (urllib + curl subprocess fallback, like `scrapers/justthegays-tv/JustTheGays.py`)
- Preserve all existing scrapers
- Update the root `README.md` to list `scrapers/gayporntube-com`

## Supported Hook Modes

| Mode | Support |
|---|---|
| sceneByURL | ✅ Required |
| sceneByName | ✅ Required |
| sceneByQueryFragment | ✅ Required |
| sceneByFragment | ✅ Required |
| performerByURL | ❌ Not supported — site has no performer pages |

## Implementation Guide

See `SCRAPER_SPEC.json` for the full machine-friendly implementation contract and `PERPLEXITY_TO_CODEX_HANDOFF.md` for the full research record.

### Key points

1. **sceneByURL**: fetch `https://www.gayporntube.com/video/{id}/{slug}`, parse JSON-LD `VideoObject`
2. **sceneByName / fragment modes**: search `https://www.gayporntube.com/search/videos/?q={query}`, parse result links (`a[href*='/video/']` with numeric ID), pick best title match using `difflib.SequenceMatcher`
3. **Headers required on all requests**:
   - `User-Agent`: realistic Firefox/Linux string
   - `Cookie: age_verified=1`
   - `Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8`
   - `Accept-Language: en-US,en;q=0.5`
4. **Metadata extraction**:
   - title: `VideoObject.name` → fallback `og:title` → fallback `h1.title`
   - date: `VideoObject.uploadDate`, strip to `YYYY-MM-DD`
   - details: `VideoObject.description` — sanitise: if value contains only whitespace/emoji/stars, return `""`
   - image: `VideoObject.thumbnailUrl` (plain string)
   - performers: return `[]` (not available)
   - tags: combine `div.video-info-tags > a` text AND `div.video-info-categories > a` text
   - studio: constant `"GayPornTube"`
5. **No performerByURL** — omit from `.yml`

## Validation

Test `sceneByURL` against:
- `https://www.gayporntube.com/video/2041527/ass-addiction`
- `https://www.gayporntube.com/video/2041520/help-cumming-00`

Test `sceneByName` with query: `bareback`

Document any fields that consistently return empty.
