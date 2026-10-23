---
name: overengineering-defence
description: "Use when auditing any spec, plan, architecture, implementation handoff or incident fix. Cuts scope to the least permanent machinery that safely unlocks the decision, and keeps full rigour only where a real high-consequence asset is at risk."
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [audit, plans, specs, proportionality, simplicity, scope-control]
    related_skills: [audit-router, implementation-plan-adversarial-review, writing-plans, spec-interview]
---

# Overengineering Defence

## Overview

Run this pass inside every audit of a spec, plan, architecture or handoff. If you
use `audit-router`, load it first, then this skill, then narrower review skills.

The goal is not minimal code at any cost. It is the least permanent machinery
that safely unlocks the operator's actual decision. A recoverable internal
failure should not be prevented with a control that costs more to build, carry,
understand and remove than the failure costs to recover from.

## Default quality bar

Treat work as an MVP or personal system unless it falls in a high-stakes class:

- simplicity and speed beat polish;
- no backwards compatibility unless someone asks for it;
- fix blockers, not preferences;
- one review pass;
- every safeguard names the asset it protects.

Use full rigour only for money or funds, secrets or credentials, customer or
user data, legal exposure, public products with external users, and
irreversible deletion. Even there, ask whether the proposed mechanism is the
simplest adequate protection.

## When to use

Always for plan, spec, architecture and handoff audits; reliability, process,
automation and agent-operating-system proposals; and incident fixes that could
turn one failure into a permanent safety ratchet.

Do not use it to weaken necessary protection for the high-stakes classes above.

## Mandatory audit pass

Answer these in order before approving the work:

1. **Decision and value:** what operator or business decision does this unlock?
   "Improve the system" is not an outcome.
2. **Failure cost:** what exact asset is at risk, how likely is failure, and what
   realistically happens if it occurs?
3. **Recovery alternative:** can the failure be bounded, observed and cheaply
   reversed instead of prevented with permanent machinery?
4. **Existing truth:** what upstream feature, existing control, manual procedure
   or small config change already gives the outcome?
5. **Smallest coherent slice:** what can be deleted while still proving the
   decision at the real boundary?
6. **Carry cost:** what new code, state, service, dependency, document, gate,
   test suite, alert or operator step must be maintained afterwards?
7. **Opportunity cost:** what useful work does this delay, now and through
   future upkeep?
8. **Proof and stop:** what one decision-grade check proves the slice, and
   exactly when does the work stop?

If the plan does not answer these, the audit is incomplete.

## Deletion test

For every proposed component, ask:

- Which acceptance criterion fails if this is removed?
- Is that failure realistic and material, or merely imaginable?
- Does an existing component already cover it?
- Is a one-time check becoming a permanent subsystem?
- Is audit feedback creating new scope instead of testing the original decision?

Delete or defer anything without a load-bearing answer.

Preference order:

1. tolerate the recoverable failure;
2. document a short manual recovery;
3. use an existing upstream capability;
4. change configuration;
5. add a small reversible patch;
6. add a new permanent subsystem only when nothing earlier can protect a
   material asset.

## Keep the audit itself small

An audit can overengineer the work too. Default to:

- one bounded adversarial pass;
- primary-source evidence for the active decision only;
- the smallest focused test set that exercises the real failure boundary;
- an existing upstream regression test before writing a new synthetic fixture;
- one correction round, for concrete blockers only;
- no new review artifact unless execution, custody or a durable decision needs it;
- no broad test programme, roadmap rewrite, extra handoff or new control document
  unless the changed scope genuinely needs it.

Do not reopen the loop for style, hypothetical edge cases or a reviewer's wish
for completeness. Another round needs a reproduced blocker, a materially changed
risk, or a high-consequence truth gap.

## Red flags

- "Best practice" with no named asset and consequence.
- Preserving every historical invariant by default.
- A low-risk fix that needs several new gates or artifacts.
- Broad tests where one focused boundary test decides the issue.
- Custom logic where released upstream behaviour already exists.
- Monitoring added before the failure is made cheap to recover from.
- A one-off migration or check turning into a recurring service.
- Process documents created mainly to justify other process documents.
- One incident turned into "never again" architecture.
- More time spent proving the control than the failure would ever cost.

## Verdicts

- **PASS:** already the smallest coherent safe slice.
- **PASS WITH CUTS:** the outcome is valid, but named components must be removed
  or deferred before execution.
- **FAIL:** unsafe, false, or cannot prove the required decision.
- **STOP / DO NOTHING:** the expected value is negative; tolerate or recover
  from the failure instead.

A finding blocks only when it changes safety, truth or the decision. Excess
complexity blocks only when it would materially increase delay, failure risk or
ongoing burden.

## Required output

Keep the section short:

1. **Value at stake:** one sentence.
2. **Realistic failure cost and reversibility:** one sentence.
3. **Cut / keep:** the exact machinery to remove and the minimum controls to keep.
4. **Stopping rule:** one proof, at most one correction round, then stop.

## Pitfalls

1. **Turning this into another big checklist.** Use the eight questions and
   report only results that change a decision.
2. **Equating simple with careless.** High-consequence assets still need strong
   protection.
3. **Deleting the tests that prove the real boundary.** Keep the smallest causal
   regression test and the real operator journey.
4. **Rejecting all process.** Durable decisions, rollback ownership and live
   approvals stay when the risk warrants them.
5. **Demanding perfect evidence for a reversible choice.** Match confidence to
   consequence.

## Checklist

- [ ] Value, failure cost, reversibility, existing alternatives, carry cost and
      opportunity cost are stated.
- [ ] Every retained component is tied to a material acceptance criterion.
- [ ] At least one deletion, substitution or explicit "nothing to cut" decision
      was made.
- [ ] The audit names one decision-grade proof and a stopping rule.
- [ ] No permanent machinery was added just to satisfy the audit.
