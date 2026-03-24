# AniGap

A sleek, Miami Vice–themed desktop app that finds anime you haven't watched — solo or with friends. Compare 1–4 AniList accounts and discover something new.

Enter 1–4 AniList usernames, set your filters, and get a curated list of unwatched anime sorted by score.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-purple) ![AniList API](https://img.shields.io/badge/API-AniList%20GraphQL-cyan)

---

## Features

- **Single or multi-user** — works solo or with up to 4 AniList accounts for group discovery
- **Smart sequel filtering** — skips sequels, recaps, and spin-offs so you only see fresh starting points
- **Movie mode** — dedicated filter that excludes adaptations of existing TV series, compilation films, and sequel movies
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

The finished executable will be at `dist/AniGap v9.exe`.

## Usage

1. Enter at least **1 AniList username** (up to 4 for group comparison)
2. Adjust filters as needed (max episodes, year range, result limit)
3. Pick a format (TV, OVA, Movie, TV+OVA, All)
4. Hit **INITIATE SEARCH**
5. Browse results — click any title to open it on AniList

## How It Works

The app queries the [AniList GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs/) to fetch each user's watched list, then searches for highly-rated finished anime that nobody in the group has seen. Sequels and prerequisites are automatically filtered out using relation data (prequels, parent series, adaptations) so every result is a valid entry point.

## License

This project is provided as-is for personal use.
