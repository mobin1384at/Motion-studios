# Retro VHS — رترو VHS

> Style folder: `styles/retro-vhs/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

A synthwave sunset with scan lines, chromatic aberration and a blinking tape timer.

## Palette hints

Sunset gradient: hot pink #FF2E88 → orange #FF7A18 → purple #7C3AED over a dark horizon #1A0B2E; sun in yellow #FDE047; grid in cyan #22D3EE.

## Motion notes

The sun slowly sets (translateY +20px over 8s), the grid scrolls toward the viewer, scan lines drift down continuously, the 'REC ● 00:00:0X' timer ticks each second; a subtle tracking glitch (2-frame horizontal offset) appears once per loop, seeded.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Retro VHS style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک رترو VHS. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
