# Motion design — grammar of movement

Synthesis of mg-styles-15, Prompt Motion's forbidden list, opus-video-prompts,
and video-edit-skill's formula-driven approach.

## 1. Formula-driven, not adjective-driven

Never write "the movement should be elastic". Write the numbers:

- Easing: `cubic-bezier(0.34,1.56,0.64,1)` (back-ease, c≈1.9) for pops.
- Pop-in: scale 0.55 → 1 in 0.2 s, plus 22 px rise and a fade-in.
- Stagger: 2–4 frames between siblings (mg-styles-15).
- Entrance overshoot is a number, not a feeling.

## 2. The forbidden list

Do **not** use these unless the chosen style explicitly demands them:

- crossfade
- spring easing (except stamp/card entrances)
- particles, glow, lens flare (unless the style is e.g. Neon Glow / Particles)
- camera shake
- 3D card flip / 3D rotation of flat cards
- gradient over chrome UI
- impact / jumpy zooms (see `references/camera-moves.md`)

This list is the main defence against AI slop. If a render looks generic,
check this list first.

## 3. Entrances

- Stamps slam in from 1.6× scale.
- Cards arrive with a little overshoot.
- Strips are laid down like tape.
- Words pop (scale 0.55 → 1, back-ease, 0.2 s).
- Big words: scale 0.35 → 1, rotation ±3°, gentle breathing, exit by
  growing ×1.25 and fading.

## 4. Timing

- Something new every 2–3 seconds.
- Visual impacts land on spoken words or beats — never between them.
- Music beat deviation: ±2 ms is the measurable bar
  (motion-video-skill); music 4–6 dB under speech.
- Keep a shared cue table (picture + sound) — see `references/sound.md`.

## 5. Looks vs. motion

A "look" is a designed set of exact values (colours, fonts, spacing,
easing), not a vibe. See `references/looks.md` for the three shipped looks.
When the user has a brand kit, the look comes from the brand kit
(`DESIGN.md` contract in the OpenDesign pattern): colours, fonts, logo,
spacing — and the motion obeys it.
