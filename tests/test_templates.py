import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TemplateTests(unittest.TestCase):
    def test_runtime_templates_use_placeholders(self):
        router = (ROOT / "templates/runtime/profile_router.yaml.example").read_text(encoding="utf-8")
        self.assertIn("CHANNEL_ID_HERE", router)
        self.assertNotRegex(router, r"\b[0-9]{17,20}\b")

    def test_project_templates_exist(self):
        for name in ["AGENTS.md", "BRIEF.md", "STATUS.md", "DECISIONS.md"]:
            self.assertTrue((ROOT / "templates/project" / name).exists())

    def test_readme_states_non_goals(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Not a hosted SaaS", readme)
        self.assertIn("not production infrastructure", readme)


if __name__ == "__main__":
    unittest.main()
