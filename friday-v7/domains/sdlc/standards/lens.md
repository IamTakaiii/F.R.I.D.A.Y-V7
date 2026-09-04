# Review lenses

The 8 code lenses live here and only here. Card level — `/fr-review` scoring and implement/fix self-review (`execution.md`) both load this. This file never scores; bands live in `review.md`, weights in `review.deep.md`.

Hunt all 8 **before** scoring or claiming self-review. Each lens emits one ledger row: `clean` + cited path · finding ids · or `N/A` + reason. Missing row = unread scope = FAIL.

| Lens | Hunt | `clean` needs this cited | Dim |
|---|---|---|---|
| security | authz · secrets · trust boundary · race · injection | authz on every entry point in scope; no secret; untrusted input validated | C3 |
| style | names · repo convention · in-scope style debt | compared against ≥1 neighbor file | C6 C7 |
| biz | invariant · impossible state · formula · rule vs Intent · error path · back-compat of a changed contract | each rule traced to an Intent/Design line; error path named | C2 |
| perf | N+1 · I/O-in-loop · timeout/retry · hot path | hot path named; no unbounded call inside a loop | C4 |
| maintain | DRY · placement · testability · hidden I/O | the seam runs without the whole app | C4 C5 C6 |
| scale | concurrent writer · blast/migration · unbounded growth · rollback · health/observability | concurrency and a growth bound both named; rollback exists or is stated N/A | C1 C4 |
| lang-fw | language/framework anti-pattern | idiom checked against a neighbor or official doc | C4 C7 |
| change-cost | rigidity · one-way door · next-change cost | one likely next change simulated | C1 C4 |

No cite in the `clean` column → that row is not `clean`; it is unread scope.

Severity anchor — the rubric in `review.md` wins on conflict:

| Lens | blocker | major | minor |
|---|---|---|---|
| security | authz bypass · secret leak | unvalidated real input · race on shared state | hardening nit |
| biz | wrong money/data rule | wrong rule on a real path | edge nobody hits |
| perf · scale | unbounded growth that takes the system down | N+1 or missing timeout on a hot path | micro-cost |
| maintain · change-cost | — | one-way door · untestable seam | dup · placement nit |
| style · lang-fw | — | anti-pattern that hides a bug | naming · convention |

Also: happy/empty/replay · missing Must/false green (C5). Simulate a likely next change; if this shape would fight it → change-cost.
