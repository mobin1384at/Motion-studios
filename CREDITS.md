# Credits

Every borrowed source, what was borrowed, and its license. The full table
with URLs is in [LICENSES.csv](LICENSES.csv).

## License hygiene — read first

- **Only MIT / Apache-2.0 code may be copied** into this skill.
- **AGPL sources (OpenMontage, Concat) and unlicensed sources
  (video-edit-skill, PDoomVideo, opus-video-prompts) are idea-only.**
  Their patterns are described in our own words; no code or text is copied.
- `herk-edit-kit` is GitHub "Other (NOASSERTION)", not MIT as one article
  claimed — idea-only until its LICENSE file is read.
- `media-pipeline` has a license conflict (GitHub says Other, README says
  MIT) — not used; listed here only so nobody copies from it blindly.
- Fonts shipped in `assets/fonts/` must be OFL-licensed (Vazirmatn, Lalezar).
  TODO: verify Lalezar's exact OFL status and source file before shipping
  the font file.
- Music/SFX from Openverse: check the license of each item before use.
- AI video/music output: the user owns the output under the provider's terms;
  record the provider and model in the handoff.

## What this skill is built from

- **Skeleton:** [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)
  (MIT + CC BY 4.0 for demo films) — DIRECTOR/TECHNIQUE/STYLE structure,
  `render(t)` contract, treatment-first, sound pipeline.
- **Determinism + camera:** [cinecode](https://github.com/sarpstar/cinecode)
  (MIT) — `frame = f(t, seed)`, one-line camera vocabulary, stage gates.
- **Prompt + rubric:** [mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)
  (MIT) — 4-part prompt template, 7-dimension rubric, 2-round review loop.
- **Core engine:** [HyperFrames](https://github.com/heygen-com/hyperframes)
  (Apache-2.0) — one HTML file = one video, seekable animation.
- **Persian path:** [persian-reel](https://github.com/aradazr/persian-reel)
  (MIT) — the four Persian traps; plus the user's own Lalezar reel prompt
  and VOX explainer prompt (see `references/persian-reel-style.md` and
  `references/vox-explainer.md`).
- **Prompt bank:** [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)
  (MIT) — 703 prompts, pointer only, not vendored.
- **20 styles:** `claude_crafts` Telegram channel — styles and base prompt
  as supplied by the user; the channel's web preview was not readable
  during research, so verify against the channel before republishing.

## Open questions (need the user)

- Public repo name for hosting the skill (needed for `npx skills add` and
  `/plugin marketplace add`).
- Whether the skill ships with the Separik brand kit as the default example.
- `styles/` and `examples/` population (v1.1): copy `STYLE.md` files from
  lemo-opuscar with attribution, and build 3–5 complete example videos.
