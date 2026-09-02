# Review standard

Hunt then score. Deep required. One track, one %. Code is one card (technical + business).

| Track | Scope | Rubric | ★ |
|---|---|---|---|
| `code` | source / PR | C1–C7 · C8 if behavior changed | C2 C3 |
| `artifact` | Design ADR Arch Intent API queue work-item Ship | T1–T8 | T2 T3 |
| `general` | brief / life / note / research | G1–G6 | G2 G3 |

Path names the track. Do not add a track “to be safe.” Folder → separate cards, not a merge.

## Score

| Level | % | |
|---|---|---|
| L1 | 0–39 | FAIL |
| L2 | 40–59 | FAIL |
| L3 | 60–79 | FAIL |
| L4 | 80–94 | FAIL |
| L5 | 95–100 | Eligible only if gates below hold |

blocker / dim≤2 → FAIL · major → FAIL · ≥3 minors → FAIL  
**PASS** = L5 · scored dims ≥3 · ★ = 4 · no blocker/major · minors < 3  
No PASS WITH CONDITIONS. Accepting a leftover major is still FAIL.

Also FAIL: unread scope · skipped required dim · `Assumed` on ★ · green tests without verify (code) · slogan docs (≤L2).

**4** = cited proof + zero findings on that dim.

Finding (else drop): path · track · why it hurts · one fix · severity.

```
ผล [code|artifact|general]: FAIL | PASS
Level: L5 — … (n/100)
Blockers: n · Majors: n · Minors: n
```

Then scores · must-fix · solid. Ship uses **code** PASS only.
