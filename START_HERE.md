# Start Here

This repo is set up for a repeatable Stash scraper workflow.

## Fastest Path

1. Run the research prompt in `workflow/PERPLEXITY_RESEARCH_INPUT.md`.
2. Have Perplexity choose and scaffold `scrapers/<site-folder>/` using the repo conventions and generic brief.
3. Have Perplexity fill in that folder, especially:
   - `SCRAPER_SPEC.json`
   - `PERPLEXITY_TO_CODEX_HANDOFF.md`
   - `CODEX_PROMPT.md`
4. Give Codex the prompt in `workflow/SIMPLE_CODEX_START.md`.
5. Validate the finished scraper with `workflow/NEW_SCRAPER_CHECKLIST.md`.

## If You Want Codex To Work Directly

Use `workflow/CODEX_PROMPT.md` and point Codex at this repo.

## Where New Scrapers Go

Create each new scraper under:

- `scrapers/<site-folder>/`

Each scraper folder should contain:

- the `.yml` scraper definition
- the backing Python script
- a short `README.md`
- `SCRAPER_SPEC.json`
- `PERPLEXITY_TO_CODEX_HANDOFF.md`
- `CODEX_PROMPT.md`
- `TODO.md`

## Starting Template

Perplexity or Codex can scaffold from:

- `templates/site-template/`

The preferred flow is for Perplexity to apply that template logic and repo rules when creating the new scraper folder.

## Final Check

Before publishing, run through:

- `workflow/NEW_SCRAPER_CHECKLIST.md`
- `python3 scripts/validate_scraper_repo.py`
