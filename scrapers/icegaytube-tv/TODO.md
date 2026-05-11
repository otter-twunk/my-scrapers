# TODO — IceGayTube Scraper

## Pre-implementation (Codex first step)

- [ ] Fetch a live scene page and confirm presence/absence of JSON-LD `VideoObject` block
- [ ] Confirm date field format (ISO-8601 string vs relative 'X days ago' text)
- [ ] Confirm performer link selector (`a[href*='/pornstars/']`) is present in scene page HTML
- [ ] Confirm tag link selector (`a[href*='/category/']`) is present in scene page HTML
- [ ] Confirm studio/channel selector (`a[href*='/channel/']`) or note if absent
- [ ] Fetch a performer page and document available fields

## Implementation

- [ ] Create `IceGayTube.py` based on justthegays-tv pattern
- [ ] Create `IceGayTube.yml` with sceneByURL, sceneByName, and performerByURL hooks
- [ ] Implement `sceneByURL` — fetch scene page, parse og:* tags + JSON-LD fallback
- [ ] Implement `sceneByName` — fetch search results, return first matching scene URL
- [ ] Implement `performerByURL` — fetch performer page, parse name, image, gender
- [ ] Set `age_verified=1` cookie in all requests
- [ ] Handle missing metadata fields gracefully
- [ ] Handle relative date strings if needed (e.g. '3 days ago' → approximate YYYY-MM-DD)

## Validation

- [ ] Test sceneByURL against `https://www.icegaytube.tv/movies/2493331/machine-fuck-him-danny-wolfe-maxence-angel`
  - [ ] title: "Machine fuck Him - Danny Wolfe & Maxence angel"
  - [ ] performers: Danny Wolfe, Maxence Angel
  - [ ] image URL populated
  - [ ] tags populated
  - [ ] date populated
- [ ] Test sceneByURL against `https://www.icegaytube.tv/movies/1116728/ultimate-str8-redneck-has-sex-with-chap-and-says-it-s-all-for-the-cash-data-max`
- [ ] Test sceneByName with query `machine fuck him danny wolfe` — confirm first result is correct scene
- [ ] Test performerByURL against a real performer slug from `/pornstars`
  - [ ] Document what fields are available

## Repo

- [ ] Write `README.md` for this scraper folder
- [ ] Update root `README.md` to add `scrapers/icegaytube-tv` to current scrapers list
- [ ] Run `scripts/validate_scraper_repo.py` if available

## Known Unknowns (resolve during pre-implementation)

- JSON-LD VideoObject: present or absent? (inferred from site type — not confirmed)
- Date format: machine-readable or relative text?
- Studio/channel field: present on scene pages?
- Performer bio fields: what is available on performer pages?
