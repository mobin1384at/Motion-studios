#!/usr/bin/env python3
"""check_cuts.py — prove cuts from the FINAL render.

For each cut time, extract the frame just after the cut and verify:
  * it is not black/empty, and
  * it differs from the previous cut's frame (the cut actually changed
    the picture — a cut to an identical frame is a no-op).

This is the video-edit-skill pattern: cuts are proven from rendered
frames, never assumed from the edit decision list.

Usage:
    python3 check_cuts.py --input final.mp4 --cuts 2.5 7.0 12.3
    python3 check_cuts.py --input final.mp4 --cuts-file cuts.txt   # one time per line
    python3 check_cuts.py --input final.mp4 --cuts 2.5 7.0 --epsilon 0.05 --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

BLACK_MEAN_THRESHOLD = 2.0
BLACK_RANGE_THRESHOLD = 2.0  # YMAX-YMIN below this => flat/empty frame


def frame_at(path: str, t: float, outdir: str, tag: str) -> str | None:
    out = os.path.join(outdir, f"cut-{tag}.png")
    proc = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", path,
         "-frames:v", "1", out],
        capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.isfile(out):
        return None
    return out


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


def duration_of(path: str) -> float:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True)
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verify cuts from the final render: each cut frame must "
                    "be non-black and different from the previous cut frame.")
    ap.add_argument("--input", required=True, help="Final rendered video.")
    ap.add_argument("--cuts", type=float, nargs="*", default=[],
                    help="Cut times in seconds.")
    ap.add_argument("--cuts-file", default=None,
                    help="File with one cut time per line.")
    ap.add_argument("--epsilon", type=float, default=0.05,
                    help="Seconds after the cut to sample (default 0.05).")
    ap.add_argument("--json", action="store_true", help="JSON output.")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("ERROR: ffmpeg/ffprobe not found on PATH.", file=sys.stderr)
        print("  Install ffmpeg: https://ffmpeg.org/download.html", file=sys.stderr)
        return 2

    cuts = list(args.cuts)
    if args.cuts_file:
        if not os.path.isfile(args.cuts_file):
            print(f"ERROR: cuts file not found: {args.cuts_file}", file=sys.stderr)
            return 2
        with open(args.cuts_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        cuts.append(float(line))
                    except ValueError:
                        print(f"ERROR: bad cut time in {args.cuts_file}: {line!r}",
                              file=sys.stderr)
                        return 2
    if not cuts:
        print("ERROR: no cut times given (--cuts or --cuts-file).", file=sys.stderr)
        return 2
    cuts = sorted(set(cuts))
    if any(c < 0 for c in cuts):
        print("ERROR: cut times must be >= 0.", file=sys.stderr)
        return 2

    total = duration_of(args.input)
    if total > 0 and max(cuts) >= total:
        print(f"ERROR: cut {max(cuts)}s is beyond video duration {total:.2f}s.",
              file=sys.stderr)
        return 2

    tmpdir = tempfile.mkdtemp(prefix="motion-studio-cuts-")
    results: list[dict] = []
    try:
        prev_md5: str | None = None
        for i, cut in enumerate(cuts):
            t = cut + args.epsilon
            png = frame_at(args.input, t, tmpdir, f"{i:02d}")
            if png is None:
                results.append({"cut": cut, "status": "FAIL",
                                "detail": f"could not extract frame at {t:.2f}s"})
                continue
            st = frame_stats(png)
            black = (st["yavg"] is not None
                     and st["yavg"] < BLACK_MEAN_THRESHOLD
                     and (st["yrange"] if st["yrange"] is not None else 99)
                     < BLACK_RANGE_THRESHOLD)
            same = prev_md5 is not None and st["md5"] == prev_md5
            if black:
                status, detail = "FAIL", f"frame at {t:.2f}s is black/empty (YAVG={st['yavg']})"
            elif same:
                status, detail = "FAIL", (f"frame at {t:.2f}s is identical to the "
                                          "previous cut frame — cut changed nothing")
            else:
                status, detail = "PASS", f"frame at {t:.2f}s OK (YAVG={st['yavg']})"
            results.append({"cut": cut, "status": status, "detail": detail})
            prev_md5 = st["md5"]
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    failed = [r for r in results if r["status"] == "FAIL"]
    if args.json:
        print(json.dumps({"file": args.input, "cuts": results,
                          "verdict": "FAIL" if failed else "PASS"},
                         indent=2, ensure_ascii=False))
    else:
        print(f"check_cuts {args.input} — {'FAIL' if failed else 'PASS'}")
        for r in results:
            print(f"  [{r['status']}] cut {r['cut']}s: {r['detail']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
