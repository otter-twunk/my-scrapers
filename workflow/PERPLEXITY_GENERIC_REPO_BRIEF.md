# Perplexity Generic Repo Brief

Give this repo brief to Perplexity along with `workflow/PERPLEXITY_RESEARCH_INPUT.md`.

The goal is for Perplexity to not only research the site, but also prepare a scraper folder that is ready for Codex.

## Repo Rules

- Repo name: `otter-twunk/my-scrapers`
- One scraper per folder under `scrapers/<site-folder>/`
- Folder names must be short, URL-safe, and site-specific
- Prefer Python-backed Stash script scrapers
- Keep one site per scraper

## Required Folder Files

Each scraper folder should contain:

- the scraper `.yml`
- the scraper Python script
- `README.md`
- `SCRAPER_SPEC.json`
- `PERPLEXITY_TO_CODEX_HANDOFF.md`
- `CODEX_PROMPT.md`
- `TODO.md`

## Perplexity's Job

Perplexity should:

1. Research the site and Stash requirements
2. Choose the best scraper folder name
3. Structure the folder according to repo conventions
4. Draft the file contents needed for Codex handoff
5. Leave the scraper folder ready for Codex to begin implementation with a simple prompt

## Codex Handoff Goal

The Codex start should be as simple as:

```text
Use the files in `scrapers/<site-folder>/` and build the scraper.
```
