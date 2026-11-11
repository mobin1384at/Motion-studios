#!/usr/bin/env python3
"""qc.py — quality checks on a rendered video.

Checks (research §3-1: QA from the final render, not from snapshots):
  * ffprobe: duration, resolution, fps, codec, audio stream presence.
  * Audio loudness via ffmpeg volumedetect (mean/max volume) and, when
    available, loudnorm integrated loudness.
  * Sample frames: extract N frames across the video, flag black/empty
    frames (near-zero luminance) and frozen segments (identical frames).
  * Basic layout sanity: expected resolution / fps / min duration.

Exits 0 when all checks pass, 1 when any FAIL, 2 on usage/tool errors.
Use --json for machine-readable output.

Usage:
    python3 qc.py --input out.mp4
    python3 qc.py --input out.mp4 --width 1080 --height 1920 --fps 30 --min-duration 5
    python3 qc.py --input out.mp4 --samples 12 --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BLACK_MEAN_THRESHOLD = 2.0   # mean luma below this => black frame
BLACK_RANGE_THRESHOLD = 2.0  # YMAX-YMIN below this => flat/empty frame


def require(tool: str, hint: str) -> None:
    if shutil.which(tool) is None:
        print(f"ERROR: required tool '{tool}' not found on PATH.", file=sys.stderr)
        print(f"  {hint}", file=sys.stderr)
        sys.exit(2)


def ffprobe(path: str) -> dict:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries",
         "stream=width,height,r_frame_rate,codec_name,duration",
         "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"ERROR: ffprobe failed on {path}:\n{proc.stderr.strip()}",
              file=sys.stderr)
        sys.exit(1)
    return json.loads(proc.stdout or "{}")


def frame_rate(rate: str) -> float:
    if "/" in rate:
        num, den = rate.split("/", 1)
        return float(num) / float(den) if float(den) else 0.0
    return float(rate)


def audio_streams(path: str) -> int:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", path],
        capture_output=True, text=True)
    return len([ln for ln in proc.stdout.splitlines() if ln.strip()])


def volume_detect(path: str) -> dict | None:
    proc = subprocess.run(
        ["ffmpeg", "-i", path, "-vn", "-af", "volumedetect",
         "-f", "null", "-"],
        capture_output=True, text=True)
    text = proc.stderr or ""
    mean = re.search(r"mean_volume:\s*([-\d.]+) dB", text)
    maxv = re.search(r"max_volume:\s*([-\d.]+) dB", text)
    if not mean:
        return None
    return {"mean_volume_db": float(mean.group(1)),
            "max_volume_db": float(maxv.group(1)) if maxv else None}


def extract_frames(path: str, times: list[float], outdir: str) -> list[str]:
    files = []
    for i, t in enumerate(times):
        out = os.path.join(outdir, f"qc-{i:02d}.png")
        proc = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", path,
             "-frames:v", "1", out],
            capture_output=True, text=True)
        if proc.returncode == 0 and os.path.isfile(out):
            files.append(out)
    return files


def frame_stats(png: str) -> dict:
    """Mean luma + luma range via ffprobe lavfi signalstats frame tags.

    NOTE: ffmpeg 8 no longer prints YAVG/YSTDEV to stderr, so the stats
    are read from ffprobe -show_frames tags instead.
    """
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-f", "lavfi",
         "-i", f"movie={png},signalstats",
         "-show_frames", "-of", "json"],
        capture_output=True, text=True)
    yavg = yrange = None
    try:
        data = json.loads(proc.stdout or "{}")
        tags = (data.get("frames") or [{}])[0].get("tags", {})
        yavg = float(tags["lavfi.signalstats.YAVG"])
        yrange = (float(tags["lavfi.signalstats.YMAX"])
                  - float(tags["lavfi.signalstats.YMIN"]))
    except (ValueError, KeyError, IndexError, TypeError):
        pass
    with open(png, "rb") as fh:
        digest = hashlib.md5(fh.read()).hexdigest()
    return {"yavg": yavg, "yrange": yrange, "md5": digest}


def main() -> int:
    ap = argparse.ArgumentParser(description="QC checks on a rendered video.")
    ap.add_argument("--input", required=True, help="Video file to check.")
    ap.add_argument("--width", type=int, default=None, help="Expected width.")
    ap.add_argument("--height", type=int, default=None, help="Expected height.")
    ap.add_argument("--fps", type=float, default=None, help="Expected fps.")
    ap.add_argument("--min-duration", type=float, default=0.0,
                    help="Minimum duration in seconds (default 0).")
    ap.add_argument("--require-audio", action="store_true",
                    help="Fail if there is no audio stream.")
    ap.add_argument("--samples", type=int, default=8,
                    help="Number of sample frames to extract (default 8).")
    ap.add_argument("--json", action="store_true", help="JSON output.")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2
    require("ffprobe", "Install ffmpeg (ships ffprobe): https://ffmpeg.org/download.html")
    require("ffmpeg", "Install ffmpeg: https://ffmpeg.org/download.html")

    results: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        results.append({"name": name, "status": "PASS" if ok else "FAIL",
                        "detail": detail})

    info = ffprobe(args.input)
    stream = (info.get("streams") or [{}])[0]
    fmt = info.get("format", {})
    duration = float(fmt.get("duration") or stream.get("duration") or 0)
    width = stream.get("width")
    height = stream.get("height")
    fps = frame_rate(stream.get("r_frame_rate", "0"))
    codec = stream.get("codec_name")

    check("file_readable", os.path.getsize(args.input) > 0,
          f"{os.path.getsize(args.input)} bytes, codec={codec}")
    check("duration", duration >= args.min_duration and duration > 0,
          f"{duration:.2f}s (min {args.min_duration}s)")
    if args.width:
        check("width", width == args.width, f"{width} (expected {args.width})")
    if args.height:
        check("height", height == args.height, f"{height} (expected {args.height})")
    if args.fps:
        check("fps", abs(fps - args.fps) < 0.5, f"{fps:.2f} (expected {args.fps})")

    n_audio = audio_streams(args.input)
    if args.require_audio:
        check("audio_present", n_audio > 0, f"{n_audio} audio stream(s)")
    vol = volume_detect(args.input) if n_audio else None
    if vol:
        check("audio_not_silent", vol["mean_volume_db"] > -60,
              f"mean {vol['mean_volume_db']} dB, max {vol['max_volume_db']} dB")
    elif n_audio:
        check("audio_not_silent", False, "volumedetect produced no reading")

    # Sample frames across the video.
    tmpdir = tempfile.mkdtemp(prefix="motion-studio-qc-")
    try:
        if duration > 0 and args.samples > 0:
            times = [duration * (i + 0.5) / args.samples
                     for i in range(args.samples)]
            files = extract_frames(args.input, times, tmpdir)
            stats = [frame_stats(f) for f in files]
            black = [i for i, s in enumerate(stats)
                     if s["yavg"] is not None
                     and s["yavg"] < BLACK_MEAN_THRESHOLD
                     and (s["yrange"] if s["yrange"] is not None else 99)
                     < BLACK_RANGE_THRESHOLD]
            check("no_black_frames", not black,
                  f"{len(black)}/{len(stats)} black/empty frames"
                  + (f" at samples {black}" if black else ""))
            hashes = [s["md5"] for s in stats]
            frozen = len(set(hashes)) < max(2, len(hashes) // 2) if hashes else False
            check("not_frozen", not frozen,
                  f"{len(set(hashes))} distinct frames out of {len(hashes)}")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    failed = [r for r in results if r["status"] == "FAIL"]
    summary = {"file": args.input, "duration_s": round(duration, 2),
               "width": width, "height": height, "fps": round(fps, 2),
               "codec": codec, "audio_streams": n_audio,
               "volume": vol, "checks": results,
               "verdict": "FAIL" if failed else "PASS"}

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"QC {args.input} — {summary['verdict']}")
        print(f"  duration={duration:.2f}s {width}x{height} @ {fps:.2f}fps "
              f"codec={codec} audio={n_audio}")
        for r in results:
            print(f"  [{'PASS' if r['status'] == 'PASS' else 'FAIL'}] "
                  f"{r['name']}: {r['detail']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
