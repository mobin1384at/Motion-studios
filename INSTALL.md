# Install — motion-studio

`motion-studio` is an open Agent Skills folder. The only required file is
`SKILL.md`. Install = copy the folder to the right path for your agent.
The zip ships `install.sh` / `install.ps1` (made by the scripts builder);
they copy the folder to **all** relevant paths at once. This page documents
the manual paths so you can install by hand or verify what the script did.

Prerequisites (checked by `scripts/setup.py`): ffmpeg, Node.js, Python 3,
and Chrome/Chromium (headless, for HyperFrames rendering).

## Claude Code

Personal (all projects):

```bash
mkdir -p ~/.claude/skills
cp -r motion-studio ~/.claude/skills/
```

Project only:

```bash
mkdir -p .claude/skills
cp -r motion-studio .claude/skills/
```

Other install routes (same result):

- Marketplace plugin: `/plugin marketplace add <owner>/<repo>` then
  `/plugin install motion-studio@<marketplace>` — TODO: repo name not yet
  decided, see open questions in `CREDITS.md`.
- `npx skills add <owner>/<repo>` — needs the public repo (TODO).

## Codex (OpenAI)

Personal:

```bash
mkdir -p ~/.agents/skills
cp -r motion-studio ~/.agents/skills/
```

Project (scanned from the working directory up to the repo root):

```bash
mkdir -p .agents/skills
cp -r motion-studio .agents/skills/
```

Notes:

- The old path `~/.codex/skills/` is still read.
- Or use `$skill-installer motion-studio` (from the `openai/skills` repo);
  it installs into `~/.codex/skills/`.
- Invoke with `/skills` or `$motion-studio`.

## Gemini CLI

Personal:

```bash
mkdir -p ~/.gemini/skills
cp -r motion-studio ~/.gemini/skills/
# ~/.agents/skills/ also works
```

Project:

```bash
mkdir -p .gemini/skills
cp -r motion-studio .gemini/skills/
# .agents/skills/ also works
```

Note: Gemini CLI was discontinued for free / Google AI Pro / Ultra users on
2026-06-18 and moved to Antigravity CLI (`agy`). Gemini CLI still works with
a paid API key or a Gemini Code Assist Standard/Enterprise license. A skill
is not an extension — extensions install with
`gemini extensions install <GitHub URL or local path>` and need a
`gemini-extension.json` manifest; this skill does not ship one.

## Antigravity (Google)

Project (portable, shared with Codex and Gemini CLI) — **use this first**:

```bash
mkdir -p .agents/skills
cp -r motion-studio .agents/skills/
```

Global, App/IDE:

```bash
mkdir -p ~/.gemini/config/skills
cp -r motion-studio ~/.gemini/config/skills/
# the old path ~/.gemini/antigravity/skills/ is still read
```

Global, CLI (`agy`):

```bash
mkdir -p ~/.gemini/antigravity-cli/skills
cp -r motion-studio ~/.gemini/antigravity-cli/skills/
```

Warning: `npx skills` installs into `~/.agents/skills/`; the IDE sees it but
the CLI does not — for CLI use, copy the folder into the CLI path as well.
The zip's install script covers all three global paths.

Global paths are based on several independent secondary sources that agree
with each other; the official Google doc was not directly reachable at research
time (2026-11-11). If a path does not take effect, verify against the current
Antigravity documentation.

## Manual zip extraction

1. Download the release zip.
2. Unzip it anywhere.
3. Copy the `motion-studio/` folder into the path for your platform above.
4. Run `python3 motion-studio/scripts/setup.py` and fix what it reports
   (missing ffmpeg / Node / Python / Chrome).
5. Restart the agent / reload skills, then ask it to do a motion task —
   the skill activates from its `description`.

## ChatGPT (web) — alternative, no zip install

ChatGPT web **cannot install a skill zip**. Use this instead:

1. Create a **Project** in ChatGPT and name it e.g. "Motion Studio".
2. Paste the contents of `SKILL.md` (or the short version below) into the
   Project's **custom instructions**.
3. Upload as **knowledge files**: `SKILL.md`, `references/engines.md`,
   `references/persian-rtl.md`, `references/rubric.md`,
   `references/styles-catalog.md`, and whichever `references/*.md` fit the
   work at hand.
4. For each video, paste `templates/brief.md` filled in, and the 4-part
   prompt from `templates/prompt-template.md`.

Short custom-instructions version (paste as-is):

> You are a motion-graphics studio. Every frame is a pure function of time
> and seed: frame = f(t, seed). Sound first, picture second. Treatment
> before code. Formula-driven motion, never adjectives. QA the final render
> with the 7-dimension rubric, max 2 review rounds. Persian subtitles only
> via libass + Vazirmatn + RLI/PDI — never ffmpeg drawtext. Never invent
> facts; verify against 2+ sources.

Notes and limits:

- Custom GPTs retire for personal accounts on **2026-12-11** (Enterprise:
  2027-02-11, confirmed deferred). New personal GPTs are already closed.
  Prefer the Project route above, or migrate a GPT to a plugin
  (My GPTs → Migrate to plugin); instructions become a skill inside the
  plugin and knowledge files become reference files, but Custom Actions,
  model settings, Conversation Starters, and sharing settings do not migrate,
  and the new plugin starts private.
- The 20 knowledge-file limit per GPT (512 MB each) is reported from a
  secondary source and is TODO to verify in the official Help Center.

## Verify the install

Ask the agent: "list your skills" or start a motion task (e.g. "make a 10 s
reel from this script"). If the skill does not activate, check that the
folder name is exactly `motion-studio` and that `SKILL.md` sits directly
inside it with `name: motion-studio` in the frontmatter.
