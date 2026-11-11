# Edit recipes — raw footage to finished video

Pattern: video-use / video-edit-skill. The core idea: **the LLM never
watches frames** — it reads a word-by-word transcript + a contact sheet of
the timeline and edits from that.

## 1. Transcript-first edit

1. Transcribe with faster-whisper (word timestamps; Persian: `large-v3`).
2. Pick the best take of each sentence from the transcript.
3. Cut silences (`silencedetect`) and filler words.
4. Write an EDL (edit decision list) — in/out points per clip.
5. Assemble with ffmpeg; verify cuts from the final render
   (`scripts/check_cuts.py`).

## 2. Best take

- Score each take of a sentence (clarity, pace, no stumble) from the
  transcript and the audio envelope — not from watching.
- Keep the best; drop the rest. Say which take was used in the handoff.

## 3. Cut silence and fillers

- Silence: `silencedetect`, cut pauses longer than the style allows.
- Fillers: cut from the word timings, then close the gap; check the cut
  frame for a jump.

## 4. Cutout / background removal

- Separate the speaker from the background (rembg / video cutout tools);
  keep the cutout as a transparent WebM layer for parallel inserts.

## 5. Word-behind (word-by-word captions)

- Captions locked to word timings; active word highlighted; groups of
  2–3 words; Persian rules in `references/persian-rtl.md` and the Lalezar
  recipe in `references/persian-reel-style.md`.

## 6. B-roll and parallel inserts

- Build B-roll / overlay scenes in parallel sub-agents (HyperFrames /
  Remotion / Manim) as transparent WebM inserts, then composite.
- Every insert lands on a word or a beat.

## 7. QA from the final render

- `scripts/check_cuts.py` proves each cut from final frames.
- `scripts/qc.py`: motion from frame 1, legibility, repeats, loudness,
  safe zone. Fix the weakest segment, max 2 rounds
  (`references/rubric.md`).
