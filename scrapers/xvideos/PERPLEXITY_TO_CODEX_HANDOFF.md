# Perplexity to Codex Handoff

Target site: `https://www.xvideos.com`

Target folder: `scrapers/xvideos/`

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
- `performerByURL`

## Site Notes

- Platform: Custom/proprietary (XVideos in-house platform)
- Site is an adult content source — keep scraping metadata-only and respect rate limits
- Perplexity live-inspected this site in May 2026; URL patterns and selectors below are verified

## Metadata Mapping

- **scene_title**: window.xv.conf.dyn.video_title OR html5player.setVideoTitle(...) OR JSON-LD VideoObject.name
- **date**: JSON-LD VideoObject.uploadDate
- **description**: JSON-LD VideoObject.description OR og:description
- **cover_image**: JSON-LD VideoObject.thumbnailUrl[0] OR html5player.setThumbUrl169(...)
- **performers**: window.xv.conf.dyn.video_models (may be empty); uploader link at /profiles/<name>
- **tags**: window.xv.conf.dyn.video_tags (array)
- **studio**: html5player.setSponsors(...) — usually false for amateur content

## Anti-Bot / Access Notes

- No Cloudflare detected on public pages.
- Standard browser-grade headers (User-Agent, Accept-Language) are sufficient.
- Add conservative request delays between pagination calls.

## Known Limitations

- video_models array is frequently empty on amateur/upload pages.
- Performer pages use /profiles/ not a dedicated pornstar path for user-uploaded content.
- Signed CDN media URLs expire; do not store raw stream URLs.
- Content URLs include signed tokens and should not be followed for download.

## Validation

Test against these live scene URLs:
- `https://www.xvideos.com/video57885821/mi_gran_polla`

- Test `sceneByURL` against a live scene page
- Test `performerByURL` if performer pages exist
- Test `sceneByName` if site search is usable
- Test fragment matching if practical
