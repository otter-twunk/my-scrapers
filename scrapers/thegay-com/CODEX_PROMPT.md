# Codex Prompt — TheGay.com

```text
Use the files in scrapers/thegay-com/ and build the scraper.

Specifically:

1. Open https://www.thegay.com/video/748987/bareback-gay-sex-with-jerk/ in a browser.
   Use DevTools > Network > Fetch/XHR to find the exact internal API endpoint the
   Vue app calls to load video metadata. The expected pattern is:
     GET /api/json/video/{id}
   Confirm the path and any required headers or query parameters.

2. Update API_ENDPOINT_PATH in TheGay.py with the confirmed path.

3. Implement scrape_scene() in TheGay.py:
   - Extract the video ID from the URL using re.search(r'/video/(\d+)/', url)
   - Call the confirmed API endpoint with: User-Agent (Firefox), Referer (scene URL),
     Cookie: age_verified=1, Accept: application/json
   - Map the JSON response fields to Stash output using SCRAPER_SPEC.json as the guide
   - Handle missing fields gracefully — return partial results, never raise

4. Do not add sceneByName, sceneByQueryFragment, sceneByFragment, or performerByURL —
   all search and performer routes are Vue SPA paths with no server-rendered data.

5. Update README.md with site-specific install and usage notes.

6. Update the root README.md to add the scrapers/thegay-com/ entry.

7. Test sceneByURL against: https://www.thegay.com/video/748987/bareback-gay-sex-with-jerk/
   Verify title, date, image, performers, and tags are populated.

All research is in PERPLEXITY_TO_CODEX_HANDOFF.md and SCRAPER_SPEC.json.
Follow repo conventions from workflow/NEW_SCRAPER_CHECKLIST.md.
```
