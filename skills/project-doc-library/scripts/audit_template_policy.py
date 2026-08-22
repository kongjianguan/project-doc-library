#!/usr/bin/env python3
"""Audit template classification, hashes, and source-project contamination."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from template_integrity import check_template_integrity, load_manifest, manifest_paths, sha256


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit project-doc-library templates for integrity and project-neutrality."
    )
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="project-doc-library skill root",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = args.skill_root.expanduser().resolve()
    template_root = skill_root / "assets/templates"
    manifest = load_manifest()
    protected, adapted = manifest_paths(manifest)
    errors = check_template_integrity(skill_root)

    for relative in protected:
        path = template_root / relative
        if path.is_file():
            print(f"PROTECTED {relative} {sha256(path)}")
    for relative in adapted:
        path = template_root / relative
        if path.is_file():
            print(f"ADAPTED   {relative} {sha256(path)}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Template policy audit passed: structure, protected hashes, and contamination scan are clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
