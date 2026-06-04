# Changelog

Public-safe changes to Hannibal OS Starter. Do not include private deployment state, platform IDs, credentials, logs, transcripts, or customer data.

## 2026-06-03 — Runtime workload isolation contract

- Shipped: Added public-safe runtime preflight guidance and env placeholders for Hermes-compatible workload isolation, plus CTO-audit compatibility signals for cwd preservation, unit-state recovery, env temp-file cleanup, and best-effort transient-unit cleanup.
- Public-facing value: Operators are told that a messaging gateway must not share a cgroup with memory-heavy foreground terminal, PTY/background coding, or LSP subprocesses; presence/symbol checks are compatibility gates only.
- Verification: `python3 scripts/verify_repo.py --path .` and GitHub Actions CI after this commit.
- Follow-up: Managed deployments still need live cgroup smoke evidence showing `hermes-terminal-*`, `hermes-terminal-pty-*`, and `hermes-lsp-*` transient units before claiming live isolation.

## 2026-05-23 — Public command and skill examples

- Shipped: Added public command and skill examples for `handover-bootstrap`, `status-refresh`, and `evidence-gate`.
- Public-facing value: Operators get copyable, public-safe prompts and skill procedures for creating project handover packets, refreshing evidence-backed status, and making go/no-go claim ledgers without leaking private runtime state.
- Verification: `python3 -m unittest tests.test_public_command_skill_pack -v`; `python3 scripts/verify_repo.py --path .`; targeted public-pack private-marker/raw-ID scan; GitHub Actions CI on commit `8126434`.
- Follow-up: These examples are not auto-installed into Hermes; each private deployment should review and adapt them before adding local command shortcuts.

## 2026-05-22 — Planned restart hardening evidence

- Shipped: Updated the smoke-test playbook to require planned restart/recovery evidence before treating a deployment as live-ready.
- Public-facing value: Operators are now told to use operator-approved detached service control, durable comeback notification markers, and journal evidence with no `TimeoutStopSec` or `SIGKILL` instead of accepting a vague post-restart response check.
- Verification: `python3 scripts/verify_repo.py`; GitHub Actions CI on commit `b58d863`.
- Follow-up: Private deployments still need their own approved restart drill; this public starter does not perform or prove a live runtime restart.
