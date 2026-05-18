# Secret Handling

## Rules

- Keep credentials out of git.
- Keep `.env` local-only.
- Prefer a password manager or secret manager for real deployments.
- Never paste tokens, API keys, private keys, OAuth secrets, or raw platform IDs into issues, pull requests, docs, or chat logs.
- Diagnostics should report key presence and placeholder status, not values.

## Bad diagnostic examples

Do not run commands that print values such as `grep TOKEN .env`.

## Better diagnostic examples

Use scripts that say `MODEL_API_KEY: present` or `MODEL_API_KEY: missing` without printing the value.
