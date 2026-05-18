#!/usr/bin/env python3
"""Render project templates into a target directory with simple placeholder replacement."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates" / "project"


def safe_value(value: str) -> str:
    if any(ch in value for ch in "\n\r"):
        raise ValueError("values must be single-line")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--project", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    project = safe_value(args.project)
    output.mkdir(parents=True, exist_ok=True)
    replacements = {
        "CURRENT_FOCUS_HERE": f"Set up {project}",
        "PRIMARY_USER_OR_TEAM_HERE": project,
        "PROJECT_SCOPE_HERE": f"Private agent operating-system starter for {project}",
        "FACT_HERE": f"Project name: {project}",
    }
    for src in TEMPLATE_DIR.glob("*.md"):
        text = src.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        (output / src.name).write_text(text, encoding="utf-8")
    print(f"Rendered project templates to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
