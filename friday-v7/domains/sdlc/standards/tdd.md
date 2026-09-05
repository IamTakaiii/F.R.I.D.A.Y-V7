# TDD standard

What makes a test worth keeping. Load on `modes/tdd.md` (every cycle) and whenever `modes/review.md` judges test quality.
Not coverage evidence (`test.md` / `test.deep.md`). Not how product code is written (`code.md`).

## Seam

A **seam** is the public boundary where behaviour is observed without reaching inside. Tests live at seams, never against internals.
You cannot test everything — agreeing seams up front is how effort lands on critical paths and complex logic instead of every edge case.

## Good test

Verifies behaviour through the public interface. Reads like a specification: `user can checkout with valid cart` says which capability exists.
Implementation can change entirely and the test still holds. One logical assertion. Name says WHAT, not HOW.

## Anti-patterns

| Name | Tell | Instead |
|---|---|---|
| Implementation-coupled | mocks an internal collaborator · asserts call count/order · tests a private method · verifies through a side channel (`SELECT` after `createUser`) | assert through the same interface you called (`getUser(id)`) |
| Tautological | expected value recomputed the way the code computes it (`expect(add(a,b)).toBe(a+b)`; a hand-derived snapshot) | independent source: known-good literal, worked example, spec |
| Horizontal slicing | all tests first, then all implementation | vertical slices: one test → one implementation → repeat |

Implementation-coupled breaks on refactor while behaviour is unchanged — that is the diagnostic, not the style preference.
Tautological passes by construction and can never disagree with the code, so it is worth zero regardless of coverage.
Horizontal slicing verifies *imagined* behaviour: it commits to test structure before the implementation is understood.

## Mocking

Mock what you do not own and cannot run: third-party network, clock, random, paid APIs. Inject them (`code.md`).
Never mock a collaborator inside the seam under test — if that seems necessary, the seam is wrong.

## Self-check

Confirmed seam · behaviour through public interface · name says WHAT · expected value independent · no internal mock · no call-count assertion · survives a rename of internals · one test per cycle.
Any fail → fix the test before the next cycle. A red-flagged test is deleted or rewritten, never kept "for coverage".
