# Friday v7

Install beside v6: `./scripts/install.sh`. Do not load friday-v6 at runtime.

## Map — read in this order

```
SKILL.md                 identity only (not the rulebook)
kernel/runtime.md        cold path SoT
docs/USER-GUIDE.md       this file
DECISIONS.md             locked calls
ROUTING.md               which /fr-* to open
schema/                  write contract (order below)
domains/<name>/SKILL.md  → one modes/<job>.md
surfaces/fr-*/SKILL.md   thin stubs only
```

Do not cold-load `schema/` until the mode writes or migrates an artifact.

## Vault write (every command)

1. Type allowed — `schema/allow.md`
2. Path — `schema/placement.md`
3. Copy type file — `schema/types/` — strip `<!-- -->` and `>` lines
4. Shape + cap — `schema/artifact.md` · `schema/write-gate.md`
5. Layout — `schema/vault.md`

Never `stem - Heading.md`. Chat is not the artifact. Intent/Design without a Feature List SoT is a failed write.

## Existing feature (change or add)

Do not open a new feature folder. Patch the same package.

| What happened | Command | Touch |
|---|---|---|
| Code moved, docs lag | `/fr-sdlc` sync | Only the wrong file |
| Contract change (flow, owner, API, data) | `/fr-design` | `design.md` + matching part · HTTP → `api/` · irreversible → ADR |
| New slice in the same boundary | queue then `/fr-implement` | New `queue.md` row + `work/TODO-…` · Intent/Design only if scope changes |
| Bug / review follow-up | `/fr-fix` | `fixes/` or `work` · Design if the contract changed |
| New review | `/fr-review` | New `reports/YYYY-MM-DD - …` — never overwrite |

Patch: same type and heading order · `Doc history` row · `rev++` only for contract or data-shape · hub Links stay on `intent.md`. No `flow-2.md` / Design v2.

## Check

```bash
python3 evals/check_tree.py
python3 evals/check_vault.py --vault "$FRIDAY_BRAIN_ROOT"
```

## Scripts

| Path | Use |
|---|---|
| `scripts/install.sh` | Symlink this clone into host skill folders |
| `scripts/vault/` | One-off vault heal / migrate — not on the cold path |
| `scripts/retired/` | Do not run |

## Words

| Term | Meaning |
|---|---|
| card | Canonical file |
| part | Registered companion (`design/` or `stack`) |
| Links | Hub = `intent.md`. Others: Intent only. Last before history. Never `[[.]]` |
| Cap | 200 body lines; YAML / Links / history do not count. Logs = unlimited (`max_lines: 0`) |
| Flow | Bound + ` ```text` ` sequence + ` ```mermaid` ` + fail/next |
| queue | Feature work index |
| work-item | What shipped + Evidence (paths + verify). Not a copy of the queue row. |
| domain | Was v6 pack |

## v6 → v7 names (no auto-migrate)

| v6 | v7 |
|---|---|
| `01 - Intent.md` | `intent.md` |
| `02 - Design.md` | `design.md` |
| `03 - TODO.md` | `queue.md` |
| `02 - Work/` | `work/` |
| Data `03`/`04` | `04 - Data/` |
| Ship `04`/`05` | `06 - Ship/` |
| `review` / test-report / perf-report | `quality-report` + `kind` |
| `project-brief` / `personal-brief` | `brief` + `project_kind` |
