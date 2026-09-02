# Review standard (deep)

Load when scoring. `score_pct = round(100 * Σ(score×weight) / Σ weights of scored dims)`. Omit N/A. **4** needs cited proof and zero findings on that dim.

## Code (C*)

Score C1–C7 always. C8 only if this diff changed observable behavior or a named contract.

| ID | Dim | 0 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| C1 | Fit | Wrong place | Leaky | Fits; nit | Proven vs arch |
| C2 | Correctness ★ | Bugs | Gap on a real path | Right; one untested edge | Contract + edges; no Assumed |
| C3 | Safety ★ | Secrets/authz/race | Partial | Threats named; gap | Trust boundaries evidenced |
| C4 | Complexity | Overbuilt | Sprawls | Simple enough | As simple as the problem |
| C5 | Tests | Missing | Some | Right level; hole | Assertions lock the risk |
| C6 | Clarity | Obscure | Readable | Clear; odd name | Names + why |
| C7 | Consistency | Fights repo | Drift | Matches | Matches; no style debt in scope |
| C8 | This-change docs | Behavior changed; docs silent | Partial | Match | Cite Design for the change |

★ C2+C3 must be **4** or code FAIL. Incomplete Design elsewhere is the **artifact** track.

Weights: C2×2 C3×2 C1×1.5 C5×1.5 C4×1 C6×1 C7×0.5 C8×1.

Hunt A–H **before** scoring: happy/empty/replay/concurrent · placement · DRY · timeout/retry · N+1 · authz/secrets · missing Must/false green · blast/migration.

`code.md` findings map: policy→infra = C1 · I/O-in-loop/unlocked cache = C4 · untestable = C5 · hidden I/O name = C6 · fights neighbor = C7.

## Artifact (T*)

| ID | Dim | 0 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| T1 | Purpose | Unclear | Skimmable | Bottom line | Audience + decision first |
| T2 | Completeness ★ | Missing decisions | Core; holes | Cold reader can act | No trip-hole |
| T3 | Correctness ★ | Contradicts evidence | Minor mismatch | Consistent; Assumed labeled | No Assumed on contracts |
| T4 | Precision | Vibes | Some seams | Named APIs/fields | Errors + owners |
| T5 | Structure | Wall / empty H2 | OK | Scannable | Tables; no filler |
| T6 | Traceability | No links | Some | SoT paths | ids + rev |
| T7 | Risk | None | Partial | Failures | Recovery + owners |
| T8 | Currency | Stale | Behind | Honest rev | Drift marked |

★ T2+T3 = 4 or artifact FAIL. Do not score T* from code style.

Weights: T2×2 T3×2 T4×1.5 T7×1.5 others ×1.

Also fail artifact: missing write-gate keys, wrong `placement.md` path, over `max_lines`, second source of truth.

## General (G*)

| ID | Dim | Fail if |
|---|---|---|
| G1 Purpose | Why/who first | Missing |
| G2 Completeness ★ | Can act | Can’t act |
| G3 Honesty ★ | Cited or Assumed | Invented |
| G4 Usefulness | Changes next action | No decision value |
| G5 Clarity | Tight | Unreadable |
| G6 Open | Owned + dated | Hidden landmines |

★ G2+G3 = 4 or general FAIL. Weights: G2×2 G3×2 G4×1.5 others ×1.

## Caps

Finding → dim ≤3. Major → ≤2 + track FAIL. Blocker → ≤1. `Assumed` on critical → ≤2 + FAIL. ≥3 minors → FAIL. Other-track finding → drop.
