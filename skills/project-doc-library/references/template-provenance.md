# Template Provenance

The Skill is derived from the documentation conventions in DeepSeek Harness, but its target-facing templates are normalized so they do not carry that project's product inventory, paths, commands, terminology, or history.

## Protected protocol templates

These files preserve the reusable protocol: document ownership, Agent Note lifecycle, archive semantics, bilingual pairing, translation quality, prose style, and postmortem boundaries.

- `.agents/notes/AGENTS.md`
- `.agents/notes/README.md`
- `.agents/notes/README.zh.md`
- `.agents/notes/archived/AGENTS.md`
- `.agents/notes/implemented/AGENTS.md`
- `docs/AGENTS.md`
- `docs/i18n/README.md`
- `docs/i18n/README.zh.md`
- `docs/i18n/style-samples.md`
- `docs/i18n/translation-prompt.md`
- `docs/i18n/translation-rules.md`
- `docs/i18n/translation-rules.zh.md`
- `docs/postmortem/README.md`
- `docs/postmortem/README.zh.md`

These files are protected by SHA-256 hashes in [template-manifest.json](template-manifest.json). The hashes protect the Skill's reviewed protocol text; they do not claim byte identity with the source repository.

## Target-adapted templates

These files provide shape and placeholders but must be populated from the target repository:

- `.agents/notes/archived/manifest.json` starts empty and records the target's sealed artifacts.
- `docs/i18n/terminology.md` records the target's actual translation decisions.
- `docs/subsystems/README.md` and `.zh.md` index the target's real subsystem pages.

Do not copy source-project names, subsystem inventories, commands, package paths, API catalogs, incident titles, dates, or historical references into a target. Replace every such fact with a target-repository observation or leave the section empty until one exists.

## Source and audit

The source material used for distillation is pinned in the manifest for traceability. A local source checkout may be used to review provenance, compare rule coverage, or investigate a future update; it must never be used as a copy source for target-facing files.

Run the policy audit from the Skill repository:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/audit_template_policy.py \
  --skill-root /absolute/path/to/project-doc-library/skills/project-doc-library
```

The audit fails when a template is unclassified, missing, has a stale protected hash, or contains a forbidden source-project token. It reports protected and adapted hashes separately so a reviewer can see which files are contracts and which files require target population.

To check only the protected copy, run:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/verify_template_integrity.py
```
