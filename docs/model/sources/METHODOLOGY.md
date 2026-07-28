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
| 1. Access & data-model familiarisation | `FINDINGS.md` + real fixtures | `docs/model/sources/<SOURCE>/api-files/` |
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
   writing the crosswalk.** This is the step whose absence caused
   [#61](https://github.com/IFRCGo/monty-stac-extension/issues/61) (a tropical
   cyclone tagged `MH0403`, *Blizzard*; the non-existent `MH0901` shipped 16×).
   Note explicitly that `get_canonical_hazard_codes()` does **not** correct a
   wrong-but-valid code — it preserves any syntactically valid UNDRR-ISC 2025
   code without checking it is the *right* one for the mapped class (see
   IFRCGo/pystac-monty#168, where USGS shipped the valid-but-wrong `GH0311` for
   years). The mapping must be right **at the source**. The
   [`scripts/check_hazard_codes.py`](https://github.com/IFRCGo/monty-stac-extension/blob/main/scripts/check_hazard_codes.py)
   checker (from [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64),
   wired into `npm test`) automates the verification against `taxonomy.md`.

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

## The document template

[`SOURCE_TEMPLATE.md`](./SOURCE_TEMPLATE.md) is the skeleton for a source README,
capturing the structure [CEMS](./CEMS/README.md) and [Charter](./Charter/README.md)
converged on: Collections → Object model (+ Mermaid) → per-type field-carriage
tables → Tracking over time → Cross-source linkage → Hazard codes → Examples →
Reference files → Decisions → Resources. Copy it to
`docs/model/sources/<SOURCE>/README.md` and fill it in. CEMS and Charter are the
worked references to read alongside it.
