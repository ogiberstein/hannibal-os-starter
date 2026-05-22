# Changelog

Public-safe changes to Hannibal OS Starter. Do not include private deployment state, platform IDs, credentials, logs, transcripts, or customer data.

## 2026-05-22 — Planned restart hardening evidence

- Shipped: Updated the smoke-test playbook to require planned restart/recovery evidence before treating a deployment as live-ready.
- Public-facing value: Operators are now told to use operator-approved detached service control, durable comeback notification markers, and journal evidence with no `TimeoutStopSec` or `SIGKILL` instead of accepting a vague post-restart response check.
- Verification: `python3 scripts/verify_repo.py`; GitHub Actions CI on commit `b58d863`.
- Follow-up: Private deployments still need their own approved restart drill; this public starter does not perform or prove a live runtime restart.
