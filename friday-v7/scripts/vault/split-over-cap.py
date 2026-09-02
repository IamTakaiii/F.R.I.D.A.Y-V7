#!/usr/bin/env python3
"""Split over-cap vault cards. Mechanical: drop Reader map, peel ## into legal companions."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)

KEEP_DESIGN = {
    "executive decision",
    "problem",
    "success and scope",
    "decision",
    "verification plan",
    "doc history",
}
DROP = {"reader map", "artifact contract"}


def parse_fm(text: str) -> tuple[dict[str, str], str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}, "", text
    raw = m.group(1)
    out: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out, raw, text[m.end() :]


def sections(body: str) -> list[tuple[str, str]]:
    lines = body.splitlines(keepends=True)
    out: list[tuple[str, str]] = []
    title = ""
    buf: list[str] = []
    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            if buf or title:
                out.append((title, "".join(buf)))
            title = line[3:].strip()
            buf = [line]
        else:
            buf.append(line)
    if buf or title:
        out.append((title, "".join(buf)))
    return out


def classify_design(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ("contract", "api", "http", "error", "request", "response", "bundle", "published", "field")):
        return "contracts"
    if any(k in t for k in ("flow", "state", "picture", "pipeline", "publisher", "collaborat", "timeline event")):
        return "flow"
    if any(k in t for k in ("verif", "test", "quality", "approval", "safety", "failure")):
        return "quality"
    return "operations"


def dump(path: Path, fm_raw: str, body: str) -> None:
    path.write_text(f"---\n{fm_raw.strip()}\n---\n\n{body.lstrip()}", encoding="utf-8")


def set_key(fm_raw: str, key: str, value: str) -> str:
    if re.search(rf"^{key}:", fm_raw, re.M):
        return re.sub(rf"^{key}:.*$", f"{key}: {value}", fm_raw, count=1, flags=re.M)
    return fm_raw.rstrip() + f"\n{key}: {value}\n"


def lines_of(fm_raw: str, body: str) -> int:
    return (f"---\n{fm_raw.strip()}\n---\n\n{body}").count("\n") + 1


def split_design(path: Path, cap: int) -> None:
    text = path.read_text(encoding="utf-8")
    fm, fm_raw, body = parse_fm(text)
    kept: list[str] = []
    parts: dict[str, list[str]] = {k: [] for k in ("contracts", "flow", "quality", "operations")}
    for title, chunk in sections(body):
        key = title.lower()
        if key in DROP:
            continue
        if key in KEEP_DESIGN or not title:
            probe = "".join(kept + [chunk])
            if title and lines_of(fm_raw, probe) > cap and title not in KEEP_DESIGN:
                parts[classify_design(title)].append(chunk)
            else:
                kept.append(chunk)
            continue
        probe = "".join(kept + [chunk])
        if lines_of(fm_raw, probe) <= cap:
            kept.append(chunk)
        else:
            parts[classify_design(title)].append(chunk)
    used = []
    dest = path.parent / "design"
    for kind, chunks in parts.items():
        if not chunks:
            continue
        dest.mkdir(exist_ok=True)
        part = dest / f"{kind}.md"
        pfm = (
            f"type: design-part\n"
            f"id: {fm.get('id', path.stem)}.part.{kind}\n"
            f"project: {fm.get('project', '')}\n"
            f"created: {fm.get('created', '')}\n"
            f"updated: {fm.get('updated', '')}\n"
            f"status: current\nrev: 1\nlifecycle: delivery\ntags: []\n"
            f"standard: 7\nmax_lines: 120\nparts: []\n"
            f"feature: {fm.get('feature', '')}\n"
            f"feature_id: {fm.get('feature_id', '')}\n"
            f"depends_on: []\npart_kind: {kind}\n"
        )
        extra = "".join(chunks)
        if part.exists():
            _pfm, pfm_raw, pbody = parse_fm(part.read_text(encoding="utf-8"))
            dump(part, pfm_raw, pbody.rstrip() + "\n\n" + extra)
        else:
            dump(part, pfm, f"# Design part — {kind}\n\n## Owner\n\n[[../design]]\n\n## Content\n\n{extra}")
        used.append(f"  - kind: {kind}\n    path: design/{kind}.md")
    if used:
        fm_raw = set_key(fm_raw, "parts", "\n" + "\n".join(used))
        if "## Parts" not in "".join(kept):
            kept.append("\n## Parts\n\n" + "\n".join(f"- {k}: design/{k}.md" for k in parts if parts[k]) + "\n")
    dump(path, fm_raw, "".join(kept))


def split_architecture(path: Path, cap: int) -> None:
    text = path.read_text(encoding="utf-8")
    fm, fm_raw, body = parse_fm(text)
    kept: list[str] = []
    overflow: list[str] = []
    for title, chunk in sections(body):
        if title.lower() in DROP:
            continue
        probe = "".join(kept + [chunk])
        if not overflow and lines_of(fm_raw, probe) <= cap:
            kept.append(chunk)
        else:
            overflow.append(chunk)
    dump(path, fm_raw, "".join(kept))
    if not overflow:
        return
    stack = path.with_name("stack.md")
    extra = "".join(overflow)
    if stack.exists():
        _sfm, sraw, sbody = parse_fm(stack.read_text(encoding="utf-8"))
        dump(stack, sraw, sbody.rstrip() + "\n\n" + extra)
    else:
        dump(
            stack,
            "type: architecture-part\nid: arch.stack\nproject: {}\ncreated: {}\nupdated: {}\nstatus: current\nrev: 1\nlifecycle: delivery\ntags: []\nstandard: 7\nmax_lines: 120\nparts: []\npart_kind: stack\n".format(
                fm.get("project", ""), fm.get("created", ""), fm.get("updated", "")
            ),
            "# Architecture part — stack\n\n## Owner\n\n[[01 - Architecture]]\n\n## Content\n\n" + extra,
        )


def strip_drop_sections(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    fm, fm_raw, body = parse_fm(text)
    if not fm:
        return
    new = []
    for title, chunk in sections(body):
        if title.lower() in DROP:
            continue
        # fix leftover v6 wikilinks
        chunk = chunk.replace("/02 - Design", "/design").replace("/01 - Intent", "/intent").replace("/03 - TODO", "/queue")
        chunk = chunk.replace("02 - Design|", "design|").replace("01 - Intent|", "intent|")
        new.append(chunk)
    dump(path, fm_raw, "".join(new))


def move_presence(vault: Path) -> None:
    src = vault / "20 - Projects/10 - Software/01 - Kraken/01 - Architecture/02 - Presence.md"
    if not src.is_file():
        return
    dest = vault / "20 - Projects/10 - Software/01 - Kraken/02 - Decisions/ADR-10 - Presence Redis TTL.md"
    text = src.read_text(encoding="utf-8")
    fm, fm_raw, body = parse_fm(text)
    fm_raw = set_key(fm_raw, "type", "adr")
    fm_raw = set_key(fm_raw, "lifecycle", "decision")
    dest.write_text(f"---\n{fm_raw.strip()}\n---\n\n{body.lstrip()}", encoding="utf-8")
    src.unlink()
    arch = vault / "20 - Projects/10 - Software/01 - Kraken/01 - Architecture/01 - Architecture.md"
    if arch.is_file():
        a = arch.read_text(encoding="utf-8")
        if "ADR-10" not in a:
            arch.write_text(a.rstrip() + "\n\n## Presence\n\n[[ADR-10 - Presence Redis TTL]]\n", encoding="utf-8")


def retarget_work_design_parts(projects: Path) -> None:
    for p in projects.rglob("work/*.md"):
        fm, fm_raw, body = parse_fm(p.read_text(encoding="utf-8"))
        if fm.get("type") != "design-part":
            continue
        fm_raw = set_key(fm_raw, "type", "work-item")
        fm_raw = set_key(fm_raw, "max_lines", "120")
        dump(p, fm_raw, body)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    args = ap.parse_args()
    vault = Path(args.vault)
    projects = vault / "20 - Projects"
    move_presence(vault)
    retarget_work_design_parts(projects)
    for p in list(projects.rglob("*.md")):
        if p.name.startswith("."):
            continue
        strip_drop_sections(p)
    for p in list(projects.rglob("*.md")):
        fm, _, _ = parse_fm(p.read_text(encoding="utf-8"))
        typ = fm.get("type")
        cap = int(fm["max_lines"]) if fm.get("max_lines", "").isdigit() else 80
        n = p.read_text(encoding="utf-8").count("\n") + 1
        if n <= cap:
            continue
        if typ == "design":
            split_design(p, 120)
        elif typ == "architecture":
            split_architecture(p, cap)
        # other types: never stem - Heading.md; compress or fail per schema/artifact.md


if __name__ == "__main__":
    main()
