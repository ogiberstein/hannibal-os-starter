import tempfile
import unittest
from pathlib import Path

from scripts.render_project_templates import render_files

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RISK_GATES = {
    "production_changes",
    "credential_changes",
    "permission_changes",
    "data_deletion",
    "spending",
    "external_messages",
}


class TemplateTests(unittest.TestCase):
    def test_runtime_templates_use_placeholders(self):
        router = (ROOT / "templates/runtime/profile_router.yaml.example").read_text(encoding="utf-8")
        self.assertIn("CHANNEL_ID_HERE", router)
        self.assertIn("profile: project_agent", router)
        self.assertNotRegex(router, r"\b[0-9]{17,20}\b")

    def test_project_templates_exist(self):
        for name in ["AGENTS.md", "BRIEF.md", "STATUS.md", "DECISIONS.md"]:
            self.assertTrue((ROOT / "templates/project" / name).exists())

    def test_readme_has_marketing_and_hermes_setup_path(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Why use this?", readme)
        self.assertIn("Start here: “I want to set up Hermes”", readme)
        self.assertIn("https://github.com/ogiberstein/hannibal-os-starter.git", readme)
        self.assertIn("separate private deployment workspace", readme)
        self.assertIn("not production infrastructure", readme)

    def test_profile_risk_gates_match_canonical_set(self):
        for path in (ROOT / "templates/profiles").glob("*.yaml.example"):
            text = path.read_text(encoding="utf-8")
            for gate in REQUIRED_RISK_GATES:
                self.assertIn(f"- {gate}", text, path.name)

    def test_config_uses_private_profiles_directory(self):
        config = (ROOT / "templates/runtime/config.yaml.example").read_text(encoding="utf-8")
        self.assertIn("directory: profiles", config)
        self.assertNotIn("directory: templates/profiles", config)

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


if __name__ == "__main__":
    unittest.main()
