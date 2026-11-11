# Rubric — 7-dimension judging rubric

Adapted (idea-level) from mg-styles-15 `rubric.md`: build → judge → fix,
two rounds. Score each dimension 0–5 on the **final render**, never on a
snapshot.

## The 7 dimensions

| # | Dimension | What to check (0–5) |
|---|---|---|
| 1 | Motion quality | Movement smooth, eased with numbers, no jitter, no forbidden-list items |
| 2 | Timing / beat sync | Impacts land on words/beats; beat deviation within ±2 ms where music is synced |
| 3 | Legibility | Every word readable on a phone; no overlap; captions inside the safe zone |
| 4 | Style consistency | One style throughout; colours/fonts match the chosen style and brand kit |
| 5 | Sound | Voice clear, music 4–6 dB under speech, SFX on picture events, mix −14 LUFS |
| 6 | Story / structure | Hook in the first 2 s; something new every 2–3 s; ending lands |
| 7 | Technical | Correct size/fps/codec, no black frames, no cropped faces, length matches brief |

## The loop

```text
build → render → judge (score all 7) → fix the WEAKEST segment only → re-render → judge
```

- **Max 2 review rounds.** After round 2, ship the best version and list
  the remaining flaws honestly in the handoff.
- Fix the weakest segment, not the whole film. Re-render that segment.
- Keep the scores in the run log so the next round can see what moved.

## Pass bar (v1 default)

- Ship when every dimension is ≥ 3 and dimensions 3 (legibility) and 7
  (technical) are ≥ 4.
- If legibility or technical is below 4 after round 2, do not ship silently —
  tell the user what is still wrong and what it would take to fix.
