# Audit-struct standard

Compare the vault project to `schema/placement.md`. Do not invent a second tree.

## Checks

| Check | Fail if |
|---|---|
| Numbers | Folder ids ≠ 00–07 software / personal modules |
| Feature files | Missing `intent.md` / `design.md` / `queue.md` where a feature is listed |
| Names | Colliding `01`/`02` with `api/` or `work/` |
| Indexes | Any `00 - Index.md` |
| Homes | Audit/review files under `{agent_root}/docs/` |
| Caps | Typed file over `max_lines` |

## Persist

Type `audit-plan` only in the vault (`00 - Overview/` or `{F}/plans/`). Findings include path + fix + apply order.
