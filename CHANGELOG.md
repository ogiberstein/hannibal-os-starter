# Changelog

Public-safe changes to Hannibal OS Starter. Do not include private deployment state, platform IDs, credentials, logs, transcripts, or customer data.

## 2026-05-23 — Public command and skill examples

- Shipped: Added public command and skill examples for `handover-bootstrap`, `status-refresh`, and `evidence-gate`.
- Public-facing value: Operators get copyable, public-safe prompts and skill procedures for creating project handover packets, refreshing evidence-backed status, and making go/no-go claim ledgers without leaking private runtime state.
- Verification: `python3 -m unittest tests.test_public_command_skill_pack -v`; `python3 scripts/verify_repo.py --path .`.
- Follow-up: These examples are not auto-installed into Hermes; each private deployment should review and adapt them before adding local command shortcuts.

## 2026-05-22 — Planned restart hardening evidence

- Shipped: Updated the smoke-test playbook to require planned restart/recovery evidence before treating a deployment as live-ready.
- Public-facing value: Operators are now told to use operator-approved detached service control, durable comeback notification markers, and journal evidence with no `TimeoutStopSec` or `SIGKILL` instead of accepting a vague post-restart response check.
- Verification: `python3 scripts/verify_repo.py`; GitHub Actions CI on commit `b58d863`.
- Follow-up: Private deployments still need their own approved restart drill; this public starter does not perform or prove a live runtime restart.
