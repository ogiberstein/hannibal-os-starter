import tempfile
import unittest
from pathlib import Path

from scripts.sanitize_repo import scan


class SanitationTests(unittest.TestCase):
    def test_rejects_secret_assignment(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            secret_line = "TO" + "KEN='" + "super-secret-value" + "'\n"
            (root / "README.md").write_text(secret_line, encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("secret_assignment" in f for f in findings))

    def test_allows_placeholders(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "env.example").write_text("MODEL_API_KEY=SET_LOCALLY_ONLY\n", encoding="utf-8")
            findings = scan(root)
        self.assertEqual(findings, [])

    def test_rejects_raw_platform_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            raw_id = "123456789" + "012345678"
            (root / "route.yaml").write_text(f"target: {raw_id}\n", encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("long_numeric_platform_id" in f for f in findings))


if __name__ == "__main__":
    unittest.main()
