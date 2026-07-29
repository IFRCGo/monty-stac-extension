#!/usr/bin/env python3
"""Detect pystac-monty transformer changes that make a source doc obsolete, and
raise one issue per affected source, assigned to whoever made the change.

A source doc in docs/model/sources/ is a *contract*: it states the item id
formats, the field carriages, the hazard-code crosswalk and how many STAC items
a source record produces. The implementation of that contract lives in
IFRCGo/pystac-monty, edited by a different team on a different cadence. Nothing
links the two, so the doc rots silently — the trigger case was
https://github.com/IFRCGo/pystac-monty/pull/181, which changes IFRC DREF impact
items from one-per-impact-type to one-per-field-report and rewrites their id
format, both of which docs/model/sources/IFRC-DREF/README.md states verbatim.

What it does
------------
1. Resolves what to watch: the transformer path from each source's `etl` URL in
   docs/model/sources/sources.yml, plus the `extra_paths` (validators) in
   .github/etl-watch.yml.
2. Diffs upstream `reviewed`..HEAD (and, unless --no-open-prs, reads open PRs)
   for changes to those paths.
3. Classifies the *net* changed lines — lines that a pure reindent or move
   leaves unchanged are dropped first, so a refactor doesn't page anyone.
   A change is reported only if at least one line matches a SIGNAL_RULE, i.e.
   touches something a source doc actually claims. Logging, error handling and
   comments are noise and never raise an issue on their own.
4. Opens (or updates) one issue per source, assigned to the upstream authors,
   naming the doc sections to re-check and quoting the evidence.

The detector is deliberately deterministic and explainable: every line in the
issue points at the rule that flagged it, so a false positive is a rule to fix
rather than a mystery. It errs towards reporting — a spurious issue costs a
close, a missed one ships a wrong mapping to every Monty consumer.

Usage
-----
    python scripts/check_etl_drift.py --dry-run          # print, touch nothing
    python scripts/check_etl_drift.py --source ifrcevent # one source
    python scripts/check_etl_drift.py --since 2026-01-01 # sweep a backlog
    python scripts/check_etl_drift.py --check-config     # offline, CI runs this
    python scripts/check_etl_drift.py                    # create/update issues

Needs a GitHub token in GH_TOKEN/GITHUB_TOKEN, or a logged-in `gh` CLI.
Reading pystac-monty needs no special scope (it is public); writing issues here
needs `issues: write`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_sources_index import load_sources  # noqa: E402  (shares sources.yml validation)

ROOT = Path(__file__).resolve().parent.parent
WATCH_YML = ROOT / ".github" / "etl-watch.yml"
THIS_REPO = "IFRCGo/monty-stac-extension"
API = "https://api.github.com"

# Marker comments make the issue its own state store: the detector finds the
# open issue for a source by ID_MARKER and knows what it has already reported
# from REPORTED_MARKER, so re-running is idempotent without committing state.
REPORTED_MARKER = "<!-- etl-watch:reported-through={} -->"
REPORTED_RE = re.compile(r"<!-- etl-watch:reported-through=([0-9a-f]{7,40}) -->")


def marker(kind: str, source_id: str) -> str:
    """`kind` separates the two families of issue this tooling raises:
    `source` for transformer-diff drift (this script) and `examples` for
    regenerated-output drift (check_example_drift.py, which imports this)."""
    return f"<!-- etl-watch:{kind}={source_id} -->"

# How much evidence to quote before it stops helping.
MAX_LINES_PER_RULE = 4
MAX_OPEN_PRS = 30


@dataclass(frozen=True)
class Rule:
    """A pattern whose appearance in a changed line means the source doc may
    now be wrong. `doc_section` names where in the doc to look — the section
    names are SOURCE_TEMPLATE.md's, which the older docs approximate."""

    id: str
    doc_section: str
    why: str
    pattern: re.Pattern[str]
    scope: str = "any"  # "any" | "validators"


def _rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern)


# Ordered by how loudly each implies the doc is stale. A line is attributed to
# the first rule that matches it.
SIGNAL_RULES: tuple[Rule, ...] = (
    Rule(
        "item-id",
        "Object → Event/Hazard/Impact/Response — the `id` row",
        "the id an item is published under is quoted verbatim in the doc",
        _rx(r"\.id\s*=|_ID_PREFIX\b|def\s+get_\w*_id\b"),
    ),
    Rule(
        "monty-fields",
        "the per-type field-carriage tables",
        "which monty: fields the transformer sets is the body of those tables",
        _rx(
            r"\bmonty\.\w+\s*=|MontyExtension|monty:[a-z_]+|"
            r"(?:Impact|Hazard)Detail\s*\(|"
            r"\b(?:impact_detail|hazard_detail|hazard_codes|country_codes|episode_number|"
            r"correlation_id|corr_id|src_(?:event|hazard|impact)_id)\b"
        ),
    ),
    Rule(
        "hazard-mapping",
        "Hazard codes",
        "the hazard-code crosswalk table is a copy of this mapping",
        _rx(r"hazard_code|get_hazard_codes|hazard_profiles|\b(?:GH|MH|TL|BI|EN|CH|SO)\d{4}\b|glide|undrr"),
    ),
    Rule(
        "cardinality",
        "Object model — how many items one source record yields",
        "iteration/emission changes alter the item count the doc describes",
        _rx(r"^for\s+[\w,\s()]+\s+in\s+.+:$|items\.append\(|\.clone\(\)|^yield\b"),
    ),
    Rule(
        "value-mapping",
        "the per-type field-carriage tables",
        "source-field → Monty-enum maps are transcribed into the doc tables",
        _rx(r"\b\w*(?:map|mapping)\w*\s*[:=]|Monty(?:Impact|Estimate|Exposure)\w*\.|CategoryValue|_category_map\b"),
    ),
    Rule(
        "stac-structure",
        "Collections, and the item structure rows",
        "collection membership, roles, assets and link relations are documented",
        _rx(
            r"properties\[|\broles\b|set_collection|get_\w+_collection|"
            r"add_asset|add_link|Asset\(|Link\(|\brel\s*=|Extent\(|Collection\("
        ),
    ),
    Rule(
        "spatiotemporal",
        "the datetime and geometry rows of the carriage tables",
        "how geometry and time are derived is stated per type",
        _rx(r"\bgeometry\b|\bbbox\b|shape\(|Point\(|Polygon\(|\b(?:start_datetime|end_datetime|datetime)\b"),
    ),
    Rule(
        "vocabulary",
        "the enumerated vocabularies (accepted types, categories)",
        "module-level constants are the lists the doc reproduces",
        _rx(r"^[A-Z][A-Z0-9_]{2,}\s*(?::[^=]+)?="),
    ),
    Rule(
        "selection",
        "Data access — which records are ingested at all",
        "filtering rules decide what the collections contain",
        _rx(r"\bcontinue\b|issubset|\bfilter\w*\(|\bexclude\w*\b"),
    ),
    Rule(
        "data-access",
        "Data access — endpoints, parameters, pagination",
        "the doc lists base URLs, endpoints and query parameters",
        _rx(r"https?://|\bendpoint\b|\bparams\b|requests\.(?:get|post)|\bpage_size\b|\bapi/v\d"),
    ),
    Rule(
        "source-model",
        "Object model — the upstream fields Monty reads",
        "validator fields are the source object model the doc tables start from",
        _rx(r"^\s*[a-z_][a-z0-9_]*\s*:\s*[A-Za-z\[\"']|class\s+\w+\(.*BaseModel"),
        scope="validators",
    ),
    Rule(
        "signature",
        "Object model — which items the transformer emits",
        "a new or removed make_*/get_* entry point changes what is produced",
        _rx(r"^def\s+(?:make|get|transform)_\w+\("),
    ),
)

# Checked before the signal rules: these lines never constitute documented
# behaviour, whatever else they happen to contain (a logged hazard code is not
# a hazard-code mapping).
NOISE_RULES: tuple[re.Pattern[str], ...] = (
    _rx(r"^#"),
    _rx(r'^(?:"""|\'\'\')'),
    _rx(r"^(?:import|from)\s+\S+"),
    _rx(r"\b(?:logger|logging)\.\w+|^print\("),
    _rx(r"transform_summary|increment_(?:failed|processed)_rows|mark_as_(?:started|complete)"),
    _rx(r"^(?:try|except|finally|raise|assert|pass|else)\b"),
    _rx(r"^@\w+"),
)


@dataclass
class Finding:
    rule: Rule
    path: str
    lineno: int | None
    kind: str  # "+" or "-"
    text: str


@dataclass
class Drift:
    source: dict[str, Any]
    paths: list[str]
    base: str
    head: str
    commits: list[dict[str, Any]] = field(default_factory=list)
    prs: list[dict[str, Any]] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    structural: list[dict[str, str]] = field(default_factory=list)
    unreviewable: list[str] = field(default_factory=list)

    @property
    def drifted(self) -> bool:
        return bool(self.findings or self.structural or self.unreviewable)

    @property
    def authors(self) -> list[str]:
        seen = {c["login"] for c in self.commits if c["login"]}
        seen |= {p["login"] for p in self.prs if p["login"]}
        return sorted(seen)


# --------------------------------------------------------------------------- #
# diff classification
# --------------------------------------------------------------------------- #

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def net_changed_lines(patch: str) -> list[tuple[str, int | None, str]]:
    """Return the (kind, new-file line number, text) of lines a hunk genuinely
    adds or removes.

    A line that is removed and re-added inside the same hunk with different
    leading whitespace is a move, not a change — reindenting a block (wrapping
    it in a new loop, for instance) otherwise marks every line of the block as
    changed and buries the two lines that actually differ. Matching added
    against removed lines on stripped text drops exactly those."""
    changed: list[tuple[str, int | None, str]] = []
    for hunk in _split_hunks(patch):
        added = [(no, text) for kind, no, text in hunk if kind == "+"]
        removed = [(no, text) for kind, no, text in hunk if kind == "-"]
        removed_pool = Counter(text.strip() for _, text in removed)
        added_pool = Counter(text.strip() for _, text in added)

        for lineno, text in added:
            if removed_pool[text.strip()]:
                removed_pool[text.strip()] -= 1
                continue
            changed.append(("+", lineno, text.strip()))
        for _, text in removed:
            if added_pool[text.strip()]:
                added_pool[text.strip()] -= 1
                continue
            changed.append(("-", None, text.strip()))
    return changed


def _split_hunks(patch: str) -> list[list[tuple[str, int | None, str]]]:
    hunks: list[list[tuple[str, int | None, str]]] = []
    current: list[tuple[str, int | None, str]] = []
    in_hunk = False
    lineno = 0
    for raw in patch.splitlines():
        match = HUNK_RE.match(raw)
        if match:
            if current:
                hunks.append(current)
            current = []
            in_hunk = True
            lineno = int(match.group(1))
            continue
        if not in_hunk:
            continue  # file header lines before the first hunk
        if raw.startswith("+"):
            current.append(("+", lineno, raw[1:]))
            lineno += 1
        elif raw.startswith("-"):
            current.append(("-", None, raw[1:]))
        else:
            lineno += 1
    if current:
        hunks.append(current)
    return hunks


def classify(path: str, patch: str) -> list[Finding]:
    """Attribute each net changed line to the first signal rule it matches."""
    scope = "validators" if "/validators/" in path else "sources"
    findings: list[Finding] = []
    for kind, lineno, text in net_changed_lines(patch):
        if not text or any(rule.search(text) for rule in NOISE_RULES):
            continue
        for rule in SIGNAL_RULES:
            if rule.scope != "any" and rule.scope != scope:
                continue
            if rule.pattern.search(text):
                findings.append(Finding(rule, path, lineno, kind, text))
                break
    return findings


# --------------------------------------------------------------------------- #
# GitHub
# --------------------------------------------------------------------------- #


def _token() -> str:
    for env in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(env):
            return os.environ[env]
    try:
        return subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit(
            "No GitHub token: set GH_TOKEN/GITHUB_TOKEN, or log in with `gh auth login`."
        )


def api(path: str, method: str = "GET", body: dict[str, Any] | None = None) -> Any:
    url = path if path.startswith("http") else f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {_token()}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request) as response:
            payload = response.read()
            return json.loads(payload) if payload else None
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:400]
        raise SystemExit(f"GitHub API {method} {url} failed ({error.code}): {detail}")


def is_assignable(login: str) -> bool:
    """Assigning a non-collaborator silently drops the assignee, so the issue
    would land on nobody. Check first, and fall back to @-mentioning."""
    request = urllib.request.Request(f"{API}/repos/{THIS_REPO}/assignees/{login}")
    request.add_header("Authorization", f"Bearer {_token()}")
    try:
        with urllib.request.urlopen(request) as response:
            return response.status == 204
    except urllib.error.HTTPError:
        return False


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #

ETL_URL_RE = re.compile(r"^https://github\.com/(?P<repo>[^/]+/[^/]+)/blob/(?P<ref>[^/]+)/(?P<path>.+)$")


def load_watch() -> dict[str, Any]:
    return yaml.safe_load(WATCH_YML.read_text(encoding="utf-8"))


def watched_paths(source: dict[str, Any], watch_entry: dict[str, Any]) -> list[str]:
    match = ETL_URL_RE.match(source["etl"])
    if not match:
        raise SystemExit(f"{source['id']}: `etl` in sources.yml is not a github blob URL: {source['etl']}")
    return [match.group("path"), *watch_entry.get("extra_paths", [])]


def _check_regenerate(sid: str, entry: dict[str, Any]) -> list[str]:
    """`regenerate` drives check_example_drift.py, which is expensive to run;
    validate its shape here so a typo surfaces in CI in a second rather than in
    the nightly job."""
    recipe = entry.get("regenerate")
    if recipe is None:
        return []
    if not isinstance(recipe, dict):
        return [f"{sid}: `regenerate` must be a mapping with `batch` and `input`"]

    errors = []
    for key in ("batch", "input"):
        if not isinstance(recipe.get(key), str) or not recipe[key]:
            errors.append(f"{sid}: `regenerate.{key}` is required and must be a non-empty string")
    fixture = recipe.get("input")
    if isinstance(fixture, str) and not (ROOT / fixture).exists():
        errors.append(f"{sid}: `regenerate.input` points at {fixture!r}, which does not exist in this repo")
    covers = recipe.get("covers")
    if covers is not None and not (isinstance(covers, list) and all(isinstance(p, str) for p in covers)):
        errors.append(f"{sid}: `regenerate.covers` must be a list of item-id globs")
    return errors


def check_config(sources: list[dict[str, Any]], watch: dict[str, Any]) -> int:
    """Offline invariants, so a source added to sources.yml can't quietly go
    unwatched. Run by CI next to gen_sources_index.py --check."""
    errors: list[str] = []
    entries = watch.get("sources") or {}

    if not re.fullmatch(r"[\w.-]+/[\w.-]+", str(watch.get("repo", ""))):
        errors.append(f"repo must be 'owner/name' (got {watch.get('repo')!r})")

    by_id = {src["id"]: src for src in sources}
    for sid in sorted(entries.keys() - by_id.keys()):
        errors.append(f"{sid}: watched here but absent from sources.yml")

    for src in sources:
        sid = src["id"]
        if src["etl"] is None:
            if sid in entries:
                errors.append(f"{sid}: watched here but has no `etl` in sources.yml")
            continue
        if sid not in entries:
            errors.append(f"{sid}: has an `etl` transformer but no entry in {WATCH_YML.name} — add one")
            continue

        entry = entries[sid] or {}
        match = ETL_URL_RE.match(src["etl"])
        if not match:
            errors.append(f"{sid}: `etl` is not a github blob URL: {src['etl']}")
        elif match.group("repo") != watch["repo"]:
            errors.append(f"{sid}: `etl` points at {match.group('repo')}, not the watched {watch['repo']}")

        reviewed = str(entry.get("reviewed", ""))
        if not re.fullmatch(r"[0-9a-f]{40}", reviewed):
            errors.append(f"{sid}: `reviewed` must be a full 40-character commit sha (got {reviewed!r})")

        for path in entry.get("extra_paths", []):
            if not isinstance(path, str) or path.startswith("/") or ".." in path:
                errors.append(f"{sid}: extra_paths entry {path!r} must be a repo-relative path")

        errors.extend(_check_regenerate(sid, entry))

    if errors:
        print(f"{WATCH_YML.relative_to(ROOT)} is inconsistent ({len(errors)} problem(s)):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"{WATCH_YML.relative_to(ROOT)} is in sync with sources.yml ({len(entries)} watched sources).")
    return 0


# --------------------------------------------------------------------------- #
# drift collection
# --------------------------------------------------------------------------- #


def collect_merged(repo: str, drift: Drift) -> None:
    """Everything merged into the default branch between the reviewed commit
    and HEAD, restricted to the watched paths."""
    if drift.base == drift.head:
        return
    comparison = api(f"/repos/{repo}/compare/{drift.base}...{drift.head}")
    watched = set(drift.paths)

    changed_files = [f for f in comparison.get("files", []) if f["filename"] in watched]
    if not changed_files:
        return

    for file in changed_files:
        # A file that appeared, vanished or moved says everything by its status:
        # line-classifying a whole new transformer flags every line it contains
        # and drowns the report in evidence nobody needs.
        if file["status"] != "modified":
            drift.structural.append(
                {
                    "path": file["filename"],
                    "status": file["status"],
                    "previous": file.get("previous_filename", ""),
                }
            )
            continue
        patch = file.get("patch")
        if not patch:
            # The compare endpoint omits patches for very large diffs; say so
            # rather than silently reporting "no signals".
            drift.unreviewable.append(file["filename"])
            continue
        drift.findings.extend(classify(file["filename"], patch))

    if not drift.drifted:
        return

    for commit in comparison.get("commits", []):
        touched = api(f"/repos/{repo}/commits/{commit['sha']}")
        if not any(f["filename"] in watched for f in touched.get("files", [])):
            continue
        drift.commits.append(
            {
                "sha": commit["sha"],
                "short": commit["sha"][:8],
                "title": commit["commit"]["message"].splitlines()[0],
                "login": (commit.get("author") or {}).get("login"),
                "url": commit["html_url"],
                "date": commit["commit"]["author"]["date"][:10],
            }
        )


def collect_open_prs(repo: str, drifts: dict[str, Drift]) -> None:
    """Open PRs are reported as a heads-up in the same issue: catching drift
    while the transformer PR is still open is what lets the doc update land in
    the same week rather than months later."""
    by_path: dict[str, list[Drift]] = {}
    for drift in drifts.values():
        for path in drift.paths:
            by_path.setdefault(path, []).append(drift)

    # Drafts are included on purpose: upstream opens transformer work as a
    # draft and keeps it there for weeks (pystac-monty#181 among them), so
    # skipping them would miss the window this heads-up exists for.
    pulls = api(f"/repos/{repo}/pulls?state=open&sort=updated&direction=desc&per_page={MAX_OPEN_PRS}")
    for pull in pulls:
        files = api(f"/repos/{repo}/pulls/{pull['number']}/files?per_page=100")
        for file in files:
            for drift in by_path.get(file["filename"], []):
                patch = file.get("patch")
                findings = classify(file["filename"], patch) if patch else []
                if not findings:
                    continue
                drift.findings.extend(findings)
                if not any(p["number"] == pull["number"] for p in drift.prs):
                    drift.prs.append(
                        {
                            "number": pull["number"],
                            "title": pull["title"],
                            "login": (pull.get("user") or {}).get("login"),
                            "url": pull["html_url"],
                            "draft": bool(pull.get("draft")),
                        }
                    )


# --------------------------------------------------------------------------- #
# issue rendering
# --------------------------------------------------------------------------- #


def render_issue(drift: Drift, repo: str, mentions: list[str]) -> str:
    src = drift.source
    doc = f"docs/model/sources/{src['doc']}"
    lines = [
        marker("source", src["id"]),
        (
            f"The **{src['name']}** transformer changed upstream in ways that touch what "
            f"[`{doc}`](https://github.com/{THIS_REPO}/blob/main/{doc}) documents. Raised automatically "
            f"by [`scripts/check_etl_drift.py`](https://github.com/{THIS_REPO}/blob/main/scripts/"
            "check_etl_drift.py)."
        ),
        "",
        f"- **Source doc:** `{doc}`",
        f"- **Watched upstream files:** {', '.join(f'`{p}`' for p in drift.paths)}",
        f"- **Reviewed through:** [`{drift.base[:8]}`](https://github.com/{repo}/commit/{drift.base})",
        "",
    ]

    if drift.commits:
        lines += ["## Merged upstream changes", ""]
        for commit in drift.commits:
            who = f"@{commit['login']}" if commit["login"] else "unknown author"
            lines.append(f"- [`{commit['short']}`]({commit['url']}) {commit['title']} — {who}, {commit['date']}")
        lines.append("")

    if drift.prs:
        lines += [
            "## Open pull requests that will cause drift",
            "",
            "Not merged yet — updating the doc alongside them keeps the two in step.",
            "",
        ]
        for pull in drift.prs:
            who = f"@{pull['login']}" if pull["login"] else "unknown author"
            state = " _(draft)_" if pull.get("draft") else ""
            lines.append(f"- [#{pull['number']}]({pull['url']}) {pull['title']} — {who}{state}")
        lines.append("")

    lines += ["## What to re-check", ""]

    if drift.structural:
        lines += ["### Files added, removed or moved upstream", ""]
        for entry in drift.structural:
            if entry["status"] == "added":
                lines.append(
                    f"- `{entry['path']}` was **added** — the mapping it implements is new, so read the "
                    "whole doc against it rather than a diff."
                )
            elif entry["status"] in ("removed", "renamed") and entry["previous"]:
                lines.append(
                    f"- `{entry['previous']}` was **renamed** to `{entry['path']}` — update the `etl` URL in "
                    "`sources.yml` and/or `extra_paths` in `.github/etl-watch.yml`, or this source stops "
                    "being watched."
                )
            else:
                lines.append(
                    f"- `{entry['path']}` was **{entry['status']}** — the doc, its `etl` link in "
                    "`sources.yml` and the source `status` may all be wrong now."
                )
        lines.append("")

    for rule, findings in _group_by_rule(drift.findings):
        lines += [
            f"### `{rule.id}` — {rule.doc_section}",
            "",
            f"_{rule.why}._",
            "",
            "```diff",
        ]
        for finding in findings[:MAX_LINES_PER_RULE]:
            where = f"{finding.path}:{finding.lineno}" if finding.lineno else finding.path
            lines.append(f"{finding.kind} {finding.text}   # {where}")
        if len(findings) > MAX_LINES_PER_RULE:
            lines.append(f"# … {len(findings) - MAX_LINES_PER_RULE} more line(s) matched this rule")
        lines += ["```", ""]

    if drift.unreviewable:
        lines += [
            "### Not classified",
            "",
            "The diff was too large for GitHub to return a patch for these files — review them by hand:",
            "",
            *[f"- `{path}`" for path in drift.unreviewable],
            "",
        ]

    if mentions:
        lines += [
            "## Authors",
            "",
            (
                f"{', '.join('@' + m for m in mentions)} — you made these changes upstream but can't be "
                "assigned here (not a collaborator on this repo), so this is a mention instead."
            ),
            "",
        ]

    lines += [
        "## How to close this",
        "",
        f"1. Re-read the sections above in `{doc}` against the upstream code and fix what no longer holds.",
        (
            "2. Regenerate or hand-check the affected `examples/` items — they are the doc's worked "
            f"proof (see [METHODOLOGY.md](https://github.com/{THIS_REPO}/blob/main/docs/model/sources/"
            "METHODOLOGY.md), rule 3), and `scripts/check_example_drift.py` reports on them where a "
            "fixture exists."
        ),
        (
            f"3. In the same PR, bump `sources.{src['id']}.reviewed` in "
            f"[`.github/etl-watch.yml`](https://github.com/{THIS_REPO}/blob/main/.github/etl-watch.yml) "
            f"to [`{drift.head[:8]}`](https://github.com/{repo}/commit/{drift.head}) and close this issue."
        ),
        "",
        (
            "If nothing in the doc was actually wrong, bump `reviewed` anyway and close — that records "
            "the review and stops this being re-reported."
        ),
        "",
        REPORTED_MARKER.format(drift.head),
    ]
    return "\n".join(lines)


def _group_by_rule(findings: list[Finding]) -> list[tuple[Rule, list[Finding]]]:
    grouped: dict[str, list[Finding]] = {}
    for finding in findings:
        grouped.setdefault(finding.rule.id, []).append(finding)
    order = {rule.id: index for index, rule in enumerate(SIGNAL_RULES)}
    return [
        (findings[0].rule, findings)
        for findings in sorted(grouped.values(), key=lambda group: order[group[0].rule.id])
    ]


def existing_issue(labels: list[str], marker_text: str) -> dict[str, Any] | None:
    query = urllib.parse.urlencode({"state": "open", "labels": ",".join(labels), "per_page": 100})
    for issue in api(f"/repos/{THIS_REPO}/issues?{query}"):
        if marker_text in (issue.get("body") or ""):
            return issue
    return None


def ensure_labels(labels: list[str]) -> None:
    existing = {label["name"] for label in api(f"/repos/{THIS_REPO}/labels?per_page=100")}
    for label in labels:
        if label in existing:
            continue
        api(
            f"/repos/{THIS_REPO}/labels",
            method="POST",
            body={
                "name": label,
                "color": "b60205",
                "description": "Source doc may be stale relative to the pystac-monty transformer",
            },
        )


def resolve_assignees(authors: list[str], watch: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Split upstream authors into who can be assigned here and who can only be
    mentioned, falling back to the configured maintainers when nobody upstream
    is a collaborator on this repo."""
    defaults = watch.get("defaults") or {}
    assignees = [login for login in authors if is_assignable(login)]
    mentions = [login for login in authors if login not in assignees]
    if not assignees:
        assignees = [login for login in (defaults.get("fallback_assignees") or []) if is_assignable(login)]
    return assignees, mentions


def upsert_issue(
    *,
    title: str,
    body: str,
    labels: list[str],
    assignees: list[str],
    marker_text: str,
    new_state_comment: str | None = None,
) -> str:
    """Create the issue, or refresh the one already carrying `marker_text`.

    Re-running must be free: the body is rewritten in place every time, and a
    comment (which notifies subscribers) is only posted when the state marker
    in the existing body has actually moved on."""
    ensure_labels(labels)
    issue = existing_issue(labels, marker_text)
    if issue is None:
        created = api(
            f"/repos/{THIS_REPO}/issues",
            method="POST",
            body={"title": title, "body": body, "labels": labels, "assignees": assignees},
        )
        return f"opened {created['html_url']}"

    previous = REPORTED_RE.search(issue.get("body") or "")
    current = REPORTED_RE.search(body)
    api(
        f"/repos/{THIS_REPO}/issues/{issue['number']}",
        method="PATCH",
        body={
            "body": body,
            "assignees": sorted({a["login"] for a in issue.get("assignees", [])} | set(assignees)),
        },
    )
    moved_on = current and (not previous or previous.group(1) != current.group(1))
    if moved_on and new_state_comment:
        api(f"/repos/{THIS_REPO}/issues/{issue['number']}/comments", method="POST", body={"body": new_state_comment})
        return f"updated {issue['html_url']} (new drift)"
    return f"refreshed {issue['html_url']}"


def publish(drift: Drift, repo: str, watch: dict[str, Any]) -> str:
    labels = list((watch.get("defaults") or {}).get("labels") or ["documentation"])
    assignees, mentions = resolve_assignees(drift.authors, watch)
    return upsert_issue(
        title=f"Source doc drift: {drift.source['name']} ({drift.source['id']})",
        body=render_issue(drift, repo, mentions),
        labels=labels,
        assignees=assignees,
        marker_text=marker("source", drift.source["id"]),
        new_state_comment=(
            "More upstream drift landed since this issue was last updated — now reported through "
            f"[`{drift.head[:8]}`](https://github.com/{repo}/commit/{drift.head}). "
            "See the issue body for the current list."
        ),
    )


# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check-config", action="store_true", help="validate etl-watch.yml offline and exit")
    parser.add_argument("--dry-run", action="store_true", help="print the issues instead of creating them")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON (implies --dry-run)")
    parser.add_argument("--source", action="append", help="only this source id (repeatable)")
    parser.add_argument("--since", help="override the reviewed baseline with a sha, tag or YYYY-MM-DD")
    parser.add_argument("--no-open-prs", action="store_true", help="only look at merged commits")
    args = parser.parse_args()

    sources = load_sources()
    watch = load_watch()

    if args.check_config:
        return check_config(sources, watch)

    repo = watch["repo"]
    entries = watch["sources"]
    head = api(f"/repos/{repo}/commits/HEAD")["sha"]
    base_override = _resolve_since(repo, args.since) if args.since else None

    drifts: dict[str, Drift] = {}
    for src in sources:
        if src["etl"] is None or src["id"] not in entries:
            continue
        if args.source and src["id"] not in args.source:
            continue
        entry = entries[src["id"]] or {}
        drifts[src["id"]] = Drift(
            source=src,
            paths=watched_paths(src, entry),
            base=base_override or entry["reviewed"],
            head=head,
        )

    for drift in drifts.values():
        collect_merged(repo, drift)
    if not args.no_open_prs:
        collect_open_prs(repo, drifts)

    drifted = [d for d in drifts.values() if d.drifted]

    if args.json:
        print(json.dumps([_as_json(d) for d in drifted], indent=2))
        return 0

    if not drifted:
        print(f"No source-doc drift: {len(drifts)} source(s) checked against {repo}@{head[:8]}.")
        return 0

    for drift in drifted:
        if args.dry_run:
            print("=" * 78)
            print(f"Source doc drift: {drift.source['name']} ({drift.source['id']})")
            print(f"assignees: {', '.join(drift.authors) or '(none resolved)'}")
            print("=" * 78)
            print(render_issue(drift, repo, []))
            print()
        else:
            print(f"{drift.source['id']}: {publish(drift, repo, watch)}")

    return 0


def _resolve_since(repo: str, since: str) -> str:
    """A date is friendlier than a sha for a backlog sweep, so accept both."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", since):
        commits = api(f"/repos/{repo}/commits?until={since}T00:00:00Z&per_page=1")
        if not commits:
            raise SystemExit(f"No commit in {repo} before {since}")
        return commits[0]["sha"]
    return api(f"/repos/{repo}/commits/{since}")["sha"]


def _as_json(drift: Drift) -> dict[str, Any]:
    return {
        "source": drift.source["id"],
        "doc": drift.source["doc"],
        "base": drift.base,
        "head": drift.head,
        "authors": drift.authors,
        "commits": drift.commits,
        "prs": drift.prs,
        "structural": drift.structural,
        "unreviewable": drift.unreviewable,
        "findings": [
            {
                "rule": f.rule.id,
                "doc_section": f.rule.doc_section,
                "path": f.path,
                "line": f.lineno,
                "kind": f.kind,
                "text": f.text,
            }
            for f in drift.findings
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())
