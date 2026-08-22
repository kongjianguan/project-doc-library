# Template Provenance

The Skill distills documentation conventions from DeepSeek Harness into a reusable protocol.

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

These files are protected by SHA-256 hashes in [template-manifest.json](template-manifest.json).

## Target-adapted templates

These files provide shape and placeholders but must be populated from the target repository:

- `.agents/notes/archived/manifest.json` starts empty and records the target's sealed artifacts.
- `docs/i18n/terminology.md` records the target's actual translation decisions.
- `docs/subsystems/README.md` and `.zh.md` index the target's real subsystem pages.

Populate these entries from the target repository during bootstrap.

## Audit

The source commit is pinned in the manifest for traceability.

Run the policy audit from the Skill repository:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/audit_template_policy.py \
  --skill-root /absolute/path/to/project-doc-library/skills/project-doc-library
```

The audit checks template classification, protected hashes, and forbidden tokens.

To check only the protected copy, run:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/verify_template_integrity.py
```
