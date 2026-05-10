# TODO — MyMuscleVideo Scraper

## Status: Scaffold ready, awaiting Codex implementation

### Implementation

- [ ] Copy/rename template files to `MyMuscleVideo.yml` / `MyMuscleVideo.py`
- [ ] Implement `sceneByURL` (OG meta + HTML DOM parsing)
- [ ] Implement `sceneByName` (`/search/video/?s=` endpoint)
- [ ] Handle both `https://mymusclevideo.com/` and `https://www.mymusclevideo.com/`
- [ ] Graceful fallbacks for all fields (title, date, description, image, tags)
- [ ] Set studio constant to `"MyMuscleVideo"`
- [ ] Confirm `og:video:release_date` is present across 5+ scene URLs

### Validation

- [ ] `sceneByURL`: `https://mymusclevideo.com/107027/sexy-guy-muscle/`
- [ ] `sceneByURL`: `https://mymusclevideo.com/115276/adam-riich/`
- [ ] `sceneByName`: `"muscle worship"`
- [ ] `sceneByName`: `"adam riich"`
- [ ] Returns empty result (no crash) for a 404 URL
- [ ] Tags list populated correctly from `/video/tag/` links

### Non-Goals

- performerByURL — login-gated (skip)
- sceneByFragment — no practical path (skip)
- sceneByQueryFragment — no practical path (skip)

### Publish

- [ ] Run `python3 scripts/validate_scraper_repo.py`
- [ ] Update root `README.md`
- [ ] Commit and push to `main`
