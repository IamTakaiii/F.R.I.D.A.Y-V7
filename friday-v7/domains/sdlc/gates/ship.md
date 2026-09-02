# Gate — Ship

Any unaccepted **must** → `no-go`. `go_with_conditions` only if the user owns residuals in writing.

## Must

| # | Gate |
|---|---|
| S0 | What ships named (commits / tags / queue ids) |
| S1 | No unaccepted Design / data-model / data-dict drift in scope |
| S2 | Verify green for release scope (`kernel/io/verify.md`) |
| S3 | Migrate plan if schema changed |
| S4 | Rollback path named |
| S5 | Smoke steps listed |
| S6 | Design/product gates checked |
| S7 | Env/secrets confirmed (not pasted into vault) |
| S8 | `ship-checklist` current at `06 - Ship/YYYY-MM-DD - Ship.md` |
| S9 | L / high-risk: latest scoped code review PASS cited |
| S14 | M/L/high-risk: health signals, fail threshold, monitor window, owner |
| S15 | Data/irreversible: rollback executable and compatible with migrate direction |

## Should

S10 data rev matches migration · S11 monitor window + owner · S12 handoff after ship · S13 cost-log glance if present

## Verdict

`go` · `go_with_conditions` · `no-go`. Never claim deployed without user/env action.
