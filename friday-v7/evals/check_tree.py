#!/usr/bin/env python3
"""Sanity: registry, caps, placement constants."""
from __future__ import annotations

import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


reg: set[str] = set()
for p in R.glob("domains/*/plugin.json"):
    data = json.loads(p.read_text())
    for s in data.get("surfaces", []):
        reg.add(s.lstrip("/"))

sur = {x.name for x in (R / "surfaces").iterdir() if (x / "SKILL.md").exists()}
if reg != sur:
    fail(f"registry mismatch extra={sur - reg} missing={reg - sur}")

cmd_dir = R / "hosts" / "opencode" / "commands"
cmd = {p.stem for p in cmd_dir.glob("*.md")} if cmd_dir.is_dir() else set()
if cmd != sur:
    fail(f"opencode commands mismatch extra={cmd - sur} missing={sur - cmd}")
for name in cmd:
    n = len((cmd_dir / f"{name}.md").read_text().splitlines())
    if n > 12:
        fail(f"fat command stub {name}: {n} lines")

for name in sur:
    lines = len((R / "surfaces" / name / "SKILL.md").read_text().splitlines())
    if lines > 25:
        fail(f"fat surface {name}: {lines} lines")

parent = len((R / "SKILL.md").read_text().splitlines())
if parent > 80:
    fail(f"parent SKILL.md {parent} > 80")

types = json.loads((R / "evals" / "behavior.json").read_text())
for retired in types["retired"]:
    if list((R / "schema" / "types").rglob(f"{retired}.md")):
        fail(f"retired type file still present: {retired}")

required = [
    "schema/types/software/intent.md",
    "schema/types/software/design.md",
    "schema/types/software/quality-report.md",
    "schema/types/software/brief.md",
    "schema/types/shared/timeline-log.md",
    "schema/vault.md",
    "schema/artifact.md",
    "schema/types.md",
    "schema/placement.md",
    "schema/write-gate.md",
    "schema/allow.md",
]
for rel in required:
    if not (R / rel).is_file():
        fail(f"missing {rel}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)

import subprocess

for script in ("check_schema.py", "check_allow.py", "check_vault.py"):
    ran = subprocess.run([sys.executable, str(R / "evals" / script)], check=False)
    if ran.returncode != 0:
        sys.exit(ran.returncode)
print("OK", f"{len(sur)} surfaces", "schema folders software/personal/shared")
