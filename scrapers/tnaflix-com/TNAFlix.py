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
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://www.tnaflix.com"
SEARCH_URL = f"{BASE_URL}/search?what={{query}}"
STUDIO = "TNAFlix"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) "
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


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False))


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
    value = re.sub(r"\.[a-z0-9]{2,5}$", "", value)
    value = re.sub(r"^\d+\s*[-_. ]\s*", "", value)
    value = re.sub(r"[_./-]+", " ", value)
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return normalize_space(value)


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


def clean_details(value):
    text = strip_html(value)
    if text.casefold() == "no description provided":
        return ""
    return text


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


def expand_json_ld_node(node):
    if isinstance(node, list):
        expanded = []
        for item in node:
            expanded.extend(expand_json_ld_node(item))
        return expanded
    if not isinstance(node, dict):
        return []
    expanded = [node]
    graph = node.get("@graph")
    if isinstance(graph, list):
        for item in graph:
            expanded.extend(expand_json_ld_node(item))
    return expanded


def find_json_ld(blocks, wanted_type):
    for block in blocks:
        for item in expand_json_ld_node(block):
            item_type = item.get("@type")
            if item_type == wanted_type:
                return item
            if isinstance(item_type, list) and wanted_type in item_type:
                return item
    return {}


def meta_content(html, key, *, attr="property"):
    pattern = rf'<meta[^>]+{attr}=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)'
    match = re.search(pattern, html, flags=re.IGNORECASE)
    return clean_text(match.group(1)) if match else ""


def extract_scene_image(video_json, html):
    image = video_json.get("thumbnailUrl", "")
    if isinstance(image, list):
        image = image[0] if image else ""
    image = clean_text(image)
    if image:
        return image
    return meta_content(html, "og:image")


def extract_scene_performers(html):
    matches = re.findall(
        r'<a[^>]+class="([^"]*\bbadge-kiss\b[^"]*)"[^>]+href="(https://www\.tnaflix\.com/profile/[^"]+|/profile/[^"]+)"[^>]*>(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    names = []
    for classes, _href, text in matches:
        if re.search(r"\bbadge-unverified\b", classes, flags=re.IGNORECASE):
            continue
        name = strip_html(text)
        if name:
            names.append(name)
    return unique_names(names)


def category_tag_from_url(url):
    try:
        path = urlparse(url).path
    except Exception:
        return []
    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        return []
    slug = parts[0]
    tag = normalize_space(slug.replace("-", " ").title())
    return [{"name": tag}] if tag else []


def scrape_scene(url):
    if not url:
        return {}

    try:
        html = fetch(url)
    except Exception:
        return {}

    blocks = load_json_ld_blocks(html)
    video = find_json_ld(blocks, "VideoObject")

    title = clean_text(video.get("name", "")) or meta_content(html, "og:title")
    if not title:
        title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
        if title_match:
            title = strip_html(title_match.group(1))

    scene = {
        "title": title,
        "url": url,
        "date": parse_date(clean_text(video.get("uploadDate", ""))),
        "details": clean_details(video.get("description", "")),
        "image": extract_scene_image(video, html),
        "performers": extract_scene_performers(html),
        "tags": category_tag_from_url(url),
        "studio": {"name": STUDIO},
    }
    return {key: value for key, value in scene.items() if value}


def extract_performer_name(html):
    header_match = re.search(
        r"<div class=\"profile-header\">.*?<h1>(.*?)</h1>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if header_match:
        name = strip_html(header_match.group(1))
        if name:
            return name

    for candidate in (
        meta_content(html, "og:title"),
        strip_html(meta_content(html, "twitter:title", attr="name")),
    ):
        if candidate:
            candidate = re.sub(r"\s*-\s*TNAFlix.*$", "", candidate, flags=re.IGNORECASE)
            candidate = re.sub(r"^Profile:\s*", "", candidate, flags=re.IGNORECASE)
            candidate = normalize_space(candidate)
            if candidate:
                return candidate

    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if title_match:
        title = strip_html(title_match.group(1))
        title = re.sub(r"\s*-\s*TNAFlix.*$", "", title, flags=re.IGNORECASE)
        title = re.sub(r"^Profile:\s*", "", title, flags=re.IGNORECASE)
        return normalize_space(title)
    return ""


def scrape_performer(url):
    if not url:
        return {}

    try:
        html = fetch(url)
    except Exception:
        return {}

    blocks = load_json_ld_blocks(html)
    person = find_json_ld(blocks, "Person")

    name = clean_text(person.get("name", "")) or extract_performer_name(html)
    image = person.get("image", "")
    if isinstance(image, dict):
        image = image.get("url", "")
    image = clean_text(image) or meta_content(html, "og:image")
    if not image:
        profile_img_match = re.search(
            r'<div class="ph-avatar">\s*<img[^>]+src="([^"]+)"',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if profile_img_match:
            image = clean_text(profile_img_match.group(1))

    performer = {
        "name": name,
        "url": url,
        "image": image,
    }
    return {key: value for key, value in performer.items() if value}


def parse_search_results(html):
    pattern = re.compile(
        r'<a[^>]+href="(https://www\.tnaflix\.com/[^"]+/[^"]+/video\d+)"[^>]+class="video-title[^"]*"[^>]*>(.*?)</a>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    results = []
    seen = set()
    for url, title_html in pattern.findall(html):
        if url in seen:
            continue
        seen.add(url)
        title = strip_html(title_html)
        if not title:
            continue
        results.append(
            {
                "title": title,
                "url": url,
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


def scene_by_url():
    data = read_stdin()
    emit(scrape_scene(data.get("url", "")))


def scene_by_name():
    data = read_stdin()
    query = data.get("name", "")
    results = search_scenes(query)
    emit(results)


def performer_by_url():
    data = read_stdin()
    emit(scrape_performer(data.get("url", "")))


def main():
    if len(sys.argv) < 2:
        emit({})
        return

    mode = sys.argv[1]
    if mode == "sceneByURL":
        scene_by_url()
        return
    if mode == "sceneByName":
        scene_by_name()
        return
    if mode == "performerByURL":
        performer_by_url()
        return

    emit({})


if __name__ == "__main__":
    main()
