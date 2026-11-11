#!/usr/bin/env python3
"""mix.py — mix voice + music/SFX and master to -14 LUFS.

Pipeline (research §3-1, §4-3):
  1. Pad every input with 1s of silence FIRST — ffmpeg's
     sidechaincompress drops trailing frames, so unpadded audio loses its
     tail. Trim the 1s back off at the end.
  2. Duck the music under the voice with sidechaincompress (music ~4-6 dB
     under speech), then loudnorm the mix to -14 LUFS (EBU R128,
     the motion-video standard: -14 LUFS, -1 dBTP ceiling).

Usage:
    python3 mix.py --voice voice.mp3 --music music.mp3 --output final.wav
    python3 mix.py --voice voice.mp3 --music music.mp3 --sfx sfx.mp3 --output final.mp3
    python3 mix.py --voice voice.mp3 --output final.wav   # voice only, loudnorm
    python3 mix.py --voice voice.mp3 --music music.mp3 --output final.mp3 --target-lufs -14
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

TARGET_LUFS = -14.0
TRUE_PEAK = -1.0


def require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print("ERROR: ffmpeg not found on PATH.", file=sys.stderr)
        print("  Install it: https://ffmpeg.org/download.html", file=sys.stderr)
        sys.exit(2)


def ffprobe_duration(path: str) -> float:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True)
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return 0.0


def run_ffmpeg(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("ERROR: ffmpeg failed:", file=sys.stderr)
        print("  " + " ".join(cmd), file=sys.stderr)
        print(proc.stderr.strip()[-2000:], file=sys.stderr)
        sys.exit(1)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Mix voice + music/SFX with ducking and master to -14 LUFS.")
    ap.add_argument("--voice", required=True, help="Narration/voice audio file.")
    ap.add_argument("--music", default=None, help="Background music file.")
    ap.add_argument("--sfx", default=None, help="SFX file (mixed at full level).")
    ap.add_argument("--output", required=True, help="Output audio file.")
    ap.add_argument("--target-lufs", type=float, default=TARGET_LUFS,
                    help="Integrated loudness target (default -14).")
    ap.add_argument("--music-duck-db", type=float, default=6.0,
                    help="How far music ducks under voice, in dB (default 6).")
    ap.add_argument("--keep-temp", action="store_true",
                    help="Keep intermediate files (debugging).")
    args = ap.parse_args()

    require_ffmpeg()
    for label, path in (("voice", args.voice), ("music", args.music),
                        ("sfx", args.sfx)):
        if path and not os.path.isfile(path):
            print(f"ERROR: {label} file not found: {path}", file=sys.stderr)
            return 2

    # Temp files live next to the output (not /tmp, which may be small/full).
    out_dir = os.path.dirname(os.path.abspath(args.output)) or "."
    tmpdir = tempfile.mkdtemp(prefix="motion-studio-mix-", dir=out_dir)
    try:
        # Step 1: pad each input with 1s silence at the START (adelay) and
        # 1s at the END (apad=pad_dur=1, BOUNDED — plain apad pads forever).
        # sidechaincompress drops trailing frames, so the tail pad protects
        # the real audio; both pads are trimmed back off below.
        padded = {}
        for label, path in (("voice", args.voice), ("music", args.music),
                            ("sfx", args.sfx)):
            if not path:
                continue
            out = os.path.join(tmpdir, f"{label}-padded.wav")
            run_ffmpeg(["ffmpeg", "-y", "-v", "error", "-i", path,
                        "-af", "adelay=1000|1000,apad=pad_dur=1",
                        "-ac", "2", "-ar", "48000", out])
            padded[label] = out

        # Step 2: build the filter graph.
        #   [0:a] voice (sidechain source), [1:a] music (ducked), [2:a] sfx.
        inputs = [padded["voice"]]
        labels = ["[0:a]"]
        if "music" in padded:
            inputs.append(padded["music"])
            labels.append("[1:a]")
        if "sfx" in padded:
            inputs.append(padded["sfx"])
            labels.append("[2:a]")

        filters: list[str] = []
        mix_inputs: list[str] = ["[voice]"]
        # Voice passthrough. NOTE: the label must NOT be [v] — ffmpeg
        # interprets [v] as the video-stream specifier and the graph
        # fails to bind. [voice] is safe.
        filters.append(f"{labels[0]}anull[voice]")
        idx = 1
        if "music" in padded:
            # sidechaincompress: voice is the sidechain, music is ducked.
            ratio = 10 ** (args.music_duck_db / 20.0)
            filters.append(
                f"[1:a][voice]sidechaincompress=threshold=0.05:ratio={ratio:.1f}:"
                f"attack=50:release=400[ducked]")
            mix_inputs.append("[ducked]")
            idx += 1
        if "sfx" in padded:
            sfx_label = f"[{idx}:a]"
            filters.append(f"{sfx_label}anull[sfx]")
            mix_inputs.append("[sfx]")

        filters.append(
            f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:"
            f"normalize=0[mixed]")
        # loudnorm (single pass; two-pass is more accurate but single-pass
        # is the documented skill default — see --help note).
        filters.append(
            f"[mixed]loudnorm=I={args.target_lufs}:TP={TRUE_PEAK}:LRA=11"
            f"[normed]")
        # Trim the 1s START pad added in step 1 (the tail pad is trimmed
        # in step 3, after measuring the intermediate duration).
        filters.append("[normed]atrim=start=1.0,asetpts=PTS-STARTPTS[out]")

        # Step 2 result goes to an intermediate file (start pad already
        # trimmed by the atrim filter); the 1s tail pad is trimmed in step 3.
        intermediate = os.path.join(tmpdir, "mixed-tmp.wav")
        cmd = ["ffmpeg", "-y", "-v", "error"]
        for path in inputs:
            cmd += ["-i", path]
        ext = os.path.splitext(args.output)[1].lower()
        codec = {".mp3": "libmp3lame", ".m4a": "aac", ".aac": "aac"}.get(
            ext, "pcm_s16le")
        cmd += ["-filter_complex", ";".join(filters),
                "-map", "[out]", "-c:a", "pcm_s16le", intermediate]
        run_ffmpeg(cmd)

        # Step 3: trim the 1s tail pad (measure, then cut).
        dur = ffprobe_duration(intermediate)
        if dur <= 1.0:
            print(f"ERROR: mixed intermediate is too short ({dur}s).",
                  file=sys.stderr)
            return 1
        run_ffmpeg(["ffmpeg", "-y", "-v", "error", "-i", intermediate,
                    "-t", f"{dur - 1.0:.3f}", "-c:a", codec, args.output])
    finally:
        if not args.keep_temp:
            shutil.rmtree(tmpdir, ignore_errors=True)
        else:
            print(f"Temp files kept in {tmpdir}", file=sys.stderr)

    if not os.path.isfile(args.output) or os.path.getsize(args.output) == 0:
        print(f"ERROR: mix produced no output: {args.output}", file=sys.stderr)
        return 1
    print(f"OK: mixed -> {args.output} (target {args.target_lufs} LUFS, "
          f"music ducked {args.music_duck_db} dB under voice)")
    print("NOTE: single-pass loudnorm is used; for broadcast-accurate "
          "mastering run ffmpeg loudnorm in two passes (see references/sound.md).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
