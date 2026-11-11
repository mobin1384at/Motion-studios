# Particles — ذرات

> Style folder: `styles/particles/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

Thousands of tiny glowing particles swirl, gather and dissolve to form the main text, then scatter again — a living, sparkling reveal.

## Palette hints

Deep dark background (near-black navy #0A0E1A), glowing particles in cyan #22D3EE, magenta #F472B6 and warm gold #FBBF24; text in bright white.

## Motion notes

Particles drift on slow sinusoidal paths, converge into the text over ~2s, hold for ~3s with a gentle shimmer, then disperse and re-form so the 8s loop is seamless. Ease in-out everywhere; no hard cuts. Use a seeded pseudo-random generator so every frame is a pure function of time t (deterministic, re-renderable).

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Particles style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک ذرات. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
