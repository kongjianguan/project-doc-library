# Maintenance and Lifecycle Work

## Route a change

Start from the changed code or user request, then inspect the nearest existing owner. Use this routing:

- New durable design choice: create or update an Agent Note.
- Shipped contract or type: update the owning README or subsystem page.
- Architecture relationship or extension map: update `docs/architecture.md`.
- Ordered contributor action: update a cookbook.
- Product workflow: update a user guide.
- Subtle systemic failure: write a postmortem.
- Source-derived inventory: update the source or generator.

Do not create a new document just because the current owner is inconvenient. Move content atomically only after checking inbound links and fragment references.

## Update an implemented note

Keep an implemented note synchronized with shipped paths, symbols, defaults, and mechanisms. Rewrite stale facts in place. Do not append a history log. A reversal of the decision is a new note linked to the old one, not a silent rewrite.

## Supersession and consolidation

Classify an overlap as full or partial. Full consolidation requires the new owner to preserve every unique decision proposition and the old behavior, compatibility handling, and current references to be gone. Repair inbound links and remove the English note, Chinese counterpart, and sidecar together. Partial supersession keeps both records and cross-links them.

## Archive

Archive only an implemented note whose decision is complete and whose rationale is unlikely to guide future work. Do not use age, length, or a target quota as the criterion. Keep active notes when they contain a durable boundary, negative guarantee, security rule, wire or persistence semantic, alternative that prevents re-litigation, or reintroduction condition.

Archiving a bilingual note moves the complete triplet to `archived/{class}/`, keeps `Status: implemented`, adds the same archive date below the status in both language files, re-records the sidecar, repairs inbound links outside the frozen note, and updates the archive manifest if the repository has one. After sealing, never edit, translate, reformat, move, or delete the artifact.

## Review-only requests

For review or audit requests, report findings without editing. For explicitly requested fixes, make the smallest owner-first change and run the relevant checks. Do not use a documentation cleanup as permission to alter product behavior.
