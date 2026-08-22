#!/usr/bin/env python3
"""Check the mechanical contracts of a project documentation library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path


LIFECYCLES = ("proposed", "implemented", "rejected", "archived")
CLASSES = ("feature", "bug-fix", "simplification", "architecture", "process", "testing")
REQUIRED_NOTE_HEADINGS = {
    "proposed": ("Problem", "Proposal", "Alternatives considered", "Acceptance criteria", "Risks"),
    "implemented": ("Problem", "Decision", "Alternatives considered", "Consequences"),
}
FORBIDDEN_IMPLEMENTED_HEADINGS = ("Proposal", "Plan", "Migration plan", "Acceptance criteria")
NOTE_FILENAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
TEMPLATE_CONTRACT_FILES = frozenset(
    {
        ".agents/notes/AGENTS.md",
        ".agents/notes/README.md",
        ".agents/notes/README.zh.md",
        ".agents/notes/archived/AGENTS.md",
        ".agents/notes/implemented/AGENTS.md",
        "docs/AGENTS.md",
        "docs/i18n/README.md",
        "docs/i18n/README.zh.md",
        "docs/i18n/style-samples.md",
        "docs/i18n/translation-prompt.md",
        "docs/i18n/translation-rules.md",
        "docs/i18n/translation-rules.zh.md",
        "docs/postmortem/README.md",
        "docs/postmortem/README.zh.md",
    }
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a structured project documentation library.")
    parser.add_argument("--root", required=True, type=Path, help="repository root")
    return parser.parse_args()


def blob_hash(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class Checker:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.errors: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def require_file(self, relative: Path) -> None:
        path = self.root / relative
        if not path.is_file():
            self.error(f"missing file: {relative}")

    def require_directory(self, relative: Path) -> None:
        path = self.root / relative
        if not path.is_dir():
            self.error(f"missing directory: {relative}")

    def check_required_structure(self, bilingual: bool) -> None:
        for relative in (
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
        ):
            self.require_directory(relative)

        for lifecycle in LIFECYCLES:
            for decision_class in CLASSES:
                self.require_directory(Path(".agents/notes") / lifecycle / decision_class)

        for relative in (
            Path(".agents/notes/README.md"),
            Path(".agents/notes/AGENTS.md"),
            Path(".agents/notes/implemented/AGENTS.md"),
            Path(".agents/notes/archived/AGENTS.md"),
            Path(".agents/notes/archived/manifest.json"),
            Path("docs/AGENTS.md"),
            Path("docs/postmortem/README.md"),
            Path("docs/subsystems/README.md"),
        ):
            self.require_file(relative)

        compatibility_link = self.root / ".agents/notes/implemented/CLAUDE.md"
        if not compatibility_link.is_symlink():
            self.error(".agents/notes/implemented/CLAUDE.md must be a symlink to AGENTS.md")
        elif os.readlink(compatibility_link) != "AGENTS.md":
            self.error(".agents/notes/implemented/CLAUDE.md must point to AGENTS.md")

        if bilingual:
            self.require_directory(Path("docs/i18n"))
            for relative in (
                Path(".agents/notes/README.zh.md"),
                Path("docs/i18n/README.md"),
                Path("docs/i18n/README.zh.md"),
                Path("docs/i18n/translation-rules.md"),
                Path("docs/i18n/translation-rules.zh.md"),
                Path("docs/i18n/terminology.md"),
                Path("docs/i18n/style-samples.md"),
                Path("docs/i18n/translation-prompt.md"),
                Path("docs/postmortem/README.zh.md"),
                Path("docs/subsystems/README.zh.md"),
            ):
                self.require_file(relative)

    def check_lifecycle_directories(self) -> None:
        notes_root = self.root / ".agents/notes"
        if not notes_root.is_dir():
            return
        allowed = set(LIFECYCLES) | {"README.md", "README.zh.md", "README.i18n.yaml", "AGENTS.md"}
        for child in notes_root.iterdir():
            if child.name not in allowed:
                self.error(f"unexpected entry under .agents/notes: {child.name}")
        for lifecycle in LIFECYCLES:
            lifecycle_path = notes_root / lifecycle
            if not lifecycle_path.is_dir():
                continue
            for child in lifecycle_path.iterdir():
                allowed_children = set(CLASSES) | {"AGENTS.md", "CLAUDE.md"}
                if lifecycle == "archived":
                    allowed_children.add("manifest.json")
                if child.name not in allowed_children:
                    self.error(f"unexpected entry under .agents/notes/{lifecycle}: {child.name}")

    def check_archive_manifest(self) -> None:
        archive_root = self.root / ".agents/notes/archived"
        manifest_path = archive_root / "manifest.json"
        if not manifest_path.is_file():
            return
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            self.error(f"invalid archive manifest: {error}")
            return
        if manifest.get("version") != 1 or not isinstance(manifest.get("files"), dict):
            self.error("archive manifest must contain version: 1 and a files map")
            return

        expected: set[str] = set()
        for path in archive_root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(archive_root)
            if relative.as_posix() in {"AGENTS.md", "manifest.json"}:
                continue
            expected.add(relative.as_posix())

        recorded = set(manifest["files"])
        for missing in sorted(expected - recorded):
            self.error(f"archived artifact is missing from manifest: {missing}")
        for extra in sorted(recorded - expected):
            self.error(f"archive manifest lists missing artifact: {extra}")

        for name, recorded_hash in manifest["files"].items():
            if Path(name).is_absolute() or ".." in Path(name).parts:
                self.error(f"archive manifest contains unsafe path: {name}")
                continue
            target = archive_root / name
            if not target.is_file():
                continue
            if not isinstance(recorded_hash, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", recorded_hash):
                self.error(f"archive manifest has invalid hash for {name}")
                continue
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if recorded_hash != f"sha256:{digest}":
                self.error(f"archived artifact hash is stale: {name}")

    def check_note(self, path: Path, lifecycle: str, decision_class: str) -> None:
        relative = path.relative_to(self.root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self.error(f"note is not UTF-8: {relative}")
            return
        lines = text.splitlines()
        if not NOTE_FILENAME.fullmatch(path.name):
            self.error(f"note filename must be yyyy-mm-dd-topic-title.md: {relative}")
        if len(lines) < 3 or not lines[0].startswith("# Agent Note: ") or lines[1] != "":
            self.error(f"note must start with the exact Agent Note header block: {relative}")
        if len(lines) < 3 or not lines[2].startswith("Status: "):
            self.error(f"note is missing the Status: header line: {relative}")

        status_match = re.search(r"^Status:\s*(.+)$", text, flags=re.MULTILINE)
        if not status_match:
            self.error(f"note is missing Status: {relative}")
        else:
            status = status_match.group(1).strip()
            if lifecycle == "proposed" and status != "proposed":
                self.error(f"proposed note has status {status!r}: {relative}")
            elif lifecycle == "implemented" and status != "implemented":
                self.error(f"implemented note has status {status!r}: {relative}")
            elif lifecycle == "rejected" and not re.fullmatch(r"rejected\s+(?:-|—)\s+.+", status):
                self.error(f"rejected note must include a reason in Status: {relative}")
            elif lifecycle == "archived" and status != "implemented":
                self.error(f"archived note must retain Status: implemented: {relative}")

        skeleton = "implemented" if lifecycle == "archived" else ("proposed" if lifecycle == "rejected" else lifecycle)
        required = REQUIRED_NOTE_HEADINGS.get(skeleton, ())
        headings = set(re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
        for heading in required:
            if heading not in headings:
                self.error(f"note is missing '## {heading}': {relative}")

        if lifecycle == "implemented" and any(heading in headings for heading in FORBIDDEN_IMPLEMENTED_HEADINGS):
            self.error(f"implemented note retains proposal headings: {relative}")

        if lifecycle == "archived":
            if len(lines) < 4 or not re.fullmatch(r"Archived:\s*\d{4}-\d{2}-\d{2}", lines[3]):
                self.error(f"archived note is missing Archived: YYYY-MM-DD: {relative}")

    def check_notes(self) -> None:
        notes_root = self.root / ".agents/notes"
        for lifecycle in LIFECYCLES:
            for decision_class in CLASSES:
                directory = notes_root / lifecycle / decision_class
                if not directory.is_dir():
                    continue
                for path in sorted(directory.rglob("*.md")):
                    if path.name.endswith(".zh.md"):
                        continue
                    self.check_note(path, lifecycle, decision_class)

    def check_pairs(self, bilingual: bool) -> None:
        if not bilingual:
            return
        candidates: list[Path] = []
        for base in (self.root / ".agents/notes", self.root / "docs"):
            if not base.is_dir():
                continue
            for path in sorted(base.rglob("*.md")):
                if path.name.endswith(".zh.md") or path.name in {"AGENTS.md", "CLAUDE.md"}:
                    continue
                if base.name == "notes" and "archived" in path.relative_to(base).parts:
                    continue
                if base.name == "docs":
                    relative_docs = path.relative_to(base)
                    if relative_docs.parts[:1] == ("i18n",) and relative_docs.name in {
                        "terminology.md",
                        "style-samples.md",
                        "translation-prompt.md",
                    }:
                        continue
                candidates.append(path)

        for english in candidates:
            chinese = english.with_name(f"{english.stem}.zh.md")
            sidecar = english.with_name(f"{english.stem}.i18n.yaml")
            relative = english.relative_to(self.root)
            if not chinese.is_file():
                self.error(f"missing Chinese pair for {relative}")
                continue
            if not sidecar.is_file():
                self.error(f"missing i18n sidecar for {relative}")
                continue
            values: dict[str, str] = {}
            for line in sidecar.read_text(encoding="utf-8").splitlines():
                match = re.fullmatch(r"([^:]+):\s*(\S+)", line.strip())
                if match:
                    values[match.group(1)] = match.group(2)
            if values.get(english.name) != blob_hash(english):
                self.error(f"English blob hash is stale: {sidecar.relative_to(self.root)}")
            if values.get(chinese.name) != blob_hash(chinese):
                self.error(f"Chinese blob hash is stale: {sidecar.relative_to(self.root)}")
            self.check_language_switchers(english, chinese)
            self.check_structure_signature(english, chinese)

    def check_language_switchers(self, english: Path, chinese: Path) -> None:
        english_text = english.read_text(encoding="utf-8")
        chinese_text = chinese.read_text(encoding="utf-8")
        if f"[中文]({chinese.name})" not in english_text:
            self.error(f"English document is missing its Chinese switcher: {english.relative_to(self.root)}")
        if f"[English]({english.name})" not in chinese_text:
            self.error(f"Chinese document is missing its English switcher: {chinese.relative_to(self.root)}")

    def check_structure_signature(self, english: Path, chinese: Path) -> None:
        def signature(path: Path) -> list[str]:
            result: list[str] = []
            in_fence = False
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("```"):
                    result.append("fence")
                    in_fence = not in_fence
                elif not in_fence and re.match(r"^#{1,6}\s+", line):
                    result.append(f"heading:{len(line) - len(line.lstrip('#'))}")
            return result

        if signature(english) != signature(chinese):
            self.error(f"English/Chinese structure differs: {english.relative_to(self.root)}")

    def check_links(self) -> None:
        link_pattern = re.compile(r"\]\(([^)]+)\)")
        for base in (self.root / ".agents/notes", self.root / "docs"):
            if not base.is_dir():
                continue
            for path in sorted(base.rglob("*.md")):
                if base.name == "notes" and "archived" in path.relative_to(base).parts:
                    continue
                if path.is_symlink():
                    # Compatibility links are checked by the structure pass;
                    # do not validate the target's links a second time from
                    # the symlink's directory.
                    continue
                if path.relative_to(self.root).as_posix() in TEMPLATE_CONTRACT_FILES:
                    # Generic contract templates may link to optional records
                    # or repository checks that a smaller project does not carry.
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                for target in link_pattern.findall(text):
                    target = target.strip().split("#", 1)[0].split("?", 1)[0]
                    if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                        continue
                    if target.startswith("/"):
                        resolved = self.root / target.lstrip("/")
                    else:
                        resolved = (path.parent / target).resolve()
                    if not resolved.is_file() and not resolved.is_dir():
                        self.error(f"broken relative link in {path.relative_to(self.root)}: {target}")

    def run(self) -> int:
        bilingual = (self.root / ".agents/notes/README.zh.md").is_file()
        self.check_required_structure(bilingual)
        self.check_lifecycle_directories()
        self.check_archive_manifest()
        self.check_notes()
        self.check_pairs(bilingual)
        self.check_links()
        if self.errors:
            for error in self.errors:
                print(f"error: {error}", file=sys.stderr)
            print(f"Documentation verification failed with {len(self.errors)} error(s).", file=sys.stderr)
            return 1
        mode = "bilingual" if bilingual else "English-only"
        print(f"Documentation structure is valid ({mode}).")
        return 0


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"error: repository root is not a directory: {root}", file=sys.stderr)
        return 2
    return Checker(root).run()


if __name__ == "__main__":
    raise SystemExit(main())
