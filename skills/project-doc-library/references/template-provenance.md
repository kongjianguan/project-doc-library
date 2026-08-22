# Template Provenance

The templates are split into two classes so a bootstrap can preserve DSH's documentation contracts without copying DSH's current product inventory.

## Canonical DSH templates

These files are copied from the DSH documentation contract and must remain byte-identical to the selected DSH checkout:

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

The canonical files carry rules, writing style, pairing mechanics, and lifecycle semantics. They may contain links to DSH-specific examples; those examples are protocol references, not project facts to copy into the target repository.
The machine-readable [template-manifest.json](template-manifest.json) pins the selected DSH commit and SHA-256 for every canonical file. The initializer refuses to run when an embedded canonical file has drifted from that manifest.

## Project-generated templates

These files keep the DSH shape but must be populated from the target repository:

- `.agents/notes/archived/manifest.json` starts empty and is sealed as notes enter the archive.
- `docs/i18n/terminology.md` records the target project's actual terms.
- `docs/subsystems/README.md` and `.zh.md` index the target project's real subsystem pages.

Do not copy DSH's Cordis terminology, subsystem inventory, or archive manifest into another project.

## Audit

Given a local DSH checkout, run:

```sh
python3 /absolute/path/to/project-doc-library/scripts/audit_template_hashes.py \
  --dsh-root /absolute/path/to/deepseek-harness
```

The audit fails when a canonical template differs, when a template is not classified, or when an expected template is missing. It reports differences in project-generated templates without treating them as errors.

To check the embedded copy without a DSH checkout, run:

```sh
python3 /absolute/path/to/project-doc-library/scripts/verify_template_integrity.py
```
