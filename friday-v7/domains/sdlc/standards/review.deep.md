# Review standard (deep)

Load when scoring. `score_pct = round(100 * Σ(score×weight) / Σ weights of scored dims)`. Omit N/A. Legal: **0 4 6 8 10**. **10** needs cited proof and zero findings on that dim.

## Code (C*)

Score C1–C7 always. C8 only if this diff changed observable behavior or a named contract.

| ID | Dim | 0 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| C1 | Fit | Wrong place | Leaky | Fits; one boundary leak | Fits; nit | Proven vs arch |
| C2 | Correctness ★ | Bugs / wrong rule | Gap on a real path or rule | Right on happy; one untested real path | Right; one untested edge | Contract + business rule + edges; no Assumed |
| C3 | Safety ★ | Secrets/authz/race | Partial | Threats named; open gap | Threats named; residual | Trust boundaries evidenced |
| C4 | Complexity | Overbuilt | Sprawls | Works; extra layer | Simple enough | As simple as the problem |
| C5 | Tests | Missing | Some | Right level; hole | Right level; thin assertion | Assertions lock the risk |
| C6 | Clarity | Obscure | Readable | Clear; odd name | Clear; nit | Names + why |
| C7 | Consistency | Fights repo | Drift | Matches; small drift | Matches | Matches; no style debt in scope |
| C8 | This-change docs | Behavior changed; docs silent | Partial | Match; missing one path | Match | Cite Design for the change |

★ C2+C3 must be **10** or code FAIL. Incomplete Design elsewhere is the **artifact** track.

Weights: C2×2 C3×2 C1×1.5 C5×1.5 C4×1 C6×1 C7×0.5 C8×1.

Hunt all 8 lenses **before** scoring. Each lens emits one ledger row: `clean` + cited path, or finding ids. Silent lens = unread scope = FAIL. Map findings to dims; do not add dims.

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

No cite for the `clean` column → that row is not `clean`; it is unread scope.

Severity anchor (rubric in `review.md` wins on conflict):

| Lens | blocker | major | minor |
|---|---|---|---|
| security | authz bypass · secret leak | unvalidated real input · race on shared state | hardening nit |
| biz | wrong money/data rule | wrong rule on a real path | edge nobody hits |
| perf · scale | unbounded growth that takes the system down | N+1 or missing timeout on a hot path | micro-cost |
| maintain · change-cost | — | one-way door · untestable seam | dup · placement nit |
| style · lang-fw | — | anti-pattern that hides a bug | naming · convention |

Also: happy/empty/replay · missing Must/false green (C5). Simulate a likely next change; if this shape would fight it → change-cost.

`code.md` findings map: policy→infra = C1 · I/O-in-loop/unlocked cache = C4 · untestable = C5 · hidden I/O name = C6 · fights neighbor = C7.

## Artifact (T*)

| ID | Dim | 0 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| T1 | Purpose | Unclear | Skimmable | Bottom line; thin | Bottom line | Audience + decision first |
| T2 | Completeness ★ | Missing decisions | Core; holes | Cold reader can act; hole | Cold reader can act | No trip-hole |
| T3 | Correctness ★ | Contradicts evidence | Minor mismatch | Consistent; unlabeled Assumed | Consistent; Assumed labeled | No Assumed on contracts |
| T4 | Precision | Vibes | Some seams | Named APIs/fields; hole | Named APIs/fields | Errors + owners |
| T5 | Structure | Wall / empty H2 | OK | Scannable; filler | Scannable | Tables; no filler |
| T6 | Traceability | No links | Some | SoT paths; missing id | SoT paths | ids + rev |
| T7 | Risk | None | Partial | Failures; no owner | Failures | Recovery + owners |
| T8 | Currency | Stale | Behind | Honest rev; unmarked drift | Honest rev | Drift marked |

★ T2+T3 = 10 or artifact FAIL. Do not score T* from code style.
Ledger: each T1–T8 emits `clean` + cite or finding before scoring. Silent dim = FAIL.

Weights: T2×2 T3×2 T4×1.5 T7×1.5 others ×1.

Also fail artifact: missing write-gate keys, wrong `placement.md` path, over `max_lines`, second source of truth.

## General (G*)

| ID | Dim | 0 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| G1 | Purpose | Missing | Vague who | Why first; thin | Why/who first | Audience + why first |
| G2 | Completeness ★ | Can’t act | Core; holes | Can act; gap | Can act | Cold reader acts; no trip-hole |
| G3 | Honesty ★ | Invented | Partial cite | Cited or Assumed | Cited; Assumed labeled | Cited; no Assumed on ★ |
| G4 | Usefulness | No decision value | Weak next step | Changes next action; fuzzy | Changes next action | Named next action |
| G5 | Clarity | Unreadable | Skimmable | Tight; noise | Tight | Tight; no filler |
| G6 | Open | Hidden landmines | Some open | Owned + dated; hole | Owned + dated | Owned + dated; no landmine |

★ G2+G3 = 10 or general FAIL. Weights: G2×2 G3×2 G4×1.5 others ×1.
Ledger: each G1–G6 emits `clean` + cite or finding before scoring. Silent dim = FAIL.

## Caps

Finding → dim ≤8. Major → ≤4 + track FAIL. Blocker → 0. `Assumed` on critical → ≤4 + FAIL. ≥3 minors → FAIL. Other-track finding → drop.
