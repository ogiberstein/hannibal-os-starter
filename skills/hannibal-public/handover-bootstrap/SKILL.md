---
name: handover-bootstrap
description: Build a public-safe project control packet for a private native-Hermes workspace without exposing secrets, raw platform IDs, logs, sessions, memories, or customer data.
triggers:
  - handover bootstrap
  - bootstrap handover
  - project handover packet
version: 0.2.0
license: MIT
---

# Handover Bootstrap

Use this skill when a person wants to start or hand over a private project-control workspace used by native Hermes profiles.

## Goal

Create a small project packet that gives the next operator or agent enough context to continue safely, without copying private runtime state or recreating a deployment platform.

## Inputs to ask for or inspect

- Project name and owner.
- Intended role/profile labels, using labels only, not raw route IDs.
- Current purpose, users, scope, risks, and explicit non-goals.
- Current runtime truth: exact Hermes version if known; otherwise mark it unknown.
- Current verification state: control-doc only, configured, preflighted, smoke-tested, or runtime-tested.

## Output: project packet

Write or update these files in the private project/control workspace, not in this public starter checkout:

1. `BRIEF.md` — purpose, users, scope, risks, boundaries.
2. `STATUS.md` — current gate, verified facts, blockers, and `Next:`.
3. `DECISIONS.md` — durable decisions with date, decision, rationale, alternatives, status.
4. `AGENTS.md` — project-specific operating rules, approval gates, and context sources.

## Safety rules

- Include no secrets, credentials, private keys, tokens, or passwords.
- Include no raw platform IDs, message links, transcripts, logs, sessions, memories, backup archives, host details, or customer-private data.
- Use placeholders such as `CHAT_ID_HERE` only in examples.
- Treat runtime readiness as unverified until private preflight and smoke-test evidence exist.
- Point changing Hermes CLI/config details to official docs; do not encode a parallel router or deployment system.

## Verification

Before calling the packet usable:

- Confirm every file exists in the private project/control workspace.
- Confirm each file has a concrete `Next:` or says why there is no next step.
- Confirm the packet distinguishes verified facts from inference.
- Confirm no private runtime source, profile memory, routes, or operational evidence was copied.
- Run the private repo's sanitation checks if the packet is committed.
