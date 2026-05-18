# First Deployment Checklist

Use this before treating a private instance as ready.

- [ ] Repo created from public-safe templates, not from private runtime state.
- [ ] Runtime chosen and installed outside this public starter repo.
- [ ] `.env` exists locally and is ignored by git.
- [ ] Config and profile router use local-only live IDs.
- [ ] Project `STATUS.md`, `BRIEF.md`, `DECISIONS.md`, and `AGENTS.md` exist.
- [ ] Secrets are customer/team-owned or operator-owned by explicit agreement.
- [ ] Runtime preflight passes without printing secret values.
- [ ] Smoke tests pass for project channel, default/CoS, restart/recovery, and scheduled update.
- [ ] Backup/restore path is documented.
- [ ] Support boundaries and escalation rules are clear.
