# Vox explainer — the full pipeline

This is the complete Vox-style mixed-media collage pipeline from the user's
prompt `PROMPT_VOX_EXPLAINER_31_dd6a.md` (30-second explainer about Mohammad
Mosaddegh, English + Persian versions). Swap the topic: change only
§1–§3 and the scene list (§7); the pipeline stays the same.

## 0. Tools

- Node.js + Playwright (render with the installed Chrome:
  `chromium.launch({channel:'chrome'})` if Chromium won't download)
- ffmpeg, Python 3 with: `numpy scipy soundfile librosa opencv-python pillow
  rembg edge-tts`
- Windows: `export PYTHONUTF8=1` (Persian text otherwise breaks Python
  file reads)

## 1. Content — no invented facts

1. Web-search the subject and confirm every fact against **at least two
   sources** (Britannica, Wikipedia, the National Security Archive at GWU,
   NPR…).
2. Facts used in the Mosaddegh video (example — verify again for any reuse):
   - Esfand 1329 / March 1951: the Majlis nationalized Iran's oil
     (the Anglo-Iranian Oil Company)
   - Britain answered with a worldwide boycott of Iranian oil and a Royal
     Navy blockade (the Abadan Crisis)
   - TIME named Mosaddegh Man of the Year 1951 (issue of 7 January 1952)
   - 28 Mordad 1332 / 19 August 1953: a coup removed him
   - 2013: declassified CIA documents admit the CIA directed the coup
   - 14 Esfand 1345 / 5 March 1967: died under house arrest in Ahmadabad,
     buried in his own home
3. Story shape (Vox): **hook → stakes → evidence → turn → kicker**,
   one through-line (oil → coup → legacy).

## 2. Script — 8 short phrases, numbers spelled out

| # | English | Persian |
|---|---|---|
| p1 | In nineteen fifty-one, Iran took its oil back from a British company. | اسفند ۱۳۲۹؛ ایران نفتش را از یک شرکت بریتانیایی پس گرفت. |
| p2 | The man who led it was Mohammad Mosaddegh. | رهبر این حرکت، محمد مصدق بود. |
| p3 | It cost him everything. | و بهایش، همه‌چیزِ او بود. |
| p4 | Britain answered with a boycott and a naval blockade. | بریتانیا با تحریم نفت و محاصره‌ی دریایی پاسخ داد. |
| p5 | TIME named him Man of the Year. | مجله‌ی تایم، او را مرد سال نامید. |
| p6 | Then, in August nineteen fifty-three, a coup removed him. | و در بیست‌وهشتم مرداد ۱۳۳۲، کودتا او را برکنار کرد. |
| p7 | Sixty years later, the CIA admitted it directed that coup. | شصت سال بعد، سیا پذیرفت که آن کودتا را هدایت کرده است. |
| p8 | Mosaddegh died under house arrest in nineteen sixty-seven, buried in his own home. | مصدق در سال ۱۳۴۵، در حبس خانگی درگذشت و در خانه‌ی خودش به خاک سپرده شد. |

## 3. Images — real archival, legal

- From **Wikimedia Commons** through its API
  (`action=query&prop=imageinfo&iiprop=url|size|extmetadata`). Keep only
  **Public domain / CC** files and write the license and author to
  `credits.json`.
- Space requests 3+ seconds apart (otherwise HTTP 429), and set a User-Agent.
- Files used in the example:
  - `Dr Mohammad Mosaddeq.jpg` (seated portrait)
  - `Portrait of Mohammad Mosaddegh - circa 1952.jpg`
  - `Mohammad Mosaddeq, Ahmadabad 1967.jpg`
  - `Abadan the city of Oil.jpg`
  - `1953 Iranian coup d'état - Tehran rally.jpg`
  - `Mohammad Mosaddegh in court martial by Ebrahim Golestan (3).jpg`
  - `Prime Minister Mohammad Mossadegh of Iran with Sr. Gladwyn Jebb.jpg`
    (United Nations, 1951)
- Map: **Natural Earth 1:50m countries** (public domain), cropped to the
  Middle East.

## 4. Making the collage assets (Python)

- **Paper backgrounds**, one colour per scene: yellow `#f6c448`, cream
  `#f2ece0`, navy `#1d2b45`, coral `#e9664e`. Add noise and fibres for a
  paper texture, plus a **halftone** dot layer.
- **Cut-outs**: `rembg` (model `isnet-general-use`) separates the person,
  then add a **rough white paper border** and a soft shadow.
- **Photo cards**: rectangular photos with torn white edges.
- **The torn portrait**: split the portrait along a jagged vertical line
  into two halves, each with a white torn edge (for "It cost him
  everything").
- **Flat map**: Iran in coral, neighbours light grey, sea transparent;
  Abadan and the Strait of Hormuz located in pixel coordinates.

## 5. Voice

- **edge-tts** (Microsoft neural voices, free):
  - English: `en-US-ChristopherNeural`, rate +4% (deep, measured
    documentary voice)
  - Persian: `fa-IR-FaridNeural`, rate +20% (Persian runs ~15% longer)
- Record each phrase as a separate take with `boundary='WordBoundary'` so
  the **timing of every word** is saved (`p1.words.json` …).
- Place the takes in a row with short breaths (0.3–0.5 s), with **the first
  word of each phrase on a quarter beat** of a 100 BPM grid → `vo.wav`.
- Persian: if it passes 31 s, raise the rate and shorten the breaths.

## 6. Timeline — everything tied to the voice

- The start of each phrase = the start of its scene (s1…s8). Then a title
  card for ~2.5 s.
- **Every visual impact sits on its spoken word** (from words.json):
  year tag → "1951"; label → "British"; strike-through → after the label;
  marker circle → "led"; name → "Mohammad"; tear → "everything";
  bars collapse → "boycott"; line + ships → "blockade";
  stamp → "Man of the Year"; date stamp → "August";
  trial photo → "removed"; redaction bars → "CIA";
  "Declassified" stamp → "admitted"; house drawing → "house";
  place tag → "1967".
- **Subtitles**: chunks of ≤ 18 characters (Persian ≤ 22), and the word
  being spoken is highlighted yellow (karaoke style). Never show two
  chunks at once.

## 7. Scenes — magazine collage, never a filmed scene

1. **Yellow**: "1951" year tag stamps on, the Abadan refinery card slides
   in, the "Anglo-Iranian Oil Co." label appears and gets struck through
   with marker.
2. **Cream**: the portrait pops in, a coral marker circle around the face,
   a yellow name strip + "Prime Minister of Iran". On "everything" the
   photo **tears in two** and the strips fall away.
3. **Navy**: the map slides up, Abadan pulses with a label, three export
   bars collapse. On "blockade" the **camera pushes into the Gulf of Oman**,
   a dashed blockade line draws on and three ships slide in.
4. **Coral**: the UN photo card + the 1952 portrait + a "Man of the Year ·
   TIME 1951" stamp with a yellow underline.
5. **Cream**: the Tehran rally photo, a red stamp "19 Aug 1953"
   (۲۸ مرداد ۱۳۳۲), the trial photo on "removed".
6. **Yellow**: "Sixty years later" types on, a CIA document whose lines are
   covered one by one with black redaction bars, a "Declassified · 2013"
   stamp.
7. **Cream**: the 1967 Ahmadabad cut-out, a hand-drawn house drawn around
   it, an "Ahmadabad · 1967" tag.
8. **Navy title card**: small portrait, big name, "Prime Minister of Iran ·
   1951–1953", underline, photo credit.

**Motion rules:** whip-pan between scenes (never a crossfade); a slow
push-in inside each scene; everything enters with **springs** (stamps slam
in from 1.6× scale, cards arrive with a little overshoot, strips are laid
down like tape); something new happens every 2–3 seconds; film grain on
top of everything.

**Fonts:** English **Anton** (headlines/subtitles) + **Montserrat** (small
text); Persian **Vazirmatn** with the `arabic` subset.

**Persian layout:** set `direction: rtl` on the stage, otherwise multi-word
lines and dates come out reversed. Right-align the labels.

## 8. Music — synthesized in code, epic and rhythmic

- 100 BPM, D minor, chords one per bar: **Dm – Bb – Gm – A**
- **Instruments:** fast spiccato strings in 16th notes (detuned saw, short
  envelope); taiko (low drum with a pitch drop); tom fill every two bars;
  kick on every beat + snare on 2 and 4; 16th-note hi-hats; 8th-note octave
  bass; brass stabs at the top of each bar; pad underneath.
- **Sections:** intro (strings + taiko building); full from scene 2; build
  with a snare roll before "sixty years later"; full again; big hit + held
  chord on the title.
- **A taiko boom + crash at the start of every scene.**

Calmer variant: vox/ticking style (clock ticks + soft pulse). More energy:
the epic style above.

## 9. Sound effects — synthesized, each on its picture event

- paper slide (`paper`), paper tear (`rip`) on "everything", marker
  drawing (`marker`), rubber stamp (`stamp`), small pops (`pop`), typing
  (`key`), whoosh on scene changes, impact on the title.

## 10. Mix and render

- Music −2 dB, SFX −4 dB, voice 0, with **the music ducked** (sidechain)
  under the voice.
- Whole mix at **−14 LUFS**, true peak ≤ −1 dBTP.
- Warning: ffmpeg's `sidechaincompress` drops the last few frames. Pad the
  inputs by 1 s and trim back to the exact length after mixing.
- The video is a pure function of time (`seek(t)`). Render with headless
  Chrome at 60 fps with motion blur, then **H.264 yuv420p CRF 16**.

## 11. Review before the final render (max 2 rounds)

- One frame per beat as a contact sheet + full-size stills of the risky
  moments (tear, blockade, stamps).
- Check: anything outside the frame? Subtitles overlapping? Persian
  reading direction right? Every impact on its word? Anything empty in
  the first 2 seconds?

## 12. Deliverables

- `mosaddegh-vox_EN_9x16.mp4`, `mosaddegh-vox_FA_9x16.mp4`
- `SOURCES.md`: bilingual script + fact sources + license/author of every
  image + voice names

## Reuse notes

- **A different topic**: change only §1–§3 and the scene list (§7).
- **More languages**: one edge-tts voice per language, its own subtitle
  font, and right-to-left layout if needed.
- **No AI video or image generation** in this pipeline (no Higgsfield,
  Runway, or Midjourney). Everything is real archival images plus code.
