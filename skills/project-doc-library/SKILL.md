---
name: project-doc-library
description: Use when bootstrapping or maintaining a repository-local documentation system modeled on DeepSeek Harness, including `.agents/notes` decision records, `docs/` tiers, bilingual pairs, postmortems, generated references, and lifecycle validation. Do not use for a one-off README edit.
---

# Project Documentation Library

Build a repository-local documentation system that gives every durable fact one owner, separates design rationale from current reference material, and gives agents a repeatable way to create, update, supersede, translate, validate, and archive documentation.

This skill is guidance, not a script or a request to copy DSH-specific product facts. Preserve the DSH shape where it improves discoverability, but derive names, subsystems, commands, generators, and terminology from the target repository. The canonical DSH protocol templates listed in [references/template-provenance.md](references/template-provenance.md) are copied in full; do not summarize, rewrite, or localize their rules. Their references to optional historical records and project-specific gates are protocol examples, not a requirement to clone DSH's entire repository. Project-generated templates remain target-specific and must be populated from the target repository.

## Choose a mode

- **Bootstrap**: establish the directory tree and contracts for a repository that lacks this system.
- **Maintain**: route a requested code or documentation change to its owning document, decision record, generated source, or postmortem.
- **Audit**: inspect placement, duplication, stale links, lifecycle drift, pairing drift, and generated artifacts without editing unless the user authorizes fixes.
- **Archive**: classify implemented notes by future decision value and seal only records that are no longer current authority.

Read [references/bootstrap.md](references/bootstrap.md) for initialization. Read [references/template-provenance.md](references/template-provenance.md) when auditing or changing templates. Read [references/notes-protocol.md](references/notes-protocol.md) before creating or moving an Agent Note. Read [references/docs-tiers.md](references/docs-tiers.md) before adding ordinary documentation. Read [references/maintenance.md](references/maintenance.md) for updates, supersession, and archive decisions. Read [references/i18n-and-generated.md](references/i18n-and-generated.md) when bilingual or generated docs are in scope.

## One home per fact

| Fact or purpose | Owning home |
|---|---|
| Standing instructions for agents | Root or subtree `AGENTS.md` |
| Current architecture and extension map | `docs/architecture.md` |
| Subsystem types, semantics, and API vocabulary | `docs/subsystems/` |
| Step-by-step procedures | `docs/cookbook/` |
| Product and contributor tutorials | `docs/user/` and `docs/development.md` |
| Incident evidence and prevention | `docs/postmortem/` |
| Decision rationale, alternatives, and trade-offs | `.agents/notes/` |
| Facts derived from source | The generator or source declaration |

Do not duplicate a rule in several homes. Link to the owner and keep local prose to the contract the reader needs at that point.

## Prose contract

- State one current fact or decision per paragraph. Prefer subject, action, boundary, and verification over scene-setting.
- Write current behavior in the present tense. Put history, incident chronology, and rationale in their owning records.
- Name the actual actor, command, file, symbol, boundary, or check. Link to an owner instead of restating its facts.
- Use `MUST`, `SHOULD`, and `MAY` only when the distinction changes enforcement. Remove narration, review choreography, speculation, and copied catalogs.
- Before finalizing, remove exact duplicate paragraphs and any paragraph that adds no contract beyond a nearby heading, table, or link.

When bilingual documentation is enabled, both sides carry equal authority. Preserve structure, code, paths, identifiers, links, warnings, and verification steps. Update the counterpart and sidecar in the same change; do not let a green structural check stand in for translation review.

## Bootstrap workflow

1. Read the repository root instructions, relevant subtree instructions, `memory/` when present, existing docs, package manifests, generators, and validation commands.
2. Inventory existing documents before creating directories. Preserve useful authority and identify duplicate or stale homes.
3. Run the bundled initializer only for missing structure:

   ```sh
   python3 /absolute/path/to/project-doc-library/scripts/init_project_docs.py --root /absolute/path/to/repository
   ```

   Add `--no-bilingual` only when the repository explicitly does not maintain a second language. The initializer does not overwrite existing files.
4. Read the generated contracts and replace project-neutral wording with facts from the repository. Do not invent subsystem names, commands, validators, or historical decisions.
5. Write the smallest useful architecture map, subsystem index, and development entry point. Create child pages only when the repository has a real subject for them; do not leave empty placeholders.
6. Add validation commands or adapters that the repository can actually run. A rule is not complete when its documented command does not exist.
7. Run the verifier, the repository's narrow documentation checks, and `git diff --check`. Report missing project-specific adapters instead of claiming DSH parity.

When changing the bundled templates, keep the canonical/adapted split in [references/template-provenance.md](references/template-provenance.md), run the embedded integrity check, and run the hash audit against a local DSH checkout when available.

## Maintenance workflow

Before editing prose, classify the requested change:

- Current behavior or API contract: update the owning reference, README, subsystem page, or generated source.
- A durable design decision: add or update an Agent Note in the same change.
- A subtle systemic failure: add a postmortem and link the guardrails it motivated.
- A procedure: update or add a cookbook guide with observable verification.
- A generated fact: change its source or generator, then regenerate.
- A translation change: update both sides and the consistency record.

For every new or changed Agent Note, search active notes for overlap before writing. Decide whether the old record remains active, is partially superseded and cross-linked, or is fully absorbed and removable. Never silently turn an old decision into its opposite.

For every lifecycle move, update both the path and the in-file status and satisfy the destination format in the same change. Never edit an archived note except through the archive procedure.

Use [references/validation.md](references/validation.md) for the minimum checks. The bundled verifier checks structure and pairing mechanics; the prose lint catches exact duplicate paragraphs; neither establishes semantic accuracy, translation quality, or whether a decision is wise.

After human review of active bilingual pairs, refresh their sidecars with:

```sh
python3 /absolute/path/to/project-doc-library/scripts/refresh_i18n_sidecars.py --root /absolute/path/to/repository --write
```

After writing documentation, run:

```sh
python3 /absolute/path/to/project-doc-library/scripts/lint_prose.py --root /absolute/path/to/repository
```

## Reporting

End with the inspected scope, documents created or updated, decisions retained or superseded, generated artifacts refreshed, checks actually run, and remaining gaps. Distinguish a clean structural check from a review judgment.
