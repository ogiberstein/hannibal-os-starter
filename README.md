# Hannibal OS Starter

Set up a private, single-tenant Hermes agent workspace with reusable profiles, channel routing, project memory docs, safety boundaries, and deployment checklists.

Hannibal OS Starter is the public-safe scaffold around a Hermes-style runtime. Hermes runs the agents. This repo helps you turn that runtime into an operating layer for a founder/operator or small team: Chief-of-Staff and project-agent profiles, explicit context files, messaging routes, preflight checks, smoke tests, and backup/recovery playbooks.

## Why use this?

Installing an agent runtime is only the beginning. The hard part is making it useful and safe in a real operating context:

- Which project context should the agent trust?
- Which channel maps to which agent profile?
- Where do decisions and current status live?
- What must never go into git?
- How do you know the gateway, routing, scheduler, and recovery path actually work?
- How do you improve the setup without leaking private state?

This starter gives you the missing operating scaffold so you do not improvise those rules after the first incident.

## Who this is for

Use this if you are:

- a technical founder/operator setting up Hermes for yourself or a small team;
- building project-aware agents for Slack, Discord, Telegram, email, or another messaging surface;
- creating a private AI Chief-of-Staff / project-agent workspace;
- looking for a safe public template before building a private deployment.

Do **not** use this if you want a hosted SaaS, a managed deployment, a compliance guarantee, or a complete production runtime in this repo.

## What you get

- Chief-of-Staff and project-agent profile templates.
- Runtime config, `.env`, and profile-router examples.
- Project memory docs: `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `AGENTS.md`.
- Messaging-route pattern for mapping channels to profiles.
- First-deployment checklist.
- Runtime preflight checklist.
- Smoke-test playbook for routing, default/CoS, recovery, and scheduled updates.
- Backup/restore, support-boundary, and transparent-learning docs.
- Sanitation and verification scripts to keep the public repo safe.

## How this relates to Hermes

| Layer | What it owns | Example |
| --- | --- | --- |
| Hermes runtime | agent execution, tools, models, memory, scheduler, gateway adapters | Hermes checkout/package and runtime home |
| Hannibal OS Starter | public-safe templates, operating docs, safety checks, smoke tests | this repo |
| Private deployment | real `.env`, channel IDs, local config, project docs, runtime state | your private instance directory/repo |

This repo does **not** install or replace Hermes. Install/run Hermes separately, then use this starter to create the config/profile/project layer around it.

## Start here: “I want to set up Hermes”

The safe path is: public starter repo → separate private deployment workspace → Hermes runtime → preflight → smoke tests.

### 0. Prerequisites

You need:

- Python 3.
- Git.
- A Hermes runtime checkout/package or another compatible agent runtime.
- A model-provider key or router key stored locally, not in git.
- Optional: a Slack/Discord/Telegram/email bot or app for messaging access.

### 1. Clone and verify the starter

```bash
git clone https://github.com/ogiberstein/hannibal-os-starter.git
cd hannibal-os-starter
python3 scripts/verify_repo.py
```

This verifies the public starter itself: Python syntax, whitespace, sanitation rules, and tests. It does **not** prove your private Hermes runtime is configured yet.

### 2. Create a separate private deployment workspace

Do not put live `.env`, channel IDs, sessions, memories, logs, or backups in this public starter checkout.

```bash
mkdir -p ../my-hermes-instance
cp templates/runtime/env.example ../my-hermes-instance/.env
cp templates/runtime/config.yaml.example ../my-hermes-instance/config.yaml
cp templates/runtime/profile_router.yaml.example ../my-hermes-instance/profile_router.yaml
cp -R templates/project ../my-hermes-instance/project
mkdir -p ../my-hermes-instance/profiles
cp templates/profiles/chief_of_staff.yaml.example ../my-hermes-instance/profiles/chief_of_staff.yaml
cp templates/profiles/project_agent.yaml.example ../my-hermes-instance/profiles/project_agent.yaml
```

Optional: render the project docs with a project/team name:

```bash
python3 scripts/render_project_templates.py \
  --project "My Team" \
  --output ../my-hermes-instance/project \
  --force
```

If you want to version the private deployment, initialize a **private** repo in `../my-hermes-instance` and keep `.env`, raw route IDs, runtime state, logs, sessions, memories, and backups ignored.

### 3. Point the private deployment at Hermes

Edit `../my-hermes-instance/.env` and `config.yaml` locally:

```text
AGENT_RUNTIME=hermes
RUNTIME_HOME=LOCAL_RUNTIME_HOME_HERE
RUNTIME_REF=PINNED_RUNTIME_VERSION_HERE
WORKSPACE_DIR=LOCAL_WORKSPACE_DIR_HERE
MODEL_API_KEY=SET_LOCALLY_ONLY
MESSAGING_BOT_TOKEN=SET_LOCALLY_ONLY
```

Use your actual Hermes runtime path/home/workspace values. Keep secrets in local `.env` or a secret manager. Do not paste them into docs, issues, pull requests, chat, or commits.

### 4. Configure profiles and routes

Edit `../my-hermes-instance/profile_router.yaml`:

```yaml
routes:
  - label: chief-of-staff-default
    platform: PLATFORM_NAME_HERE
    target: CHANNEL_ID_HERE
    profile: chief_of_staff

  - label: project-channel
    platform: PLATFORM_NAME_HERE
    target: PROJECT_CHANNEL_ID_HERE
    profile: project_agent
```

Replace placeholders only in your private deployment. The router should map each messaging surface to a profile in `../my-hermes-instance/profiles/`.

### 5. Fill the project memory docs

Edit the copied files under `../my-hermes-instance/project/`:

- `BRIEF.md` — what this workspace is for, users, scope, risks.
- `STATUS.md` — current phase, gate, next step, blockers.
- `DECISIONS.md` — durable decisions and why they were made.
- `AGENTS.md` — operating instructions and boundaries for agents.

These docs are the lightweight memory/control plane for your private workspace.

### 6. Run a private runtime preflight

Use `docs/runtime-preflight.md` as the checklist. A good preflight confirms presence only:

- local `.env` exists;
- required key names are present;
- config and profile router exist;
- Hermes runtime checkout/package exists;
- placeholders are replaced in private config;
- diagnostics do not print secret values or raw platform IDs.

Do not source `.env` as shell code just to inspect it. Do not print secret values.

### 7. Start Hermes / gateway

Start Hermes using the command recommended by your Hermes install/runtime. Keep the runtime home and workspace pointed at your private deployment, not this public starter checkout.

This repo intentionally does not hard-code a Hermes start command because runtime packaging and gateway adapters can change. The invariant is stable: Hermes owns execution; this starter owns the operating scaffold around it.

### 8. Smoke test the four required loops

Use `docs/smoke-test-playbook.md` and prove:

1. project channel routes to `project_agent`;
2. default/Chief-of-Staff route reaches `chief_of_staff`;
3. restart/recovery preserves config and routes;
4. one scheduled update delivers once to the intended test target.

Record evidence privately. Redact raw IDs, message contents, secrets, logs, transcripts, sessions, and memory files before sharing anything.

### 9. Decide go/no-go

Before relying on the setup:

- complete `docs/first-deployment-checklist.md`;
- document support boundaries using `docs/support-boundaries.md`;
- document backup/restore using `docs/backup-restore.md`;
- decide how improvements flow using `docs/improvement-propagation.md`;
- keep learning/observability explicit using `docs/transparent-learning.md`.

## Repository layout

```text
docs/        Architecture, safety boundaries, and operating playbooks.
templates/   Runtime, profile, and project-doc examples with placeholders only.
scripts/     Sanitation, verification, and template-rendering helpers.
tests/       Regression tests for public-safe templates and scans.
```

## Security defaults

- Keep secrets in local `.env` or a password manager, never in git.
- Use obvious placeholders such as `CHANNEL_ID_HERE`; avoid fake numeric IDs that look real.
- Diagnostics should report presence/status only, not values.
- Ask before production, credential, permission, deletion, spending, or external-message actions.
- Do not commit transcripts, logs, sessions, memories, backups, customer data, or deployment evidence containing private identifiers.

## What “done” looks like

A private Hermes workspace is ready for real use only when:

- starter verification passes;
- private runtime preflight passes without printing secrets;
- profile/router mapping is explicit and tested;
- four smoke-test loops pass;
- backup/restore path is documented;
- support and improvement boundaries are clear;
- no live secrets, raw IDs, logs, sessions, memories, or backups are committed.

## Maturity

This is a v0 starter/reference kit. Treat it as an operating pattern and checklist, not production infrastructure.

## Contributing

See `CONTRIBUTING.md`. Public contributions must not include private customer data, raw platform IDs, credentials, transcripts, logs, memories, sessions, or backups.
