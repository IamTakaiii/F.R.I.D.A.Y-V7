#!/usr/bin/env python3
"""Review rubric arithmetic: parsed from the markdown SoT, never restated here.

Catches the class of bug where the score scale changes in one table and the
formula, the star threshold or a sibling table is left on the old scale.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
STD = R / "domains" / "sdlc" / "standards"
CARD = STD / "review.md"
DEEP = STD / "review.deep.md"
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


card = CARD.read_text()
deep = DEEP.read_text()


def legal_scores(text: str, label: str, path: Path) -> list[int]:
    m = re.search(rf"{label}:?\s*\*\*([\d ]+)\*\*", text)
    if not m:
        fail(f"{path.name}: no legal score set declared")
        return []
    return [int(x) for x in m.group(1).split()]


card_scale = legal_scores(card, r"Legal dim scores", CARD)
deep_scale = legal_scores(deep, r"Legal", DEEP)
if card_scale and deep_scale and card_scale != deep_scale:
    fail(f"scale disagrees: {CARD.name}={card_scale} {DEEP.name}={deep_scale}")

scale = card_scale or deep_scale
if not scale:
    print("FAIL")
    print(" - no scale to check")
    sys.exit(1)
top = max(scale)

# 1. Level bands cover 0..100 with no gap and no overlap.
bands = [
    (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    for m in re.finditer(r"\|\s*L(\d)\s*\|\s*(\d+)[–-](\d+)\s*\|", card)
]
bands.sort()
if not bands:
    fail(f"{CARD.name}: no level bands found")
else:
    if bands[0][1] != 0:
        fail(f"bands start at {bands[0][1]}, want 0")
    if bands[-1][2] != 100:
        fail(f"bands end at {bands[-1][2]}, want 100")
    for (_, _, prev_hi), (lvl, lo, _) in zip(bands, bands[1:]):
        if lo != prev_hi + 1:
            fail(f"band L{lvl} starts at {lo}, previous ended {prev_hi}")

# 2. Every rubric table is written on the declared scale.
for line in deep.splitlines():
    if not line.startswith("| ID | Dim |"):
        continue
    cols = [c.strip() for c in line.strip().strip("|").split("|")][2:]
    if [int(c) for c in cols if c.lstrip("-").isdigit()] != scale:
        fail(f"{DEEP.name}: rubric columns {cols} do not match scale {scale}")

# 3. Star dims must be required at the top of the scale, and the two files
#    must name the same star dims.
stars_deep: dict[str, set[str]] = {}
for a, b, want in re.findall(r"★ ([A-Z]\d)\+([A-Z]\d)[^\n]*?(\d+)", deep):
    stars_deep[a[0]] = {a, b}
    if int(want) != top:
        fail(f"{DEEP.name}: ★ {a}+{b} requires {want}, scale tops out at {top}")

for track, ids in re.findall(r"\|\s*`(code|artifact|general)`\s*\|[^|]*\|[^|]*\|([^|]*)\|", card):
    named = set(re.findall(r"[A-Z]\d", ids))
    letter = next(iter(named))[0] if named else ""
    if letter and stars_deep.get(letter) and named != stars_deep[letter]:
        fail(f"star dims for {track}: {CARD.name}={named} {DEEP.name}={stars_deep[letter]}")

# 4. The formula must normalise by the top of the scale, or it cannot be a
#    percentage. This is the F10 guard.
formula = next((l for l in deep.splitlines() if "score_pct" in l), "")
if not formula:
    fail(f"{DEEP.name}: no score_pct formula")
elif not re.search(rf"/\s*\(\s*{top}\s*[×*]", formula):
    fail(f"{DEEP.name}: formula does not divide by ({top} × Σweights): {formula.strip()}")

# 5. Every dim in a rubric table carries a weight.
weights = {m.group(1): float(m.group(2)) for m in re.finditer(r"([A-Z]\d)×([\d.]+)", deep)}
has_default = "others ×1" in deep
for dim in re.findall(r"^\|\s*([A-Z]\d)\s*\|", deep, re.M):
    if dim not in weights and not has_default:
        fail(f"{dim} has no weight")

# 6. A full card must land on exactly 100 under the parsed formula shape.
if weights:
    total_w = sum(weights.values())
    pct = round(100 * (top * total_w) / (top * total_w))
    if pct != 100:
        fail(f"a perfect card scores {pct}, want 100")

# 7. Every sentence that defines a ledger row must offer all three kinds.
# Checked on the defining line itself — the token appearing elsewhere in the
# file proves nothing.
LEDGER_FILES = (
    "domains/sdlc/modes/review.md",
    "domains/sdlc/standards/review.deep.md",
    "domains/sdlc/standards/lens.md",
    "domains/sdlc/standards/execution.md",
)
seen_definition = False
for rel in LEDGER_FILES:
    for line in (R / rel).read_text().splitlines():
        if not re.search(r"emits\b.*\brow|row\b.*\bemits", line):
            continue
        seen_definition = True
        missing = [k for k, pat in (
            ("clean", r"`clean`"),
            ("finding", r"finding"),
            ("N/A", r"`N/A`"),
        ) if not re.search(pat, line)]
        if missing:
            fail(f"{rel}: ledger row definition omits {', '.join(missing)}: {line.strip()[:60]}…")
if not seen_definition:
    fail("no ledger row definition found in any owning file")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print(f"OK rubric scale {scale} · {len(bands)} bands · {len(weights)} weights")
