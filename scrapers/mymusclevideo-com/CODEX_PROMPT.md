# Codex Prompt: MyMuscleVideo Scraper

Create a working Stash scraper for **https://mymusclevideo.com/** in this repository.

## Requirements

- Follow the existing repo structure: one scraper per folder under `scrapers/<site-folder>/`
- Folder: `scrapers/mymusclevideo-com/`
- Include:
  - `MyMuscleVideo.yml`
  - `MyMuscleVideo.py`
  - `README.md`
- Keep:
  - `SCRAPER_SPEC.json`
  - `PERPLEXITY_TO_CODEX_HANDOFF.md`
  - `CODEX_PROMPT.md`
- Follow official Stash scraper conventions
- Support `sceneByURL` and `sceneByName`
- Do NOT implement `performerByURL`, `sceneByFragment`, `sceneByQueryFragment`
- Python only, stdlib + optional certifi
- Test against live pages if possible
- Preserve existing scrapers
- Update the root `README.md` with the new scraper folder

## Also

- Start from `templates/site-template/`
- Rename the template files to `MyMuscleVideo.yml` and `MyMuscleVideo.py`
- Document limitations (no performers, low-res cover, no performerByURL)
- Use `SCRAPER_SPEC.json` as the primary machine-friendly implementation guide
- Use `PERPLEXITY_TO_CODEX_HANDOFF.md` for full research context and code stubs
