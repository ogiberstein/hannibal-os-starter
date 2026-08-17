# Architecture

## V2 boundary

Hannibal OS Starter is a thin reference layer around upstream Hermes.

```text
Upstream Hermes
  Runtime, models, tools, memory, sessions, skills, cron, native profiles,
  profile routing, messaging gateways, configuration, and lifecycle commands.

Thin Hannibal layer
  Role contracts, operator judgment, project-control docs, public-safe examples,
  sanitation, and simple verification guidance.

Private operator state
  Credentials, route IDs, memories, sessions, logs, runtime databases,
  operational evidence, customer data, and recovery material.
```

The public starter must not become another runtime, router, deployment system, recovery platform, or copy of a private control plane.

## Design principles

- **Upstream first:** adopt supported Hermes capabilities before adding local machinery.
- **Native boundaries:** use Hermes profiles for independent state and native `gateway.profile_routes` for supported routing.
- **State outside source:** keep durable/private state separate from replaceable runtime code.
- **Operator-led change:** supervise updates and restarts; make failure observable; keep rollback cheap.
- **Proportionate recovery:** prefer a documented previous-good runtime and ordinary host backup over custom promotion/recovery infrastructure.
- **Explicit limits:** profiles isolate Hermes state but do not sandbox host filesystem access.
- **Public sanitation:** publish role patterns and control docs, never live identifiers or operational state.

## Current role model

- `chief_of_staff`: persistent operator/DM front door and operating-system steward.
- `default`: unmatched fallback and general project operator.
- project profiles: optional bounded lanes for explicit projects or responsibilities.

Routing chooses context. It does not expand authority: credentials, services, routes, production, destructive actions, customer data, and funds remain approval-gated.
