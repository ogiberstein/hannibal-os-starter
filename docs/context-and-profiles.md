# Context and Profiles

A profile is a scoped operating contract for an agent.

## Suggested profile fields

- `name`: short profile name.
- `role`: what the agent is responsible for.
- `sources`: allowed context sources.
- `tools`: allowed capabilities.
- `risk_posture`: when to ask before acting.
- `deliver_to`: human-readable delivery label, not a raw platform ID.
- `status_artifacts`: files the agent should maintain.

## Source boundaries

Prefer explicit source lists over broad implicit memory. Treat memory and summaries as navigation, not proof. Runtime logs, repo state, docs, and commands are better evidence than recalled context.

## Example profile types

- Chief-of-Staff: cross-project triage, reminders, summaries, status discipline.
- Project Operator: project-specific execution, docs, evidence, and handoff.
- Reviewer: adversarial review, readiness checks, leak checks, and go/no-go calls.
