# Styles catalog

How to use this file: pick **one** style per video, name it in the treatment,
and copy its base prompt. Do not mix two styles in one video unless the
treatment justifies it.

## 1. The 20 claude_crafts styles

Source: the `claude_crafts` Telegram channel (20 animation styles) and its
Instagram reel. **Note:** the channel's web preview was not readable during
the research (2026-11-11) and the prompt texts were not obtained from the
web. The 20 style names and descriptions below are the list supplied by the
user; the base prompt is the user's own template, verbatim.

**Base prompt (English) — use verbatim, filling in `[style]` and `[your text]`:**

> Build an 8-second vertical (1080×1920) animation in a single file with HTML,
> CSS and JavaScript, in the [style] style. Movements smooth and loopable,
> main text '[your text]', colours matching the style. Return only the complete
> file code.

**Base prompt (Persian, original) — قالب اصلی فارسی:**

> یه انیمیشن ۸ ثانیه‌ای عمودی (۱۰۸۰×۱۹۲۰) با HTML و CSS و JavaScript توی یه
> فایل بساز، به سبک [سبک]. حرکت‌ها نرم و لوپ‌شونده باشن، متن اصلی «[متن تو]»
> باشه و رنگ‌ها هماهنگ با همون سبک. فقط کد کامل فایل رو بده.

| # | Style | What it looks like |
|---|---|---|
| 1 | Particles | Thousands of tiny glowing particles swirling to form the text |
| 2 | Liquid Morph | Glossy chrome bubbles merging/splitting like liquid |
| 3 | Holographic | Rotating 3D ring, rainbow holographic colours |
| 4 | Neon Glow | Neon sign with blinking light tunnel |
| 5 | Wireframe 3D | Blue wireframe 3D knot on perspective grid |
| 6 | Glassmorphism | Frosted glass cards on blurred colourful background |
| 7 | Kinetic Type | Big words swapping/repeating on the beat |
| 8 | Isometric | Stepped isometric pyramid, cubes rippling |
| 9 | Clay 3D | Soft clay shapes (ball, cube, donut) bouncing |
| 10 | ASCII Art | Rotating 3D shape made of green terminal characters |
| 11 | Gradient Mesh | Coloured gradient clouds slowly dissolving into each other |
| 12 | Comic Book | Comic panel with "WHOOSH!" and halftone dots |
| 13 | Split-Flap | Airport board letters flipping to form the text |
| 14 | Retro VHS | Synthwave sunset with scan lines and tape timer |
| 15 | Halftone | 3D spheres with print halftone shading |
| 16 | Bauhaus | Red/yellow/blue geometric shapes swapping places |
| 17 | Pixel Art | Pixel game scene with character and coins |
| 18 | Blueprint | Blue technical-drawing gears rotating together |
| 19 | Art Deco | Gold deco arches drawn line by line |
| 20 | Neo-Brutalism | Colourful cards with thick black borders and energetic buttons |

## 2. The 66 lemo-opuscar styles

Source: [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) (MIT for
code/docs + CC BY 4.0 for demo films; 6 sound tracks excluded). Each style
has a `STYLE.md` + a fully code-built demo film. Style slugs verified from
the repo tree on 2026-11-11 (67 `STYLE.md` files including the `_template`).

1. archive-lighttable
2. art-deco
3. ascii-crt
4. backrooms
5. blueprint
6. brick-toy
7. briefing-board
8. caption-news
9. cel-anime-80s
10. chalkboard
11. circuit-board
12. city-symphony
13. countdown
14. crayon-book
15. dark-keynote
16. data-physical
17. dataviz
18. desktop-flythrough
19. engraving
20. game-show
21. glass-product
22. halftone-dossier
23. hd-2d
24. hologram-hud
25. impasto
26. ink-wash
27. iso-infographic
28. isometric-picture-book
29. kino-montage
30. lidar-survey
31. living-screencast
32. lowpoly-island
33. memphis-diorama
34. microgame
35. microscope
36. midcentury-toon
37. news-package
38. newsreel
39. one-line
40. paper-lantern
41. paper-popup
42. papercut-red
43. pictogram-motion
44. pixel-rpg
45. printed-long-take
46. risograph
47. rubber-hose
48. satellite-briefing
49. scifi-toon
50. shadow-puppet
51. silent-film
52. silkscreen-poster
53. spy-titles
54. stained-glass
55. swiss-motion
56. teardown
57. telestrator
58. tilt-shift
59. transit-map
60. ukiyoe
61. urban-sketch
62. visual-investigation
63. watercolor
64. white-model
65. whiteboard
66. woodcut

Full per-style files live in the lemo-opuscar repo (`styles/<slug>/STYLE.md`).
TODO (v1.1): copy the `STYLE.md` pattern into this skill's `styles/` folder
for the styles actually used, respecting the MIT + CC BY 4.0 split
(demo films are CC BY 4.0; the 6 excluded sound tracks are not included).

## 3. The 15 mg-styles-15 styles

Source: [mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)
(MIT for code/prompts/films; third-party files keep their own licenses).
Each style is one 10-second film from one prompt.

1. Frame-by-frame (فریم‌به‌فریم)
2. Isometric 2.5D (ایزومتریک ۲٫۵بعدی)
3. Flat vector (فلت وکتور)
4. Line art (لاین‌آرت)
5. 3D render, Blender (رندر سه‌بعدی)
6. Morph (مورف)
7. Sticker explainer (استیکر اکسپلینر)
8. Cyberpunk HUD (هاد سایبرپانک)
9. Collage (کولاژ)
10. Aurora / glassmorphism (آرورا/گلس‌مورفیسم)
11. Bauhaus (باهاوس)
12. Synthwave / VHS (سینث‌ویو/VHS)
13. Pixel art (پیکسل‌آرت)
14. Liquid motion (لیکویید موشن)
15. Variety-show caption, 9:16 (کپشن واریته‌شو)

The most valuable parts of this repo for this skill are its `rubric.md`
(→ `references/rubric.md`) and its 4-part prompt template
(→ `templates/prompt-template.md`).

## 4. The 703-prompt bank

Source: [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)
(MIT) — 703 prompts for viral videos built with Opus 5.5. Categories:
motion-graphics (58), explainer (16), 3D scene (14), game/interactive (12),
plus the rest. Each entry maps prompt → technology (most frequent:
Canvas+SVG+GSAP, Three.js+GLSL, Web Audio).

Use it as a **prompt bank**, not as code: pick a prompt close to the job,
adapt it with `templates/prompt-template.md`, and rebuild — do not copy a
prompt's video and claim it as original. Rights to each entry belong to its
creator.

TODO: the bank is not vendored into this skill. A future step can index the
703 prompts by category and link the closest ones from the treatment.
