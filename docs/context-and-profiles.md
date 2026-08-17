# Context and Profiles

Use native Hermes profiles as independent Hermes homes. Each profile has its own configuration, secrets, role contract, memories, sessions, skills, cron jobs, logs, and state database.

A profile is not a filesystem sandbox. On the local terminal backend it normally has the same OS-user access as the process running Hermes. Use an explicit `terminal.cwd`, tool restrictions, or a sandbox backend when stronger boundaries matter.

## Chief-of-Staff model

The recommended example is:

- `chief_of_staff` is the persistent operator/DM front door for cross-project judgment, prioritization, escalation, retrospectives, and control-doc coherence;
- `default` handles unmatched traffic and general project work;
- project profiles receive only explicit bounded routes;
- project escalation returns to the operator/DM lane rather than creating hidden cross-project authority.

Broad tools and end-to-end accountability do not authorize unilateral production, route, service, credential, permission, destructive, customer-data, or funds-impacting changes.

## Role contract

Keep each profile's `SOUL.md` concise and explicit about:

1. role and outcome;
2. trusted source hierarchy;
3. project/control documents it maintains;
4. tool and workspace expectations;
5. approval boundaries;
6. escalation and handoff behavior.

Keep durable project truth in `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, and `AGENTS.md`. Treat profile memory and session summaries as navigation, not proof.

## Safe profile creation

Use the current official profile commands. Prefer a fresh profile plus selective configuration over blind copying of memory, sessions, cron, plugins, credentials, or auth state.

Changing `SOUL.md` takes effect cleanly in a new session. Verify the active profile and working directory directly; asking the model to describe them is not isolation proof.

Official source: [Hermes profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles).
