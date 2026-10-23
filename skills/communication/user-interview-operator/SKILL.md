---
name: user-interview-operator
description: Use when running or synthesizing user or customer discovery interviews, or validating pain, willingness to pay and adoption risk before building. Neutral one-question-at-a-time probing, evidence tagging and a decision-ready summary.
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [user-research, interviews, discovery, product, validation]
    related_skills: [spec-interview, evidence-gate, writing-plans, plain-style]
---

# User Interview Operator

## Purpose

Collect decision-grade user insight fast, without leading questions, fluff or
early solutioning.

## Use when

- Discovery interviews with users or customers.
- Owner-led interviews where speed and signal quality matter.
- Pre-build validation of pain, willingness to pay and adoption risk.
- Turning raw interview notes or transcripts into a decision summary.

Not for: gathering requirements from the owner about what to build. Use
`spec-interview` for that.

## Two modes

- **Agent as interviewer (live chat):** ask one question per message. Wait for
  the answer. Reflect back in one line only when it helps confirm meaning.
- **Agent as synthesizer (human-led transcript):** work only from what is in
  the notes. Quote exactly, attribute to an anonymized participant label
  (P1, P2), and never invent or "tidy up" quotes.

## Interview defaults

- One question at a time.
- Short, neutral wording.
- Probe for specifics: examples, frequency, the last time it happened.
- Prioritize behavior over opinions.
- Do not pitch a solution until the evidence threshold is met.

## Hard rules

1. **No leading questions.**
   - Bad: "Would you pay $20/month for this?"
   - Better: "How do you handle this today?"
2. **Ask for concrete recent examples.**
   - "Tell me about the last time this happened."
3. **Quantify pain and frequency.**
   - "How often per week?"
   - "What does this cost you in time, money or stress?"
4. **Separate facts from interpretations.**
5. **Tag confidence explicitly** (High / Medium / Low) on every claim.
6. **End with decision implications, not generic takeaways.**

## Interview flow

### Phase 1: Context

- role and situation
- current workflow
- goals and constraints

### Phase 2: Problem reality

- trigger moments
- current workaround
- failure points
- severity and frequency

### Phase 3: Economics and behavior

- what they already pay for, or time spent
- switching friction
- adoption blockers
- trust and compliance concerns

### Phase 4: Validation

- recap key points to confirm understanding
- ask what would change their mind
- identify the strongest unresolved unknown

## Question bank (high signal)

- "Walk me through the last time you hit this problem."
- "What did you do instead?"
- "How often does this happen?"
- "What's the cost when this goes wrong?"
- "What have you tried already, and why didn't it stick?"
- "Who else is affected when this happens?"
- "If this got solved, what number would improve first?"

## Anti-patterns

- Interrogation mode: too many broad questions at once.
- Brainstorming features during the interview.
- Accepting vague statements without an example.
- Concluding from one or two responses.
- Mixing in context from other projects or channels.
- Counting compliments or "I'd use that" as demand.

## Privacy

Interview notes often contain names, employers and contact details. Keep them
out of shared channels and summaries. Use participant labels and store raw
notes where the owner decides.

## Output contract

Produce a concise report with this structure:

```markdown
# User Interview Summary: [Project], [Date]

## Executive Summary
- 3-5 bullets max

## Evidence Table
| Claim | Evidence (quote/behavior) | Confidence (H/M/L) | Notes |
|---|---|---|---|

## Facts vs Assumptions vs Unknowns
- Facts:
- Assumptions:
- Unknowns:

## Decision Implications
- Continue / pause / pivot signals
- What must be tested next
- What to avoid building yet

## Next Interview Questions
- 3-5 highest-leverage follow-ups
```

Omit a section rather than fill it with guesses. If the evidence is thin, say
so in the executive summary.

## Quality bar

A good interview output lets the owner answer:

1. Is the problem real and frequent enough?
2. Is there credible willingness to pay or intent to switch?
3. What single uncertainty should be tested next?
