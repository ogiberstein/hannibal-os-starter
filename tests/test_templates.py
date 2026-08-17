import tempfile
import unittest
from pathlib import Path

from scripts.render_project_templates import render_files

ROOT = Path(__file__).resolve().parents[1]
RELEASE_TAG = "v2026.8.3"
RELEASE_COMMIT = "3c27eb6234bf91b8ceee9e9071591b31e9b148cb"
MAIN_COMMIT = "f51aa6a9b5ce514e15f8e337777f522fd5cc6fa2"


class TemplateTests(unittest.TestCase):
    def test_native_routing_fragment_uses_placeholders(self):
        config = (ROOT / "templates/runtime/config.yaml.example").read_text(encoding="utf-8")
        for required in [
            "gateway:",
            "multiplex_profiles: true",
            "profile_routes:",
            "chat_id: CHAT_ID_HERE",
            "profile: chief_of_staff",
            "profile: project_agent",
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
        for name in ["AGENTS.md", "BRIEF.md", "STATUS.md", "DECISIONS.md"]:
            self.assertTrue((ROOT / "templates/project" / name).exists())

    def test_readme_states_pause_v2_and_exact_compatibility(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("commercial and product work on hannibal os is paused", readme.lower())
        for required in [
            "not an actively supported hosted product",
            "V2 operating model",
            "persistent operator/DM front door",
            "gateway.profile_routes",
            "v2026.8.3` warns and falls back",
            RELEASE_TAG,
            RELEASE_COMMIT,
            MAIN_COMMIT,
            "No live Hermes profile, route, credential, gateway, service, or runtime was changed",
            "https://hermes-agent.nousresearch.com/docs/user-guide/profiles",
            "https://github.com/ogiberstein/hannibal-os-starter.git",
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
            "Bounded project lane",
            "Unmatched fallback",
            "version: `v2026.8.3` warns and falls back",
            "not runtime-tested",
        ]:
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
