# Agent Note Protocol

Agent Notes are durable decision records. They preserve the problem, the decision or proposal, alternatives that lost, consequences, verification, and named gaps that ordinary code and reference docs cannot carry.

## Path and lifecycle

Use `{lifecycle}/{class}/yyyy-mm-dd-topic-title.md`.

- `proposed/`: a future change under consideration.
- `implemented/`: a decision that shipped and is maintained in present tense.
- `rejected/`: a proposal kept only while its rationale prevents a plausible mistake.
- `archived/`: a frozen historical snapshot of an implemented note.

Use the closed classes `feature`, `bug-fix`, `simplification`, `architecture`, `process`, and `testing`. The date is the first-proposed date, not the acceptance date.

## Paired files

When bilingual documentation is enabled, every active note is a sibling triplet:

```text
topic.md
topic.zh.md
topic.i18n.yaml
```

Both language files have equal authority. The sidecar records the last-confirmed Git blob hash of both files. Do not update a sidecar until both sides have been reviewed for meaning and structure.

## Header and body

The first block is:

```markdown
# Agent Note: <title>

Status: <status>
```

Required statuses are `proposed`, `implemented`, and `rejected — <reason>`. The body starts with `## Problem` and always has `## Alternatives considered`, unless a pre-format historical record has an explicitly documented grandfather exception. The class and first-proposed date live in the path, not in the header.

Use these lifecycle skeletons:

```markdown
## Problem
## Proposal
## Alternatives considered
## Acceptance criteria
## Risks
```

for `proposed/`, and:

```markdown
## Problem
## Decision
## Alternatives considered
## Consequences
```

for `implemented/`. An implemented note may add present-tense `Testing`, `Deferred`, or `Related` sections. It MUST NOT retain `Proposal`, `Plan`, `Migration plan`, or `Acceptance criteria` as shipped-state headings.

Rejected notes retain their proposal shape and put the verdict on the `Status:` line. Archived notes retain their body and add only `Archived: YYYY-MM-DD` below `Status: implemented` in both language files. The archive manifest seals every file in the frozen tree with a content hash.

## When to write or update

Write or update an Agent Note when a change alters behavior, architecture, a shared contract, process or tooling, testing strategy, durable or wire format, configuration semantics, security policy, or another decision a maintainer may revisit. Updating the existing owner is better than creating a duplicate.

An Agent Note is not a migration checklist, implementation diary, test walkthrough, or copy of a current API reference. Keep the rationale and the verification contract, then link to current code and docs.

## Supersession

Search active notes by symbols, package names, configuration keys, event names, and distinctive phrases before adding a note. A full supersession is safe only when the new owner preserves every unique rationale, alternative, consequence, required verification, and coverage gap, and no old behavior or compatibility obligation survives. Partial supersession keeps both notes active and cross-linked.

Never invent alternatives. If the historical record cannot establish them, state that honestly rather than manufacturing a plausible debate.
