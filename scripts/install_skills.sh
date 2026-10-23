#!/usr/bin/env bash
# Copy this repo's skills into Hermes or Claude Code.
#
#   scripts/install_skills.sh hermes [--force] [SKILL...]   -> ${HERMES_HOME:-$HOME/.hermes}/skills/<category>/<skill>
#   scripts/install_skills.sh claude [--force] [SKILL...]   -> ${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/<skill>
#
# With no SKILL names, installs every skill. Existing skills are skipped unless --force.
# For a non-default Hermes profile, set HERMES_HOME to that profile's home first.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-}"; shift || true
force=0
if [[ "${1:-}" == "--force" ]]; then force=1; shift; fi

case "$target" in
  hermes) dest_root="${HERMES_HOME:-$HOME/.hermes}/skills" ;;
  claude) dest_root="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}" ;;
  *) sed -n '2,8p' "$0"; exit 2 ;;
esac

installed=0; skipped=0
for skill_md in "$REPO"/skills/*/*/SKILL.md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  category="$(basename "$(dirname "$src")")"
  if [[ $# -gt 0 ]] && ! printf '%s\n' "$@" | grep -qx "$name"; then continue; fi
  if [[ "$target" == hermes ]]; then dest="$dest_root/$category/$name"; else dest="$dest_root/$name"; fi
  if [[ -e "$dest" && $force -eq 0 ]]; then
    echo "skip (exists, use --force): $dest"; skipped=$((skipped + 1)); continue
  fi
  mkdir -p "$(dirname "$dest")"
  if [[ -e "$dest" ]]; then rm -rf "$dest"; fi
  cp -R "$src" "$dest"
  echo "installed: $dest"; installed=$((installed + 1))
done
echo "$installed installed, $skipped skipped"
