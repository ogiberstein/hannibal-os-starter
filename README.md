# Hannibal OS Starter

A public starter for running your own agent operating system on [Hermes Agent](https://github.com/NousResearch/hermes-agent). It is the setup behind the October 2026 Maven workshop *How to ship products with your own agent operating system*, cleaned of anything private.

You get the working parts: the build loop, the agent rulebook, role contracts, project control files, 15 skills, a routing config, and a safe way to update Hermes. Hermes itself does the heavy lifting. This repo is the operating layer on top.

This is a reference, not a product. There is no hosted service, support promise, or compatibility guarantee. Copy what you understand.

## How the system works

Three agents and one human, each with a clear job:

| Who | Where | Job |
| --- | --- | --- |
| You | Phone or laptop | Answer the interview. Approve the spec. Merge the code. |
| Claude Code | Laptop | Writes the spec, slices it, dispatches builds to Hermes, runs reviews. |
| Codex | Laptop | Second opinion: reviews the plan, then the code. |
| Hermes | Always-on server, over Slack | Interviews you, builds each slice and pushes it for review. Keeps working with your laptop shut. |
| Hermes chief of staff | Same server, your DM | Looks in on long runs and flags problems. |

Slack is the conversation. The repo is the record.

### Three profiles

Hermes runs as three profiles from one gateway. Each has its own rulebook, memory, skills and sessions:

| Profile | Gets | Owns |
| --- | --- | --- |
| `chief_of_staff` | Your DM | Cross-project priorities, check-ins on long runs, escalation, keeping the system itself simple. |
| `default` | Every chat no route claims, including project channels | Engineer and PM: interviews, builds, project status. Each project channel gets its context from a channel prompt. |
| `cio` | Your markets channels | A domain lead, here for markets and investing: research, backtests, dashboards. No trades, transfers or spend without your approval. |

Start with `default` alone. Add `chief_of_staff` when you run more than one project. Add a domain lead only when a recurring kind of work needs its own memory and limits. Role contracts for all three are in `templates/soul/`.

### The build loop

1. **Interview.** Hermes asks one question at a time until you agree what is in, what is out, and how you will know it works. Skill: `spec-interview`.
2. **Spec and plan.** Claude writes the spec and slices it into small pieces that each ship on their own. Codex reviews the plan; Claude fixes what it finds. Skills: `writing-plans`, `overengineering-defence`, `implementation-plan-adversarial-review`. **You approve the spec.**
3. **Build.** Hermes builds one slice at a time on a branch, commits and pushes per item, and hands back. The pull request is opened by Claude, or by Hermes when the brief says so. Claude watches the run. Skill: `hermes-build-operations`.
4. **Review.** Claude and Codex check the code in a clean checkout. Skills: `audit-router`, `anti-slop-agent-guardrails`.
5. **Merge.** **You merge.** Then the next slice.

Two checkpoints per build are yours: the spec and every merge. The rest runs on its own. You never hand over money, passwords, customer data, or anything you cannot undo.

The full orchestrator playbook (dispatching over Slack, monitoring a run, clean-context Codex audits, merge hygiene) is in [`docs/claude-hermes-build-loop.md`](docs/claude-hermes-build-loop.md).

### Written down, not remembered

Every project repo carries the same control files. The agents read them before they act and keep them current:

| File | Holds |
| --- | --- |
| `AGENTS.md` | Start here: what the project is, where to look, what needs approval. |
| `BRIEF.md` | What we are doing and for whom. |
| `STATUS.md` | Where we are now, what is blocked, the next step. |
| `ROADMAP.md` | Where we are going, in order. |
| `DECISIONS.md` | Why we chose this. |

Templates are in `templates/project/`.

## What is in this repo

```text
templates/soul/       agent rulebook and role contracts for each Hermes profile
templates/project/    AGENTS, BRIEF, STATUS, ROADMAP, DECISIONS templates
templates/runtime/    config fragment: profile routing and per-channel prompts
skills/               15 skills for Hermes and Claude Code (build, operating, communication)
docs/                 build loop, profiles, runtime updates, preflight, smoke tests, security
scripts/              skill installer, Hermes runtime switcher, sanitation and verification
commands/examples/    prompt examples for three of the skills
```

## Start here

Start on your laptop. Add a server later.

**On your laptop** you need GitHub, Claude Code, and Codex. That is enough to run the interview, spec, plan, and review steps yourself.

**Later, on a server**, add Hermes and Slack so builds run while you sleep and you can steer from your phone.

### 1. Install Hermes

Follow the official [installation guide](https://hermes-agent.nousresearch.com/docs/getting-started/installation). Confirm it runs with `hermes --version` and `hermes doctor`.

### 2. Get this repo and check it

```bash
git clone https://github.com/ogiberstein/hannibal-os-starter.git
cd hannibal-os-starter
python3 scripts/verify_repo.py
```

This proves the starter is consistent and clean. It does not prove your own setup works.

### 3. Install the skills

```bash
scripts/install_skills.sh hermes            # into $HERMES_HOME/skills/<category>/<skill>
scripts/install_skills.sh claude            # into ~/.claude/skills/<skill>
scripts/install_skills.sh claude spec-interview writing-plans   # just some
```

Existing skills with the same name are skipped unless you pass `--force`. For a named Hermes profile, set `HERMES_HOME` to that profile's home first.

### 4. Give each agent its rulebook

Each Hermes profile reads its own `SOUL.md`. Copy `templates/soul/SOUL.md` into each profile, put that profile's role contract on top (`default.role.md`, `chief_of_staff.role.md`, `cio.role.md`), replace `OPERATOR`, and cut any rule that does not match how you work. Short rulebooks get followed. Long ones get skimmed.

### 5. Add profiles and routing (when you want more than one agent)

```bash
hermes profile create chief_of_staff
hermes profile create cio     # optional domain lead; or delete its route from the fragment
```

Every profile a route names must exist; a route to a missing profile makes Hermes reject that chat's messages. Then merge `templates/runtime/config.yaml.example` into the **default** profile's `config.yaml`. It sends your DM to `chief_of_staff`, your markets channel to `cio`, and everything else to `default`. Project channels stay on `default` and get their context from `slack.channel_prompts`, which points each channel at its repo without a new profile. Often that is all you need.

A profile is its own Hermes home (rulebook, config, secrets, memory, skills, sessions). It is not a filesystem sandbox. Read the `agent-role-profile-design` skill before adding another.

### 6. Set up a project

```bash
python3 scripts/render_project_templates.py --project "My Project" --output ../my-project
```

It refuses to overwrite existing files unless you pass `--force`.

### 7. Prove it end to end

From a test chat: your DM reaches `chief_of_staff`; a markets channel reaches `cio`; a project channel stays on `default` and knows its repo; one small slice goes through interview, spec, build, review and merge. Config parsing and green tests here are not that proof. See `docs/smoke-test-playbook.md`.

## Skills

Every skill is a single `SKILL.md` that loads in Hermes and in Claude Code. A few mention Hermes tools or optional upstream skills; in Claude Code, read those as the nearest equivalent.

**Build loop** (`skills/build/`)

- `spec-interview`: an adaptive, one-question-at-a-time requirements interview that ends with a shared model you confirm.
- `writing-plans`: implementation plans with bite-sized tasks, exact paths and test commands, sized to the stakes.
- `overengineering-defence`: cuts a plan to the least machinery that safely unlocks the decision.
- `implementation-plan-adversarial-review`: tests a plan against the real repo before anyone codes.
- `hermes-build-operations`: the builder's contract when a build is dispatched over Slack.
- `audit-router`: picks the review type, depth and verdict format. MVP depth by default.

**Operating** (`skills/operating/`)

- `agent-role-profile-design`: which roles deserve their own profile, and how to pilot one.
- `true-stuck-check-reporting`: reports only work that is truly stuck, not waiting or parked.
- `workstream-kill-and-archive-docs`: makes a repo tell the truth when you kill or park a project.
- `status-refresh`: refreshes `STATUS.md` from evidence.
- `handover-bootstrap`: builds a handover packet for a new agent or session.
- `evidence-gate`: go/no-go with claims separated from proof.

**Communication** (`skills/communication/`)

- `plain-style`: plain English for docs, READMEs and copy.
- `anti-slop-agent-guardrails`: makes it hard for an agent to look done without being done.
- `user-interview-operator`: neutral customer discovery interviews and decision-ready summaries.

Hermes also ships useful skills of its own, such as `systematic-debugging`, `test-driven-development` and `requesting-code-review`. For deeper adversarial thinking, see [claude-thinking-skills](https://github.com/ogiberstein/claude-thinking-skills) (`premortem`, `paranoid-review`, `mental-models`, `steelman`).

## The quality bar

The rulebook defaults every agent to an MVP standard: simplicity and speed beat polish, no backwards compatibility unless someone depends on it, fix blockers and list the rest, one review pass, and every new safeguard must name what it protects. Full rigour is kept for money, secrets, customer data, legal exposure, public products, and irreversible deletion.

This came from experience. Without it, agents treat a weekend project like bank infrastructure: they audit every "done", fix every finding, and build safety machinery that costs more than the failures it prevents.

## Updating Hermes

On a laptop, `hermes update` is fine. On a server, keep the previous release installed next to the new one so a bad update is one command away from undone. See [`docs/runtime-updates.md`](docs/runtime-updates.md) and `scripts/hermes-runtime.sh`.

## Compatibility

Checked on 2026-10-23 against Hermes **v0.22.2** source and the **v0.22.5** docs (latest release at the time). In those versions:

- `hermes profile create` makes an isolated Hermes home per profile;
- `gateway.multiplex_profiles` plus `gateway.profile_routes` route chats to profiles; the most specific route wins and unmatched chats stay on `default`; a route to a missing profile is rejected;
- `slack.channel_prompts` injects per-channel context on every turn;
- the older `gateway.multiplex_profile_allowlist` key is retired.

This was checked by reading source, docs and running this repo's tests. Nothing in this pass changed or exercised a live gateway. Hermes moves fast; check the official docs: [configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration), [profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles), [multi-profile gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways), [Slack](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack), [updating](https://hermes-agent.nousresearch.com/docs/getting-started/updating).

## Keep private things private

Never commit or publish credentials, tokens, keys, `.env` or auth files; raw user, channel or chat IDs; agent memories, sessions, transcripts, logs, databases or backups; or customer information. Use placeholders such as `CHAT_ID_HERE`. `scripts/sanitize_repo.py` checks this repo for the common cases and runs in CI.

Ask before production, credential, permission, deletion, spending, external-message, route, service, or destructive actions. The rulebook says the same to your agents.

## Credits

`writing-plans` is adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT). The review modes in `audit-router` are inspired by [garrytan/gstack](https://github.com/garrytan/gstack) (MIT). Hermes Agent is by [Nous Research](https://github.com/NousResearch/hermes-agent).

## Contributing

See `CONTRIBUTING.md`. Contributions must keep the sanitation boundary and must not turn this repo into a second runtime or a mirror of anyone's private operations.
