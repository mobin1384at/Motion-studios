# Glassmorphism — شیشه‌ای / گلس‌مورفیسم

> Style folder: `styles/glassmorphism/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

Frosted glass cards float over a blurred, colourful background; the text sits on a glass panel with soft depth.

## Palette hints

Blurred gradient blobs in coral #FB7185, violet #A78BFA, sky #7DD3FC and mint #6EE7B7 over a light base #F8FAFC; glass panels white at 20% opacity with 1px white border; text in dark ink #1E293B.

## Motion notes

Background blobs drift slowly (translate ±40px over 8s); glass cards float with a gentle ±8px vertical bob, staggered; text fades and rises 12px on entry. Blur is static (backdrop-filter), motion comes from the blobs and cards only.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Glassmorphism style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک شیشه‌ای / گلس‌مورفیسم. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
