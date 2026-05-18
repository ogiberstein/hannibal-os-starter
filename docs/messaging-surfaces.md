# Messaging Surfaces

Messaging surfaces are entry points into profiles: Slack channels, Discord channels, Telegram chats, email aliases, or other adapters supported by your runtime.

## Public-safe routing rule

Docs may describe labels, not live IDs.

Good:

```yaml
routes:
  - label: project-channel
    platform: slack
    target: CHANNEL_ID_HERE
    profile: project_agent
```

Bad:

```yaml
routes:
  - target: real-live-channel-or-user-id
```

## Smoke-test labels

Every private instance should prove:

1. project channel routes to the intended profile
2. default or Chief-of-Staff route works
3. restart/recovery preserves routing
4. one scheduled update delivers to the intended target
