---
name: true-stuck-check-reporting
description: Use when a scheduled or ad-hoc status pass must report only work that is truly stuck. Separates real execution blockers from waiting states, owner actions, intentional holds and stale docs, and returns a minimal report.
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [status, monitoring, cron, blockers, reporting, operations]
    related_skills: [status-refresh, anti-slop-agent-guardrails, systematic-debugging, plain-style]
---

# True Stuck Check Reporting

## Use when

- A cron job or status pass must report only items that are truly stuck.
- The owner wants blocker detection, not a general status summary.
- Project docs may over-label items as blocked, or lag behind reality.

## Core rule

Report an item as **stuck** only if work that should be happening *now* is
prevented by a concrete issue.

| State | Meaning | Report? |
|---|---|---|
| **Stuck** | Expected execution is failing now, with current evidence | Yes |
| **Waiting** | Execution depends on a person, partner or date that has not arrived | No |
| **Owner action** | The next step belongs to the owner (setup, sign-off, credentials, approval) | No |
| **Intentional hold** | Paused, parked or gated on purpose | No |
| **Stale docs** | Docs say "blocked" but current evidence shows progress or a resolved issue | No (fix docs separately) |
| **Noise** | A failure unrelated to any active lane or to this report's delivery | No |

Do **not** report:

- waiting on owner or user action;
- deliberate holds;
- no recent work or no update;
- open questions with no active execution dependency;
- general risks or caveats;
- "next step pending", unless something that should already be running is
  concretely failing.

## Decision test (per project)

1. What is supposed to be running now?
2. Is it really expected to run now, or is it intentionally waiting?
3. Is there a concrete blocker or failure, not just a risk or an owner
   dependency?
4. Do I have current evidence, not just stale wording in docs?

Report only if all four answers are yes.

## Evidence order

1. **Project truth.** Read the repo's `STATUS.md` and `BRIEF.md` on the
   default branch. If `STATUS.md` points elsewhere, follow the pointer.
2. **Runtime and automation truth.** Check same-day cron, service, log and
   health evidence for anything that should be running. Same-day evidence
   beats older summaries.
3. **Prior sessions.** If still ambiguous, search past sessions for known
   false positives, outages or earlier definitions of "blocked".

## Fast portfolio triage

For scheduled checks across several projects:

1. Read your portfolio or allocation list. Deep-check only active lanes
   (whatever you call them: execute, explore, monitor).
2. Read each active lane's `STATUS.md` and `BRIEF.md` from a clean,
   default-branch checkout.
3. Separate a blocked **outcome** from a blocked **execution path**. A
   required sign-off, an intentional ship gate or open audit findings are not
   stuck while remediation or other planned work can proceed.
4. Probe the canonical live endpoint or scheduled job that should be healthy
   now. A current healthy response outweighs an older dashboard timestamp.
5. Scan scheduler failures, but count only those tied to an active lane or to
   this report's own delivery path.
6. If nothing active is concretely failing, return exactly the no-stuck
   sentence. Do not recap gates or waiting states.

## Evidence matrix

| Evidence | Meaning | Stuck? |
|---|---|---|
| Lane paused for expert or owner review; live health is green | Outcome gated, no failing execution path | No |
| Open ship/audit gates, remediation still executable, services healthy | Quality gate | No |
| Checkout helper lands on an old feature branch; default branch shows a newer intentional pause | Stale navigation | No |
| Enabled automation has a same-day concrete failure, and it is the expected execution path now | Execution blocked | Yes |
| A project job is paused by allocation choice | Intentional hold | No |
| An unrelated support or updater job failed; active lanes and delivery are healthy | Noise | No |
| Job name mentions one channel, but its configured delivery target is another, healthy one | Naming drift | No |
| The current delivery target is unhealthy, so this report cannot arrive | Reliability blocker | Yes |

## Common false positives

- `Blocked: None`, plus a risks section that mentions something that *could*
  block later.
- Setup tasks explicitly assigned to the owner.
- "Pending next-step decision" after a completed gate.
- Known data-quality caveats that are being worked around and do not stop the
  active run.
- Historical failures that are already resolved.
- A review step returning "hold for manual review": that is a go/no-go
  decision state, not stuck, unless the job itself fails.
- Advisory outputs such as "wait" or "manual review needed" from a
  monitoring job. Stuck only if the monitoring or reporting path itself fails.

## Rules from experience

Each rule is followed by why it exists.

**Scheduler and runtime**

- Inspect the live cron store (`$HERMES_HOME/cron/jobs.json`) for `enabled`,
  `schedule`, `last_run_at`, `last_status`, `last_error`, `deliver` and
  `last_delivery_error`. Parse the JSON directly. *Why: job names and prose
  drift; the store is the runtime truth.*
- A monitor-only project can still be stuck if its scheduled monitoring job
  fails repeatedly today (for example, an API response schema change breaks
  parsing). Report it as "fix the parser and rerun", not as an execution
  blocker. *Why: the expected monitoring path is what is blocked.*
- Check live timers, services and recent logs, not notes, when the question
  is current health. A clean recent run that publishes fresh output means
  "not stuck". *Why: notes describe the past.*
- An active reliability incident (for example, a full disk causing failed
  writes) is stuck if it makes current data unreliable. The same incident is
  not stuck once current runs succeed and headroom is restored. *Why: judge
  the present, not the incident history.*
- A queued deploy next to a recent successful deploy is not a blocker unless
  the active service is failing. *Why: queues are normal.*
- During the running check, `next_run_at` may already have advanced while
  `last_run_at` still shows the previous run. *Why: that is normal
  persistence timing, not a stuck job.*
- When reproducing a failure in your own shell, check `PATH` first. A missing
  toolchain in a non-login shell is your probe's problem, not the project's.

**Delivery path**

- Judge delivery health from the job's configured `deliver` target and that
  transport's current health, not from the job name.
- Past delivery failures do not count if the transport is healthy now and the
  scheduler will deliver this report.
- If delivery is the blocker, confirm with both the health check and the
  bridge or gateway logs (for example, a logged-out messaging session). Report
  it as delivery reliability, with the fix: re-pair or restart, then resume.

**Repo truth**

- If a checkout helper lands on an older feature branch, compare against
  `origin/main` (for example `git show origin/main:STATUS.md`) before using
  it. *Why: stale branches look like stale projects.*
- Recent scoped commits plus a changing working tree are positive evidence
  that work is happening, even if the branch has diverged or summaries are
  old. *Why: divergence and dirty files are not blockers.*
- Treat a same-day portfolio snapshot as a starting point. Re-check the repo,
  PR and CI state before repeating an exception. If the fix is merged and
  green and only owner approval for a production step remains, exclude it.
  *Why: that is an authorization boundary, not stuck execution.*

**Gates**

- A reviewed gate defect *is* stuck when it blocks the active next step (for
  example, an audit returns "no go" on a concrete bug and the next pipeline
  step cannot run until it is fixed). Report the defect and the fix/re-audit
  step, without implying the runtime is down.
- Missing collaborator inputs, owner go-ahead, OAuth setup, secrets or publish
  approval are waiting states, unless an approved agent-owned path is
  failing.
- A fail-closed readiness gate on a support project (for example, a
  restore-readiness check failing on unregistered repos) is not automatically
  an incident. Report it only if the expected automation is failing now, it
  actively degrades recoverability, or it blocks an active lane. Keep wording
  narrow: `project -> check fails on <specific findings> -> fix, then rerun`.
- A successful backup does not prove restore readiness. Verify both
  separately. A readiness failure caused only by another process owning a
  worktree right now is transient, not stuck.

**Probing**

- Read a verifier's accepted arguments before running it. If it exits
  nonzero with no clear error, run the named sub-check directly.
- Take endpoint names from the newest repo docs or config. A 404 from a
  retired alias is a probe error, not an outage.
- Healthy runtime plus current implementation activity outweighs older
  `blocked` headings about sign-off, sharing, deploy or quality gates.
- If a terminal guard blocks a quick `curl`, use a read-only browser or API
  fetch of the same URL. Do not fall back to stale docs.
- Browser probes share one page. Serialize each navigate-then-read pair;
  parallel navigations can overwrite each other.

## Output format

If nothing is truly stuck, return exactly:

```
Nothing is stuck.
```

If something is stuck, output bullets only, one per item:

```
- <project or channel> -> <what should be running> -> <concrete blocker> -> <next step to unstick>
```

Keep it minimal. No evidence dump, no recap of waiting states.

If a generic unattended-job wrapper offers a silence token (such as
`[SILENT]`) but the task asks for an exact no-stuck sentence, the task wins:
return `Nothing is stuck.` with nothing added.
