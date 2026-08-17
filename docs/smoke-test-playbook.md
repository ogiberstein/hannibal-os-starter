# Smoke Test Playbook

Run only on a private test surface and only after the operator approves any required route or gateway change.

## 1. Chief-of-Staff DM

Send a harmless message in the operator DM. Verify the active profile is `chief_of_staff`, the response uses the intended role contract, and no prior unrelated project session was inherited.

## 2. Bounded project lane

Send a harmless message in one explicitly routed project lane. Verify the intended project profile receives it and uses the correct project/control docs.

## 3. Unmatched fallback

Send a harmless message from an unconfigured test lane and verify it remains on `default`. Do not intentionally break a live route merely for this check. Confirm all explicit targets exist, then record the behavior documented for the exact installed Hermes version: `v2026.8.3` warns and falls back to default for a missing target, while inspected upstream `main` rejects ingress for a missing or disallowed target.

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
- use the lifecycle command documented for the installed Hermes version;
- verify gateway health and the three routing cases again;
- roll back if the operator journey fails.

Do not build a custom restart supervisor or recovery platform for this starter.

## Evidence rule

Repo tests and config parsing do not prove live routing. Record live evidence privately and sanitize it before sharing. If the live boundary was not exercised, say **not runtime-tested**.
