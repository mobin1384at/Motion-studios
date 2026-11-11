# Gotchas — real traps

Each trap cost at least one render. Check this file before rendering.

## Rendering

- `<html dir="rtl">` renders the video completely black. Set `direction: rtl`
  on the stage element only — never on `<html>`.
- Negative `letter-spacing` closes Persian word gaps. Never use it on Persian.
- Persian zero "۰" can render as a dot. Check it in the final render.
- Whisper `small` breaks Persian. Use `large-v3`.
- ffmpeg `sidechaincompress` drops the last few frames. Pad inputs by 1 s,
  trim back after mixing.
- If one image stream is used twice in a filter graph, add `split` or ffmpeg
  errors.
- iPhone videos carry rotation in metadata; ffmpeg applies it, but verify
  with a sample frame that the video is vertical and correct.
- iPhone videos can have several audio/data streams — select `0:a:0`.

## Motion

- Impact / jumpy zooms read as a bug. Use cosine ease in-out, ~1 s approach,
  short hold, slow retreat, max 1.20×.
- Without a dark caption box, subtitles disappear on light clothing.
  Always put a dark rounded box behind captions.
- Music that is only 3 dB under the voice is far too loud. Measure with
  `volumedetect`: music should be ~12–15 dB under the speaker's average
  (Lalezar reel recipe) or 4–6 dB under speech (general bar) — measure, do not
  guess.
- Never leave a short word like "و" alone on screen for long — group it
  with the next word.

## Sound / voice

- ElevenLabs v4 speed setting effectively does not work — fix pacing in
  the text, not in the speed slider.
- Some Persian diacritics are mispronounced by ElevenLabs — simplify the
  text where the voice stumbles.
- Overlapping SRT/ASS cues cause vertical jitter in libass — keep cues
  non-overlapping.
- `ffmpeg drawtext` does not shape Persian — letters come out disconnected
  and reversed. Use libass (`subtitles` / `ass` filter).

## Process

- A single account cannot buy its own listing; a full end-to-end order flow
  needs a separate buyer identity. (Separik QA lesson — applies to any
  marketplace test, not just video.)
- If a render fails twice the same way, stop and report — do not loop.
- Never invent a fact, a price, a font file, or an API key. Mark it TODO
  and ask.
