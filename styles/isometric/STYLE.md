# Isometric — ایزومتریک

> Style folder: `styles/isometric/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

A stepped isometric pyramid built from cubes; a ripple travels across the cubes like a wave.

## Palette hints

Warm paper background #F5EFE6; cubes in terracotta #E07856, sage #8FA98F, ochre #E9B44C and slate #475569; soft shadows; text in dark brown #292524.

## Motion notes

Ripple propagates cube by cube (each cube lifts 10px with a 60ms stagger); the whole pyramid gently rotates ±3°; the wave completes and returns to rest by t=8s for a clean loop.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Isometric style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک ایزومتریک. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
