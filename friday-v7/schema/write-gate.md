# Vault write gate

One procedure for every `/fr-*` and every domain. Chat is not the artifact.

`allow.md` → type legal for this mode · `types.md` → type · `placement.md` → path · type file → copy · `artifact.md` → keys + cap.

## Copy (new file)

1. **Allow** — type is in the current mode’s row in `schema/allow.md`. Else stop.
2. Copy YAML + H1 + `##` sections from the type file.
3. **Drop** HTML comments and every `>` line — they must not appear in the vault.
4. Replace `{{placeholders}}`. `id` is stable forever.
5. Fill **required** sections in `<!-- fill: … -->`. Only `-`, empty table, or leftover `{{` → **failed**.
6. Omit empty optional sections. No fake `N/A` tables.
7. If `max_lines` is `0` (logs), skip count. Else count **body** lines (exclude YAML, `## Links`, `## Doc history`). Over `max_lines` → compress, then split only registered parts in `artifact.md`. `stem - Heading.md` = failed. Still over → failed.
8. `Doc history` row on create. Later: append on substantive edit. `rev++` only for contract or data-shape change.
9. Approve (`kernel/io/write.md`), then write via brain port.

## Patch

Keep keys and section order. History row. Re-count cap. Type stays the same (`patch` in allow.md).

## After

Cite the vault path. Do not paste the body. Over cap = not Done.

**Feature List SoT:** creating `intent.md` or `design.md` without a Feature List row whose SoT points at that feature → **failed**. Add or patch the row in the same work package (`type: feature-list`).

## Never

Second frontmatter schema · mode-local template · type off `allow.md` · orphan Design/Intent · empty required section · Design in the git repo or `.agent/` · Inbox rename-only promote · `doc_status` / `load_profile` · bare path in `## Links` / `## Parts` (must be `[[wikilink]]`)
