# Bilingual and Generated Documentation

## Bilingual pairs

If the repository maintains two languages, use three sibling files and no locale directories:

```text
foo.md
foo.zh.md
foo.i18n.yaml
```

Both languages carry equal authority. Preserve heading hierarchy, list shape, table dimensions, code fences and bodies, inline code, semantic links, and language switchers. Translate prose naturally, but do not add or drop facts.

The sidecar records blob hashes, not commit hashes. Use the sibling file names as keys so the record can be computed with `git hash-object`:

```yaml
foo.md: <git-blob-hash>
foo.zh.md: <git-blob-hash>
```

A changed side must be paired in the same change and the sidecar re-recorded only after human semantic review. A green structural gate proves only that the recorded contents and structure match; it does not prove translation quality.

The English side links to the Chinese side and the Chinese side links back. Preserve heading depths, list shape, table dimensions, code fences, inline code, semantic links, and language switchers. Do not use locale directories or interleaved bilingual files.

Keep terminology in one `terminology.md` source of truth. Add a term there when the repository has made a durable translation choice. Keep machine-consumed prompt templates and agent instruction files outside the ordinary pair scope when pairing them would change behavior or duplicate a frozen artifact.

## Generated references

Generated English is owned by its source declaration or generator. Never hand-edit the generated region. Regenerate it, then update the reviewed counterpart and pairing record. A generated file MUST state its generator and freshness command near the top.

Examples of suitable generated references include type-equivalence pages, event and configuration catalogs, dependency graphs, and tool schemas. Create one only when the source data is authoritative and a freshness check can fail loudly.

## Exclusions

Document explicit exclusions in the i18n contract. Typical exclusions are agent instruction files, frozen archived notes, bilingual-by-construction terminology and style samples, machine-consumed prompt templates, and generated sources for which maintaining a reviewed counterpart is not meaningful.
