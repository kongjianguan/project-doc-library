# Bootstrap Workflow

## Goal

Create a usable documentation library without fabricating project knowledge. The bootstrap result should make the next non-trivial change easy to document and should not require a later rewrite of every file.

## Discovery order

1. Read the root `AGENTS.md` and every applicable subtree instruction.
2. Read `memory/`, existing `docs/`, component READMEs, source JSDoc, generators, and validation scripts. Treat the protected protocol templates listed in [template-provenance.md](template-provenance.md) as reusable contract text; preserve their rules and structure while replacing all target facts with findings from the target repository.
3. Record the repository's package manager, test commands, build commands, document languages, and generated-file conventions.
4. Locate existing architecture, API, tutorial, incident, and decision documents. Do not move them until inbound links and ownership are understood.
5. Identify facts that are already generated. The generator remains their source of truth.

## Initial tree

The initializer creates the structured skeleton below and skips files that already exist:

```text
.agents/notes/
├── AGENTS.md
├── README.md
├── README.zh.md
├── README.i18n.yaml
├── proposed/{feature,bug-fix,simplification,architecture,process,testing}/
├── implemented/{feature,bug-fix,simplification,architecture,process,testing}/
│   ├── AGENTS.md
│   └── CLAUDE.md -> AGENTS.md
├── rejected/{feature,bug-fix,simplification,architecture,process,testing}/
└── archived/{feature,bug-fix,simplification,architecture,process,testing}/
    ├── AGENTS.md
    └── manifest.json

docs/
├── AGENTS.md
├── i18n/{README.md,README.i18n.yaml,translation-rules.md,translation-rules.i18n.yaml,terminology.md,style-samples.md,translation-prompt.md}
├── subsystems/README.md
├── postmortem/README.md
├── cookbook/
└── user/{guide,develop/{basic,framework,practice}}/
```

The class set is deliberately closed. Add a class only when the repository has a real distinction and the validator and README change together.

The i18n contract excludes instruction files, frozen archived notes, bilingual-by-construction terminology and style samples, and machine-consumed translation prompts. Do not add sidecars for those exclusions.

The bundled templates distinguish protected protocol files from target-adapted files. Protected files preserve normalized rules and style; the archive manifest, terminology table, and subsystem index are populated from the target repository.

## After scaffolding

- Replace generic wording with the repository's actual package, source, command, and generator names.
- Create `docs/architecture.md` only after reading the code and mapping composition, core components, lifecycle, and extension points.
- Create subsystem pages for real stable vocabularies, not for every package.
- Add a cookbook page when a contributor must perform an ordered sequence to reach a verifiable outcome.
- Add a postmortem only for a subtle, systemic, and expensive-to-rediscover failure.
- Add an Agent Note for a decision that a future maintainer may reasonably revisit.
- Keep the initial change small enough to review. The library is useful only after one real change exercises it.
