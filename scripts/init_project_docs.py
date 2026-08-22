#!/usr/bin/env python3
"""Create the project documentation structure without overwriting user files."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

from template_integrity import check_template_integrity


LIFECYCLES = ("proposed", "implemented", "rejected", "archived")
CLASSES = ("feature", "bug-fix", "simplification", "architecture", "process", "testing")

BASE_DIRECTORIES = (
    Path(".agents"),
    Path(".agents/notes"),
    Path(".agents/skills"),
    Path("docs"),
    Path("docs/postmortem"),
    Path("docs/subsystems"),
    Path("docs/cookbook"),
    Path("docs/user"),
    Path("docs/user/guide"),
    Path("docs/user/develop"),
    Path("docs/user/develop/basic"),
    Path("docs/user/develop/framework"),
    Path("docs/user/develop/practice"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a DSH-shaped project documentation library."
    )
    parser.add_argument("--root", required=True, type=Path, help="repository root")
    parser.add_argument(
        "--no-bilingual",
        action="store_true",
        help="omit translated templates and the docs/i18n contract",
    )
    return parser.parse_args()


def blob_hash(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def add_directory(path: Path, created: list[str]) -> None:
    if path.exists():
        if path.is_dir():
            return
        raise RuntimeError(f"path exists but is not a directory: {path}")
    path.mkdir(parents=True)
    created.append(str(path))


def copy_templates(
    root: Path, template_root: Path, bilingual: bool, created: list[str], skipped: list[str]
) -> None:
    for source in sorted(template_root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(template_root)
        if not bilingual and relative.parts[:2] == ("docs", "i18n"):
            skipped.append(str(relative))
            continue
        if not bilingual and (relative.name.endswith(".zh.md") or relative.name.endswith(".i18n.yaml")):
            skipped.append(str(relative))
            continue

        destination = root / relative
        if destination.exists() or destination.is_symlink():
            if destination.is_dir():
                raise RuntimeError(f"template target is a directory: {destination}")
            skipped.append(str(relative))
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        if not bilingual and relative.name == "README.md":
            lines = data.decode("utf-8").splitlines()
            lines = [line for line in lines if not line.startswith("English | [中文](")]
            data = ("\n".join(lines) + "\n").encode("utf-8")
        destination.write_bytes(data)
        created.append(str(relative))


def write_sidecars(root: Path, bilingual: bool, created: list[str], skipped: list[str]) -> None:
    if not bilingual:
        return

    pairs = (
        Path(".agents/notes/README.md"),
        Path("docs/i18n/README.md"),
        Path("docs/i18n/translation-rules.md"),
        Path("docs/postmortem/README.md"),
        Path("docs/subsystems/README.md"),
    )
    for relative_english in pairs:
        english = root / relative_english
        chinese = english.with_name(f"{english.stem}.zh.md")
        sidecar = english.with_name(f"{english.stem}.i18n.yaml")
        if not english.is_file() or not chinese.is_file():
            continue
        if sidecar.exists() or sidecar.is_symlink():
            skipped.append(str(sidecar.relative_to(root)))
            continue
        content = (
            f"{english.name}: {blob_hash(english)}\n"
            f"{chinese.name}: {blob_hash(chinese)}\n"
        )
        with sidecar.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        created.append(str(sidecar.relative_to(root)))


def create_lifecycle_tree(root: Path, created: list[str]) -> None:
    notes_root = root / ".agents/notes"
    for lifecycle in LIFECYCLES:
        for decision_class in CLASSES:
            add_directory(notes_root / lifecycle / decision_class, created)


def create_compatibility_link(root: Path, created: list[str], skipped: list[str]) -> None:
    link = root / ".agents/notes/implemented/CLAUDE.md"
    if link.exists() or link.is_symlink():
        skipped.append(str(link.relative_to(root)))
        return
    os.symlink("AGENTS.md", link)
    created.append(str(link.relative_to(root)))


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"error: repository root is not a directory: {root}", file=sys.stderr)
        return 2

    template_root = Path(__file__).resolve().parents[1] / "assets/templates"
    integrity_errors = check_template_integrity(template_root.parent.parent)
    if integrity_errors:
        for error in integrity_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    created: list[str] = []
    skipped: list[str] = []

    try:
        for relative in BASE_DIRECTORIES:
            if not args.no_bilingual or relative != Path("docs/i18n"):
                add_directory(root / relative, created)
        create_lifecycle_tree(root, created)
        copy_templates(root, template_root, not args.no_bilingual, created, skipped)
        create_compatibility_link(root, created, skipped)
        write_sidecars(root, not args.no_bilingual, created, skipped)
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    mode = "bilingual" if not args.no_bilingual else "English-only"
    print(f"Initialized {mode} project documentation structure at {root}")
    print(f"Created: {len(created)} paths")
    if skipped:
        print(f"Preserved: {len(skipped)} existing paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
