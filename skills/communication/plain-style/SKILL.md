---
name: plain-style
description: Use when writing or editing prose a human will read outside the chat, such as docs, READMEs, PR descriptions, release notes, user-facing copy or emails. Applies plain-English rules without losing accuracy. Not for chat replies or code comments.
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [writing, style, documentation, plain-english, communication]
    related_skills: [humanizer, anti-slop-agent-guardrails]
---

# Plain style

Write for a smart reader with no time. Match jargon to the audience:
end-user copy assumes no technical background; engineer-facing docs (PR
descriptions, READMEs, design docs) stay technical but still follow every
rule below. When a rule and accuracy collide, accuracy wins.

## Scope

- Use for: docs, READMEs, PR descriptions, release notes, user-facing copy,
  emails, reports a person will read later.
- Skip for: chat replies (keep those short by default instead), code
  comments, and verbatim quotes.

## Structure

- First sentence states the point. Context comes after, never before.
- One idea per sentence. A sentence that needs two commas gets split.
- Keep average sentence length under 20 words.
- Prose by default; a list only for 3+ genuinely parallel items.
- No closing summary that restates the piece.

## Words

- Common word always: use (not utilize/leverage), help (not facilitate),
  about (not approximately), before (not prior to), if (not in the event
  that), to (not in order to), several (not a number of), so (not
  therefore/thus).
- Kill nominalizations: decide (not make a decision), assess (not carry out
  an assessment), help (not provide assistance).
- Banned filler: simply, easily, seamlessly, robust, performant, actionable,
  cutting-edge, please note, it's worth noting, in today's world.
- Define any unavoidable technical term at first use. A few words in
  brackets are fine.
- Prefer active voice and present tense. Use second person where the reader
  acts. Use past tense for records of what happened (release notes, incident
  reports).

## Accuracy under compression

- Numbers, thresholds and scoped conditions stay exact. Never round,
  generalize or widen them.
- Warnings and caveats stay attached to their point. Never defer them to the
  end, and never cut them for length.
- Do not claim more than the evidence shows. "Tested on Linux" is not
  "works everywhere".

## Before / after

- "In order to leverage this functionality, users are simply required to
  create an account" → "To use this feature, create an account."
- "Please note that it is not currently possible to export your data" →
  "You can't export your data yet."
- "This allows for the optimization of performance" → "This makes it faster."
- "An assessment should be carried out prior to deployment" → "Assess the
  change before you deploy."
- "We provide a robust, seamless solution for money management" → say what
  it does: "It tracks all your bank accounts in one place."

## Self-check before you hand it over

1. Does the first sentence state the point?
2. Any banned filler or nominalization left?
3. Are all numbers, limits and conditions exactly as in the source?
4. Is every caveat next to the claim it limits?
5. Would a reader who skips the last paragraph lose anything? If not, cut it.
