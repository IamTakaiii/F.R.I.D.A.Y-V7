# SDLC — design experiment

Build disposable code to answer **one named design question**. The question decides the artifact.

| Question | Experiment |
|---|---|
| Does this logic or state model behave right? | One runnable state explorer; controls drive hard cases and show the full state after every action. |
| What should this interaction look like? | Several radically different variants on one route, switchable without rebuild. |

Ambiguous → ask. User unavailable → infer from surrounding code and mark the assumption at the top.

## Rules

1. Mark `PROTOTYPE — NOT PRODUCTION`; place near the target using repo conventions.
2. One command to run, no setup puzzle.
3. State in memory by default. Persistence only when it is the question; use clearly disposable storage.
4. No production polish: no abstractions, tests, or error handling beyond what answers the question.
5. Surface all decision-relevant state and events.
6. Define the verdict before coding: what observation answers yes/no or chooses a variant.

## Close

Run it with the user. Record: question · observation · verdict · decision affected.

Fold only the validated decision into Design/ADR. Keep the experiment off main (throwaway branch with a pointer) when it is valuable primary evidence; otherwise delete it. Production never depends on it.
