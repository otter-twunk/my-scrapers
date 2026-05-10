# MyMuscleVideo Scraper

Stash scraper for [mymusclevideo.com](https://mymusclevideo.com/) — a custom muscle/bodybuilder video tube site.

## Supported Modes

| Mode | Supported |
|---|---|
| `sceneByURL` | ✅ Yes |
| `sceneByName` | ✅ Yes |
| `performerByURL` | ❌ No (login-gated) |
| `sceneByFragment` | ❌ No |
| `sceneByQueryFragment` | ❌ No |

## Scraped Fields

| Field | Source |
|---|---|
| Title | `og:title` meta tag |
| Date | `og:video:release_date` meta property |
| Description | `og:description` meta property |
| Cover Image | `og:image` (300×226 JPG) |
| Tags | `/video/tag/` anchor links on scene page |
| Studio | Constant: `MyMuscleVideo` |
| Performers | ❌ Not available |

## Install

1. Copy `MyMuscleVideo.yml` and `MyMuscleVideo.py` into your Stash `scrapers/` folder.
2. Restart Stash.
3. The scraper will appear as **MyMuscleVideo** in the scraper list.

## Usage

- **Scene by URL**: paste a scene URL such as `https://mymusclevideo.com/107027/sexy-guy-muscle/`
- **Scene by Name**: enter a title string — the scraper queries `/search/video/?s=` and returns matching candidates

## Known Limitations

- **No performer data**: scene pages show only the uploader account, not named performers.
- **Low-resolution cover**: `og:image` is 300×226px — no full-res public alternative.
- **Model pages are login-gated**: `performerByURL` is not implemented.
- **Visible date is relative** (`"5 years ago"`): the scraper uses `og:video:release_date` for the real date.
