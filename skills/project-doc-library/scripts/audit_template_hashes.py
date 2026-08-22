#!/usr/bin/env python3
"""Compare documentation templates with a local DeepSeek Harness checkout."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from template_integrity import check_template_integrity, load_manifest, manifest_paths, sha256


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit project-doc-library templates against a local DSH checkout."
    )
    parser.add_argument("--dsh-root", required=True, type=Path, help="local DSH checkout")
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="project-doc-library skill root",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    template_root = args.skill_root.resolve() / "assets/templates"
    dsh_root = args.dsh_root.expanduser().resolve()
    manifest = load_manifest()
    canonical, adapted = manifest_paths(manifest)
    expected = set(canonical) | set(adapted)
    actual = {
        path.relative_to(template_root)
        for path in template_root.rglob("*")
        if path.is_file()
    }

    errors = check_template_integrity(args.skill_root)
    for extra in sorted(actual - expected):
        errors.append(f"unclassified template: {extra}")
    for missing in sorted(expected - actual):
        errors.append(f"missing template: {missing}")

    for relative in (*canonical, *adapted):
        template = template_root / relative
        dsh_file = dsh_root / relative
        if not template.is_file() or not dsh_file.is_file():
            continue
        template_hash = sha256(template)
        dsh_hash = sha256(dsh_file)
        kind = "canonical" if relative in canonical else "adapted"
        result = "MATCH" if template_hash == dsh_hash else "INTENTIONAL-DIFF"
        print(f"{kind:9} {result:16} {relative}")
        print(f"  skill {template_hash}")
        print(f"  dsh   {dsh_hash}")
        if relative in canonical and template_hash != dsh_hash:
            errors.append(f"canonical template differs from DSH: {relative}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("All canonical templates match the supplied DSH checkout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
