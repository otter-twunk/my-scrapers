# Repo Workflow

Use this reference when the target repo follows the `my-scrapers` layout and Perplexity is responsible for the initial research and handoff.

## Files To Read First

1. `README.md`
2. `START_HERE.md`
3. `workflow/NEW_SCRAPER_CHECKLIST.md`
4. `scrapers/<site-folder>/SCRAPER_SPEC.json` if the folder already exists

## Repo Helpers

- `workflow/PERPLEXITY_RESEARCH_INPUT.md` is the first step when the site has not been researched yet.
- `scripts/create_scraper_from_template.sh <site-folder>` copies the template folder unchanged.
- `scripts/create_scraper_from_spec.py <path-to-SCRAPER_SPEC.json>` copies the template, renames the scraper files, and writes Perplexity's researched spec into the new folder.
- `python3 scripts/validate_scraper_repo.py` checks that each scraper folder contains the required files.

## Required Scraper Folder Contents

- The scraper `.yml`
- The backing Python script
- `README.md`
- `SCRAPER_SPEC.json`
- `PERPLEXITY_TO_CODEX_HANDOFF.md`
- `CODEX_PROMPT.md`
- `TODO.md`

## Naming Rules

- Keep scraper folders under `scrapers/<site-folder>/`
- Keep `folder_name` lowercase and URL-safe
- Derive the script stem from `site_name` when using `create_scraper_from_spec.py`

## Research Contract

Treat `SCRAPER_SPEC.json` as the source of truth for:

- Supported Stash hook modes
- URL patterns
- Metadata mapping
- Parsing notes
- Known limitations
- Validation examples
- Source links

Treat `PERPLEXITY_TO_CODEX_HANDOFF.md` as the narrative handoff that explains how to interpret that structured research during implementation.
