---
name: writing-plans
description: "Use when you have a spec or clear requirements for a multi-step task. Writes an implementation plan with bite-sized tasks, exact file paths, complete code and verification commands, sized to the stakes. Also covers decision models and spec-only artifacts."
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [planning, design, implementation, workflow, documentation]
    related_skills: [spec-interview, overengineering-defence, implementation-plan-adversarial-review, subagent-driven-development, test-driven-development, requesting-code-review]
---

# Writing Implementation Plans

Adapted from obra/superpowers (MIT).

## Overview

Write plans for an implementer who is a skilled developer but knows almost
nothing about this codebase, toolset or domain, and is weak at test design.
Give them what they need: files to touch, complete code, test commands, docs to
check, how to verify. Bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

**Core principle:** a good plan makes implementation obvious. If the implementer
has to guess, the plan is incomplete.

## Size the plan to the stakes

The default bar is MVP / personal system: simplicity and speed beat polish, no
backwards compatibility unless asked, fix blockers, one review pass. A small
change needs a short plan with exact files and one verification command.

Use full rigour (complete TDD steps, negative tests, rollback, an independent
review) when the work touches money, secrets or credentials, customer or user
data, legal exposure, a public product with external users, or irreversible
deletion. Whenever a plan adds a safeguard, name the asset it protects.

## When to use

Always before multi-step features, complex requirements, or delegating to
subagents (`subagent-driven-development`). Do not skip it because the feature
looks simple, you will build it yourself, or you work alone.

Not every planning request wants the full task format. Pick the shape:

| Request | Shape |
|---|---|
| Build a feature from a spec | Full implementation plan (below) |
| Cost, throughput, feasibility, go/no-go | Decision model |
| "Don't code yet, write the spec" | Spec-only artifact |
| Blocked dependency, need evidence first | Measurement-first spec |
| "We agree on the order, spec it first" | Spec-first sequencing |
| A name changes across many systems | Rename manifest |

The non-default shapes are under "Other plan shapes".

## Task granularity

Each task is 2-5 minutes of focused work. Each step is one action: write the
failing test; run it and see it fail; write the minimal code; run the tests and
see them pass; commit.

Too big: "Task 1: Build authentication system" (50 lines across 5 files).
Right size: "Create User model with email field" (10 lines, 1 file), then "Add
password hash field", then "Create password hashing utility".

## Plan document structure

Every plan starts with:

```markdown
# <Feature> Implementation Plan

> **For the implementing agent:** use subagent-driven-development to run this plan task by task.

**Goal:** <one sentence>
**Architecture:** <2-3 sentences>
**Tech stack:** <key technologies>
**Non-goals:** <what this plan will not do>
---
```

Each task:

````markdown
### Task N: <descriptive name>

**Objective:** <one sentence>

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67`
- Test: `tests/path/to/test_file.py`

**Step 1: Write the failing test**
```python
def test_specific_behavior():
    assert function(input) == expected
```

**Step 2: Run it and confirm failure**
Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expected: FAIL, "function not defined"

**Step 3: Minimal implementation**
```python
def function(input):
    return expected
```

**Step 4: Run it and confirm pass**
Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**
`git add <files> && git commit -m "feat: <what>"`
````

## Writing process

1. **Understand the requirements:** spec or description, acceptance criteria,
   constraints. If the owner asks to "verify acceptance criteria and
   dependencies first" or for "the smallest plan before coding", stop at a gate:
   list the exact docs read, the acceptance criteria quoted from source (not
   from memory), dependencies that are present, missing or blocked, baseline
   behaviour to preserve, and the smallest plan with non-goals. Code only after
   explicit approval.
2. **Explore the codebase** with your file tools: project layout
   (`search_files("*.py", target="files", path="src/")`), similar features,
   existing tests, key files.
3. **Design the approach:** pattern, file layout, dependencies, test strategy.
4. **Write tasks in order:** setup, core behaviour (TDD each), edge cases,
   integration, cleanup and docs.
5. **Add complete detail:** exact paths (`src/config/settings.py`, not "the
   config file"), complete code (not "add validation"), exact commands with
   expected output, a verification step per task. Check commands against the
   repo's real scripts and flags.
6. **Review the plan:** tasks sequential and bite-sized; paths exact; code
   copy-pasteable; commands have expected output; no missing context. Run the
   `overengineering-defence` deletion test. For non-trivial or high-stakes plans,
   run `implementation-plan-adversarial-review` before handing off.
7. **Save it:** `docs/plans/YYYY-MM-DD-<feature>.md`, then commit
   (`docs: add implementation plan for <feature>`).

**Chat length rule.** Do not paste a long plan into chat. Save it, then send a
short summary: path, verification status, next action. When another agent
reviews the plan, cap its reply length and patch the saved file instead of
streaming long review text through chat.

## Principles

- **DRY:** extract shared logic once instead of copying validation into three places.
- **YAGNI:** build only what is needed now. No `preferences = {}` or `metadata = {}`
  fields "for later".
- **TDD:** every code task has the full cycle: failing test, see it fail,
  minimal code, see it pass. See `test-driven-development`.
- **Frequent commits:** commit after every task.

## Common mistakes

| Bad | Good |
|---|---|
| "Add authentication" | "Create User model with email and password_hash fields" |
| "Step 1: Add validation function" | The step plus the complete function code |
| "Step 3: Test it works" | "Run `pytest tests/test_auth.py -v`; expected: 3 passed" |
| "Create the model file" | "Create: `src/models/user.py`" |

## Other plan shapes

### Decision models (cost, feasibility, go/no-go)

1. Frame the decision: what it unlocks, which evidence is strong enough for it,
   and what is explicitly not being proven.
2. Inspect repo truth first: seams that exist, gaps that block stronger claims.
3. Check external facts (pricing, provider limits, API behaviour) only when
   material. Record the date and source in the artifact.
4. Calculate with visible assumptions: small, likely and stress scenarios.
   Keep raw cost separate from throughput and rate limits.
5. Write a file artifact, not a long chat answer. Update decision and status
   docs if planning state changes.

Pitfalls: a cost model is not readiness proof. Do not optimise for the cheapest
model before measuring the quality baseline. Do not produce a full
implementation plan when a decision model was asked for.

### Spec-only artifacts ("don't code yet")

For UI or demo polish, read-only dashboards, role or onboarding flows, and
review/approval flows. Every such spec has: a repo freshness check; inspection of
the current surface (and any reference prototype); a goal; the top 3-5 journeys
or views; non-goals; acceptance criteria including empty, loading, error and
stale states; a verification plan; risks where polish could imply readiness the
system cannot back; files likely touched; and the next slice only.

- **UI/demo polish:** borrow a prototype's visual style, not its claims. Keep
  safety gates visible. Do not spec a design system for one polish pass.
- **Read-only control surfaces:** for each view, list the operator question it
  answers, truth sources, fields, freshness, failure states and redaction rules.
  Unknown or stale is a visible state. Every claim links to a source. Mutation
  controls (restarts, scheduled-job edits, dispatch, config changes) are
  non-goals. Prefer a local snapshot generator before a web app. Do not commit
  live snapshots unless redacted.
- **Roles, profiles, preflight checks:** name the roles, how each capability is
  proven, forbidden tools, and rollback. Deployment, runtime flags and key
  changes are non-goals unless separately approved.
- **Review/approval flows:** map the existing state machine first. Keep
  submitter, reviewer and admin credentials separate. No force-approve and no
  direct status edits. Approval acts on the exact reviewed content plus the
  current version (compare-and-swap) and fails closed when stale. Show "intake
  open", "reviewer configured" and "approval ready" as separate states.
  Readiness markers are non-secret declarations, never inferred from token
  files. Describe tokens by shape (path, file mode, label), never by value or
  hash. A one-shot run is not scheduler setup. Treat submitted content as
  untrusted data. Give explicit stop and rollback steps (revoke by label,
  versioned reject).

### Measurement-first specs

Use when a dependency is blocked or the evidence cannot yet support a readiness
verdict. State the decision the measurement will unlock. Define additive
artifacts only: schemas, pure metric builders, reports, fixtures, tests.
Thresholds are reporting bands, not gates. Keep tail metrics and full cost
precision, because averages hide the expensive failures; round only for display.
Add typed redaction for anything logged. Keep eligibility reasons instead of one
boolean. Use no real customer documents without approval. Profiling is evidence
for a later decision, not a verification pass.

### Spec-first sequencing

When the owner agrees on the order but says "spec it first", stop before code.
Agreeing on an approach is not approval to code.

- Patch the tactical status doc, not just the roadmap, so the next session
  inherits the spec gate.
- Write a short sequencing spec: ordered slices, why this order, non-goals,
  acceptance checks, what not to build yet.
- For a single-slice spec, include files likely touched, a regression test for
  the known false-pass or false-fail case, parity expectations across CLI and
  API surfaces, compatibility decisions, and future verification commands.
- If a fresh session will pick it up, save a self-contained prompt under
  `docs/handoff/`: what to read, what not to touch, where to write.
- Commit docs only. Ask before coding.

### Cross-system renames

Aim for zero unexplained current references, not zero old-name matches.

- **Manifest first:** one row per surface with owner, old and new value, class,
  source of truth, mode (replace, alias, redirect, retain, annotate), cutover
  gate, rollback and status.
- **Classify:** display names are renamed. Technical slugs and paths migrate with
  callers, aliases and rollback mapped. Stable IDs are kept. URLs, domains and
  email senders get compatibility first. Historical or regulated artifacts keep
  their original bytes. Logs, caches and backups are excluded from counts. Never
  rewrite git history, issued reports, audit trails or old decisions.
- **Sequence:** freeze baselines; lock the naming policy; stage new domains,
  auth callbacks and redirects while the old ones still work; cut over and
  smoke-test; update control state and regenerate derived files; update routing
  and scheduled jobs without resetting IDs or state; pause scheduled writers
  across note or path moves; rename chat channels; sweep external providers;
  observe before retiring aliases.
- **Traps:** renaming a local path while jobs still use it; pointing a writer at
  a path that does not exist yet; assuming domain aliases keep sessions alive;
  redirects that drop the path or query string.
- **Verify:** classify every old-name match as ALLOW-HISTORICAL, ALLOW-COMPAT,
  FIX-CURRENT or INVESTIGATE. Done means FIX-CURRENT is zero and every
  INVESTIGATE has an owner.
- **Roll back** layer by layer, never by a global reverse replace.

## Execution handoff

After saving, offer: "Plan saved at `<path>`. Ready to run it with
subagent-driven-development: a fresh subagent per task, a spec-compliance review
then a code-quality review after each. Proceed?"

When executing: one fresh subagent per task with full context; spec-compliance
review after each task; code-quality review after that passes; move on only when
both pass.

## Remember

Bite-sized tasks. Exact file paths. Complete code. Exact commands with expected
output. A verification step per task. DRY, YAGNI, TDD. Frequent commits. Depth
matched to stakes.
