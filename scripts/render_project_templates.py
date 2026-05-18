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


def render_files(output: Path, project: str, *, dry_run: bool, force: bool) -> list[Path]:
    replacements = {
        "CURRENT_FOCUS_HERE": f"Set up {project}",
        "PRIMARY_USER_OR_TEAM_HERE": project,
        "PROJECT_SCOPE_HERE": f"Private agent operating-system starter for {project}",
        "FACT_HERE": f"Project name: {project}",
    }
    planned = sorted(TEMPLATE_DIR.glob("*.md"))
    targets = [output / src.name for src in planned]
    existing = [target for target in targets if target.exists()]
    if existing and not force:
        names = ", ".join(str(path) for path in existing)
        raise FileExistsError(f"refusing to overwrite existing files without --force: {names}")
    if dry_run:
        return targets
    output.mkdir(parents=True, exist_ok=True)
    for src, target in zip(planned, targets):
        text = src.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        target.write_text(text, encoding="utf-8")
    return targets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--dry-run", action="store_true", help="show files that would be rendered without writing")
    parser.add_argument("--force", action="store_true", help="allow overwriting existing project docs")
    args = parser.parse_args()
    output = Path(args.output).resolve()
    project = safe_value(args.project)
    targets = render_files(output, project, dry_run=args.dry_run, force=args.force)
    action = "Would render" if args.dry_run else "Rendered"
    for target in targets:
        print(f"{action}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
