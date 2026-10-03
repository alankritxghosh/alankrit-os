"""Phase 1: inventory the source corpus (read-only).

Discovers project boundaries by locating `extraction_manifest.json` files. A
directory holding a manifest is a project root; files not under any manifest
are reported as unassigned rather than guessed into a project.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from common import EXPECTED_ARTIFACTS, EXPECTED_ARTIFACTS_V2, sha256, slug, source_dir

MD_HEADING = re.compile(r"^#{1,3} ", re.M)


def _project_slug(name: str) -> str:
    # "Icarus (formerly JARVIS Engineering Intelligence)" -> "icarus"
    return slug(name.split("(")[0]) or "unnamed"


def scan(src: Path | None = None) -> dict:
    src = src or source_dir()
    if not src.is_dir():
        raise FileNotFoundError(f"source corpus not found: {src}")

    # archive/ holds superseded snapshots (v2 protocol); never treat them as live projects
    all_files = sorted(p for p in src.rglob("*") if p.is_file() and "archive" not in p.relative_to(src).parts)
    all_dirs = sorted({p.parent for p in all_files} | {src})
    manifests = [p for p in all_files if p.name == "extraction_manifest.json"]

    projects = []
    for m in manifests:
        try:
            data = json.loads(m.read_text(encoding="utf-8"))
            parse_ok = True
        except json.JSONDecodeError:
            data, parse_ok = {}, False
        root = m.parent
        present = sorted(p.name for p in root.iterdir() if p.is_file())
        expected = EXPECTED_ARTIFACTS_V2 if "04_BELIEF_EVOLUTION.md" in present else EXPECTED_ARTIFACTS
        projects.append({
            "slug": _project_slug(data.get("project_name", root.name)),
            "name": data.get("project_name", root.name),
            "root": str(root),
            "manifest": str(m),
            "manifest_parses": parse_ok,
            "extraction_date": data.get("extraction_date"),
            "latest_evidence_date": data.get("latest_evidence_date"),
            "declared_confidence": data.get("confidence"),
            "declared_counts": {k: v for k, v in data.items() if k.endswith("_found")},
            "coverage_gaps": data.get("coverage_gaps", []),
            "secondary_sources": data.get("secondary_sources", []),
            "present_artifacts": present,
            "schema": "v2" if expected is EXPECTED_ARTIFACTS_V2 else "v1",
            "missing_artifacts": [a for a in expected if a not in present],
            "unexpected_artifacts": [a for a in present if a not in expected],
        })

    roots = {Path(p["root"]): p["slug"] for p in projects}

    def owner(path: Path) -> str | None:
        for parent in [path.parent, *path.parent.parents]:
            if parent in roots:
                return roots[parent]
        return None

    files = []
    hashes: dict[str, list[str]] = {}
    for p in all_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        digest = sha256(p)
        hashes.setdefault(digest, []).append(str(p.relative_to(src)))
        issues = []
        if p.stat().st_size == 0:
            issues.append("empty")
        if p.suffix == ".md" and not MD_HEADING.search(text):
            issues.append("no markdown heading")
        if p.suffix == ".md" and text.count("```") % 2:
            issues.append("unbalanced code fence")
        files.append({
            "path": str(p.relative_to(src)),
            "project": owner(p),
            "bytes": p.stat().st_size,
            "lines": text.count("\n") + 1,
            "sha256": digest,
            "modified": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
            "expected_artifact": p.name in EXPECTED_ARTIFACTS or p.name in EXPECTED_ARTIFACTS_V2,
            "issues": issues,
        })

    duplicates = [v for v in hashes.values() if len(v) > 1]
    return {
        "source_path": str(src),
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "directories": [str(d.relative_to(src)) or "." for d in all_dirs],
        "file_count": len(files),
        "total_bytes": sum(f["bytes"] for f in files),
        "projects": projects,
        "unassigned_files": [f["path"] for f in files if f["project"] is None],
        "duplicates": duplicates,
        "files": files,
    }


if __name__ == "__main__":
    print(json.dumps(scan(), indent=2)[:4000])
