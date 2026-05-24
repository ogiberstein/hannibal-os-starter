---
name: evidence-gate
description: Produce a public-safe go/no-go evidence gate for a private agent workspace, separating claims from proof and using PASS/FAIL/INCONCLUSIVE outcomes.
triggers:
  - evidence gate
  - go no-go evidence
  - readiness evidence
version: 0.1.0
license: MIT
---

# Evidence Gate

Use this skill before claiming a private Hannibal/Hermes-style workspace is ready, live, deployed, recovered, or safe to rely on.

## Core rule

A claim is not verified until there is evidence. Documentation, memory, or intent is not enough.

## Output format

```md
# Evidence Gate

## Verdict
PASS / PASS WITH RISKS / FAIL / INCONCLUSIVE

## Claim ledger
| Claim | Evidence | Status |
| --- | --- | --- |
| Project route reaches intended profile | ... | PASS / FAIL / INCONCLUSIVE |
| Default or Chief-of-Staff route works | ... | PASS / FAIL / INCONCLUSIVE |
| Restart/recovery path works | ... | PASS / FAIL / INCONCLUSIVE |
| Scheduled update delivers once and is cleaned up | ... | PASS / FAIL / INCONCLUSIVE |

## Gaps and risks
- ...

## Next
- Next: ...
```

## Required evidence types

- Repo verification output for the private deployment or project repo.
- Preflight evidence showing required local config exists without printing secret values.
- Smoke-test evidence for route, default profile, recovery, and scheduled update loops.
- Sanitized artifact paths or summaries; no raw logs or message contents.

## Verdict rules

- Use `PASS` only when every required claim has direct evidence.
- Use `PASS WITH RISKS` only when gaps are explicit, bounded, and accepted.
- Use `FAIL` when evidence contradicts the claim.
- Use `INCONCLUSIVE` when evidence is missing or only inferred.

## Safety rules

- Do not include secrets, raw platform IDs, transcripts, logs, sessions, memories, backups, or customer-private data.
- Do not treat successful config parsing as transport-health evidence.
- Do not treat a repo test pass as proof of live runtime delivery.
