"""Phase 2: parse every extraction artifact into line-anchored records.

Parsers are format-specific to the extraction template (bold-ID blocks,
markdown tables, numbered lists). Each record keeps `file` and `line` so any
compiled claim can be traced back to the exact source line.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from common import find_conf, norm_date


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _blocks(lines, start_re, stop_re=re.compile(r"^(#{1,3} |\*\*[A-Z]+\d+[ .·])")):
    """Yield (line_no, match, body_lines) for each block opened by start_re."""
    i = 0
    while i < len(lines):
        m = start_re.match(lines[i])
        if not m:
            i += 1
            continue
        start, body = i, [lines[i]]
        i += 1
        while i < len(lines) and not stop_re.match(lines[i]):
            body.append(lines[i])
            i += 1
        yield start + 1, m, body


def _section_at(lines, idx):
    for j in range(idx, -1, -1):
        if lines[j].startswith("## "):
            return lines[j][3:].strip()
    return None


def _table(lines, first_cell_re):
    for n, line in enumerate(lines, 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and first_cell_re.match(cells[0]):
            yield n, cells


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


FIELD = re.compile(
    r"\b(Context|Options|Chosen|Rejected|Reason(?: for re-enable)?|Evidence|Tradeoff(?: accepted openly)?|"
    r"Consequence|Status|Source|Trigger|Terms|Outcome|Abort rule|Key insights adopted)s?:"
)


def _fields(text: str) -> dict:
    parts = FIELD.split(text)
    out = {"_lead": _clean(parts[0])}
    for k, v in zip(parts[1::2], parts[2::2]):
        out[k.split()[0].lower()] = _clean(v)
    return out


def _split_bold(body, prefix_len):
    """Join a block and split '<title>**<rest>' even when the bold title wraps lines."""
    joined = _clean(" ".join(body))[prefix_len:]
    title, _, rest = joined.partition("**")
    return title.strip(), rest.strip()


# ---------------------------------------------------------------- parsers

def parse_decisions(path):
    lines = _lines(path)
    rx = re.compile(r"^\*\*(D\d+) · ([^·]+?) · (.+?)\*\*(.*)$")
    for ln, m, body in _blocks(lines, rx):
        text = _clean(" ".join([m.group(4)] + body[1:]))
        f = _fields(text)
        status = f.get("status", "")
        yield {
            "local_id": m.group(1), "file": path.name, "line": ln,
            "date_raw": m.group(2).strip(), "date": norm_date(m.group(2)),
            "title": m.group(3).strip().rstrip("."), "text": text, "fields": f,
            "status_raw": status or ("active" if "active" in text.lower() else "unstated"),
            "confidence": find_conf(text, "HIGH"),  # register default: "HIGH unless stated"
        }


def parse_beliefs(path):
    lines = _lines(path)
    rx = re.compile(r"^\*\*(B\d+)\. ")
    for ln, m, body in _blocks(lines, rx):
        statement, text = _split_bold(body, m.end())
        kind = re.search(r"\b(EXPLICIT|INFERRED)\b", text)
        yield {
            "local_id": m.group(1), "file": path.name, "line": ln,
            "statement": statement, "text": text,
            "domain": _section_at(lines, ln - 1),
            "kind": kind.group(1) if kind else "UNSTATED",
            "confidence": find_conf(text),
        }


def parse_reasoning(path):
    lines = _lines(path)
    rx = re.compile(r"^\*\*(R\d+)\. ")
    for ln, m, body in _blocks(lines, rx):
        pattern, text = _split_bold(body, m.end())
        yield {"local_id": m.group(1), "file": path.name, "line": ln,
               "pattern": pattern, "text": text, "confidence": find_conf(text)}


def parse_contradictions(path):
    lines = _lines(path)
    rx = re.compile(r"^\*\*(C\d+)\. ")
    for ln, m, body in _blocks(lines, rx):
        title, text = _split_bold(body, m.end())
        low = text.lower()
        if "unresolved" in low or "stale" in low:
            status = "UNRESOLVED"
        elif "intentional" in low or "evolution" in low:
            status = "INTENTIONAL_EVOLUTION"
        else:
            status = "UNCLASSIFIED"
        yield {"local_id": m.group(1), "file": path.name, "line": ln,
               "title": title, "text": text, "status": status}


def parse_open_loops(path):
    lines = _lines(path)
    for ln, c in _table(lines, re.compile(r"^O\d+$")):
        c += [""] * (7 - len(c))
        yield {"local_id": c[0], "file": path.name, "line": ln,
               "question": c[1].strip("*"), "why": c[2], "understanding": c[3],
               "next_step": c[4], "status": c[5], "source_ref": c[6]}


def parse_timeline(path):
    lines = _lines(path)
    for i, (ln, c) in enumerate(_table(lines, re.compile(r"^(pre-|~)?\d{2,4}-|^\d{4}")), 1):
        c += [""] * (4 - len(c))
        yield {"local_id": f"T{i:02d}", "file": path.name, "line": ln,
               "date_raw": c[0], "date": norm_date(c[0]),
               "event": c[1], "why": c[2], "source_ref": c[3]}


def parse_glossary(path):
    lines = _lines(path)
    for ln, c in _table(lines, re.compile(r"^(?!Term$|---)[^|-].*")):
        if len(c) < 3:
            continue
        yield {"local_id": f"G{ln}", "file": path.name, "line": ln,
               "term": c[0].strip("*"), "meaning": c[1], "status": c[2],
               "related": c[3] if len(c) > 3 else ""}


def parse_failures(path):
    lines = _lines(path)
    rx = re.compile(r"^(\d+)\. \*\*(.+?)\*\*(.*)$")
    stop = re.compile(r"^(\d+\. \*\*|#{1,3} |- )")
    for ln, m, body in _blocks(lines, rx, stop):
        text = _clean(" ".join([m.group(3)] + body[1:]))
        yield {"local_id": f"F{int(m.group(1)):02d}", "file": path.name, "line": ln,
               "title": m.group(2).strip().rstrip("."), "text": text,
               "category": _section_at(lines, ln - 1),
               "date": norm_date(m.group(2) + " " + text)}
    # bullet sections: abandoned items and cross-cutting lessons
    section, counters = None, {"L": 0, "A": 0}
    for n, line in enumerate(lines, 1):
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("- ") and section:
            kind = "lesson" if section.lower().startswith("cross-cutting") else "abandoned"
            pre = "L" if kind == "lesson" else "A"
            counters[pre] += 1
            text, k = line[2:], n
            while k < len(lines) and lines[k].startswith("  ") and lines[k].strip():
                text += " " + lines[k].strip()
                k += 1
            yield {"local_id": f"{pre}{counters[pre]}", "file": path.name,
                   "line": n, "kind": kind, "category": section,
                   "title": _clean(text), "text": _clean(text)}


def parse_bullets(path):
    """Generic: every '- ' bullet with its heading, for narrative sources."""
    lines = _lines(path)
    heading, count = None, 0
    for n, line in enumerate(lines, 1):
        if re.match(r"^#{1,3} ", line):
            heading = line.lstrip("#").strip()
            continue
        if line.startswith("- "):
            text = line[2:]
            k = n
            while k < len(lines) and lines[k].startswith("  ") and lines[k].strip():
                text += " " + lines[k].strip()
                k += 1
            count += 1
            code = path.name[:2] if path.name[:2].isdigit() else "99"
            yield {"local_id": f"X{code}L{count}", "file": path.name, "line": n,
                   "heading": heading, "text": _clean(text), "confidence": find_conf(text)}


FACT_RX = re.compile(r"`FACT`")


def parse_facts(path):
    """Statements explicitly tagged `FACT` by the extractor (paragraph or bullet)."""
    lines = _lines(path)
    n = 0
    while n < len(lines):
        if FACT_RX.search(lines[n]) and not lines[n].startswith("Labels:"):
            start, buf = n, [lines[n]]
            n += 1
            while n < len(lines) and lines[n].strip() and not lines[n].startswith(("- ", "#", "|")):
                buf.append(lines[n])
                n += 1
            text = _clean(" ".join(buf)).lstrip("- ")
            yield {"local_id": f"FACT{path.name[:2]}L{start + 1}", "file": path.name, "line": start + 1,
                   "heading": _section_at(lines, start), "text": text,
                   "confidence": find_conf(text)}
        else:
            n += 1


def parse_phases(path):
    """Strategic-evolution phases from 13_KNOWLEDGE_GRAPH.md."""
    lines = _lines(path)
    rx = re.compile(r"^\*\*((?:Phase \d+|Current)) — ")
    for i, (ln, m, body) in enumerate(_blocks(lines, rx, re.compile(r"^(#{1,3} |\*\*(Phase \d+|Current) — )")), 1):
        title, text = _split_bold(body, 2)
        yield {"local_id": f"PH{i}", "file": path.name, "line": ln, "title": title, "text": text,
               "date": norm_date(title)}


def parse_project(root: Path) -> dict:
    v2_names = {  # v1 artifact name -> v2 protocol name
        "04_REASONING_PATTERNS.md": "05_REASONING_PATTERNS.md", "05_WORKING_STYLE.md": "06_WORKING_STYLE.md",
        "06_VOICE_PROFILE.md": "07_VOICE_PROFILE.md", "07_PROJECT_TIMELINE.md": "01_PROJECT_TIMELINE.md",
        "01_ALANKRIT_CONTEXT.md": "12_ALANKRIT_CONTEXT.md",
    }

    def p(name):
        f = root / name
        if f.exists():
            return f
        alt = root / v2_names.get(name, "")
        return alt if name in v2_names and alt.exists() else None

    out = {k: [] for k in ["decisions", "beliefs", "reasoning", "contradictions", "open_loops",
                           "timeline", "glossary", "failures", "facts", "transferable",
                           "voice", "working_style", "alankrit", "handoff", "graph", "project"]}
    plan = [
        ("decisions", "02_DECISION_REGISTER.md", parse_decisions),
        ("beliefs", "03_BELIEF_SYSTEM.md", parse_beliefs),
        ("reasoning", "04_REASONING_PATTERNS.md", parse_reasoning),
        ("contradictions", "10_CONTRADICTIONS.md", parse_contradictions),
        ("open_loops", "09_OPEN_LOOPS.md", parse_open_loops),
        ("timeline", "07_PROJECT_TIMELINE.md", parse_timeline),
        ("glossary", "12_GLOSSARY.md", parse_glossary),
        ("failures", "08_FAILURES_AND_LESSONS.md", parse_failures),
        ("transferable", "11_TRANSFERABLE_CONTEXT.md", parse_bullets),
        ("voice", "06_VOICE_PROFILE.md", parse_bullets),
        ("working_style", "05_WORKING_STYLE.md", parse_bullets),
        ("alankrit", "01_ALANKRIT_CONTEXT.md", parse_bullets),
        ("handoff", "HANDOFF_TO_ALANKRIT_OS.md", parse_bullets),
        ("project", "00_PROJECT_CONTEXT.md", parse_bullets),
        ("graph", "13_KNOWLEDGE_GRAPH.md", parse_phases),
    ]
    for key, name, fn in plan:
        f = p(name)
        if f:
            out[key] = list(fn(f))
    for name in ["00_PROJECT_CONTEXT.md", "01_ALANKRIT_CONTEXT.md"]:
        f = p(name)
        if f:
            out["facts"].extend(parse_facts(f))
    return out


if __name__ == "__main__":
    from common import source_dir
    parsed = parse_project(source_dir())
    print(json.dumps({k: len(v) for k, v in parsed.items()}, indent=2))
