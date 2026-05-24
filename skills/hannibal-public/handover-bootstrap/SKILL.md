---
name: handover-bootstrap
description: Build a public-safe project packet for starting or handing over a private agent workspace without exposing secrets, raw platform IDs, logs, sessions, memories, or customer data.
triggers:
  - handover bootstrap
  - bootstrap handover
  - project handover packet
version: 0.1.0
license: MIT
---

# Handover Bootstrap

Use this skill when a person wants to start or hand over a private Hannibal/Hermes-style workspace from this public starter.

## Goal

Create a small project packet that gives the next operator or agent enough context to continue safely, without copying private runtime state.

## Inputs to ask for or inspect in the private deployment

- Project name and owner.
- Intended messaging surface labels, using labels only, not raw channel IDs.
- Current purpose, users, scope, risks, and explicit non-goals.
- Current runtime status: not installed, configured, preflighted, smoke-tested, or live-ready.
- Existing public starter files copied into the private deployment.

## Output: project packet

Write or update these files in the private deployment workspace, not in this public starter checkout:

1. `BRIEF.md` — purpose, users, scope, risks, boundaries.
2. `STATUS.md` — current gate, verified facts, blockers, and `Next:`.
3. `DECISIONS.md` — durable decisions with date, decision, rationale, alternatives, status.
4. `AGENTS.md` — project-specific operating rules, safety gates, context sources.

## Safety rules

- Include no secrets, credentials, private keys, tokens, or passwords.
- Include no raw platform IDs, message links, transcripts, logs, sessions, memories, backup archives, or customer-private data.
- Use placeholders such as `CHANNEL_ID_HERE` only in examples.
- Treat runtime or deployment readiness as unverified until private preflight and smoke-test evidence exist.

## Verification

Before calling the packet usable:

- Confirm every file exists in the private deployment workspace.
- Confirm each file has a concrete `Next:` or says why there is no next step.
- Confirm the packet distinguishes verified facts from inference.
- Run the private repo's sanitation or starter `scripts/verify_repo.py` if the packet is being committed.
