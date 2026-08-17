# Reference Setup Checklist

Use this before relying on a private Hermes profile/routing setup.

- [ ] Current upstream Hermes is installed using the official method.
- [ ] Exact installed release/commit or version is recorded privately.
- [ ] Native `chief_of_staff` and any project profiles exist.
- [ ] Each role has a reviewed `SOUL.md` and explicit approval boundaries.
- [ ] Required project `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, and `AGENTS.md` exist.
- [ ] Credentials and raw route IDs exist only in private local state.
- [ ] The default profile uses native `gateway.profile_routes`; no parallel router is running.
- [ ] Unmatched traffic remains on `default`.
- [ ] Read-only preflight passes without exposing values.
- [ ] Private smoke evidence proves Chief-of-Staff DM, project route, and unmatched fallback behavior.
- [ ] Gateway failure is observable and one cheap rollback target is known.
- [ ] Any restart/update test was separately approved and used the installed Hermes version's supported lifecycle.
- [ ] No custom deployment, hardening, synchronization, or recovery platform was added from this reference.

Passing repository tests alone does not satisfy this checklist.
