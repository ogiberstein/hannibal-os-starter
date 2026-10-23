# Agent Instructions

Start here. This file tells any agent what the project is, where to look, and what needs approval.

## Project

PROJECT_SUMMARY_HERE (one or two sentences; details live in `BRIEF.md`).

## Operating stance

- Keep answers concise and evidence-backed.
- Treat memory and summaries as navigation, not proof.
- Read `STATUS.md`, `BRIEF.md`, `ROADMAP.md`, and `DECISIONS.md` before current-state claims.
- Default to the MVP quality bar: simplest working slice, fix blockers, one review pass.
- Do not expose secrets, raw platform IDs, transcripts, logs, sessions, memories, or backups.
- Ask before production, credential, permission, deletion, spending, or external-message actions.
- Builders do not merge their own work. The owner approves the spec and every merge.

## Source of truth

- `STATUS.md`: tactical state, blockers, next step.
- `BRIEF.md`: purpose, users, scope, constraints.
- `ROADMAP.md`: where the project is going, in order.
- `DECISIONS.md`: durable decisions and why.
- `docs/`: specs, plans, reviews, runbooks.

## Build parameters

- Branches: BRANCH_CONVENTION_HERE. Forbidden files: `.env*`, FORBIDDEN_PATHS_HERE.
- Gates: TEST_COMMAND_HERE, LINT_COMMAND_HERE, BUILD_COMMAND_HERE.
- Post-merge smoke check: SMOKE_CHECK_HERE.
