# TODO — MyMuscleVideo Scraper

## Status: Implemented and locally validated

### Implementation

- [x] Copy/rename template files to `MyMuscleVideo.yml` / `MyMuscleVideo.py`
- [x] Implement `sceneByURL` (OG meta + HTML DOM parsing)
- [x] Implement `sceneByName` (`/search/video/?s=` endpoint)
- [x] Handle both `https://mymusclevideo.com/` and `https://www.mymusclevideo.com/`
- [x] Graceful fallbacks for all fields (title, date, description, image, tags)
- [x] Set studio constant to `"MyMuscleVideo"`
- [x] Confirm `og:video:release_date` on the validated scene URLs

### Validation

- [x] `sceneByURL`: `https://mymusclevideo.com/107027/sexy-guy-muscle/`
- [x] `sceneByURL`: `https://mymusclevideo.com/115276/adam-riich/`
- [x] `sceneByName`: `"muscle worship"`
- [x] `sceneByName`: `"adam riich"`
- [x] Returns empty result (no crash) for a 404 URL
- [x] Tags list populated correctly from `/video/tag/` links

### Non-Goals

- performerByURL — login-gated (skip)
- sceneByFragment — no practical path (skip)
- sceneByQueryFragment — no practical path (skip)

### Publish

- [ ] Run `python3 scripts/validate_scraper_repo.py`
- [x] Update root `README.md`
- [ ] Commit and push to `main`

Repo-wide validator is currently blocked by pre-existing `gayporntube-com` issues unrelated to this scraper:

- missing scraper `.py` file
- `SCRAPER_SPEC.json` missing `sources`
- `SCRAPER_SPEC.json` missing `validation_examples`
