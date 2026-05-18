#!/usr/bin/env python3
"""Single local/CI verification entrypoint."""
from __future__ import annotations

import pathlib
import py_compile
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def check_python_compile() -> None:
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        py_compile.compile(str(path), doraise=True)
    print("python compile passed")


def check_whitespace() -> None:
    bad: list[str] = []
    for path in ROOT.rglob("*"):
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts) or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                bad.append(f"{path.relative_to(ROOT)}:{i}: trailing whitespace")
        if text and not text.endswith("\n"):
            bad.append(f"{path.relative_to(ROOT)}: missing final newline")
    if bad:
        print("Whitespace check failed:")
        print("\n".join(bad))
        raise SystemExit(1)
    print("whitespace passed")


def main() -> int:
    check_python_compile()
    check_whitespace()
    run([sys.executable, "scripts/sanitize_repo.py", "--path", "."])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    print("verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
