# Split-Flap — تابلوی فرودگاهی (Split-Flap)

> Style folder: `styles/split-flap/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

An airport departure-board: letters flip one by one until they spell the text.

## Palette hints

Board black #0F0F0F, flaps in charcoal #1F2937 with cream letters #F5F5DC; thin divider lines #374151; text in warm white.

## Motion notes

Each letter cycles through the alphabet quickly then locks into place, left to right, with a 120ms stagger and a flip (rotateX) animation; a soft click feel via a 2-frame scale pulse on each lock. All letters settle by ~5s, hold to 8s.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Split-Flap style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک تابلوی فرودگاهی (Split-Flap). حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
