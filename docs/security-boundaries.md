# Security Boundaries

This starter encourages safe defaults, but it is not a security or compliance guarantee.

## Safe defaults

- Single-tenant first.
- Secrets only in local `.env` or a password manager.
- No live sessions, memories, logs, backups, or transcripts in git.
- Presence-only diagnostics.
- Human approval for production, permission, deletion, spending, external-message, or credential changes.

## Host basics for an always-on agent server

An agent that can run shell commands can read every secret its user can read. One prompt injection is enough. Keep the box small and the credentials narrow:

- **SSH by key only.** Set `PasswordAuthentication no`, `KbdInteractiveAuthentication no` and `PermitRootLogin prohibit-password` in a drop-in that sorts before the cloud image's own file (for example `/etc/ssh/sshd_config.d/00-key-only.conf`). Check with `sshd -t` and `sshd -T`, and keep a console login ready before you reload.
- **Firewall on, deny incoming by default.** Open only SSH and the web ports you serve (for example `ufw default deny incoming`, then allow 22, 80 and 443, and allow SSH before you run `ufw enable`). This stops an agent's dev server bound to `0.0.0.0` from being reachable. Ports published by Docker bypass `ufw`, so bind container ports to `127.0.0.1`.
- **No public route to the Hermes dashboard.** Keep it on loopback and reach it through an SSH tunnel.
- **Remove what you do not use**: old reverse-proxy routes, VPN agents, desktop backends, logged-out messaging sessions, old `.env` copies.
- **Limit credential reach.** Give the server's GitHub login access only to the orgs and repos the agents work on. Prefer secrets the platform will not show again (write-only variables) over readable ones.

## Not promised

- Self-serve SaaS.
- Multi-tenant isolation.
- Formal compliance.
- Confidential compute.
- Protection from a compromised host.
- Protection from unsafe third-party integrations.
