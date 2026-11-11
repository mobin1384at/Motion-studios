# Blueprint — بلوپرینت

> Style folder: `styles/blueprint/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

A blue technical drawing: gears rotate together, dimension lines and annotations draw themselves.

## Palette hints

Blueprint blue #1B4F9C background (or white lines on blue); lines in white #FFFFFF and light blue #93C5FD; dimension marks in yellow #FDE047.

## Motion notes

Gears rotate at meshed speeds (ratio by tooth count, e.g. 2:1); dimension lines draw in (stroke-dashoffset) one by one; the text appears as a title-block stamp at ~6s. Motion is mechanical and precise — constant angular velocity.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Blueprint style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک بلوپرینت. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
