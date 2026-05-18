# Architecture

Hannibal OS Starter separates three concerns:

```text
Agent runtime
  Tools, model calls, gateway adapters, schedules, memory, sessions, and execution.

Starter repository
  Templates, docs, public-safe examples, checklists, and verification scripts.

Private instance
  Local credentials, live config, channel IDs, memory, sessions, logs, backups, and evidence.
```

The starter should remain generic. A private instance can adapt it to a specific runtime, workspace, and messaging surface.

## Design principles

- Single-tenant first.
- Explicit project/profile boundaries.
- Local ownership of secrets and live state.
- Presence-only diagnostics.
- Boring recovery and rollback docs before live use.
- Improvement propagation that separates reusable lessons from private instance state.

## Profile loop

A useful agent profile usually declares:

1. role and operating stance
2. source/context boundaries
3. allowed tools and risk posture
4. delivery surface
5. status/decision artifacts it maintains
6. escalation conditions for human approval
