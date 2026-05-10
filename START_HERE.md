# Start Here

This repo is set up for a repeatable Stash scraper workflow.

## Fastest Path

1. Run the research prompt in `workflow/PERPLEXITY_RESEARCH_INPUT.md`.
2. Paste the result into `workflow/PERPLEXITY_TO_CODEX_HANDOFF.md`.
3. Give that handoff prompt to Codex.
4. Validate the finished scraper with `workflow/NEW_SCRAPER_CHECKLIST.md`.

## If You Want Codex To Work Directly

Use `workflow/CODEX_PROMPT.md` and point Codex at this repo.

## Where New Scrapers Go

Create each new scraper under:

- `scrapers/<site-folder>/`

Each scraper folder should contain:

- the `.yml` scraper definition
- the backing Python script
- a short `README.md`

## Starting Template

Use:

- `templates/site-template/`

Copy it, rename the files, then implement the site-specific logic.

## Final Check

Before publishing, run through:

- `workflow/NEW_SCRAPER_CHECKLIST.md`
