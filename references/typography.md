# Typography — type and kinetic type

## 1. Fonts

| Use | Latin | Persian |
|---|---|---|
| Headlines / subtitles | Anton (Vox pattern) | Vazirmatn (with `arabic` subset) |
| Small text | Montserrat | Vazirmatn |
| Reel captions | DejaVu Sans Bold (small Latin labels) | **Lalezar** (see `references/persian-reel-style.md`) |
| Code / mono | TODO: pick one OFL mono font | — |

Fonts must be OFL-licensed (or otherwise freely licensed) when shipped in
`assets/fonts/`. Vazirmatn: `rastikerdar/vazirmatn`, family name `Vazirmatn`.
Check installation with `fc-list :lang=fa`. Emergency fallback: Tahoma.

## 2. Real kerning

- Kinetic type uses real kerning (pdoom pattern), not per-letter hacks.
- Persian/Arabic: **never** letter-by-letter. Captions are word-by-word;
  letters inside a word are shaped together (libraqm / libass shaping).
- Negative `letter-spacing` on Persian closes word gaps — forbidden
  (see `references/persian-rtl.md`).

## 3. Kinetic type rules

- Big words swap / repeat on the beat (Kinetic Type style).
- One chunk on screen at a time; never two caption chunks at once.
- Caption chunks: ≤ 18 characters (Persian ≤ 22).
- Active word highlighted (karaoke style): orange `#D97757` with glow in
  the Lalezar reel style; yellow highlight in the Vox style.
- Readability on mobile: check the smallest text at real phone size.
  If it cannot be read on a phone, it is too small.

## 4. Numbers and dates

- Spell out numbers in narration ("nineteen fifty-one", not "1951").
- Persian zero "۰" renders as a dot in some renderers — check it in the
  final render (see `references/persian-rtl.md`).
- Mixed Persian + English lines: wrap the Persian in RLI…PDI isolates and
  put English terms in their own chip (see `references/persian-rtl.md`).
