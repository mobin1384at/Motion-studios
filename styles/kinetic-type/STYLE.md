# Kinetic Type — تایپ جنبشی

> Style folder: `styles/kinetic-type/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

Big words swap, slide and repeat on the beat — typography itself is the motion.

## Palette hints

High-contrast: ink black #111111 on paper white #FAFAF9, with one accent word in burnt orange #EA580C; or inverted (white on black) for reels.

## Motion notes

Words enter with a fast slide + slight overshoot (cubic-bezier(0.34,1.56,0.64,1)), hold ~1.2s, exit with a scale-down; word swaps land exactly on the beat grid (every 1s at 120 BPM feel). No letter-spacing on Persian text (it breaks joining).

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Kinetic Type style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک تایپ جنبشی. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
