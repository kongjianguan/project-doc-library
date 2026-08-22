# Subsystems

English | [中文](README.zh.md)

This directory describes real subsystems and the contracts that connect them. It is an index of owned reference pages, not a directory of arbitrary package summaries.

| Page | Owns |
|---|---|
<!-- Add one row per real subsystem page after inspecting the source. -->

## One page per subsystem

Create a page when a subsystem has its own vocabulary, boundary, lifecycle, extension point, or failure modes. Give the page a stable name, add it to the table above, and link it from `docs/architecture.md`.

Each page SHOULD answer:

```markdown
# <Subsystem>

## Purpose

State the responsibility and the boundary.

## Ownership and dependencies

State who owns the boundary and which dependencies it may call.

## Core concepts

Define the types, states, and invariants that readers must share.

## API and extension points

Describe the supported entry points and the rules for extending them.

## Failure behavior

Describe errors, recovery, and observable diagnostics.

## Verification

List the focused tests, commands, or generated checks that establish the contract.
```

## Source-equivalent facts

Type signatures, public options, generated API regions, and other source-derived facts MUST have a source owner. Link to generated references or regenerate them from the source declaration. Do not hand-maintain a second signature catalog in prose.

## Boundaries

Describe dependency direction and ownership explicitly. A subsystem page MAY link to an Agent Note for rationale, but the current contract belongs here or in the source it describes.

## Review standard

Keep pages precise enough to verify and small enough to scan. Split a page when it has multiple unrelated boundaries or audiences. Update the architecture map when adding, removing, or renaming a subsystem.
