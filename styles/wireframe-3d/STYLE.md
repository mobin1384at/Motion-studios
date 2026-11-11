# Wireframe 3D — وایرفریم سه‌بعدی

> Style folder: `styles/wireframe-3d/`
> Source: claude_crafts Telegram channel (20 animation styles) — style list and base prompt as supplied by the user; the channel itself was not readable from the web during research (see research synthesis §2-ج), so descriptions below are the supplied one-line briefs expanded into usable guidance, not quoted channel text.

## Description

A blue wireframe 3D knot (torus knot) rotates over a perspective grid, technical and precise.

## Palette hints

Dark blueprint background #06121F; wireframe lines in bright blue #38BDF8 and cyan #22D3EE; grid in dim blue #1E3A5F; text in white #F8FAFC.

## Motion notes

Knot rotates slowly and continuously (one full turn per 8s); grid lines scroll toward the viewer to suggest forward motion; text fades in with a tracking (letter-spacing) animation. All motion is a pure function of t.

## Base prompt

**English:**

```
Build an 8-second vertical (1080×1920) animation in a single file with HTML, CSS and JavaScript, in the Wireframe 3D style. Movements smooth and loopable, main text '[your text]', colours matching the style. Return only the complete file code.
```

**فارسی:**

```
یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه فایل بساز، به سبک وایرفریم سه‌بعدی. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]» باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.
```

## Usage notes

- Replace `[your text]` / `[متن تو]` with the actual headline. For Persian text, keep the font Persian-capable (Vazirmatn for body, Lalezar for display) and never use `letter-spacing` on Persian words — it breaks letter joining.
- Duration is fixed at 8 seconds, vertical 1080×1920, single self-contained HTML file.
- Motion must be a pure function of time `t` (deterministic, seekable): no `Math.random()`, no CSS transitions, no state between frames — so the file renders identically frame by frame (HyperFrames / `capture.mjs` contract).
