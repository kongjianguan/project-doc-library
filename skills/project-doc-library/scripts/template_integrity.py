#!/usr/bin/env python3
"""Shared template manifest and integrity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "references/template-manifest.json"


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_paths(manifest: dict[str, object]) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    canonical = tuple(Path(path) for path in dict(manifest["canonical"]).keys())
    adapted = tuple(Path(path) for path in list(manifest["adapted"]))
    return canonical, adapted


def check_template_integrity(skill_root: Path) -> list[str]:
    manifest = load_manifest()
    template_root = skill_root.resolve() / "assets/templates"
    canonical, adapted = manifest_paths(manifest)
    expected = set(canonical) | set(adapted)
    actual = {
        path.relative_to(template_root)
        for path in template_root.rglob("*")
        if path.is_file()
    }

    errors: list[str] = []
    for extra in sorted(actual - expected):
        errors.append(f"unclassified template: {extra}")
    for missing in sorted(expected - actual):
        errors.append(f"missing template: {missing}")

    expected_hashes = dict(manifest["canonical"])
    for relative in canonical:
        path = template_root / relative
        if not path.is_file():
            continue
        actual_hash = sha256(path)
        expected_hash = expected_hashes[str(relative)]
        if actual_hash != expected_hash:
            errors.append(f"canonical template hash differs from manifest: {relative}")
    return errors
