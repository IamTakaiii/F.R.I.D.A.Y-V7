# Test standard (card)

`/fr-test` also covers bench/load (`kind: perf`) and tooling init. Not review. Not write `.http`.

## Layers

| Layer | Question | Evidence |
|---|---|---|
| Run | Suite green? | `kernel/io/verify.md` — repo command only |
| Cover | DoD + contracts + dominant risks hit? | Design / Plan Lock + coverage cmd **if** in recipe/CI |
| Effect | Would a real break fail a test? | Mutation/CRAP only if those cmds exist |

Do not invent commands. Missing tool → `tool: none`, not FAIL.

## Scope

Default = unit + declared e2e. Feature folder → also requirement-evidence matrix.
HTTP with no repo e2e → name the gap; do not fail for missing httpyac.

## Pass

FAIL: red run · Must contract with no test · false-green · ≥3 minors.
PASS: run green (or accepted not-run) · Must cases mapped · no blocker.
Feature folder / score / `ละเอียด` → load `test.deep.md` and fill the evidence matrix — no shallow “tests passed”.

Persist `quality-report` (`kind: test` or `perf`) via write-gate.

Deep: `test.deep.md` on score / matrix / `ละเอียด`.
