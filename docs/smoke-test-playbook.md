# Smoke Test Playbook

Run these before live-ready claims.

## 1. Project channel route

Send a harmless test message in the project channel. Verify the intended project profile responds and records the correct context boundary.

## 2. Default / Chief-of-Staff route

Send a harmless default-route message. Verify it reaches the default or Chief-of-Staff profile, not a project-specific profile.

## 3. Restart / recovery

Restart the gateway or runtime service. Verify routes and local config are still loaded and no secrets are printed in logs or diagnostics.

## 4. Scheduled update

Create a one-shot scheduled update to a test target. Verify it delivers once, then remove or disable it.

## 5. Transport-health evidence

auth/config success is not enough for live-ready status. For each enabled messaging surface, record sanitized evidence of:

- recent successful send from the managed gateway/runtime to an approved test route;
- recent inbound message or command reaching the intended project/default profile;
- scheduled update delivery to the intended target, followed by cleanup/removal of the test job;
- restart/recovery proof that the same route still works after the gateway/service restarts; planned restarts must use operator-approved detached service control, durable comeback notification markers, and journal evidence with no `TimeoutStopSec`/`SIGKILL`.

Use route labels instead of raw IDs. Do not paste transcripts, tokens, private logs, or customer-private message content.

## Evidence rule

Record evidence in the private deployment repo or local ops notes. Redact raw IDs, message contents, secrets, logs, and transcripts before sharing.
