#!/usr/bin/env python3
"""Keep the documented exposure categories aligned with the JSON Schema."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "json-schema" / "schema.json"
TAXONOMY = ROOT / "docs" / "model" / "taxonomy.md"
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


def load_schema_categories() -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return schema["definitions"]["fields"]["properties"]["monty:impact_detail"][
        "properties"
    ]["category"]["enum"]


def load_taxonomy_categories() -> list[str]:
    lines = TAXONOMY.read_text(encoding="utf-8").splitlines()
    heading_index = lines.index("### Exposure Category")

    rows = []
    in_table = False
    for line in lines[heading_index + 1 :]:
        match = TABLE_ROW_RE.match(line)
        if match:
            in_table = True
            rows.append([cell.strip() for cell in match.group(1).split("|")])
        elif in_table:
            break

    return [row[0] for row in rows[2:] if row and row[0]]


def main() -> int:
    schema_categories = load_schema_categories()
    taxonomy_categories = load_taxonomy_categories()

    if taxonomy_categories == schema_categories:
        print(
            f"All {len(schema_categories)} exposure categories in taxonomy.md "
            "match json-schema/schema.json."
        )
        return 0

    schema_set = set(schema_categories)
    taxonomy_set = set(taxonomy_categories)
    missing = [category for category in schema_categories if category not in taxonomy_set]
    unexpected = [category for category in taxonomy_categories if category not in schema_set]

    print("Exposure categories in taxonomy.md do not match the schema.", file=sys.stderr)
    if missing:
        print(f"  Missing from taxonomy.md: {missing}", file=sys.stderr)
    if unexpected:
        print(f"  Not present in the schema: {unexpected}", file=sys.stderr)
    if not missing and not unexpected:
        print("  The categories are in a different order.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
