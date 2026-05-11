#!/usr/bin/env python3

import json
import re
import ssl
import subprocess
import sys
from datetime import datetime
from html import unescape
from urllib.error import URLError
from urllib.request import Request, urlopen


BASE_URL = "https://manporn.xxx"
STUDIO = "ManPorn"
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


def normalize_space(value):
    return re.sub(r"\s+", " ", value or "").strip()


def strip_html(value):
    return normalize_space(unescape(re.sub(r"<[^>]+>", " ", value or "")))


def fetch(url):
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": f"{BASE_URL}/",
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
                f"Referer: {BASE_URL}/",
                "-H",
                f"Cookie: {COOKIES}",
                url,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout


def is_cloudflare_challenge(html):
    prefix = (html or "")[:1000]
    return any(
        marker in prefix or marker in html
        for marker in (
            "cf_chl",
            "Just a moment",
            "Cloudflare",
            "/cdn-cgi/challenge-platform/",
        )
    )


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
    return normalize_space(unescape(match.group(1))) if match else ""


def parse_date(value):
    if not value:
        return ""
    value = normalize_space(value)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value.split("T", 1)[0]


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


def extract_title(video, html):
    title = normalize_space(video.get("name", ""))
    if title:
        title = re.sub(r"\s*[-|]\s*manporn(?:\.xxx)?\s*$", "", title, flags=re.IGNORECASE)
        return normalize_space(title)
    title = meta_content(html, "og:title")
    if title:
        title = re.sub(r"\s*[-|]\s*manporn(?:\.xxx)?\s*$", "", title, flags=re.IGNORECASE)
        return normalize_space(title)
    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not title_match:
        return ""
    title = strip_html(title_match.group(1))
    title = re.sub(r"\s*[-|]\s*manporn(?:\.xxx)?\s*$", "", title, flags=re.IGNORECASE)
    return normalize_space(title)


def extract_image(video, html):
    image = video.get("thumbnailUrl", "")
    if isinstance(image, list):
        image = image[0] if image else ""
    image = normalize_space(image)
    if image:
        return image
    return meta_content(html, "og:image")


def extract_tags(video, html):
    keywords = video.get("keywords", [])
    if isinstance(keywords, str):
        keywords = re.split(r"\s*,\s*", keywords)
    tags = unique_names(keywords)
    if tags:
        return tags

    matches = re.findall(
        r'href="https?://manporn\.xxx/(?:categories|tags)/[^"]+"[^>]*>(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return unique_names(strip_html(match) for match in matches)


def extract_performers(video, html):
    actors = video.get("actor", [])
    if isinstance(actors, dict):
        actors = [actors]

    names = []
    for actor in actors:
        if isinstance(actor, dict):
            names.append(actor.get("name", ""))
        elif isinstance(actor, str):
            names.append(actor)

    performers = unique_names(names)
    if performers:
        return performers

    matches = re.findall(
        r'href="https?://manporn\.xxx/models/[^"]+/"[^>]*title="([^"]+)"',
        html,
        flags=re.IGNORECASE,
    )
    return unique_names(matches)


def scrape_scene(url):
    if not url:
        return {}

    try:
        html = fetch(url)
    except Exception:
        return {}

    if is_cloudflare_challenge(html):
        return {}

    blocks = load_json_ld_blocks(html)
    video = find_json_ld(blocks, "VideoObject")

    scene = {
        "title": extract_title(video, html),
        "url": url,
        "date": parse_date(normalize_space(video.get("uploadDate", ""))),
        "details": normalize_space(unescape(video.get("description", ""))),
        "image": extract_image(video, html),
        "performers": extract_performers(video, html),
        "tags": extract_tags(video, html),
        "studio": {"name": STUDIO},
    }
    return {key: value for key, value in scene.items() if value}


def slug_to_name(slug):
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def scrape_performer(url):
    if not url:
        return {}

    slug_match = re.search(r"/models/([^/]+)/?$", url)
    fallback_name = slug_to_name(slug_match.group(1)) if slug_match else ""

    try:
        html = fetch(url)
    except Exception:
        html = ""

    if html and not is_cloudflare_challenge(html):
        title_match = re.search(
            r'<h1[^>]*class="[^"]*title-line[^"]*"[^>]*>(.*?)</h1>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        name = ""
        if title_match:
            name = strip_html(title_match.group(1))
            name = re.sub(r"\s+videos\s*$", "", name, flags=re.IGNORECASE)
        if not name:
            title_tag = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
            if title_tag:
                name = strip_html(title_tag.group(1))
                name = re.sub(r"\s+Gay Pornstar videos.*$", "", name, flags=re.IGNORECASE)

        performer = {
            "name": name or fallback_name,
            "url": url,
            "gender": "Male",
            "image": meta_content(html, "og:image"),
            "details": meta_content(html, "description", attr="name"),
        }
        if performer["details"]:
            performer["details"] = re.sub(
                r"^Watch pornstar .*? model page at ManPorn\.XXX,\s*",
                "",
                performer["details"],
                flags=re.IGNORECASE,
            )
        return {key: value for key, value in performer.items() if value}

    performer = {
        "name": fallback_name,
        "url": url,
        "gender": "Male",
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
    elif mode == "performerByURL":
        result = scrape_performer(data.get("url", ""))
    else:
        result = {}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
