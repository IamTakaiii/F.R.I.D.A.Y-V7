# Gate — Ready

Fail **must** → do not code. `Gate failed: R#`.

## All tiers

| # | Must |
|---|---|
| R0 | Outcome in one line |
| R1 | Out-of-scope named or `none` |
| R2 | No invent — paths from Design, OpenAPI, code, or user |
| R12 | Risk screened (`execution.md`); unknown ≠ low |

S-light only when every applicable risk dim is low.

## M / L / high-risk

| # | Must |
|---|---|
| R3 | Feature List row + Intent (or approved package) |
| R16 | Queue `next`/`ready` ≤5 or skip-reason |
| R4 | Work-item has checkable DoD |
| R5 | Approach fork resolved if ≥2 options |
| R7 | Design card exists; contracts usable; required deep musts passed or N/A + evidence (L must; M if contract/fork) |
| R8 | DB: data path known or “no schema change” |
| R10 | Each unfinished dep has stub/contract/flag/block/narrow |
| R11 | Fits Architecture if that card exists |
| R13 | Plan Lock on the work-item |
| R14 | Compat/migrate/rollback/health or evidenced N/A |
| R15 | Each DoD + dominant risk → planned verify |

Fail → `/fr-design` · `/fr-sdlc` arch/sync · counsel — not implement.
