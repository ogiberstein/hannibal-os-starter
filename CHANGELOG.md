# Changelog

Public-safe changes to Hannibal OS Starter. Historical entries describe their time; they are not current operating instructions.

## 2026-08-11 — V2 truth alignment and paused-reference status

- Reframed the starter around current upstream Hermes as the runtime and a thin Hannibal layer for role contracts, project-control docs, native profiles/routing, operator judgment, observability, and cheap rollback.
- Marked Hannibal OS commercial/product work paused and this repository an unsupported public reference.
- Replaced the standalone router/custom profile/runtime examples with a native `gateway.profile_routes` fragment verified by source/docs inspection against Hermes `v2026.8.3` / `3c27eb6234bf91b8ceee9e9071591b31e9b148cb` and cross-checked against upstream `main` `f51aa6a9b5ce514e15f8e337777f522fd5cc6fa2`.
- Removed obsolete managed-deployment flags, V1 cgroup-symbol checks, custom restart-hardening contract, and bespoke recovery-platform guidance.
- No live Hermes runtime, profile, route, credential, gateway, service, cron, or customer state was changed or runtime-tested.

## Historical V1-era entries

The entries below are retained only as repository history. Their managed-deployment and restart-hardening guidance was superseded by the V2 refresh above.

### 2026-06-03 — Runtime workload isolation contract

Added public preflight guidance for a then-current custom managed-deployment isolation contract. The flags, symbol checks, and transient-unit requirements were removed from current guidance on 2026-08-11.

### 2026-05-23 — Public command and skill examples

Added public-safe examples for handover bootstrap, status refresh, and evidence gating. They remain optional prompt/skill examples and are not automatically installed.

### 2026-05-22 — Planned restart hardening evidence

Added a custom managed-restart evidence contract. It was removed from current guidance on 2026-08-11 in favor of current upstream Hermes lifecycle documentation, supervised change, observable failure, and simple rollback.
