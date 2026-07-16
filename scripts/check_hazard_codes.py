#!/usr/bin/env python3
"""Validate `monty:hazard_codes` values shipped in examples/ against the
canonical codes documented in docs/model/taxonomy.md.

Deliberately not a JSON Schema `enum`: an enum in json-schema/schema.json
would be too restrictive and would couple schema releases to taxonomy
updates. See https://github.com/IFRCGo/monty-stac-extension/issues/64 and
the incident that prompted it, https://github.com/IFRCGo/monty-stac-extension/issues/61.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_MD = ROOT / "docs" / "model" / "taxonomy.md"
EXAMPLES_DIR = ROOT / "examples"

# Codes that are known not to resolve against taxonomy.md but are shipped
# deliberately. Each entry must document *why*, and point at the issue
# tracking its resolution, so the list doesn't silently grow.
WAIVED_CODES: dict[str, str] = {
    "BH0001": (
        "DesInventar-only code, absent from taxonomy.md under any prefix; "
        "out of scope for #61, tracked separately "
        "(examples/desinventar-events/grd-200.json, "
        "examples/desinventar-impacts/grd-200-deaths.json)."
    ),
}

TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


def _table_rows(lines: list[str], header_index: int) -> list[list[str]]:
    """Parse the markdown table whose header starts at `header_index`.

    Returns the data rows (header and separator rows excluded) as lists of
    stripped cell values.
    """
    rows = []
    for line in lines[header_index:]:
        match = TABLE_ROW_RE.match(line.rstrip())
        if not match:
            break
        rows.append([cell.strip() for cell in match.group(1).split("|")])
    return rows[2:]


def _find_table_after(lines: list[str], heading_re: re.Pattern[str]) -> list[list[str]]:
    for i, line in enumerate(lines):
        if heading_re.match(line):
            for j in range(i + 1, len(lines)):
                if TABLE_ROW_RE.match(lines[j].rstrip()):
                    return _table_rows(lines, j)
            raise ValueError(f"no table found under heading matching {heading_re.pattern!r}")
    raise ValueError(f"heading matching {heading_re.pattern!r} not found in {TAXONOMY_MD}")


def load_canonical_codes() -> set[str]:
    """Collect the first-column values of the three code tables in
    taxonomy.md that examples/ draw `monty:hazard_codes` from: the GLIDE
    classification, the EM-DAT classification key, and the current
    UNDRR-ISC 2025 Hazard List.

    The "2020 Hazard Information Profiles (Historical Reference)" table is
    intentionally excluded — those codes are superseded, and treating them
    as valid would have let #61 (MH0403/MH0901/...) pass unnoticed.
    """
    lines = TAXONOMY_MD.read_text(encoding="utf-8").splitlines()

    glide = _find_table_after(lines, re.compile(r"^### GLIDE Classification"))
    emdat = _find_table_after(lines, re.compile(r"^### \[EM-DAT CRED Classification Tree\]"))
    undrr = _find_table_after(lines, re.compile(r"^#### Complete 2025 Hazard List"))

    return {row[0] for row in (*glide, *emdat, *undrr) if row and row[0]}


def iter_hazard_code_usages(examples_dir: Path):
    for path in sorted(examples_dir.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        codes = data.get("properties", {}).get("monty:hazard_codes")
        if codes is None:
            codes = data.get("summaries", {}).get("monty:hazard_codes")
        if not isinstance(codes, list):
            continue
        for code in codes:
            yield path, code


def main() -> int:
    canonical = load_canonical_codes()
    errors = []
    waivers_used = set()

    for path, code in iter_hazard_code_usages(EXAMPLES_DIR):
        if code in canonical:
            continue
        if code in WAIVED_CODES:
            waivers_used.add(code)
            continue
        errors.append(
            f"{path.relative_to(ROOT)}: {code!r} is not a recognized hazard code "
            "(GLIDE, EM-DAT classification key, or UNDRR-ISC 2025 Hazard Code) "
            "and is not in the waiver list"
        )

    stale_waivers = WAIVED_CODES.keys() - waivers_used
    if stale_waivers:
        print(
            f"Note: waiver(s) {sorted(stale_waivers)} are no longer used by any example "
            "— consider removing them from WAIVED_CODES.",
            file=sys.stderr,
        )

    if errors:
        print(f"Found {len(errors)} unrecognized hazard code(s) in examples/:\n", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print(
        f"All monty:hazard_codes values in examples/ resolve to one of "
        f"{len(canonical)} canonical codes from taxonomy.md "
        f"({len(waivers_used)} waived)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
