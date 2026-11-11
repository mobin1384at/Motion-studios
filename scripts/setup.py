#!/usr/bin/env python3
"""setup.py — self-diagnosis for the motion-studio skill.

Checks OS, Python, Node, ffmpeg/ffprobe, Chrome/Chromium, and optional
Python packages (faster-whisper, numpy, librosa). Prints a STATUS report
and a list of missing tools. Exits 0 only when all REQUIRED tools are
present; optional tools are reported but do not fail the check.

Usage:
    python3 setup.py [--json] [--quiet]
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], timeout: int = 15) -> str | None:
    """Run a command, return stripped stdout, or None on any failure."""
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if out.returncode != 0:
        # Some tools print version to stderr (ffmpeg, node --version is stdout).
        text = (out.stdout or "") + (out.stderr or "")
        return text.strip() or None
    return (out.stdout or out.stderr or "").strip()


def first_version(text: str | None) -> str | None:
    if not text:
        return None
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", text)
    return m.group(1) if m else None


def check_tool(name: str, cmd: list[str]) -> dict:
    path = shutil.which(cmd[0])
    if path is None:
        return {"name": name, "found": False, "path": None, "version": None}
    raw = run(cmd)
    return {
        "name": name,
        "found": True,
        "path": path,
        "version": first_version(raw),
        "raw": (raw.splitlines()[0] if raw else None),
    }


def check_python_module(name: str) -> dict:
    try:
        __import__(name)
        return {"name": name, "found": True}
    except ImportError:
        return {"name": name, "found": False}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check the motion-studio toolchain and print STATUS."
    )
    ap.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    ap.add_argument("--quiet", action="store_true", help="Only print missing tools.")
    args = ap.parse_args()

    checks: dict[str, dict] = {}
    # Required tools
    checks["python"] = {
        "name": "python",
        "found": True,
        "path": sys.executable,
        "version": platform.python_version(),
    }
    checks["node"] = check_tool("node", ["node", "--version"])
    checks["ffmpeg"] = check_tool("ffmpeg", ["ffmpeg", "-version"])
    checks["ffprobe"] = check_tool("ffprobe", ["ffprobe", "-version"])
    # Chrome: try several binary names; first hit wins. Also honour
    # PUPPETEER_EXECUTABLE_PATH and the puppeteer browser cache
    # (~/.cache/puppeteer), where `npx puppeteer browsers install chrome`
    # puts Chrome without adding it to PATH.
    chrome = None
    for cand in ("google-chrome", "google-chrome-stable", "chromium",
                 "chromium-browser", "chrome"):
        c = check_tool("chrome", [cand, "--version"])
        if c["found"]:
            chrome = c
            break
    if chrome is None:
        env_path = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
        candidates = ([env_path] if env_path else []) + sorted(
            Path.home().glob(".cache/puppeteer/chrome/*/chrome-linux*/chrome"))
        for p in candidates:
            if p and Path(p).is_file() and os.access(p, os.X_OK):
                chrome = {"name": "chrome", "found": True,
                          "path": str(p), "version": "puppeteer cache"}
                break
    checks["chrome"] = chrome or {"name": "chrome", "found": False,
                                  "path": None, "version": None}
    # Optional Python packages
    for mod in ("faster_whisper", "numpy", "librosa"):
        checks[mod] = check_python_module(mod)

    required = ["python", "node", "ffmpeg", "ffprobe", "chrome"]
    optional = ["faster_whisper", "numpy", "librosa"]
    missing_required = [k for k in required if not checks[k]["found"]]
    missing_optional = [k for k in optional if not checks[k]["found"]]

    status = "OK" if not missing_required else "MISSING_TOOLS"
    report = {
        "status": status,
        "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "python_version": platform.python_version(),
        "checks": checks,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"motion-studio setup — {report['os']}")
        print(f"STATUS: {status}")
        print()
        for key in required + optional:
            c = checks[key]
            mark = "OK  " if c["found"] else "MISS"
            ver = c.get("version") or ""
            path = c.get("path") or "-"
            print(f"  [{mark}] {key:<15} {ver:<12} {path}")
        if missing_required:
            print()
            print("Missing REQUIRED tools:")
            hints = {
                "node": "  node: install Node.js 20+ from https://nodejs.org",
                "ffmpeg": "  ffmpeg: https://ffmpeg.org/download.html "
                          "(also provides ffprobe)",
                "ffprobe": "  ffprobe: ships with ffmpeg — install ffmpeg.",
                "chrome": "  chrome: install Google Chrome or Chromium; "
                          "capture.mjs needs it for headless rendering.",
            }
            for k in missing_required:
                print(hints.get(k, f"  {k}: install it and retry."))
        if missing_optional:
            print()
            print("Missing OPTIONAL packages (features degrade gracefully):")
            for k in missing_optional:
                if k == "faster_whisper":
                    print("  faster_whisper: pip install faster-whisper "
                          "(needed by transcribe.py)")
                elif k == "numpy":
                    print("  numpy: pip install numpy (needed by beat_grid.py "
                          "fallback and qc helpers)")
                elif k == "librosa":
                    print("  librosa: pip install librosa (beat_grid.py uses "
                          "numpy fallback without it)")

    if not args.quiet and not args.json and not missing_required:
        print()
        print("All required tools present. Next: python3 render.py --help")
    return 0 if not missing_required else 1


if __name__ == "__main__":
    raise SystemExit(main())
