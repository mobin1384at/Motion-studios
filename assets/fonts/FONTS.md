# Fonts — فونت‌ها

Fonts bundled with the motion-studio skill for Persian + Latin motion graphics.
All fonts in this folder are under the **SIL Open Font License 1.1 (OFL-1.1)** — free for personal
and commercial use, including embedding in videos and documents. The font files themselves
may not be sold on their own. Full license text: `OFL.txt` in this folder.

## Files

| File | Font | Version / source | md5 |
|---|---|---|---|
| `Lalezar-Regular.ttf` | Lalezar Regular (display, Arabic/Latin) | Copied from the user's file `Lalezar-Regular__1__27_qwkn.ttf`; md5 verified `b09134ac350e6345b0b6cd94f78f6ffc` | `b09134ac350e6345b0b6cd94f78f6ffc` |
| `Vazirmatn-Variable.ttf` | Vazirmatn variable (wght 100–900) | GitHub release v33.003, `rastikerdar/vazirmatn` — file `fonts/variable/Vazirmatn[wght].ttf` inside `vazirmatn-v33.003.zip`, renamed on copy | `63d2e128b5b911ac9455e5204f36d45f` |
| `OFL.txt` | — | SIL OFL 1.1 text as shipped inside the Vazirmatn v33.003 release zip | `88985b4355a8a44627dde041f10aba75` |

## License verification (2026-11-11)

- **Lalezar — SIL OFL 1.1, verified.** Fontsource page for Lalezar lists license `OFL-1.1`,
  copyright "2015 The Lalezar Project Authors (https://github.com/BornaIz/Lalezar)", designer
  Borna Izadpanah. Google Fonts also lists it under the SIL Open Font License 1.1.
  Sources checked 2026-11-11: https://fontsource.org/fonts/lalezar/about
- **Lalezar build note (2026-11-11):** the vendored file is the 1.003 build supplied by the
  user (md5 `b09134ac...`); the official repo master currently serves the 1.0 build
  (md5 `793f1fe6...`, verified by download). Both are Lalezar by Borna Izadpanah, OFL 1.1.
  `scripts/fetch_fonts.py` downloads the official-master build and accepts either md5
  on `--check`, so a GitHub checkout (which cannot carry binary fonts) still gets a
  verified font.
- **Vazirmatn — SIL OFL 1.1, verified.** The `OFL.txt` file shipped inside the official
  v33.003 release zip begins: "Copyright 2015 The Vazirmatn Project Authors
  (https://github.com/rastikerdar/vazirmatn) — This Font Software is licensed under the SIL
  Open Font License, Version 1.1." Release: https://github.com/rastikerdar/vazirmatn/releases/tag/v33.003

## Usage notes

- **Vazirmatn** is the default Persian font for body text and captions (variable weight 100–900;
  use `font-variation-settings: 'wght' 700` for bold captions). Use it for all Persian subtitles —
  never `ffmpeg drawtext` for Persian (it renders letters disconnected and reversed); burn
  subtitles with libass + Vazirmatn instead (see `references/persian-rtl.md`).
- **Lalezar** is a display font for big Persian headlines only (weight 400 only, no bold).
  It supports Persian/Arabic + Latin; use it for titles, not body text.
- Persian rendering traps (from persian-reel): never set negative `letter-spacing` on Persian
  text (it closes word gaps); Persian zero "۰" can render as a dot in some pipelines — check
  the rendered frames.
- **Download note (environment quirk, 2026-11-11):** the first download attempt failed with
  curl exit 23 because `/tmp` was 100% full (512 MB tmpfs). Downloading the release zip into
  the workspace succeeded. If a future download fails the same way, check `df -h /tmp` first.
  Manual download URL if needed: https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/vazirmatn-v33.003.zip
