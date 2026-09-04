# Review standard

Hunt then score. Deep required. One track, one %. Code is one card (technical + business).
Same bar always — `deep` / `เข้มงวด` is spawn, not a second rubric. Lenses: `review.deep.md`.

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

Legal dim scores: **0 4 6 8 10**. blocker / dim≤4 → FAIL · major → FAIL · ≥3 minors → FAIL  
**PASS** = L5 · scored dims ≥3 · ★ = 10 · no blocker/major · minors < 3  
No PASS WITH CONDITIONS. Accepting a leftover major is still FAIL.

Also FAIL: unread scope · silent ledger row · skipped required dim · `Assumed` on ★ · green tests without verify (code) · slogan docs (≤L2).

**10** = cited proof + zero findings on that dim.

Finding (else drop): path · track · why it hurts · one fix · severity.

## Severity

By consequence, not by dim. One finding, one severity. Unsure between two → take the higher.

| | code | artifact | general |
|---|---|---|---|
| **blocker** | data loss · auth bypass · secret leak · corruption · outage | wrong contract/decision — reader ships the wrong thing | stated as fact, actually invented |
| **major** | wrong behavior on a real path · contract violation · no safe workaround | missing decision or stale contract a cold reader trips on | cannot act; key step missing |
| **minor** | local quality; no behavior risk | nit: structure · link · wording | nit |

Cosmetic preference with no cited harm is not a finding — drop it.

```
ผล [code|artifact|general]: FAIL | PASS
Level: L5 — … (n/100)
Scope: n paths (locked) · profile lean|full
Ledger: n/n reported
Blockers: n · Majors: n · Minors: n
```

Then scores · must-fix · solid. Ship uses **code** PASS only.
