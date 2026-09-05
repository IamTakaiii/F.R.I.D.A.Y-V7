# Routing Policy (v7)

Machine-readable SoT: `routing/registry.json`. Do not duplicate route signals or mode lists here, in surfaces, or in domain orient modes.

## Precedence

1. Exact registered surface or alias.
2. Clear outcome evidence; apply both `positive` and `negative` signals.
3. Tied plausible routes → one contrast question.
4. No evidence → six-group fallback from the registry.
5. Greeting, thanks, simple math → no skill.

One request has one primary route. Secondary work is an explicit handoff.

## Confidence

| Level | Action |
|---|---|
| high | Name `surface → mode`, load its domain mode, and continue **in this turn**. Do not make the user repeat the request. |
| medium | Ask one contrast question naming the two outcomes and your bet. Answer → dispatch in the next turn. |
| low | Show only the registry's six outcome groups. Ask which result they want; never dump surfaces or modes. |

The deterministic aid `routing/route.py` uses the registry's evidence weights. The LLM may understand paraphrases the script cannot, but it must obey the same precedence, exclusions, and confidence actions.

## Evidence contract

`routing/registry.json` carries signals only. Examples live in `evals/routing-examples.json` and are **proven by score** — there is no exact-match shortcut, so an example that only passes because it is listed is a failing example.

Two rules keep sibling routes apart:

1. A `negative` names the **sibling's canonical positive phrase**, never a generic word. `load test capacity` discriminates; `test` does not.
2. A contrast example ("do X, not Y") mentions Y, so Y's negative fires against X. The intended route therefore needs **≥2 positive hits** on the intent half, and the rival needs a negative naming X. One hit each is a tie, and a tie is `medium` — correct behaviour, but not a passing example.

Mine positives from the intent half only. Never promote the contrast half to a positive.

## Hierarchy

The registry targets `domain.mode` and its owning surface. `/fr` may load that surface and mode directly after a high-confidence route. Domain surfaces use the same registry filtered to their domain; they do not maintain another classification table.

Loading order after dispatch:

1. `kernel/runtime.md` (once)
2. owning `domains/<domain>/SKILL.md`
3. exactly one `domains/<domain>/modes/<mode>.md`
4. only what that mode names

## Aliases

An alias beginning with `/` is legal only when:

- its first token is a registered surface, **or**
- `hosts/opencode/commands/<alias>.md` exists and dispatches to the owning surface+mode.

Aliases are OpenCode conveniences, not extra surfaces. Claude/Codex use `/fr <outcome>` or a registered surface.

## Boundaries

`negative` evidence is load-bearing. In particular: intake ≠ review · debug ≠ load test · current architecture ≠ architecture improvement · vault audit ≠ code architecture · incident runbook ≠ guided setup · stakeholder brief ≠ stakeholder questions · Design ≠ experiment · locked slices ≠ uncertain decision map · TDD loop ≠ run the existing suite.

Outcome beats a keyword. Never route v7 to v5/v6. Durable writes still follow `schema/allow.md` and `schema/placement.md`.
