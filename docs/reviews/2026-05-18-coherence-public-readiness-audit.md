# Coherence and Public-Readiness Audit — Hannibal OS Starter

Date: 2026-05-18T11:36:24Z
Target: `hannibal-os-starter`
Scope: public-release safety, repo coherence, README/product positioning, Hermes setup journey, scripts/tests/templates consistency.

## Audit route

- Audit type: repo-stage/product/coherence audit.
- Escalation depth: paranoid for public-safety boundaries and first-user setup clarity.
- Evidence inspected: git state, README, docs, templates, scripts, tests, CI, local verification output, independent audit artifacts.
- Independent artifacts:
  - `/tmp/hannibal-os-starter-public-release-audit-2026-05-18.md`
  - `/tmp/hannibal-os-starter-readme-founder-marketing-audit.md`
  - `/tmp/hannibal-os-starter-post-change-audit.md`

## Initial verdict before fixes

Not ready for public release as-is. No tracked secret/customer leak was found, but the repo had safety and coherence gaps:

- sanitizer missed common unquoted/JSON secrets and several platform-ID/key-header formats;
- verification did not enforce several public/private boundary claims;
- README did not give a strong “why use this?” or a clear Hermes setup path;
- quick start copied private config into the starter checkout;
- docs/templates used inconsistent profile names and risk gates;
- template renderer could overwrite existing project docs without confirmation.

## Changes made from audit

- Rewrote `README.md` around a marketing-focused but honest promise:
  - why use this instead of only installing Hermes;
  - who it is for / not for;
  - what the repo gives;
  - how the starter relates to Hermes;
  - step-by-step path from “I want to set up Hermes” to private deployment, preflight, gateway start, smoke tests, and go/no-go.
- Changed quick start to create a separate private deployment workspace instead of placing live config in the public starter checkout.
- Strengthened `scripts/sanitize_repo.py`:
  - unquoted env-style secrets;
  - JSON/config-style secrets;
  - OpenSSH/private-key headers;
  - Slack-like non-channel IDs;
  - long numeric IDs;
  - Telegram-style chat IDs;
  - phone-like values;
  - broader text suffix coverage.
- Added regression tests for the new scanner cases.
- Made `scripts/render_project_templates.py` refuse overwrites unless `--force` is passed and added `--dry-run`.
- Added tests for render dry-run and overwrite refusal.
- Aligned profile naming to `project_agent` in routing docs/templates.
- Aligned high-risk approval gates across profile templates and runtime config.
- Changed runtime config profile directory to `profiles` for the private deployment layout.

## Verification after fixes

Command run from repo root:

```bash
python3 scripts/verify_repo.py
```

Result: PASS.

Checks covered:

- Python compile;
- whitespace/final-newline check;
- sanitation scan;
- unit tests.

Current unit-test count after fixes: 15 passing tests.

Additional check:

```bash
git diff --check
```

Result: PASS.

## Post-change independent audit

Independent post-change audit verdict: conditional pass for public release. It found:

- one medium sanitizer gap for Telegram-style negative chat IDs;
- one low README ambiguity around profile `.yaml.example` copying;
- one low terminology drift around Project Operator vs Project Agent.

All three were patched:

- Telegram regex changed to detect negative chat IDs without relying on a leading word boundary;
- README now copies profile examples into private deployment as `.yaml` files;
- context docs now use Project Agent terminology.

## Final verdict

PASS WITH RISKS for private staging / public go-no-go review.

No known tracked secret, customer data, raw platform ID, live runtime state, or private deployment artifact is present after the fixes. The repo is materially more coherent for a first-time technical founder/operator starting from Hermes setup.

## Remaining risks / explicit non-claims

- This is still a v0 starter/reference kit, not production infrastructure.
- It does not install Hermes or guarantee compatibility with every Hermes packaging/runtime command; README intentionally tells users to follow their Hermes runtime install/start path.
- Sanitation is a guardrail, not a formal secret-detection guarantee.
- Public release should still be a separate visibility go/no-go after reviewing the GitHub-rendered README and CI on the final commit.
