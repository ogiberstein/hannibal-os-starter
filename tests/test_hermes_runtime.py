import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "hermes-runtime.sh"


def fake_runtime(root: Path, tag: str) -> Path:
    """A stand-in runtime: venv/bin/python plus a `hermes` entry point and a `gateway` package."""
    d = root / tag / "hermes-agent"
    (d / "venv" / "bin").mkdir(parents=True)
    (d / "venv" / "bin" / "python").symlink_to(os.path.realpath(sys.executable))
    (d / "hermes").write_text(f"print('Hermes Agent {tag}')\n", encoding="utf-8")
    (d / "gateway").mkdir()
    (d / "gateway" / "__init__.py").write_text("", encoding="utf-8")
    (d / "gateway" / "run.py").write_text("", encoding="utf-8")
    return d


class HermesRuntimeScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "runtimes"
        self.live = base / "live"
        self.restarts = base / "restarts.log"
        self.old = fake_runtime(self.root, "v1.0.0")
        self.new = fake_runtime(self.root, "v1.1.0")
        self.live.symlink_to(self.old)
        self.env = {
            **os.environ,
            "HERMES_RUNTIME_ROOT": str(self.root),
            "HERMES_LIVE_LINK": str(self.live),
            "HERMES_RESTART_CMD": f"echo restart >> {self.restarts}",
            "HERMES_HEALTH_CMD": "true",
        }

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, *args, check=True):
        return subprocess.run(
            ["bash", str(SCRIPT), *args], env=self.env, text=True, capture_output=True, check=check
        )

    def test_bash_syntax(self):
        subprocess.run(["bash", "-n", str(SCRIPT)], check=True)

    def test_dry_run_changes_nothing(self):
        out = self.run_script("switch", "v1.1.0", "--dry-run").stdout
        self.assertIn("dry run", out)
        self.assertEqual(os.path.realpath(self.live), str(self.old))
        self.assertFalse((self.root / "previous").exists())

    def test_switch_then_rollback(self):
        self.run_script("switch", "v1.1.0")
        self.assertEqual(os.path.realpath(self.live), str(self.new))
        self.assertEqual(os.path.realpath(self.root / "previous"), str(self.old))
        self.run_script("rollback")
        self.assertEqual(os.path.realpath(self.live), str(self.old))
        self.assertEqual(os.path.realpath(self.root / "previous"), str(self.new))
        self.assertEqual(self.restarts.read_text().count("restart"), 2)

    def test_refuses_switch_to_live_or_missing_runtime(self):
        self.assertNotEqual(self.run_script("switch", "v1.0.0", check=False).returncode, 0)
        self.assertNotEqual(self.run_script("switch", "v9.9.9", check=False).returncode, 0)
        self.assertNotEqual(self.run_script("rollback", check=False).returncode, 0)

    def test_refuses_when_live_link_missing_or_not_a_symlink(self):
        self.live.unlink()
        result = self.run_script("switch", "v1.1.0", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("one-time setup", result.stderr)
        self.assertFalse(self.live.exists())
        self.assertFalse((self.root / "previous").exists())
        self.live.mkdir()
        result = self.run_script("switch", "v1.1.0", check=False)
        self.assertIn("not a symlink", result.stderr)
        self.assertFalse((self.root / "previous").exists())
        self.assertFalse(self.restarts.exists())

    def test_unhealthy_switch_fails_loudly(self):
        self.env["HERMES_HEALTH_CMD"] = "false"
        self.env["HERMES_HEALTH_WAIT_S"] = "0"
        result = self.run_script("switch", "v1.1.0", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rollback", result.stderr)

    def test_status_lists_runtimes(self):
        out = self.run_script("status").stdout
        self.assertIn("v1.0.0", out)
        self.assertIn("v1.1.0", out)


if __name__ == "__main__":
    unittest.main()
