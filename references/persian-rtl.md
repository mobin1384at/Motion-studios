# Persian / RTL — the mandatory rules

**Read this file before any task involving Persian text. It is mandatory,
not optional.** Sources: persian-reel (MIT), claude-motion-studio (MIT),
AE-Whisper-Captions (MIT), and the user's own Lalezar reel prompt and
VOX explainer prompt.

## 1. The golden rule

Persian subtitles **only** via **libass + Vazirmatn font + RLI/PDI isolates**.

```bash
ffmpeg -i input.mp4 -vf subtitles=subs.srt out.mp4
```

For styled / coloured / positioned captions, convert SRT to ASS first.
libass does shaping and bidi correctly.

**NEVER `ffmpeg drawtext` for Persian.** It does not shape Arabic-script
lines and does not do bidi: letters render disconnected and reversed.

## 2. The four persian-reel traps

| # | Trap | Rule |
|---|---|---|
| 1 | `<html dir="rtl">` renders the video **completely black** | Never put `dir="rtl"` on the render-stage `<html>`. Set `direction: rtl` on the **stage element** only (Vox pattern), or handle RTL in the drawing code (Pillow: `direction='rtl'`). |
| 2 | Negative `letter-spacing` closes Persian word gaps | Never use negative `letter-spacing` on Persian text. |
| 3 | Persian zero "۰" renders as a dot | Check every "۰" in the final render; if it breaks, replace the rendering path (font / renderer) and re-check. |
| 4 | Whisper `small` model breaks Persian | Use Whisper `large-v3` for Persian (faster-whisper or WhisperX). `small` is not acceptable for Persian. |

## 3. Fonts and shaping

- **Vazirmatn** — source `rastikerdar/vazirmatn`, family name `Vazirmatn`.
  Install in `~/.fonts/vazir/`; verify with `fc-list :lang=fa`.
  Emergency fallback: Tahoma.
- **Lalezar** — the display font for Persian reel captions
  (see `references/persian-reel-style.md`). The user attaches
  `Lalezar-Regular.ttf`; if it is not attached, stop and ask — do not continue
  with a default font.
- Shaping before drawing into a static PDF/image: `arabic_reshaper.reshape()`
  + `python-bidi get_display()`, then embed the TTF. `fpdf2` and raw
  `pymupdf insert_text` do **not** shape.
- Pillow: `ImageDraw.text(..., direction='rtl', language='fa')` with libraqm;
  verify with `features.check('raqm')`. Fallback: `arabic_reshaper` +
  `python-bidi`. Never draw Persian text without shaping.

## 4. Bidi isolates

- Mixed Persian + English lines: wrap each Persian run in a **bidi isolate**:
  `RLI … PDI` (isolating; preferred over RLE — VLC/mpv/fribidi honour it).
- Punctuation: use the RLM character (`\u200F`).
- In DOCX/PPTX: RTL must be set at run level (`w:rtl=1` + `w:lang=fa-IR` +
  CS font); paragraph-level `w:bidi` alone is not enough.
- SRT/ASS cues must not overlap — overlapping cues cause vertical jitter
  in libass.
- Persian layout in HTML stages: set `direction: rtl` on the stage,
  right-align labels. Otherwise multi-word lines and dates come out reversed.

## 5. Captions — word by word, never letter by letter

- Persian captions are **word-by-word** (claude-motion-studio Arabic/RTL
  pattern). Never animate letter-by-letter: letters in a word are shaped
  together and splitting them breaks the word.
- Put an English term inside its own chip, separate from the Persian line.
- Caption chunks: ≤ 22 characters for Persian (≤ 18 for English).
- Never show two chunks at once. The spoken word is highlighted (karaoke).

## 6. Voice and timing

- Persian voice: ElevenLabs v3/v4 or Azure/edge-tts `fa-IR-DilaraNeural` /
  `fa-IR-FaridNeural`. See `references/sound.md` §2 for the honest table.
- Persian runs ~15% longer than English — plan timing for it.
- Whisper `large-v3` for Persian transcription (see trap 4 above).
- WhisperX adds precise word timestamps + RTL detection.

## 7. VOX Persian layout notes

From the user's VOX explainer prompt (`PROMPT_VOX_EXPLAINER_31_dd6a.md`):

- Set `direction: rtl` on the stage, otherwise multi-word lines and dates
  come out reversed. Right-align the labels.
- Persian font: **Vazirmatn** with the `arabic` subset.
- Persian voice: `fa-IR-FaridNeural`, rate +20%.
- Subtitle chunks ≤ 22 characters; spoken word highlighted yellow.
- If the Persian version passes 31 s, raise the rate and shorten breaths.

## 8. Lalezar font notes

From the user's Lalezar reel prompt (`claude_video_edit_prompt_29_mwjn.md`):

- **Lalezar** for all Persian text; DejaVu Sans Bold for small Latin labels.
- If the Lalezar file is not attached, tell the user and do not continue.
- Full workflow: `references/persian-reel-style.md`.
