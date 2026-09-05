#!/usr/bin/env python3
"""Deterministic registry check and routing aid; the LLM uses the same evidence rules."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REGISTRY = Path(__file__).with_name("registry.json")


def normalize(text: str) -> str:
    return " ".join(text.casefold().strip().split())


def route(prompt: str, registry: dict | None = None) -> dict:
    data = registry or json.loads(REGISTRY.read_text(encoding="utf-8"))
    text = normalize(prompt)
    scoring = data["scoring"]

    for item in data["routes"]:
        if text in {normalize(example) for example in item.get("examples", [])}:
            return {"confidence": "high", "winner": item, "candidates": [item]}

    surfaces = {normalize(item["surface"]) for item in data["routes"]}
    aliases = []
    for item in data["routes"]:
        for alias in item["aliases"]:
            value = normalize(alias)
            first = value.split()[0]
            if text == value or (
                text.startswith(value + " ") and (value != first or first not in surfaces)
            ):
                aliases.append((len(value), item))
    if aliases:
        _, winner = max(aliases, key=lambda pair: pair[0])
        return {"confidence": "high", "winner": winner, "candidates": [winner]}

    scoped_surface = None
    for surface in sorted(surfaces, key=len, reverse=True):
        if text.startswith(surface + " "):
            text = text[len(surface) + 1 :]
            scoped_surface = None if surface == "/fr" else surface
            break

    candidates = [
        item for item in data["routes"]
        if scoped_surface is None or normalize(item["surface"]) == scoped_surface
    ]
    ranked = []
    for item in candidates:
        score = sum(scoring["positive"] for phrase in item["positive"] if normalize(phrase) in text)
        score += sum(scoring["negative"] for phrase in item["negative"] if normalize(phrase) in text)
        if score > 0:
            ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    if not ranked:
        return {"confidence": "low", "winner": None, "candidates": []}

    top = ranked[0][0]
    leaders = [item for score, item in ranked if score == top]
    confidence = "high" if top >= scoring["high"] and len(leaders) == 1 else "medium"
    return {"confidence": confidence, "winner": leaders[0] if len(leaders) == 1 else None, "candidates": leaders}


if __name__ == "__main__":
    result = route(" ".join(sys.argv[1:]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
