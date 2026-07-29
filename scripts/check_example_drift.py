#!/usr/bin/env python3
"""Re-run the real pystac-monty transformers over the fixtures committed in
docs/model/sources/ and compare the result with the items in examples/.

This is the *ground truth* half of the drift tooling. Where
check_etl_drift.py reads the upstream diff and infers what may have broken,
this one executes the mapping and shows what actually broke — expressed in the
same vocabulary the docs use (item ids, roles, monty: fields) rather than in
Python lines. It also does what METHODOLOGY.md rule 3 asks for and nothing
enforced until now: keep the worked examples regenerable from the transformer.

What it compares
----------------
examples/ holds a *curated subset* of a transformer's output — a few worked
items per collection, not a full run. So the invariant is one-directional:

    every committed example item must still be produced, byte-for-byte
    (modulo the volatile fields below), by the current transformer

Extra generated items are expected and are only summarised as counts. A
committed example that is no longer produced is the loud case: it means the id
format, the filtering, or the item cardinality changed.

Coverage
--------
Only sources whose entry in .github/etl-watch.yml has a `regenerate:` block,
which needs two things to exist: a batch exporter registered upstream in
pystac_monty.sources.batch_export.BATCH_EXPORTS, and a machine-readable fixture
committed here. Several early fixtures were saved from a browser and carry a
`// <timestamp>` preamble that is not valid JSON — those sources can't be
covered until the fixture is recaptured. Anything not covered here is still
watched by check_etl_drift.py, which needs neither.

Usage
-----
    python scripts/check_example_drift.py --dry-run
    python scripts/check_example_drift.py --source cems --diff
    python scripts/check_example_drift.py            # create/update issues

Needs pystac-monty installed (`pip install -e ../pystac-monty` or from PyPI);
exits 0 with a notice if it isn't, so a scheduled run degrades to the diff
watcher instead of failing.
"""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
import tempfile
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_etl_drift import (  # noqa: E402  (shared config, GitHub and issue plumbing)
    REPORTED_MARKER,
    THIS_REPO,
    load_watch,
    marker,
    resolve_assignees,
    upsert_issue,
)
from gen_sources_index import load_sources  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"

# Regenerating always rewrites these, and none of them is a mapping decision:
# comparing them would make every run report drift.
#   links      - rewritten by the exporter for the output catalog layout
#   created/updated - stamped at generation time
IGNORED_ITEM_KEYS = ("links",)
IGNORED_PROPERTIES = ("created", "updated")

MAX_DIFFS_PER_ITEM = 12
MAX_ITEMS_REPORTED = 8


class Skip(Exception):
    """This source can't be checked in this environment — pystac-monty isn't
    installed, or upstream registers no batch exporter for it. Never drift:
    nothing was learned about the doc either way."""


class FixtureRejected(Exception):
    """The transformer ran and refused the fixture committed here. That *is*
    drift, and a sharp kind: the payload the whole source analysis is grounded
    in no longer satisfies the code that consumes it."""


# --------------------------------------------------------------------------- #
# regeneration
# --------------------------------------------------------------------------- #


def regenerate(batch: str, input_path: Path, output_dir: Path) -> None:
    """Run the upstream batch exporter in-process.

    The transformers resolve their collection JSON from
    `MontyDataTransformer.base_collection_url`; upstream's default points at a
    checkout nested inside pystac-monty, so it is repointed at *this* repo's
    examples/ before anything runs. That also means the collections under test
    are the ones committed here, which is what we want to be comparing."""
    try:
        from pystac_monty.sources import batch_export
        from pystac_monty.sources.common import MontyDataTransformer
    except ImportError as error:  # pragma: no cover - depends on the environment
        raise Skip(f"pystac-monty is not importable ({error})")

    if batch not in batch_export.BATCH_EXPORTS:
        raise Skip(
            f"upstream has no batch exporter named {batch!r} "
            f"(available: {', '.join(sorted(batch_export.BATCH_EXPORTS))})"
        )

    MontyDataTransformer.base_collection_url = str(EXAMPLES)
    batch_export.use_local_collection_examples = lambda: None  # keep the line above

    try:
        batch_export.run_batch(batch, input_path, output_dir)
    except Exception as error:  # noqa: BLE001 - upstream raises anything
        raise FixtureRejected(f"{type(error).__name__}: {error}")


def upstream_provenance() -> str:
    """Which pystac-monty actually produced the items, as precisely as it can
    be determined.

    This is not cosmetic. Run against a stale checkout, this tool reports drift
    that upstream fixed months ago — it did exactly that on its first outing,
    replaying a hazard-code bug that
    https://github.com/IFRCGo/monty-stac-extension/pull/74 had already fixed —
    and a drift report nobody can attribute to a commit is worse than none. So
    every run, and every issue it files, says what it ran."""
    try:
        import pystac_monty
    except ImportError:
        return "pystac-monty (not installed)"

    try:
        from importlib.metadata import version

        release = version("pystac_monty")
    except Exception:  # noqa: BLE001 - metadata is best-effort
        release = "unknown version"

    package_dir = Path(pystac_monty.__file__).resolve().parent
    try:
        sha = subprocess.run(
            ["git", "-C", str(package_dir), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()[:8]
        return f"pystac-monty {release} (git {sha}, {package_dir.parent})"
    except (OSError, subprocess.CalledProcessError):
        return f"pystac-monty {release} ({package_dir.parent})"


def load_items(root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """Index the regenerated items by (collection, id). Ids are only unique
    within a collection — GDACS publishes an event and its hazard under the
    same id today — so the collection has to be part of the key."""
    items: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(root.rglob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(doc, dict) and doc.get("type") == "Feature" and "id" in doc:
            items[(doc.get("collection") or "", doc["id"])] = doc
    return items


def committed_items(source: dict[str, Any], recipe: dict[str, Any]) -> list[tuple[Path, dict[str, Any]]]:
    """The examples this fixture is expected to reproduce — a list, not a dict,
    because the committed examples do contain repeated ids.

    `covers` narrows that to the records the fixture actually contains: one
    captured payload rarely covers every worked example a source has, and an
    example the fixture never mentions must not be reported as lost."""
    patterns = recipe.get("covers")
    found: list[tuple[Path, dict[str, Any]]] = []
    for collection in source["collections"]:
        for path in sorted((EXAMPLES / collection).glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            if doc.get("type") != "Feature":
                continue
            if patterns and not any(fnmatch(doc["id"], pattern) for pattern in patterns):
                continue
            found.append((path, doc))
    return found


# --------------------------------------------------------------------------- #
# comparison
# --------------------------------------------------------------------------- #


def diff_item(committed: dict[str, Any], generated: dict[str, Any]) -> list[str]:
    """Field-level differences, as `path: committed → generated` lines."""
    return _walk("", _prune(committed), _prune(generated))


def _prune(item: dict[str, Any]) -> dict[str, Any]:
    pruned = {k: v for k, v in item.items() if k not in IGNORED_ITEM_KEYS}
    properties = {k: v for k, v in pruned.get("properties", {}).items() if k not in IGNORED_PROPERTIES}
    pruned["properties"] = properties
    return pruned


def _walk(path: str, left: Any, right: Any) -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        diffs = []
        for key in sorted(set(left) | set(right)):
            here = f"{path}.{key}" if path else key
            if key not in left:
                diffs.append(f"{here}: (absent) → {_short(right[key])}")
            elif key not in right:
                diffs.append(f"{here}: {_short(left[key])} → (absent)")
            else:
                diffs.extend(_walk(here, left[key], right[key]))
        return diffs
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return [f"{path}: {len(left)} entr(ies) → {len(right)}: {_short(left)} → {_short(right)}"]
        return [d for i, (a, b) in enumerate(zip(left, right)) for d in _walk(f"{path}[{i}]", a, b)]
    if left != right:
        return [f"{path}: {_short(left)} → {_short(right)}"]
    return []


def _short(value: Any, limit: int = 90) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= limit else text[: limit - 1] + "…"


# --------------------------------------------------------------------------- #
# per-source check
# --------------------------------------------------------------------------- #


class Result:
    def __init__(self, source: dict[str, Any]) -> None:
        self.source = source
        self.skipped: str | None = None
        self.rejected: str | None = None                # transformer refused our fixture
        self.missing: list[tuple[str, Path, str]] = []  # committed, no longer produced, closest match
        self.changed: list[tuple[str, Path, list[str]]] = []
        self.counts: dict[str, int] = {}                # generated items per collection
        self.total_generated = 0

    @property
    def drifted(self) -> bool:
        return bool(self.missing or self.changed or self.rejected)


def check_source(source: dict[str, Any], recipe: dict[str, Any]) -> Result:
    result = Result(source)
    fixture = ROOT / recipe["input"]
    if not fixture.exists():
        result.skipped = f"fixture `{recipe['input']}` does not exist"
        return result

    with tempfile.TemporaryDirectory(prefix="monty-regen-") as tmp:
        out = Path(tmp)
        try:
            regenerate(recipe["batch"], fixture, out)
        except Skip as skip:
            result.skipped = str(skip)
            return result
        except FixtureRejected as rejected:
            result.rejected = str(rejected)
            return result
        generated = load_items(out)
        result.total_generated = len(generated)
        for collection, _ in generated:
            result.counts[collection or "(none)"] = result.counts.get(collection or "(none)", 0) + 1

        for path, doc in committed_items(source, recipe):
            key = (doc.get("collection") or "", doc["id"])
            if key not in generated:
                result.missing.append((doc["id"], path, _closest(doc, generated)))
                continue
            diffs = diff_item(doc, generated[key])
            if diffs:
                result.changed.append((doc["id"], path, diffs))

    return result


def _closest(doc: dict[str, Any], generated: dict[tuple[str, str], dict[str, Any]]) -> str:
    """The generated id most like the lost one. An id-format change is the
    common cause of a disappearance, and naming its replacement turns
    'this example is gone' into 'this example was renamed to that'."""
    candidates = [item_id for collection, item_id in generated if collection == (doc.get("collection") or "")]
    matches = difflib.get_close_matches(doc["id"], candidates, n=1, cutoff=0.3)
    return matches[0] if matches else ""


# --------------------------------------------------------------------------- #
# reporting
# --------------------------------------------------------------------------- #


def render_issue(result: Result, recipe: dict[str, Any]) -> str:
    src = result.source
    doc = f"docs/model/sources/{src['doc']}"
    lines = [
        marker("examples", src["id"]),
        (
            f"Re-running the **{src['name']}** transformer over "
            f"[`{recipe['input']}`](https://github.com/{THIS_REPO}/blob/main/{recipe['input']}) no longer "
            "reproduces the worked examples committed for this source. Raised automatically by "
            f"[`scripts/check_example_drift.py`](https://github.com/{THIS_REPO}/blob/main/scripts/"
            "check_example_drift.py)."
        ),
        "",
        f"- **Source doc:** [`{doc}`](https://github.com/{THIS_REPO}/blob/main/{doc})",
        f"- **Fixture:** `{recipe['input']}` (batch exporter `{recipe['batch']}`)",
        f"- **Ran against:** `{upstream_provenance()}`",
        f"- **Items regenerated:** {result.total_generated}"
        + (
            " — " + ", ".join(f"{count} × `{name}`" for name, count in sorted(result.counts.items()))
            if result.counts
            else ""
        ),
        "",
    ]

    if result.rejected:
        lines += [
            "## The transformer rejected the committed fixture",
            "",
            (
                "It did not get as far as producing items. The captured payload this whole analysis is "
                "grounded in (METHODOLOGY.md rule 2) no longer satisfies the code that reads it — so "
                "either the upstream source changed its schema and the fixture must be recaptured, or "
                "the validator upstream now demands something the doc's object model doesn't mention."
            ),
            "",
            "```",
            result.rejected[:1500],
            "```",
            "",
        ]

    if result.missing:
        lines += [
            "## No longer produced",
            "",
            (
                "These example items exist in `examples/` but the transformer does not emit them any "
                "more. An id format change, a filtering change or a cardinality change will all look "
                "like this — and each of those is also a statement the source doc makes."
            ),
            "",
        ]
        for item_id, path, closest in result.missing[:MAX_ITEMS_REPORTED]:
            link = f"[`{path.relative_to(ROOT)}`](https://github.com/{THIS_REPO}/blob/main/{path.relative_to(ROOT)})"
            suggestion = f" — closest item now generated: `{closest}`" if closest else ""
            lines.append(f"- `{item_id}` in {link}{suggestion}")
        lines.append("")

    if result.changed:
        lines += [
            "## Produced, but different",
            "",
            "Same id, different content. Every line below is a claim the doc's field tables may also make.",
            "",
        ]
        for item_id, path, diffs in result.changed[:MAX_ITEMS_REPORTED]:
            lines += [f"### `{item_id}`", "", f"`{path.relative_to(ROOT)}` (committed → regenerated)", "", "```"]
            lines += diffs[:MAX_DIFFS_PER_ITEM]
            if len(diffs) > MAX_DIFFS_PER_ITEM:
                lines.append(f"… {len(diffs) - MAX_DIFFS_PER_ITEM} more difference(s)")
            lines += ["```", ""]

    lines += [
        "## How to close this",
        "",
        (
            "1. Decide which side is right. The transformer usually is — "
            f"[METHODOLOGY.md](https://github.com/{THIS_REPO}/blob/main/docs/model/sources/METHODOLOGY.md)"
            " rule 3 makes hand-written examples provisional until regenerated from it."
        ),
        "2. Regenerate the affected examples:",
        "",
        "```sh",
        f"python scripts/check_example_drift.py --source {src['id']} --diff   # inspect",
        f"python scripts/check_example_drift.py --source {src['id']} --write  # rewrite examples/",
        "```",
        "",
        (
            f"3. Update the parts of `{doc}` those items contradict, and run `npm test` "
            "(schema + hazard-code validation) before pushing."
        ),
        "",
        REPORTED_MARKER.format(_state_hash(result)),
    ]
    return "\n".join(lines)


def _state_hash(result: Result) -> str:
    """A stable digest of *what* is currently wrong, so re-running only
    notifies when the situation actually changes. Reuses the reported-through
    marker slot that check_etl_drift.py fills with a commit sha."""
    import hashlib

    payload = json.dumps(
        {
            "rejected": result.rejected,
            "missing": sorted(item_id for item_id, _, _ in result.missing),
            "changed": {item_id: diffs for item_id, _, diffs in result.changed},
        },
        sort_keys=True,
    )
    return hashlib.sha1(payload.encode()).hexdigest()


def write_examples(result: Result, recipe: dict[str, Any]) -> list[Path]:
    """Rewrite the committed examples from the regenerated output, in place.

    Only files that already exist are touched: examples/ is curated, and this
    tool has no opinion about which of the several hundred generated items
    deserve to be worked examples."""
    written: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="monty-regen-") as tmp:
        out = Path(tmp)
        regenerate(recipe["batch"], ROOT / recipe["input"], out)
        generated = load_items(out)
        for path, committed in committed_items(result.source, recipe):
            key = (committed.get("collection") or "", committed["id"])
            if key not in generated:
                continue  # id changed: which generated item replaces it is a human call
            fresh = generated[key]
            # Keep the links the repo curates (relative catalog links between
            # the committed examples); everything else comes from upstream.
            fresh["links"] = committed.get("links", [])
            path.write_text(json.dumps(fresh, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            written.append(path)
    return written


def publish(result: Result, recipe: dict[str, Any], watch: dict[str, Any]) -> str:
    labels = list((watch.get("defaults") or {}).get("labels") or ["documentation"])
    assignees, _ = resolve_assignees([], watch)
    return upsert_issue(
        title=f"Examples no longer reproducible: {result.source['name']} ({result.source['id']})",
        body=render_issue(result, recipe),
        labels=labels,
        assignees=assignees,
        marker_text=marker("examples", result.source["id"]),
        new_state_comment=(
            "The set of examples that no longer reproduce has changed — see the updated issue body. "
            "The companion `Source doc drift` issue, if open, names the upstream commits behind it."
        ),
    )


# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="print instead of creating issues")
    parser.add_argument("--diff", action="store_true", help="print the full field diffs (implies --dry-run)")
    parser.add_argument("--write", action="store_true", help="rewrite the affected examples/ items in place")
    parser.add_argument("--source", action="append", help="only this source id (repeatable)")
    args = parser.parse_args()

    watch = load_watch()
    entries = watch["sources"]
    recipes = {sid: entry["regenerate"] for sid, entry in entries.items() if (entry or {}).get("regenerate")}
    if not recipes:
        print("No source declares a `regenerate:` recipe in .github/etl-watch.yml — nothing to check.")
        return 0

    results: list[tuple[Result, dict[str, Any]]] = []
    for source in load_sources():
        if source["id"] not in recipes:
            continue
        if args.source and source["id"] not in args.source:
            continue
        recipe = recipes[source["id"]]
        result = check_source(source, recipe)
        results.append((result, recipe))

    if not results:
        print("Nothing matched.")
        return 0

    publishing = not (args.dry_run or args.diff or args.write)
    print(f"Regenerating with {upstream_provenance()}")
    exit_code = 0
    for result, recipe in results:
        sid = result.source["id"]
        if result.skipped:
            print(f"{sid}: skipped — {result.skipped}")
            continue
        if not result.drifted:
            print(f"{sid}: {len(committed_items(result.source, recipe))} committed example(s) still "
                  f"reproduce exactly ({result.total_generated} items generated).")
            continue

        exit_code = 1
        if result.rejected:
            print(f"{sid}: the transformer rejected `{recipe['input']}` — {result.rejected.splitlines()[0]}")
            if publishing:
                print(f"  → {publish(result, recipe, watch)}")
            continue

        if args.write:
            written = write_examples(result, recipe)
            print(f"{sid}: rewrote {len(written)} example(s):")
            for path in written:
                print(f"  - {path.relative_to(ROOT)}")
            continue

        print(f"{sid}: {len(result.missing)} example(s) no longer produced, {len(result.changed)} changed")
        for item_id, path, closest in result.missing:
            hint = f"  → closest now generated: {closest}" if closest else ""
            print(f"  - gone: {item_id}  ({path.relative_to(ROOT)}){hint}")
        for item_id, path, diffs in result.changed:
            print(f"  - changed: {item_id}  ({path.relative_to(ROOT)})")
            for line in diffs if args.diff else diffs[:MAX_DIFFS_PER_ITEM]:
                print(f"      {line}")
            if not args.diff and len(diffs) > MAX_DIFFS_PER_ITEM:
                print(f"      … {len(diffs) - MAX_DIFFS_PER_ITEM} more (use --diff)")

        if publishing:
            print(f"  → {publish(result, recipe, watch)}")

    # Filing an issue is this tool doing its job, so a scheduled run stays
    # green. Run as a local check (--dry-run/--diff), drift is a failure.
    return 0 if publishing else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
