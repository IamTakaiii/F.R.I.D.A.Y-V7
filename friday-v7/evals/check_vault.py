#!/usr/bin/env python3
"""Check a live vault (optional). No vault → skip 0."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REGISTERED = {p.stem for p in (R / "schema" / "types").rglob("*.md")}
NAME_HINT = {
    "intent": "intent.md",
    "design": "design.md",
    "queue": "queue.md",
    "architecture": "01 - Architecture.md",
    "feature-list": "Feature List.md",
}


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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--vault", default=os.environ.get("FRIDAY_BRAIN_ROOT", ""))
    args = p.parse_args()
    root = Path(args.vault).expanduser() if args.vault else None
    if not root or not root.is_dir():
        print("SKIP no vault (set FRIDAY_BRAIN_ROOT or --vault)")
        return 0

    errors: list[str] = []
    for path in root.rglob("*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        text = path.read_text(errors="replace")
        if not text.startswith("---"):
            continue
        fm = parse_fm(text)
        typ = fm.get("type")
        if not typ:
            continue
        rel = str(path.relative_to(root))
        if typ not in REGISTERED:
            errors.append(f"{rel}: unregistered type {typ}")
            continue
        if "<!-- fill:" in text or re.search(r"^> Placement", text, re.M):
            errors.append(f"{rel}: template leak")
        if "[[.]]" in text:
            errors.append(f"{rel}: [[.]] wikilink")
        if " - " in path.stem:
            parent = path.with_name(path.stem.rsplit(" - ", 1)[0] + ".md")
            if parent.is_file():
                errors.append(f"{rel}: heading sibling of {parent.name}")
        cap = fm.get("max_lines")
        log_uncap = typ in {"timeline-log", "memory-lesson"} or "/90 - Log/" in rel.replace("\\", "/")
        if log_uncap:
            cap = "0"
        if cap and cap.isdigit() and int(cap) > 0:
            body = re.sub(r"^---\n.*?\n---\n?", "", text, count=1, flags=re.S)
            body = re.sub(r"^## Links\n.*?(?=^## |\Z)", "", body, flags=re.S | re.M)
            body = re.sub(r"^## Doc history\n.*?(?=^## |\Z)", "", body, flags=re.S | re.M)
            n = body.count("\n") + (0 if body.endswith("\n") else 1)
            if n > int(cap):
                errors.append(f"{rel}: over cap {n}/{cap} (body)")
        hint = NAME_HINT.get(typ)
        if hint and path.name != hint and hint not in path.name:
            errors.append(f"{rel}: type {typ} unexpected filename")

    for design in root.glob("**/03 - Features/*/design.md"):
        project = design.parents[2]
        listing = project / "00 - Overview" / "02 - Feature List.md"
        token = design.parent.name
        slug = token.split(" - ", 1)[-1]
        if not listing.is_file():
            errors.append(f"{design.relative_to(root)}: missing Feature List")
        elif slug not in listing.read_text(errors="replace") and token not in listing.read_text(
            errors="replace"
        ):
            errors.append(f"{design.relative_to(root)}: orphan — not on Feature List")

    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("OK vault", root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
