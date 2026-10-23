---
name: agent-role-profile-design
description: Use when deciding which agent roles deserve their own Hermes profile, re-baselining a role catalog after an upgrade, or planning a first profile pilot and chat routing. Favors the smallest profile set that improves real owner outcomes.
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [agent-os, profiles, role-design, multi-agent, routing, rollout]
    related_skills: [spec-interview, writing-plans, overengineering-defence, implementation-plan-adversarial-review, anti-slop-agent-guardrails]
---

# Agent Role Profile Design

## Purpose

Design or re-baseline your set of agent roles before you create profiles,
change chat routes or enable multi-agent dispatch.

The central distinction:

> A profile is a durable state and policy boundary, not a job title or a
> prompt template.

Aim for the smallest profile model that repeatedly improves the owner's
outcomes. Do not fill out a role catalog for symmetry.

## Use when

- Deciding which proposed roles deserve a separate profile.
- Re-baselining an old profile design after a Hermes upgrade.
- Choosing between a profile, a skill, a temporary mode, a delegated agent,
  project context or a task-board assignee.
- Defining a chief-of-staff, engineering, product, design, research or
  domain profile.
- Picking the first profile pilot and its owner journey.

Not for routine profile creation after the role model is approved. Use the
Hermes docs for the mechanics.

## Required posture

1. **Planning and implementation are separate gates.** A request to discuss,
   review or plan does not authorize creating profiles, editing config,
   changing routes or credentials, or restarting services.
2. **Inspect current behavior.** Read your installed Hermes version, its
   profile docs and your live config. Old design docs describe desired state,
   not current capability.
3. **Start from owner value.** Name a recurring journey and the decision it
   improves, not infrastructure completeness.
4. **Prefer cheap recovery to speculative machinery.** Keep strong boundaries
   for secrets, destructive actions, production, customer data, legal exposure
   and money. Accept manual invocation when automation would cost more than
   the failure it prevents.
5. **Bound the investigation.** One inspection and one synthesis are usually
   enough. Reopen only for a reproduced blocker or a material change in risk.

## What a Hermes profile is (and is not)

Check these against your installed version before relying on them.

- `hermes profile create <name>` makes a separate home under
  `$HERMES_HOME/profiles/<name>/` with its own `SOUL.md`, `config.yaml`,
  `.env`, skills, memory, sessions, cron jobs and logs.
- **A profile is not a filesystem sandbox.** On the local terminal backend the
  agent has the same file access as your user account. `terminal.cwd` only
  sets where commands start.
- **Clone options copy more than you might expect.** In recent releases
  `--clone` copies `config.yaml`, `.env` (your secrets), `SOUL.md`, skills,
  plugins and the curated memory files; `--clone-all` copies nearly
  everything except history and cron jobs. Prefer selective inheritance
  (below).
- **Routing chats to profiles:** set `gateway.multiplex_profiles: true` on the
  default profile, then list `gateway.profile_routes`. Each route matches a
  `platform` plus any of `chat_id`, `thread_id`, `user_id` or `guild_id`; the
  most specific match wins and unmatched messages go to `default`.
- **Per-channel context without a new profile:** `slack.channel_prompts` maps
  a channel ID to a prompt injected on every turn. Often this is all a
  "role" needs.
- **One credential owner per bot token.** A given platform token lives in
  exactly one profile's `.env`. A second profile that reuses the token is
  refused or parked, not started as a second poller. With multiplexing, routes on the default profile's shared bot are
  the usual way to reach other profiles.
- **Credential isolation depends on version.** Some releases let a profile
  with no provider key fall back to the default profile's provider login.
  Check before you claim isolation.

Example route block (placeholders, not real IDs):

```yaml
gateway:
  multiplex_profiles: true
  profile_routes:
    - name: owner-dm
      platform: slack
      chat_id: "<your-dm-channel-id>"
      profile: chief_of_staff
```

## Recommended starting shape

- **chief_of_staff:** the front door. Usually the owner's DM.
- **default:** the engineer/PM fallback for project channels and anything
  unmatched.
- **Optional domain profiles** (for example a domain lead for markets or
  research): add only when a recurring journey proves the need.
- **Spec, review and build work** (for example Claude Code writing specs,
  Codex reviewing, Hermes building) is usually done by delegated tools and
  agents, not by more profiles.

## Workflow

### 1. Establish current truth

Record four layers separately:

1. **Owner outcome:** what repeated work should improve.
2. **Upstream capability:** what your Hermes version provides.
3. **Live configuration:** what you have actually enabled.
4. **Historical machinery:** what an older setup built, and why.

A feature present upstream is not necessarily enabled. A historical control
is not necessarily still needed. Inspect the profile list, routing settings
and task-board identity config without printing secrets.

### 2. Build the boundary matrix

For each proposed profile, ask whether it needs durable separation of:

| Boundary | Question |
|---|---|
| Soul/persona | Must its behavior persist across unrelated sessions? |
| Memory | Does specialist memory improve repeated decisions, or fragment shared truth? |
| Skills | Is a stable, focused skill set better than loading skills on demand? |
| Tools/policy | Does it need a different tool surface or approval boundary? |
| Credentials | Are separate credentials truly needed, and does your version enforce isolation? |
| Sessions | Is a separate history worth the switching cost and split search? |
| Workspace | Does anything bind it to a workspace, or must cwd still be supplied? |
| Routing | Is a persistent chat route needed, or is explicit invocation enough? |
| Task-board identity | Does a real workflow need a persistent named assignee? |

Then name the burden: duplicated config, souls, skills and credentials;
fragmented memory and sessions; switching friction; routing complexity;
contradictory doctrine across profiles; more homes to check after each
upgrade; and false claims of isolation.

### 3. Classify every role

- **Profile:** only when durable identity, state or policy gives repeated
  value that invocation or delegation cannot cheaply reproduce. A profile
  should usually buy at least two real boundaries (for example specialist
  memory plus separate sessions, or focused policy plus a task-board
  identity).
- **Skill, mode or delegated agent:** when the specialization is a reasoning
  lens, an artifact workflow, project context or a bounded task. Typical
  cases: design and content work driven by skills; product management grounded
  in repo docs; engineering execution by task-scoped delegated agents;
  decision coaching through a template; research or review lenses.
- **Defer:** when a profile may become useful after a specific dependency
  exists. Name the evidence that would reopen it.
- **Delete from the catalog:** when the title adds symmetry but no boundary.
  Keep the useful behavior as a skill.

## Chief-of-staff pattern

A chief-of-staff profile earns its place when it is a separate, recurring
operating surface, not a copy of `default`.

It owns:

- cross-project priority, conflicts, opportunity cost and decision quality;
- coherence of status, brief, roadmap and decision docs;
- proportional safeguards, cheap rollback and pressure to delete;
- stopping rules for reviews, so process does not become the product;
- delegating product, engineering, design, research and execution;
- escalating high-consequence decisions to the owner.

It does **not** get:

- unilateral changes to runtime, routes, credentials, services, production or
  money;
- permanent review or hardening loops;
- routine project management for every workstream;
- authority to override specialist judgment without evidence.

Broad tool access is not mutation authority. Live runtime, credential, route,
production, destructive, customer-data and money actions still need owner
approval.

Resolve identity first: if `default` already acts as chief of staff, either
keep it there or make `default` the general fallback and the chief of staff
a separate front door. Building both without deciding creates duplicate
souls, memory and confusion.

## First-profile selection

Compare candidates on: immediate owner value; build and operating
complexity; reversibility; what it teaches about specialization; dependence on
routes, credentials, task boards or service changes; and the risk that a
temporary role becomes permanent infrastructure.

Challenge inherited ordering. An engineering worker should not go first just
because an old task-board plan needed an assignee. Without the task board, it
is a worse version of a delegated agent and teaches little.

## Thin pilot contract

- one profile;
- one real owner journey, optionally with a second touch to test continuity;
- explicit invocation first, or one exact route if invocation would make the
  pilot artificial;
- no broad routes, task boards, dashboards, new credentials or second profile;
- one success/failure test declared up front;
- cheap rollback and one stopping rule.

**Success looks like:** it changed or sped up a real decision; the follow-up
needed less steering; it kept its role boundary; its work beat `default` or
an invoked skill; the switching cost was acceptable.

**Failure looks like:** output indistinguishable from `default`; duplicated or
contradictory memory; frequent use of the wrong profile; setup complexity
before value appears; no second use in the window; drift into unapproved
execution or infrastructure work.

**Rollback:** stop invoking and remove one un-routed profile after saving any
useful artifact. Avoid first pilots whose rollback needs route migration,
gateway repair or credential rotation.

**Stopping rule:** at the end of the window decide `keep`, `adjust once for an
observed defect`, or `delete`. Do not start the next profile until then.

## Discussion protocol

1. Present the synthesis: purpose, role classification, chief-of-staff
   boundaries, 2-3 viable pilots, a recommendation and only the material open
   decisions.
2. Challenge redundant roles and inherited sequencing directly.
3. Lead with owner value, then mechanics. Use plain English.
4. Ask one decision question at a time. The first is usually the identity
   question (is `default` the chief of staff, or the fallback?).
5. No implementation plan until the role model and first profile are agreed.

## Implementation traps

Use only after the pilot is approved.

1. **Selective inheritance over cloning.** Create the profile, then copy only
   what is worth inheriting: `SOUL.md`, chosen skills, curated durable memory
   and non-secret config. Start with fresh sessions. Do not copy `.env`,
   auth files, state databases, cron jobs, sessions or platform tokens.
2. **Set role policy in the profile config:** working directory, task-board
   dispatch off unless in scope, approval-sensitive actions kept manual,
   shared secret references removed.
3. **Prove secret exclusion before any restart:** `.env` has no active lines
   you did not intend; no auth file was copied; cron is empty; no sessions
   were copied. A working model call proves auth works, not that credentials
   are isolated.
4. **Inventory every existing profile before enabling multiplexing,**
   including stopped ones. The multiplexer serves every live named profile, so
   one route can bring an unrelated profile's adapters, cron or dispatch
   online. Park it reversibly, approve the wider activation, or defer
   routing. Never let it start as a side effect.
5. **Verify config types, not command success.** After setting nested values
   (such as `gateway.profile_routes`) via the CLI, read the YAML back and
   confirm `profile_routes` is a list and `multiplex_profiles` is a boolean.
   Then test one matching chat and one unmatched control chat that should
   fall back to `default`.
6. **Back up before you change.** Save the default `config.yaml` (mode 600)
   and write a restore step before touching routes.
7. **Don't restart the gateway from a chat that runs through that gateway.**
   Use a separate shell or detached service, and plan how you will verify and
   report after the restart.
8. **Test routing and profile value separately.** Doing both at once makes
   results ambiguous and rollback larger. Keep project-channel escalation
   manual during the first pilot.

## Common pitfalls

- Confusing a behavior overlay (prompt, channel prompt, skill) with a state
  boundary.
- Rebuilding old lifecycle machinery (readiness, quarantine, attestation) by
  default. It must justify itself against current assets and failure costs.
- Letting the chief of staff become an infrastructure maximizer. Stewardship
  includes deleting and stopping.

## Verification checklist

- [ ] Installed version and live config were checked.
- [ ] Upstream capability, live config and historical machinery are separated.
- [ ] Every role is classified: profile / skill-mode-delegate / defer-delete.
- [ ] Benefits and burdens are named for each profile.
- [ ] Workspace and credential isolation claims were checked, not assumed.
- [ ] Chief-of-staff mutation boundaries are explicit.
- [ ] The inherited first-profile choice was challenged.
- [ ] The pilot has one role, one journey, evidence, rollback and a stopping rule.
- [ ] Task boards, dashboards, credentials, routes and extra profiles stay out
      unless the chosen journey needs them.
- [ ] Only one material decision question is asked at a time.
