# Architecture

## Boundary

Hannibal OS Starter is a thin reference layer around upstream Hermes. Claude Code and Codex sit beside it on the operator's laptop: Claude specs and orchestrates, Codex reviews, Hermes builds on an always-on server (see `docs/claude-hermes-build-loop.md`).

```text
Upstream Hermes
  Runtime, models, tools, memory, sessions, skills, cron, native profiles,
  profile routing, messaging gateways, configuration, and lifecycle commands.

Thin Hannibal layer
  Agent rulebook and role contracts, project-control docs, skills, the build
  loop, a runtime switcher, sanitation, and simple verification guidance.

Private operator state
  Credentials, route IDs, memories, sessions, logs, runtime databases,
  operational evidence, customer data, and recovery material.
```

The public starter must not become another runtime, router, deployment system, recovery platform, or copy of a private control plane.

## Design principles

- **Upstream first:** adopt supported Hermes capabilities before adding local machinery.
- **Native boundaries:** use Hermes profiles for independent state, native `gateway.profile_routes` for routing, and `slack.channel_prompts` for per-channel project context.
- **MVP by default:** simplicity and speed beat polish; full rigour only for money, secrets, customer data, legal exposure, public products, and irreversible deletion.
- **State outside source:** keep durable/private state separate from replaceable runtime code.
- **Operator-led change:** supervise updates and restarts; make failure observable; keep rollback cheap.
- **Proportionate recovery:** prefer a previous-good runtime kept next to the live one (`docs/runtime-updates.md`) and ordinary host backup over custom promotion/recovery infrastructure.
- **Explicit limits:** profiles isolate Hermes state but do not sandbox host filesystem access.
- **Public sanitation:** publish role patterns and control docs, never live identifiers or operational state.

## Current role model

- `chief_of_staff`: persistent operator/DM front door and operating-system steward.
- `default`: unmatched fallback and general project operator.
- `cio`: an optional domain lead (here markets and investing) routed to its own channels.
- project channels: stay on `default`, with per-channel context from `slack.channel_prompts`.

Routing chooses context. It does not expand authority: credentials, services, routes, production, destructive actions, customer data, and funds remain approval-gated.
