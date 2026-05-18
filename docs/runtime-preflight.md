# Runtime Preflight

A preflight should answer: "Is this instance configured enough to smoke test?" It should not expose secrets.

## Check presence only

- `.env` exists locally.
- Required key names are present.
- Config file exists.
- Profile router exists.
- Runtime checkout or package exists.
- Service wrapper exists if using a long-running gateway.
- Placeholders have been replaced in private local config.

## Do not

- Source `.env` as shell code.
- Print key values.
- Print raw platform IDs.
- Print transcripts, logs, sessions, memories, or backups.
- Mutate runtime checkouts unless the operator explicitly asks for an upgrade.
