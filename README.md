# Hannibal OS Starter

A starter kit and reference architecture for running a private, single-tenant AI operating system for a founder/operator or small team.

Hannibal OS Starter is intentionally small: it gives you templates, safety boundaries, and operating checklists for project-aware agents. It does **not** ship a hosted service or a complete production runtime.

## What this is

- A reference architecture for a private agent operating system.
- Sanitized templates for profiles, project docs, runtime config, and channel routing.
- Checklists for first deployment, smoke testing, backup/restore, and improvement propagation.
- A safety-first repo scaffold with sanitation and verification scripts.

## What this is not

- Not a hosted SaaS.
- Not a managed customer deployment.
- Not a security, privacy, or compliance guarantee.
- Not a replacement for an agent runtime such as Hermes or another provider.
- Not a place to store live credentials, memories, transcripts, sessions, or channel IDs.

## Mental model

```text
Agent runtime
  Executes agents, tools, model calls, memory, sessions, cron/schedules, messaging adapters.

Hannibal OS Starter
  Defines templates, repo boundaries, safety checks, smoke tests, and operating playbooks.

Local/private instance
  Owns .env, live config, channel IDs, memory, sessions, logs, deployment evidence, and backups.
```

Keep those layers separate. The public starter should stay generic; each private instance owns its own state.

## Quick start

```bash
git clone https://github.com/YOUR-USER/hannibal-os-starter.git
cd hannibal-os-starter
python3 scripts/verify_repo.py
```

Then copy examples into a private instance or scratch directory:

```bash
cp templates/runtime/env.example .env
cp templates/runtime/config.yaml.example config.yaml
cp templates/runtime/profile_router.yaml.example profile_router.yaml
```

Replace placeholders locally. Do not commit `.env`, live channel IDs, credentials, sessions, memories, logs, or backups.

## Core workflows

1. Create a project brief and status file from `templates/project/`.
2. Add a Chief-of-Staff or project-agent profile from `templates/profiles/`.
3. Route one messaging surface to that profile using placeholder config as a guide.
4. Run the first-deployment checklist.
5. Smoke test the four required loops: project channel, default/CoS, restart/recovery, scheduled update.
6. Record decisions and improvements without committing private runtime state.

## Security defaults

- Keep secrets in local `.env` or a password manager, never in git.
- Diagnostics should report presence/status only, not values.
- Use obvious placeholders such as `CHANNEL_ID_HERE`; avoid fake numeric IDs that look real.
- Do not commit transcripts, logs, sessions, memories, backups, customer data, or deployment evidence containing private identifiers.

## Repository layout

```text
docs/        Architecture, safety boundaries, and operating playbooks.
templates/   Runtime, profile, and project-doc examples with placeholders only.
scripts/     Sanitation and verification helpers.
tests/       Regression tests for public-safe templates and scans.
```

## Maturity

This is a v0 starter/reference kit. Treat it as an operating pattern and checklist, not production infrastructure.

## Contributing

See `CONTRIBUTING.md`. Public contributions must not include private customer data, raw platform IDs, credentials, transcripts, logs, memories, sessions, or backups.
