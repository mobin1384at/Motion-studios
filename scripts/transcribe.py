#!/usr/bin/env python3
"""transcribe.py — transcribe audio/video to word-level SRT/JSON.

Uses faster-whisper (local, free) when installed; otherwise fails with a
clear install instruction instead of pretending to transcribe.

Persian note (research §4-5): use model `large-v3` for Persian — the
`small` model corrupts Persian. Default language is `fa`; pass --language
for other languages.

Usage:
    python3 transcribe.py --input voice.mp3 --output subs.srt [--model large-v3]
    python3 transcribe.py --input voice.mp3 --output words.json --format json
    python3 transcribe.py --input voice.mp3 --output subs.srt --language en --model base
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys


def srt_time(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def check_ffmpeg_for_video(path: str) -> str:
    """If input is a video container, extract its audio to a temp wav."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".mp4", ".mov", ".mkv", ".webm", ".avi"):
        if shutil.which("ffmpeg") is None:
            print("ERROR: input is a video file and ffmpeg is not installed; "
                  "cannot extract audio.", file=sys.stderr)
            sys.exit(2)
        tmp = path + ".audio.wav"
        proc = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", path, "-vn",
             "-ac", "1", "-ar", "16000", tmp],
            capture_output=True, text=True)
        if proc.returncode != 0 or not os.path.isfile(tmp):
            print(f"ERROR: ffmpeg could not extract audio from {path}:\n"
                  f"{proc.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        return tmp
    return path


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Transcribe audio to word-level SRT/JSON with faster-whisper."
    )
    ap.add_argument("--input", required=True, help="Audio or video file.")
    ap.add_argument("--output", required=True, help="Output .srt or .json file.")
    ap.add_argument("--model", default="large-v3",
                    help="Whisper model (default large-v3; use large-v3 for Persian).")
    ap.add_argument("--language", default="fa",
                    help="Language code, e.g. fa, en (default fa).")
    ap.add_argument("--format", choices=["srt", "json"], default="srt",
                    help="Output format (default srt).")
    ap.add_argument("--device", default="cpu",
                    help="faster-whisper device: cpu or cuda (default cpu).")
    ap.add_argument("--compute-type", default="int8",
                    help="faster-whisper compute type (default int8).")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR: faster-whisper is not installed.", file=sys.stderr)
        print("  Install it with:  pip install faster-whisper", file=sys.stderr)
        print("  (First run downloads the model; large-v3 is ~3 GB.)",
              file=sys.stderr)
        return 2

    audio = check_ffmpeg_for_video(args.input)
    tmp_created = audio != args.input

    print(f"Transcribing {args.input} with model={args.model} "
          f"language={args.language} ...", file=sys.stderr)
    try:
        model = WhisperModel(args.model, device=args.device,
                             compute_type=args.compute_type)
        segments, _info = model.transcribe(audio, language=args.language,
                                           word_timestamps=True)
        segments = list(segments)
    except Exception as exc:  # model download / device errors
        print(f"ERROR: transcription failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if tmp_created and os.path.isfile(audio):
            os.remove(audio)

    if not segments:
        print("ERROR: transcription produced no segments — check the audio "
              "file is not silent/empty.", file=sys.stderr)
        return 1

    if args.format == "json":
        data = [{
            "start": s.start, "end": s.end, "text": s.text.strip(),
            "words": [{"word": w.word, "start": w.start, "end": w.end,
                       "probability": w.probability}
                      for w in (s.words or [])],
        } for s in segments]
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    else:
        lines: list[str] = []
        for i, seg in enumerate(segments, 1):
            lines.append(str(i))
            lines.append(f"{srt_time(seg.start)} --> {srt_time(seg.end)}")
            lines.append(seg.text.strip())
            lines.append("")
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))

    words = sum(len(s.words or []) for s in segments)
    print(f"OK: {len(segments)} segments, {words} words -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
