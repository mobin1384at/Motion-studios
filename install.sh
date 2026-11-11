#!/usr/bin/env bash
# install.sh — install the motion-studio skill into every supported agent.
#
# Copies the skill folder (the directory this script lives in) to:
#   Claude Code : ~/.claude/skills/motion-studio
#   Codex       : ~/.agents/skills/motion-studio
#   Gemini CLI  : ~/.gemini/skills/motion-studio  (also ~/.agents/skills/)
#   Antigravity : .agents/skills/motion-studio (project, if run inside a
#                 project) + ~/.gemini/config/skills/ + ~/.gemini/antigravity-cli/skills/
#                 (global Antigravity paths are NOT confirmed in the official
#                 docs — the script copies there if the directories exist and
#                 says so; the project path .agents/skills/ is the certain one)
#   Project     : .agents/skills/motion-studio (shared by Codex/Gemini/Antigravity)
#
# ChatGPT web cannot install a skill zip — see INSTALL.md for the
# Project + custom-instructions alternative.
#
# Usage:
#   ./install.sh            # install to all applicable locations
#   ./install.sh --link     # symlink instead of copying (dev use)
set -euo pipefail

SKILL_NAME="motion-studio"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="copy"
if [ "${1:-}" = "--link" ]; then MODE="link"; fi
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: ./install.sh [--link]"
  echo "  default: copy the skill folder into each agent's skills directory"
  echo "  --link : symlink instead (for developing the skill)"
  exit 0
fi

install_one() {
  local dest="$1"
  local label="$2"
  mkdir -p "$(dirname "$dest")"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    rm -rf "$dest"
    echo "  (replaced existing $dest)"
  fi
  if [ "$MODE" = "link" ]; then
    ln -s "$SRC" "$dest"
  else
    cp -r "$SRC" "$dest"
  fi
  echo "  OK  $label -> $dest"
}

echo "Installing $SKILL_NAME ($MODE) from $SRC"

# Personal (global) locations — always applicable.
install_one "$HOME/.claude/skills/$SKILL_NAME" "Claude Code (personal)"
install_one "$HOME/.agents/skills/$SKILL_NAME" "Codex / Gemini shared (personal)"
install_one "$HOME/.gemini/skills/$SKILL_NAME" "Gemini CLI (personal)"

# Antigravity global paths: documented in secondary sources only, paths
# differ between sources. Copy only where the parent dir already exists.
for base in "$HOME/.gemini/config/skills" "$HOME/.gemini/antigravity-cli/skills" "$HOME/.gemini/antigravity/skills"; do
  if [ -d "$(dirname "$base")" ]; then
    install_one "$base/$SKILL_NAME" "Antigravity (global, unverified path)"
  else
    echo "  SKIP Antigravity global $base (parent dir does not exist)"
  fi
done

# Project location — only when we are inside a project (a .git dir or an
# existing .agents folder signals one).
if [ -d ".git" ] || [ -d ".agents" ]; then
  install_one "$PWD/.agents/skills/$SKILL_NAME" "Project (.agents/skills)"
else
  echo "  SKIP project .agents/skills (not inside a project dir)"
fi

echo "Done. Verify with: ls ~/.claude/skills/$SKILL_NAME"
echo "ChatGPT web cannot install skill zips — see INSTALL.md for the alternative."
