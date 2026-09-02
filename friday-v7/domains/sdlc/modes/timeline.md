# SDLC — timeline

Four evidence-backed logs in Overview. Collection is read-only (no git write). Persist the chosen view.

## Views

| View | File |
|---|---|
| production_feature_log | `00 - Overview/04 - production feature log.md` |
| development_feature_log | `00 - Overview/05 - development feature log.md` |
| production_change_log | `00 - Overview/06 - production change log.md` |
| development_change_log | `00 - Overview/07 - development change log.md` |

## Evidence

Vault dated intent/design/ADR/release. Git = metadata; impact is `inferred` unless corroborated. Missing dates = `undated`. Never invent dates. Unlabelled commits = development, not production.

## Content

Feature item: what users can do · get · why + cite. Change item: what changed · from · to · why (`Not stated` if unknown).

## Persist

Type `timeline-log`. One view unless user asks all four. Optional CLI: `scripts/fr-timeline.py` after approve.

## Done

Saved path or `Artifacts: none — user skipped`.
