# Backup, Rollback, and Recovery

Keep recovery proportional and separate runtime code from durable state.

## Separate the assets

- **Replaceable runtime:** upstream Hermes source/package and its exact release/commit.
- **Durable private state:** config, secrets, auth, profiles, memories, sessions, skills, cron, and state databases.
- **Project truth:** private Git repositories containing `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `AGENTS.md`, and project artifacts.

A runtime rollback is not automatically a state rollback. Stop if a newer runtime may have changed state in a way the previous version cannot read.

## Preferred approach

- use upstream Hermes backup/export/checkpoint features that exist in the installed version;
- keep one known previous-good runtime/version before supervised changes;
- use ordinary encrypted host/off-host backup appropriate to the value at risk;
- document one short manual recovery path;
- verify recovery only to the depth justified by the consequence of failure.

Do not build a custom deployment transaction, immutable promotion system, self-repair daemon, or bespoke recovery platform from this starter.

## Never publish

Do not commit backup archives, `.env`, auth files, raw route IDs, memories, sessions, logs, runtime databases, customer data, or operational evidence to this repository.

Use the official [updating](https://hermes-agent.nousresearch.com/docs/getting-started/updating), [profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles), and current backup/import documentation for the installed Hermes version.
