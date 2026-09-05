# SDLC — debug

Hard bugs and performance regressions. The feedback loop comes before the theory. Writes: `fix-note`; then hand the proven fix to normal implementation discipline.

Secrets in commands, output, traces, and captures become `<REDACTED>` before display or persistence.

## D0 Build the loop

Find one agent-runnable command that exercises the user's **exact symptom** and can turn red on the bug, then green on the fix. Prefer: failing test → HTTP script → CLI+fixture → browser assertion → trace replay → throwaway harness → property/fuzz → `git bisect run` → old/new differential → structured HITL script.

Spend disproportionate effort here. Tighten until:

| Gate | Must |
|---|---|
| red-capable | asserts the symptom, not merely “did not crash” |
| deterministic | same verdict; flaky case has a pinned, high reproduction rate |
| fast | seconds, not minutes; name the unavoidable setup if slower |
| agent-runnable | one command, already run once, with redacted output |

No red-capable command → no hypothesis. State what was tried; ask for environment access, a redacted capture, or permission for temporary instrumentation.

## D1 Reproduce and minimise

Confirm it is the reported bug, across repeated runs. Remove inputs, callers, config, data, and steps one at a time. Re-run after each cut. Done when every remaining element is load-bearing.

## D2 Hypotheses

List 3–5 ranked, falsifiable hypotheses before testing any. Format: `If X is the cause, changing Y makes the bug disappear / Z makes it worse.` A claim without a prediction is a vibe — drop it.

Show the ranking to the user; continue if they are AFK.

## D3 Probe

One variable per probe; each probe maps to one prediction. Prefer debugger/REPL → targeted boundary logs → never “log everything and grep”. Tag temporary logs `[DEBUG-<id>]`.

Perf: establish a numeric baseline and profiler/query-plan evidence, then bisect. Measure first, fix second.

## D4 Lock the regression

Use the seam where the real bug pattern occurs. Turn the minimal repro into a failing test, watch red, apply the smallest fix, watch green, then run D0 against the original scenario.

No correct seam is an architecture finding — do not write a shallow test that gives false confidence.

## D5 Cleanup and capture

- Original loop green; regression green (or missing seam documented).
- Grep and remove every `[DEBUG-<id>]`; delete throwaway harnesses.
- `fix-note`: symptom · one-command repro · minimal cause · rejected hypotheses · fix · regression seam · verification.
- Review follow-up still uses `modes/fix.md`; incident procedure uses `runbook` there.
