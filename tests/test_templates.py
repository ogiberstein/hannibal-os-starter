import tempfile
import unittest
from pathlib import Path

from scripts.render_project_templates import render_files

ROOT = Path(__file__).resolve().parents[1]
CHECKED_SOURCE = "v0.22.2"
CHECKED_DOCS = "v0.22.5"


class TemplateTests(unittest.TestCase):
    def test_native_routing_fragment_uses_placeholders(self):
        config = (ROOT / "templates/runtime/config.yaml.example").read_text(encoding="utf-8")
        for required in [
            "gateway:",
            "multiplex_profiles: true",
            "profile_routes:",
            "chat_id: CHAT_ID_HERE",
            "profile: chief_of_staff",
            "profile: cio",
            "channel_prompts:",
            CHECKED_SOURCE,
        ]:
            self.assertIn(required, config)
        self.assertNotIn("multiplex_profile_allowlist", config)
        self.assertNotRegex(config, r"\b[0-9]{17,20}\b")

    def test_obsolete_v1_runtime_templates_are_absent(self):
        for relative in [
            "templates/runtime/env.example",
            "templates/runtime/profile_router.yaml.example",
            "templates/profiles/chief_of_staff.yaml.example",
            "templates/profiles/project_agent.yaml.example",
        ]:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_project_templates_exist(self):
        for name in ["AGENTS.md", "BRIEF.md", "STATUS.md", "ROADMAP.md", "DECISIONS.md"]:
            self.assertTrue((ROOT / "templates/project" / name).exists())

    def test_role_contracts_use_placeholder_operator(self):
        for name in ["chief_of_staff.role.md", "default.role.md", "cio.role.md", "SOUL.md"]:
            text = (ROOT / "templates/soul" / name).read_text(encoding="utf-8")
            self.assertIn("OPERATOR", text)

    def test_readme_states_scope_loop_and_compatibility(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for required in [
            "This is a reference, not a product.",
            "### The build loop",
            "**You approve the spec.**",
            "**You merge.**",
            "gateway.profile_routes",
            "slack.channel_prompts",
            CHECKED_SOURCE,
            CHECKED_DOCS,
            "Nothing in this pass changed or exercised a live gateway.",
            "https://hermes-agent.nousresearch.com/docs/user-guide/profiles",
            "https://github.com/ogiberstein/hannibal-os-starter.git",
            "docs/claude-hermes-build-loop.md",
            "docs/runtime-updates.md",
            "### Three profiles",
        ]:
            self.assertIn(required, readme)

    def test_current_docs_do_not_require_v1_custom_contract(self):
        current_paths = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
        forbidden = [
            "HERMES_GATEWAY_SESSION=1",
            "HERMES_TERMINAL_SYSTEMD_ISOLATION=1",
            "_gateway_systemd_isolation_enabled",
            "_systemd_run_command",
            "hermes-terminal-pty-*",
            "durable comeback notification markers",
            "profile_router.yaml",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in current_paths)
        for value in forbidden:
            self.assertNotIn(value, combined)

    def test_render_project_templates_refuses_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            (output / "STATUS.md").write_text("existing\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                render_files(output, "My Team", dry_run=False, force=False)

    def test_render_project_templates_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            targets = render_files(output, "My Team", dry_run=True, force=False)
            self.assertTrue(targets)
            self.assertFalse(any(target.exists() for target in targets))

    def test_smoke_playbook_covers_current_role_journey_and_truth_limit(self):
        text = (ROOT / "docs/smoke-test-playbook.md").read_text(encoding="utf-8")
        for required in [
            "Chief-of-Staff DM",
            "Domain lead and project channels",
            "Unmatched fallback",
            "rejects that chat's messages",
            "One real build slice",
            "not runtime-tested",
        ]:
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
