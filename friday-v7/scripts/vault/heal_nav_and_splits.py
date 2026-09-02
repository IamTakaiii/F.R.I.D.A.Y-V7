#!/usr/bin/env python3
"""Merge stem - Heading.md siblings into the parent card and add ## Links."""
from __future__ import annotations

import argparse
import os
import re
from collections import defaultdict
from pathlib import Path

SPLIT_RE = re.compile(r"^## Split\s*$", re.M)
OWNER_RE = re.compile(r"^## Owner\s*$", re.M)
LINKS_RE = re.compile(r"^## Links\s*$", re.M)
HISTORY_RE = re.compile(r"^## Doc history\s*$", re.M)
STUB_RE = re.compile(
    r"see the canonical design and existing plan detail for this concern",
    re.I,
)
DUMP_MARKERS = (
    "\n# Design —",
    "\n# System Architecture",
    "\n# Architecture —",
    "\n# Intent —",
)
CAP_BY_TYPE = {
    "queue": 80,
    "feature-list": 80,
    "api": 160,
    "quality-report": 160,
    "feature-plan": 160,
    "design": 120,
    "design-part": 120,
    "architecture-part": 120,
}
DEFAULT_CAP = 120


def parse_fm(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---"):
        return {}, "", text
    rest = text[3:]
    if rest.startswith("\n"):
        rest = rest[1:]
    end = rest.find("\n---")
    if end < 0:
        return {}, "", text
    raw = rest[:end]
    body = rest[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    fm: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, raw, body


def render(fm_raw: str, body: str) -> str:
    return f"---\n{fm_raw.strip()}\n---\n\n{body.lstrip()}"


def nlines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def set_key(fm_raw: str, key: str, value: str) -> str:
    if re.search(rf"^{key}:", fm_raw, re.M):
        return re.sub(rf"^{key}:.*$", f"{key}: {value}", fm_raw, count=1, flags=re.M)
    return fm_raw.rstrip() + f"\n{key}: {value}\n"


def cap_for(typ: str, fm: dict[str, str]) -> int:
    want = CAP_BY_TYPE.get(typ, DEFAULT_CAP)
    cur = int(fm["max_lines"]) if fm.get("max_lines", "").isdigit() else want
    return max(want, cur) if typ in {"queue", "feature-list"} else want


def parent_of(path: Path) -> Path | None:
    if " - " not in path.stem:
        return None
    parent = path.with_name(path.stem.rsplit(" - ", 1)[0] + ".md")
    if parent.is_file() and parent != path:
        return parent
    return None


def root_of(path: Path) -> Path:
    seen: set[Path] = set()
    while path not in seen:
        seen.add(path)
        p = parent_of(path)
        if not p:
            return path
        path = p
    return path


def strip_split(body: str) -> str:
    return SPLIT_RE.split(body)[0].rstrip() + "\n"


def strip_dump(body: str, typ: str) -> str:
    if typ in {"design", "architecture", "intent"}:
        return body
    for marker in DUMP_MARKERS:
        if marker in body:
            body = body.split(marker, 1)[0]
    return body.rstrip() + "\n"


def is_stub(body: str) -> bool:
    rest = strip_split(body)
    rest = re.sub(r"^#+\s+.*$", "", rest, flags=re.M)
    rest = re.sub(r"\[\[.*?\]\]", "", rest)
    rest = re.sub(r"\s+", " ", rest).strip()
    if not rest:
        return True
    return bool(STUB_RE.fullmatch(rest.lower().rstrip(".")))


def unique_body(paths: list[Path], typ: str) -> str:
    chunks: list[str] = []
    seen: set[str] = set()
    for p in paths:
        if not p.is_file():
            continue
        _fm, _raw, body = parse_fm(p.read_text(encoding="utf-8", errors="replace"))
        body = strip_dump(strip_split(body), typ)
        if is_stub(body):
            continue
        norm = re.sub(r"\s+", " ", body).strip()
        if not norm or norm in seen:
            continue
        seen.add(norm)
        chunks.append(body.strip())
    return "\n\n".join(chunks).rstrip() + "\n"


def trim_history(body: str, keep: int = 5) -> str:
    m = HISTORY_RE.search(body)
    if not m:
        return body
    head, hist = body[: m.start()], body[m.start() :]
    lines = hist.splitlines()
    rows = [ln for ln in lines if ln.startswith("|") and not re.match(r"^\|[\s:-]+\|\s*$", ln)]
    header = [ln for ln in lines if ln.startswith("|")][:2]
    data = [ln for ln in rows if ln not in header][-keep:]
    return head.rstrip() + "\n\n## Doc history\n\n" + "\n".join(header + data) + "\n"


def wikilink(src: Path, dest: Path) -> str:
    rel = os.path.relpath(dest.with_suffix(""), src.parent)
    text = rel.replace("\\", "/")
    if text.startswith("./"):
        text = text[2:]
    return f"[[{text}]]"


def feature_folder(path: Path) -> Path | None:
    for parent in path.parents:
        if parent.parent.name == "03 - Features":
            return parent
    return None


def existing(folder: Path, name: str) -> Path | None:
    p = folder / name
    return p if p.is_file() else None


def standard_links(path: Path) -> list[str]:
    feat = feature_folder(path)
    bullets: list[str] = []
    if feat:
        cores = []
        for name in ("intent.md", "design.md", "queue.md"):
            hit = existing(feat, name)
            if hit and hit != path:
                cores.append(wikilink(path, hit))
        if cores:
            bullets.append("- " + " · ".join(cores))
        api_dir = feat / "api"
        if api_dir.is_dir():
            apis = [wikilink(path, p) for p in sorted(api_dir.glob("*.md")) if parent_of(p) is None and p != path]
            if apis:
                bullets.append("- API: " + " · ".join(apis[:6]))
        plans = feat / "plans"
        if plans.is_dir():
            items = [wikilink(path, p) for p in sorted(plans.glob("*.md")) if parent_of(p) is None and p != path]
            if items:
                bullets.append("- Plan: " + " · ".join(items[:4]))
        reports = feat / "reports"
        if reports.is_dir():
            items = [wikilink(path, p) for p in sorted(reports.glob("*.md")) if parent_of(p) is None and p != path]
            if items:
                bullets.append("- Reports: " + " · ".join(items[:4]))
        design_dir = feat / "design"
        if design_dir.is_dir() and path.name == "design.md":
            parts = []
            for kind in ("contracts", "flow", "quality", "operations"):
                hit = existing(design_dir, f"{kind}.md")
                if hit:
                    parts.append(wikilink(path, hit))
            if parts:
                bullets.append("- Parts: " + " · ".join(parts))
        if path.parent == design_dir:
            card = existing(feat, "design.md")
            if card:
                bullets = [f"- Card: {wikilink(path, card)}"] + bullets
        return bullets

    # project overview / architecture
    for parent in path.parents:
        if (parent / "00 - Overview").is_dir() and parent.parent.name in {"10 - Software", "20 - Personal"}:
            project = parent
            break
    else:
        return bullets
    overview = project / "00 - Overview"
    arch = project / "01 - Architecture" / "01 - Architecture.md"
    brief = overview / "01 - Brief.md"
    fl = overview / "02 - Feature List.md"
    if path.name == "01 - Brief.md" and fl.is_file():
        bullets.append(f"- {wikilink(path, fl)}")
        if arch.is_file():
            bullets[-1] += f" · {wikilink(path, arch)}"
    elif path.name == "02 - Feature List.md":
        bits = []
        if brief.is_file():
            bits.append(wikilink(path, brief))
        if arch.is_file():
            bits.append(wikilink(path, arch))
        if bits:
            bullets.append("- " + " · ".join(bits))
    elif path.name == "01 - Architecture.md":
        bits = []
        if brief.is_file():
            bits.append(wikilink(path, brief))
        if fl.is_file():
            bits.append(wikilink(path, fl))
        stack = path.with_name("stack.md")
        if stack.is_file():
            bits.append(wikilink(path, stack))
        if bits:
            bullets.append("- " + " · ".join(bits))
    elif path.parent.name == "02 - Decisions" and arch.is_file():
        bullets.append(f"- {wikilink(path, arch)}")
    elif path.name == "stack.md" and arch.is_file():
        bullets.append(f"- Card: {wikilink(path, arch)}")
    return bullets


def upsert_links(body: str, bullets: list[str]) -> str:
    if not bullets:
        return body
    block = "## Links\n\n" + "\n".join(bullets) + "\n"
    if LINKS_RE.search(body):
        parts = LINKS_RE.split(body, maxsplit=1)
        rest = parts[1]
        nxt = re.search(r"^## ", rest, re.M)
        after = rest[nxt.start() :] if nxt else ""
        return parts[0].rstrip() + "\n\n" + block + ("\n" + after.lstrip() if after else "")
    if OWNER_RE.search(body) and not LINKS_RE.search(body):
        body = OWNER_RE.sub("## Links", body, count=1)
        if LINKS_RE.search(body):
            return upsert_links(body, bullets)
    if HISTORY_RE.search(body):
        return HISTORY_RE.sub(block + "\n## Doc history", body, count=1)
    return body.rstrip() + "\n\n" + block


def upsert_parts(body: str, path: Path) -> str:
    if path.name != "design.md":
        return body
    feat = feature_folder(path)
    if not feat:
        return body
    rows = []
    for kind in ("contracts", "flow", "quality", "operations"):
        hit = existing(feat / "design", f"{kind}.md")
        if hit:
            rows.append(f"| {kind} | {wikilink(path, hit)} |")
    if not rows:
        return body
    table = "## Parts\n\n| Kind | Path |\n|---|---|\n" + "\n".join(rows) + "\n"
    if re.search(r"^## Parts\s*$", body, re.M):
        return body
    if LINKS_RE.search(body):
        return LINKS_RE.sub(table + "\n## Links", body, count=1)
    if HISTORY_RE.search(body):
        return HISTORY_RE.sub(table + "\n## Doc history", body, count=1)
    return body.rstrip() + "\n\n" + table


def merge_family(root: Path, members: list[Path], dry: bool) -> tuple[int, list[Path]]:
    text = root.read_text(encoding="utf-8", errors="replace")
    fm, fm_raw, _ = parse_fm(text)
    typ = fm.get("type", "")
    ordered = [root] + [p for p in sorted(members) if p != root]
    body = unique_body(ordered, typ)
    body = trim_history(body)
    fm_raw = set_key(fm_raw, "max_lines", str(CAP_BY_TYPE.get(typ, DEFAULT_CAP)))
    fm_raw = set_key(fm_raw, "updated", "2026-09-02")
    out = render(fm_raw, body)
    deleted = [p for p in members if p != root]
    if not dry:
        root.write_text(out, encoding="utf-8")
        for p in deleted:
            p.unlink(missing_ok=True)
    return nlines(out), deleted


def iter_roots(vault: Path) -> list[Path]:
    roots = []
    software = vault / "20 - Projects" / "10 - Software"
    personal = vault / "20 - Projects" / "20 - Personal"
    if software.is_dir():
        roots.extend(sorted(p for p in software.iterdir() if p.is_dir()))
    if personal.is_dir():
        roots.extend(sorted(p for p in personal.iterdir() if p.is_dir()))
    return roots


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    vault = Path(args.vault)
    families: dict[Path, list[Path]] = defaultdict(list)
    typed: list[Path] = []
    for project in iter_roots(vault):
        for p in project.rglob("*.md"):
            if any(part.startswith(".") for part in p.parts):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            if not text.startswith("---"):
                continue
            typed.append(p)
            root = root_of(p)
            if root != p:
                families[root].append(p)
                families[root]  # ensure
            families.setdefault(root, [])
            if p not in families[root]:
                families[root].append(p)

    merged = 0
    deleted_n = 0
    over: list[str] = []
    for root, members in sorted(families.items(), key=lambda kv: str(kv[0])):
        kids = [p for p in members if p != root]
        if not kids or not root.is_file():
            continue
        n, deleted = merge_family(root, [root] + kids, args.dry_run)
        merged += 1
        deleted_n += len(deleted)
        fm = parse_fm(root.read_text(encoding="utf-8", errors="replace") if not args.dry_run else root.read_text(encoding="utf-8", errors="replace"))[0]
        cap = cap_for(fm.get("type", ""), fm)
        if n > cap:
            over.append(f"{n}/{cap} {root}")

    linked = 0
    scan = []
    for project in iter_roots(vault):
        scan.extend(project.rglob("*.md"))
    for p in scan:
        if any(part.startswith(".") for part in p.parts):
            continue
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        if parent_of(p) is not None:
            continue
        fm, fm_raw, body = parse_fm(text)
        if not fm.get("type"):
            continue
        bullets = standard_links(p)
        new_body = upsert_parts(body, p)
        new_body = upsert_links(new_body, bullets)
        if new_body == body:
            continue
        linked += 1
        if not args.dry_run:
            p.write_text(render(fm_raw, new_body), encoding="utf-8")

    print(f"families merged {merged}; siblings deleted {deleted_n}; links upserted {linked}; dry={args.dry_run}")
    print(f"over cap after merge: {len(over)}")
    for row in over[:40]:
        print(" ", row)


if __name__ == "__main__":
    main()
