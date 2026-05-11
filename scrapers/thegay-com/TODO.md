# TODO — TheGay.com scraper

## Blocked on (Codex must do first)

- [ ] **Confirm internal API endpoint** — open a scene page in browser DevTools (Network >
  Fetch/XHR) and record the exact path the Vue app uses to load video JSON. Expected:
  `/api/json/video/{id}`. Replace `API_ENDPOINT_PATH` in `TheGay.py`.

## Implementation

- [ ] Implement `scrape_scene()` in `TheGay.py` using confirmed API endpoint
- [ ] Map all JSON fields per `SCRAPER_SPEC.json` metadata_mapping section
- [ ] Handle missing/null fields gracefully
- [ ] Verify `age_verified=1` cookie is sent on all requests
- [ ] Handle API response wrapper keys (`data`, `video`, or direct root object)

## Validation

- [ ] Test `sceneByURL` against `https://www.thegay.com/video/748987/bareback-gay-sex-with-jerk/`
- [ ] Confirm title, date, image, performers, tags are populated
- [ ] Confirm graceful empty result when URL does not match a real video

## Docs

- [ ] Write `README.md` with install instructions and known limitations
- [ ] Update root `README.md` to add `scrapers/thegay-com/` entry

## Out of scope (until further research)

- sceneByName — SPA search, no server-rendered results
- sceneByQueryFragment / sceneByFragment — same blocker
- performerByURL — SPA performer pages, no server-rendered data
