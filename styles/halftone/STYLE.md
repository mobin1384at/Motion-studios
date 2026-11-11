# Halftone — هافتون

> Style folder: `styles/halftone/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

3D spheres shaded with print halftone dots — a poster-print look in motion.

## Palette hints

Paper white #FAFAF9 background; spheres in ink black #111111, red #DC2626 and blue #1D4ED8; halftone dots in the same inks.

## Motion notes

Spheres rotate slowly and bob; the halftone dot pattern scales with the light direction, so shading moves across the surface as the sphere turns. Dot size is a function of the surface normal — keep it deterministic per frame.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Halftone style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک هافتون. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
