# Looks — designed looks with exact values

A look is a set of exact values, not a vibe. Pick one (or take the values
from the user's brand kit) and use the numbers everywhere.

## Look 1 — Lalezar reel (Persian educational reel)

From the user's Lalezar reel prompt. Full workflow:
`references/persian-reel-style.md`.

| Item | Value |
|---|---|
| Output | 1080×1920, 24 fps, H.264, CRF 18, `+faststart`, AAC 192k |
| Orange | `#D97757` (217,119,87) |
| Cream | `#F4EDE4` (244,237,228) |
| Dark | `#18120F` (24,18,16) |
| Colour grade | `eq=contrast=1.08:saturation=1.15:brightness=0.01` + `vignette=PI/6` |
| Caption font | Lalezar 136, dark stroke 5 px + soft shadow |
| Caption box | rounded (radius ≈ 56), `rgba(22,16,14,0.84)`, 3 px orange border; width = group width + 110 px, height ≈ 224; centre y = 1400 |
| Active / keyword word | orange `#D97757` with glow (orange layer, GaussianBlur radius 26, alpha ×3), ×1.06 larger |
| Top capsule | rounded rect 560×84, dark with orange border, small orange circle + Latin text, back-ease entrance from 0.3 s |
| Progress bar | 14 px high, orange on translucent background, bottom |
| Zoom | cosine ease, max 1.20×, centre on the face |

## Look 2 — Vox collage (documentary explainer)

From the user's VOX explainer prompt. Full pipeline:
`references/vox-explainer.md`.

| Item | Value |
|---|---|
| Output | 1080×1920, 60 fps, H.264 yuv420p, CRF 16 |
| Paper colours | yellow `#f6c448`, cream `#f2ece0`, navy `#1d2b45`, coral `#e9664e` |
| Texture | paper noise + fibres + halftone dot layer; film grain on top of everything |
| Cut-outs | rembg (`isnet-general-use`), rough white paper border, soft shadow |
| Fonts | Anton (headlines/subtitles) + Montserrat (small text); Persian: Vazirmatn with `arabic` subset |
| Subtitles | chunks ≤ 18 chars (Persian ≤ 22), spoken word highlighted yellow |
| Motion | whip-pan between scenes, slow push-in inside a scene, springs on entrances (stamps from 1.6×), something new every 2–3 s |
| Music | 100 BPM, D minor, Dm – Bb – Gm – A, one chord per bar |
| Mix | music −2 dB, SFX −4 dB, voice 0 dB, whole mix −14 LUFS, true peak ≤ −1 dBTP |

## Look 3 — Warm paper (brand default)

A neutral warm look for launch/brand work when the user has no brand kit.
TODO: exact hex values are not yet fixed — take them from the user's brand
kit when one exists (Separik brand: cream `#FEF3E2`, burnt orange `#D4621A`,
ink brown `#2A1A0E`, light cream `#FFF0D1`; fonts Vazirmatn + Manrope).
Do not invent brand colours — ask for the brand kit or use Look 1/2 values.
