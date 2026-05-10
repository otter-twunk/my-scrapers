#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "site-template"
SCRAPERS_DIR = ROOT / "scrapers"
REQUIRED_KEYS = {"site_name", "site_url", "folder_name"}


def load_spec(spec_path: Path) -> dict:
    with spec_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("SCRAPER_SPEC.json must contain a JSON object")
    missing = sorted(REQUIRED_KEYS - set(data.keys()))
    if missing:
        raise ValueError(f"SCRAPER_SPEC.json is missing required keys: {', '.join(missing)}")
    return data


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug


def to_pascal_case(value: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", value)
    if not parts:
        raise ValueError("Unable to derive scraper script name from site name")
    return "".join(part[:1].upper() + part[1:] for part in parts)


def replace_tokens(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def scaffold_scraper(spec_path: Path) -> Path:
    spec = load_spec(spec_path)
    folder_name = spec["folder_name"].strip()
    if folder_name != slugify(folder_name):
        raise ValueError("folder_name must already be lowercase and URL-safe")

    site_name = spec["site_name"].strip()
    site_url = spec["site_url"].strip()
    script_stem = to_pascal_case(site_name)

    target_dir = SCRAPERS_DIR / folder_name
    if target_dir.exists():
        raise FileExistsError(f"Target already exists: {target_dir}")

    shutil.copytree(TEMPLATE_DIR, target_dir)

    original_py = target_dir / "SiteScraper.py"
    original_yml = target_dir / "SiteScraper.yml"
    scraper_py = target_dir / f"{script_stem}.py"
    scraper_yml = target_dir / f"{script_stem}.yml"
    original_py.rename(scraper_py)
    original_yml.rename(scraper_yml)

    replacements = {
        "Site Name": site_name,
        "SITE_URL": site_url,
        "<site-folder>": folder_name,
        "SiteScraper": script_stem,
    }

    for text_file in [
        target_dir / "README.md",
        target_dir / "CODEX_PROMPT.md",
        target_dir / "PERPLEXITY_TO_CODEX_HANDOFF.md",
        target_dir / "TODO.md",
        target_dir / "SCRAPER_SPEC.json",
        scraper_py,
        scraper_yml,
    ]:
        replace_tokens(text_file, replacements)

    (target_dir / "SCRAPER_SPEC.json").write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return target_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new scraper folder from a completed SCRAPER_SPEC.json.",
    )
    parser.add_argument("spec_path", help="Path to SCRAPER_SPEC.json")
    args = parser.parse_args()

    spec_path = Path(args.spec_path).resolve()
    if not spec_path.exists():
        print(f"Spec not found: {spec_path}", file=sys.stderr)
        return 1

    try:
        target_dir = scaffold_scraper(spec_path)
    except (ValueError, FileExistsError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Created {target_dir}")
    print("Next steps:")
    print("1. Review the generated README, handoff files, and TODO list")
    print("2. Implement site-specific parsing in the Python scraper")
    print("3. Validate with python3 scripts/validate_scraper_repo.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
