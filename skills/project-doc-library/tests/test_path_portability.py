#!/usr/bin/env python3
"""Regression tests for path values that cross the JSON/Markdown boundary."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path, PureWindowsPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from template_integrity import manifest_key


class PathPortabilityTests(unittest.TestCase):
    def test_manifest_keys_use_forward_slashes_on_windows(self) -> None:
        windows_path = PureWindowsPath(".agents", "notes", "README.md")

        self.assertEqual(manifest_key(windows_path), ".agents/notes/README.md")

    def test_native_relative_paths_are_manifest_compatible(self) -> None:
        native_path = Path("docs") / "i18n" / "translation-rules.md"

        self.assertEqual(manifest_key(native_path), "docs/i18n/translation-rules.md")


if __name__ == "__main__":
    unittest.main()
