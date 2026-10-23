# The Claude–Hermes build loop

**Version:** public edition of private guide v32 (dated 2 October 2026), published 23 October 2026. Rules marked as observed defaults reflect that date; check them against your current Hermes release.

This guide is for a Claude Code session that dispatches, monitors, or
verifies a build run by Hermes Agent. Four roles take part:

- **Orchestrator**: Claude Code on the operator's laptop. Specs, dispatches,
  monitors, verifies, merges.
- **Builder**: Hermes on an always-on VPS, driven through Slack.
- **Auditor**: the Codex CLI on the orchestrator's machine.
- **Owner**: the human. Approves the spec and every merge.

The builder's half of the contract is the `hermes-build-operations` skill.
Each rule carries a one-line reason where a session might skip it. Timeouts
and budgets are observed defaults; check them against your runtime.

## 1. Hard rules

1. **Dispatch only on the owner's explicit instruction.** If a task looks
   Hermes-shaped, say so in the conversation. Never ask by posting the Slack
   mention: the mention is the dispatch.
2. **Merge and production are always the owner's gate.** A builder never
   approves its own work.
3. **Never leave a running session unmonitored.** Dispatching without arming
   the monitoring contract (§5) is a defect.
4. **A new top-level mention starts a new session.** A mention inside the
   dispatch thread talks to that thread's session. Never use a top-level
   mention as a liveness probe; it starts a second worker on the same branch.

## 2. The delivery loop

The orchestrator drives. The owner gates twice. An independent model audits
twice.

1. **Spec and brief.** Acceptance criteria, non-goals, branch, stop
   conditions, sanctioned test-pin changes, and a second method for each kind
   of value a fixture pins (§7).
2. **Spec audit by Codex.** Never skip it; it catches unbuildable designs,
   stale facts, and broken test pins. A spec that encodes a provider's
   behaviour cites a measurement at the exact operating point the code will
   use, and an idea carried over from earlier gets probed before it is
   specified. One probe is cheaper than a build and two audit rounds.
3. **Owner approves the scope** (gate 1), then **instructs the dispatch**.
4. **Hermes builds** on the task branch, one commit per item, pushing after
   each, while the orchestrator runs §5.
5. **Clean-context implementation audit.** Codex reads a worktree pinned to
   the frozen handback commit (§7). FAIL → remediation brief → re-verify.
   FAIL then PASS is the normal shape, not a crisis.
6. **Owner approves the merge** (gate 2) → merge → push → production smoke
   check → docs and status update.

**Proportionality.** Run the full loop for any change that is behavioural,
multi-file, a dependency or schema change, security-relevant, production- or
customer-facing, irreversible, or has side effects outside the repo
(migrations, sent mail, provider link/init/connect, new cloud resources,
third-party posts). The owner may approve a shorter loop for a trivial edit
at scope approval. That is the owner's call, never the orchestrator's guess.

Proportionality also limits breadth. Only safety-core items (money paths,
keys, idempotency, reconciliation) get exhaustive tests; briefs list
representative ones. From round 3 of a handback audit, re-audit P1 classes
only. Why: exhaustive briefs, not code, cause days of remediation.

**Round caps.** A round is one full audit sweep ending in a `VERDICT:` line.
Parallel scope-split runs are one round; a run that dies without a verdict
is a re-run.

- Spec audit: four rounds. Handback audit: the first audit plus three
  remediate-and-re-audit cycles. A PASS on the last permitted round is a pass.
- A scope that passed carries forward unless a later fix touches its files
  or something it depends on.
- Extra rounds need the owner. Scope them to the last round's findings:
  FIXED or NOT FIXED for each, then "did the fixes add a new P1?"
- **Oscillation stop.** One round correcting the last round's premise is
  normal. A finding that flips back to a position it already held, on
  unchanged code, ends the loop.
- At a cap or an oscillation stop, post the open findings, who holds which
  position, and a recommendation to the owner. Then wait.

**Review map.** Skill passes run on the orchestrator's side next to the two
Codex audits. They never replace them.

| Stage | Instrument | Orchestrator skill pass |
|---|---|---|
| Brief drafted | — | `overengineering-defence`, then `audit-router` docs class: citations resolve, counts recomputed, no self-contradiction |
| Spec audit | Codex per §7, strongest reasoning model | — |
| Every push | §6 glance; CI or preview status | — |
| Handback | Codex clean-context audit, CLI default model; independent re-derivation | `audit-router` at Paranoid depth for security, payments, schema, or data; `paranoid-review` for input, async, or retry surfaces |
| Merge | every gate re-run on the merged tree (§7a) | `requesting-code-review` on the merged tree; `premortem` only for production or irreversible changes |
| Docs and status | — | `status-refresh` and a docs check; the next session rebuilds context from these files |

`paranoid-review` and `premortem` come from the `claude-thinking-skills` pack.

A one-shot `codex review` of the checkout's diff is not this audit (see
§7). A shorter loop drops the handback skill pass and `premortem` first, then
the brief's docs check; never the Codex handback audit or merged-tree gates.

## 3. Dispatching a session over Slack

- **Use real mention markup**: `<@YOUR_HERMES_BOT_USER_ID>` through the Slack
  API or MCP. Plain text "@hermes" is inert. Get the ID from Slack's mention
  autocomplete or the bot's profile.
- **One message plus its thread is one session.** The dispatch body is the
  prompt: brief location, branch, expectations.
- **Never start a dispatch with a slash.** An unknown command can discard
  the whole body. Ask in prose for Hermes to rebuild context from the repo
  docs (STATUS, BRIEF, ROADMAP, DECISIONS, AGENTS).
- **Know your auto-approve setting.** Without per-session auto-approve
  (`/yolo`), sessions stall on prompts nobody sees. Check the default and set
  a policy before dispatch.
- **Plain text, under 4,000 characters.** Tables can be rejected, and a
  longer body can split into top-level messages where only the first carries
  the mention. Commit long briefs to the repo. Without push access, post them
  as numbered mentioned thread replies and tell Hermes to join them first.
- **Slack turns URLs and some file names into links** and can split a URL at
  a trailing dot. Give exact values in words or as repo paths.
- **Hermes sees only its own thread**, and only mentioned messages in it.
  Anything it must read goes there or in the repo. A mention in the channel,
  even an aside, starts a new session.
- **In-thread messages interrupt the active turn** and can abort a tool call
  (busy-input mode `interrupt`). Stay quiet during long gate runs unless the
  message changes the work.
- **A fresh session inherits the checkout's current branch.** Name the branch
  and say "pull latest main first" in any dispatch that writes files.
- **Signed-commit repos.** Keep signing keys off the VPS. Hermes commits
  through GitHub's GraphQL `createCommitOnBranch`, which GitHub signs.
- **Protected files** (`AGENTS.md` and similar) can gate on a host approval
  that expires in about five minutes and cannot be answered in the thread.
  Carve them out of the builder's scope and commit them yourself after handback.
- **Read repo facts from the branch at dispatch time.** Pins such as
  `.python-version` move. If the VPS lacks the pinned interpreter, put the
  setup in the dispatch: update `uv`, install the pin, venv outside the
  checkout, install the lock, confirm version and imports before item 1.
- **When the base moves**, run `git diff --name-only <old> <new> -- <paths>`
  and re-check every fixture path, line anchor, and baseline the brief cites.

Every dispatch includes: commit per item; push after every commit; a
continuation trigger before stopping; bounded builds. Heavy builds run in a
memory-capped transient unit (for example `systemd-run` with `MemoryHigh`
and `MemoryMax`), and generated build caches are deleted before an
interrupted build is retried. A half-written cache stalls the next run.

```text
<@YOUR_HERMES_BOT_USER_ID> Build slice 3 per docs/briefs/slice-3.md on
main. Branch: feat/slice-3. Pull latest main, then check out the branch.
Rebuild context from AGENTS.md and STATUS.md. Commit per item, push after
each commit. Run builds under systemd-run with the memory caps in the brief.
Post "Continuation trigger:" with the last pushed SHA before you stop.
Do not merge, deploy, or edit AGENTS.md.
```

## 4. Session lifecycle

- **Sessions have a finite iteration budget** the session cannot see. On
  exhaustion Hermes posts a summary and a continuation trigger.
- **One session per phase.** Retire a session older than about a day at a
  clean boundary; very long sessions slow and stall. Send "commit, push, then
  stop for good" and wait for that push before the new mention, so two
  sessions never share a branch.
- **Revive with a mentioned "continue" in the same thread.** Same session,
  full context. A fresh mention starts cold.
- **A summary with a continuation trigger is not a death.** Hermes posts the
  same shape as a mid-run checkpoint and resumes within minutes. Only an
  explicit "iteration budget exhausted" line or a provider or billing error
  marks a stop. A "continue" sent on the summary alone interrupts a live turn.
- **A checkpoint with no trigger line is decided by the clock.** Self-resumes
  have come within about four minutes, so probe that shape at 8 minutes of
  silence. Use 15 minutes for every other silence.
- **Diff before you continue.** Compare the last bot message with your
  previous read. If the session is alive, send nothing. A duplicate
  "continue" interrupts the turn. A duplicate top-level mention starts a
  second writer that can repeat commits, deploys, and posts.
- **Stopping a duplicate.** Post `<@YOUR_HERMES_BOT_USER_ID> !stop` as a
  mentioned reply in the duplicate's own thread (Slack blocks native slash
  commands in threads). The stop is unconfirmed until that thread shows a
  turn-end marker and no further edits. Its pushed commits are untrusted
  until a §6 glance clears them. Then revive the real session.
- **Silence has several causes.** Context compression queues your message;
  it is not lost. After an abnormal turn end, replies can lag about five
  minutes. End-of-turn markers followed by silence and no push for about 15
  minutes means stopped: probe once.
- **Branch state cannot tell deaths apart.** Budget, provider, and billing
  failures all look like a long gate run from `git ls-remote`. Only the
  thread shows the reason, and its status line can change between reads.
  A budget death needs "continue". A billing error (for example HTTP 402)
  needs the owner: say so in the heartbeat, stop the thread timer, and keep
  a slow push watch.
- **Approval prompts are invisible to the orchestrator.** Detect them by
  silence: no thread activity and no pushes. They expire in about five
  minutes, and an in-thread "approved" does not answer them. Either the
  owner is at the keyboard when Hermes re-sends, or Hermes defers the gated
  command and continues. Never queue a time-sensitive approval while the
  owner is away.

## 5. Monitoring contract

No single signal covers every failure, so the contract layers them.

| Signal | Mechanism | Catches | Misses |
|---|---|---|---|
| Branch push | `git ls-remote` every ~90 s, 45-minute lifetime | Commits; timeout doubles as dead-man alarm | Stops, handbacks, questions, approval stalls |
| Thread content | Thread replies on the dispatch `ts`, diffed | Stops, handbacks, questions, progress | Approval prompts |
| Silence | Both quiet past the cadence window | Suspected stall, confirmed by one probe | A healthy quiet gate run looks the same |
| CI / preview | Status of every push | Build breaks mid-round | Logic defects |
| Heartbeat log | One line per wake | Monitoring itself dying | Anything about Hermes |

1. **Arm first.** Re-arm the wake timer before anything else each turn.
   Any wake text, even a bare "continue", means run the checklist and
   re-arm. Answering it with nothing kills the loop.
2. **Read the clock** (`date -u +%T`) with each read. Never estimate elapsed
   time from timer ticks.
3. **Push watcher.** Background `git -C <repo> ls-remote` on the branch every
   ~90 seconds, exiting on a SHA change, living about 45 minutes. Use
   `git -C` because tool working directories can reset.
4. **Thread timer.** A background `sleep <cadence>` that wakes the
   orchestrator to read the thread; a shell can poll git but not Slack.
   Re-arm both watchers on every wake.
5. **Read thread replies, not channel history**, with no cursor and a high
   limit. In some Slack clients a cursor returns messages up to that point,
   which hides the newest one, the one you are waiting for.
6. **Diff content; do not count messages.** Hermes edits one progress
   message in place.
7. **Heartbeat.** Append one line (UTC time and state) per wake to
   `~/.claude/logs/hermes-heartbeat-<project>.log`. A stale heartbeat shows
   monitoring has died.
8. **Escalate to the owner's phone** with a push notification on a suspected
   stall, a handback, or a verdict. The owner must not be the detector.
9. **Cadence is a dispatch parameter the owner sets.** Record it in the
   first heartbeat line. Default: 5 minutes in active phases, 15–25 minutes
   in long gate runs, never longer than the push watcher's lifetime.
10. **CI and preview builds are a free early gate.** On a failure, send the
    exact error as a small follow-up instead of re-running full gates.
11. **Retry stalls on a schedule.** Transient failures (rate limit, gateway,
    provider fallback) get one probe after about 15 minutes, then hourly. A
    probe costs a message; a passive night costs the night. Go passive only
    when a human must act (revoked auth, spend cap), and say so.

## 6. During-build hygiene

- Glance at every pushed commit: right item, right files, no schema or
  dependency change beyond the brief, no env or credential files, `main`
  untouched.
- Never share one writable checkout between two writers. Verification gets
  its own worktree pinned to the commit under test.
- Hermes never calls the Codex CLI; the VPS copy is unauthenticated by
  design. Independent review runs on the orchestrator's machine.
- Credentials: fingerprint the target before exporting, pass only
  allowlisted variables, keep mail keys out of test lanes, delete pulled env
  files after use. Provider link/init/connect and auto-confirm flags are
  mutations.

## 7. Verification with Codex, clean context

- **Recipe.** `git worktree add --detach <tmp> <frozen-tip>`, then
  `codex exec -s read-only "<prompt>" -C <tmp> -c 'model_reasoning_effort="high"'`.
  Wrap small runs in `timeout 540` with stdout to a file. Detach larger ones
  (`nohup timeout 840 codex exec ... > out 2>&1 < /dev/null &`) and poll.
- **Polling.** Never `pgrep -f` the command text (your polling shell
  matches itself) or grep the whole log for `VERDICT:` (Codex echoes files
  it reads). Read the final answer block.
- **Split by scope.** A broad prompt over a large diff dies before its
  verdict. Give each parallel run a file list, at most eight questions, and
  "start from `git diff <base> HEAD -- <paths>`". Fix re-checks fit one run.
- **Authority and format.** Give Codex the brief and handback as authority.
  Ask for [P1]/[P2] findings, pass or fail per item, and a final `VERDICT:`
  line. A claim about control flow is a hypothesis until checked. Codex can
  mark FAIL on a P2 alone; read the findings, not the word.
- **Independent re-derivation.** For each kind of value a record or fixture
  pins (block number, timestamp, balance, hash), check at least one instance
  by a second method that does not pass through the code or records under
  audit. Example: a recorded block timestamp against that block's header.
  The brief names the method. A value with no second method is listed as
  unverified. Why: checking code against the brief and tests against
  fixtures inherits every error the fixtures carry.
- **Mutation runs on safety-core tests**, before the Codex audit: remove the
  rule a test names and run it. A test that stays green protects nothing.
  Never mutate the worktree a reviewer is reading.
- **The builder's closure audit is not the audit.** Builders audit
  optimistically; always run your own.
- **Sandbox limits.** Codex's sandbox may lack a temp dir and the repo's
  interpreter, so it verifies statically; run the full suites yourself. A
  run can die silently (laptop sleep): check for `VERDICT:`, not the exit code.
- **Send findings back as R1, R2, R3**, each with the exact test to add.
  Scope the re-audit to the fix commits.
- **Model policy.** Your strongest reasoning model for spec audits (highest
  leverage per token); the CLI default for handback audits (the time cap is
  the risk). Pass it per invocation (`-m <model>`), not in global config.
  Probe it first with a one-word prompt; if that fails, tell the owner and
  never fall back silently. Report the model used, from the session log,
  next to the verdict.
- **If Codex is unavailable**, ask the owner before using a substitute,
  usually fresh-context Claude subagents in the same pinned worktree with
  the same prompts and verdict format. Record the substitution.

## 7a. Merge hygiene (gate 2)

A green branch tip does not prove a green merged tree.

- **Fetch first.** Scheduled jobs and other merges move `main` during a
  build. Inspect what landed since the branch point.
- **Re-run every gate on the merged tree, locally, before pushing**, with
  the pinned dependencies. Tests that assert literal values from live data
  go red when it refreshes; freeze a fixture instead.
- **Check push access** (`gh auth status`) at dispatch time, not merge time.
- **Deploy platforms may block commits from non-team authors.** Set a team
  identity in the clone before merging. Never amend and force-push `main`;
  add one small commit on top. Read deploy state from the commit's
  deployment statuses, not the production URL.
- **Regenerate derived files** with every command the repo's `AGENTS.md`
  names, on the merged tree. Diff against a clean `main` worktree to
  separate old lint findings from new ones.
- **CI may require the PR head to contain `main`'s tip.** Budget a sync merge.
- **Signing.** An SSH signing key without `commit.gpgsign true` signs
  nothing. **External repos:** gate 2 means opening the pull request.
- **If the owner has Hermes merge directly,** verify afterwards: the merge's
  parents are the tip and the expected `main`, and every gate passes.
- **Close the thread.** Tell Hermes it is closed and where `main` is.

## 8. Per-project parameter block

This guide is portable. Each repo states its own facts in its harness
(`AGENTS.md`, `STATUS.md`, `DECISIONS.md`, runbooks). Read them before
dispatch. A minimal block:

```markdown
## Build parameters
- Slack: channel #<project>-builds; one thread per dispatch
- Branches: feat/<slice>; forbidden files: .env*, secrets/
- Gates: <test>, <typecheck>, <lint>, <build>
- Credentialed lanes: <tests and their allowlisted variables>
- Database: no production migrations from the builder; path: <runbook>
- Post-merge smoke: <URL or command and expected result>
- Monitoring cadence: 5 min active, 20 min long gates
```

If a repo has no block, ask the owner. Never borrow another project's
values. Project-specific lessons go in that repo's harness, not here.

## 9. Update discipline

Keep one canonical copy. A session that learns a durable lesson updates it
in the same session: the rule plus a one-line why, no incident stories,
dates only on facts that can go stale. Bump the version line, then sync
copies on other machines.
