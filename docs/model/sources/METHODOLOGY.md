# Source Analysis Methodology

How a disaster data source goes from a raw upstream feed to a running Monty
pipeline. This is the process behind every source doc in this folder, and
[`SOURCE_TEMPLATE.md`](./SOURCE_TEMPLATE.md) is the skeleton stage 2 produces.

[Charter](./Charter/README.md) and [CEMS](./CEMS/README.md) are its fullest
reference implementations — the most recent, and the closest to the template
below — so read them for the **shape** of a source doc. But every documented
source in the [source index](./README.md) is worth reading: the earlier
analyses (for example [GDACS](./GDACS/README.md), [IDMC](./IDMC/README.md),
[PDC](./PDC/README.md), [USGS](./USGS/README.md)) predate this template and use a
lighter structure, yet they carry source-specific **substance** — API quirks,
hazard-code crosswalks, field mappings — that a template can't. Read the source
closest to the one you're adding alongside CEMS/Charter.

The five stages below are reverse-engineered from the Charter and CEMS
integrations, which are identical in shape. Each stage has a concrete **output**,
a **home**, and a **gate** that must hold before the next stage starts.

## The five-stage pipeline

| Stage | Output | Where |
|-------|--------|-------|
| 1. Access & data-model familiarisation | `FINDINGS.md` + real fixtures | `docs/model/sources/<SOURCE>/FINDINGS.md` + `docs/model/sources/<SOURCE>/api-files/` |
| 2. Analysis & Monty mapping | source analysis README | `docs/model/sources/<SOURCE>/README.md` |
| 3. Collection templates + worked examples | collections + ≥1 item each | `examples/<source>-{events,hazards,impacts,response}/` |
| 4. ETL transformer spec | spec issue | [`IFRCGo/pystac-monty`](https://github.com/IFRCGo/pystac-monty) |
| 5. ETL implementation + deployment | transformer + pipeline | [`pystac-monty`](https://github.com/IFRCGo/pystac-monty) + [`montandon-etl`](https://github.com/IFRCGo/montandon-etl) |

These stages map onto the `status` field in [`sources.yml`](./sources.yml): a
source is `undocumented` before stage 1, `analysis` during stage 1, `templates`
once stage 3's mapping is fully specified, `etl` once a transformer exists
(stage 4/5), and `production` once the pipeline is proven behind the shipped
examples.

### Stage 1 — Access & data-model familiarisation

Hands-on exploration of the live source: what the endpoints/bucket are, how they
authenticate and paginate, what the payload actually contains, and which single
call is the "ETL unit". The output is a `FINDINGS.md` (see
[CEMS/FINDINGS.md](./CEMS/FINDINGS.md) for the model) plus **real** captured
payloads in `api-files/`.

**Gate:** the object model is understood well enough to name every entity Monty
will emit, and the fixtures to prove it are committed.

### Stage 2 — Analysis & Monty mapping

Write the source README from [`SOURCE_TEMPLATE.md`](./SOURCE_TEMPLATE.md): the
collections, the object model, and one field-carriage table per Monty type,
every claim grounded in a stage-1 fixture. Resolve the hazard-code crosswalk
here (see the rules below). Register the source in [`sources.yml`](./sources.yml)
and run `python scripts/gen_sources_index.py`.

**Gate:** every mapping decision is settled — the "Decisions (resolved)" table
has no open rows — so nothing blocks the ETL.

### Stage 3 — Collection templates + worked examples

Add the STAC collections and at least one worked item per collection under
`examples/<source>-<type>/`. These validate against `json-schema/schema.json`
via `npm test` and are what the README's "Examples" section links to.

**Gate:** `npm test` passes on the new examples.

### Stage 4 — ETL transformer spec

Specify the transformer as an issue in
[`pystac-monty`](https://github.com/IFRCGo/pystac-monty) — the mapping from
stage 2 restated as an implementation contract.

### Stage 5 — ETL implementation + deployment

Implement the transformer in
[`pystac-monty`](https://github.com/IFRCGo/pystac-monty) and wire it into the
pipeline in [`montandon-etl`](https://github.com/IFRCGo/montandon-etl). The
transformer becomes the source of truth for the examples (see rule 3), and the
source moves to `status: production` once the pipeline is proven.

## Rules every source doc follows

These are the unwritten conventions the recent integrations actually followed —
made explicit so the next one doesn't have to rediscover them.

1. **The taxonomy is the gate.** A mapping that needs a taxonomy or response-type
   code that doesn't exist yet is blocked until that code lands — as its **own**
   PR, first. [#50](https://github.com/IFRCGo/monty-stac-extension/issues/50)
   extended `response-taxonomy.md` with `eo-dat` *before*
   [#43](https://github.com/IFRCGo/monty-stac-extension/issues/43) could use it.

2. **Every claim is grounded in a committed fixture.** No field mapping, enum, or
   "the API ignores X" assertion goes in a source doc unless a real payload under
   `api-files/` backs it. This is what makes an analysis auditable.

3. **Hand-written examples are provisional** until regenerated from the real
   transformer. [#53](https://github.com/IFRCGo/monty-stac-extension/issues/53)
   replaced [#43](https://github.com/IFRCGo/monty-stac-extension/issues/43)'s
   by-hand examples wholesale once the transformer existed. Write examples by hand
   to prove the mapping; expect the transformer to overwrite them.

4. **`schema.json` and `README.md` field descriptions stay verbatim-identical.**
   A schema field change means editing both `json-schema/schema.json` and the
   field description in the root `README.md` in the same PR.

5. **Verify every hazard code against [`taxonomy.md`](../taxonomy.md) before
   writing the crosswalk.** A syntactically valid UNDRR-ISC 2025 code can still
   be the *wrong* code for the mapped class, and `get_canonical_hazard_codes()`
   does **not** catch that — it preserves any valid code without checking it is
   the right one for the class. The mapping must therefore be correct **at the
   source**. The
   [`scripts/check_hazard_codes.py`](https://github.com/IFRCGo/monty-stac-extension/blob/main/scripts/check_hazard_codes.py)
   checker (wired into `npm test`) verifies every code in `examples/` against
   `taxonomy.md`.

## Fixture policy

Stage-1 fixtures live in `api-files/` and are the evidence base for the whole
analysis. To keep the repo clonable:

- **Placement: `api-files/` only.** Do not scatter fixtures at the source root.
  (Charter currently has some at both levels — new sources should not.)
- **Size: trim aggressively.** Cap **new** fixtures at roughly **1 MB** — keep
  the minimum payload that grounds the claims (one representative activation, not
  the whole catalogue; drop unused fields/features where it doesn't weaken the
  evidence).
- **Leave existing large files alone.** The repo already carries some heavy
  fixtures (a 9.6 MB `IDMC/idu-export.json`, multi-MB GDACS geometry, `.zip`/
  `.xlsx`/PDF). Purging them would mean rewriting git history — changing every
  commit hash and breaking existing clones and forks — which is not worth it for
  a repo this size. The cap applies going forward.

## Keeping a doc alive after stage 5

Stage 5 hands the mapping to [`pystac-monty`](https://github.com/IFRCGo/pystac-monty),
and from then on the transformer, not this repo, decides what Monty actually
publishes. The doc keeps asserting item id formats, field carriages, hazard-code
crosswalks and item counts that a transformer PR can invalidate without anyone
here noticing —
[pystac-monty#181](https://github.com/IFRCGo/pystac-monty/pull/181) changes IFRC
DREF impact items from one-per-impact-type to one-per-field-report and rewrites
their id format, both of which [IFRC-DREF/README.md](./IFRC-DREF/README.md)
states verbatim.

Two automated checks close that loop, run daily by
[`.github/workflows/etl-drift.yml`](https://github.com/IFRCGo/monty-stac-extension/blob/main/.github/workflows/etl-drift.yml).
Both raise (and keep updating) one issue per affected source; the watch list for
both is [`.github/etl-watch.yml`](https://github.com/IFRCGo/monty-stac-extension/blob/main/.github/etl-watch.yml).

| | [`check_etl_drift.py`](https://github.com/IFRCGo/monty-stac-extension/blob/main/scripts/check_etl_drift.py) | [`check_example_drift.py`](https://github.com/IFRCGo/monty-stac-extension/blob/main/scripts/check_example_drift.py) |
|---|---|---|
| Reads | the upstream diff since `reviewed`, plus open PRs | the transformer's actual output |
| Method | classifies changed lines against rules for what a doc claims (`item-id`, `hazard-mapping`, `cardinality`, …) | re-runs the transformer over the fixtures committed here and compares with `examples/` |
| Covers | every source with an `etl` URL | sources with a `regenerate:` recipe |
| Says | "these lines suggest section X is stale", and who wrote them | "this example item is no longer produced / now differs in these fields" |

They are deliberately kept together: the first is a tripwire that always fires
and names an author to assign; the second is the evidence, and only exists where
a machine-readable fixture and a registered upstream batch exporter both exist.
Widening the second is the cheapest way to make the loop stronger — recapture a
fixture that was saved from a browser (those start with a `// timestamp`
preamble and are not valid JSON), or ask upstream to register a batch exporter
for the source.

Working on a drift issue:

```sh
python scripts/check_etl_drift.py --dry-run --source <id>       # what changed upstream
python scripts/check_example_drift.py --source <id> --diff      # what that did to the examples
python scripts/check_example_drift.py --source <id> --write     # regenerate them (rule 3)
```

> [!IMPORTANT]
> `check_example_drift.py` reports on whichever `pystac-monty` is importable, so
> install it from **`main`** — a stale local checkout replays drift that upstream
> has already fixed, which is how the first run of this tool re-reported the
> hazard-code bug [#74](https://github.com/IFRCGo/monty-stac-extension/pull/74)
> had fixed weeks earlier. Every run prints the commit it used; check it before
> acting on a result.

Then fix the doc, bump that source's `reviewed` in `.github/etl-watch.yml` to
the sha named in the issue, and close the issue in the same PR. Bump `reviewed`
even when the doc turned out to be fine — that records the review and stops the
change being re-reported.

## The document template

[`SOURCE_TEMPLATE.md`](./SOURCE_TEMPLATE.md) is the skeleton for a source README,
capturing the structure [CEMS](./CEMS/README.md) and [Charter](./Charter/README.md)
converged on: Collections → Object model (+ Mermaid) → per-type field-carriage
tables → Tracking over time → Cross-source linkage → Hazard codes → Examples →
Reference files → Decisions → Resources. Copy it to
`docs/model/sources/<SOURCE>/README.md` and fill it in. CEMS and Charter are the
worked references to read alongside it.
