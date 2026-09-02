#!/usr/bin/env python3
"""Every type template must share the same frontmatter + history contract."""
from __future__ import annotations

import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REQUIRED = (
    "type",
    "id",
    "project",
    "created",
    "updated",
    "status",
    "rev",
    "lifecycle",
    "tags",
    "standard",
    "max_lines",
    "parts",
)
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def parse_fm(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


for path in sorted((R / "schema" / "types").rglob("*.md")):
    text = path.read_text()
    fm = parse_fm(text)
    stem = path.stem
    if fm.get("type") != stem:
        fail(f"{path.name}: type {fm.get('type')!r} != {stem}")
    for key in REQUIRED:
        if key not in fm:
            fail(f"{path.name}: missing {key}")
    if fm.get("standard") != "7":
        fail(f"{path.name}: standard {fm.get('standard')!r}")
    want_cap = "0" if stem in {"timeline-log", "memory-lesson"} else "200"
    if fm.get("max_lines") != want_cap:
        fail(f"{path.name}: max_lines {fm.get('max_lines')!r} want {want_cap}")
    if "## Doc history" not in text:
        fail(f"{path.name}: no Doc history")
    if "## Links" not in text:
        fail(f"{path.name}: no Links")
    if "load_profile" in fm or "doc_status" in fm:
        fail(f"{path.name}: retired frontmatter key")
    if re.search(r"^> Placement", text, re.M) or "Split via `schema" in text:
        fail(f"{path.name}: agent placement leaked into template body")
    if "<!-- fill:" not in text:
        fail(f"{path.name}: missing <!-- fill: --> contract")

for name in ("write-gate.md", "placement.md", "artifact.md", "types.md", "vault.md", "allow.md"):
    if not (R / "schema" / name).is_file():
        fail(f"missing schema/{name}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print("OK", "type templates share frontmatter contract")
