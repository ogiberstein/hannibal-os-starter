import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(ROOT.glob("skills/*/*/SKILL.md"))
EXPECTED = {
    "build": {
        "spec-interview",
        "writing-plans",
        "overengineering-defence",
        "implementation-plan-adversarial-review",
        "hermes-build-operations",
        "audit-router",
    },
    "operating": {
        "agent-role-profile-design",
        "true-stuck-check-reporting",
        "workstream-kill-and-archive-docs",
        "evidence-gate",
        "handover-bootstrap",
        "status-refresh",
    },
    "communication": {"plain-style", "anti-slop-agent-guardrails", "user-interview-operator"},
}
# Skills that ship with upstream Hermes and may be named as related skills.
UPSTREAM_SKILLS = {
    "systematic-debugging",
    "test-driven-development",
    "requesting-code-review",
    "subagent-driven-development",
    "dogfood",
    "humanizer",
    "plan",
    "spike",
}
FORBIDDEN_MARKERS = [
    "En" + "scribe",
    "/" + "root" + "/",
    "~/" + ".hermes",
    "SLACK_BOT_TOKEN=",
    "DISCORD_BOT_TOKEN=",
    "TELEGRAM_BOT_TOKEN=",
]
PUBLIC_COMMANDS = {
    "handover-bootstrap.md": "Use the handover-bootstrap skill",
    "status-refresh.md": "Use the status-refresh skill",
    "evidence-gate.md": "Use the evidence-gate skill",
}


def frontmatter(text: str) -> dict[str, str]:
    """Minimal stdlib parser: top-level `key: value` pairs plus related_skills."""
    assert text.startswith("---\n"), "missing frontmatter"
    block = text.split("---", 2)[1]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"')
        m = re.match(r"^\s+related_skills:\s*\[(.*)\]\s*$", line)
        if m:
            fields["related_skills"] = m.group(1)
    return fields


class SkillPackTests(unittest.TestCase):
    def test_expected_skills_present(self):
        found: dict[str, set[str]] = {}
        for path in SKILLS:
            found.setdefault(path.parent.parent.name, set()).add(path.parent.name)
        self.assertEqual(found, EXPECTED)

    def test_frontmatter_is_portable(self):
        names = {p.parent.name for p in SKILLS}
        for path in SKILLS:
            with self.subTest(skill=path.parent.name):
                fm = frontmatter(path.read_text(encoding="utf-8"))
                self.assertEqual(fm.get("name"), path.parent.name)
                self.assertTrue(fm.get("description", "").startswith("Use when"), fm.get("description"))
                self.assertLessEqual(len(fm["description"]), 1024)
                self.assertEqual(fm.get("license"), "MIT")
                related = [s.strip() for s in fm.get("related_skills", "").split(",") if s.strip()]
                for rel in related:
                    self.assertIn(rel, names | UPSTREAM_SKILLS, f"{path}: unknown related skill {rel}")

    def test_skills_are_public_safe(self):
        for path in SKILLS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(skill=path.parent.name):
                for marker in FORBIDDEN_MARKERS:
                    self.assertNotIn(marker, text)
                self.assertNotRegex(text, r"\b[0-9]{17,20}\b")
                self.assertNotRegex(text, r"\b[CDGUTW][0-9][A-Z0-9]{8,}\b")
                self.assertNotRegex(text, r"(?<!\d)-100[0-9]{8,}\b")
                self.assertNotRegex(text, r"\bDEC-\d{3,}\b")

    def test_readme_lists_every_skill(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for path in SKILLS:
            self.assertIn(f"`{path.parent.name}`", readme)

    def test_command_examples_reference_shipped_skills(self):
        for filename, expected in PUBLIC_COMMANDS.items():
            with self.subTest(command=filename):
                text = (ROOT / "commands" / "examples" / filename).read_text(encoding="utf-8")
                self.assertIn(expected, text)
                self.assertIn("does not automatically install", text.lower())
                skill = expected.split()[2]
                self.assertTrue(any(p.parent.name == skill for p in SKILLS), skill)

    def test_installer_hermes_layout_and_no_clobber(self):
        with tempfile.TemporaryDirectory() as d:
            env = {**os.environ, "HERMES_HOME": d}
            script = str(ROOT / "scripts" / "install_skills.sh")
            subprocess.run(["bash", script, "hermes"], env=env, check=True, capture_output=True)
            for path in SKILLS:
                rel = path.relative_to(ROOT / "skills")
                self.assertTrue((Path(d) / "skills" / rel).is_file(), rel)
            marker = Path(d) / "skills" / "build" / "audit-router" / "SKILL.md"
            marker.write_text("local edit\n", encoding="utf-8")
            out = subprocess.run(["bash", script, "hermes"], env=env, check=True, capture_output=True, text=True)
            self.assertIn("skip", out.stdout)
            self.assertEqual(marker.read_text(encoding="utf-8"), "local edit\n")
            subprocess.run(["bash", script, "hermes", "--force", "audit-router"], env=env, check=True, capture_output=True)
            self.assertNotEqual(marker.read_text(encoding="utf-8"), "local edit\n")

    def test_installer_claude_layout_is_flat(self):
        with tempfile.TemporaryDirectory() as d:
            env = {**os.environ, "CLAUDE_SKILLS_DIR": d}
            subprocess.run(
                ["bash", str(ROOT / "scripts" / "install_skills.sh"), "claude", "plain-style", "spec-interview"],
                env=env,
                check=True,
                capture_output=True,
            )
            self.assertEqual(sorted(os.listdir(d)), ["plain-style", "spec-interview"])
            self.assertTrue((Path(d) / "plain-style" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
