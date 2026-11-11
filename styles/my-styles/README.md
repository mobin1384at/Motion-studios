# My Styles — ساخت سبک خودت

> Flow adapted from lemo-opuscar (MIT): each style is a `STYLE.md` + a fully coded demo film. A style is not a mood board — it is a written contract the model can follow.

## The 5-step flow

### 1. Name the feeling, not the look
Write one sentence: what should the viewer *feel* in the first 2 seconds? (e.g. "warm, handmade, trustworthy" — not "orange and round").
Pick 3 reference frames (a film still, a poster, a reel) and write down what they share: palette, geometry, pacing, texture.

### 2. Write the STYLE.md skeleton
Copy any existing `styles/*/STYLE.md` and fill in the same sections:
- **Description** — one paragraph, what the style *is*.
- **Palette hints** — 3–6 hex colours + background + text colour, with roles (not just a swatch list).
- **Motion notes** — timing, easing values (numbers, not adjectives), loop behaviour, what is forbidden.
- **Base prompt** — the EN + FA prompt that generates an 8-second vertical animation in this style.

### 3. Build one 8-second demo
Generate the demo from the base prompt (single self-contained HTML file, 1080×1920, seekable `seek(t)` / `render(t)` contract, deterministic — no `Math.random()`, no CSS transitions).
Watch it at 3 speeds: real-time, frame-by-frame (does every frame hold up?), and muted (does it work without sound?).

### 4. Judge it with the rubric, twice
Score the demo against the 7-dimension rubric in `references/rubric.md` (from mg-styles-15): fix the weakest dimension, re-render, score again. Two review rounds minimum — stop only when the weakest score stops improving.

### 5. Freeze and file it
When the demo passes: give the style a kebab-case folder name (`styles/<your-style>/STYLE.md`), put the demo next to it, add one line to the styles catalog (`references/styles-catalog.md`), and record the style's license/source in the file header. A style without a demo is a draft, not a style.
