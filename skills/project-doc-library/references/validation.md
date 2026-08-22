# Validation

The bundled scripts provide structural checks. The target repository remains responsible for its own Markdown, link, generator, build, and CI commands.

## Platform notes

The scripts use `pathlib` for filesystem paths. On Windows, pass repository and Skill roots as native paths such as `C:\work\repository` or forward-slash paths such as `C:/work/repository`. JSON manifest keys and repository-relative Markdown paths intentionally use `/` on every platform; the scripts normalize native paths before comparing them.

## Initialize

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/init_project_docs.py --root /absolute/path/to/repository
```

The initializer is additive and refuses to replace existing files. Use `--no-bilingual` only when the repository has no second-language contract.
It also verifies the embedded protected-template manifest before copying anything.

## Verify

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/verify_project_docs.py --root /absolute/path/to/repository
```

Refresh reviewed active pairs with:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/refresh_i18n_sidecars.py --root /absolute/path/to/repository --write
```

Check exact duplicate prose paragraphs in active project docs with:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/lint_prose.py --root /absolute/path/to/repository
```

When editing this Skill, run the same check against its entrypoint and references:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/lint_prose.py \
  --skill-root /absolute/path/to/project-doc-library/skills/project-doc-library
```

When auditing the Skill templates for classification, protected hashes, and source-project contamination, run:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/audit_template_policy.py \
  --skill-root /absolute/path/to/project-doc-library/skills/project-doc-library
```

For an embedded-template integrity check, run:

```sh
python3 /absolute/path/to/project-doc-library/skills/project-doc-library/scripts/verify_template_integrity.py
```

The verifier checks:

- required contracts and lifecycle directories;
- the closed Agent Note class set;
- note header, lifecycle status, required sections, and archive metadata;
- complete bilingual triplets and current sidecar blob hashes;
- language switchers and the structural signature of each active pair;
- the implemented-to-archived path rule and the frozen archive manifest.

It does not judge architecture, prose quality, translation meaning, link reachability, or whether a generated catalog is fresh. Run the project's own narrow checks after it.

## Minimum project checks

Select checks from the actual repository:

- Markdown wrapping and link validation for changed docs;
- bilingual pairing for touched pairs;
- generator freshness for generated references;
- type-equivalence or code-fence checks when docs embed declarations;
- focused tests when visible strings or runtime behavior changed;
- `git diff --check` for every documentation change.

Report commands that were not available instead of inventing a passing result.
