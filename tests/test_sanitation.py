import tempfile
import unittest
from pathlib import Path

from scripts.sanitize_repo import scan


class SanitationTests(unittest.TestCase):
    def test_rejects_quoted_secret_assignment(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            secret_line = "TO" + "KEN='" + "super-secret-value" + "'\n"
            (root / "README.md").write_text(secret_line, encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("secret_assignment" in f for f in findings))

    def test_rejects_unquoted_env_secret_assignment(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            key = "MESSAGING_" + "BOT_TOKEN"
            value = "xoxb-real-looking-value"
            (root / "settings.env").write_text(f"{key}={value}\n", encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("secret_assignment" in f for f in findings))

    def test_rejects_json_secret_assignment(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            key = "api" + "_key"
            value = "real-looking-json-value"
            (root / "settings.json").write_text(f'{{"{key}": "{value}"}}\n', encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("secret_assignment" in f for f in findings))

    def test_allows_placeholders(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "env.example").write_text("MODEL_API_KEY=SET_LOCALLY_ONLY\n", encoding="utf-8")
            findings = scan(root)
        self.assertEqual(findings, [])

    def test_rejects_long_numeric_platform_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            raw_id = "123456789" + "012345678"
            (root / "route.yaml").write_text(f"target: {raw_id}\n", encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("long_numeric_platform_id" in f for f in findings))

    def test_rejects_slack_like_non_channel_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            raw_id = "U" + "012ABCDEF1"
            (root / "route.yaml").write_text(f"target: {raw_id}\n", encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("slack_like_id" in f for f in findings))

    def test_rejects_telegram_chat_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            raw_id = "-100" + "1234567890"
            (root / "route.yaml").write_text(f"target: {raw_id}\n", encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("telegram_chat_id" in f for f in findings))

    def test_rejects_openssh_private_key_header(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            header = "-----BEGIN " + "OPENSSH PRIVATE KEY-----\n"
            (root / "key.pem").write_text(header, encoding="utf-8")
            findings = scan(root)
        self.assertTrue(any("private_key_header" in f for f in findings))


if __name__ == "__main__":
    unittest.main()
