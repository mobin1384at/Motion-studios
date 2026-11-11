# Sound — sound design, voice, music, mix

## 1. Sound first, picture second

The timeline is built from narration timing. Steps:

1. Voice first (`scripts/tts.py` or the user's recorded voice).
2. Word timings (`scripts/transcribe.py`, or TTS `WordBoundary` events).
3. Beat grid (`scripts/beat_grid.py`) for music.
4. Visuals are placed on words and beats — see the cue table below.

## 2. Voice

### Persian TTS — the honest table

| Engine | Auth | Persian | Notes |
|---|---|---|---|
| ElevenLabs v3 / v4 | API key, `POST /v1/text-to-speech/{voice_id}` | Yes — v3 lists 70+ languages, v4 90+, incl. `fa` | Models: `eleven_v3`, `eleven_v4`, `eleven_multilingual_v2`, `eleven_flash_v2_5`. Older multilingual models do **not** list Persian. Voice cloning from a short sample (~30 s); public figures need consent; v4 has Clone Strength. |
| Azure Speech / edge-tts | Azure key / subscription; edge-tts is free, unofficial, no SLA | Yes — `fa-IR-DilaraNeural` (female), `fa-IR-FaridNeural` (male) | edge-tts gives `WordBoundary` timings — use them for karaoke captions. |
| Piper (local) | none, local CPU | Reportedly yes — 5 voices (amir, ganji, ganji_adabi, gyro, reza_ibrahim), medium quality | TODO: verify against the official Piper voice list. |
| Kokoro (local) | none | Not listed in the researched sources | TODO: verify. |
| OpenAI TTS | API key | **Not verified** — user tests say Persian reads but lower quality; OpenAI publishes no official TTS language list. Do not count as "official Persian". | No cloning; 6 built-in voices only. |
| Google Cloud TTS | API key / service account | **Contradictory — do not rely on it.** Marketing says "Persian"; an independent check (Oct 2026) found no Persian voice in the official list, and a forum report shows `400 voice does not exist` for `fa-IR-Wavenet-D` / `fa-IR-Standard-A`. Only Gemini-TTS (Preview) lists `fa-IR`. | TODO: check the official Supported voices page directly. |
| Coqui XTTS-v2 | local, GPU 4–6 GB VRAM | **No Persian.** 17 languages, Persian not among them. | Best open-source cloning (6 s reference) but **CPML non-commercial license**; Coqui shut down Dec 2023 / Jan 2024. Not for commercial video. |

### ElevenLabs — tts-director lessons (from the user's own tests)

- **v4 speed setting effectively does not work** — do not rely on it to fix
  pacing; fix pacing by editing the text (punctuation, pauses) instead.
- **Some diacritics are mispronounced** — check Persian diacritics in the
  render and simplify the text where the voice stumbles.
- **The $1 plan gives a Persian voice** — the cheapest paid tier is enough
  to get Persian; do not assume Persian needs a higher tier.
- Persian voice quality was **not practically tested** in the research —
  verify with a real test render before promising a client a Persian voice.

### General voice rules

- Persian runs ~15% longer than the same English text — plan timing for it
  (edge-tts: raise the rate, e.g. +20% for `fa-IR-FaridNeural`, and shorten
  breaths if the video passes its length budget).
- Record each phrase as a separate take; place takes with short breaths
  (0.3–0.5 s); put the first word of each phrase on a quarter beat of the
  music grid (Vox pattern).
- **Only clone a voice you have permission to clone.**

## 3. Music and SFX

- Free, no key: **Openverse API** (https://api.openverse.org/ — 5M+ music
  and SFX, no API key). Check each item's license before use.
- **Earshot** (https://github.com/Leonxlnx/earshot) — gives the agent
  "hearing": it understands which sound is used and where an SFX belongs.
  TODO: the repo was not directly checked in the research — verify before
  relying on it.
- Procedural sound: Web Audio (Cinecode/HyperFrames) and NumPy/SciPy
  synthesis in Python (see `references/vox-explainer.md` §8 and
  `references/persian-reel-style.md` §5 for two worked synth recipes).
- Subscription music services (Epidemic Sound / Artlist): prices and
  licenses were not in the researched sources — check the license of each
  track on that service's page before commercial use.
- SFX per picture event: paper slide, paper tear, marker, stamp, pop,
  typing, whoosh, impact. Synthesize them in code where possible so the
  project stays self-contained.

## 4. Mix and master

- Levels: music −2 dB, SFX −4 dB, voice 0 dB; music ducked (sidechain)
  under the voice.
- Whole mix at **−14 LUFS**, true peak ≤ −1 dBTP.
- Music 4–6 dB under speech; beat deviation ±2 ms.
- ffmpeg warning: `sidechaincompress` drops the last few frames — pad
  inputs by 1 s and trim back to the exact length after mixing.
- `scripts/mix.py` does the mix; verify loudness with `loudnorm` /
  `volumedetect` on the final file.

## 5. Shared picture/sound cue table

One table, both columns — every visual cue has a sound cue:

| Visual cue | Sound cue |
|---|---|
| year tag stamps on | stamp |
| card slides in | paper slide |
| photo tears | rip |
| label struck through | marker |
| scene change | whoosh |
| title card | impact + held chord |
| word pops | pop (quiet, or none) |
| bars collapse | low thud |

Keep the table in `cues.json` so picture and sound never drift apart.
