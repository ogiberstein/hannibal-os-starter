# Contributing

Contributions are welcome if they keep this repo public-safe and starter-focused.

## Contribution rules

- Do not include credentials, tokens, private keys, `.env` values, or screenshots containing secrets.
- Do not include live Slack, Discord, Telegram, WhatsApp, email, phone, user, workspace, server, channel, chat, or thread IDs.
- Do not include private customer data, transcripts, logs, memories, sessions, backups, deployment evidence, or support bundles.
- Use obvious placeholders such as `CHANNEL_ID_HERE`, not realistic numeric fake IDs.
- Keep examples generic and reusable.
- Run `python3 scripts/verify_repo.py` before opening a pull request.

## Good contributions

- Clearer operating playbooks.
- Safer sanitation checks.
- Better placeholder templates.
- Runtime-agnostic docs that preserve local/private state boundaries.
- Small scripts that are dry-run or read-only by default.

## Out of scope

- Hosted SaaS infrastructure.
- Multi-tenant control planes.
- Customer-specific configuration.
- Runtime patches that have not been generalized into public-safe requirements.
