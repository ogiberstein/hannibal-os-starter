# Messaging Surfaces and Native Routing

Hermes messaging platforms are the entry points. Hannibal adds role intent, not a parallel router.

Hermes supports `gateway.profile_routes` when `gateway.multiplex_profiles` is enabled. Routes may match `platform` plus optional `guild_id`, `chat_id`, `thread_id`, and `user_id`, then select a native profile. Matching is most-specific-first. Unmatched traffic stays on the default/active profile.

## Public-safe example

```yaml
gateway:
  multiplex_profiles: true
  profile_routes:
    - name: operator-dm
      platform: PLATFORM_NAME_HERE
      chat_id: CHAT_ID_HERE
      profile: chief_of_staff
    - name: markets-channel
      platform: PLATFORM_NAME_HERE
      chat_id: MARKETS_CHAT_ID_HERE
      profile: cio
```

Merge this into the default profile's existing `config.yaml`; do not replace a working configuration wholesale. Use raw IDs only in private local config. Do not put them in this repo, screenshots, issues, logs, or support messages.

Every route target must exist. In Hermes v0.22.x a route that names a missing profile rejects that chat's messages instead of falling back to `default`. The older `gateway.multiplex_profile_allowlist` key is retired; to stop serving a profile, park it (`hermes -p <name> gateway stop`) or delete it.

For per-channel project context without a separate profile, use `slack.channel_prompts` (see `templates/runtime/config.yaml.example`). Point each prompt at the repo's `STATUS.md` and `BRIEF.md` rather than copying state into config.

For current syntax and lifecycle commands, use the official [multi-profile gateway documentation](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways).
