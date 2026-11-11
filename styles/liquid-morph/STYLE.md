# Liquid Morph — مایع / مورف

> Style folder: `styles/liquid-morph/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

Glossy chrome bubbles merge, split and flow like liquid metal, morphing around and through the text.

## Palette hints

Liquid chrome/silver gradients (#E5E7EB → #9CA3AF) on a deep indigo background #1E1B4B, with iridescent highlights in pink #F9A8D4 and aqua #67E8F9.

## Motion notes

Bubbles ease together with squash-and-stretch (scale 1 → 1.15 on merge), surface tension wobble via sine deformation; morphs complete in ~1.5s and hold. Loop by returning every blob to its start position by t=8s.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Liquid Morph style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک مایع / مورف. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
