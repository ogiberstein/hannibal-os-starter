# Messaging Surfaces and Native Routing

Hermes messaging platforms are the entry points. Hannibal adds role intent, not a parallel router.

Current released Hermes supports `gateway.profile_routes` when `gateway.multiplex_profiles` is enabled. Routes may match `platform` plus optional `guild_id`, `chat_id`, and `thread_id`, then select a native profile. Matching is most-specific-first. Unmatched traffic stays on the default/active profile.

## Public-safe example

```yaml
gateway:
  multiplex_profiles: true
  profile_routes:
    - name: operator-dm
      platform: PLATFORM_NAME_HERE
      chat_id: CHAT_ID_HERE
      profile: chief_of_staff
    - name: bounded-project-lane
      platform: PLATFORM_NAME_HERE
      chat_id: PROJECT_CHAT_ID_HERE
      profile: project_agent
```

Merge this into the default profile's existing `config.yaml`; do not replace a working configuration wholesale. Use raw IDs only in private local config. Do not put them in this repo, screenshots, issues, logs, or support messages.

The included fragment is the common subset between the verified released and upstream commits. In `v2026.8.3`, a route naming a missing profile logs a warning and falls back to the default home. At inspected upstream `main`, a missing profile—or a profile excluded by the newer `multiplex_profile_allowlist`—causes ingress rejection. Verify the exact installed behavior, ensure every route target exists, and configure any supported allowlist before restart.

For current syntax and lifecycle commands, use the official [multi-profile gateway documentation](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways).
