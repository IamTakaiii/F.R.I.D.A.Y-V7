# Review lenses

The 8 code lenses live here and only here. Card level — `/fr-review` scoring and implement/fix self-review (`execution.md`) both load this. This file never scores; bands live in `review.md`, weights in `review.deep.md`.

Hunt all 8 **before** scoring or claiming self-review. Each lens emits one ledger row: `clean` + cited path · finding ids · or `N/A` + reason. Missing row = unread scope = FAIL.

| Lens | Hunt | `clean` needs this cited | Dim |
|---|---|---|---|
| security | authz · secrets · trust boundary · race · injection | authz on every entry point in scope; no secret; untrusted input validated | C3 |
| style | names · repo convention · in-scope style debt · **smell baseline** | compared against ≥1 neighbor file **and** the baseline below | C6 C7 |
| biz | invariant · impossible state · formula · rule vs Intent · **not asked for** (`creep`) · error path · back-compat of a changed contract | each rule traced to an Intent/Design line; error path named; nothing in the diff without a requirement | C2 |
| perf | N+1 · I/O-in-loop · timeout/retry · hot path | hot path named; no unbounded call inside a loop | C4 |
| maintain | DRY · placement · testability · hidden I/O | the seam runs without the whole app | C4 C5 C6 |
| scale | concurrent writer · blast/migration · unbounded growth · rollback · health/observability | concurrency and a growth bound both named; rollback exists or is stated N/A | C1 C4 |
| lang-fw | language/framework anti-pattern | idiom checked against a neighbor or official doc | C4 C7 |
| change-cost | rigidity · one-way door · next-change cost | one likely next change simulated | C1 C4 |

No cite in the `clean` column → that row is not `clean`; it is unread scope.

## Smell baseline

Repo convention is **relative**; this is the floor underneath it. It applies even when the repo documents nothing. "Matches the neighbors" is not `clean` when the neighbors carry the smell — say both: matches convention, still smells.

Three rules bind it:

1. **Repo wins.** A documented repo standard beats the baseline. Where the repo endorses the shape, suppress the smell and cite the standard.
2. **Always a judgement call.** Emit as `possible <smell>` with the hunk quoted. Never a hard violation, never a blocker on its own.
3. **Skip what tooling enforces.** Linter/formatter territory is not a finding.

| Smell | Tell in the diff | Fix |
|---|---|---|
| Mysterious name | name does not reveal what it does or holds | rename; no honest name = the design is murky |
| Duplicated code | same logic shape in >1 hunk or file | extract the shape, call it from both |
| Feature envy | reaches into another object's data more than its own | move the method onto the data it envies |
| Data clumps | same few fields/params keep travelling together | bundle into one type, pass that |
| Primitive obsession | string/primitive standing in for a domain concept | give the concept its own small type |
| Repeated switches | same switch/if-cascade on the same type recurs | polymorphism, or one map both sites share |
| Shotgun surgery | one logical change forces scattered edits | gather what changes together into one module |
| Divergent change | one module edited for several unrelated reasons | split so each changes for one reason |
| Speculative generality | abstraction/params/hooks the spec never asked for | delete; inline back until a real need shows |
| Message chains | long `a.b().c().d()` the caller should not depend on | hide the walk behind one method on the first object |
| Middle man | mostly delegates onward | cut it, call the real target direct |
| Refused bequest | ignores or overrides most of what it inherits | drop inheritance, use composition |

Dim map: naming → C6 · duplication, clumps, primitive obsession, switches, chains, middle man, refused bequest → C7 · speculative generality → C4 · shotgun surgery, divergent change → C1.

A baseline smell caps its dim at 8 (minor). It reaches `major` only when it already caused a defect on a real path — then it is that lens's finding, not a smell.

Severity anchor — the rubric in `review.md` wins on conflict:

| Lens | blocker | major | minor |
|---|---|---|---|
| security | authz bypass · secret leak | unvalidated real input · race on shared state | hardening nit |
| biz | wrong money/data rule | wrong rule on a real path | edge nobody hits |
| perf · scale | unbounded growth that takes the system down | N+1 or missing timeout on a hot path | micro-cost |
| maintain · change-cost | — | one-way door · untestable seam | dup · placement nit |
| style · lang-fw | — | anti-pattern that hides a bug | naming · convention |

Also: happy/empty/replay · missing Must/false green (C5). Simulate a likely next change; if this shape would fight it → change-cost.

Tests **in** the diff are judged against `tdd.md`: unconfirmed seam · implementation-coupled · tautological → C5. A tautological test is `major`, not a nit — it passes by construction, so it is false green no matter what coverage says.
