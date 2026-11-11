# Camera moves — one-line vocabulary

From cinecode's one-line camera vocabulary, plus the 7 cinematic moves
reported in the research (Follow Shot etc.). Each move is one line in the
shot list: `move(parameters, duration, easing)`.

## Moves

| Move | One-liner | Use |
|---|---|---|
| Static | `static()` | dialogue, titles, anything that must be read |
| Push-in | `push_in(from=1.0, to=1.15, dur=1.0s, ease=cosine)` | emphasis inside a scene; the default "something is happening" move |
| Pull-out | `pull_out(from=1.15, to=1.0, dur=1.0s, ease=cosine)` | reveal, end of a scene |
| Pan | `pan(dx, dur, ease=cosine)` | follow a horizontal element (map, timeline, bars) |
| Whip-pan | `whip_pan(dir, dur=0.25s)` | scene change — never a crossfade |
| Tilt | `tilt(dy, dur, ease=cosine)` | vertical reveal |
| Follow | `follow(subject, offset)` | keep a moving subject framed (Follow Shot) |
| Orbit | `orbit(angle, radius, dur)` | 3D product / exploded view |
| Dolly-zoom | `dolly_zoom(...)` | rare; only when the style demands it |

## Rules

- **Cosine ease in-out for zooms:** `z = z0 + (z1-z0) * (0.5 - 0.5*cos(π*(t-t0)/(t1-t0)))`.
  Smooth, cinematic. **Impact / jumpy zooms are forbidden** — they read as a bug.
- Zoom moves are ~1 s of approach, a short hold, then a slow retreat.
  Max zoom ≈ 1.20× — beyond that faces/lips get cropped.
- Zoom centre: keep it on the face, not the middle of the body
  (e.g. `y = (ih - ih/zoom) * 0.2` in a zoompan filter).
- Camera shake is on the forbidden list (`references/motion-design.md`).
- In code-built scenes the camera is a function of `t` like everything else:
  `camera(t)` returns scale + translation, seeded and deterministic.
