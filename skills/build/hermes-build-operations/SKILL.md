---
name: hermes-build-operations
description: "Use when Hermes receives, runs, resumes, or hands back a build that an orchestrator (such as Claude Code) dispatched over Slack. Builder-side contract: scope, commit and push per item, continuation triggers, mid-run thread posts, and the approvals Hermes cannot grant itself."
version: 1.1.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [hermes, build, dispatch, slack, builder, handback, continuation]
    related_skills: [audit-router, writing-plans, anti-slop-agent-guardrails, true-stuck-check-reporting, evidence-gate, status-refresh]
---

# Hermes Build Operations (builder side)

Load this skill when a Slack message dispatches a build to you, when a thread
asks you to continue or remediate one, or when you prepare a handback. The
orchestrator (usually Claude Code on the operator's laptop) wrote the brief.
The operator approved it. You build. Others review. The operator merges.

The orchestrator-side rules live in the companion guide
`docs/claude-hermes-build-loop.md`. This skill is the part you must follow.

## Authority and scope

- The dispatch message and the approved brief are your whole authority. They
  cover building on the named branch. They do not cover merging, deploying,
  production changes, scope changes, or starting other sessions.
- A green build or a passing review is not permission to merge or deploy.
  The operator approves the spec and every merge.
- Your own closure audit is input, not the verdict. The orchestrator runs an
  independent audit on its own machine. Builders audit optimistically.
- Independent review (for example the Codex CLI) runs on the orchestrator's
  machine. If the review CLI on your host is unauthenticated by design, do not
  log it in or call it.
- Treat review findings as evidence to check. Confirm a material finding
  against the code or runtime before you change anything for it.

## Operating contract

1. **Read before you build.** Read the brief in full and the repo's
   `AGENTS.md`. If the brief lives on `main`, read it with
   `git show origin/main:<path>`. Do not merge `main` into your branch to get it.
2. **Check out the named branch.** A fresh session inherits whatever branch
   the checkout is on. Fetch, switch, and pull before the first edit.
3. **Check environment facts on the branch.** Read pins such as
   `.python-version` and the lockfile from the branch. Pins move between
   builds. Build the virtualenv outside the checkout. Confirm the interpreter
   version and key imports before item 1.
4. **Stay inside the brief.** Respect acceptance criteria, non-goals, stop
   conditions, credential boundaries, and the list of sanctioned test-pin
   changes. No schema or dependency change the brief does not name. No env,
   credential, or forbidden files.
5. **Commit per item. Push after each commit.** Pushes are the progress signal
   the orchestrator watches, and pushed work survives a dead session.
6. **Run the repo's gates before each push where practical.** Report exact
   commands and exit codes. A build that is still compiling is not a pass;
   the exact process must exit 0.
7. **Bound heavy builds.** Run memory-hungry builds in a capped transient unit
   (for example `systemd-run` with `MemoryHigh`/`MemoryMax`, values from the
   brief). Delete generated build state before retrying an interrupted build.
   Half-written build caches stall the retry.
8. **Signed-commit repos.** If the host holds no signing key, use the method
   the project names, such as GitHub's GraphQL `createCommitOnBranch`, which
   GitHub signs. Never add a signing key to the host yourself.
9. **Check whether `main` moved before item 1.** Orchestrators often commit
   state files to `main` right after dispatching. Compare
   `git ls-remote origin refs/heads/main` with the commit you branched from.
   If it moved and your branch has no commits yet, fast-forward the branch
   (`git merge --ff-only main` after pulling `main`). Post that SHA with one
   line saying what moved; it is your "main untouched" baseline.
10. **Keep handback evidence outside scratch space.** A build that waits days
    for the owner's device checks outlives a scratch directory that prunes
    idle files. Keep the status file, suite outputs, check outputs and the
    pull-request body draft in a per-build directory. On resume, before any
    write: `date -u`, `git fetch`, local tip equals the remote branch tip,
    and the services the brief deployed are active. Rerun scripted checks to
    regenerate lost outputs; do not quote old thread messages instead.

## Continuation triggers

- When your iteration budget runs low, post a compact summary that ends with a
  line starting `Continuation trigger:`. Include the last pushed SHA, items
  done, the next item, and anything half-finished.
- Put the same line on mid-run checkpoint summaries. The orchestrator uses it
  to tell a checkpoint from a stop.
- On a mentioned in-thread `continue`, compare the local and remote SHAs
  first. Resume from the last pushed tip. Do not redo pushed items.
- **Remediation rounds** arrive as a new message in the same thread, after the
  orchestrator commits the audit record to `main`. Resume from your last
  pushed tip. Read the findings with `git show origin/main:<path>`. Fix them
  group by group (R1, R2, ...), adding the exact test each finding names.
  Follow the round's commit rule (one commit per group, or per finding if it
  says so), pushed after each. Hand back FIXED or NOT FIXED per finding, with
  evidence.
  - If the audit arrives as "part 1 of N", do only a read-only freshness
    check until the last part lands. Later parts often add items and the
    deploy and handback steps.
  - Prove each new test fails on the old code before you commit it, for
    example `git stash push <fixed file>`, run the test, `git stash pop`, run
    it again.
  - If a finding's literal reproduction passes on the old code, do not claim
    it failed. Find the mechanism the finding names, build a deterministic
    reproduction, and fix that. Say plainly in the handback which case
    passed before the fix and which case failed.
- On "commit, push, then stop for good", do exactly that and post the final SHA.
- Provider, rate-limit, or billing errors are not yours to fix. State the
  exact error in the thread. The operator has to act.

## Mid-run thread posts

- Your reply reaches the thread only when your turn ends. When the brief asks
  for a confirmation, progress note, or question before that, post it with
  Slack `chat.postMessage`, the bot token from your Hermes env file, and the
  dispatch `thread_ts`. Use a small helper that never prints the token. Then
  keep working in the same turn.
- **Disputed items.** If the brief asks you to raise a disagreement before you
  implement an item, that question must reach the thread mid-turn. If you
  cannot post, keep the spec's behaviour for that item, finish the other
  items, and lead the handback with the conflict.
- **Split briefs.** Long briefs can arrive as several thread replies, and
  Slack HTML-escapes their text. Save each part to disk, `html.unescape` them
  when you join them, and post the part count plus a sha256 prefix.
- **Mangled strings.** Slack turns URLs, and file names with domain-like
  extensions, into links. Strip `<...|...>` link wrappers and confirm exact
  values against the repo before using them.
- A new in-thread message reaches you while you work. With busy-input mode
  `interrupt` (the upstream default) it can abort a running tool call; with
  `steer` it arrives after the next tool call; with `queue` it waits for
  your next turn. Either way, check branch and process state before you act
  on it.
- **Recurring status line.** When the brief asks for one line every few
  minutes, create a cron job with `no_agent` and a small script that prints
  `HH:MM UTC | <contents of a status file>`. Cron scripts must live in the
  profile's `scripts/` directory under `HERMES_HOME`; only the status file
  goes in the per-build directory. Set `deliver` explicitly to
  `slack:<channel_id>:<thread_ts>`: a job created from a thread can record
  its origin without the thread, so the default delivery posts in the
  channel. Check the job's `origin` and `deliver` after creating it.
  Overwrite the status file at each step (`item N | <doing what>`). Remove
  the job and its script when the brief says, and at handback.
- Do not use `cronjob run` on that job for one-off posts. Each run sends a
  completion notice back into your conversation as a new turn, and each
  reply becomes another thread post. Use `chat.postMessage` for one-offs.
- Before a long gate run, post one line with the expected duration. Silence
  you announced reads as work, not as a stall.

## Before handback: self-review

Run this before you hand back, and before you open the pull request if the
brief says you open it. These are the findings an independent reviewer most
often returns as P1 on small services:

- read-then-write races (a value computed by one read and written by a
  later statement; make it one statement or one locked transaction);
- unbounded body reads and missing read deadlines;
- input that cannot be parsed or stored (oversized ids, invalid text)
  escaping as a dropped connection instead of a 4xx;
- exceptions that leave the handler without a 500 and a one-line log;
- auth-gate tests that count verifier calls but never check the reply;
- fail-closed branches no test forces;
- tests that still pass with the feature removed (remove the rule, run
  the test, confirm it fails, restore it).

For a web page, `curl` proves only that the file is served. Drive the page
in a headless browser through the brief's steps, and report that as an extra
check beyond the brief.

## Approvals you cannot grant yourself

Ask in the thread, or defer the step and list it in the handback:

- merging to the default branch, or opening the outward-facing pull request
  unless the brief says you open it;
- deploys, production data changes, and production migrations;
- provider link/init/connect commands and auto-confirm flags, creating cloud
  resources, sending mail, or posting to any third party;
- adding or exporting credentials or keys beyond the brief's allowlist;
- editing protected harness files (`AGENTS.md` and similar);
- changing a test pin the brief does not sanction, or widening scope;
- hook bypasses (`--no-verify`, skip-hook env variables) and any `--global`
  config change;
- starting, reviving, or stopping other sessions.

Host approval prompts expire in about five minutes, and text in the thread
does not satisfy them. If a command gates on one, do not retry in a loop.
Defer it, carry on with other items, and list it in the handback. The
orchestrator commits protected-file edits itself after handback.

The operator can widen this list in writing, for example "merge it yourself
in this session". Only then, and record it in the handback.

## Handback

Post one message with: branch, final pushed SHA, each item with its commit
SHA and status, gate commands with exit codes, deviations from the brief,
what you could not verify, and open questions. Every "done" needs its
evidence (see `anti-slop-agent-guardrails`). Once the orchestrator accepts the
handback, do not commit to that branch again. It may add its own commits and
open the pull request.

- **Long outputs get cut.** Gateway notices and thread copies can truncate
  long curl or test output. Put the full output in the pull-request body too.
- **Leak-scan the branch diff, the commit messages
  (`git log --format=%B origin/main..HEAD`) and the pull-request body** with a
  small script that reads the sensitive values (domain, server address, keys)
  from your env files and prints only true or false per value. Values on a
  command line end up in logs.
- **Editing an open pull request's body** (when you opened it). Read it with
  `gh api repos/<owner>/<repo>/pulls/<n> --jq .body > <file>`, edit the file,
  then write it back with `gh api -X PATCH repos/<owner>/<repo>/pulls/<n> -F body=@<file>`.
  `gh pr edit` can fail on some repos without saving the body, so confirm the
  new text is there before you post the handback.

## What the orchestrator watches

Knowing this keeps you visible:

- **Branch pushes** every ~90 seconds. No push for a long time looks like death.
- **Thread content**, diffed between reads. You stream progress by editing one
  message in place, so keep that message current.
- **Silence**: no push and no thread change past its cadence window means a
  suspected stall. It sends one mentioned probe, which lands in your turn.
- **CI or preview status** on every push. A red preview comes back as a small
  follow-up with the exact error.

## Environment pitfalls

- **Global hooks path.** A host-wide `core.hooksPath` can hide the repo's own
  hooks, so a suite that tests its commit gate fails on a clean `main`. With
  the orchestrator's approval, set `git config --local core.hooksPath <repo
  hooks dir>`, run the repo's gate, then commit. Unset it at handback.
- **Externally managed Python.** If a brief needs packages in the pinned
  interpreter itself, copy that interpreter to a scratch path and install into
  the copy. Leave the original clean. Report it as a deviation.
- **Long suites.** Run them from a background script that appends
  `name exit= secs=` lines to a summary file. Poll it with short sleeps under
  your tool's timeout.
- **Long command chains.** A lifecycle guard may refuse one command that
  chains many scripts. Split it into one script per call, or into a shell file.

## Runtime facts to re-check

These are observed behaviour, not permanent law. Check your current Hermes
config before relying on them: session iteration budget, Slack mention
policy, per-session auto-approve (`/yolo`), busy-input mode (`interrupt`,
`steer`, or `queue`), thread-to-session routing, approval expiry, and
continuation behaviour.
