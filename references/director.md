# Director — directing a code-built video

Adapted (idea-level) from lemo-opuscar `DIRECTOR.md`, cinecode, and showreel.
No text is copied from those sources; the structure below is the synthesis.

## 1. Treatment first

Never write scene code before `TREATMENT.md` (template:
`templates/treatment.md`). A treatment has:

1. **Logline** — one sentence: who, what changes, why it matters.
2. **Three candidate structures** — e.g. hook → stakes → evidence → turn →
   kicker (Vox shape); problem → agitate → solve (launch); beat-by-beat
   (music video). Pick one and say why the other two lost.
3. **Shot list** — one row per shot: time, frame (what is on screen), angle,
   camera move, sound, and *why* this shot and not another.
4. **Style choice** — one style from `references/styles-catalog.md`, with the
   reason it fits the audience and the message.
5. **Sound plan** — voice, music, SFX, and where each lands.

Film mode (cinecode): 6 steps with approval — treatment, then build.
Quick mode (≤ ~3 min): show the treatment, then proceed.

## 2. Story shapes

| Shape | When | Beats |
|---|---|---|
| Vox explainer | explainers | hook → stakes → evidence → turn → kicker, one through-line |
| Launch | product / brand | problem → agitate → solve → proof → CTA |
| Beat map | music video | intro → verse → chorus → bridge → outro, visuals on beats |
| Three-act | short film | setup → confrontation → resolution |
| List / how-to | reels | hook (first 2 s) → steps → payoff → CTA |

Rule: **something new happens every 2–3 seconds.** Nothing empty in the
first 2 seconds.

## 3. Shot discipline

- One idea per shot. If a shot needs two sentences to explain, split it.
- Every visual impact sits on a spoken word or a beat — never between them.
- Prefer a slow push-in inside a scene over a cut. Whip-pan between scenes;
  never a crossfade (see forbidden list in `references/motion-design.md`).
- Stamps slam in from 1.6× scale; cards arrive with a little overshoot;
  strips are laid down like tape. Springs are for entrances, not for drift.

## 4. Directing the agent (parallel work)

- Give sub-agents a brief, not a chat: `ANIMATION_GUIDE.md`-style briefs
  (one per chapter/scene) with a shared scene API.
- Storyboard first, then code — one file per chapter with a common API.
- Keep a `STATE.md` so work continues in a new chat: what is done, what is
  decided, what is still open.

## 5. Review before the final render (max 2 rounds)

- One frame per beat as a contact sheet + full-size stills of the risky
  moments (tears, stamps, map moves, big words).
- Check: anything outside the frame? Subtitles overlapping? Persian reading
  direction right? Every impact on its word? Anything empty in the first 2 s?
- Score with `references/rubric.md`. Fix only the weakest segment, then
  re-render that segment — not the whole film.
