# Smoke Test Playbook

Run only on a private test surface and only after the operator approves any required route or gateway change.

## 1. Chief-of-Staff DM

Send a harmless message in the operator DM. Verify the active profile is `chief_of_staff`, the response uses the intended role contract, and no prior unrelated project session was inherited.

## 2. Domain lead and project channels

Send a harmless message in a channel routed to a domain profile (for example `cio`). Verify that profile answers with its own role contract. Then send one in a project channel that stays on `default` and verify its channel prompt points the agent at the right repo and control docs.

## 3. Unmatched fallback

Send a harmless message from an unconfigured test lane and verify it remains on `default`. Do not intentionally break a live route merely for this check. Confirm every explicit route target exists. In Hermes v0.22.x a route that names a missing profile rejects that chat's messages instead of falling back, so a typo silently cuts off a lane. Older releases warned and fell back to `default`; check the behaviour of the version you run.

## 4. Observability

Record sanitized evidence of:

- active Hermes release/commit or version;
- intended profile name for each test lane;
- recent inbound and outbound success;
- gateway status and bounded error evidence;
- no duplicate credential/profile-adapter conflict.

Use route labels, booleans, timestamps, and redacted summaries. Do not paste raw IDs, message contents, credentials, sessions, memories, or private logs.

## 5. Supervised restart/update — optional and separately approved

If the setup will rely on a long-running gateway, prove one supported Hermes restart or update journey only after approval:

- capture the current runtime/version and rollback target;
- use the lifecycle command documented for the installed Hermes version, or `scripts/hermes-runtime.sh` (see `docs/runtime-updates.md`);
- verify gateway health and the three routing cases again;
- roll back if the operator journey fails.

Do not build a custom restart supervisor or recovery platform for this starter.

## 6. One real build slice

The system exists to ship work. Take one small slice through the whole loop: interview, spec, Codex plan review, your approval, Hermes build on a branch, Claude and Codex code review, your merge. If any step needed manual glue, write it down in the project's `STATUS.md` before the next slice.

## Evidence rule

Repo tests and config parsing do not prove live routing. Record live evidence privately and sanitize it before sharing. If the live boundary was not exercised, say **not runtime-tested**.
