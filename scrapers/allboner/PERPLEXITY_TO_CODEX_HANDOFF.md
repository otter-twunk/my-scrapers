# Perplexity to Codex Handoff

Target site: `https://www.allboner.com`

Target folder: `scrapers/allboner/`

Use this file as the site-specific Codex handoff.

## What Codex Should Do

- Build a working Stash scraper for this site in this folder
- Create or update:
  - `SCRAPER_SPEC.json`
  - the scraper `.yml`
  - the backing Python script
  - `README.md`
- Preserve existing scrapers elsewhere in the repo
- Update the root `README.md` with this scraper folder

## Suggested Hook Modes

- `sceneByURL`
- `sceneByName`

## Site Notes

- Platform: KVS (Kernel Video Sharing)
- Standard KVS route map confirmed: `/videos/<id>/<slug>/`, `/categories/`, `/sites/`, `/search/<query>/`
- `pageContext.langUrls` present in page JS confirming KVS structure
- Cloudflare present — use standard browser headers and set age-gate cookies
- Site is an adult content source — keep scraping metadata-only and respect rate limits
- Perplexity live-inspected this site in May 2026

## Metadata Mapping

- **scene_title**: `og:title`
- **date**: `meta[property='ya:ovs:upload_date']`
- **description**: `og:description`
- **cover_image**: `og:image`
- **performers**: `a[href*='/models/']` — not consistently present on all pages
- **tags**: `a[href*='/categories/']` or `meta[property='video:tag']`
- **studio**: `a[href*='/sites/']`

## Anti-Bot / Access Notes

- Cloudflare present but content accessible with standard browser headers.
- Set Cookie: `age_verified=1; kt_tc=1` to bypass age gate.
- `pageContext.langUrls` confirms standard KVS route map.
- Use conservative request delays.

## Known Limitations

- Model/performer links not visible on sampled scene pages — may not be populated for all content.
- Cloudflare may tighten; implement fallback for 403/challenge responses.
- Adult content — keep scraper metadata-only.

## Validation

Test against these live scene URLs:
- `https://www.allboner.com/videos/89122/homoemo-deep-rides-and-explosive-orgasms-with-james-radford-and-kai-alexander/`
- `https://www.allboner.com/videos/87214/gay-teens-fuck-each-other-in-the-little-ass-without-a-condom/`

- Test `sceneByURL` against a live scene page
- Test `sceneByName` via `/search/<query>/`
- Test fragment matching if practical
