# Documentation Tiers

## One home per fact

Classify a document by its intended use, not its filename. Keep each fact in the tier whose job it is and link to that tier elsewhere.

| Tier | Owns | Excludes |
|---|---|---|
| Root `AGENTS.md` | Repo-wide standing orders | Stories and long procedures |
| Subtree `AGENTS.md` | Rules local to a subtree | Rules already owned by the root |
| `docs/architecture.md` | Ordered system map and extension points | Type catalogs, package details, decision rationale |
| `docs/subsystems/` | Stable types, semantics, and subsystem vocabulary | Cross-system behavior narration |
| `.agents/notes/` | Decision rationale, alternatives, trade-offs, and verification | Current API reference and task checklists |
| `docs/postmortem/` | Failure evidence, causal chain, and prevention | Ordinary bug fixes and design proposals |
| `docs/cookbook/` | Ordered how-to instructions with verification | Architecture rationale |
| `docs/user/` | Product-facing guides and tutorials | Maintainer policy and generated catalogs |
| Package README | Package consumer contract, limitations, and extension points | Restated JSDoc and other packages' concerns |
| Generated catalog | Exhaustive source-derived facts | Hand-edited English content |
| `.agents/skills/` | Reusable workflows and decision standards | Runtime or product contracts |

## Tutorial versus reference

A tutorial leads a reader through ordered work to an observable outcome. Establish prerequisites before dependent concepts and move optional advanced detail to a later page. A reference supports lookup within an explicit scope and does not require sequential reading. Split substantial mixed forms; label a small secondary form instead of creating needless files.

## Authoring rules

- Describe current state in durable docs. Put change history in commits, Agent Notes, and postmortems.
- Keep the direct document subject detailed and summarize children by purpose, responsibility, and high-level behavior.
- Put testing infrastructure at the lowest owning level.
- Keep comments and JSDoc focused on complete contracts: behavior, failure, timing, ownership, exceptions, and consequences.
- Remove duplicated rationale, control-flow narration, review choreography, and hand-written inventories when a source or generator is authoritative.
- Use repository-relative Markdown links and verify fragments before moving a file.
- Keep one physical line per prose paragraph only when the repository's Markdown gate requires it.

## Budgets

Treat word-count ceilings as guardrails, not reduction targets. When a document exceeds its budget, relocate content that belongs elsewhere, condense content that belongs here, and raise the ceiling only when the subject genuinely needs the space. Keep a small headroom below the ceiling.
