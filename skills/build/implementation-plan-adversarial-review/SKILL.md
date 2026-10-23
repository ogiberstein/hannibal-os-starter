---
name: implementation-plan-adversarial-review
description: "Use when a plan or spec is written but coding has not started. Tests the plan against real repo and runtime truth to catch plan/code mismatches, ordering and restart hazards, fail-open paths, false assumptions and weak verification, then records findings and a go/no-go."
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [review, planning, audit, specs, verification, risk]
    related_skills: [audit-router, overengineering-defence, writing-plans, requesting-code-review, anti-slop-agent-guardrails]
---

# Implementation Plan Adversarial Review

## Use when

- a plan, spec or design doc proposes changes and no code exists yet;
- the owner asks whether a plan really fixes the issues it claims to fix;
- findings must go into the plan before it is handed to an implementing agent.

## Goal

Test the plan against actual repo behaviour, not against its own internal logic.

Core question: if a skilled implementer followed this plan exactly, where would
it still ship the wrong thing?

## Evidence rule

Never review a plan as prose alone when you can reach the repo or runtime.
Inspect the real files, interfaces, tests, configs, deployment shape, data and
existing patterns the plan depends on. Flag every step that names a missing file
or API, assumes a hook point that does not exist, ignores the current
architecture, or verifies a proxy instead of the real blocker.

## Proportionality

Default to the MVP bar: one bounded adversarial pass, one correction round for
concrete blockers, then stop. A blocker changes safety, truth or the decision;
style is not a blocker. Repeat review only when the plan touches money,
secrets or credentials, customer or user data, legal exposure, a public product
with external users, or irreversible deletion, or when a fix materially changes
the risk. Run `overengineering-defence` in the same pass: a review that adds
scope has failed in a different way.

## Workflow

1. **Load current truth.** Read repo instructions and brief/status docs. Pull the
   latest branch if the plan depends on recent changes. Read the whole plan.
   Audit a stable snapshot: if files change mid-review, re-read, re-run focused
   checks and record the commit you reviewed.
2. **Trace every planned change to live code.** For each claimed fix:
   - the named file, function or type exists;
   - current control flow allows the proposed hook point;
   - no existing cleanup, prune or reconcile step would undo the new logic;
   - referenced state is persisted, not process-local;
   - commands match the repo's real scripts and flags. Run the advertised
     `--help` or `--dry-run` with harmless values; ad hoc flag parsers often
     swallow the next argument or ignore a flag.
3. **Apply risk lenses.**
   - **Plan/code mismatch:** a hook point or state transition the code does not allow.
   - **Ordering bugs:** logic runs after the data it needs was deleted or pruned.
   - **Restart and idempotency:** in-memory dedupe, timers or promotion state in a
     process that restarts.
   - **Fail-open paths:** a fallback, missing adapter or caught exception that
     quietly continues down the default path.
   - **Metric insufficiency:** checks prove mechanics, not the real improvement.
   - **Scope leakage:** the plan claims to fix X but leaves the top blocker intact.
4. **Map findings back to the owner's concern.** Does this fix the blocker they
   named, or a symptom? Does it make measurement repeatable? Does it keep
   "measured" separate from "ready"? Does it survive runtime conditions the repo
   has already seen?
5. **Get one independent pass for non-trivial plans.** When the plan affects
   money-moving logic, execution semantics, validation gates, auth or security,
   public endpoints, or a repo shared with outside reviewers, ask a second model
   (for example Codex) or a fresh subagent with no stake in the plan. Ask for:
   verdict, blockers, non-blockers, recommended edits, go/no-go, under a length
   cap. If it finds blockers:
   - patch the plan and every control doc that carries the same decision;
   - grep for stale terms, old thresholds, renamed fields and dropped concepts;
   - re-review only for high-stakes work or a materially changed risk;
     otherwise record remaining items as accepted risks.
6. **Resolve ambiguity in the plan, not in the code.** If terms are ambiguous
   (gross vs net, hard filter vs advisory hint, per-item vs shared limit), write
   the choice, the reason and a test into the plan. Do not leave "open
   questions" that the implementer will silently answer in code.
7. **Write findings down.** Prefer `docs/reviews/YYYY-MM-DD-<plan>-review.md`:
   initial verdict, blockers, how each was resolved, remaining non-blockers,
   final go/no-go. If implementers need the findings in the plan, add a separate
   `## Adversarial Review Findings` section (severity, failure mode, why the plan
   misses it, required correction). Do not mix findings into the author's voice.
8. **Commit only after reading the diff.** Preserve existing decision and status
   history; scripted rewrites can truncate control docs. Push only if asked.

## Output format

- `CRITICAL`: the plan can silently fail or does not achieve the stated fix.
- `HIGH`: likely runtime or production issue, or non-idempotent behaviour.
- `MEDIUM`: a verification or reporting weakness that can hide failure.

End with one verdict: **GO**, **GO WITH FIXES** (list them) or **NO-GO**.

## Common gotchas

**Plan vs runtime**

- The plan compares against in-memory state that the code clears before the check.
- Promotion logic uses process uptime instead of persisted run state.
- Verification checks that a veto changed, not that the outcome improved.
- Fixing a measurement is treated as being ready to ship.
- A proxy metric (say, an image-similarity score) is framed too broadly. Keep the
  narrow claim it proves and add the missing gate separately.
- A platform capability is assumed because the docs mention the feature
  category. Require a tiny capability spike before trusting the path.
- An inherited environment credential overrides the scoped file the plan meant
  to use, or a target filter works only in dry-run mode, so the live run hits
  the wrong item. Require unsetting higher-precedence credentials and testing
  real targeting before targeted runs.
- Startup hooks that call the network or write state. Keep hooks local and
  read-only; put probes in an explicit doctor or preflight command.

**Stale scope after a decision**

- A late decision narrows the first cut, but gates, test matrices, rollout,
  checklists, onboarding and runbooks still describe the fuller design. Sweep
  the whole doc into "first cut" and "deferred". Otherwise builders overbuild or
  falsely block the MVP.
- A spike updates the plan but leaves status and decision docs stale.
- A security section names the future enforcement mechanism, not the first-cut
  one. State plainly what protects data today, including operator access.
- Words like "public", "private" or "team" change meaning when the architecture
  narrows. Define the first-cut meaning and sweep the copy.
- A demo spec polishes visuals while proof stays weak: stale commit evidence,
  vague "preserve safety" wording, an unauthenticated smoke test standing in
  for logged-in QA, prototype copy that implies production readiness.

**Proof of value**

- A self-reported flag (`applied=true`, `accepted`) is not proof. Require an
  artifact that shows the decision changed: before/after summary, sanitised
  excerpt, owner quote, a dead end avoided.
- A demo that only proves plumbing (exact-title search, manual lookup) is setup
  smoke, not value proof. If the claim is that agents do something unprompted,
  test that on a realistic task, including a bounded no-match case.

**Tool and permission surfaces (MCP servers, CLIs, agent roles)**

- Check how the client really names and exposes tools. Some prefix names by
  server, store config per profile, or fall back to shared credentials when an
  env var is missing. Record the discovered names and the non-secret env shape.
- Hidden from the tool list is not the same as uncallable. Require raw-call
  negative tests that prove forbidden calls fail before any credential is read.
- A broad env flag that enables write modes needs a client-side allowlist and
  absence checks for publish or admin tools. "Inert without a key" is not enough
  on an operator's machine.
- Audit each client's setup script separately; one generic script rarely sets
  every role and flag.
- Local checks that mirror a server validator must exercise the same parser and
  field aliases, cover every input the server uses, and test pass/fail flags
  separately from data fields.
- Status endpoints that report a category need a closed set of values.

**Isolation, activation and policy splits**

- Map construction, recovery and termination for every process family
  (foreground, background, PTY, separately spawned managers). A fallback to an
  unisolated path is fail-open. Missing adapters, adapter errors, uncertain
  recovery and kill must all fail closed; unknown stays unknown.
- A subclassable internal class behind a closed factory is not an extension
  point. Monkeypatching is runtime patching, not a supported boundary.
- If a directory or file appearing activates something, treat creation as
  activation: hold one lock across check and rename, and journal for crash
  recovery.
- Block on unknown statuses: list the terminal states that allow progress and
  treat everything else as blocking.
- Not copying credentials is not the same as no access. Inherited env, the real
  home directory and global auth fallbacks can still expose them.
- Keep read-only structural checks separate from mutating smoke tests. Bind smoke
  evidence to the exact commit and file hashes. Clean up only artifacts proven
  new. Confirm the runtime you inspected is the one actually invoked.
- A manifest-driven check needs a closed expected set; an empty manifest must fail.
- Isolated data can still leak through shared operational planes: scheduled
  jobs, reviewer secrets, admin or metrics routes, telemetry. Add a teardown and
  retention list (queries, logs, backups, exports, configs, token files).
- A capability probe is not authority. Choose a looser policy only when local
  intent and remote capability agree; default to the stricter one; overrides may
  only tighten. Enforce policy at the approval boundary, not in UI labels, and
  record the policy version in each verdict.
- Copying content to a public plane needs negative tests proving private IDs,
  paths and hostnames are stripped. Vague rules like "internal evidence counts"
  need a grammar with pass and fail examples. Label consent and data
  classification as human assertions, not enforcement.

**AI evals and prompt contracts across repos**

- Green eval tests prove mechanics. Compare case-level gold labels in both repos;
  a perfect score can reward the wrong behaviour.
- The output vocabulary must be able to express the safe outcome (abstain,
  needs human review).
- Citations: invented IDs are zero tolerance; real but unexpected ones need
  review; track expected-citation recall and explicitly excluded citations
  separately.
- Pin the full request: provider and API version, immutable model ID, every
  inference parameter, how the schema is delivered, how inputs are rendered.
  Share golden input-to-request vectors across both repos.
- An embedded `eligible: true` is self-asserted, and a self-hash proves nothing
  until pinned. Recompute eligibility, pin by reviewed commit plus hash, and fail
  closed on mismatch.

## Checklist

- [ ] Plan read in full, against a stable snapshot.
- [ ] Every referenced code path, command and flag was inspected or run.
- [ ] State lifecycle, restart and fail-open behaviour were checked.
- [ ] Verification is tied to the real blocker, not a proxy.
- [ ] Findings sit in a separate section or review doc, with a GO / GO WITH
      FIXES / NO-GO verdict.
- [ ] Review stayed proportional: one pass and one correction round unless the
      stakes or a material risk change justified more.
