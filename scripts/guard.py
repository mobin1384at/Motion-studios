#!/usr/bin/env python3
"""guard.py — pre-flight guards for the motion-studio skill.

Stops mechanical errors where they happen, before an expensive render.
Checks a scene file (HTML/JS) and an ffmpeg command line:

  1. Persian via ffmpeg drawtext — REJECTED. drawtext cannot shape Arabic/
     Persian script or do bidi; letters render detached and reversed.
     Persian captions must go through libass (subtitles/ass filter) —
     see captions.py.
  2. Non-determinism in seek(t) HTML — REJECTED: Math.random(), CSS
     transitions/animations, or state carried between frames (a frame must
     be a pure function of time: frame = f(t, seed)). Randomness must be
     seeded (e.g. mulberry32) and transitions replaced by explicit
     time-based interpolation.
  3. Crossfade — REJECTED unless the style explicitly asks for it
     (pass --allow-crossfade, or a style file containing the word
     "crossfade"). Default banned list (research §3-1): crossfade, spring
     easing, particles/glow/lens flare, camera shake, 3D card flips,
     gradients on chrome UI.

Usage:
    python3 guard.py --scene scene.html
    python3 guard.py --scene scene.html --style styles/kinetic-type/STYLE.md
    python3 guard.py --ffmpeg-cmd "ffmpeg -i in.mp4 -vf drawtext=text='سلام' out.mp4"
    python3 guard.py --scene scene.html --allow-crossfade
    python3 guard.py --scene scene.html --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

FA_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")

# Banned-by-default patterns in scene code (name, regex, fix hint).
DETERMINISM_RULES = [
    ("Math.random()", r"Math\.random\s*\(",
     "Replace with a seeded PRNG (e.g. mulberry32(seed)) so the same t "
     "always gives the same frame."),
    ("Date.now()/performance.now() in scene code",
     r"\b(Date\.now|performance\.now)\s*\(",
     "Time must come only from the seek(t) argument, never the wall clock."),
    ("CSS transition", r"transition\s*:",
     "Transitions carry state between frames. Interpolate explicitly from t."),
    ("CSS animation", r"animation\s*:",
     "CSS animations are wall-clock driven. Drive every motion from seek(t)."),
    ("setTimeout/setInterval in scene code", r"\b(setTimeout|setInterval)\s*\(",
     "Timers carry state between frames. Everything must derive from t."),
    ("requestAnimationFrame loop", r"requestAnimationFrame\s*\(",
     "The render loop calls seek(t) itself; a rAF loop would fight it."),
]

BANNED_STYLE_PATTERNS = [
    ("crossfade", r"cross-?fade",
     "Crossfades are banned by default (research §3-1). If the style "
     "explicitly asks for one, pass --allow-crossfade."),
    ("spring easing", r"spring|elastic|bounce",
     "Spring/elastic/bounce easing is banned by default. Use an explicit "
     "cubic-bezier instead."),
    ("particles/glow/lens flare", r"particle|lens[- ]?flare|\bglow\b",
     "Particles, glow and lens flare are banned by default."),
    ("camera shake", r"camera[- ]?shake|shake\s*:",
     "Camera shake is banned by default."),
    ("3D card flip", r"rotateY\s*\(\s*180|flip",
     "3D card flips are banned by default."),
]


def _strip_comments(code: str) -> str:
    """Remove /* */ and // comments for pattern scanning.

    Heuristic only: a mention of a banned pattern inside a comment
    (e.g. "no Math.random()") must not fail the guard. Strings are not
    protected, which is fine for scanning — the checked patterns do not
    occur in URLs or string literals in practice.
    """
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    code = re.sub(r"<!--.*?-->", "", code, flags=re.DOTALL)
    code = re.sub(r"//[^\n]*", "", code)
    return code


def check_scene(path: str, allow_crossfade: bool,
                style_text: str) -> list[dict]:
    issues: list[dict] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        code = fh.read()
    # Pattern scans run on comment-stripped code so that a comment such as
    # "no Math.random()" cannot fail the guard. The drawtext and Persian-trap
    # checks below intentionally scan the raw file (markup, not comments).
    scan = _strip_comments(code)

    # 1. Persian rendered via drawtext — only relevant if the file itself
    #    contains an ffmpeg/drawtext invocation (e.g. a build script in HTML
    #    comments). Checked mainly via --ffmpeg-cmd; here we catch embedded
    #    drawtext calls with Persian text.
    for m in re.finditer(r"drawtext[^\n]*", code):
        if FA_RE.search(m.group(0)):
            issues.append({"rule": "persian-drawtext", "severity": "error",
                           "detail": "Persian text in an ffmpeg drawtext call "
                                     "— use libass (subtitles/ass) via captions.py."})

    # 2. Determinism (comment-stripped code).
    for name, pattern, hint in DETERMINISM_RULES:
        if re.search(pattern, scan):
            issues.append({"rule": f"nondeterminism:{name}", "severity": "error",
                           "detail": hint})

    # 3. Banned style patterns — lifted when the style file explicitly asks
    #    for that element (same rule as crossfade: the style is the authority).
    style_lower = style_text.lower()
    style_allows = {
        "crossfade": "crossfade" in style_lower,
        "spring easing": any(k in style_lower
                             for k in ("spring", "elastic", "bounce")),
        "particles/glow/lens flare": any(k in style_lower for k in
                                         ("particle", "glow", "lens flare")),
        "camera shake": "shake" in style_lower,
        "3D card flip": "flip" in style_lower,
    }
    for name, pattern, hint in BANNED_STYLE_PATTERNS:
        if name == "crossfade" and allow_crossfade:
            continue
        if style_allows.get(name):
            continue
        if re.search(pattern, scan, re.IGNORECASE):
            issues.append({"rule": f"banned-style:{name}", "severity": "error",
                           "detail": hint})

    # 4. Persian traps from persian-reel (warnings, not errors).
    if re.search(r'<html[^>]*\bdir\s*=\s*["\']rtl["\']', code, re.IGNORECASE):
        issues.append({"rule": "persian-rtl-html", "severity": "warning",
                       "detail": "<html dir=\"rtl\"> renders the video fully "
                                 "black in HyperFrames (persian-reel trap #1). "
                                 "Set direction on inner elements instead."})
    if re.search(r"letter-spacing\s*:\s*-", code):
        issues.append({"rule": "persian-letter-spacing", "severity": "warning",
                       "detail": "Negative letter-spacing closes Persian word "
                                 "gaps (persian-reel trap #2)."})
    if "۰" in code and re.search(r"font|0", code):
        issues.append({"rule": "persian-zero", "severity": "warning",
                       "detail": "Persian zero '۰' can render as a dot in some "
                                 "fonts (persian-reel trap #3) — verify in a "
                                 "test frame."})
    return issues


def check_ffmpeg_cmd(cmd: str) -> list[dict]:
    issues: list[dict] = []
    if "drawtext" in cmd:
        # drawtext text=... may contain Persian directly or via a file.
        if FA_RE.search(cmd):
            issues.append({"rule": "persian-drawtext", "severity": "error",
                           "detail": "ffmpeg drawtext with Persian text — it "
                                     "cannot shape/bidi Persian. Use the "
                                     "subtitles/ass filter (libass) instead."})
        else:
            issues.append({"rule": "drawtext-latin-only", "severity": "warning",
                           "detail": "drawtext is in the command. It is fine "
                                     "for Latin text only — never for Persian."})
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Pre-flight guards: reject Persian drawtext, "
                    "non-deterministic seek(t), and banned style patterns.")
    ap.add_argument("--scene", default=None, help="HTML/JS scene file to check.")
    ap.add_argument("--ffmpeg-cmd", default=None,
                    help="An ffmpeg command line to check (quoted).")
    ap.add_argument("--style", default=None,
                    help="Style file (STYLE.md); if it explicitly asks for a "
                         "crossfade, the crossfade ban is lifted for that style.")
    ap.add_argument("--allow-crossfade", action="store_true",
                    help="Allow crossfade in this scene.")
    ap.add_argument("--json", action="store_true", help="JSON output.")
    args = ap.parse_args()

    if not args.scene and not args.ffmpeg_cmd:
        print("ERROR: give --scene and/or --ffmpeg-cmd.", file=sys.stderr)
        return 2

    style_text = ""
    if args.style:
        if not os.path.isfile(args.style):
            print(f"ERROR: style file not found: {args.style}", file=sys.stderr)
            return 2
        with open(args.style, encoding="utf-8") as fh:
            style_text = fh.read()

    issues: list[dict] = []
    if args.scene:
        if not os.path.isfile(args.scene):
            print(f"ERROR: scene file not found: {args.scene}", file=sys.stderr)
            return 2
        issues += check_scene(args.scene, args.allow_crossfade, style_text)
    if args.ffmpeg_cmd:
        issues += check_ffmpeg_cmd(args.ffmpeg_cmd)

    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    if args.json:
        print(json.dumps({"issues": issues,
                          "verdict": "FAIL" if errors else "PASS"},
                         indent=2, ensure_ascii=False))
    else:
        if not issues:
            print("GUARD PASS — no violations found.")
        else:
            for i in issues:
                print(f"[{i['severity'].upper()}] {i['rule']}: {i['detail']}")
            print(f"GUARD {'FAIL' if errors else 'PASS'} — "
                  f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
