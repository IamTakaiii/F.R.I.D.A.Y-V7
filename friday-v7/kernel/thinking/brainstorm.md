# Friday v7 — Brainstorm (panel)

User-opt panel. **Default: do not spawn.** Not a domain. Load only on `/fr-panel` or an accepted design/review offer.

## Enter

`/fr-panel` `[N]` · design/review offer once · alias `brainstorm` in the surface description only (not the surface name). Skip → owning-mode counsel. Invalid N → ask, no spawn.

## Bounds

| Knob | Value |
|---|---|
| N | default 3 · min 2 · max 5 |
| Rounds | 1 |
| Lean | this beat only, N≤5 |
| Secrets | never pass keys/tokens to panel |

## Roles

| Owning mode | Catalog (first N in listed order, no dupes, no shuffle) |
|---|---|
| design | critic · customer · operator |
| review | security · domain · maintain · perf · lang-fw |
| other | critic · operator · then unused from both catalogs |

Review prefix: 3 = security · domain · maintain · 5 = all five.
Review lens: security=C3 · domain=C2 · maintain=C4/C5/C6+change-cost · perf=C4/scale · lang-fw=C7/C4

## Run

1. Validate N ∈ [2,5]
2. Pick first N in catalog order (no shuffle)
3. Spawn parallel, disjoint prompts (topic + role + no shared chat)
4. Partial fail OK; 0 success → counsel (parent next)
5. Parent synth: keep / drop / tension — no vote, no average
6. Return to the owning mode. Panel does not lock design.

## Spawn vs subagent

`extras/subagent.md` stays default never. This beat is the only lean N>0 exception, and only after user opt.
