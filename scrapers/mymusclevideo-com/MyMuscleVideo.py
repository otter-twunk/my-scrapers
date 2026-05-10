#!/usr/bin/env python3

import json
import re
import ssl
import subprocess
import sys
from datetime import datetime
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


BASE_URL = "https://mymusclevideo.com"
STUDIO = "MyMuscleVideo"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) "
    "Gecko/20100101 Firefox/115.0"
)

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
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.5",
        },
    )
    try:
        with urlopen(req, timeout=30, context=SSL_CONTEXT) as response:
            return response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code == 404:
            return ""
        raise
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
                "Accept: text/html,application/xhtml+xml",
                "-H",
                "Accept-Language: en-US,en;q=0.5",
                url,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return ""
        return result.stdout


def normalize_space(value):
    return re.sub(r"\s+", " ", value or "").strip()


def clean_text(value):
    return normalize_space(unescape(value or ""))


def unique_names(values):
    seen = set()
    output = []
    for value in values:
        name = clean_text(value)
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        output.append({"name": name})
    return output


def normalize_title(value):
    value = unescape(value or "").lower()
    value = re.sub(r"\.[a-z0-9]{2,5}$", "", value)
    value = re.sub(r"[_./-]+", " ", value)
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return normalize_space(value)


def similarity(a, b):
    a_norm = normalize_title(a)
    b_norm = normalize_title(b)
    if not a_norm or not b_norm:
        return 0.0
    if a_norm == b_norm:
        return 1.0
    a_words = set(a_norm.split())
    b_words = set(b_norm.split())
    overlap = len(a_words & b_words)
    return (2.0 * overlap) / (len(a_words) + len(b_words))


def absolute_url(value):
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("//"):
        return "https:" + value
    if value.startswith("/"):
        return BASE_URL + value
    return value


def extract_meta(html, attr, key):
    patterns = [
        rf'<meta[^>]+{attr}=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+{attr}=["\']{re.escape(key)}["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.IGNORECASE)
        if match:
            return clean_text(match.group(1))
    return ""


def extract_title_from_html(html):
    title = extract_meta(html, "property", "og:title")
    if title:
        return title

    match = re.search(
        r'<div[^>]+id=["\']video["\'][^>]*>.*?<h1>(.*?)</h1>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return clean_text(re.sub(r"<[^>]+>", " ", match.group(1)))
    return ""


def extract_date(html):
    value = extract_meta(html, "property", "og:video:release_date")
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value.split("T", 1)[0]


def extract_tags(html):
    tag_links = re.findall(
        r'<a[^>]+href=["\']/video/tag/[^"\']+["\'][^>]*>(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    tags = [
        clean_text(re.sub(r"<[^>]+>", " ", value))
        for value in tag_links
        if clean_text(re.sub(r"<[^>]+>", " ", value))
    ]
    if tags:
        return unique_names(tags)

    meta_tags = re.findall(
        r'<meta[^>]+property=["\']video:tag["\'][^>]+content=["\']([^"\']+)',
        html,
        flags=re.IGNORECASE,
    )
    if meta_tags:
        return unique_names(meta_tags)

    keywords = extract_meta(html, "name", "keywords")
    if keywords:
        return unique_names(part.strip() for part in keywords.split(","))
    return []


def normalize_scene_url(url):
    url = (url or "").strip()
    if not url:
        return ""
    url = re.sub(r"^https?://www\.mymusclevideo\.com", BASE_URL, url, flags=re.IGNORECASE)
    if re.match(r"^https?://", url, flags=re.IGNORECASE):
        return url
    if url.startswith("/"):
        return BASE_URL + url
    return BASE_URL + "/" + url.lstrip("/")


def scrape_scene(url):
    url = normalize_scene_url(url)
    if not url:
        return {}

    html = fetch(url)
    if not html:
        return {}

    scene = {
        "title": extract_title_from_html(html),
        "url": url,
        "date": extract_date(html),
        "details": extract_meta(html, "property", "og:description")
        or extract_meta(html, "name", "description"),
        "image": absolute_url(extract_meta(html, "property", "og:image")),
        "tags": extract_tags(html),
        "performers": [],
        "studio": {"name": STUDIO},
    }
    return {key: value for key, value in scene.items() if value not in ("", [], None)}


def parse_search_results(html):
    pattern = re.compile(
        r'<li[^>]+id=["\']video-(\d+)["\'][^>]*class=["\'][^"\']*\bvideo\b[^"\']*["\'][^>]*>.*?'
        r'<a[^>]+href=["\']/(?:\d+)/([^"\']+)/["\'][^>]+title=["\']([^"\']+)["\'][^>]*class=["\']image["\'][^>]*>.*?'
        r'<img[^>]+src=["\']([^"\']+)',
        flags=re.IGNORECASE | re.DOTALL,
    )

    results = []
    seen_ids = set()
    for video_id, slug, title, image in pattern.findall(html):
        if video_id in seen_ids:
            continue
        seen_ids.add(video_id)
        results.append(
            {
                "title": clean_text(title) or clean_text(slug.replace("-", " ")),
                "url": f"{BASE_URL}/{video_id}/{slug}/",
                "image": absolute_url(image),
            }
        )
    return results


def search_scenes(query):
    query = normalize_space(query)
    if not query:
        return []

    html = fetch(f"{BASE_URL}/search/video/?s={quote_plus(query)}")
    if not html:
        return []

    results = parse_search_results(html)
    results.sort(
        key=lambda item: (
            normalize_title(item["title"]) != normalize_title(query),
            -similarity(item["title"], query),
            item["title"].casefold(),
        )
    )
    return results


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
    else:
        result = {}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
