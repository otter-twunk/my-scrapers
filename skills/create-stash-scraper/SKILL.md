---
name: create-stash-scraper
description: Build or scaffold a Stash scraper from repo-local research files. Use when Codex is working in the `my-scrapers` repo or a repo with the same layout and needs to: turn a completed `SCRAPER_SPEC.json` into a new scraper folder, implement a site-specific Python-backed Stash scraper, update folder-local handoff files, or validate that a scraper matches the repo workflow.
---

# Create Stash Scraper

## Overview

Use this skill to convert Perplexity-prepared repo research into a working scraper with the least possible re-discovery. Treat Perplexity as the initiator of site research, folder naming, and handoff structure; treat Codex as the implementer and finisher after that handoff exists.

## Workflow

1. Read `README.md`, `START_HERE.md`, and `workflow/NEW_SCRAPER_CHECKLIST.md`.
2. Confirm whether Perplexity has already produced the site research and handoff files:
   - `SCRAPER_SPEC.json`
   - `PERPLEXITY_TO_CODEX_HANDOFF.md`
   - `CODEX_PROMPT.md`
3. If that handoff already exists, read `scrapers/<site-folder>/SCRAPER_SPEC.json` first.
4. If research exists as a completed `SCRAPER_SPEC.json` outside `scrapers/`, run `python3 scripts/create_scraper_from_spec.py <path-to-SCRAPER_SPEC.json>` to materialize Perplexity's structure in the repo.
5. If Perplexity has not run yet, stop and use `workflow/PERPLEXITY_RESEARCH_INPUT.md` to initiate the research pass before implementing.
6. Implement the scraper in the generated folder:
   - keep one site per folder
   - prefer a Python-backed script scraper
   - handle missing metadata gracefully
   - preserve existing scrapers
7. Validate with `python3 scripts/validate_scraper_repo.py`.

## Implementation Rules

- Use `SCRAPER_SPEC.json` as the source of truth for supported hooks, URL patterns, metadata mapping, parsing notes, and known limitations.
- Preserve Perplexity's folder-local handoff files as the research record, updating them only when implementation findings materially change the contract.
- Keep the scraper `.yml`, Python script, `README.md`, and workflow files in the same folder.
- Support only realistic hook modes. Do not stub unsupported modes into the final scraper unless the repo convention requires a documented placeholder.
- Update the root `README.md` when adding a new scraper folder.
- Document site-specific limitations in both `README.md` and `SCRAPER_SPEC.json` when they affect scrape quality.

## Repo-Specific Notes

Read [references/repo-workflow.md](references/repo-workflow.md) when you need the exact folder contract, helper commands, or naming rules for this repo.
