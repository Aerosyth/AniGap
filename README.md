# AniGap

A sleek, Miami Vice–themed desktop app that finds anime you haven't watched — solo or with friends. Compare 1–4 AniList accounts and discover something new.

Enter 1–4 AniList usernames, set your filters, and get a curated list of unwatched anime sorted by score.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-purple) ![AniList API](https://img.shields.io/badge/API-AniList%20GraphQL-cyan)

---

## Features

- **Single or multi-user** — works solo or with up to 4 AniList accounts for group discovery
- **Smart sequel filtering** — skips sequels, recaps, and spin-offs so you only see fresh starting points
- **Next-season discovery** — optional toggle that surfaces the next unwatched season of shows all participants have already seen, without skipping ahead in the chain (e.g. if everyone watched S1, S2 appears — but S3 won't show until everyone has also seen S2)
- **Sequels-only mode** — a second toggle that narrows results to show *only* next seasons, hiding all new series so you can focus on continuing what you've started (searches deeper to fill your result limit)
- **Movie mode** — dedicated filter that excludes adaptations of existing TV series, compilation films, and sequel movies; sequel toggles work correctly with movies too
- **Configurable filters** — max episodes, result limit, min/max year
- **Format toggle** — TV, OVA, Movie, TV+OVA, or All
- **English titles preferred** — displays English anime titles by default, with Japanese (romaji) as fallback
- **Clickable results** — titles link directly to their AniList page
- **Copy to clipboard** — one-click export of your results with scores, metadata, and AniList links
- **Standalone EXE** — build a portable Windows executable with the included batch script

## Requirements

- Python 3.8+
- Dependencies: `customtkinter`, `requests`, `pyperclip`, `pillow`

## Installation

```bash
pip install customtkinter requests pyperclip pillow
```

Then run:

```bash
python anigap.py
```

## Building a Standalone EXE (Windows)

Place `anigap.py`, `icon.ico`, and `build_exe.bat` in the same folder, then double-click `build_exe.bat` (or run it from a terminal). It will:

1. Install all dependencies + PyInstaller
2. Bundle everything into a single `.exe`

The finished executable will be at `dist/AniGap v10.exe`.

## Usage

1. Enter at least **1 AniList username** (up to 4 for group comparison)
2. Adjust filters as needed (max episodes, year range, result limit)
3. Pick a format (TV, OVA, Movie, TV+OVA, All)
4. Toggle **"Include next unwatched seasons"** if you want to see sequels that everyone in the group is ready for
5. Toggle **"Show only next seasons"** to hide all new series and show exclusively continuations (requires the first toggle to be on — note: this searches deeper and may take longer)
6. Hit **INITIATE SEARCH**
7. Browse results — click any title to open it on AniList

## How It Works

The app queries the [AniList GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs/) to fetch each user's watched list, then searches for highly-rated finished anime that nobody in the group has seen. Sequels and prerequisites are automatically filtered out using relation data (prequels, parent series, adaptations) so every result is a valid entry point.

When the **next-season toggle** is enabled, the app also includes sequels where every participant has completed all prerequisite seasons. It walks the full prequel chain for each candidate — so a third season only appears if all users have seen both the first and second seasons. Recaps and compilations are still filtered out regardless of the toggle. Movie mode correctly distinguishes sequel movies from standalone films — adaptation and source-material filters always apply, and only movies with a valid prequel chain are let through.

When the **sequels-only toggle** is enabled on top of that, the app filters out all new series entirely and shows only next seasons you're ready to continue. Because qualifying results are rarer, the search scans up to 50 pages (vs. the normal 15) to fill your result limit. This applies to all formats including movies.

## License

This project is provided as-is for personal use.
