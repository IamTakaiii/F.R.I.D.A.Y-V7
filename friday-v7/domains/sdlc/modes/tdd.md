# SDLC — tdd

Test-first delivery of one work item: red → green, one vertical slice per cycle. Writes: work-item, queue via write-gate.

Not the suite runner (`modes/test.md`). Not coverage evidence (`../standards/test.md`). Not the non-test-first path (`modes/implement.md`).
Test quality bar: `../standards/tdd.md` — load it before T0 and keep it open for every cycle.

Red and green verdicts are real command output only (`kernel/io/verify.md`). A described run is not a verdict.

## T0 Seam lock (gate)

Write the seams under test — the public boundaries where behaviour is observed without reaching inside — and **get the user to confirm them**. No test is written at an unconfirmed seam.

Ask: what is the public interface, and which seams should we test?

| Gate | Must |
|---|---|
| named | each seam is a real callable interface in this repo, with a path |
| observable | behaviour is assertable through that seam alone |
| bounded | seams cover DoD + dominant risk, not every edge case |
| runnable | one repo command already runs tests at that seam, once, green |

Interface shape itself in question (module depth, where the seam belongs) → that is Design, not TDD: hand to `modes/design.md` and stop.
No correct seam exists → architecture finding. Say so; never write a shallow test for false confidence.

User AFK → propose the seams, state you are proceeding on the proposal, and record it in the work-item.

## T1 Red

One seam, one test, one behaviour. Name it as a capability (WHAT), not a call sequence (HOW). Expected values come from an independent source — literal, worked example, spec — never recomputed the way the code computes them.

Run it. **Watch it fail for the stated reason.** Passing on the first run, or failing on a setup error, means the test is wrong — fix the test before any product code.

## T2 Green

Only enough code to pass this test. No speculative branches, no anticipating T1 of the next cycle, no drive-by.

Run the seam command. Red still → the last edit is the suspect; revert it rather than stacking guesses. Green with the previous cycles still green → close the slice.

## T3 Next slice

Repeat T1–T2. Each test is a tracer bullet that answers what the last cycle taught you.
**Never** write the tests in bulk and then the implementation — that is horizontal slicing (`../standards/tdd.md`).

New seam appears mid-loop → back to T0 for that seam only. Scope grew past the item → stop and re-queue.

## T4 Done

Refactoring is **not** in this loop — it belongs to `modes/review.md`. Leave the shape as-is and name it as a review candidate.

- Full suite run, redacted output, green (or accepted not-run with reason).
- Diff reviewed: no test at an unconfirmed seam · no anti-pattern from `../standards/tdd.md` · no drive-by.
- work-item + queue: `Done · Seams · Cycles · Verify · Left`.
- Coverage/effect evidence wanted → `/fr-test`; scored review → `/fr-review`.
