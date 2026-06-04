# Runtime Preflight

A preflight should answer: "Is this instance configured enough to smoke test?" It should not expose secrets.

## Check presence only

- `.env` exists locally.
- Required key names are present.
- Config file exists.
- Profile router exists.
- Runtime checkout or package exists.
- Service wrapper exists if using a long-running gateway.
- Placeholders have been replaced in private local config.
- A pinned runtime ref is set (`HERMES_REF`/`RUNTIME_REF` equivalent); preflight should report only presence, not the literal value.
- For Hermes-compatible managed gateways, `HERMES_GATEWAY_SESSION=1`, `HERMES_TERMINAL_SYSTEMD_ISOLATION=1`, bounded terminal memory env vars (`HERMES_TERMINAL_MEMORY_HIGH`, `HERMES_TERMINAL_MEMORY_MAX`, `HERMES_TERMINAL_MEMORY_SWAP_MAX`), and bounded LSP memory env vars (`HERMES_LSP_MEMORY_HIGH`, `HERMES_LSP_MEMORY_MAX`, `HERMES_LSP_MEMORY_SWAP_MAX`) are present.
- Runtime compatibility symbols are present when the checkout is available: `_gateway_systemd_isolation_enabled`, `_systemd_run_command`, process-registry `systemd_unit` support, and LSP transient-unit support.
- Latest CTO-audit compatibility signals are present when the checkout is available: cwd-preserving `--working-directory`, `systemctl show` recovery using `ActiveState` / `SubState` / `MainPID`, Hermes env temp-file cleanup (`hermes-terminal-env-*`), and best-effort transient-unit cleanup.

## Do not

- Source `.env` as shell code.
- Print key values.
- Print raw platform IDs.
- Print transcripts, logs, sessions, memories, or backups.
- Mutate runtime checkouts unless the operator explicitly asks for an upgrade.

## Runtime workload isolation contract

For a Hermes-compatible managed deployment, the messaging gateway/control plane must not share a cgroup with memory-heavy terminal, coding, or LSP subprocesses. This is not about increasing gateway memory; it is about keeping heavy workloads outside the gateway service cgroup.

Customer/public-safe preflight should do presence and symbol checks only unless running on a real deployment host. It should warn/fail honestly: a compatibility gate does not prove live cgroup isolation.

Live isolation is proven only after sanitized smoke evidence from a real deployment observes:

- foreground terminal work in `hermes-terminal-*` transient units;
- PTY/background coding sessions in `hermes-terminal-pty-*` transient units;
- LSP servers in `hermes-lsp-*` transient units;
- no secrets, raw platform IDs, `.env` values, logs, transcripts, sessions, or memories in the evidence.
