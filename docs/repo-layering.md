# Repository Layering

Use separate repositories or directories for separate responsibilities.

## Public starter

Owns the agent operating-system layer: rulebook and role templates, routing fragment, skills, docs, checklists, and sanitation scripts. It must not contain live runtime state.

## Project harness

[agent-trainer-harness](https://github.com/ogiberstein/agent-trainer-harness) owns the five project files (`AGENTS.md`, `BRIEF.md`, `STATUS.md`, `ROADMAP.md`, `DECISIONS.md`) that go into every project repo. This starter does not keep its own copy.

## Private deployment repo

Owns a specific team's project docs, profile choices, support notes, and deployment checklist. It should still avoid committing credentials, raw platform IDs, transcripts, sessions, memories, logs, or backups.

## Local runtime state

Owns `.env`, live config, route IDs, memory, sessions, scheduled-job state, logs, and backups. This should stay outside git unless explicitly sanitized.

## Change routing

- Reusable pattern → public starter.
- Team-specific setup → private deployment repo.
- Secret or live state → local secret store/runtime only.
- Runtime bug or integration issue → upstream to the runtime project after removing private context.
