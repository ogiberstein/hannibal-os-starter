# Hannibal OS Starter

> **Status — paused reference:** Commercial and product work on Hannibal OS is paused. This repository remains a public reference starter. It is not an actively supported hosted product, managed service, deployment platform, or promise of future maintenance.

Hannibal OS Starter is a thin, public-safe operating layer for [Hermes Agent](https://github.com/NousResearch/hermes-agent). Upstream Hermes owns runtime execution, models, tools, memory, sessions, skills, cron, profiles, routing, and messaging gateways. This repository adds only reusable role-contract examples, lightweight project-control documents, safety boundaries, and verification checks.

It is intentionally **not** a public copy of a private operating system.

## V2 operating model

| Layer | Owns |
| --- | --- |
| Upstream Hermes | Installation, updates, configuration, profiles, profile routing, gateway lifecycle, tools, memory, sessions, cron, and native rollback/checkpoint features. |
| Thin Hannibal layer | Role contracts, operator judgment, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `AGENTS.md`, public-safe examples, and sanitation checks. |
| Private operator state | Credentials, raw route IDs, profile memory, sessions, logs, evidence, customer data, and recovery material. Keep this outside runtime source and outside this public repo. |

V2 principles:

- adopt current upstream Hermes instead of maintaining a custom runtime fork;
- use native Hermes profiles and `gateway.profile_routes` where supported;
- keep durable/private state separate from replaceable runtime source;
- prefer supervised updates, observable failure, and a cheap previous-good rollback;
- accept bounded recoverable downtime instead of building a second deployment or recovery platform;
- retain strong approval boundaries for credentials, user/customer data, production changes, destructive actions, and funds.

## Chief-of-Staff example

The current example is a **persistent operator/DM front door**:

- `chief_of_staff` handles the operator's direct-message lane, cross-project judgment, prioritization, escalation, and operating-model coherence;
- `default` remains the unmatched fallback and can handle general project work;
- optional project profiles handle explicitly routed, bounded project lanes;
- broad capability does not grant authority to mutate credentials, routes, services, production, customer data, or funds without approval.

This is an operating contract, not a custom router or orchestration service.

## What remains useful here

- project-control templates under `templates/project/`;
- a native Hermes routing **config fragment** under `templates/runtime/config.yaml.example`;
- public-safe command/skill examples under `commands/examples/` and `skills/hannibal-public/`;
- lightweight architecture, profile, preflight, smoke-test, recovery, and security notes;
- sanitation and verification scripts.

Obsolete V1 custom profile YAML, standalone router YAML, managed-deployment environment flags, cgroup-symbol gates, and bespoke restart/recovery guidance have been removed. Historical changelog and review records are evidence only, not current instructions.

## Compatibility truth

This refresh was checked on **2026-08-11** against:

- latest published Hermes release **`v2026.8.3`**, whose annotated tag resolves to commit **`3c27eb6234bf91b8ceee9e9071591b31e9b148cb`**;
- upstream `main` commit **`f51aa6a9b5ce514e15f8e337777f522fd5cc6fa2`** for current documentation/source drift.

At the released commit, source and docs contain native profile creation, profile-local state, gateway multiplexing, and `gateway.profile_routes` with `platform`, optional `guild_id` / `chat_id` / `thread_id`, and `profile`. Unmatched traffic stays on the default/active profile. **Version difference:** `v2026.8.3` warns and falls back to the default home if an explicit route names a missing profile; inspected upstream `main` adds `gateway.multiplex_profile_allowlist` and rejects ingress when the matched profile is missing or disallowed. The included fragment uses the common subset and requires operators to verify every route target before reliance.

Compatibility verification in this repository was **documentation/source inspection plus repository tests only**. No live Hermes profile, route, credential, gateway, service, or runtime was changed or exercised by this pass.

Hermes changes quickly. Treat commands and config below as a pinned example, then check the authoritative current docs before use:

- [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Updating](https://hermes-agent.nousresearch.com/docs/getting-started/updating)
- [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Multiple gateways and profile routing](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)
- [Messaging gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)

## Reference setup

These steps describe the shape of a setup. They are not a managed installation runbook.

### 1. Install and configure upstream Hermes

Use the official installation and setup docs rather than copying installer commands from this repository. Confirm the installed version and health with the current Hermes CLI.

### 2. Verify this starter

```bash
git clone https://github.com/ogiberstein/hannibal-os-starter.git
cd hannibal-os-starter
python3 scripts/verify_repo.py
```

This proves only that the public starter is internally consistent and sanitized. It does not prove a private gateway or route works.

### 3. Create native profiles

Current released Hermes supports native profiles:

```bash
hermes profile create chief_of_staff --description "Persistent operator front door and cross-project coordinator."
hermes profile create project_agent --description "Bounded project execution and evidence-backed status."
hermes profile show chief_of_staff
hermes profile show project_agent
```

Configure each profile through the current Hermes CLI and its own `SOUL.md`, `config.yaml`, and secret store. A profile scopes Hermes state; it is **not** a filesystem sandbox. Set an explicit `terminal.cwd` or use a sandbox backend if that boundary matters.

Do not blindly clone memories, sessions, cron jobs, plugins, credentials, or auth state between roles. Selective inheritance is safer than treating a profile copy as a role design.

### 4. Add native profile routing

`templates/runtime/config.yaml.example` is a fragment to merge into the **default profile's** existing `config.yaml`; it is not a complete replacement config. Replace placeholders only in private state.

The example routes an operator DM to `chief_of_staff`, a bounded project lane to `project_agent`, and leaves unmatched traffic on `default`. Native `profile_routes` require multiplexing to be enabled. The fragment deliberately omits the newer `multiplex_profile_allowlist` key so it remains compatible with the released baseline; operators on newer Hermes may add that key using the current official docs.

After editing, use the current official config and gateway commands to validate and restart through the supported Hermes lifecycle. Do not invent a parallel router service.

### 5. Copy the lightweight control docs

```bash
mkdir -p ../my-project-control
cp -R templates/project/. ../my-project-control/
python3 scripts/render_project_templates.py \
  --project "My Project" \
  --output ../my-project-control \
  --force
```

Use:

- `BRIEF.md` for purpose, scope, and constraints;
- `STATUS.md` for the current gate, blocker, and next step;
- `DECISIONS.md` for durable choices and rationale;
- `AGENTS.md` for agent instructions and approval boundaries.

Keep these durable project truths in a private project/control repository. Keep credentials, raw IDs, memories, sessions, logs, and runtime databases out of it unless a deliberately encrypted private process requires them.

## Optional public command and skill examples

`skills/hannibal-public/` and `commands/examples/` contain generic handover, status, and evidence prompts. This repository does not automatically install these into Hermes. Review and adapt them inside private state; they are not runtime extensions or support commitments.

### 6. Verify the operator journey

Use `docs/runtime-preflight.md` and `docs/smoke-test-playbook.md`. At minimum, prove from a private test surface that:

1. the operator DM reaches `chief_of_staff`;
2. one explicit project lane reaches its project profile;
3. unmatched traffic stays on `default`, and every explicit route target exists so the installed version's missing-target behavior cannot misroute work;
4. status/log evidence is observable without exposing secrets;
5. a separately approved restart or update has a simple rollback path.

Do not claim live compatibility from config parsing or repo tests alone.

## Security and privacy boundaries

Never commit or publish:

- credentials, tokens, private keys, `.env`, or auth files;
- raw user, workspace, server, channel, chat, or thread identifiers;
- profile memories, sessions, transcripts, logs, runtime databases, or backups;
- customer information, private routes, host details, or operational evidence;
- private control-plane scripts or machinery.

Use obvious placeholders such as `CHAT_ID_HERE`, not realistic fake identifiers. Ask before production, credential, permission, deletion, spending, external-message, route, service, or destructive actions.

## Maturity and support

This is a paused v0 reference kit. It has no hosted offering, support SLA, compatibility promise, automatic synchronization process, or deployment service. Fork or copy only the lightweight pieces you understand, and rely on official Hermes documentation for changing runtime behavior.

## Contributing

See `CONTRIBUTING.md`. Public contributions must preserve the sanitation boundary and must not turn this repository into a second runtime, deployment platform, or private-operations mirror.
