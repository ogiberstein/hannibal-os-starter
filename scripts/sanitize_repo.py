#!/usr/bin/env python3
"""Public-safety sanitation scan for Hannibal OS Starter."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SECRET_KEY_WORDS = (
    "api[_-]?key",
    "access[_-]?token",
    "auth[_-]?token",
    "bot[_-]?token",
    "client[_-]?secret",
    "password",
    "passwd",
    "private[_-]?key",
    "secret",
    "token",
)
SECRET_KEY_PATTERN = "|".join(SECRET_KEY_WORDS)
SECRET_VALUE_PATTERN = r"(?:['\"][^'\"]{8,}['\"]|[^\s#'\"]{8,})"

SECRET_PATTERNS = {
    "secret_assignment": re.compile(
        rf"(?i)(?:^|[^A-Z0-9_])['\"]?(?:[A-Z0-9_.-]*?(?:{SECRET_KEY_PATTERN})[A-Z0-9_.-]*?)['\"]?\s*[:=]\s*{SECRET_VALUE_PATTERN}"
    ),
    "private_key_header": re.compile("BEGIN " + r"[A-Z ]*PRIVATE KEY"),
    "slack_like_id": re.compile(r"\b[CDGUTW][0-9][A-Z0-9]{8,}\b"),
    "long_numeric_platform_id": re.compile(r"\b[0-9]{17,20}\b"),
    "telegram_chat_id": re.compile(r"(?<!\d)-100[0-9]{8,}\b"),
    "phone_like": re.compile(r"\+[0-9][0-9 .()\-]{8,}[0-9]"),
}

SAFE_VALUE_FRAGMENTS = {
    "SET_LOCALLY_ONLY",
    "REPLACE_ME",
    "PLACEHOLDER",
    "_HERE",
    "YOUR_",
    "***",
    "PINNED_RUNTIME_VERSION_HERE",
    "present",
    "missing",
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
    "/" + "root" + "/",
    "~/" + ".hermes",
    "BEGIN " + "PRIVATE KEY",
]

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
TEXT_EXTS = {
    "",
    ".cfg",
    ".conf",
    ".env",
    ".example",
    ".gitignore",
    ".ini",
    ".json",
    ".key",
    ".md",
    ".pem",
    ".sample",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_NAMES = {"LICENSE", "README.md", "CONTRIBUTING.md", "SECURITY.md"}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def is_text_file(path: Path) -> bool:
    return path.suffix in TEXT_EXTS or path.name in TEXT_NAMES


def is_allowed_secret_match(snippet: str) -> bool:
    return any(fragment in snippet for fragment in SAFE_VALUE_FRAGMENTS)


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
                snippet = match.group(0)
                if is_allowed_secret_match(snippet):
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
