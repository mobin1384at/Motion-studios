# Technique — building and rendering

Synthesis of lemo-opuscar `TECHNIQUE.md`, cinecode, HyperFrames, and the
pdoom-video `ENGINE.md` pattern. Idea-level only; no copied code.

## 1. The determinism contract

```text
frame = f(t, seed)
```

- `t` is time in seconds (or frame number). `seed` is a fixed integer.
- No `Math.random()`, no `Date.now()`, no CSS transitions/animations, no
  state carried between frames. All randomness is seeded (e.g. a mulberry32
  PRNG from the seed).
- Consequence: renders are parallelisable, resumable, and reproducible —
  the same input always gives the same video.
- In HyperFrames this is the `seek(t)` contract: the page must render any
  time `t` on demand. In cinecode it is `capture --verify`.

## 2. One HTML file = one video (HyperFrames contract)

- A video is a single HTML file with `data-start` / `data-duration` on
  scenes. GSAP / Lottie / Three.js / Anime.js are allowed only through a
  seekable adapter — the animation must be drivable by `seek(t)`.
- Render: headless Chrome captures frame by frame (`scripts/capture.mjs`),
  ffmpeg assembles to MP4 (`scripts/render.py`).
- Motion blur: adaptive — sample sub-frames when velocity is high.
  TODO: exact sub-frame counts per engine are in the scripts builder's notes.

## 3. Scene API (code-built scenes)

Every scene is a pure function of time plus seeded randomness:

- Inputs: `t` (seconds), `seed`, scene data (beats, word timings, cues).
- Outputs: the frame at `t`.
- Shared data files: `cues.json` (visual/sound cues), `beat_grid.json`
  (tempo grid), `words.json` (word timings from transcription or TTS).
- For music video: a beat grid + word timings + envelopes (tempo in BPM,
  e.g. 132.007 BPM in the pdoom reference — measure the real tempo, do not
  guess it).

## 4. Rendering pipeline

```text
plan → write → wire → lint → preview → render
```

1. **plan** — treatment + shot list.
2. **write** — scene code.
3. **wire** — cues, timings, assets.
4. **lint** — `scripts/guard.py` + `scripts/qc.py` on stills.
5. **preview** — contact sheet, one frame per beat.
6. **render** — full frame-by-frame render + mix + master.

## 5. Performance notes (from the research)

- A 4K60 render of a complex coded video is heavy (the pdoom reference took
  ~57 min on an M5 Pro, peak 23 GB RAM). Default to 1080p; 4K only on request.
- Pre-build sprites (e.g. each caption word in cream and in glowing orange)
  and only resize/paste per frame — do not re-draw text every frame.
- If one image stream is used twice in an ffmpeg filter graph, add `split`
  or ffmpeg errors.
- Chrome is required for HyperFrames rendering. If Chrome is missing,
  `scripts/setup.py` reports it; install via
  `npx puppeteer browsers install chrome` or the system package manager.

## 6. Engines — which renderer for which job

See `references/engines.md` §1. Short version: HyperFrames is the default;
Remotion for data-driven/templated video; Manim for math/science; Motion
Canvas / Revideo as MIT alternatives; Cinecode for cinematic code-built film.
