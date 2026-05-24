import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SKILLS = {
    "handover-bootstrap": [
        "project packet",
        "STATUS.md",
        "BRIEF.md",
        "DECISIONS.md",
        "no secrets",
    ],
    "status-refresh": [
        "Verified facts",
        "Inference",
        "Next:",
        "STATUS.md",
    ],
    "evidence-gate": [
        "claim ledger",
        "PASS",
        "INCONCLUSIVE",
        "evidence",
    ],
}
PUBLIC_COMMANDS = {
    "handover-bootstrap.md": "Use the handover-bootstrap skill",
    "status-refresh.md": "Use the status-refresh skill",
    "evidence-gate.md": "Use the evidence-gate skill",
}
FORBIDDEN_PUBLIC_PACK_MARKERS = [
    "En" + "scribe",
    "/" + "root" + "/",
    "~/" + ".hermes",
    "SLACK_BOT_TOKEN",
    "DISCORD_BOT_TOKEN",
    "TELEGRAM_BOT_TOKEN",
]


class PublicCommandSkillPackTests(unittest.TestCase):
    def skill_file(self, name: str) -> Path:
        return ROOT / "skills" / "hannibal-public" / name / "SKILL.md"

    def test_public_skills_have_frontmatter_and_customer_safe_content(self):
        for skill, required_phrases in PUBLIC_SKILLS.items():
            with self.subTest(skill=skill):
                path = self.skill_file(skill)
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"), path)
                frontmatter = text.split("---", 2)[1]
                self.assertIn(f"name: {skill}", frontmatter)
                self.assertRegex(frontmatter, r"description: .+")
                for phrase in required_phrases:
                    self.assertIn(phrase.lower(), text.lower())
                for marker in FORBIDDEN_PUBLIC_PACK_MARKERS:
                    self.assertNotIn(marker, text)
                self.assertNotRegex(text, r"\b[0-9]{17,20}\b")
                self.assertNotRegex(text, r"\b[CDGUTW][0-9][A-Z0-9]{8,}\b")
                self.assertNotRegex(text, r"(?<!\d)-100[0-9]{8,}\b")

    def test_command_examples_reference_public_skills_without_runtime_claims(self):
        for filename, expected in PUBLIC_COMMANDS.items():
            with self.subTest(command=filename):
                path = ROOT / "commands" / "examples" / filename
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                self.assertIn(expected, text)
                self.assertIn("private deployment", text)
                self.assertNotIn("automatically installs", text.lower())
                for marker in FORBIDDEN_PUBLIC_PACK_MARKERS:
                    self.assertNotIn(marker, text)
                self.assertNotRegex(text, r"\b[0-9]{17,20}\b")
                self.assertNotRegex(text, r"\b[CDGUTW][0-9][A-Z0-9]{8,}\b")
                self.assertNotRegex(text, r"(?<!\d)-100[0-9]{8,}\b")

    def test_readme_and_changelog_explain_optional_public_pack(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        for required in [
            "Optional public command and skill examples",
            "skills/hannibal-public/",
            "commands/examples/",
            "does not automatically install these into Hermes",
        ]:
            self.assertIn(required, readme)
        for required in [
            "public command and skill examples",
            "handover-bootstrap",
            "status-refresh",
            "evidence-gate",
        ]:
            self.assertIn(required, changelog)


if __name__ == "__main__":
    unittest.main()
