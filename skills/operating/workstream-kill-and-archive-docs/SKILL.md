---
name: workstream-kill-and-archive-docs
description: Use when the owner kills or parks a project, feature track or experiment and the repo still reads as if it were active. Updates control docs, archives stale plans and code, logs the decision, and verifies no active-state language remains.
version: 1.0.0
author: Hannibal OS Starter
license: MIT
metadata:
  hermes:
    tags: [project-hygiene, archive, documentation, status, decisions]
    related_skills: [status-refresh, handover-bootstrap, true-stuck-check-reporting, plain-style]
---

# Workstream Kill and Archive Docs

## Use when

- The owner explicitly kills a strategy, feature track, experiment or
  workstream.
- The owner parks a repo or workstream and wants it out of daily review, with
  clear rules for coming back.
- The owner wants a repo refocused on one active lane, with everything else
  archived but not deleted.
- Repo docs still show the lane as active, pending, blocked or gated even
  though it is killed or parked.
- The repo uses control docs such as `STATUS.md`, `BRIEF.md`, `DECISIONS.md`,
  `README.md`, plus plans, runbooks and specs.

## Kill vs park

- **Killed:** the lane is over. Archive it and log why. No re-entry rule needed.
- **Parked:** the lane may return. Archive or label it, and write the exact
  re-entry rule (the first action, and what must be re-checked before
  trusting local state).

## Goal

Make the repo tell the truth immediately:

- the workstream is dead or parked;
- no active gate or blocker language remains in control docs unless real
  execution is happening;
- old docs are preserved as history, not silently deleted;
- a future operator can see the re-entry rule before trusting repo state.

## Procedure

### 1. Read the control docs first

Read `AGENTS.md` if present, then `STATUS.md`, `BRIEF.md`, `DECISIONS.md` and
`README.md`. In a harness-managed repo these are the main state surface.

### 2. Find every stale active-state reference

Search for the workstream name, its aliases and code names, and status words
such as: `active`, `in progress`, `pending`, `decision gate`, `go/no-go`,
`Draft for execution`, `runbook`, `active path`.

### 3. Update the control docs

- **`STATUS.md`**
  - Set the phase to killed, paused or regrouping, or `Parked`.
  - Move the workstream's tasks out of `In Progress`.
  - For parked work, do not list prerequisites as `Blocked`. Record them as
    re-entry notes. "Blocked" implies execution is being prevented.
  - Set `Next Step` to `None while parked` when no action is wanted, and state
    the first reactivation action.
  - Add a completed item saying the workstream was killed and why, or a
    parked note explaining why repo state is not decision-grade.
- **`BRIEF.md`**: remove statements that imply the work is active. Add a note
  that it is closed or parked if future operators need to know.
- **`DECISIONS.md`**: add an entry with the date, the rationale and which
  earlier decisions it supersedes.
- **`README.md`**: add a current-posture note at the top. Mark affected
  commands, runbooks and schedules as archived or do-not-run.

### 4. Label historical docs, don't pretend-delete them

For plans, runbooks, specs and reviews tied to the dead lane:

- prefix titles with `(Archived)` or `(Historical)`;
- add a short banner near the top with the date and "do not treat as active";
- keep the historical content unless the owner asked for deletion.

Banner template:

```markdown
> **Archived (YYYY-MM-DD).** This workstream was <killed|parked>. Kept for
> reference only. Do not run or follow this document.
> Re-entry: <first action and what to re-check, or "none">.
```

### 5. Archive code too, if the repo should read as one lane

When stale code, tests, config or scripts still dominate the repo:

- create `archive/<lane-name>/` (or `archive/legacy-<lane>/`);
- move whole vertical slices together with `git mv`: config, scripts, source,
  tests and any tracked sample outputs;
- add `archive/README.md` stating the directory is preserved reference only;
- leave only the active code path, tests and operator commands at top level;
- simplify the CLI or package entry points so stale commands are no longer the
  defaults;
- rewrite `README.md`, `BRIEF.md`, `STATUS.md` and active runbooks so a new
  reviewer can find the live lane in about 30 seconds.

If only the docs are stale and the code is still in use, do not archive code.

### 6. Fix internal contradictions

- Fix lines like `Status: Draft for execution` in archived specs.
- Reword lines that still call the workstream the active path.
- Prefer a `Historical note:` over rewriting history.

### 7. Update outside surfaces that are canonical

If the project is also tracked outside the repo, update those in the same
pass so it does not re-enter daily review through stale notes:

- project pages, decision logs and portfolio registers in your notes vault or
  dashboard;
- agent memory entries about the project;
- cross-project maps that list allocation status.

Use the repo's decision entry as the source of truth. Mark the project
`Parked` (or killed), move it out of the default review surface, and set the
next step to `None while parked` unless a concrete re-entry trigger exists.

### 8. Verify

- Run `git diff` on touched docs and moved files.
- Search again for stale active-state phrases, in the repo and in outside
  surfaces.
- Confirm remaining hits are history, archive banners or preserved artifacts.
- Check markdown tables for rows broken by automated edits.
- Run a small secret scan over the staged diff. Confirm untracked files that
  hold credentials stay untracked.
- If code moved, run the smallest active test suite and the CLI help path to
  prove the narrowed repo still works.
- For docs-only changes, `git diff --check` plus the targeted search is
  usually enough.
- Commit and push after checking `git status`, `git diff --cached --stat` and
  the staged diff, if the repo convention allows.

## Output

Report:

- which docs and paths changed;
- the new repo posture (killed or parked, plus the re-entry rule);
- any remaining untracked or unrelated changes you left alone.

## Pitfalls

- Updating only `STATUS.md` while `README.md` or specs still describe active
  work.
- Deleting historical docs when an archive label is enough.
- Calling parked prerequisites `Blocked`.
- Trying to clean all dirty local work when the owner only asked for docs
  hygiene. Prefer a bounded docs-only commit if other changes are unrelated or
  unreviewed.
- Leaving contradictory fields like `Draft for execution`.
- Forgetting the decision-log entry.
- Treating every historical mention as a bug. Not every reference should go.
