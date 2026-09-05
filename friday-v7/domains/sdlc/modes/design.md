# SDLC — design

One counsel beat per turn. Picture-first (`kernel/thinking/clarity.md`).
Writes: write-gate. Paths: `schema/placement.md` — do not restate them here.

**Chat ≠ Design.** No vault file (or explicit skip) = not done.

New folder? `feature-identity.md` first. Absorb/extend. Duplicates → consolidate.

## When to load

Counsel + Feature List + Arch (if any) + **`design.grill.md`** on enter. **`design.deep.md` at Capture** — earlier only if HTTP/data/async/security/scale or `ละเอียด`.

## Run

| Phase | Do | Stop until |
|---|---|---|
| Grill | `design.grill.md`. Frontier rounds — numbered questions, each with a recommended answer. Facts are yours to find, decisions are the user's. No design yet. | Frontier empty · floor closed · no open blocker · close card echoed or amended by the user. |
| Decide | Outcome · evidence (Unknown/Assumed) · ≥2 options + pick · stress the pick. Tier L or irreversible → offer `design.twice.md` first. | User names the lock in one line (not `โอเค`). Mismatch → back to Grill. Do not dump the whole column. |
| Capture | Deep if missing. Outline *applicable* sections → `a` → Intent then Design from type templates. HTTP → `api/` pages. Over cap → split `design/*` parts. Same package: Feature List SoT (`allow.md` + write-gate). | File exists, listed, or skip + reason. |
| Queue | 1–5 `next`/`ready` (id · DoD) or skip reason | Cited in Artifacts |

Opinion-only if the user asked — then offer Capture.

**Panel:** offer once at Decide — `skip` or N (2–5). Accepted → `modes/panel.md`, then return here. Panel does not lock.

## Lock

Cold implementer does not invent contract, safety, capacity, deploy, or recovery.
Any open blocker row in `design.grill.md` → **no lock**.
Any **required** lens that fails its must-checks in `design.deep.md` → **no lock**.
Critical unknown → counsel / ADR / research. Omit N/A sections — do not fake them.
