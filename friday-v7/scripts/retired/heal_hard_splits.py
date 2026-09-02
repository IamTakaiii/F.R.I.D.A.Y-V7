#!/usr/bin/env python3
"""Rejoin Kraken/RoamPouch hard-cuts at heading/table boundaries. No invented copy."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
SPLIT_RE = re.compile(r"^## Split\s*$", re.M)
LINK_RE = re.compile(r"\[\[([^\]|#]+)\]\]")
FAMILY_TAIL = re.compile(r" - (\d+|more-\d+|x\d+|Split)$")
KEEP_DESIGN = {
    "executive decision",
    "problem",
    "success and scope",
    "decision",
    "verification plan",
    "doc history",
}
DROP = {"reader map", "artifact contract", "split"}


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


def render(fm_raw: str, body: str) -> str:
    return f"---\n{fm_raw.strip()}\n---\n\n{body.lstrip()}"


def dump(path: Path, fm_raw: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(fm_raw, body), encoding="utf-8")


def set_key(fm_raw: str, key: str, value: str) -> str:
    if re.search(rf"^{key}:", fm_raw, re.M):
        return re.sub(rf"^{key}:.*$", f"{key}: {value}", fm_raw, count=1, flags=re.M)
    return fm_raw.rstrip() + f"\n{key}: {value}\n"


def lines_of(fm_raw: str, body: str) -> int:
    return render(fm_raw, body).count("\n") + 1


def strip_split(body: str) -> str:
    return SPLIT_RE.split(body)[0].rstrip()


def is_stub(body: str) -> bool:
    rest = strip_split(body)
    rest = re.sub(r"^# Split\s*", "", rest, flags=re.M).strip()
    rest = re.sub(r"^#+\s+Split\s*$", "", rest, flags=re.M).strip()
    return not rest


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


def family_root_stem(stem: str) -> str:
    while True:
        nxt = FAMILY_TAIL.sub("", stem)
        if nxt == stem:
            return stem
        stem = nxt


def existing_root(path: Path) -> Path:
    if path.name.startswith("overflow-"):
        design = path.parent.parent / "design.md"
        if design.is_file():
            return design
    stem = family_root_stem(path.stem)
    candidate = path.with_name(f"{stem}.md")
    if candidate.is_file():
        return candidate
    parts = stem.split(" - ")
    for i in range(len(parts) - 1, 0, -1):
        cand = path.with_name(" - ".join(parts[:i]) + ".md")
        if cand.is_file():
            return cand
    return path


def project_of(path: Path, software: Path) -> Path | None:
    try:
        rel = path.relative_to(software)
    except ValueError:
        return None
    if not rel.parts:
        return None
    return software / rel.parts[0]


def feature_folder(path: Path) -> Path | None:
    for parent in path.parents:
        if parent.parent.name == "03 - Features":
            return parent
    return None


def resolve_link(link: str, start: Path, project: Path) -> Path | None:
    name = link.split("/")[-1]
    direct = start.parent / f"{name}.md"
    if direct.is_file():
        return direct
    if name == "design - 1":
        ov = start.parent / "design" / "overflow-1.md"
        if ov.is_file():
            return ov
    feat = feature_folder(start)
    if feat:
        note = project / "89-Notes" / "Notes" / f"{feat.name} - {name}.md"
        if note.is_file():
            return note
    hits = [p for p in project.rglob("*.md") if p.stem == name or p.stem.endswith(f" - {name}")]
    if feat:
        ranked = [h for h in hits if feat in h.parents or feat.name in h.stem]
        if ranked:
            return ranked[0]
    if len(hits) == 1:
        return hits[0]
    return None


def collect_chain(root: Path, project: Path) -> list[Path]:
    seen: list[Path] = []
    queue = [root]
    extra = []
    if root.name == "design.md":
        extra.extend(sorted((root.parent / "design").glob("overflow-*.md")))
    stem = family_root_stem(root.stem)
    for sib in root.parent.glob("*.md"):
        if family_root_stem(sib.stem) == stem and sib != root:
            extra.append(sib)
    queue.extend(extra)
    while queue:
        p = queue.pop(0)
        if p in seen or not p.is_file():
            continue
        seen.append(p)
        text = p.read_text(encoding="utf-8", errors="replace")
        _fm, _raw, body = parse_fm(text)
        after = body
        if "## Split" in body:
            after = body.split("## Split", 1)[1]
        for m in LINK_RE.finditer(after):
            hit = resolve_link(m.group(1), p, project)
            if hit and hit not in seen:
                queue.append(hit)
    return seen


def concat_bodies(paths: list[Path]) -> str:
    chunks: list[str] = []
    seen_norm: set[str] = set()
    for p in paths:
        if not p.is_file():
            continue
        _fm, _raw, body = parse_fm(p.read_text(encoding="utf-8", errors="replace"))
        body = strip_split(body)
        if is_stub(body):
            continue
        norm = re.sub(r"\s+", " ", body).strip()
        if not norm or norm in seen_norm:
            continue
        seen_norm.add(norm)
        chunks.append(body.strip() + "\n")
    return "\n".join(chunks)


def table_blocks(chunk: str) -> list[str]:
    """Split a ## chunk without cutting a markdown table in half."""
    lines = chunk.splitlines(keepends=True)
    if not lines:
        return []
    heading = ""
    i = 0
    if lines[0].startswith("## "):
        heading = lines[0]
        i = 1
    blocks: list[str] = []
    buf: list[str] = []
    in_table = False
    for line in lines[i:]:
        if line.startswith("### ") and buf and not in_table:
            blocks.append("".join(buf))
            buf = [line]
            continue
        if line.startswith("|"):
            in_table = True
            buf.append(line)
            continue
        if in_table:
            if line.strip() == "":
                in_table = False
                buf.append(line)
                blocks.append("".join(buf))
                buf = []
            else:
                buf.append(line)
            continue
        buf.append(line)
    if buf:
        blocks.append("".join(buf))
    if not blocks:
        return [chunk]
    out = [heading + blocks[0]]
    for b in blocks[1:]:
        if heading and not b.startswith("#"):
            out.append(heading.rstrip() + " (cont.)\n\n" + b)
        else:
            out.append(b if b.startswith("#") else heading + b)
    return out


def _table_header(lines: list[str]) -> tuple[int, int] | None:
    for i, line in enumerate(lines[:-1]):
        if line.startswith("|") and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            return i, i + 2
    return None


def force_fit(fm_raw: str, chunk: str, cap: int) -> list[str]:
    if lines_of(fm_raw, chunk) <= cap:
        return [chunk]
    lines = chunk.splitlines(keepends=True)
    heading = lines[0] if lines and lines[0].startswith("#") else ""
    th = _table_header(lines)
    header_lines = lines[th[0] : th[1]] if th else []
    out: list[str] = []
    buf: list[str] = []
    start = 0
    if heading:
        buf.append(heading)
        start = 1

    def fits(extra: list[str]) -> bool:
        return lines_of(fm_raw, "".join(buf + extra)) <= cap

    i = start
    while i < len(lines):
        line = lines[i]
        extra = [line]
        if not fits(extra):
            if buf and "".join(buf).strip() not in {heading.strip(), ""}:
                out.append("".join(buf))
            buf = [heading] if heading else []
            if header_lines and line.startswith("|") and line not in header_lines:
                buf.extend(header_lines)
            if not fits([line]):
                # single line cannot fit — still emit to avoid loop
                buf.append(line)
                out.append("".join(buf))
                buf = [heading] if heading else []
                i += 1
                continue
        buf.append(line)
        i += 1
    if buf and "".join(buf).strip():
        out.append("".join(buf))
    return [p for p in out if p.strip()] or [chunk]


def pack_sections(fm_raw: str, segs: list[tuple[str, str]], cap: int) -> list[str]:
    files: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            files.append("".join(current))
            current.clear()

    for title, chunk in segs:
        if title.lower() in DROP:
            continue
        if not chunk.strip():
            continue
        probe = "".join(current + [chunk])
        if lines_of(fm_raw, probe) <= cap:
            current.append(chunk)
            continue
        if lines_of(fm_raw, chunk) <= cap:
            flush()
            current.append(chunk)
            continue
        flush()
        for piece in force_fit(fm_raw, chunk, cap):
            if current and lines_of(fm_raw, "".join(current) + piece) <= cap:
                current.append(piece)
            else:
                flush()
                current.append(piece)
    flush()
    return [f for f in files if f.strip()]


def peel_for_tail(fm_raw: str, body: str, tail: str, cap: int) -> tuple[str, list[str]]:
    overflow: list[str] = []
    segs = [(t, c) for t, c in sections(body) if c.strip() and t.lower() not in DROP]
    while segs and lines_of(fm_raw, "".join(c for _, c in segs) + tail) > cap:
        if len(segs) == 1:
            pieces = force_fit(fm_raw, segs[0][1], max(cap - (lines_of(fm_raw, tail) - lines_of(fm_raw, "")), 40))
            if len(pieces) > 1:
                segs = [("", pieces[0])]
                overflow = pieces[1:] + overflow
                continue
            break
        _t, chunk = segs.pop()
        overflow.insert(0, chunk)
    return "".join(c for _, c in segs), overflow


def slug(title: str, i: int) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-")[:40]
    return s or f"part-{i}"


def _child_path(root: Path, extra: str, i: int, typ: str) -> Path:
    title = next((t for t, _ in sections(extra) if t), f"part-{i}")
    child = root.with_name(f"{family_root_stem(root.stem)} - {slug(title, i)}.md")
    if typ == "intent":
        feat = feature_folder(root)
        for p in root.parents:
            if p.name in {"01 - Kraken", "02 - RoamPouch"} and feat:
                return p / "89-Notes" / "Notes" / f"{feat.name} - intent - {slug(title, i)}.md"
    return child


def write_packed(root: Path, packed: list[str], fm: dict, fm_raw: str) -> set[Path]:
    typ = fm.get("type", "")
    cap = cap_of(fm_raw, fm)
    flat: list[str] = []
    for piece in packed:
        flat.extend(force_fit(fm_raw, piece, cap))
    packed = flat
    while True:
        children = [_child_path(root, extra, i, typ) for i, extra in enumerate(packed[1:], 1)]
        idx = _index(children)
        if lines_of(fm_raw, packed[0] + idx) <= cap:
            break
        head, peeled = peel_for_tail(fm_raw, packed[0], idx, cap)
        if not peeled or head == packed[0]:
            # force smaller first file
            bits = force_fit(fm_raw, packed[0], max(cap - 8, 40))
            if len(bits) > 1:
                packed = bits + packed[1:]
                continue
            break
        packed = [head] + peeled + packed[1:]
    children = [_child_path(root, extra, i, typ) for i, extra in enumerate(packed[1:], 1)]
    dump(root, fm_raw, packed[0] + (_index(children) if children else ""))
    keep = {root}
    for i, (child, extra) in enumerate(zip(children, packed[1:]), 1):
        cfm = set_key(fm_raw, "id", f"{fm.get('id', root.stem)}.{i}")
        if typ == "intent":
            cfm = set_key(cfm, "type", "note")
            cfm = set_key(cfm, "lifecycle", "note")
        bits = force_fit(cfm, extra, cap)
        dump(child, cfm, bits[0])
        keep.add(child)
        for j, more in enumerate(bits[1:], 1):
            sib = child.with_name(f"{child.stem} - more-{j}.md")
            dump(sib, set_key(cfm, "id", f"{fm.get('id', root.stem)}.{i}.{j}"), more)
            keep.add(sib)
    return keep


def cap_of(fm_raw: str, fm: dict) -> int:
    if fm.get("max_lines", "").isdigit():
        return int(fm["max_lines"])
    return 80


def _index(children: list[Path]) -> str:
    if not children:
        return ""
    return "\n\n## Split\n\n" + "\n".join(f"- [[{c.stem}]]" for c in children) + "\n"


def heal_design(root: Path, family: list[Path]) -> set[Path]:
    fm, fm_raw, _ = parse_fm(root.read_text(encoding="utf-8", errors="replace"))
    body = concat_bodies(family)
    cap = 120
    kept: list[str] = []
    parts: dict[str, list[str]] = {k: [] for k in ("contracts", "flow", "quality", "operations")}
    for title, chunk in sections(body):
        key = title.lower()
        if key in DROP:
            continue
        if key == "parts":
            continue
        if key in KEEP_DESIGN or not title:
            probe = "".join(kept + [chunk])
            if title and lines_of(fm_raw, probe) > cap and title not in KEEP_DESIGN:
                parts[classify_design(title)].append(chunk)
            else:
                if lines_of(fm_raw, probe) <= cap:
                    kept.append(chunk)
                else:
                    parts[classify_design(title or "operations")].append(chunk)
            continue
        probe = "".join(kept + [chunk])
        if lines_of(fm_raw, probe) <= cap:
            kept.append(chunk)
        else:
            parts[classify_design(title)].append(chunk)
    keep: set[Path] = {root}
    dest = root.parent / "design"
    used: list[str] = []
    existing_parts = []
    if dest.is_dir():
        for kind in parts:
            part = dest / f"{kind}.md"
            if part.exists():
                existing_parts.append(kind)
    for kind, chunks in parts.items():
        if not chunks:
            if kind in existing_parts:
                used.append(kind)
            continue
        dest.mkdir(exist_ok=True)
        part = dest / f"{kind}.md"
        extra = "".join(chunks)
        if part.exists():
            _pfm, pfm_raw, pbody = parse_fm(part.read_text(encoding="utf-8"))
            pbody = strip_split(pbody)
            if extra.strip() not in pbody:
                dump(part, pfm_raw, pbody.rstrip() + "\n\n" + extra)
        else:
            dump(
                part,
                (
                    f"type: design-part\n"
                    f"id: {fm.get('id', root.stem)}.part.{kind}\n"
                    f"project: {fm.get('project', '')}\n"
                    f"created: {fm.get('created', '')}\n"
                    f"updated: {fm.get('updated', '')}\n"
                    f"status: current\nrev: 1\nlifecycle: delivery\ntags: []\n"
                    f"standard: 7\nmax_lines: 120\nparts: []\n"
                    f"feature: {fm.get('feature', '')}\n"
                    f"feature_id: {fm.get('feature_id', '')}\n"
                    f"depends_on: []\npart_kind: {kind}\n"
                ),
                f"# Design part — {kind}\n\n## Owner\n\n[[../design]]\n\n## Content\n\n{extra}",
            )
        keep.add(part)
        used.append(kind)
    for kind in existing_parts:
        keep.add(dest / f"{kind}.md")
        if kind not in used:
            used.append(kind)
    if used:
        block = "\n" + "\n".join(f"  - kind: {k}\n    path: design/{k}.md" for k in used)
        fm_raw = set_key(fm_raw, "parts", block)
    body = "".join(c for t, c in sections("".join(kept)) if t.lower() != "parts")
    while lines_of(fm_raw, body) > 120:
        segs = [(t, c) for t, c in sections(body) if c.strip()]
        peel = None
        for t, c in reversed(segs):
            if t.lower() not in KEEP_DESIGN and t.lower() not in {"parts", ""}:
                peel = (t, c)
                break
        if not peel:
            break
        body = "".join(c for t, c in segs if (t, c) != peel)
        kind = classify_design(peel[0])
        dest.mkdir(exist_ok=True)
        part = dest / f"{kind}.md"
        extra = peel[1]
        if part.exists():
            _pfm, pfm_raw, pbody = parse_fm(part.read_text(encoding="utf-8"))
            if extra.strip() not in strip_split(pbody):
                dump(part, pfm_raw, strip_split(pbody).rstrip() + "\n\n" + extra)
        keep.add(part)
    dump(root, fm_raw, body)
    for part in dest.glob("*.md") if dest.is_dir() else []:
        _pfm, pfm_raw, pbody = parse_fm(part.read_text(encoding="utf-8"))
        pbody = strip_split(pbody)
        if lines_of(pfm_raw, pbody) <= 120:
            keep.add(part)
            continue
        packed = pack_sections(pfm_raw, sections(pbody), 120)
        dump(part, pfm_raw, packed[0])
        keep.add(part)
        for i, extra in enumerate(packed[1:], 1):
            sib = part.with_name(f"{part.stem} - {slug(next((t for t,_ in sections(extra) if t), 'cont'), i)}.md")
            dump(sib, set_key(pfm_raw, "id", f"{_pfm.get('id', part.stem)}.{i}"), extra)
            keep.add(sib)
    return keep


def main() -> None:
    raise SystemExit(
        "retired: do not create stem - Heading.md. Use scripts/vault/heal_nav_and_splits.py merge-only."
    )
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    args = ap.parse_args()
    software = Path(args.vault) / "20 - Projects" / "10 - Software"
    roots = [software / "01 - Kraken", software / "02 - RoamPouch"]
    healed = 0
    deleted = 0
    for project in roots:
        if not project.is_dir():
            continue
        split_files = []
        for p in project.rglob("*.md"):
            text = p.read_text(encoding="utf-8", errors="replace")
            if not text.startswith("---"):
                continue
            fm = parse_fm(text)[0]
            cap = int(fm["max_lines"]) if fm.get("max_lines", "").isdigit() else 80
            if "## Split" in text or (fm.get("type") and text.count("\n") + 1 > cap):
                split_files.append(p)
        handled: set[Path] = set()
        families: list[tuple[Path, list[Path]]] = []
        seen_root: set[Path] = set()
        for path in sorted(split_files, key=lambda p: (p.name != "design.md", len(p.parts), str(p))):
            if path in handled or not path.is_file():
                continue
            root = existing_root(path)
            if root in seen_root:
                continue
            seen_root.add(root)
            chain = collect_chain(root, project)
            for c in chain:
                handled.add(c)
            families.append((root, chain))
        for root, chain in families:
            if not root.is_file():
                continue
            fm, _, _ = parse_fm(root.read_text(encoding="utf-8", errors="replace"))
            typ = fm.get("type", "")
            cap = int(fm["max_lines"]) if fm.get("max_lines", "").isdigit() else 80
            if typ == "design":
                keep = heal_design(root, chain)
            else:
                _fm, fm_raw, _ = parse_fm(root.read_text(encoding="utf-8"))
                body = concat_bodies(chain)
                packed = pack_sections(fm_raw, sections(body), cap)
                if not packed:
                    continue
                keep = write_packed(root, packed, _fm, fm_raw)
            for extra in chain:
                if extra not in keep and extra.is_file():
                    # only delete hard-cut leftovers
                    if FAMILY_TAIL.search(extra.stem) or extra.name.startswith("overflow-"):
                        extra.unlink()
                        deleted += 1
            healed += 1
    print(f"healed {healed} families, deleted {deleted} leftover cuts")


if __name__ == "__main__":
    main()
