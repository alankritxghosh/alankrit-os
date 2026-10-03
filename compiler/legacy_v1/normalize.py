"""Phase 2b: normalize parsed records into one typed, globally-identified model.

Global id = "<project>:<local_id>". Every record carries `source` = {file, line}
relative to the project root inside the source corpus.
"""
from __future__ import annotations

TYPE_OF = {
    "decisions": "decision", "beliefs": "belief", "reasoning": "reasoning_pattern",
    "contradictions": "contradiction", "open_loops": "open_loop", "timeline": "episode",
    "glossary": "definition", "facts": "fact", "transferable": "transferable_insight",
    "voice": "voice_rule", "working_style": "working_style_note", "alankrit": "identity_note",
    "handoff": "handoff_note", "project": "project_note", "graph": "phase",
}


def normalize(parsed_by_project: dict[str, dict], scan: dict) -> dict:
    model = {"projects": {}, "records": {}, "by_kind": {}, "scan": scan}
    for proj in scan["projects"]:
        model["projects"][proj["slug"]] = proj
    for slug, parsed in parsed_by_project.items():
        root = next(p["root"] for p in scan["projects"] if p["slug"] == slug)
        for kind, rows in parsed.items():
            for r in rows:
                if kind == "failures":
                    rtype = {"lesson": "lesson", "abandoned": "abandoned"}.get(r.get("kind"), "failure")
                else:
                    rtype = TYPE_OF.get(kind, kind)
                gid = f"{slug}:{r['local_id']}"
                rec = dict(r)
                if rtype == "decision":
                    rec.setdefault("classification", "PROJECT-SPECIFIC")  # decisions never become traits by default
                rec.update(id=gid, type=rtype, project=slug, kind_bucket=kind,
                           source={"root": root, "file": r["file"], "line": r["line"]})
                model["records"][gid] = rec
                model["by_kind"].setdefault(kind, []).append(rec)
        # the manifest itself is a citable source record
        model["records"][f"{slug}:MANIFEST"] = {
            "id": f"{slug}:MANIFEST", "type": "manifest", "project": slug,
            "text": "extraction_manifest.json", "source": {"root": root, "file": "extraction_manifest.json", "line": 1},
        }
    return model


def get(model, gid):
    return model["records"].get(gid)
