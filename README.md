# motion-studio

A motion-graphics studio skill for AI coding agents. It turns the agent into a
director, animator, sound designer, and editor that delivers a finished MP4 —
with or without sound, in Persian or English, local/free by default, with paid
engines available behind the user's own API key.

- **License:** MIT — copyright (c) 2026 Mobin Aboutalebiyan
- **Format:** open Agent Skills format (`SKILL.md` + `scripts/` + `references/`
  + `templates/`). One folder, no binary plugin.
- **Install:** see [INSTALL.md](INSTALL.md).

## The 9 workflows

| # | Workflow | Input | Output |
|---|---|---|---|
| 1 | Reels / Shorts | script + your voice | vertical 9:16 MP4, word-synced captions |
| 2 | Launch / ad | brief + brand kit | 15–60 s MP4, horizontal or vertical |
| 3 | Explainer / educational | text / data | MP4 with animated charts and captions |
| 4 | Music video / lyric video | song + lyrics | MP4 up to 4K60, karaoke typography |
| 5 | Short film | idea | MP4 up to 10+ minutes, code-built scenes |
| 6 | Raw-footage edit | raw clips | finished MP4 + EDL |
| 7 | Cartoon / character | idea + character | cartoon MP4 |
| 8 | Product exploded view | product model / description | interactive SVG/HTML + MP4 |
| 9 | Data / map video | data / GeoJSON | MP4 with animated map |

Routing rules, principles, and the full workflow live in
[SKILL.md](SKILL.md).

## Engines at a glance

- **Local renderers (free, deterministic):** HyperFrames (Apache-2.0, the core
  engine), Remotion (special license — data-driven video), Motion Canvas (MIT),
  Revideo (MIT), Cinecode (MIT, cinematic), Manim (MIT, math/science).
- **AI video APIs (paid, API key):** Veo, Runway, Kling, Wan, Higgsfield —
  or fal.ai / Replicate as aggregators with one key.
- **Audio:** ElevenLabs v3/v4 and Azure/edge-tts `fa-IR` for Persian voice;
  Piper/Kokoro local; Openverse for free music/SFX (no key).
- **Sora is excluded** — its app/website shut down 2026-04-26 and its API shut
  down 2026-09-24.

Full matrix with auth and pricing notes: [references/engines.md](references/engines.md).

## Principles

1. Deterministic frame: `frame = f(t, seed)` — same input, same video.
2. Sound first, picture second — the timeline comes from narration timing.
3. Treatment first — no code before `TREATMENT.md`.
4. Formula-driven, not adjective-driven — `cubic-bezier(0.34,1.56,0.64,1)`,
   not "make it elastic".
5. QA from the final render, with a 7-dimension rubric and max 2 review rounds.
6. Persian/RTL is a first-class path, not an afterthought
   ([references/persian-rtl.md](references/persian-rtl.md)).

## Layout

```text
motion-studio/
├── SKILL.md            # the skill (frontmatter + routing + workflow)
├── README.md           # this file
├── INSTALL.md          # per-platform install
├── LICENSE             # MIT
├── LICENSES.csv        # every borrowed source + its license
├── CREDITS.md          # credits for borrowed work
├── scripts/            # render / transcribe / captions / tts / mix / qc
├── references/         # director, technique, camera, sound, Persian RTL,
│                       # engines, styles catalog, rubric, gotchas, looks,
│                       # layout, edit recipes, vox explainer, persian reel
├── templates/          # prompt, treatment, brief, handoff
├── styles/             # per-style STYLE.md files (stubs exist; full ports TODO in v1.1)
├── assets/             # fonts (Vazirmatn + OFL Latin), sfx, HyperFrames blocks
└── examples/           # example videos built with the skill
```

## Sources

This skill is a synthesis, not a copy. Its skeleton comes from
[lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) (MIT),
[cinecode](https://github.com/sarpstar/cinecode) (MIT),
[mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) (MIT) and
[HyperFrames](https://github.com/heygen-com/hyperframes) (Apache-2.0).
The Persian path comes from
[persian-reel](https://github.com/aradazr/persian-reel) (MIT).
The full source table with licenses is in [LICENSES.csv](LICENSES.csv) and
[CREDITS.md](CREDITS.md).

**License hygiene:** only MIT/Apache-2.0 code may be copied into this skill.
AGPL and unlicensed sources are idea-only — see `LICENSES.csv`.

## Status

v1 — built and tested 2026-11-11. All 12 scripts are real and syntax-checked;
`setup.py`, `guard.py`, `captions.py`, `mix.py`, `beat_grid.py`, `qc.py` and
`check_cuts.py` passed smoke tests with real data; both examples were rendered
end-to-end with `capture.mjs` + headless Chrome + ffmpeg and passed `qc.py`
(see `examples/*/README.md`). `transcribe.py`/`tts.py`/`capture.mjs` degrade
gracefully with install instructions when their optional dependencies are
missing (faster-whisper, ElevenLabs/Azure keys, puppeteer). `install.ps1`
(Windows) is written but not syntax-verified — no PowerShell on the build
machine. Items still open are marked TODO in the files.

## GitHub checkout vs. the release zip

The release zip (`motion-studio.zip`) is self-contained: it vendors the OFL
fonts (`assets/fonts/*.ttf`) and the two rendered example MP4s. A GitHub
checkout cannot carry binary files through the connector push, so:

- **Fonts:** run `python3 scripts/fetch_fonts.py` — it downloads Vazirmatn
  v33.003 and Lalezar from their official sources and verifies them by md5
  (see `assets/fonts/FONTS.md`).
- **Example MP4s:** not in the repo; render them with the commands in
  `examples/*/README.md`, or download them from the release zip.
