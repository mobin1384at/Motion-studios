# install.ps1 — install the motion-studio skill into every supported agent (Windows).
#
# Copies the skill folder (the directory this script lives in) to:
#   Claude Code : $env:USERPROFILE\.claude\skills\motion-studio
#   Codex       : $env:USERPROFILE\.agents\skills\motion-studio
#   Gemini CLI  : $env:USERPROFILE\.gemini\skills\motion-studio
#   Antigravity : .agents\skills\motion-studio (project) +
#                 $env:USERPROFILE\.gemini\config\skills\ and
#                 $env:USERPROFILE\.gemini\antigravity-cli\skills\
#                 (global Antigravity paths are NOT confirmed in the official
#                 docs — copied only if the parent dir exists)
#   Project     : .agents\skills\motion-studio
#
# ChatGPT web cannot install a skill zip — see INSTALL.md for the alternative.
#
# Usage:
#   .\install.ps1          # copy
#   .\install.ps1 -Link    # symlink instead (dev use; needs Developer Mode / admin)
param(
  [switch]$Link,
  [switch]$Help
)

if ($Help) {
  Write-Host "Usage: .\install.ps1 [-Link]"
  Write-Host "  default: copy the skill folder into each agent's skills directory"
  Write-Host "  -Link   : symlink instead (for developing the skill)"
  exit 0
}

$SkillName = "motion-studio"
$Src = Split-Path -Parent $MyInvocation.MyCommand.Path
$Mode = if ($Link) { "link" } else { "copy" }

function Install-One {
  param([string]$Dest, [string]$Label)
  $Parent = Split-Path -Parent $Dest
  if (-not (Test-Path $Parent)) { New-Item -ItemType Directory -Force -Path $Parent | Out-Null }
  if (Test-Path $Dest) {
    Remove-Item -Recurse -Force $Dest
    Write-Host "  (replaced existing $Dest)"
  }
  if ($Mode -eq "link") {
    New-Item -ItemType SymbolicLink -Path $Dest -Target $Src | Out-Null
  } else {
    Copy-Item -Recurse -Force $Src $Dest
  }
  Write-Host "  OK  $Label -> $Dest"
}

Write-Host "Installing $SkillName ($Mode) from $Src"

Install-One "$env:USERPROFILE\.claude\skills\$SkillName" "Claude Code (personal)"
Install-One "$env:USERPROFILE\.agents\skills\$SkillName" "Codex / Gemini shared (personal)"
Install-One "$env:USERPROFILE\.gemini\skills\$SkillName" "Gemini CLI (personal)"

foreach ($base in @("$env:USERPROFILE\.gemini\config\skills",
                   "$env:USERPROFILE\.gemini\antigravity-cli\skills",
                   "$env:USERPROFILE\.gemini\antigravity\skills")) {
  if (Test-Path (Split-Path -Parent $base)) {
    Install-One "$base\$SkillName" "Antigravity (global, unverified path)"
  } else {
    Write-Host "  SKIP Antigravity global $base (parent dir does not exist)"
  }
}

if ((Test-Path ".git") -or (Test-Path ".agents")) {
  Install-One "$PWD\.agents\skills\$SkillName" "Project (.agents\skills)"
} else {
  Write-Host "  SKIP project .agents\skills (not inside a project dir)"
}

Write-Host "Done. Verify with: Get-ChildItem $env:USERPROFILE\.claude\skills\$SkillName"
Write-Host "ChatGPT web cannot install skill zips — see INSTALL.md for the alternative."
