---
name: evidence-gate
description: Produce a public-safe evidence gate for a native Hermes profile/routing setup, separating claims from proof and using PASS/FAIL/INCONCLUSIVE outcomes.
triggers:
  - evidence gate
  - go no-go evidence
  - readiness evidence
version: 0.2.0
license: MIT
---

# Evidence Gate

Use this skill before claiming a private native-Hermes profile/routing setup is ready, live, recovered, or safe to rely on.

## Core rule

A claim is not verified until there is direct evidence. Documentation, config parsing, memory, repository tests, or intent are not end-to-end runtime proof.

## Output format

```md
# Evidence Gate

## Verdict
PASS / PASS WITH RISKS / FAIL / INCONCLUSIVE

## Claim ledger
| Claim | Evidence | Status |
| --- | --- | --- |
| Operator DM reaches `chief_of_staff` | ... | PASS / FAIL / INCONCLUSIVE |
| Explicit project lane reaches its project profile | ... | PASS / FAIL / INCONCLUSIVE |
| Unmatched traffic remains on `default` | ... | PASS / FAIL / INCONCLUSIVE |
| Missing-route-target behavior matches the exact installed Hermes version | ... | PASS / FAIL / INCONCLUSIVE |
| Gateway/runtime identity and rollback target are known | ... | PASS / FAIL / INCONCLUSIVE |

## Gaps and risks
- ...

## Next
- Next: ...
```

## Required evidence types

- Exact installed Hermes release/commit or version.
- Native profile and route configuration evidence with raw identifiers omitted.
- Private smoke evidence for Chief-of-Staff DM, explicit project route, unmatched fallback, and version-appropriate missing-target behavior without intentionally breaking a live route.
- Sanitized gateway status/error summaries; no raw logs or message contents.
- If restart/update compatibility is claimed, evidence from one separately approved supported-Hermes lifecycle plus the known rollback target.

## Verdict rules

- Use `PASS` only when every required claim has direct evidence.
- Use `PASS WITH RISKS` only when gaps are explicit, bounded, and accepted.
- Use `FAIL` when evidence contradicts the claim.
- Use `INCONCLUSIVE` when evidence is missing or only inferred.

## Safety rules

- Do not include secrets, raw platform IDs, transcripts, logs, sessions, memories, backups, host details, or customer-private data.
- Do not treat successful config parsing, repo tests, or service-active state as transport-health evidence.
- Do not mutate profiles, routes, credentials, gateways, services, cron, or runtime merely to complete a read-only evidence review.
- Do not introduce a custom router, deployment system, or recovery platform to make the gate pass.
