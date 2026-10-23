#!/usr/bin/env bash
# hermes-runtime: side-by-side Hermes installs with a one-command rollback.
#
#   install TAG [--dir DIR]   clone upstream TAG into ROOT/TAG/hermes-agent, build its own venv
#                             (uv sync --locked), smoke-test it. Nothing live changes.
#   switch TAG [--dry-run]    record the live runtime as previous, flip the live symlink,
#                             restart the gateway, wait for health
#   rollback [--dry-run]      switch back to the recorded previous runtime
#   status                    show live, previous and installed runtimes
#
# Layout: LIVE (a symlink your `hermes` launcher and service use) -> ROOT/<tag>/hermes-agent.
# Reference script from hannibal-os-starter. Read docs/runtime-updates.md first and adapt the
# variables below to your host. Run it from a shell, never from a chat that the gateway serves.
set -euo pipefail

UPSTREAM="${HERMES_UPSTREAM:-https://github.com/NousResearch/hermes-agent.git}"
ROOT="${HERMES_RUNTIME_ROOT:-/opt/hermes-runtimes}"
LIVE="${HERMES_LIVE_LINK:-/usr/local/lib/hermes-agent}"
PREVIOUS="$ROOT/previous"
EXTRAS="${HERMES_EXTRAS:-all slack anthropic}"
RESTART_CMD="${HERMES_RESTART_CMD:-hermes gateway restart --system}"
HEALTH_CMD="${HERMES_HEALTH_CMD:-systemctl is-active --quiet hermes-gateway.service}"
HEALTH_WAIT_S="${HERMES_HEALTH_WAIT_S:-120}"

die() { echo "hermes-runtime: $*" >&2; exit 1; }
log() { echo "[$(date -u +%H:%M:%S)] $*"; }

runtime_dir() {  # TAG -> its hermes-agent dir
  echo "$ROOT/$1/hermes-agent"
}

smoke() {  # DIR
  "$1/venv/bin/python" -B "$1/hermes" --version
  (cd "$1" && "$1/venv/bin/python" -B -c 'import gateway.run' >/dev/null)
}

cmd_install() {
  local tag="$1" dir extras=()
  dir=$(runtime_dir "$tag")
  [[ "${2:-}" == "--dir" ]] && dir="${3:?--dir needs a path}"
  [[ -e "$dir" ]] && die "$dir already exists"
  for e in $EXTRAS; do extras+=(--extra "$e"); done
  log "clone $tag -> $dir"
  mkdir -p "$(dirname "$dir")"
  git clone -q --depth 1 --branch "$tag" "$UPSTREAM" "$dir"
  git -C "$dir" remote set-url --push origin DISABLED
  # uv picks the tag's own .python-version, so each runtime keeps the Python it was released with.
  log "uv sync --locked ($EXTRAS)"
  (cd "$dir" && UV_PROJECT_ENVIRONMENT="$dir/venv" uv sync -q --locked --no-dev "${extras[@]}")
  # Newer releases treat an unstamped source checkout as self-updating and build their own
  # environment on first launch. Stamp it as externally managed so it keeps using this venv.
  if [[ -f "$dir/scripts/write_install_stamp.py" ]]; then
    "$dir/venv/bin/python" -B "$dir/scripts/write_install_stamp.py" --output "$dir/install-stamp.json" \
      --update-mechanism external --base-version "${tag#v}" --distance 0 >/dev/null
  fi
  smoke "$dir"
  log "installed $tag at $dir ($(git -C "$dir" rev-parse --short HEAD))"
}

flip_and_restart() {  # NEW_DIR [--dry-run]
  local new="$1" dry="${2:-}" cur waited=0
  [[ -L "$LIVE" ]] || die "$LIVE is not a symlink; do the one-time setup in docs/runtime-updates.md first"
  cur=$(readlink -f "$LIVE")
  [[ -x "$new/venv/bin/python" ]] || die "$new has no venv; run install first"
  [[ "$(readlink -f "$new")" == "$cur" ]] && die "$new is already live"
  echo "current:   $cur"
  echo "switch to: $new"
  [[ "$dry" == "--dry-run" ]] && { echo "(dry run: nothing changed)"; return; }
  smoke "$new"
  ln -sfn "$cur" "$PREVIOUS.tmp" && mv -Tf "$PREVIOUS.tmp" "$PREVIOUS"
  ln -sfn "$new" "$LIVE.tmp" && mv -Tf "$LIVE.tmp" "$LIVE"
  log "symlink flipped; restarting: $RESTART_CMD"
  bash -c "$RESTART_CMD"
  while (( waited < HEALTH_WAIT_S )); do
    if bash -c "$HEALTH_CMD" >/dev/null 2>&1; then log "healthy on $new"; return; fi
    sleep 5; waited=$((waited + 5))
  done
  die "not healthy after ${HEALTH_WAIT_S}s; roll back with: hermes-runtime rollback"
}

cmd_status() {
  echo "live:     $LIVE -> $(readlink -f "$LIVE") ($(git -C "$LIVE" describe --tags --always 2>/dev/null || echo '?'))"
  if [[ -L "$PREVIOUS" ]]; then echo "previous: $(readlink -f "$PREVIOUS")"; else echo "previous: (none recorded)"; fi
  echo "installed:"
  ls -1d "$ROOT"/*/hermes-agent 2>/dev/null | sed 's/^/  /' || true
}

case "${1:-}" in
  install)  [[ -n "${2:-}" ]] || die "usage: install TAG [--dir DIR]"; shift; cmd_install "$@" ;;
  switch)   [[ -n "${2:-}" ]] || die "usage: switch TAG [--dry-run]"; flip_and_restart "$(runtime_dir "$2")" "${3:-}" ;;
  rollback) [[ -L "$PREVIOUS" ]] || die "no previous runtime recorded at $PREVIOUS"
            flip_and_restart "$(readlink -f "$PREVIOUS")" "${2:-}" ;;
  status)   cmd_status ;;
  *) sed -n '2,13p' "$0"; exit 2 ;;
esac
