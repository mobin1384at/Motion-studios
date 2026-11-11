# Neo-Brutalism — نئو بروتالیسم

> Style folder: `styles/neo-brutalism/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

Colourful cards with thick black borders, hard shadows and energetic buttons that slam in.

## Palette hints

Loud flat colours: hot pink #FF90E8, yellow #FFC900, lime #A6FAFF / #B8F135, orange #FF6B35 on white #FFFFFF; everything outlined in black #000000 with a 4px hard offset shadow.

## Motion notes

Cards slam in with a fast scale + hard stop (no soft bounce — a single 80ms overshoot at most), buttons wiggle on hover-beat; a sticker element rotates in at ~5s. Motion is punchy and deliberately un-smooth.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Neo-Brutalism style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک نئو بروتالیسم. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
