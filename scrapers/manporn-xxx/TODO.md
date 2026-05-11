# TODO — ManPorn Scraper

## Pre-Implementation

- [x] Do a live fetch of `https://manporn.xxx/videos/3400273/hot-threesome-action-with-indian-pornstars/` and confirm:
  - [x] Page responds successfully (no Cloudflare block) with Firefox UA + `age_verified=1` cookie
  - [x] JSON-LD VideoObject block is present in the HTML
  - [x] Confirm correct age-gate cookie name (live fetch worked with `age_verified=1`)
  - [x] Note actual field names in the VideoObject block (`thumbnailUrl`, `uploadDate`, `keywords`)

## Implementation

- [x] Create `ManPorn.py` based on justthegays-tv + boyfriendtv-com pattern
- [x] Complete `ManPorn.yml` with sceneByURL and performerByURL hooks
- [x] Implement `sceneByURL` — fetch scene page, parse JSON-LD VideoObject
- [x] Implement `performerByURL` — attempt fetch; return name-from-slug + gender fallback on CF block
- [x] Set age-gate cookie in all requests
- [x] Handle missing metadata fields gracefully

## Validation

- [x] Test sceneByURL against `https://manporn.xxx/videos/3400273/hot-threesome-action-with-indian-pornstars/`
  - [x] title populated
  - [x] date populated (YYYY-MM-DD)
  - [ ] performers populated
  - [x] tags populated
  - [x] image URL populated
  - [x] studio: "ManPorn"
- [x] Test performerByURL against `https://manporn.xxx/models/reign/`
  - [x] Document what is returned: name + gender + generic description, no image observed
- [x] Test performerByURL against `https://manporn.xxx/models/zbynek-onderka/`

## Repo

- [x] Write `README.md` for this scraper folder
- [x] Update root `README.md` to add `scrapers/manporn-xxx` to current scrapers list
- [x] Run `scripts/validate_scraper_repo.py`

## Known Blockers

- sceneByName / sceneByQueryFragment / sceneByFragment: search expected to be Cloudflare-blocked — do not implement
- performerByURL: performer pages may trigger CF challenge — return minimal data (name + gender) as fallback
- Age-gate cookie name unconfirmed — must validate on first live fetch
