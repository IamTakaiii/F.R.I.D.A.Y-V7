# Execution / risk

Controlled decisions + evidence — not longer chat. Used by implement and fix. Design owns contracts; gates own the result.

## Size ≠ risk

| Dimension | High-risk signals |
|---|---|
| Data | irreversible migration · tenancy · recovery unclear |
| Security | authz · secrets · sensitive data · trust boundary |
| Contract | public API/event/schema · persisted format · external consumers |
| Correctness | money · concurrency · idempotency · distributed state |
| Operations | prod path · wide blast · weak rollback/observability |
| Evidence | unfamiliar · stale contract · weak tests |

Rate each `low | medium | high | unknown` + one evidence phrase. **Unknown ≠ low.**
Any `high` or unresolved critical `unknown` → full Ready/Done + Plan Lock.

## Control flow

Contract → risk screen → inspect (no tree tour) → Plan Lock if full → execute small increments → self-review **actual diff** → verify map → Done.

## Plan Lock (full path)

Record on the work-item or a short work package:

| Field | Must |
|---|---|
| Outcome / out | What changes; what does not |
| Touch set | Files/modules; source of each path |
| Invariants | Rules that stay true |
| Sequence | Ordered increments |
| Assumptions | Evidence or `Assumed` + owner |
| Compatibility | API/schema/event impact or `none` |
| Failure plan | Partial fail · retry · cleanup |
| Verify map | Each DoD/risk → evidence |
| Operate | Flag/migrate/rollback/health when applicable |
| Stop | Discoveries that force re-plan |

## Stop and re-plan

Pause when blast radius grows, contract/arch changes unexpectedly, assumption dies, tests show different behavior, or rollback disappears. Do not hide re-plan inside coding.

## Self-review lenses

`correctness` · `errors` · `data` · `security` · `concurrency` · `compat` · `bounds` · `ops` · `tests` · `drift` · `no drive-by`  
Shape: `code.md`. Do not invent scale infra.

## Evidence matrix

| Requirement / risk | Kind | Evidence | Result |
|---|---|---|---|
| DoD or dominant risk | happy/error/edge/regression/operation | cmd/path or manual | pass/fail/not-run |

“Tests passed” ≠ DoD covered.
