---
name: status-refresh
description: Refresh a project STATUS.md with evidence-backed current state, gaps, blockers, and a concrete Next step while keeping public/private boundaries intact.
triggers:
  - status refresh
  - refresh status
  - update status doc
version: 0.1.0
license: MIT
---

# Status Refresh

Use this skill when updating a private deployment or project `STATUS.md` from repo/runtime evidence.

## Required source order

1. Current `STATUS.md`, `BRIEF.md`, `DECISIONS.md`, and `AGENTS.md` in the private deployment or project repo.
2. Git status, recent commits, verification output, and generated artifacts.
3. Runtime evidence only when explicitly available and safe to inspect.
4. Chat memory or summaries only as navigation, not proof.

## Output format

Use a compact structure:

```md
# STATUS

## Current gate
- ...

## Verified facts
- ...

## Inference
- ...

## Blockers
- ...

## Next
- Next: ...
```

## Rules

- Put only verified facts under `Verified facts`.
- Put guesses or likely implications under `Inference`.
- Call something a blocker only when execution is concretely prevented.
- Always include `Next:` unless no useful next step exists; then write `Next: none — waiting on ...`.
- Do not include secrets, raw platform IDs, transcripts, logs, sessions, memories, or private customer data.

## Verification

Before finishing:

- Re-read the changed `STATUS.md`.
- Check that stale completed-history did not replace current gate/next step.
- Run the repo's verification or sanitation check before committing.
