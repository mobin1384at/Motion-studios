#!/usr/bin/env python3
"""render.py — render router for the motion-studio skill.

Routes a render request to the right engine and prints (or runs) the
exact commands. Engines (see references/engines.md):
  hyperframes  HTML/CSS/JS scene -> capture.mjs (headless Chrome) + ffmpeg
  remotion     React/TypeScript project -> `npx remotion render`
  manim        Python Scene class -> `manim -pqh`
  cinecode     single film.html -> capture.mjs + ffmpeg

Never pretends success: every external tool is checked with shutil.which
before use, and a missing tool aborts with install instructions.

Usage:
    python3 render.py --engine hyperframes --input scene.html --output out.mp4
    python3 render.py --engine remotion --input ./my-video --output out.mp4
    python3 render.py --engine manim --input anim.py --scene MyScene --output out.mp4
    python3 render.py --engine cinecode --input film.html --output out.mp4
    python3 render.py --engine hyperframes --input scene.html --dry-run
    python3 render.py --engine hyperframes --input scene.html --fps 30 --width 1080 --height 1920
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.join(HERE, "capture.mjs")

ENGINES = ("hyperframes", "remotion", "manim", "cinecode")


def require(tool: str, hint: str) -> str:
    path = shutil.which(tool)
    if path is None:
        print(f"ERROR: required tool '{tool}' not found on PATH.", file=sys.stderr)
        print(f"  {hint}", file=sys.stderr)
        sys.exit(2)
    return path


def build_commands(args: argparse.Namespace) -> list[list[str]]:
    """Return the exact command list for this render (no execution)."""
    out = args.output
    if args.engine in ("hyperframes", "cinecode"):
        if not os.path.isfile(args.input):
            print(f"ERROR: input HTML file not found: {args.input}", file=sys.stderr)
            sys.exit(2)
        if not os.path.isfile(CAPTURE):
            print(f"ERROR: capture.mjs not found next to render.py: {CAPTURE}",
                  file=sys.stderr)
            sys.exit(2)
        cmd = [
            "node", CAPTURE,
            "--input", args.input,
            "--output", out,
            "--fps", str(args.fps),
            "--width", str(args.width),
            "--height", str(args.height),
            "--duration", str(args.duration),
        ]
        if args.start is not None:
            cmd += ["--start", str(args.start)]
        return [cmd]
    if args.engine == "remotion":
        if not os.path.isdir(args.input):
            print(f"ERROR: Remotion project directory not found: {args.input}",
                  file=sys.stderr)
            sys.exit(2)
        return [[
            "npx", "remotion", "render", args.input,
            args.composition or "Main",
            out,
            "--fps", str(args.fps),
            "--width", str(args.width),
            "--height", str(args.height),
        ]]
    if args.engine == "manim":
        if not os.path.isfile(args.input):
            print(f"ERROR: input Python file not found: {args.input}", file=sys.stderr)
            sys.exit(2)
        if not args.scene:
            print("ERROR: --scene is required for --engine manim "
                  "(the Scene class name).", file=sys.stderr)
            sys.exit(2)
        quality = {"1080p": "-pqh", "720p": "-pqm", "480p": "-pql"}.get(
            args.quality, "-pqh")
        return [[
            "manim", quality, args.input, args.scene,
            "-o", os.path.basename(out),
            "--media_dir", os.path.dirname(os.path.abspath(out)) or ".",
        ]]
    print(f"ERROR: unknown engine: {args.engine}", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Route a render to hyperframes / remotion / manim / cinecode."
    )
    ap.add_argument("--engine", required=True, choices=ENGINES,
                    help="Render engine.")
    ap.add_argument("--input", required=True,
                    help="HTML file (hyperframes/cinecode), project dir (remotion), "
                         "or .py file (manim).")
    ap.add_argument("--output", required=True, help="Output MP4 path.")
    ap.add_argument("--scene", default=None,
                    help="Manim Scene class name (manim only).")
    ap.add_argument("--composition", default=None,
                    help="Remotion composition id (default: Main).")
    ap.add_argument("--fps", type=int, default=30, help="Frames per second (default 30).")
    ap.add_argument("--width", type=int, default=1080, help="Width px (default 1080).")
    ap.add_argument("--height", type=int, default=1920, help="Height px (default 1920).")
    ap.add_argument("--duration", type=float, default=10.0,
                    help="Duration in seconds for HTML engines (default 10).")
    ap.add_argument("--start", type=float, default=None,
                    help="Start time in seconds for HTML engines (default 0).")
    ap.add_argument("--quality", default="1080p", choices=["480p", "720p", "1080p"],
                    help="Manim quality preset (default 1080p).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the exact commands and exit without running them.")
    args = ap.parse_args()

    if args.fps <= 0 or args.width <= 0 or args.height <= 0 or args.duration <= 0:
        print("ERROR: --fps, --width, --height and --duration must be > 0.",
              file=sys.stderr)
        return 2

    commands = build_commands(args)

    if args.dry_run:
        print("DRY RUN — commands that would be executed:")
        for cmd in commands:
            print("  " + " ".join(cmd))
        return 0

    # Pre-flight: check the external tool for the chosen engine exists.
    if args.engine in ("hyperframes", "cinecode"):
        require("node", "Install Node.js 20+ from https://nodejs.org")
        require("ffmpeg", "Install ffmpeg: https://ffmpeg.org/download.html")
    elif args.engine == "remotion":
        require("npx", "Install Node.js 20+ from https://nodejs.org")
    elif args.engine == "manim":
        require("manim", "pip install manim  (also needs ffmpeg + LaTeX for formulas)")

    for cmd in commands:
        print("RUN: " + " ".join(cmd))
        proc = subprocess.run(cmd)
        if proc.returncode != 0:
            print(f"ERROR: command failed with exit code {proc.returncode}: "
                  f"{cmd[0]}", file=sys.stderr)
            return proc.returncode

    if os.path.isfile(args.output) and os.path.getsize(args.output) > 0:
        print(f"OK: wrote {args.output} "
              f"({os.path.getsize(args.output)} bytes)")
        return 0
    print(f"ERROR: render finished but output is missing or empty: {args.output}",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
