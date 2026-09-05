# SDLC — implement

One queue item (`next`/`ready` ≤5). No-artifact only for a tiny local edit — still need a known path + verify.
Writes: work-item via write-gate.

| Path | When | Before code |
|---|---|---|
| **S** | One item · DoD clear · all risks **low** · no arch/contract/schema | Ready-light. No `code.md`. |
| **Full** | high / unknown-critical · contract/arch · multi-file · L | `execution.md` + Ready + Plan Lock. User restates Ready in one line. Then `code.md`. |

S fails or scope grows → Full now. Ready fail → `Gate failed: R#`, no edits.
Test-first requested, or the item is complex logic behind one interface → run `modes/tdd.md` for the build, then return here for Done.

Unfinished `depends_on` → `../standards/deps.md`. Schema touch → `../standards/data.md`. Contract/schema change → write-gate `rev++` + history (Done **D6**).

## Ready-light / Done-light (S)

Ready: item+DoD · risks all low · path known · no contract/arch/schema · dep strategy · work-item file · honest names, no hidden I/O, no new infra, no drive-by.

Done: verify or accepted not-run · diff reviewed · queue + work-item `Done · Where · Verify · Left` · no drive-by.

## Pulse

```
T1 Ready(+light) + parallel reads
T2 Batch disjoint edits; re-plan if blast/contract/assumption breaks
T3 Diff lenses → verify vs DoD
T4 Done(+light) + vault
```

Close session only if the turn ends (`kernel/session/session.md`).
