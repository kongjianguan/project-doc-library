#!/usr/bin/env python3
"""Refresh active English/Chinese documentation sidecars after semantic review."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


EXCLUDED_I18N_FILES = {"terminology.md", "style-samples.md", "translation-prompt.md"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh active documentation i18n sidecars.")
    parser.add_argument("--root", required=True, type=Path, help="repository root")
    parser.add_argument(
        "--write",
        action="store_true",
        help="write current blob hashes; without this flag only report differences",
    )
    return parser.parse_args()


def blob_hash(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def is_excluded(base: Path, path: Path) -> bool:
    relative = path.relative_to(base)
    if path.name.endswith(".zh.md") or path.name in {"AGENTS.md", "CLAUDE.md"}:
        return True
    if base.name == "notes" and "archived" in relative.parts:
        return True
    return base.name == "docs" and relative.parts[:1] == ("i18n",) and path.name in EXCLUDED_I18N_FILES


def candidates(root: Path) -> list[tuple[Path, Path, Path]]:
    pairs: list[tuple[Path, Path, Path]] = []
    for base in (root / ".agents/notes", root / "docs"):
        if not base.is_dir():
            continue
        for english in sorted(base.rglob("*.md")):
            if is_excluded(base, english):
                continue
            chinese = english.with_name(f"{english.stem}.zh.md")
            if not chinese.is_file():
                continue
            sidecar = english.with_name(f"{english.stem}.i18n.yaml")
            pairs.append((english, chinese, sidecar))
    return pairs


def sidecar_content(english: Path, chinese: Path) -> str:
    return (
        f"{english.name}: {blob_hash(english)}\n"
        f"{chinese.name}: {blob_hash(chinese)}\n"
    )


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"error: repository root is not a directory: {root}", file=sys.stderr)
        return 2

    changed = 0
    stale = 0
    for english, chinese, sidecar in candidates(root):
        expected = sidecar_content(english, chinese)
        current = sidecar.read_text(encoding="utf-8") if sidecar.is_file() else None
        relative = sidecar.relative_to(root)
        if current == expected:
            print(f"ok: {relative}")
            continue
        stale += 1
        if args.write:
            with sidecar.open("w", encoding="utf-8", newline="\n") as stream:
                stream.write(expected)
            changed += 1
            print(f"updated: {relative}")
        else:
            print(f"stale: {relative}")

    if args.write:
        print(f"Updated {changed} sidecar(s).")
        return 0
    if stale:
        print(f"{stale} sidecar(s) require refresh.", file=sys.stderr)
        return 1
    print("All active i18n sidecars are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
