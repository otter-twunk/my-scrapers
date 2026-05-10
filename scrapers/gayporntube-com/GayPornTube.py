#!/usr/bin/env python3

import json
import re
import ssl
import subprocess
import sys
from datetime import datetime
from difflib import SequenceMatcher
from html import unescape
from urllib.error import URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


BASE_URL = "https://www.gayporntube.com"
SEARCH_URL = f"{BASE_URL}/search/videos/?q={{query}}"
STUDIO = "GayPornTube"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) "
    "Gecko/20100101 Firefox/115.0"
)
COOKIE = "age_verified=1"
SCENE_URL_RE = re.compile(r"^https?://(?:www\.)?gayporntube\.com/video/\d+/[^/?#]+/?$", re.IGNORECASE)

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
            "Cookie": COOKIE,
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
                f"Cookie: {COOKIE}",
                url,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout


def normalize_space(value):
    return re.sub(r"\s+", " ", value or "").strip()


def clean_text(value):
    return normalize_space(unescape(value or ""))


def strip_html(value):
    return clean_text(re.sub(r"<[^>]+>", " ", value or ""))


def normalize_title(value):
    value = unescape(value or "").lower()
    value = re.sub(r"\.[a-z0-9]{2,5}$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^\d+\s*[-_. ]\s*", "", value)
    value = re.sub(r"[_./-]+", " ", value)
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return normalize_space(value)


def normalize_fragment_text(value):
    value = unescape(value or "")
    value = re.sub(r"\.[a-z0-9]{2,5}$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^\d+\s*[-_. ]\s*", "", value)
    value = re.sub(r"[_./-]+", " ", value)
    return normalize_space(value)


def title_tokens(value):
    return [token for token in normalize_title(value).split() if token]


def similarity(a, b):
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def parse_date(value):
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value.split("T", 1)[0]


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


def extract_meta(html, attr, key):
    if attr == "property":
        pattern = rf'<meta[^>]+property=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)'
    else:
        pattern = rf'<meta[^>]+name=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)'
    match = re.search(pattern, html, flags=re.IGNORECASE)
    return clean_text(match.group(1)) if match else ""


def load_json_ld_blocks(html):
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>\s*(.*?)\s*</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    parsed = []
    for block in blocks:
        text = unescape(block).strip()
        if not text:
            continue
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(value, list):
            parsed.extend(item for item in value if isinstance(item, dict))
        elif isinstance(value, dict):
            parsed.append(value)
    return parsed


def find_json_ld(blocks, wanted_type):
    for block in blocks:
        block_type = block.get("@type")
        if block_type == wanted_type:
            return block
        if isinstance(block_type, list) and wanted_type in block_type:
            return block
    return {}


def extract_h1_title(html):
    match = re.search(r'<h1[^>]*class=["\'][^"\']*\btitle\b[^"\']*["\'][^>]*>(.*?)</h1>', html, flags=re.IGNORECASE | re.DOTALL)
    return strip_html(match.group(1)) if match else ""


def clean_details(value):
    text = clean_text(value)
    if not text:
        return ""
    if not any(char.isalnum() for char in text):
        return ""
    return text


def extract_section_names(html, class_name):
    pattern = re.compile(
        rf'<div[^>]+class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'][^>]*>(.*?)</div>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        return []
    section_html = match.group(1)
    return [
        clean_text(text)
        for text in re.findall(r"<a\b[^>]*>(.*?)</a>", section_html, flags=re.IGNORECASE | re.DOTALL)
        if clean_text(text)
    ]


def scrape_scene(url):
    if not url:
        return {}

    try:
        html = fetch(url)
    except Exception:
        return {}

    blocks = load_json_ld_blocks(html)
    video = find_json_ld(blocks, "VideoObject")

    image = ""
    thumbnail = video.get("thumbnailUrl", "") if video else ""
    if isinstance(thumbnail, list):
        image = thumbnail[0] if thumbnail else ""
    elif isinstance(thumbnail, str):
        image = thumbnail

    title = clean_text(video.get("name", "")) if video else ""
    if not title:
        title = extract_meta(html, "property", "og:title")
    if not title:
        title = extract_h1_title(html)

    tags = unique_names(
        extract_section_names(html, "video-info-tags")
        + extract_section_names(html, "video-info-categories")
    )

    scene = {
        "title": title,
        "url": url,
        "date": parse_date(video.get("uploadDate", "")) if video else "",
        "details": clean_details(video.get("description", "")) if video else "",
        "image": image or extract_meta(html, "property", "og:image"),
        "performers": [],
        "tags": tags,
        "studio": {"name": STUDIO},
    }
    return {key: value for key, value in scene.items() if value not in ("", [], None)}


def parse_search_results(html):
    image_map = {}
    for href, title_attr, image in re.findall(
        r'<a[^>]+class=["\'][^"\']*\bimage\b[^"\']*["\'][^>]+href=["\'](https://www\.gayporntube\.com/video/\d+/[^"\']+)["\'][^>]*title=["\']([^"\']*)["\'][^>]*>.*?<img[^>]+(?:data-src|src)=["\']([^"\']+)["\']',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        image_map[href] = {
            "title": clean_text(title_attr),
            "image": image.strip(),
        }

    seen = set()
    results = []
    for href, inner_html in re.findall(
        r'<a[^>]+href=["\'](https://www\.gayporntube\.com/video/\d+/[^"\']+)["\'][^>]*class=["\'][^"\']*\btitle\b[^"\']*["\'][^>]*>(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        if href in seen:
            continue
        seen.add(href)
        title = strip_html(inner_html) or image_map.get(href, {}).get("title", "")
        if not title:
            continue
        results.append(
            {
                "title": title,
                "url": href,
                "image": image_map.get(href, {}).get("image", ""),
                "details": "",
                "date": "",
            }
        )
    return results


def search_scenes(query):
    query = normalize_space(query)
    if not query:
        return []

    try:
        html = fetch(SEARCH_URL.format(query=quote_plus(query)))
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


def best_scene_match(query):
    results = search_scenes(query)
    if not results:
        return {}
    best = results[0]
    query_norm = normalize_title(query)
    title_norm = normalize_title(best["title"])
    if title_norm == query_norm:
        return scrape_scene(best["url"])

    query_parts = title_tokens(query)
    title_parts = set(title_tokens(best["title"]))
    if not query_parts:
        return {}
    if not all(part in title_parts for part in query_parts):
        return {}
    if similarity(best["title"], query) < 0.8:
        return {}
    return scrape_scene(best["url"])


def extract_fragment_query(fragment):
    if isinstance(fragment, dict):
        direct = fragment.get("title") or fragment.get("name") or fragment.get("code")
        if direct:
            return normalize_fragment_text(direct)

        url = fragment.get("url", "")
        if SCENE_URL_RE.match(url):
            return url

        for file_info in fragment.get("files", []):
            basename = file_info.get("basename") or file_info.get("path") or ""
            if basename:
                return normalize_fragment_text(basename)
    elif isinstance(fragment, str):
        if SCENE_URL_RE.match(fragment):
            return fragment
        return normalize_fragment_text(fragment)
    return ""


def handle_scene_by_fragment(fragment):
    query = extract_fragment_query(fragment)
    if not query:
        return {}
    if SCENE_URL_RE.match(query):
        return scrape_scene(query)
    return best_scene_match(query)


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
    elif mode in {"sceneByQueryFragment", "sceneByFragment"}:
        result = handle_scene_by_fragment(data)
    else:
        result = {}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
