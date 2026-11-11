#!/usr/bin/env python3
"""fetch_fonts.py — download the OFL fonts for the motion-studio skill.

The skill zip vendors the font files, but the GitHub repo cannot carry
binary files through the connector's text-only snapshot push. This script
re-fetches the same fonts from their official sources and verifies them
by md5, so a checkout of the repo is complete without the binaries.

Fonts (both SIL OFL 1.1, see assets/fonts/OFL.txt):
  * Vazirmatn variable — official release v33.003 zip; the extracted
    fonts/variable/Vazirmatn[wght].ttf must match md5
    63d2e128b5b911ac9455e5204f36d45f (verified 2026-11-11).
  * Lalezar Regular — official repo master branch; the file there is the
    1.0 build, md5 793f1fe6a8e3f92c3d7ae501b440ecec (verified 2026-11-11).
    NOTE: the copy vendored in the zip is the newer 1.003 build supplied
    by the user (md5 b09134ac350e6345b0b6cd94f78f6ffc); the official repo
    currently serves 1.0. Both are Lalezar by Borna Izadpanah, OFL 1.1 —
    --check accepts either md5.

Usage:
    python3 scripts/fetch_fonts.py            # download missing fonts
    python3 scripts/fetch_fonts.py --check    # verify files already present
    python3 scripts/fetch_fonts.py --force    # re-download even if present
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS_DIR = HERE.parent / "assets" / "fonts"

VAZIRMATN_URL = (
    "https://github.com/rastikerdar/vazirmatn/releases/download/"
    "v33.003/vazirmatn-v33.003.zip"
)
VAZIRMATN_MEMBER = "fonts/variable/Vazirmatn[wght].ttf"
VAZIRMATN_MD5 = "63d2e128b5b911ac9455e5204f36d45f"

LALEZAR_URL = (
    "https://raw.githubusercontent.com/BornaIz/Lalezar/master/"
    "fonts/Lalezar-Regular.ttf"
)
# Official repo currently serves the 1.0 build; the zip vendors 1.003.
LALEZAR_MD5S = {
    "793f1fe6a8e3f92c3d7ae501b440ecec",  # official master (1.0)
    "b09134ac350e6345b0b6cd94f78f6ffc",  # vendored copy (1.003)
}


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "motion-studio/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
        for chunk in iter(lambda: resp.read(1 << 20), b""):
            fh.write(chunk)


def fetch_vazirmatn(target: Path) -> bool:
    print(f"downloading Vazirmatn v33.003 ...")
    with tempfile.TemporaryDirectory(prefix="motion-studio-font-") as td:
        zpath = Path(td) / "vazirmatn-v33.003.zip"
        download(VAZIRMATN_URL, zpath)
        with zipfile.ZipFile(zpath) as zf:
            data = zf.read(VAZIRMATN_MEMBER)
        if hashlib.md5(data).hexdigest() != VAZIRMATN_MD5:
            print("ERROR: Vazirmatn md5 mismatch after download.", file=sys.stderr)
            return False
        target.write_bytes(data)
    print(f"  OK: {target} ({target.stat().st_size} bytes, md5 verified)")
    return True


def fetch_lalezar(target: Path) -> bool:
    print("downloading Lalezar Regular (official repo master) ...")
    with tempfile.TemporaryDirectory(prefix="motion-studio-font-") as td:
        fpath = Path(td) / "Lalezar-Regular.ttf"
        download(LALEZAR_URL, fpath)
        if md5_of(fpath) not in LALEZAR_MD5S:
            print("ERROR: Lalezar md5 mismatch after download.", file=sys.stderr)
            return False
        target.write_bytes(fpath.read_bytes())
    print(f"  OK: {target} ({target.stat().st_size} bytes, md5 verified)")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="Only verify fonts already present in assets/fonts/.")
    ap.add_argument("--force", action="store_true",
                    help="Re-download even if the files are already present.")
    args = ap.parse_args()

    vaz = FONTS_DIR / "Vazirmatn-Variable.ttf"
    lal = FONTS_DIR / "Lalezar-Regular.ttf"
    ok = True

    if args.check:
        for path, good in ((vaz, {VAZIRMATN_MD5}), (lal, LALEZAR_MD5S)):
            if not path.is_file():
                print(f"MISSING: {path}")
                ok = False
            elif md5_of(path) not in good:
                print(f"BAD MD5: {path} ({md5_of(path)})")
                ok = False
            else:
                print(f"OK: {path} (md5 {md5_of(path)})")
        return 0 if ok else 1

    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    if args.force or not vaz.is_file() or md5_of(vaz) != VAZIRMATN_MD5:
        ok = fetch_vazirmatn(vaz) and ok
    else:
        print(f"present: {vaz} (md5 verified)")
    if args.force or not lal.is_file() or md5_of(lal) not in LALEZAR_MD5S:
        ok = fetch_lalezar(lal) and ok
    else:
        print(f"present: {lal} (md5 verified)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
