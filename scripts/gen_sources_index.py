#!/usr/bin/env python3
"""Regenerate the source indexes from docs/model/sources/sources.yml, the
single source of truth for Monty data sources.

Without arguments, writes:
  - docs/model/sources/README.md — "Available Sources" and "Data Types by
    Source" sections, replaced between the gen_sources_index.py BEGIN/END markers
  - examples/index.md — the "Collections" listing grouped by Monty type,
    replaced between the gen_sources_index.py BEGIN/END markers. This is the single authoritative
    example index; docs/examples/index.md (the published page) pulls the same
    listing in via a pymdownx.snippets include, so a new collection surfaces on
    the site with no second edit. See https://github.com/IFRCGo/monty-stac-extension/issues/66.
  - docs/sources.json — machine-readable index, published by MkDocs
    (consumed by https://github.com/developmentseed/montandon-website)

With --check (what CI runs), nothing is written: the script recomputes both
outputs and fails if the working tree doesn't already match, and asserts the
structural invariants sources.yml is supposed to guarantee:
  - every non-`undocumented` source has a `doc` file under docs/model/sources/
    and is reachable from mkdocs.yml `nav`
  - `collections` matches the actual examples/<collection>/ directories,
    in both directions — nothing declared-but-missing, nothing shipped-but-
    undeclared

See https://github.com/IFRCGo/monty-stac-extension/issues/65.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "docs" / "model" / "sources"
SOURCES_YML = SOURCES_DIR / "sources.yml"
SOURCES_README = SOURCES_DIR / "README.md"
MKDOCS_YML = ROOT / "mkdocs.yml"
EXAMPLES_DIR = ROOT / "examples"
EXAMPLES_INDEX = EXAMPLES_DIR / "index.md"
SOURCES_JSON = ROOT / "docs" / "sources.json"

SITE_BASE_URL = "https://ifrcgo.org/monty-stac-extension/"
EXAMPLES_TREE_URL = "https://github.com/IFRCGo/monty-stac-extension/tree/main/examples"

VALID_STATUSES = {"undocumented", "analysis", "templates", "etl", "production"}
VALID_TYPES = {"event", "hazard", "impact", "response"}
TYPE_COLUMNS = [("event", "Events"), ("hazard", "Hazards"), ("impact", "Impacts"), ("response", "Response")]

# Maps a Monty type to the suffix its example collections use (e.g. cems-events),
# so the collections listing can be grouped by type.
COLLECTION_SUFFIX = {"event": "-events", "hazard": "-hazards", "impact": "-impacts", "response": "-response"}

# Collection directories under examples/ that aren't a source's collection
# and are deliberately excluded from the reconciliation check.
NON_SOURCE_EXAMPLE_DIRS = {"_response-impact-pairing"}

BEGIN = "<!-- gen_sources_index.py: BEGIN {} -->"
END = "<!-- gen_sources_index.py: END {} -->"


class _MkDocsYamlLoader(yaml.SafeLoader):
    """mkdocs.yml uses custom tags (`!!python/name:...`, `!relative`) for
    markdown-extension config that we don't care about here — just enough of
    a loader to walk `nav` without importing the tagged objects."""


_MkDocsYamlLoader.add_multi_constructor("tag:yaml.org,2002:python/name:", lambda loader, suffix, node: None)
_MkDocsYamlLoader.add_constructor("!relative", lambda loader, node: loader.construct_scalar(node))


def load_sources() -> list[dict[str, Any]]:
    data = yaml.safe_load(SOURCES_YML.read_text(encoding="utf-8"))
    sources = data["sources"]

    errors = []
    seen_ids = set()
    for src in sources:
        sid = src.get("id")
        if not sid:
            errors.append(f"source entry missing 'id': {src!r}")
            continue
        if sid in seen_ids:
            errors.append(f"duplicate source id: {sid!r}")
        seen_ids.add(sid)

        if src.get("status") not in VALID_STATUSES:
            errors.append(f"{sid}: invalid status {src.get('status')!r} (expected one of {sorted(VALID_STATUSES)})")
        if src.get("status") == "undocumented" and src.get("doc") is not None:
            errors.append(f"{sid}: status is 'undocumented' but 'doc' is set — undocumented sources must have doc: null")
        if src.get("status") != "undocumented" and src.get("doc") is None:
            errors.append(f"{sid}: 'doc' is null but status is {src.get('status')!r} — only undocumented sources may omit doc")

        bad_types = set(src.get("types", [])) - VALID_TYPES
        if bad_types:
            errors.append(f"{sid}: unknown type(s) {sorted(bad_types)} (expected one of {sorted(VALID_TYPES)})")

    if errors:
        _fail("sources.yml is malformed:", errors)

    return sorted(sources, key=lambda s: s["id"])


def _fail(header: str, errors: list[str]) -> None:
    print(header, file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    raise SystemExit(1)


def check_collections(sources: list[dict[str, Any]]) -> list[str]:
    errors = []
    declared: dict[str, str] = {}
    for src in sources:
        for collection in src["collections"]:
            if collection in declared:
                errors.append(f"collection {collection!r} declared by both {declared[collection]!r} and {src['id']!r}")
            declared[collection] = src["id"]
            if not (EXAMPLES_DIR / collection).is_dir():
                errors.append(f"{src['id']}: declared collection {collection!r} has no examples/{collection}/ directory")

    actual = {
        p.name
        for p in EXAMPLES_DIR.iterdir()
        if p.is_dir() and p.name not in NON_SOURCE_EXAMPLE_DIRS
    }
    undeclared = actual - declared.keys()
    if undeclared:
        errors.append(
            "examples/ directories not declared by any source in sources.yml: "
            f"{sorted(undeclared)} — add them to an existing source's `collections`, "
            "or a new source entry (status: undocumented if there's no doc yet)"
        )

    return errors


def check_docs_and_nav(sources: list[dict[str, Any]]) -> list[str]:
    errors = []
    nav_paths = set(_mkdocs_nav_paths())

    for src in sources:
        if src["doc"] is None:
            continue
        doc_path = SOURCES_DIR / src["doc"]
        if not doc_path.is_file():
            errors.append(f"{src['id']}: doc {src['doc']!r} does not exist at {doc_path.relative_to(ROOT)}")

        nav_path = f"model/sources/{src['doc']}"
        if nav_path not in nav_paths:
            errors.append(f"{src['id']}: {nav_path!r} is not reachable from mkdocs.yml nav")

    return errors


def _mkdocs_nav_paths() -> list[str]:
    data = yaml.load(MKDOCS_YML.read_text(encoding="utf-8"), Loader=_MkDocsYamlLoader)

    def walk(items):
        for item in items:
            if isinstance(item, dict):
                for value in item.values():
                    if isinstance(value, str):
                        yield value
                    elif isinstance(value, list):
                        yield from walk(value)

    return list(walk(data["nav"]))


def render_available_sources(sources: list[dict[str, Any]]) -> str:
    lines = ["## Available Sources", "", "| Source | Organisation | Status |", "|---|---|---|"]
    for src in sources:
        label = f"[{src['name']}](./{src['doc']})" if src["doc"] else src["name"]
        org = src["org"] or "—"
        lines.append(f"| {label} | {org} | {src['status']} |")
    return "\n".join(lines) + "\n"


def render_data_types_by_source(sources: list[dict[str, Any]]) -> str:
    header = "| Source | " + " | ".join(label for _, label in TYPE_COLUMNS) + " |"
    sep = "|" + "---|" * (len(TYPE_COLUMNS) + 1)
    lines = ["## Data Types by Source", "", header, sep]
    for src in sources:
        label = f"[{src['name']}](./{src['doc']})" if src["doc"] else src["name"]
        types = set(src["types"])
        marks = [("✓" if t in types else "-") for t, _ in TYPE_COLUMNS]
        lines.append(f"| {label} | " + " | ".join(marks) + " |")
    return "\n".join(lines) + "\n"


def render_examples_collections(sources: list[dict[str, Any]]) -> str:
    buckets: dict[str, list[tuple[str, str]]] = {t: [] for t, _ in TYPE_COLUMNS}
    other: list[tuple[str, str]] = []
    for src in sources:
        for collection in src["collections"]:
            for t, suffix in COLLECTION_SUFFIX.items():
                if collection.endswith(suffix):
                    buckets[t].append((collection, src["name"]))
                    break
            else:
                other.append((collection, src["name"]))

    def group(label: str, entries: list[tuple[str, str]]) -> str:
        items = "\n".join(
            f"- [{collection}]({EXAMPLES_TREE_URL}/{collection}) — {name}"
            for collection, name in sorted(entries)
        )
        return f"### {label}\n\n{items}"

    blocks = [group(label, buckets[t]) for t, label in TYPE_COLUMNS if buckets[t]]
    if other:
        blocks.append(group("Other", other))
    return "\n\n".join(blocks) + "\n"


def _replace_section(text: str, key: str, body: str) -> str:
    begin, end = BEGIN.format(key), END.format(key)
    start_idx = text.index(begin)
    end_idx = text.index(end)
    return text[: start_idx + len(begin)] + "\n" + body + text[end_idx:]


def render_readme(current: str, sources: list[dict[str, Any]]) -> str:
    sections = {
        "available-sources": render_available_sources(sources),
        "data-types-by-source": render_data_types_by_source(sources),
    }
    text = current
    for key, body in sections.items():
        text = _replace_section(text, key, body)
    return text


def render_sources_json(sources: list[dict[str, Any]]) -> str:
    payload = []
    for src in sources:
        doc_url = None
        if src["doc"]:
            doc_dir = str(Path(src["doc"]).parent)
            doc_url = f"{SITE_BASE_URL}model/sources/{doc_dir}/"
        payload.append(
            {
                "id": src["id"],
                "name": src["name"],
                "org": src["org"],
                "url": src["url"],
                "license": src["license"],
                "status": src["status"],
                "types": src["types"],
                "collections": src["collections"],
                "doc": doc_url,
                "etl": src["etl"],
            }
        )
    return json.dumps({"sources": payload}, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify outputs are in sync; don't write anything")
    args = parser.parse_args()

    sources = load_sources()

    errors = check_collections(sources) + check_docs_and_nav(sources)
    if errors:
        _fail(f"sources.yml is inconsistent with the repository ({len(errors)} problem(s)):", errors)

    current_readme = SOURCES_README.read_text(encoding="utf-8")
    new_readme = render_readme(current_readme, sources)
    current_examples = EXAMPLES_INDEX.read_text(encoding="utf-8")
    new_examples = _replace_section(current_examples, "examples-collections", render_examples_collections(sources))
    new_sources_json = render_sources_json(sources)

    outputs = [
        (SOURCES_README, current_readme, new_readme),
        (EXAMPLES_INDEX, current_examples, new_examples),
        (SOURCES_JSON, SOURCES_JSON.read_text(encoding="utf-8") if SOURCES_JSON.exists() else None, new_sources_json),
    ]

    if args.check:
        drift = [
            f"{path.relative_to(ROOT)} is out of date — run scripts/gen_sources_index.py"
            for path, current, new in outputs
            if new != current
        ]
        if drift:
            _fail("Generated source indexes are stale:", drift)
        print(f"sources.yml and generated indexes are in sync ({len(sources)} sources).")
        return 0

    for path, _current, new in outputs:
        path.write_text(new, encoding="utf-8")
    print(f"Wrote {', '.join(str(path.relative_to(ROOT)) for path, _, _ in outputs)} from "
          f"{len(sources)} sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
