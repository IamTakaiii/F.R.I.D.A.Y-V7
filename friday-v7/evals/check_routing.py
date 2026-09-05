#!/usr/bin/env python3
"""Verify the routing registry covers every mode and its evidence examples."""
from __future__ import annotations

import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "routing"))
from route import route  # noqa: E402

registry = json.loads((R / "routing" / "registry.json").read_text(encoding="utf-8"))
errors: list[str] = []

registered: set[str] = set()
surfaces: set[str] = set()
for path in R.glob("domains/*/plugin.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    domain = path.parent.name
    surfaces.update(data.get("surfaces", []))
    registered.update(
        f"{domain}.{item.removeprefix('mode.').replace('_', '-')}"
        for item in data.get("provides", [])
        if item.startswith("mode.")
    )

routes = registry["routes"]
route_ids = {item["id"] for item in routes}
if route_ids != registered:
    errors.append(f"route coverage extra={route_ids - registered} missing={registered - route_ids}")

if any("examples" in item for item in routes):
    errors.append("registry.json must not carry examples; they live in evals/routing-examples.json")

example_data = json.loads((R / "evals" / "routing-examples.json").read_text(encoding="utf-8"))
examples = example_data["examples"]
if set(examples) != route_ids:
    errors.append(
        f"example coverage extra={set(examples) - route_ids} missing={route_ids - set(examples)}"
    )

for item in routes:
    if item["surface"] not in surfaces:
        errors.append(f"{item['id']}: unknown surface {item['surface']}")
    if not item.get("positive"):
        errors.append(f"{item['id']}: no positive evidence")
    owned = examples.get(item["id"], [])
    if len(owned) < 3:
        errors.append(f"{item['id']}: needs direct + natural + contrast examples")
    for example in owned:
        result = route(example, registry)
        winner = result["winner"]
        if winner is None or winner["id"] != item["id"]:
            got = [candidate["id"] for candidate in result["candidates"]] or ["fallback"]
            errors.append(f"{item['id']}: {example!r} -> {got}")
    for alias in item["aliases"]:
        command = alias.split()[0].lstrip("/")
        if command in {surface.lstrip("/") for surface in surfaces}:
            continue
        stub = R / "hosts" / "opencode" / "commands" / f"{command}.md"
        body = stub.read_text(encoding="utf-8") if stub.is_file() else ""
        surface_path = f"surfaces/{item['surface'].lstrip('/')}/SKILL.md"
        mode = item["id"].split(".", 1)[1]
        if surface_path not in body or mode not in body:
            errors.append(f"{item['id']}: alias /{command} does not dispatch to {item['surface']} {mode}")

case_data = json.loads((R / "evals" / "routing.json").read_text(encoding="utf-8"))
for case in case_data["cases"]:
    result = route(case["q"], registry)
    winner = result["winner"]
    if winner is None or winner["id"] != f"{case['domain']}.{case['mode']}":
        got = [candidate["id"] for candidate in result["candidates"]] or ["fallback"]
        errors.append(f"case {case['q']!r} -> {got}")

confidence_cases = {
    "/fr ช่วย reproduce แล้วหา root cause ของบั๊กนี้": "high",
    "triage issue status and review code diff": "medium",
    "/fr ช่วยหน่อยเรื่องหนึ่ง": "low",
}
for prompt, expected in confidence_cases.items():
    actual = route(prompt, registry)["confidence"]
    if actual != expected:
        errors.append(f"confidence {prompt!r}: expected {expected}, got {actual}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    raise SystemExit(1)

total = sum(len(v) for v in examples.values())
print(
    f"OK {len(routes)} modes · {total} examples routed by evidence "
    f"· {len(case_data['cases'])} adversarial cases"
)
