# TODO — IceGayTube Scraper

## Pre-implementation (Codex first step)

- [x] Fetch a live scene page and confirm presence/absence of JSON-LD `VideoObject` block
- [x] Confirm date field format (relative `X years ago` text on sampled scene)
- [x] Confirm performer link selector is present in scene page HTML (`/pornstar/` on live page)
- [x] Confirm tag link selector (`a[href*='/category/']`) is present in scene page HTML
- [x] Confirm studio/channel selector (`a[href*='/channel/']`) or note if absent
- [x] Fetch a performer page and document available fields

## Implementation

- [x] Create `IceGayTube.py` based on justthegays-tv pattern
- [x] Create `IceGayTube.yml` with sceneByURL, sceneByName, and performerByURL hooks
- [x] Implement `sceneByURL` — fetch scene page, parse live HTML metadata
- [x] Implement `sceneByName` — fetch search results, return matching scene URLs
- [x] Implement `performerByURL` — fetch performer page, parse name, gender, details
- [x] Set `age_verified=1` cookie in all requests
- [x] Handle missing metadata fields gracefully
- [x] Handle relative date strings if needed (e.g. '3 days ago' → approximate YYYY-MM-DD)

## Validation

- [x] Test sceneByURL against `https://www.icegaytube.tv/movies/2493331/machine-fuck-him-danny-wolfe-maxence-angel`
  - [x] title: "Machine fuck Him - Danny Wolfe & Maxence angel"
  - [x] performers: Danny Wolfe, Maxence Angel
  - [x] image URL populated
  - [x] tags populated
  - [x] date populated
- [ ] Test sceneByURL against `https://www.icegaytube.tv/movies/1116728/ultimate-str8-redneck-has-sex-with-chap-and-says-it-s-all-for-the-cash-data-max`
- [x] Test sceneByName with query `machine fuck him danny wolfe` — confirm first result is correct scene
- [x] Test performerByURL against a real performer slug from `/pornstars`
  - [x] Document what fields are available: name + gender + description, no image observed

## Repo

- [x] Write `README.md` for this scraper folder
- [x] Update root `README.md` to add `scrapers/icegaytube-tv` to current scrapers list
- [x] Run `scripts/validate_scraper_repo.py`

## Known Unknowns (resolve during pre-implementation)

- JSON-LD VideoObject: present or absent? (inferred from site type — not confirmed)
- Date format: machine-readable or relative text?
- Studio/channel field: present on scene pages?
- Performer bio fields: what is available on performer pages?
