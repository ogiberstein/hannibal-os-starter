# Runtime Preflight

A preflight answers: "Is current upstream Hermes configured enough for a private smoke test?" It must not expose secrets and it must not mutate live state.

## Read-only checks

Use the current official CLI to confirm:

- installed Hermes version and install method;
- `hermes doctor` / config validation results;
- required native profiles exist and show the intended profile homes;
- each profile has an explicit role contract and, where needed, an explicit `terminal.cwd`;
- the default profile's config contains only intended `gateway.profile_routes`;
- every routed profile is installed; if the installed Hermes supports a multiplex allowlist, every routed profile is allowed;
- gateway status and bounded logs are observable without printing credentials or raw IDs;
- a previous-good runtime or other cheap rollback target is known before an approved update/restart.

CLI and config details change. Use the official [configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration), [profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles), [updating](https://hermes-agent.nousresearch.com/docs/getting-started/updating), and [gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) documentation for exact current commands.

## Do not

- source `.env` as shell code merely to inspect it;
- print secret values, auth files, raw route IDs, memories, sessions, logs, or backups;
- modify profiles, routes, credentials, services, cron, or runtime during a read-only preflight;
- require obsolete custom router files, managed-deployment flags, private runtime symbols, cgroup unit names, or bespoke service wrappers;
- call config parsing, repo tests, or `active (running)` proof of an end-to-end messaging route.

This repository does not provide or verify a custom deployment/hardening contract.
