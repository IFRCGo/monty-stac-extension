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
scripts/                  # gen_sources_index.py + the CI and drift checks
.github/etl-watch.yml     # which transformer files each source doc is checked against
docs/model/               # taxonomy, response docs, correlation
docs/model/sources/       # per-source analyses + sources.yml (the manifest)
```

## How to check your work

```bash
npm install      # once
npm test         # markdown lint + example validation + link types + hazard codes + impact categories
```

`npm test` runs: markdown lint (root and `docs/` under a relaxed profile),
`stac-node-validator` over every `examples/**` file against the schema,
`check-link-types.mjs`, `check_hazard_codes.py`, and
`check_impact_categories.py`. CI additionally runs `mkdocs build --strict`,
`python scripts/gen_sources_index.py --check`, and
`python scripts/check_etl_drift.py --check-config` — run those if you touched
`docs/`, `sources.yml`, or `.github/etl-watch.yml`.

## Decisions that stay with people

An agent drafts, compares, and regenerates. It does not decide. Stop and ask, or
open an issue with the options and their evidence, when the task needs one of
these:

- A change to the data model, the taxonomy, or the meaning of a term.
- The acceptance of a new source, or the scope of an existing one.
- A mapping decision in the first analysis of a source, or in a major change to
  a source. A person who knows the source and the model leads this work.
- A gap that no fixture or taxonomy code fills. Record it as a known limit; do
  not fill it with a plausible value.

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

5. **The taxonomy is the gate.** A mapping that needs a hazard, impact, or
   response-type code that does not exist yet is blocked until that code lands,
   as its own change, first.

6. **Hand-written examples are provisional.** Regenerate them from the real
   transformer when it exists; do not edit a regenerated example by hand.

## Working on an `etl-drift` issue

A daily check compares each source doc with its transformer in `pystac-monty`
and opens one issue per source that diverged. Follow "Keeping a doc alive after
stage 5" in the [methodology](docs/model/sources/METHODOLOGY.md): re-read the
named doc sections against the upstream code, regenerate the examples, and bump
that source's `reviewed` sha in [`.github/etl-watch.yml`](.github/etl-watch.yml)
in the same change.

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
