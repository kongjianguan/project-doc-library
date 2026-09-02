---
name: find-simplifications
description: Use when auditing a repository for non-obvious simplification candidates, writing durable decision records or local TODO notes, consolidating superseded records, or evaluating simplification ideas from another branch; especially for dead, duplicated, speculative, over-built, or hand-rolled surfaces.
---

# Finding Simplifications

Turn a broad "find things to simplify" request into a small set of evidence-backed changes. Decide what can be removed, merged, demoted, or replaced without treating complexity alone as a defect. Follow the code and prefer a few well-proven candidates over a pile of thin guesses.

## Establish Repository Context

- Read the repository's instructions, architecture notes, testing conventions, and decision-record rules before judging the target area.
- Identify intentional extension points, compatibility surfaces, supported implementations, and recently settled decisions before proposing their removal.
- Locate the repository's existing decision-record and TODO conventions. Use them instead of creating a parallel record system.
- Identify production paths, runtime and configuration entry points, generated files, tests, and documentation that may consume the target.

When the repository uses [project-doc-library](../project-doc-library/SKILL.md), use it for documentation structure, Agent Note lifecycle, bilingual pairing, generated files, archive rules, and documentation validation. This Skill supplies simplification judgment; it does not replace that documentation system.

## Strong Candidates

A strong simplification removes, folds, or demotes something real and has clear evidence that the current design costs more than it buys:

- A public method, event, config knob, registry notification, helper, package, durable record, or test artifact has no production consumer.
- Tests or docs are the only consumers, and the behavior they pin is not load-bearing.
- Two representations mirror the same fact.
- A seam has methods every implementation must support but no consumer uses.
- A separate package exists only for test/demo/support code and adds publish or dependency overhead.
- A feature implements speculative generality without a current caller, requirement, or owner.
- An invariant, rollback path, expected-output set, or special-case test exists only to protect an unused API.
- Hand-rolled code reimplements what the language standard library or a well-maintained dependency already provides, and the swap would delete the implementation plus its dedicated tests.
- The simplified behavior may differ slightly, but the new behavior is still reasonable and easier to explain.

Thin candidates are usually not enough for a durable decision record: deleting one typo, running a static tool once, removing an intentionally documented implementation, or flagging "this looks complex" without call-site proof.

## Survey Broadly

Start with the largest production-code deltas and highest-cost lifecycle paths. A survey that stops after obvious unused symbols can miss duplicated lifecycle or defensive machinery carrying most of the cost.

Use parallel subagents only when breadth is needed. Split the survey by domain and require evidence, not guesses. Useful domains include core lifecycle, I/O and execution, adapters and extension points, configuration, and packages/scripts/tests.

If subagents are unavailable, cover the same domains yourself. Do not let the first good candidate stop the survey when breadth was requested.

## Trust And Lifecycle Boundaries

For every defensive copy, freeze, validator, and callback capture, name where the value came from and who owns it next. Same-process typed calls ordinarily borrow readonly values; parsers, config loaders, queues, serialized data, durable files, workers, processes, and wire decoders own or validate their data. Tests built around hostile getters, fake typed objects, callback replacement, or mutation after a same-process handoff are evidence of a potentially speculative contract, not automatic justification for keeping it.

For complex asynchronous code, draw the ownership graph and map each sentinel, readiness promise, cancellation path, disposer, and state flag to a distinct owner or transition. When several mechanisms mirror the same liveness or settlement fact, propose one transaction or lifecycle controller instead. Preserve separate machinery where it protects publication and rollback, callback containment, first-terminal-outcome arbitration, worker/process ownership, or dispose-to-quiescence.

## Hand-Rolled Code Versus A Dependency

Introducing a dependency is a valid simplification move when it produces net deletion. Use the repository's dependency policy and language version as the bar. For parsers, framers, retry/backoff loops, glob matchers, diff engines, and similar infrastructure, check whether the standard library or a well-maintained package already covers the required behavior.

Prove a dependency-swap candidate like any other, plus:

- Read the hand-rolled implementation and name the exact surface the replacement covers; residual semantics count against the swap and stay in the decision record.
- Check the replacement's maintenance, adoption, compatibility, and transitive footprint. Prefer the standard library when it is sufficient.
- Check existing decision records first. A replacement that collapses an intentional seam must beat its recorded rationale, not merely cite a dependency policy.
- Weigh net deletion: implementation plus dedicated tests plus docs, minus the glue that remains. A wrapper that relocates the same complexity is not a win.

## Prove Or Reject Each Candidate

For every symbol or behavior, classify consumers before writing:

- Production corpus: application/library source, runtime scripts, configuration, schemas, migrations, generated catalogs, and supported examples.
- Non-production corpus: tests, README/docs, decision records, snapshots, generated expected outputs, and comments.
- Ambiguous corpus: examples and scripts that may be product smoke paths. Inspect usage before classifying.

Use `rg` or the repository's equivalent search tool first. Search the exact symbol, event name, package name, config key, method name with both `.name(` and `name(`, and any serialized or wire strings. Then read the call sites. Static analysis can help, but it is not a substitute for understanding public interfaces, dynamic names, tests, docs, and runtime loading.

Reject or downgrade a candidate when:

- A production caller exists and the simplification would be a feature decision rather than a cleanup.
- The API is explicitly justified by an existing decision record or a hard-won defensive pattern, and the new evidence does not beat that reason.
- The removal would force unrelated churn without actually reducing the public API or required behavior.
- The idea is correct but tiny. Add a targeted TODO/FIXME/XXX instead, using the repository's local convention.

## Coalesce Superseded Decision Records

Audit the repository's decision-record tree when the user asks to reduce or coalesce it, or when the simplification being implemented makes an owning record obsolete. Do not expand every code-simplification survey into a repository-wide record audit.

Follow the repository's retention and archive rules. Preserve records that explain a current contract, compatibility obligation, rejected alternative, or condition for reintroduction. Archive or delete records only when the repository's rules say to do so; do not edit an archived record while simplifying current prose or code.

For each candidate chain:

1. Identify the current owner from shipped code, configuration, generated catalogs, package docs, newer decision records, and inbound links; dates and titles are discovery hints, not proof.
2. Classify the old record as fully or partially superseded. Any surviving behavior, current contract, durable format, compatibility obligation, or independently current rejected alternative makes it partial. Rationale that can be transferred to the current owner does not by itself make supersession partial.
3. For full supersession, move every unique rationale, alternative, consequence, shipped verification evidence, and named coverage gap into the current owner. An inventory that only describes deleted implementation mechanics is not one of those decision facts.
4. Repair every inbound link, then remove all required language variants and consistency records together.
5. Search exact filenames, symbols, config keys, event names, and wire strings after the edit. Keep partial supersessions cross-linked and current.

An added-then-removed feature is a common full-supersession case. Let the removal record own the history only when the feature is absent from production code, configuration, schemas, durable or wire formats, migrations, and compatibility behavior; no current documentation presents it as available; and no test exercises it as supported behavior. Removal rationale and tests that enforce absence may remain. Preserve why the feature originally existed, why that motivation no longer justified it, alternatives to full removal, the capability given up, conditions for reintroduction, and evidence that removal is complete.

Reject consolidation when the removal is only one transport, default, implementation, or presentation of a feature; when persisted data or compatibility handling survives; or when the removal record does not yet carry enough rationale to prevent accidental reintroduction. A current negative design decision may legitimately need its own record even though the removed implementation is gone.

## Write The Decision Record

For a durable proposal, use the repository's decision-record format and location. If the repository has no convention, choose a clear location and state the lifecycle explicitly. Keep one record per proposal and use links relative to the repository.

Prefer this structure, adjusting when the idea needs it:

- `# <action-oriented title>`
- `Status: proposed` or the repository's equivalent
- `## Problem`: name the current API, cite the relevant files, and state the consumer evidence. Separate production callers from tests/docs.
- `## Proposal`: say exactly what to remove, fold, demote, or rehome. Include tests, docs, READMEs, JSDoc, event-taxonomy, snapshot, and generated-file cleanup when relevant.
- `## Why not keep it?` or `## What we give up`: make the strongest counterargument legible.
- `## Acceptance criteria`: observable end state and gates.
- `## Risks`: public API changes, behavior changes, future product wants, and why the tradeoff is still reasonable.

Be concrete enough that an implementing change can follow the trail. Avoid vague "simplify this package" records. When a proposal overlaps an existing record, consolidate the useful details into the existing owner rather than creating a duplicate.

## Inline TODO Notes

Use inline TODO/FIXME/XXX only for small, local cleanups that are clearly useful but not durable design decisions. Keep them short and actionable:

- Name the smell with a stable tag, e.g. `TODO(double-default)` or `XXX(unused-default)`.
- Explain why it is safe to revisit and what action would simplify it.
- Do not add TODOs for speculative complaints or for behavior that needs a durable decision.

## When Folding Another Branch Or Change

Diff the sibling branch against the common base or repository default branch, not against the current branch, so you see its independent contribution. For each item:

- Port non-overlapping decision records or TODOs that meet the quality bar.
- Consolidate overlapping material into the existing record that owns the topic.
- Do not port duplicate or lower-confidence proposals just to preserve the count.
- Update the change description so reviewers see the true candidate count and scope.
- Close or delete duplicate external work only when the user asked you to, or when that housekeeping is clearly in scope.

## Validation

Run the repository's relevant documentation, lint, typecheck, and test commands for the affected surface, plus `git diff --check`. For code comments or Skill changes, run the relevant validator when one exists. Do not claim a check passed unless it was available and run.

When recording or proposing the change, summarize:

- How many decision records and inline notes were added, consolidated, retained as partial supersessions, or deleted.
- The main areas surveyed.
- What was intentionally excluded.
- Which checks passed.

For each consolidation group, name the old and current owners, state the evidence for full supersession, and explain why deletion is safe. If an added-then-removed scan finds no qualifying record, report that result and the representative partial cases retained.
