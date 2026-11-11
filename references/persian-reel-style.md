# Persian reel style — the Lalezar workflow

The full workflow from the user's prompt
`claude_video_edit_prompt_29_mwjn.md`: turn a vertical talking-head video
into an engaging educational reel/short with code only (ffmpeg + Python).
Output: one vertical MP4, 1080×1920.

## 0. Role and inputs

- Input: the user's vertical video (a person talking) + the attached font
  file `Lalezar-Regular.ttf` + the exact spoken text.
- The user also gives: keywords that must stay orange, and 2–3 very
  important words that must appear big and glowing in the middle of the
  screen.
- Requirement: "Code Execution and File Creation" enabled in Claude settings.
- If the Lalezar file is not attached, tell the user and do not continue.

## 1. Tools and preparation

- Only tools present in the environment: `ffmpeg`, `ffprobe`, `python3`,
  `Pillow (with libraqm)`, `numpy`. No internet — install nothing. Check
  each one first.
- Fonts: **Lalezar** (attached file) for all Persian text. DejaVu Sans Bold
  for small Latin labels (top capsule).
- Persian shaping: `ImageDraw.text(..., direction='rtl', language='fa')`
  with libraqm; verify with `features.check('raqm')`. Fallback:
  `arabic_reshaper` + `python-bidi`. Never draw Persian text without shaping.
- Phone video usually carries rotation in metadata. ffmpeg applies it, but
  check a sample frame that it is vertical and correct.

## 2. Visual design

| Item | Value |
|---|---|
| Output | 1080×1920, 24 fps, H.264, CRF 18, `+faststart`, AAC 192k |
| Orange | `#D97757` (217,119,87) |
| Cream | `#F4EDE4` (244,237,228) |
| Dark | `#18120F` (24,18,16) |
| Colour grade | `eq=contrast=1.08:saturation=1.15:brightness=0.01` + `vignette=PI/6` |
| Bottom shade | dark gradient from the bottom up to 700 px high, for caption legibility |

Fixed elements on the picture:

- **Top capsule:** rounded rect (560×84), dark with orange border, a small
  orange circle + Latin text, back-ease entrance from 0.3 s.
- **Glowing rings:** two thin orange rings with three cream dots that rotate
  (top-right corner and mid-left) and breathe slightly.
- **Progress bar** at the bottom: 14 px high, orange on a translucent
  background.
- **End card:** from ~8.5 s (when the speech ends): darkened background +
  spinning orange circular logo + «آموزش‌های بیشتر …» (Lalezar, size 110) +
  «فالو کن و ادامه بده» (orange, size 76).

## 3. Subtitles — the heart of the style

- Groups of **2–3 words**. Each word enters exactly when it is spoken.
- Word entrance: **pop with overshoot**. Scale 0.55 → 1 with back-ease
  (c≈1.9) in 0.2 s, plus 22 px rise from below and a fade-in.
- Active word (being spoken) and keywords: **orange `#D97757` with glow**
  (orange layer with GaussianBlur radius 26 and alpha ×3 under the text)
  and slightly larger (×1.06). The rest cream.
- Every text: Lalezar size 136, dark stroke 5 px + soft shadow.
- **Caption background:** for each group a rounded box (radius ≈ 56),
  `rgba(22,16,14,0.84)` with a 3 px orange border. Width = group width +
  110 px, height ≈ 224. The box pops 0.82 → 1 with the first word and fades
  in the last 0.12 s of the group. Caption centre: y = 1400.
- RTL layout: first word on the right. Word gap 34 px. The whole group's
  layout is computed up front so words do not shift as they appear.
- **Big word:** for very important words, one big glowing orange word in
  the middle of the screen (y≈960), Lalezar starting at size 360 and
  shrinking to a max width of 900 px, with pop (scale 0.35→1), rotation
  ±3°, gentle breathing, and exit by growing ×1.25 and fading. No small
  caption appears at that moment.
- Never leave a short word like «و» alone for long. Group it with the next
  word.

### Word timing

If a speech-to-text tool (Whisper or similar) is available, use the exact
word times. If not:

1. Convert audio to wav with `ffmpeg -ac 1 -ar 16000` and extract the energy
   envelope (RMS every 10 ms, smoothed).
2. Find the pauses (deep valleys) — these are sentence boundaries.
3. Count the syllables of each word and split each inter-pause interval
   between words in proportion to syllable count. Then re-check against
   the energy peaks and valleys.
4. Tell the user honestly that the timing is estimated and ask them to watch
   the video and report misaligned words.

## 4. Zoom — impact/jumpy zoom is forbidden

The earlier mistake: sudden zooms constantly jumping up and back, which
looked like a bug. **Correct:** a few smooth cinematic moves, each ~1 s
approach, a short hold, then a slow retreat. Low intensity, timed on
important words.

- Implementation: `zoompan` filter on the main video (4K, so quality does
  not drop when zooming) with `d=1:s=1080x1920:fps=24`.
- Curve: keyframes `(time, zoom)` with cosine interpolation (ease in-out):
  `z = z0 + (z1-z0) * (0.5 - 0.5*cos(PI*(t-t0)/(t1-t0)))` where `t = on/24`.
- Sample keyframes (for a ~10 s video): `(0,1.0) (1.0,1.0) (2.1,1.13)
  (2.9,1.13) (3.9,1.02) (4.9,1.15) (5.0,1.15) (5.5,1.06) (6.4,1.19)
  (6.9,1.19) (8.2,1.05) (9.0,1.0)`. Strongest push-in on the big word.
- Zoom centre: `x='(iw-iw/zoom)/2'`, `y='(ih-ih/zoom)*0.2'` so the frame
  stays on the face, not the middle of the body.
- Max zoom ≈ 1.20. More crops the lips and face.
- Build the expression from the last segment backwards with nested
  `if(lt(on/24,t1), seg(...), rest)`.

## 5. Music

- Mellow, calm music that does **not** cover the speaker.
- If the user gave no music file: synthesize it with numpy. Soft pad
  (several sines with slight detune and weak harmonics) over the chords
  Am → Fmaj7 → Cmaj7 → G (each chord ≈ 2.65 s, soft in/out), plus a gentle
  arpeggio (sine pluck with exponential decay, step ≈ 0.43 s) and stereo
  echo. Then normalize and save as 48 kHz stereo wav.
- Mix with ffmpeg: `lowpass=f=2600, volume=0.055, afade in 0.8s,
  afade out 1.7s`, then `amix=inputs=2:duration=first:normalize=0`.
- **Measure the volume** (`volumedetect`). Average music should be about
  **12–15 dB below** the speaker's average. The first version was only
  3 dB below and far too loud.
- No copyrighted music. If the user gave a song, use that one.

## 6. Render architecture

1. Read length, resolution, rotation, and audio streams with `ffprobe`.
   (iPhone videos have several audio/data streams; select `0:a:0`.)
2. Draw each frame of the graphics layer (captions, box, rings, capsule,
   progress bar, end card) with Pillow as RGBA and pipe it **raw
   (rawvideo rgba)** into ffmpeg's second input. No need to save thousands
   of PNGs.
3. In `filter_complex`: main video → `fps, eq, zoompan, vignette` →
   `overlay` graphics layer → `format=yuv420p`. Audio → `amix` with music.
4. Pre-build each word's sprite (cream version and glowing-orange version)
   and only resize/paste per frame, to keep the render fast.
5. If one image stream is used twice, add `split` (without it ffmpeg errors).

## 7. QC checklist (before delivery)

- Extract key frames (first, middle of each caption group, big word, end
  card), build a sheet, and look at it: is the Persian written correctly
  and connected? Is the box centred on the text? Is the caption on the
  face? Did the zoom crop the face?
- Output length equals input length; size 1080×1920.
- Check the music volume with `volumedetect`.
- Deliver the file and briefly say what was built and what is estimated.

## 8. Honesty

- If a font, the text, or a capability (e.g. code execution) is unavailable,
  say so at the start and invent nothing.
- If you cannot hear the audio, the timing is estimated — say so.
- After the first version, ask: «زمان‌بندی کلمه‌ها، حجم موزیک و شدت زوم رو
  چطور حس کردی؟» and fix only those.

## 9. Past mistakes (do not repeat)

- Impact zoom again and again → looks like a bug. Use soft ease in-out.
- First music was too loud. Measure the volume.
- Persian text with the default font was legible but not beautiful.
  Ask for Lalezar.
- Without a background, captions got lost on light clothing → put a dark
  box behind them.
