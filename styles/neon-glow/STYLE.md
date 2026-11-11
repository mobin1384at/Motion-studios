# Neon Glow — نئون

> Style folder: `styles/neon-glow/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

A neon sign flickers on, buzzing with electric light, with a blinking light tunnel receding behind the text.

## Palette hints

Near-black background #050505; hot pink neon #FF2E88, electric cyan #00E5FF and warm amber #FFB300; glow via layered text-shadow / box-shadow.

## Motion notes

Sign flickers on in the first 1s (two quick on-off blinks, then steady), tunnel rings pulse outward on the beat, glow intensity breathes slowly. Flicker pattern must be seeded/deterministic, not Math.random().

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Neon Glow style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک نئون. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
