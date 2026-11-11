#!/usr/bin/env python3
"""beat_grid.py — onset / beat grid of a music track.

Uses librosa if available (onset strength + beat tracking); otherwise a
numpy fallback (spectral-flux onset envelope + autocorrelation tempo).
Output is JSON: {"tempo_bpm": ..., "beats": [t, ...], "onsets": [t, ...]}.

The beat grid is what lyric/music videos sync cuts and karaoke to
(research §2: pdoom-video beat grid, 132.007 BPM).

Usage:
    python3 beat_grid.py --input music.mp3 --output beats.json
    python3 beat_grid.py --input music.mp3 --output beats.json --tempo 132.0
    python3 beat_grid.py --input music.mp3   # prints JSON to stdout
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile

SR = 22050
HOP = 512


def load_audio_mono(path: str) -> "object":
    """Decode any audio file to a mono float32 numpy array at SR via ffmpeg."""
    import numpy as np
    import shutil
    if shutil.which("ffmpeg") is None:
        print("ERROR: ffmpeg not found on PATH (needed to decode audio).",
              file=sys.stderr)
        sys.exit(2)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", path,
             "-ac", "1", "-ar", str(SR), "-f", "f32le", tmp_path],
            capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"ERROR: ffmpeg could not decode {path}:\n{proc.stderr.strip()}",
                  file=sys.stderr)
            sys.exit(1)
        with open(tmp_path, "rb") as fh:
            data = fh.read()
        return np.frombuffer(data, dtype=np.float32)
    finally:
        os.unlink(tmp_path)


def spectral_flux_onsets(y, sr: int, hop: int):
    """Return (onset_times, onset_envelope, frame_times) — numpy only."""
    import numpy as np
    n_fft = 2048
    frames = []
    for start in range(0, max(1, len(y) - n_fft), hop):
        frame = y[start:start + n_fft] * np.hanning(n_fft)
        frames.append(np.abs(np.fft.rfft(frame)))
    if not frames:
        return [], [], []
    spec = np.array(frames).T  # (freq, time)
    flux = np.maximum(0, np.diff(spec, axis=1)).sum(axis=0)
    flux = np.concatenate([[0.0], flux])
    times = np.arange(len(flux)) * hop / sr
    # Peak-pick: local maxima above median + 0.5*std.
    thr = float(np.median(flux) + 0.5 * np.std(flux))
    onsets = []
    for i in range(1, len(flux) - 1):
        if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]:
            onsets.append(float(times[i]))
    return onsets, flux, times


def estimate_tempo(onsets: list[float], flux, times) -> float:
    """Autocorrelation of the onset envelope over 60-200 BPM."""
    import numpy as np
    if len(onsets) < 4 or len(flux) < 10:
        return 0.0
    env = np.asarray(flux, dtype=float)
    env = env - env.mean()
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    sr_frames = SR / HOP  # frames per second
    best_bpm, best_val = 0.0, -1.0
    for bpm in range(60, 201):
        lag = int(round(60.0 / bpm * sr_frames))
        if 0 < lag < len(ac) and ac[lag] > best_val:
            best_val, best_bpm = float(ac[lag]), float(bpm)
    return best_bpm


def beats_from_tempo(onsets: list[float], tempo: float, duration: float) -> list[float]:
    if tempo <= 0 or not onsets:
        return []
    period = 60.0 / tempo
    # Anchor the grid on the first strong onset.
    anchor = onsets[0]
    beats = []
    t = anchor
    while t <= duration:
        beats.append(round(t, 3))
        t += period
    # Also extend backwards from the anchor.
    t = anchor - period
    while t >= 0:
        beats.append(round(t, 3))
        t -= period
    return sorted(beats)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compute onset/beat grid of a music track (librosa if "
                    "present, numpy fallback otherwise).")
    ap.add_argument("--input", required=True, help="Music audio file.")
    ap.add_argument("--output", default=None, help="Output JSON file (default: stdout).")
    ap.add_argument("--tempo", type=float, default=None,
                    help="Force a known tempo in BPM (skips estimation).")
    ap.add_argument("--backend", choices=["auto", "librosa", "numpy"],
                    default="auto", help="Onset backend (default auto).")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2
    try:
        import numpy  # noqa: F401
    except ImportError:
        print("ERROR: numpy is not installed — beat_grid.py needs it.",
              file=sys.stderr)
        print("  pip install numpy   (add librosa for better results: "
              "pip install librosa)", file=sys.stderr)
        return 2

    backend = args.backend
    if backend == "auto":
        try:
            import librosa  # noqa: F401
            backend = "librosa"
        except ImportError:
            backend = "numpy"
            print("NOTE: librosa not installed — using numpy fallback "
                  "(less accurate beat tracking).", file=sys.stderr)

    y = load_audio_mono(args.input)
    duration = len(y) / SR

    if backend == "librosa":
        import librosa
        import numpy as np
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=SR, hop_length=HOP)
        beats = [round(float(t), 3) for t in librosa.frames_to_time(
            beat_frames, sr=SR, hop_length=HOP)]
        onset_env = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env,
                                                  sr=SR, hop_length=HOP)
        onsets = [round(float(t), 3) for t in librosa.frames_to_time(
            onset_frames, sr=SR, hop_length=HOP)]
        tempo_bpm = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)
    else:
        onsets, flux, times = spectral_flux_onsets(y, SR, HOP)
        tempo_bpm = args.tempo or estimate_tempo(onsets, flux, times)
        beats = beats_from_tempo(onsets, tempo_bpm, duration)
        onsets = [round(t, 3) for t in onsets]

    if args.tempo:
        tempo_bpm = args.tempo
        beats = beats_from_tempo(onsets, tempo_bpm, duration)

    result = {
        "file": os.path.basename(args.input),
        "duration_s": round(float(duration), 3),
        "tempo_bpm": round(float(tempo_bpm), 3) if tempo_bpm else 0.0,
        "backend": backend,
        "beats": beats,
        "onsets": onsets,
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"OK: {len(beats)} beats, {len(onsets)} onsets, "
              f"tempo {result['tempo_bpm']} BPM ({backend}) -> {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
