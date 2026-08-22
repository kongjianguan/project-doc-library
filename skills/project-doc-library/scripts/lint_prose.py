#!/usr/bin/env python3
"""Find exact duplicate prose paragraphs in active project documentation."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from template_integrity import load_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find exact duplicate prose paragraphs.")
    parser.add_argument("--root", type=Path, help="repository root")
    parser.add_argument("--skill-root", type=Path, help="Skill root")
    return parser.parse_args()


def protected_files() -> set[str]:
    manifest = load_manifest()
    return set(dict(manifest["protected"]).keys())


def prose_blocks(path: Path) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    start = 0
    current: list[str] = []

    def flush() -> None:
        nonlocal current, start
        text = " ".join(line.strip() for line in current).strip()
        current = []
        if not text or in_fence:
            return
        if text.startswith(("#", "|", "- ", "* ", "> ", "<!--")):
            return
        if len(text) < 40:
            return
        blocks.append((start, re.sub(r"\s+", " ", text)))

    for number, line in enumerate(lines, start=1):
        if line.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if not line.strip():
            flush()
            continue
        if not current:
            start = number
        current.append(line)
    flush()
    return blocks


def main() -> int:
    args = parse_args()
    if args.root is None and args.skill_root is None:
        print("error: provide --root or --skill-root", file=sys.stderr)
        return 2

    errors: list[str] = []
    if args.root is not None:
        root = args.root.expanduser().resolve()
        if not root.is_dir():
            print(f"error: repository root is not a directory: {root}", file=sys.stderr)
            return 2
        protected = protected_files()
        paths: list[tuple[Path, str]] = []
        for base in (root / ".agents/notes", root / "docs"):
            if not base.is_dir():
                continue
            for path in sorted(base.rglob("*.md")):
                relative = path.relative_to(root).as_posix()
                if path.is_symlink() or relative in protected or "archived" in path.relative_to(base).parts:
                    continue
                paths.append((path, relative))
    else:
        skill_root = args.skill_root.expanduser().resolve()
        if not skill_root.is_dir():
            print(f"error: Skill root is not a directory: {skill_root}", file=sys.stderr)
            return 2
        paths = [(skill_root / "SKILL.md", "SKILL.md")]
        paths.extend((path, str(path.relative_to(skill_root))) for path in sorted((skill_root / "references").glob("*.md")))

    for path, label in paths:
        locations: dict[str, list[int]] = defaultdict(list)
        for line, block in prose_blocks(path):
            locations[block].append(line)
        for block, lines in locations.items():
            if len(lines) > 1:
                errors.append(f"duplicate prose in {label} at lines {', '.join(map(str, lines))}: {block}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"Prose lint failed with {len(errors)} duplicate(s).", file=sys.stderr)
        return 1
    print("No exact duplicate prose paragraphs found in active project docs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
