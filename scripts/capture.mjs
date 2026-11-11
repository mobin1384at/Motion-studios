#!/usr/bin/env node
/**
 * capture.mjs — frame-by-frame capture of a seekable HTML scene.
 *
 * Contract (HyperFrames / cinecode): the page exposes a pure function of
 * time, `seek(t)` (seconds), which sets the scene to exactly time `t`
 * with no randomness, no CSS transitions and no state carried between
 * frames. This script calls seek(t) for each frame, screenshots to PNG,
 * then assembles the PNGs with ffmpeg into an MP4.
 *
 * Requirements: Node 20+, a headless Chrome/Chromium, the `puppeteer`
 * package (npm i puppeteer), and ffmpeg on PATH.
 * If puppeteer or Chrome is missing, this script fails with install
 * instructions — it never pretends to have rendered.
 *
 * Usage:
 *   node capture.mjs --input scene.html --output out.mp4 \
 *       --fps 30 --width 1080 --height 1920 --duration 10 [--start 0]
 */
import { spawn, execSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve, dirname, basename } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

function fail(msg) {
  console.error(`ERROR: ${msg}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = { fps: 30, width: 1080, height: 1920, duration: 10, start: 0 };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) fail(`unexpected argument: ${a}`);
    const key = a.slice(2);
    if (key === "help") { printHelp(); process.exit(0); }
    const val = argv[++i];
    if (val === undefined) fail(`missing value for --${key}`);
    if (["fps", "width", "height"].includes(key)) args[key] = parseInt(val, 10);
    else if (["duration", "start"].includes(key)) args[key] = parseFloat(val);
    else if (["input", "output"].includes(key)) args[key] = val;
    else fail(`unknown option --${key}`);
  }
  for (const k of ["input", "output"]) {
    if (!args[k]) fail(`--${k} is required. Run with --help for usage.`);
  }
  if (!(args.fps > 0 && args.width > 0 && args.height > 0 && args.duration > 0)) {
    fail("--fps, --width, --height and --duration must all be > 0.");
  }
  return args;
}

function printHelp() {
  console.log(`capture.mjs — capture a seekable HTML scene to MP4.

Usage:
  node capture.mjs --input scene.html --output out.mp4 [options]

Options:
  --input <file>     HTML scene file (required). Must expose window.seek(t).
  --output <file>    Output MP4 path (required).
  --fps <n>          Frames per second (default 30).
  --width <n>        Frame width in px (default 1080).
  --height <n>       Frame height in px (default 1920).
  --duration <s>     Duration in seconds (default 10).
  --start <s>        Start time in seconds (default 0).

Requirements: puppeteer (npm i puppeteer), headless Chrome, ffmpeg on PATH.
The page contract: seek(t) is a pure function of time — no Math.random(),
no CSS transitions, no state between frames (see guard.py).`);
}

function which(tool) {
  try {
    execSync(`command -v ${tool}`, { stdio: "pipe" });
    return true;
  } catch { return false; }
}

function run(cmd, args) {
  return new Promise((resolvePromise, reject) => {
    const p = spawn(cmd, args, { stdio: "inherit" });
    p.on("error", reject);
    p.on("close", (code) =>
      code === 0 ? resolvePromise() : reject(new Error(`${cmd} exited ${code}`)));
  });
}

const args = parseArgs(process.argv);
const inputPath = resolve(args.input);
if (!existsSync(inputPath)) fail(`input file not found: ${inputPath}`);
if (!which("ffmpeg")) {
  fail("ffmpeg not found on PATH. Install it: https://ffmpeg.org/download.html");
}

import { createRequire } from "node:module";

// Resolve puppeteer: plain import() first (works when the package sits in
// node_modules next to this script or the project). ESM import() ignores
// NODE_PATH and cannot import a package directory, so fall back to
// createRequire().resolve() with explicit search dirs — PUPPETEER_MODULE_PATH
// (the package folder itself) or node_modules next to the working directory.
let puppeteer = null;
try {
  const mod = await import("puppeteer");
  puppeteer = mod.default ?? mod;
} catch { /* fall through to require.resolve below */ }
if (!puppeteer) {
  const searchDirs = [process.cwd()];
  if (process.env.PUPPETEER_MODULE_PATH) {
    searchDirs.push(dirname(process.env.PUPPETEER_MODULE_PATH));
  }
  try {
    const localRequire = createRequire(import.meta.url);
    const resolved = localRequire.resolve("puppeteer", { paths: searchDirs });
    const mod = await import(pathToFileURL(resolved).href);
    puppeteer = mod.default ?? mod;
  } catch { /* handled below */ }
}
if (!puppeteer) {
  fail(
    "puppeteer is not installed. Run:\n" +
    "  npm install puppeteer\n" +
    "in the project directory (it downloads a headless Chrome), " +
    "or install Chrome/Chromium and set PUPPETEER_EXECUTABLE_PATH.\n" +
    "If puppeteer lives elsewhere, set PUPPETEER_MODULE_PATH to its folder."
  );
}

const totalFrames = Math.round(args.duration * args.fps);
// Frames dir: honour MOTION_STUDIO_TMPDIR first — some machines have a
// tiny /tmp (e.g. 512 MB tmpfs) that cannot hold hundreds of PNGs.
const framesBase = process.env.MOTION_STUDIO_TMPDIR || tmpdir();
const framesDir = join(framesBase, `motion-studio-frames-${Date.now()}`);
mkdirSync(framesDir, { recursive: true });

let browser;
try {
  browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-gpu-sandbox", "--hide-scrollbars",
           `--window-size=${args.width},${args.height}`],
    ...(process.env.PUPPETEER_EXECUTABLE_PATH
      ? { executablePath: process.env.PUPPETEER_EXECUTABLE_PATH } : {}),
  });
} catch (e) {
  rmSync(framesDir, { recursive: true, force: true });
  fail(`could not launch headless Chrome: ${e.message}\n` +
    "Install Google Chrome/Chromium, or run `npm install puppeteer` so it " +
    "downloads its own Chromium. If Chrome is installed elsewhere, set " +
    "PUPPETEER_EXECUTABLE_PATH to its binary.");
}

try {
  const page = await browser.newPage();
  await page.setViewport({ width: args.width, height: args.height });
  await page.goto(pathToFileURL(inputPath).href, { waitUntil: "networkidle0" });

  const hasSeek = await page.evaluate(() => typeof window.seek === "function");
  if (!hasSeek) {
    fail(`page does not expose window.seek(t): ${inputPath}\n` +
      "The scene must define a global seek(t) function that sets the scene " +
      "to time t (seconds). See references/technique.md.");
  }

  for (let i = 0; i < totalFrames; i++) {
    const t = args.start + i / args.fps;
    await page.evaluate((tt) => window.seek(tt), t);
    // Let one animation frame settle so seek() side-effects paint.
    await new Promise((r) => setTimeout(r, 16));
    const name = join(framesDir, `frame-${String(i).padStart(6, "0")}.png`);
    await page.screenshot({ path: name });
    if ((i + 1) % 60 === 0 || i === totalFrames - 1) {
      console.error(`captured ${i + 1}/${totalFrames} frames`);
    }
  }
} finally {
  await browser.close();
}

const got = readdirSync(framesDir).filter((f) => f.endsWith(".png")).length;
if (got !== totalFrames) {
  rmSync(framesDir, { recursive: true, force: true });
  fail(`expected ${totalFrames} frames, captured ${got}. Aborting.`);
}

const outPath = resolve(args.output);
mkdirSync(dirname(outPath), { recursive: true });
try {
  await run("ffmpeg", [
    "-y", "-framerate", String(args.fps),
    "-i", join(framesDir, "frame-%06d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", outPath,
  ]);
} finally {
  rmSync(framesDir, { recursive: true, force: true });
}

console.log(`OK: wrote ${outPath} (${totalFrames} frames, ${args.fps} fps)`);
