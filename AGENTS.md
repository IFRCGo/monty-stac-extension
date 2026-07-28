# Agents

Brief for AI agents working in this repository. Read this first, then the file
the task points at. Keep changes small, grounded, and verified with `npm test`.

## What this repo is

The **Monty STAC Extension** — three pillars that build on each other:

1. **Spec** ([`README.md`](README.md)) — the normative `monty:*` STAC fields,
   roles and relation types. The machine-checkable form is
   [`json-schema/schema.json`](json-schema/schema.json).
2. **Model** ([`docs/model/`](docs/model/)) — the data model behind the spec: the
   canonical [hazard/impact taxonomy](docs/model/taxonomy.md), the
   [response taxonomy](docs/model/response-taxonomy.md), and the
   [event correlation](docs/model/correlation_identifier.md) algorithm.
3. **Sources** ([`docs/model/sources/`](docs/model/sources/)) — per-source
   analyses mapping real disaster feeds onto the model, indexed by
   [`sources.yml`](docs/model/sources/sources.yml).

The transformers that execute these mappings live in a **separate** repo,
[`IFRCGo/pystac-monty`](https://github.com/IFRCGo/pystac-monty) (which vendors
this repo as a submodule); the deployed pipeline is
[`IFRCGo/montandon-etl`](https://github.com/IFRCGo/montandon-etl).

## Repository map

```text
README.md                 # normative extension spec
CONTRIBUTING.md           # contribution paths + release procedure
json-schema/schema.json   # machine-checkable spec
examples/                 # STAC Items/Collections, one set per source-collection
scripts/                  # gen_sources_index.py + the CI checks
docs/model/               # taxonomy, response docs, correlation
docs/model/sources/       # per-source analyses + sources.yml (the manifest)
```

## How to check your work

```bash
npm install      # once
npm test         # markdown lint + example validation + link types + hazard codes
```

`npm test` runs: markdown lint (root and `docs/` under a relaxed profile),
`stac-node-validator` over every `examples/**` file against the schema,
`check-link-types.mjs`, and `check_hazard_codes.py`. The docs site additionally
builds under `mkdocs build --strict` and `python scripts/gen_sources_index.py
--check` in CI — run those if you touched `docs/` or `sources.yml`.

## Invariants — do not violate these

1. **`docs/model/taxonomy.md` is canonical for hazard codes.** Verify every code
   against it before writing a crosswalk — a syntactically valid UNDRR-ISC 2025
   code can still be the *wrong* code for the class, and canonicalisation does not
   catch that. See [the hazard-code procedure](.claude/skills/add-monty-source/references/hazard-code-verification.md).

2. **`monty:corr_id` is not a cross-source join key.** Its format is
   `{datetime}-{country_code}-{block_id}-{hazard_code}-{episode_number}-GCDB`, and
   it is **deterministic and per-source**: suitable for intra-source pairing and
   exact lookups only. Two sources describing the same event will usually compute
   **different** `corr_id`s (date, normalization, `block_id`, or episode differ).
   To correlate *across* sources, use the dynamic algorithms in
   [`docs/model/correlation_identifier.md`](docs/model/correlation_identifier.md),
   never a `corr_id` equality join. An agent that gets this wrong industrialises
   the misconception across every source it touches.

3. **`schema.json` and `README.md` field descriptions stay verbatim-identical.**
   A schema field change means editing both
   [`json-schema/schema.json`](json-schema/schema.json) and the field description
   in [`README.md`](README.md) in the same change.

4. **Every claim is grounded in a committed fixture.** No field mapping, enum, or
   "the API does X" assertion goes into a source doc unless a real payload under
   that source's `api-files/` backs it.

## Adding or changing a source

Follow the five-stage [methodology](docs/model/sources/METHODOLOGY.md) and write
the source README from
[`SOURCE_TEMPLATE.md`](docs/model/sources/SOURCE_TEMPLATE.md); the
[`add-monty-source`](.claude/skills/add-monty-source/SKILL.md) skill drives that
workflow end-to-end. Register the source in
[`sources.yml`](docs/model/sources/sources.yml) and run
`python scripts/gen_sources_index.py` to regenerate the derived indexes.
[CEMS](docs/model/sources/CEMS/README.md) and
[Charter](docs/model/sources/Charter/README.md) are the worked references.
