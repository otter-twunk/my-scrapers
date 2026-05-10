# Perplexity → Codex Handoff: MyMuscleVideo

Create a working Stash scraper for **https://mymusclevideo.com/** in this repository.

## Repository

- Repo: `otter-twunk/my-scrapers`
- Structure: one scraper per folder under `scrapers/<site-folder>/`
- Target folder: `scrapers/mymusclevideo-com/`

## Your Job

- Read this research and use it as implementation guidance
- Create the scraper in `scrapers/mymusclevideo-com/`
- Include:
  - `MyMuscleVideo.yml`
  - `MyMuscleVideo.py`
  - `README.md`
  - Keep `SCRAPER_SPEC.json` as the machine-friendly research contract
  - Keep `PERPLEXITY_TO_CODEX_HANDOFF.md` in the folder as the research record
  - Update `CODEX_PROMPT.md` if implementation details change
  - Update `TODO.md` as tasks are completed
- Follow official Stash scraper conventions
- Preserve existing scrapers and repo structure
- Update the root `README.md` with the new scraper folder

## Implementation Requirements

- Python script scraper
- Support `sceneByURL` and `sceneByName`
- Do NOT implement `performerByURL`, `sceneByFragment`, `sceneByQueryFragment`
- Scope to this single site only
- Handle missing metadata gracefully (return empty string / empty list)
- No unnecessary dependencies beyond stdlib and certifi

## Validation Requirements

- Test `sceneByURL`:
  - `https://mymusclevideo.com/107027/sexy-guy-muscle/`
  - `https://mymusclevideo.com/115276/adam-riich/`
- Test `sceneByName` with `"muscle worship"` and `"adam riich"`
- Report known limitations in `README.md` and `TODO.md`

## Use These Repo Helpers

- Start from `templates/site-template/`
- Follow `workflow/NEW_SCRAPER_CHECKLIST.md`
- Use `SCRAPER_SPEC.json` first when specific implementation details are needed

---

## Research Summary

### Platform

Custom tube site. No Cloudflare. No JSON-LD. No WordPress. All metadata is in **Open Graph `<meta>` tags** and the **HTML DOM** of the scene page. No authentication required for scene pages or search.

### Scene URL Pattern

```
https://mymusclevideo.com/{video_id}/{slug}/
https://www.mymusclevideo.com/{video_id}/{slug}/
```

Examples:
- `https://mymusclevideo.com/107027/sexy-guy-muscle/`
- `https://mymusclevideo.com/115276/adam-riich/`

### Supported Stash Hook Modes

| Mode | Supported | Notes |
|---|---|---|
| `sceneByURL` | ✅ Yes | Fetch scene page, parse OG + HTML |
| `sceneByName` | ✅ Yes | Search URL works without auth or CF |
| `sceneByFragment` | ❌ No | No reliable URL reconstruction |
| `sceneByQueryFragment` | ❌ No | Same as above |
| `performerByURL` | ❌ No | Model pages are login-gated |

### Metadata Field Mapping

| Field | Source | Notes |
|---|---|---|
| `title` | `og:title` meta | Clean title, no site suffix |
| `date` | `og:video:release_date` meta | ISO-8601, strip to YYYY-MM-DD |
| `details` | `og:description` meta | Free-text description |
| `image` | `og:image` meta | 300×226 JPG thumbnail |
| `tags` | `<a href="/video/tag/{tag}/">` anchor text | Plus `meta name="keywords"` fallback |
| `studio` | Constant `"MyMuscleVideo"` | |
| `performers` | **Not available** | Uploader is a community user |

### Selectors / Parsing Strategy

```python
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import re, json, sys, ssl
from urllib.parse import quote_plus

BASE_URL = "https://mymusclevideo.com"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"

def fetch(url):
    req = Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.5",
    })
    ctx = ssl.create_default_context()
    with urlopen(req, timeout=30, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")

def parse_scene(html, url):
    # Open Graph helpers
    def og(prop):
        m = re.search(r'<meta[^>]+property=["\']' + re.escape(prop) + r'["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']' + re.escape(prop) + r'["\']', html)
        return m.group(1).strip() if m else ""

    title = og("og:title")
    date_raw = og("og:video:release_date")  # '2020-11-20T22:59:54+00:00'
    date = date_raw.split("T")[0] if date_raw else ""
    details = og("og:description")
    image = og("og:image")

    # Tags from /video/tag/ links
    tags = re.findall(r'<a[^>]+href=["\']/video/tag/[^"\']+["\'][^>]*>([^<]+)</a>', html)
    tags = [t.strip() for t in tags if t.strip()]

    # Fallback: meta keywords
    if not tags:
        kw_m = re.search(r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^"\']+)["\']', html)
        if kw_m:
            tags = [t.strip() for t in kw_m.group(1).split(",") if t.strip()]

    return {
        "title": title,
        "date": date,
        "details": details,
        "image": image,
        "studio": {"name": "MyMuscleVideo"},
        "tags": [{"name": t} for t in tags],
        "performers": [],
    }

def search_scenes(query):
    url = f"{BASE_URL}/search/video/?s={quote_plus(query)}"
    html = fetch(url)
    pairs = re.findall(r'href="/(\d+)/([^"]+)/"', html)
    seen = set()
    results = []
    for vid_id, slug in pairs:
        if vid_id not in seen:
            seen.add(vid_id)
            results.append({
                "title": slug.replace("-", " ").title(),
                "url": f"{BASE_URL}/{vid_id}/{slug}/",
            })
    return results
```

### Known Limitations

1. **No performer data** — scene pages show an uploader account, not a named performer. `performers` is always empty.
2. **Low-resolution cover** — `og:image` is 300×226px. No full-res public alternative.
3. **Date in visible HTML is relative** — always use `og:video:release_date`.
4. **Model pages are login-gated** — `performerByURL` is not implementable.
5. **Search title is slug-derived** — use slug as placeholder; caller can scrape full URL for real title.
