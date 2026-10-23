---
name: spec-interview
description: "Use when requirements are unclear enough that writing a spec would force the agent to invent product decisions. Runs an adaptive, file-backed interview after project setup, one question at a time, and ends with an owner-confirmed shared model."
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [requirements, interview, product, specification, domain-modeling]
    related_skills: [writing-plans, user-interview-operator, evidence-gate, overengineering-defence, plain-style]
---

# Spec Interview

Build a shared product and domain model with the owner before anyone writes a
spec or code. The interview is adaptive and file-backed: each answer updates the
model, exposes consequences and decides the next question.

The goal is not to finish a questionnaire. It is to find and settle the
decisions that change what gets built, why, how it behaves, or what must be true
before it is credible.

## When to use

Use after project setup when:

- the context is known but the product model is unclear;
- a request hides consequential choices about users, scope, workflow, data,
  integrations, economics or risk;
- several plausible readings would lead to materially different plans;
- the owner wants to rethink direction or assumptions before a spec;
- building would otherwise force the agent to invent product decisions.

Suggest it in one line after setup: "Setup is done, but the product model is
still under-specified. I suggest a short requirements interview before the spec."

Skip it for trivial fixes, narrow implementation tasks, mechanical migrations,
copy edits, audits, incident response, or work that already has clear
requirements and acceptance checks.

If the gap is upstream strategy (target problem, primary user, value metric),
settle that first in a separate step. The interview may challenge strategy. It
must not silently invent it.

**Who runs it.** Your general engineering/PM agent. A coordinator or
chief-of-staff role runs one only when the owner asks for a cross-project
operating-model interview. Specialist roles run it only when they own the
requirements decision.

## Sequence

Run these as separate, serial steps:

1. **Setup:** repo and channel identified, freshness checked, control docs read.
2. **Interview:** a distinct file-backed session, optimised only for shared
   understanding and consequential decisions.
3. **Confirmation:** the model, corrections, superseded decisions and open truth
   gaps, explicitly confirmed by the owner.
4. **Downstream work:** audits, spec, plan, handoff or build, each as its own step.

Do not merge these into one prompt. A narrow fact check may support the next
question. It must not take over the session.

## State lives in files

Never rely on chat memory for what was asked, changed or superseded. Use repo
conventions if they exist. Otherwise:

- Ledger and evolving model: `docs/interviews/YYYY-MM-DD-<topic>-interview.md`
- Confirmed synthesis: `docs/interviews/YYYY-MM-DD-<topic>-synthesis.md`
- Spec, only after confirmation: `docs/specs/YYYY-MM-DD-<topic>-spec.md`

With no repo, use a scratch workspace and say it is not canonical.

Before every question: read the ledger; update the model with the last answer and
any verified facts; find the open branch with the largest effect; classify it
(see "Interview loop", step 4); ask exactly one question if it is an owner
choice. After the answer, write it to the ledger before doing anything else.

**Ledger hygiene.** Edit with exact-string replacements that assert each anchor
exists; a replace that silently matches nothing leaves the log stale. Append
answer blocks at the end of the answers section and check heading order
(`grep -n '^##'`). Update the State block on every write.

**Pre-seeded ledgers.** If another role prepared the ledger with fixed IDs and a
progress line, keep its structure; add a decision map and a "facts checked"
section. Order questions by decision value, not ID. Rows the brief already
answers are marked `drafted from brief; confirm at end` and stay open until
confirmation. New must-resolve branches get the next free ID and grow the total;
folding them into old IDs fakes progress.

**Logs that may be shown on screen.** Summarise personal items (list names, task
text, people) by category; do not echo them in chat. Refer to other projects and
hosts in general terms. Never copy sign-in URLs from tool output.

## Running it in chat

- Ask each question as a plain message and end the turn.
- After each answer, say in one or two sentences what changed in the model, give
  the progress line if one exists, then the next question. Do not paste the ledger.
- If an answer arrives cut off, log it as partial and ask only for the rest.
  Never guess the missing part.
- When a choice also needs an approval (new public URL, credential, spend), list
  each option with its cost and the fallback that needs no approval, so the
  answer settles the approval too.

## Bootstrap

1. Confirm setup is complete. If repo, branch or project boundary is unresolved,
   finish setup first.
2. Read the smallest relevant context: brief or status, strategy, decisions,
   existing specs, the request.
3. Check cheap, decision-relevant facts yourself (what already runs, syncs or is
   installed; what the repo already does). Log them as `observed`. Do not ask
   the owner for facts you can inspect.
4. Write an initial decision graph. It is a hypothesis, not a checklist.
5. Mark the strongest premise and the highest-consequence uncertainty.
6. Ask the question that most reduces decision uncertainty or could invalidate
   the largest part of the model.

The first reply confirms the context in one sentence and asks one question. No
interview plan.

## Decision graph, not questionnaire

Start only with branches the project supports:

- **Objective:** what outcome matters, for whom, over what horizon?
- **User and trigger:** who acts, when, and what happens just before and after?
- **Value or economics:** what is maximised, protected, paid for or traded off?
- **Domain model:** actors, objects, states, events, permissions, invariants.
- **Workflow:** the real end-to-end path, including failure and recovery.
- **Boundary:** in scope, out, manual, automated, deferred.
- **Constraints:** time, money, privacy, compliance, platform, reliability.
- **Truth gaps:** facts that must be observed, not assumed.
- **Acceptance:** observable behaviour that proves the first useful version works.

Add, split, close or reopen branches as the model changes.

## Interview loop

1. **Capture faithfully.** Keep the owner's material wording. Separate the
   answer, your interpretation, the consequence, and claims that need proof.
2. **Work out consequences.** If this is true, what follows? Which premise is
   strengthened or broken, which decision becomes possible or impossible, what
   changes in scope, workflow, architecture or acceptance, which branch appears
   or reopens. The interview earns its keep when answers change the model.
3. **Supersede explicitly.** Mark the old item `superseded` and link the answer
   that changed it. Never keep the model consistent by ignoring a conflict.
4. **Pick the next question by decision value.** Classify the open branch:
   - **Owner choice:** a preference, trade-off or boundary only the owner can
     set. Ask when it could change a consequential decision or the first slice.
   - **Agent-owned fact:** code, runtime, first-party behaviour, feasibility.
     Inspect it. If it needs a bigger audit, log the gap for later.
   - **Implied constraint:** already follows from a confirmed goal. State it in
     the model and invite correction at confirmation. Never ask the owner to
     choose between honouring a goal and defeating it. If it proves impossible,
     return with the real trade-off.

   Prefer owner choices that could reverse the objective, remove or create a
   major component, change the primary user or economics, expose an unproven
   prerequisite, change the first slice, or invalidate a prior decision. Check
   whether one concrete scenario could settle several linked ambiguities at once.

## Question quality

One short, neutral question at a time. Make the model more concrete; do not
steer toward your preferred solution.

Lead with a concrete case when related boundaries need defining: show the
trigger, the proposed action and who is affected, ask what should happen, then
state the rule. One scenario can settle a term and a permission boundary at once.

Use a binary only for a real owner trade-off. Name the failure cost without
implying one option is virtuous or that the list is exhaustive.

Useful forms:

- "Walk me through the last real example, from trigger to outcome."
- "If we optimise for X, what are you willing to make worse?"
- "What should happen when Y is missing, late or wrong?"
- "What case would break this rule?"
- "When you say 'automatic', which actions still need a person?"
- "What evidence would make us drop this direction?"
- "If speed and accuracy conflict here, which wins, and at what cost?"

A term is clear when two people would predict the same behaviour from it.

Avoid: leading yes/no questions; long option menus before the model exists;
abstract preference questions when an example exists; asking for facts in the
source material; solution pitches dressed as discovery; treating owner
statements as runtime or market proof.

## Provenance

Label every ledger entry `user_decision`, `observed`, `first_party`
(authoritative docs or source), `inferred` or `unresolved`.

Owner answers settle intent and acceptable trade-offs. They do not prove
external behaviour, deployed state, economics or security. If a factual gap
blocks the next decision, pause for the smallest research step, then resume with
a narrower question. Do not turn the interview into an audit.

## Checkpoints and stopping

Every five questions is a checkpoint, not a cap. Show only: model changes that
matter; reopened or superseded decisions; remaining consequential owner choices;
questions that turned out to be facts or implied constraints; whether another
round would change a decision.

Stop when the model is coherent enough for the next artifact, what remains is
research or deferrable detail, two questions in a row change no decision, or the
owner asks to stop.

## Confirmation gate

Write a compact proposed model:

1. objective and success condition;
2. primary user, trigger and value;
3. actors, objects, states, permissions and workflows;
4. clarified terms that affected decisions;
5. decisions and consequences;
6. superseded decisions and why;
7. scope and non-goals;
8. open truth gaps, each with an owner and downstream effect;
9. proposed changes to existing project docs;
10. the exact next artifact or evidence step.

Ask once: "Is this now the shared model, or what is still wrong?" If corrected,
re-show only the affected part. No execution-ready spec until confirmed.

Default to the MVP bar: simplicity and speed beat polish, no backwards
compatibility unless asked. Raise the bar only for money, secrets, customer or
user data, legal exposure, public products with external users, or irreversible
deletion.

## Ledger template

```markdown
# Interview: <project/feature> (YYYY-MM-DD)

## State
- Topic / Mode (new-project | feature | scope-rethink | gap-fill)
- Status: in_progress | awaiting_confirmation | confirmed | paused_for_fact
- Current question ID / Questions since checkpoint / Last updated

## Context read
## Current model
## Decision graph
| Node | Depends on | Hypothesis | Status | Consequence if wrong |
## Question ledger
| ID | Node | Question | Answer | Provenance | Consequence | Status |
## Superseded decisions
| Decision | Superseded by | Why | Docs affected |
## Terms under test
| Term | Competing meanings | Disambiguating scenario | Confirmed meaning |
## Truth gaps
| Gap | Why it matters | Owner/source | Blocks |
## Proposed shared model
```

## After confirmation

- Keep the ledger as evidence; write the synthesis separately.
- Propose the next artifact instead of silently creating everything.
- When authorised, patch existing specs and decisions; do not create competing truth.
- Move open factual gaps into an evidence plan, not more preference questions.

**Was it worth it?** A useful interview changes a decision, reopens an earlier
one, clarifies a term so predicted behaviour changes, or exposes a hidden truth
gap before the spec. If none of that happened, say so plainly.

## Pitfalls

- Bundling setup and interviewing.
- Treating the five-question checkpoint as a cap or a target.
- Building an evidence checklist instead of a decision graph.
- Agent-framed binaries, such as asking the owner to "choose" a constraint an
  agreed goal already implies.
- Never reopening earlier answers.
- Equating length with depth.
- Writing the spec before confirmation.
- Relying on chat memory instead of the ledger.

## Checklist

- [ ] Setup finished first; the ledger was read before every question.
- [ ] Each open branch was classified: owner choice, fact or implied constraint.
- [ ] Each answer has a consequence and a provenance label.
- [ ] Contradicted decisions are marked superseded.
- [ ] The interview stopped on falling decision value, not a count.
- [ ] The owner confirmed the model before spec, plan, audit or build.
