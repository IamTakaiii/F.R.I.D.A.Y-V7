#!/usr/bin/env python3
"""Every registered type is allowed somewhere; every allow token is registered."""
from __future__ import annotations

import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SPECIAL = {"none", "promote", "patch", "—", "-"}
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


registered = {p.stem for p in (R / "schema" / "types").rglob("*.md")}

allow_text = (R / "schema" / "allow.md").read_text()
allowed: set[str] = set()
for line in allow_text.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 3 or cells[0] in {"Mode", "---"} or cells[0].startswith("---"):
        continue
    for tok in re.split(r"[,/]", cells[2]):
        t = tok.strip().strip("`")
        if not t or t in SPECIAL or t.startswith("/"):
            continue
        allowed.add(t)

for t in sorted(allowed - registered):
    fail(f"allow.md unknown type: {t}")
for t in sorted(registered - allowed):
    fail(f"type never allowed: {t}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print("OK", f"{len(registered)} types allowed")
