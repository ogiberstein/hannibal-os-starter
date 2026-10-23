---
name: audit-router
description: "Use when the user explicitly asks for an audit, review, CTO or paranoid pass, adversarial or red-team review, stage gate, or ship-readiness verdict. Picks the audit class, depth, evidence bar, and verdict format. Defaults to MVP depth."
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [audit, review, red-team, adversarial, verification, quality-gate, routing]
    related_skills: [overengineering-defence, implementation-plan-adversarial-review, anti-slop-agent-guardrails, evidence-gate, hermes-build-operations, writing-plans, spec-interview]
---

# Audit Router

Use this skill only when someone explicitly asks for an audit, review, CTO
pass, paranoid or adversarial review, red-team, stage gate, or ship-readiness
verdict. An ordinary "is it done?" or "is it fixed?" gets one direct check,
not this router. If a readiness claim touches a full-rigour domain (see
below) and nobody asked for an audit, offer one in a single line.

The router decides three things before any reading starts: how deep to go,
which audit class applies, and what evidence a verdict needs.

The CTO-style and paranoid review modes are inspired by garrytan/gstack (MIT).

## Core posture

The job is to stop false confidence about things that matter. It is not to
maximise the finding count.

- **At MVP depth** find what would break the decision or lose something that
  matters. Report blockers. List the rest in one line each. Stop.
- **At Paranoid depth and above** act as the CTO looking for the one gap
  that invalidates the work. Assume the obvious bugs are gone. The rest hide
  in assumptions, boundaries, state transitions, and untested failure paths.
  Green tests, tidy docs, and a healthy-looking runtime can all be wrong.
  Agents overclaim unless made to attach evidence.

**Full-rigour domains:** money and trading, secrets and credentials, customer
or user data, legal exposure, public products with external users,
irreversible deletion, production deploys and migrations.

## Step 1: pick the depth

Choose the smallest depth that can answer the question honestly.

| Depth | Use for | What it means |
|---|---|---|
| **MVP** (default) | MVPs, experiments, internal tools, personal systems | Inspect the directly relevant artifact. Run the one check that decides it. Blockers only, plus a one-line list of the rest. One pass. |
| **Standard** | Code or plans other people or external users depend on | Read the context and the diff. Run the feasible checks. "No PASS without evidence" applies from here up. |
| **Paranoid** | Explicit paranoid/CTO/red-team request, or non-trivial behaviour in a full-rigour domain | Full attack checklist, explicit failure modes, an independent reviewer where practical. |
| **Production-blocking** | Live money, user data, credentials, destructive actions, production deploys | Runtime truth, a tested rollback path, and explicit human approval before any risky side effect. |

If you cannot tell whether the user wants more than MVP, ask in one line.

## Step 2: pick the audit class

At MVP depth, each "evidence" list is a menu. Run the one decisive check.
At Standard depth and above, the list is the bar for a PASS.

**1. Code diff (local, uncommitted, pre-commit).** Evidence: `git status`,
the diff plus surrounding code, a secret scan of added lines, test/lint/type/
build output, a map of untested behaviour. Pair with `requesting-code-review`
and `test-driven-development`.

**2. Pull request or branch.** Evidence: PR metadata and changed-file list,
the diff against the base, CI status with local reproduction where practical,
file and line for every blocker. Check that CI ran on the head SHA you
reviewed. Add the domain class if the PR touches money, auth, data, or runtime.

**3. Plan, spec, docs, or handoff.** Always run `overengineering-defence`
first: decision value, failure cost, cuts, carry cost, one stopping rule. Then
`implementation-plan-adversarial-review`. Evidence: the document read in full;
every cited file, function, config, and count checked against the repo; a
mismatch table (claim → repo fact → risk); a test plan tied to the real
blocker. For factual docs, also: citations resolve, counts recomputed, no
section contradicts another, dangerous commands carry guards, stale facts
flagged. If a decision demotes an option, ask for a steelman of it.

**4. Done, fixed, shipped, or stage-gate claim.** Pair with
`anti-slop-agent-guardrails` and `evidence-gate`. Evidence: acceptance
criteria listed explicitly, git state (clean or dirty), the commit, branch,
and deployed SHA, check output, runtime logs or artifacts where relevant, and
a claim ledger. Separate caught, fixed locally, committed, pushed, merged,
and deployed. They are six different states. Without the evidence the
verdict is `INCONCLUSIVE` or `FAIL`, never `PASS`.

**5. Runtime and infrastructure truth.** Schedulers, cron, gateways,
deploys, backups, jobs, ports, live config. Evidence: the runtime config
source (not only repo docs), process and log state with timestamps, the
deployed version, artifact presence and parse checks, a negative probe ("how
could this look green and still fail?"), and the rollback path.

**6. Money and trading.** Anything that can lose money, create exposure, or
place orders. Evidence: the edge thesis and why it persists; fees, slippage,
spread, and capital lock; executable versus indicative prices; exposure caps
and kill switches; fill, reconciliation, and restart behaviour; replay or
shadow evidence with unrecoverable metrics named. Default bias: do not scale
until the evidence survives an attack on market structure.

**7. Data pipeline, research, or discovery.** Crawlers, classifiers,
ingestion, scoring inputs, evaluation sets. Evidence: admission logic,
identity and dedupe rules, provenance fields, observed versus modelled rows
kept apart, live spot checks (not only fixtures), retention and truncation,
and what downstream decisions the data feeds.

**8. Web app QA.** Pair with `dogfood`. Evidence: tested URL and scope,
console errors after interactions, screenshots, repro steps, severity, what
was not tested, and realistic negative scenarios (bad amounts, odd URLs,
missing data, confusing duplicate choices, exact error copy). For beta
readiness, give a launch-size recommendation separate from the verdict.

**9. Agent and process claims.** Auditing what an agent said it did. Evidence:
a claim ledger; transcripts, logs, files, and configs; the difference between
policy intent and what ran. Unsupported claims are marked `UNPROVEN`.

**10. Security.** Repo security audits, input-parsing and stream-parsing
code, auth, and incident triage ("am I affected by this advisory?").
Evidence: a failure-mode list written before reading the code; trust
boundaries; hand-traced inputs for each finding; every rejection path tested
in each shape the input can take (list and object, missing and duplicate).
For triage: advisory facts, lockfiles and global packages searched, named
persistence paths inspected, and no suspect install scripts run. Prefer
`PASS WITH RESIDUAL RISK` over `PASS` when only local indicators were
checked. Never probe live endpoints without the owner's say-so.

High-stakes code that is not trading (payments, permissions, migrations,
background jobs, destructive actions) uses class 1 or 2 at Paranoid depth.
Trace the value or state through the smallest unit touched. Check
idempotency, retry, replay, and partial failure. For split stores (database
plus object store, database plus index), trace create, update, delete, and
retry separately.

## Evidence hierarchy

Stronger evidence wins. Weaker evidence never overrides stronger.

1. Runtime and artifact truth: logs, deployed config, generated files,
   screenshots, process state, live API responses.
2. Repo truth: source, config, tests, diffs, commits.
3. External truth: upstream docs, API behaviour, package versions.
4. Documents supplied by the user: specs, plans, briefs.
5. Memory and chat summaries.
6. Inference.

Memory and chat are navigation aids, not proof. A finding with no hand-traced
input is a hypothesis.

## Severity

- **BLOCKER**: unsafe to merge, ship, or approve. A false claim, a likely
  data, security, money, or runtime loss, or missing hard-gate evidence.
- **HIGH**: likely production breakage, silent wrong results, a missing
  critical test, a serious operational gap.
- **MEDIUM**: edge-case breakage, a maintenance trap, thin observability.
- **LOW**: cleanup, naming, small doc or style drift.
- **QUESTION**: an ambiguity that blocks confidence until answered.

Any BLOCKER means no approval. Several HIGHs usually mean no approval unless
the owner accepts them with a stated mitigation.

## Fix policy

- Fix every BLOCKER.
- Fix a HIGH only if it changes the decision or protects a full-rigour asset.
- List MEDIUM and LOW in one line each and leave them unless asked.
  Backwards-compatibility and code-tidiness points are LOW by default on MVP work.
- One review pass. Open a second round only for a reproduced blocker or a
  material change in risk.
- **Containment is a valid fix.** If a blocker cannot be fixed in this layer,
  disable the unsafe path, narrow the claim, and route the real fix to a
  separate approval.
- **Cap the loop.** If rounds keep producing narrower requirements, freeze a
  finite checklist and an exact snapshot, and require a reproduction for any
  new blocker. If a finding flips back to a position it already held on
  unchanged code, stop and hand the open findings to the owner.
- If the user says the review is taking too long, treat that as a scope
  correction. State the decision status first, then offer a bounded close.

## Decision truth probe

For work that creates confidence (benchmarks, backtests, revenue numbers,
security claims, customer-facing claims), ask before approving:

1. What decision does this work unlock?
2. What underlying fact must be true for that decision not to mislead?
3. Is that fact observed and reconciled, or modelled, inferred, or scaffolded?
4. Would a cheaper prerequisite improve that truth more than this task?

Scaling, automating, or packaging on top of weak truth is at least a HIGH.

## Attack checklist

Run all twelve at Paranoid depth and above. At MVP depth use 1, 2, and 12.

1. What is the strongest claim, and what evidence proves it?
2. What could be silently wrong while every visible check stays green?
3. Which retry, restart, concurrency, or partial-failure path went untested?
4. Which trust boundary moved?
5. What is the dual of the last fix, and did this change introduce it?
6. Which external API, doc, or version assumption could be stale?
7. What data could be lost, duplicated, corrupted, or misfiled?
8. What operator action could make this unsafe or confusing?
9. Which metric is a proxy posing as an outcome?
10. What is the rollback or stop path if this is wrong in production?
11. What concrete input would expose the bug if the concern is real?
12. What one negative probe would most cheaply falsify the happy story?

For deeper adversarial passes, `paranoid-review`, `premortem`, and `steelman`
from the `claude-thinking-skills` pack fit here.

## Independent reviewers

- An external model or agent audit is evidence, not proof. Save its output.
  Spot-check its top claims against the repo or runtime before you report
  them as verified.
- Freeze and name the snapshot (commit SHA) before the reviewer starts. Do not
  edit reviewed files while it runs. Reconcile each finding against the
  current head afterwards.
- Do not sign off while an independent review is still pending. If it lands
  after sign-off and finds a defect, retract the sign-off in writing, add a
  failing test per gap, fix, and re-run the full gate.
- When you hand an audit to a fresh session, write a self-contained prompt:
  repo and exact commit, the decision it gates, the invariants, allowed
  checks, credential limits, and the verdict format below.

## Output contract

Use this unless a loaded skill sets a stricter one. Omit empty sections.

```md
## Audit Route
- Target:
- Audit class:
- Depth:
- Skills used:
- Evidence inspected:
- Evidence missing:

## Verdict
PASS / PASS WITH RISKS / FAIL / INCONCLUSIVE

## Findings
- [BLOCKER|HIGH|MEDIUM|LOW|QUESTION] path/artifact — the risk, the evidence,
  why checks could miss it, the fix or check required.

## Claim Ledger
| Claim | Evidence | Status |
| --- | --- | --- |

## Required Next Checks
- ...
```

Keep chat summaries short. Put long reports in a file and link it.

## Pitfalls

At MVP depth only the truth pitfalls apply: do not claim what you did not check.

- Running a generic code review when the real risk is runtime, data, or money.
- Reviewing a plan without comparing it to the repo.
- Treating CI as proof of business correctness, or repo config as proof of
  what is deployed.
- Approving a clean diff when the surrounding code holds the bug.
- Calling something verified without opening the artifact.
- Treating a build that is still compiling as a pass. The exact process must
  exit 0.
- Reading a killed or timed-out local CI watcher as the CI result. Query the
  remote run and match its SHA to the head you reviewed.
- Treating a credential file that exists as a credential that works against
  the exact target.
- Treating mocked tests as evidence that the real boundary was exercised.
- Running a Paranoid audit on MVP work, or fixing every MEDIUM and LOW.
  That is process theatre.
- Forgetting the user may want a wild adversarial pass when they ask for one.
