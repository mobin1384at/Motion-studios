# Engines — full matrix and how to connect

Default path is **local and free**. Paid engines are opt-in and need the
user's own API key. Prices change monthly and secondary sources disagree —
figures below are ballpark, not official rates. Check the official page
before budgeting.

## 1. Local code-driven renderers (no API key, deterministic output)

| Tool | Language / input | Render | Needs | License / cost | Best for |
|---|---|---|---|---|---|
| HyperFrames | HTML/CSS/JS; video = one HTML file with `data-start`/`data-duration`; GSAP/Lottie/Three.js/Anime.js via seekable adapter | Local; Puppeteer (headless Chrome, frame-by-frame seek) + FFmpeg; MP4/WebM/MOV/GIF | Node 22+, FFmpeg; `npx hyperframes init/preview/render` | Apache-2.0; local render free; cloud render via HeyGen credits (cloud price not in sources) | **Core engine of this skill** — HTML video without React or a build step |
| Remotion | React/TypeScript; video = component; `useCurrentFrame` | Local; headless Chrome + FFmpeg; MP4/WebM/GIF; Lambda cloud render | Node 18+, Chrome; no API key | **Special license** — free for individuals / non-profits / companies up to 3 people; larger companies need a company license; Creators $25/seat/month reported in secondary sources — **re-check at remotion.dev/license** | Second engine; deterministic motion, animated charts, data-driven templated video |
| Motion Canvas | TypeScript with generators | Local; editor with live preview | Local | MIT | MIT alternative to Remotion for explanatory / vector animation |
| Revideo | TypeScript (shape, text, media, animation) | Local; headless render API, parallel render, React player | Local; zero-dep core | MIT | Light second engine for server / serverless rendering |
| Cinecode | Skill; agent writes a screenplay and builds each frame in code; single-page `film.html`, Canvas 2D or three.js/WebGL | Local; frame-by-frame capture in headless Chrome (`capture.mjs`) + FFmpeg; MP4 + audio mastered −14 LUFS | Node 22+, Python 3.9+, ffmpeg, Chrome; optional narrator with the **user's own Gemini key** (has a free quota) or ElevenLabs | MIT; very new (2026-11-03) | Short film / ad / explainer / music video with 3D scenes |
| Manim (Community Edition) | Python; `Scene` class with `self.play()` | Local; `manim -pqh file.py SceneName`; MP4 in `media/videos/` | FFmpeg + LaTeX (for formulas) + Cairo/Pango; no API key | MIT; free | Math / science / technical animation, precise charts and diagrams; not photorealistic scenes |

## 2. AI video APIs (real footage — only when needed)

| Model / service | Auth | Subscription / payment | Key notes |
|---|---|---|---|
| Google Veo (Veo 3.1) | Two paths: **Gemini API with API key**, or **Vertex AI / Google Cloud with Service Account / OAuth and billing enabled**; indirect: fal.ai / Replicate / Runway / Higgsfield | Yes — paid; one source says no free tier on Gemini API; GCP $300 trial mentioned in one source (needs verification) | Models `veo-3.1-generate-001`, `veo-3.1-fast-generate-001` reported as GA, `veo-3.1-lite` as Preview. One source says Veo 3.1 preview models were switched off in Gemini API on 2026-10-22 and developers were referred to Gemini Omni Flash — **verify in Google's official docs**. Invisible SynthID watermark. Reported rates $0.05–$0.75/sec — **not in an official source**. |
| OpenAI Sora (Sora 2) | — | — | **EXCLUDED. Shut down.** App and website 2026-04-26, **API 2026-09-24**. Do not put it in the shortlist. |
| Runway (Gen-4 / Gen-4.5) | **API key** in the Developer Portal; billing in credits (1 credit = $0.01); MCP at `https://mcp.runwayml.com/mcp` with account login (no key, OAuth) | Yes — pay-as-you-go; limited free plan with 125 one-time credits reported in one source; reported rates: Gen-4 Turbo 5 credits/sec, Gen-4.5 12 credits/sec | Also sells other people's models (Veo, Kling, Wan) with the same key — one key, several models. |
| Kling (Kuaishou) | **API key** on the Kuaishou developer platform (async, task-based API); MCP at `https://kling.ai/mcp` with account login | Yes — credits / subscription; reported rates $0.11–$0.196/sec — **not in an official source** | One source says Kling has no clean global first-party API and most teams reach it via fal or Replicate — **needs verification**. |
| Wan (Alibaba) | **API key** in Alibaba Cloud Model Studio (DashScope); also via fal / Replicate / Runway / Higgsfield | Yes — pay-as-you-go; open models Wan 2.1/2.2 can also run locally (needs GPU) | Wan 3.0 went GA 2026-08-24 with **closed weights** (unlike 2.1/2.2); up to 30 s, 1080p. |
| Higgsfield | **API key in `KEY_ID:KEY_SECRET` format**; header `Authorization: Key $HF_KEY`; official SDK `@higgsfield/client` (server-side only); MCP at `https://mcp.higgsfield.ai/mcp` with account login | Yes — credits / subscription; Starter $9/month (120 credits) in one source, $15/month (200 credits) in another — **sources disagree; exact price not in an official source** | Hosts its own models (Soul, Cinema Studio) and others (Kling, Seedance, Veo, Wan); 15+ models. |

**Aggregators** (one key instead of one per model): **fal.ai** and **Replicate**
give hundreds of models (Veo, Kling, Wan…) with one key/token. fal works
with OAuth or a key; Replicate with an API key. Billing gets simpler, but
check each model's rate on that model's page.

## 3. Editing

| Tool | Connection | Scriptability |
|---|---|---|
| ffmpeg | Local CLI; no key, no account, no subscription | Fully scriptable; backbone of all renderers: cut, concat (demuxer without re-encode / filter with re-encode), audio mix (`sidechaincompress` for ducking, `loudnorm` for EBU R128), crop/zoom (`zoompan`/`crop`), subtitles (see §4), format conversion (`-pix_fmt yuv420p`) |
| Concat (app) | Local; built-in MCP server (`concat --mcp`) + JSON-RPC API + two `.claude/skills/` skills (`run-concat`, `study-editors`) | Agent control of the editor: project, import, cut, title, caption, keyframes, export |
| DaVinci Resolve | Local; no API key for scripting | Resolve Scripting API with `DaVinciResolveScript` on `fusionscript`; Python and Lua; ProjectManager, MediaPool, Timeline, Fusion comp, render queue; headless with `-nogui`. **Needs verification in Blackmagic docs:** one secondary report says Python was removed from the free version in 21.1 (Lua only) and Workflow Integrations / external scripting became Studio-only; official Resolve MCP added in 21.1 for Studio. Studio price reported as $295 vs $299 in different secondary sources. |

## 4. Captions / subtitles

- **Whisper** (OpenAI, open source, ~99 languages incl. Persian): SRT/VTT
  output. Local: `whisper.cpp`, `faster-whisper` (free, word timestamps);
  **WhisperX** adds precise word timestamps + RTL detection. Cloud: OpenAI
  Whisper API with API key. **Persian: use `large-v3`** — `small` breaks
  Persian (see `references/persian-rtl.md`).
- FFmpeg 8.0: a secondary source mentions a `whisper` filter for automatic
  subtitles — **not confirmed in the official FFmpeg docs; needs verification**.
- `drawtext`: **do not use for Persian** — no shaping, no bidi.
  `subtitles` / `ass` filter (libass): **the correct way** — libass does
  shaping and bidi.

## 5. How to connect a paid engine (checklist)

1. User creates the account and the API key themselves (never ask for the
   key in chat — use the platform's normal key flow).
2. Store the key in the environment (`export VEo_API_KEY=…` etc.) or the
   agent's secure credential flow — never in a file in the repo, never in
   a prompt, never in a log.
3. Run one cheap test call (shortest clip / smallest model) and confirm
   billing works before building the real video.
4. Record the model name, rate, and cost in the handoff
   (`templates/handoff.md`) so the user sees what the video cost.
