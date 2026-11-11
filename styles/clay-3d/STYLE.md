# Clay 3D — کلی / خمیری سه‌بعدی

> Style folder: `styles/clay-3d/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

Soft clay shapes — a ball, a cube and a donut — bounce and squash with a handmade, tactile feel.

## Palette hints

Soft pastel clay: blush pink #F9A8D4, butter yellow #FDE68A, mint #A7F3D0, sky #BAE6FD on a warm cream background #FFF7ED; soft ambient shadows.

## Motion notes

Shapes bounce with squash-and-stretch (scaleY 0.8 on impact, 1.15 on rebound), staggered by ~0.4s; the donut wobbles on landing. Bounces are timed to a steady rhythm so the loop restarts cleanly.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Clay 3D style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک کلی / خمیری سه‌بعدی. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
