#!/usr/bin/env python3

import json
import re
import ssl
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from html import unescape
from urllib.error import URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


BASE_URL = "https://www.icegaytube.tv"
STUDIO = "IceGayTube"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) "
    "Gecko/20100101 Firefox/115.0"
)
COOKIES = "age_verified=1"

SSL_CONTEXT = None
try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CONTEXT = ssl.create_default_context()


def read_stdin():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def fetch(url):
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Cookie": COOKIES,
        },
    )
    try:
        with urlopen(req, timeout=30, context=SSL_CONTEXT) as response:
            return response.read().decode("utf-8", errors="replace")
    except URLError:
        result = subprocess.run(
            [
                "curl",
                "-L",
                "--silent",
                "--fail",
                "-A",
                USER_AGENT,
                "-H",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H",
                "Accept-Language: en-US,en;q=0.5",
                "-H",
                f"Cookie: {COOKIES}",
                url,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout


def normalize_space(value):
    return re.sub(r"\s+", " ", value or "").strip()


def strip_html(value):
    return normalize_space(unescape(re.sub(r"<[^>]+>", " ", value or "")))


def normalize_title(value):
    value = unescape(value or "").lower()
    value = re.sub(r"\.[a-z0-9]{2,5}$", "", value)
    value = re.sub(r"[_./-]+", " ", value)
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return normalize_space(value)


def similarity(a, b):
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def meta_content(html, key, *, attr="property"):
    pattern = rf'<meta[^>]+{attr}=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)'
    match = re.search(pattern, html, flags=re.IGNORECASE)
    return normalize_space(unescape(match.group(1))) if match else ""


def parse_iso_date(value):
    if not value:
        return ""
    value = normalize_space(value)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value.split("T", 1)[0]


def parse_relative_date(value):
    value = normalize_space(value).lower()
    if not value:
        return ""
    today = datetime.now(timezone.utc).date()
    if value == "today":
        return today.isoformat()
    if value == "yesterday":
        return (today - timedelta(days=1)).isoformat()

    match = re.match(r"(\d+)\s+(day|week|month|year)s?\s+ago", value)
    if not match:
        return ""

    amount = int(match.group(1))
    unit = match.group(2)
    if unit == "day":
        delta = timedelta(days=amount)
    elif unit == "week":
        delta = timedelta(weeks=amount)
    elif unit == "month":
        delta = timedelta(days=amount * 30)
    else:
        delta = timedelta(days=amount * 365)
    return (today - delta).isoformat()


def parse_date(html):
    for candidate in (
        meta_content(html, "article:published_time"),
        meta_content(html, "date", attr="name"),
    ):
        parsed = parse_iso_date(candidate)
        if parsed:
            return parsed

    match = re.search(
        r'<span class="b-info__title"><i class="icon-calendar"></i>Date added:</span>\s*'
        r'<span class="b-info__text">(.*?)</span>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""

    text = strip_html(match.group(1))
    parsed = parse_relative_date(text)
    if parsed:
        return parsed

    absolute = re.search(r"([A-Z][a-z]{2,9}\s+\d{1,2},\s+\d{4})", text)
    if absolute:
        for fmt in ("%B %d, %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(absolute.group(1), fmt).date().isoformat()
            except ValueError:
                continue
    return ""


def unique_names(values):
    seen = set()
    output = []
    for value in values:
        name = normalize_space(unescape(value))
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        output.append({"name": name})
    return output


def clean_scene_title(value):
    value = normalize_space(unescape(value))
    value = re.sub(r"\s+at Ice Gay Tube\s*$", "", value, flags=re.IGNORECASE)
    return normalize_space(value)


def extract_scene_title(html):
    title = meta_content(html, "og:title")
    if title:
        return clean_scene_title(title)

    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if title_match:
        return clean_scene_title(strip_html(title_match.group(1)))
    return ""


def extract_scene_image(html):
    for candidate in (
        meta_content(html, "og:image"),
        meta_content(html, "twitter:image", attr="name"),
    ):
        if candidate:
            return candidate

    for pattern in (
        r'poster="([^"]+)"',
        r'data-gallery-img="([^"]+)"',
        r'<source type="image/jpeg" srcset="([^"]+)"',
    ):
        match = re.search(pattern, html, flags=re.IGNORECASE)
        if match:
            return normalize_space(match.group(1))
    return ""


def extract_scene_details(html):
    for candidate in (
        meta_content(html, "og:description"),
        meta_content(html, "description", attr="name"),
    ):
        cleaned = clean_scene_title(candidate)
        if cleaned:
            return cleaned
    return ""


def extract_scene_tags(html):
    matches = re.findall(
        r'<a href="/(?:category|search)/[^"]+" class="b-info__cat-link">(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return unique_names(strip_html(match) for match in matches)


def extract_scene_performers(html):
    matches = re.findall(
        r'<a href="/pornstar[s]?/[^"]+" class="b-info__cat-link">(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    performers = unique_names(strip_html(match) for match in matches)
    if performers:
        title = extract_scene_title(html)
        title_match = re.search(r"\s-\s(.+)$", title)
        if title_match:
            inferred = []
            for part in re.split(r"\s*&\s*|\s+and\s+", title_match.group(1), flags=re.IGNORECASE):
                cleaned = normalize_space(part)
                if cleaned:
                    inferred.append(cleaned)
            combined = unique_names([item["name"] for item in performers] + inferred)
            if combined:
                return combined
        return performers

    title = extract_scene_title(html)
    title_match = re.search(r"\s-\s(.+)$", title)
    if not title_match:
        return []
    inferred = []
    for part in re.split(r"\s*&\s*|\s+and\s+", title_match.group(1), flags=re.IGNORECASE):
        cleaned = normalize_space(part)
        if cleaned:
            inferred.append(cleaned)
    return unique_names(inferred)


def scrape_scene(url):
    if not url:
        return {}

    try:
        html = fetch(url)
    except Exception:
        return {}

    scene = {
        "title": extract_scene_title(html),
        "url": url,
        "date": parse_date(html),
        "details": extract_scene_details(html),
        "image": extract_scene_image(html),
        "performers": extract_scene_performers(html),
        "tags": extract_scene_tags(html),
        "studio": {"name": STUDIO},
    }
    return {key: value for key, value in scene.items() if value}


def parse_search_results(html):
    pattern = re.compile(
        r'href="(/movies/\d+/[^"]+)"[^>]*title="([^"]+)"',
        flags=re.IGNORECASE,
    )
    results = []
    seen = set()
    for path, title in pattern.findall(html):
        url = f"{BASE_URL}{path}"
        if url in seen:
            continue
        seen.add(url)
        clean_title = normalize_space(unescape(title))
        if not clean_title:
            continue
        results.append({"title": clean_title, "url": url})
    return results


def search_scenes(query):
    query = normalize_space(query)
    if not query:
        return []

    url = f"{BASE_URL}/search/{quote_plus(query).replace('+', '-')}"
    try:
        html = fetch(url)
    except Exception:
        return []

    results = parse_search_results(html)
    results.sort(
        key=lambda item: (
            normalize_title(item["title"]) != normalize_title(query),
            -similarity(item["title"], query),
            item["title"],
        )
    )
    return results


def scrape_performer(url):
    if not url:
        return {}

    try:
        html = fetch(url)
    except Exception:
        html = ""

    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    name = ""
    if title_match:
        name = strip_html(title_match.group(1))
        name = re.sub(r"\s+at Ice Gay Tube\s*$", "", name, flags=re.IGNORECASE)

    if not name:
        slug_match = re.search(r"/pornstar[s]?/([^/]+)/?$", url)
        if slug_match:
            name = " ".join(part.capitalize() for part in slug_match.group(1).split("-") if part)

    performer = {
        "name": normalize_space(name),
        "url": url,
        "gender": "Male",
        "image": meta_content(html, "og:image"),
        "details": meta_content(html, "description", attr="name"),
    }
    return {key: value for key, value in performer.items() if value}


def main():
    if len(sys.argv) < 2:
        print("{}")
        return

    mode = sys.argv[1]
    data = read_stdin()

    if mode == "sceneByURL":
        result = scrape_scene(data.get("url", ""))
    elif mode == "sceneByName":
        result = search_scenes(data.get("name", ""))
    elif mode == "performerByURL":
        result = scrape_performer(data.get("url", ""))
    else:
        result = {}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
