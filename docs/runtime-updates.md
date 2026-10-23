# Updating Hermes with a cheap rollback

On a laptop, use the official `hermes update`. Recent releases stop the gateway during the update, check the new code compiles, and roll the checkout back if it does not. That is enough for most people.

On an always-on server, the gateway is how you reach every agent. If an update breaks it, you lose the chat you would use to fix it. The pattern below keeps the old version installed next to the new one, so getting back is one command and one restart.

## The pattern

- Each Hermes release lives in its own folder with its own virtual environment: `/opt/hermes-runtimes/<tag>/hermes-agent`.
- One symlink (`/usr/local/lib/hermes-agent`) points at the live release. Your `hermes` launcher and the gateway service use the symlink.
- `/opt/hermes-runtimes/previous` points at the release you switched away from.
- No private patches. You run exact upstream releases, so every update is a clean swap.

`scripts/hermes-runtime.sh` implements this in about 100 lines. Install it once:

```bash
sudo install -m 0755 scripts/hermes-runtime.sh /usr/local/sbin/hermes-runtime
```

Then read the variables at the top and set the ones that differ on your host (`HERMES_RUNTIME_ROOT`, `HERMES_LIVE_LINK`, `HERMES_RESTART_CMD`, `HERMES_HEALTH_CMD`, `HERMES_EXTRAS`).

## One-time setup

The official installer puts Hermes in one folder, and your launcher and gateway service point straight at it. The script needs them to go through the live symlink instead. It refuses to switch until that symlink exists.

1. Install the release you run today side by side: `hermes-runtime install v0.22.5` (use your current tag).
2. Create the live symlink: `sudo ln -s /opt/hermes-runtimes/v0.22.5/hermes-agent /usr/local/lib/hermes-agent`.
3. Make the `hermes` on your PATH a two-line wrapper that runs the live release:

   ```bash
   #!/usr/bin/env bash
   exec /usr/local/lib/hermes-agent/venv/bin/python /usr/local/lib/hermes-agent/hermes "$@"
   ```

4. Reinstall the gateway service from that wrapper (`sudo hermes gateway install --system`), restart it, and send one real message to check it answers.

The defaults assume a system-wide service named `hermes-gateway.service`. If you run a user service, set `HERMES_RESTART_CMD` and `HERMES_HEALTH_CMD` to the matching Hermes restart command and a `systemctl --user is-active` check. `install` needs `uv` on the PATH. Under `sudo` it often is not (uv usually lives in `~/.local/bin`), so pass the full PATH or run as the user that owns the runtime folder.

## Use it

```bash
hermes-runtime install v0.22.5     # side-by-side install; nothing live changes
hermes-runtime switch v0.22.5 --dry-run
hermes-runtime switch v0.22.5      # flip the symlink, restart, wait for health
hermes-runtime rollback --dry-run
hermes-runtime rollback            # back to the previous release
hermes-runtime status
```

After a switch, send one real message to the bot and check the reply arrives. A healthy service is not the same as a working chat.

## Before you switch

- **Run it from an SSH shell.** Never ask an agent to restart the gateway it is answering through.
- **Read the release notes.** Look for config migrations. A new release may rewrite settings in every profile's `config.yaml` on first start. If you want to keep your current values, back up each profile's `config.yaml` first and diff it after the switch.
- **Back up the session database once** before a major version. Newer releases may migrate it on first start. Check the notes for whether the previous release can still read it.
- **Restart anything else that runs Hermes code** (desktop backends, long-running CLI sessions). They keep old code in memory.
- **Keep one previous release.** Delete older folders by hand once the new one has run for a few days.

## What the install step does

1. Shallow-clones the tag from upstream and disables pushes from that clone.
2. Runs `uv sync --locked` into the release's own `venv`, using the tag's own `.python-version`.
3. Writes an install stamp marking the checkout as externally managed, when the release supports it. Without the stamp, newer releases treat a source checkout as self-updating and build a separate environment on first launch.
4. Smoke-tests `hermes --version` and the gateway import.

## Verification status

The switch, rollback, dry-run, refusal and failed-health paths are covered by `tests/test_hermes_runtime.py` with stand-in runtimes. The install path mirrors a script used on a real server for several upstream releases, but this public copy has not run an install end to end. Try `install` on a scratch `HERMES_RUNTIME_ROOT` before you rely on it.
