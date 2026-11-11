---
name: motion-studio
description: Turn the agent into a motion-graphics studio. Build reels, launch videos, explainers, music videos, short films, raw-footage edits, cartoons, product exploded views, and data/map videos — with or without sound — using deterministic code-driven rendering (HyperFrames/Remotion/Manim/Cinecode) plus optional AI video APIs. Use when the user asks for any motion-graphics or video work: a reel, short, explainer, lyric video, product launch, cartoon, or edited footage.
license: MIT
---

# motion-studio

A motion-graphics studio skill. It turns the agent into a director, animator,
sound designer, and editor that delivers a finished MP4 — not a description of one.

Default path is **local and free**. Paid engines are opt-in and need the user's
own API key. Nothing is invented: facts in explainers must be verified against
2+ sources, and every borrowed asset is credited (see `CREDITS.md`).

## Core principles

1. **Deterministic frame = f(t, seed).** Every frame is a pure function of time
   and a seed. No `Math.random()`, no CSS transitions, no state carried between
   frames. Same input = same video. This enables parallel rendering and resume.
2. **Sound first, picture second.** Build the timeline from the narration
   timing (word timings from `scripts/transcribe.py` / TTS word boundaries),
   not the other way round.
3. **Treatment first.** Before any code, write `TREATMENT.md` (see
   `templates/treatment.md`): three candidate structures, logline, shot list
   with frame/angle/camera move and *why*.
4. **Formula-driven, not adjective-driven.** Never "make the movement elastic".
   Write `cubic-bezier(0.34,1.56,0.64,1)` with a 2–4 frame offset.
5. **Forbidden list** (unless the style explicitly demands it): no crossfade,
   no spring easing, no particles/glow/lens flare, no camera shake, no 3D card
   flip, no gradient over chrome UI. See `references/motion-design.md`.
6. **QA from the final render.** Judge the rendered MP4, never a snapshot.
   `scripts/qc.py` and `scripts/check_cuts.py` prove cuts from final frames.
   Two review rounds maximum, scored with the 7-dimension rubric
   (`references/rubric.md`).
7. **License hygiene.** Only MIT/Apache-2.0 code may be copied. AGPL and
   unlicensed sources are idea-only. See `LICENSES.csv`.

## The 9 workflows — routing rules

Pick the workflow by the user's input, then follow its reference file(s).

| # | Workflow | Input | Output | Main engine | Read first |
|---|---|---|---|---|---|
| 1 | reels | script + user's voice | vertical 9:16 MP4, word-synced captions | HyperFrames + faster-whisper | `references/persian-reel-style.md`, `references/edit-recipes.md` |
| 2 | launch | brief + brand kit | 15–60 s MP4, horizontal/vertical | HyperFrames (+ Remotion for data) | `references/motion-design.md`, `references/looks.md` |
| 3 | explainer | educational text/data | MP4 with animated charts + captions | Remotion / Manim / Motion Canvas | `references/vox-explainer.md`, `references/technique.md` |
| 4 | music-video | song + lyrics | MP4 up to 4K60, karaoke typography | pdoom-style engine (three.js + beat grid) | `references/sound.md`, `references/typography.md` |
| 5 | short-film | idea | MP4 up to 10+ min | Cinecode (Quick or Film mode) | `references/director.md`, `references/camera-moves.md` |
| 6 | raw-footage-edit | raw clips | finished MP4 + EDL | video-use pattern + ffmpeg | `references/edit-recipes.md`, `references/gotchas.md` |
| 7 | cartoon | idea + character | cartoon MP4 | p5.js + p5.brush (ClaudeAnimationBase pattern) | `references/director.md`, `references/technique.md` |
| 8 | product-exploded-view | product model/description | interactive SVG/HTML + MP4 | Anatomy pattern + HyperFrames | `references/technique.md`, `references/layout.md` |
| 9 | data-map | data / GeoJSON | MP4 with animated map | Remotion maps / HyperFrames | `references/technique.md`, `references/layout.md` |

Routing rules:

- **Real footage of people is needed** → use an AI video API
  (`references/engines.md` §2: Veo / Runway / Kling / Wan / Higgsfield,
  or fal.ai / Replicate as aggregators). Code-drawn scenes cannot do
  photorealistic humans well.
- **Math/science diagrams** → Manim, not HTML.
- **Data-driven / templated video** → Remotion, not raw HTML.
- **Persian or RTL text anywhere** → read `references/persian-rtl.md` first.
  It is mandatory, not optional.
- **No voice, no budget, no API keys** → stay on the local path:
  HyperFrames + Whisper + Piper/Kokoro + Openverse music/SFX.
- **Sora is excluded.** Its app/website shut down 2026-04-26 and its API
  shut down 2026-09-24. Any guide still asking for a Sora key is outdated.

## How to work

1. **Brief.** Fill `templates/brief.md` with the user (goal, audience, length,
   aspect, language, budget, deadline). If the user only gave an idea, ask at
   most 3 clarifying questions, then proceed with sensible defaults and say so.
2. **Treatment.** Write `TREATMENT.md` from `templates/treatment.md`.
   Get the user's approval on the treatment before building (Film mode).
   Quick mode (≤ ~3 min) may proceed with the treatment shown, not approved.
3. **Sound.** Generate or place the voice first (`scripts/tts.py`),
   get word timings (`scripts/transcribe.py`), build the beat grid
   (`scripts/beat_grid.py`). See `references/sound.md`.
4. **Build.** Write the scene as code — one HTML file per video
   (HyperFrames contract) or a React/Manim/Cinecode scene as routed.
   `frame = f(t, seed)` always. Use `scripts/render.py` as the render router.
5. **Assemble.** `scripts/mix.py` mixes voice + music + SFX, masters at
   −14 LUFS, true peak ≤ −1 dBTP, music ducked under voice.
6. **QA.** Render, watch the final MP4 (contact sheet + risky stills),
   score with `references/rubric.md`, fix, max 2 review rounds.
7. **Deliver.** MP4 + `SOURCES.md` (facts, sources, image licenses) +
   credits entry. Use `templates/handoff.md`.

## Scripts

`scripts/` is owned by the scripts builder; the agent only calls them:

| Script | Purpose |
|---|---|
| `setup.py` | Detect OS, check ffmpeg/Node/Python/Chrome, print STATUS |
| `render.py` | Render router: HyperFrames / Remotion / Manim / Cinecode |
| `capture.mjs` | Frame-by-frame capture in headless Chrome |
| `transcribe.py` | faster-whisper transcription, word-level timestamps |
| `captions.py` | Kinetic captions locked to words + ASS/SRT (Persian RTL-safe) |
| `tts.py` | Narration (ElevenLabs / Azure fa-IR / Piper / Kokoro) |
| `mix.py` | Mix + master −14 LUFS + ducking |
| `beat_grid.py` | Beat grid of a song + lyric alignment |
| `qc.py` | Quality checks (motion from frame 1, legibility, repeats, loudness, safe zone) |
| `check_cuts.py` | Prove cuts from the final render |
| `guard.py` | Guard/hook: stop mechanical errors where they happen |
| `fetch_fonts.py` | Download the OFL fonts from official sources (md5-verified) |

Run `scripts/setup.py` first in any new environment and fix what it reports
before building.

## References (progressive disclosure — read only what the task needs)

- `references/director.md` — directing: treatment, shot list, story shape
- `references/technique.md` — building and rendering, determinism, seek(t)
- `references/camera-moves.md` — one-line camera vocabulary
- `references/motion-design.md` — motion grammar + forbidden list
- `references/typography.md` — typography + kinetic type + real kerning
- `references/sound.md` — sound design + shared picture/sound cue table
- `references/persian-rtl.md` — **Persian/RTL traps (mandatory for fa)**
- `references/engines.md` — full engine + API matrix and how to connect
- `references/styles-catalog.md` — style catalog (15 + 66 + 20 + 703 prompts)
- `references/rubric.md` — 7-dimension judging rubric + 2 review rounds
- `references/gotchas.md` — real traps ("each trap cost one render")
- `references/looks.md` — designed looks with exact values
- `references/layout.md` — safe zones for 9:16 / 16:9 / 1:1
- `references/edit-recipes.md` — edit recipes (EDL, best take, cut silence…)
- `references/vox-explainer.md` — full Vox-style explainer pipeline
- `references/persian-reel-style.md` — Lalezar Persian reel workflow

## Templates

- `templates/prompt-template.md` — 4-part prompt template
- `templates/treatment.md` — treatment template
- `templates/brief.md` — production brief template
- `templates/handoff.md` — delivery + credits template

## Persian rules — summary

Full rules: `references/persian-rtl.md`. The short version:

- Persian subtitles **only** via libass + Vazirmatn font + RLI/PDI isolates.
  **NEVER** `ffmpeg drawtext` for Persian (it renders letters disconnected
  and reversed).
- Never put `<html dir="rtl">` on a render stage — it renders the video black.
- Never use negative `letter-spacing` on Persian — it closes word gaps.
- Persian zero "۰" renders as a dot in some renderers — check it in the render.
- Whisper `small` breaks Persian — use `large-v3`.
- Persian captions are word-by-word, never letter-by-letter; keep an English
  term inside its own chip.
- Persian voice: ElevenLabs v3/v4 or Azure/edge-tts `fa-IR-DilaraNeural` /
  `fa-IR-FaridNeural`. Persian runs ~15% longer than English — plan timing.

## When to stop and ask

- The user wants a paid engine but has no API key → explain the key step,
  do not invent one.
- A fact for an explainer cannot be confirmed by 2+ sources → mark it TODO,
  do not invent it.
- The user asks for a cloned voice without consent → refuse the clone;
  offer a stock voice instead.
- A render fails twice the same way → stop, report the error and the last
  working state instead of looping.
