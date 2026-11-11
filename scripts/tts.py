#!/usr/bin/env python3
"""tts.py — Persian/English narration via several TTS backends.

Backends (research §4-4):
  elevenlabs  ElevenLabs API. Models: eleven_v3 / eleven_v4 (both list
              Persian `fa`). Needs env ELEVENLABS_API_KEY.
  azure       Microsoft Azure Speech, voice fa-IR-DilaraNeural (female)
              or fa-IR-FaridNeural (male). Needs AZURE_SPEECH_KEY +
              AZURE_SPEECH_REGION. Requires the `azure-cognitiveservices-
              speech` package.
  edge        edge-tts (unofficial, free, no key, no SLA). Voices
              fa-IR-DilaraNeural / fa-IR-FaridNeural. Needs `edge-tts`.
  piper       Local Piper (CPU, light). Needs the `piper` binary and a
              Persian voice model file (--model-path). Five Persian voices
              are reported (amir, ganji, ganji_adabi, gyro, reza_ibrahim)
              — verify against the official Piper voice list.
  kokoro      Local Kokoro. Needs the `kokoro` package. Persian is NOT
              documented for Kokoro in the research — the script warns and
              still tries, but reports honestly if the language fails.

TTS-DIRECTOR LESSONS (from the research synthesis — also in --help):
  * ElevenLabs v4: the speed setting effectively does NOT work; do not
    rely on it to fix pacing — edit the text or split sentences instead.
  * Some Persian diacritics are mispronounced by ElevenLabs; test a short
    sample before a long render and simplify diacritics if needed.
  * Only clone a voice you have permission to clone.

Usage:
    python3 tts.py --backend edge --text "سلام دنیا" --output voice.mp3
    python3 tts.py --backend elevenlabs --text-file script.txt --output voice.mp3 --model eleven_v3 --voice-id <id>
    python3 tts.py --backend azure --text-file script.txt --output voice.wav --voice fa-IR-FaridNeural
    python3 tts.py --backend piper --text-file script.txt --output voice.wav --model-path fa_IR-amir-medium.onnx
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

FA_VOICES = {"fa-IR-DilaraNeural", "fa-IR-FaridNeural"}
ELEVENLABS_MODELS = {"eleven_v3", "eleven_v4", "eleven_multilingual_v2",
                     "eleven_flash_v2_5"}


def read_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.text_file:
        if not os.path.isfile(args.text_file):
            print(f"ERROR: text file not found: {args.text_file}", file=sys.stderr)
            sys.exit(2)
        with open(args.text_file, encoding="utf-8") as fh:
            return fh.read().strip()
    print("ERROR: provide --text or --text-file.", file=sys.stderr)
    sys.exit(2)


def check_out(path: str) -> None:
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)


def backend_elevenlabs(args: argparse.Namespace, text: str) -> int:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY is not set in the environment.",
              file=sys.stderr)
        print("  Get a key at https://elevenlabs.io and export it:", file=sys.stderr)
        print("    export ELEVENLABS_API_KEY=sk_...", file=sys.stderr)
        return 2
    if args.model in ("eleven_multilingual_v2", "eleven_flash_v2_5"):
        print("WARNING: model", args.model, "does not list Persian (fa) in "
              "the research — prefer eleven_v3 or eleven_v4 for Persian.",
              file=sys.stderr)
    if args.model == "eleven_v4" and args.speed is not None:
        print("NOTE (tts-director lesson): in eleven_v4 the speed setting "
              "effectively does not work — pacing must be fixed in the "
              "text, not here.", file=sys.stderr)
    try:
        import urllib.request
    except ImportError:  # pragma: no cover
        print("ERROR: urllib is unavailable (broken Python install).",
              file=sys.stderr)
        return 1
    import json as _json
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{args.voice_id}"
    payload = {"text": text, "model_id": args.model,
               "voice_settings": {"stability": args.stability,
                                  "similarity_boost": args.similarity}}
    req = urllib.request.Request(
        url, data=_json.dumps(payload).encode("utf-8"),
        headers={"xi-api-key": key, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            audio = resp.read()
    except Exception as exc:
        print(f"ERROR: ElevenLabs request failed: {exc}", file=sys.stderr)
        print("  Check the API key, voice id and model name.", file=sys.stderr)
        return 1
    if not audio:
        print("ERROR: ElevenLabs returned empty audio.", file=sys.stderr)
        return 1
    with open(args.output, "wb") as fh:
        fh.write(audio)
    return 0


def backend_azure(args: argparse.Namespace, text: str) -> int:
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        print("ERROR: Azure needs AZURE_SPEECH_KEY and AZURE_SPEECH_REGION "
              "in the environment.", file=sys.stderr)
        return 2
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        print("ERROR: azure-cognitiveservices-speech is not installed.",
              file=sys.stderr)
        print("  pip install azure-cognitiveservices-speech", file=sys.stderr)
        return 2
    config = speechsdk.SpeechConfig(subscription=key, region=region)
    config.speech_synthesis_voice_name = args.voice
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=args.output)
    synth = speechsdk.SpeechSynthesizer(speech_config=config,
                                        audio_config=audio_config)
    result = synth.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"ERROR: Azure synthesis failed: {result.reason}", file=sys.stderr)
        if result.cancellation_details:
            print(f"  {result.cancellation_details.reason}: "
                  f"{result.cancellation_details.error_details}", file=sys.stderr)
        return 1
    return 0


def backend_edge(args: argparse.Namespace, text: str) -> int:
    if shutil.which("edge-tts") is None:
        print("ERROR: edge-tts is not installed.", file=sys.stderr)
        print("  pip install edge-tts", file=sys.stderr)
        return 2
    cmd = ["edge-tts", "--voice", args.voice, "--text", text,
           "--write-media", args.output]
    if args.rate:
        cmd += ["--rate", args.rate]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0 or not os.path.isfile(args.output):
        print(f"ERROR: edge-tts failed: {proc.stderr.decode(errors='replace')}",
              file=sys.stderr)
        return 1
    return 0


def backend_piper(args: argparse.Namespace, text: str) -> int:
    if shutil.which("piper") is None:
        print("ERROR: piper binary not found on PATH.", file=sys.stderr)
        print("  Install Piper: https://github.com/rhasspy/piper", file=sys.stderr)
        return 2
    if not args.model_path or not os.path.isfile(args.model_path):
        print("ERROR: --model-path is required for piper (a Persian .onnx "
              "voice model, e.g. fa_IR-amir-medium.onnx).", file=sys.stderr)
        print("  Voice list: https://github.com/rhasspy/piper (verify the "
              "Persian voices there).", file=sys.stderr)
        return 2
    proc = subprocess.run(
        ["piper", "--model", args.model_path, "--output_file", args.output],
        input=text.encode("utf-8"), capture_output=True)
    if proc.returncode != 0 or not os.path.isfile(args.output):
        print(f"ERROR: piper failed: {proc.stderr.decode(errors='replace')}",
              file=sys.stderr)
        return 1
    return 0


def backend_kokoro(args: argparse.Namespace, text: str) -> int:
    print("WARNING: Persian is NOT documented for Kokoro in the research — "
          "output quality for fa is unverified.", file=sys.stderr)
    try:
        from kokoro import KPipeline  # type: ignore
    except ImportError:
        print("ERROR: kokoro package is not installed.", file=sys.stderr)
        print("  pip install kokoro", file=sys.stderr)
        return 2
    try:
        import soundfile as sf
    except ImportError:
        print("ERROR: soundfile is not installed (needed by kokoro).",
              file=sys.stderr)
        print("  pip install soundfile", file=sys.stderr)
        return 2
    try:
        pipeline = KPipeline(lang_code=args.lang or "a")
        segments = list(pipeline(text, voice=args.voice or "af_heart"))
        audio = b"".join(seg[2].tobytes() for seg in segments)
        sf.write(args.output, __import__("numpy").frombuffer(
            audio, dtype="float32"), 24000)
    except Exception as exc:
        print(f"ERROR: Kokoro synthesis failed: {exc}", file=sys.stderr)
        return 1
    return 0


BACKENDS = {"elevenlabs": backend_elevenlabs, "azure": backend_azure,
            "edge": backend_edge, "piper": backend_piper,
            "kokoro": backend_kokoro}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Text-to-speech narration (ElevenLabs / Azure / edge-tts / "
                    "Piper / Kokoro).",
        epilog="TTS-director lessons: ElevenLabs v4 speed setting effectively "
               "does not work — fix pacing in the text. Some Persian "
               "diacritics are mispronounced by ElevenLabs — test a short "
               "sample first. Only clone a voice you have permission to clone.")
    ap.add_argument("--backend", required=True, choices=sorted(BACKENDS),
                    help="TTS backend.")
    ap.add_argument("--text", default=None, help="Text to speak.")
    ap.add_argument("--text-file", default=None, help="File containing the text.")
    ap.add_argument("--output", required=True, help="Output audio file (.mp3/.wav).")
    ap.add_argument("--model", default="eleven_v3",
                    help="ElevenLabs model_id (default eleven_v3). "
                         "eleven_v3/eleven_v4 list Persian (fa).")
    ap.add_argument("--voice-id", default=None,
                    help="ElevenLabs voice id (elevenlabs backend).")
    ap.add_argument("--voice", default="fa-IR-DilaraNeural",
                    help="Voice name for azure/edge/kokoro "
                         "(default fa-IR-DilaraNeural).")
    ap.add_argument("--lang", default=None, help="Kokoro lang code (e.g. a, e).")
    ap.add_argument("--model-path", default=None,
                    help="Piper .onnx voice model path.")
    ap.add_argument("--rate", default=None,
                    help="edge-tts rate, e.g. +10%% or -10%%.")
    ap.add_argument("--speed", type=float, default=None,
                    help="Requested speed — NOTE: ignored in practice by "
                         "ElevenLabs v4 (see epilog).")
    ap.add_argument("--stability", type=float, default=0.5)
    ap.add_argument("--similarity", type=float, default=0.75)
    args = ap.parse_args()

    if args.backend == "elevenlabs" and not args.voice_id:
        print("ERROR: --voice-id is required for the elevenlabs backend.",
              file=sys.stderr)
        return 2
    if args.backend in ("azure", "edge") and args.voice not in FA_VOICES:
        print(f"WARNING: voice {args.voice} is not one of the documented "
              f"Persian voices {sorted(FA_VOICES)} — continuing anyway.",
              file=sys.stderr)

    text = read_text(args)
    if not text:
        print("ERROR: text is empty.", file=sys.stderr)
        return 2
    check_out(args.output)

    rc = BACKENDS[args.backend](args, text)
    if rc != 0:
        return rc
    if not os.path.isfile(args.output) or os.path.getsize(args.output) == 0:
        print(f"ERROR: backend finished but output is missing/empty: "
              f"{args.output}", file=sys.stderr)
        return 1
    print(f"OK: {args.backend} -> {args.output} "
          f"({os.path.getsize(args.output)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
