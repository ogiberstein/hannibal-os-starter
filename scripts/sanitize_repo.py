#!/usr/bin/env python3
"""Public-safety sanitation scan for Hannibal OS Starter."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SECRET_PATTERNS = {
    "secret_assignment": re.compile(r"(?i)(api[_-]?key|secret|password|token|passwd)\s*=\s*['\"][^'\"]{6,}['\"]"),
    "private_key": re.compile(r"BEGIN (RSA|OPENSSH|PRIVATE) KEY"),
    "slack_channel_id": re.compile(r"\bC0[A-Z0-9]{8,}\b"),
    "long_numeric_platform_id": re.compile(r"\b[0-9]{17,20}\b"),
}

FORBIDDEN_PATH_PARTS = {
    ".env",
    "sessions",
    "memories",
    "memory",
    "logs",
    "backups",
    "cron",
    ".cache",
}

FORBIDDEN_TEXT = [
    "En" + "scribe",
    "ogi" + "berstein",
    "/" + "root" + "/",
    "~/" + ".hermes",
    "BEGIN " + "PRIVATE KEY",
]

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
TEXT_EXTS = {".md", ".py", ".yml", ".yaml", ".txt", ".example", ".gitignore", ""}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def is_text_file(path: Path) -> bool:
    return path.suffix in TEXT_EXTS or path.name in {"LICENSE", "README.md", "CONTRIBUTING.md", "SECURITY.md"}


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_files(root):
        rel = path.relative_to(root)
        parts = set(rel.parts)
        bad_parts = sorted(parts & FORBIDDEN_PATH_PARTS)
        if bad_parts and path.name != "env.example":
            findings.append(f"forbidden path component {bad_parts}: {rel}")
        if not is_text_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"non-utf8 text-like file: {rel}")
            continue
        for name, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                # Allow placeholder env/example values that are intentionally non-secret.
                snippet = match.group(0)
                if "SET_LOCALLY_ONLY" in snippet:
                    continue
                findings.append(f"{name}: {rel}: {snippet[:80]}")
        for marker in FORBIDDEN_TEXT:
            if marker in text:
                findings.append(f"forbidden marker {marker!r}: {rel}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".", help="repository path to scan")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    findings = scan(root)
    if findings:
        print("Sanitation failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Sanitation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
