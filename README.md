# My Scrapers

This repo groups Stash scrapers by site, with one folder per scraper.

## Start Here

If you are creating a new scraper, use these files in order:

1. `START_HERE.md`
2. `workflow/PERPLEXITY_RESEARCH_INPUT.md`
3. `workflow/PERPLEXITY_TO_CODEX_HANDOFF.md`
4. `workflow/NEW_SCRAPER_CHECKLIST.md`

If you want Codex to build directly without a separate research pass, use:

- `workflow/CODEX_PROMPT.md`

## Layout

Each scraper lives in:

- `scrapers/<site-folder>/`

Each scraper folder should contain:

- the Stash scraper `.yml`
- the backing Python script
- a short `README.md`

Current scrapers:

- `scrapers/justthegays-tv`
- `scrapers/justthegays-com`

## Workflow

### Recommended Flow

1. Run the Perplexity research brief in `workflow/PERPLEXITY_RESEARCH_INPUT.md`.
2. Paste that output into `workflow/PERPLEXITY_TO_CODEX_HANDOFF.md`.
3. Ask Codex to build the scraper in this repo.
4. Validate and publish with `workflow/NEW_SCRAPER_CHECKLIST.md`.

### Direct Codex Flow

1. Use `workflow/CODEX_PROMPT.md`.
2. Point Codex at this repo.
3. Have it create the scraper from `templates/site-template/`.

## Add a New Scraper Manually

1. Copy `templates/site-template/`.
2. Rename the folder to `scrapers/<site-folder>/`.
3. Rename the template files for the target site.
4. Implement the scraper logic.
5. Test against live scene and performer pages when possible.
6. Update this README with the new scraper folder.

## Stash Install

For any scraper in this repo:

1. Copy that scraper's `.yml` and script file into your Stash `scrapers` directory.
2. Reload scrapers in Stash or restart the app.

## Conventions

- One site per scraper.
- Prefer Python-backed script scrapers.
- Keep folder names short and URL-safe.
- Document supported scrape modes in each scraper README.
- Preserve existing scraper behavior when adding new ones.

## Workflow Files

- `START_HERE.md`: one-page overview of the whole process
- `workflow/PERPLEXITY_RESEARCH_INPUT.md`: research brief for Perplexity
- `workflow/PERPLEXITY_TO_CODEX_HANDOFF.md`: handoff prompt from research to Codex
- `workflow/CODEX_PROMPT.md`: direct Codex build prompt
- `workflow/NEW_SCRAPER_CHECKLIST.md`: QA and publish checklist
