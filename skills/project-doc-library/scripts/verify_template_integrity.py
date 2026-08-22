#!/usr/bin/env python3
"""Verify protected generic templates before using the Skill."""

from __future__ import annotations

import sys
from pathlib import Path

from template_integrity import check_template_integrity, load_manifest, manifest_paths, sha256


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    manifest = load_manifest()
    protected, _ = manifest_paths(manifest)
    template_root = skill_root / "assets/templates"
    errors = check_template_integrity(skill_root)
    for relative in protected:
        path = template_root / relative
        if path.is_file():
            print(f"PROTECTED {relative} {sha256(path)}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("Protected generic templates are intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
