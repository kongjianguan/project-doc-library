# Codex Skills

Reusable Codex skills maintained as independent packages.

## Available Skills

- [project-doc-library](skills/project-doc-library/SKILL.md): bootstrap and maintain a repository-local documentation system modeled on DeepSeek Harness.

## Repository Layout

Each directory under `skills/` is one self-contained Skill package. Its `SKILL.md` is the entrypoint; `agents/`, `references/`, `scripts/`, and `assets/` are package resources.

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
├── references/
├── scripts/
└── assets/
```

