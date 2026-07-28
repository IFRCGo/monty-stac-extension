---
name: add-monty-source
description: >-
  Use when adding a new disaster data source to the Monty STAC Extension, or
  advancing an existing source doc through its lifecycle. Drives the five-stage
  source-analysis pipeline — API/data-model familiarisation, the Monty mapping,
  worked examples, and handoff to the pystac-monty transformer — producing a
  FINDINGS.md, a source README, example collections, and a sources.yml entry.
---

# Add a Monty source

This skill *orchestrates* the source-analysis pipeline. It does not restate the
method or the doc structure — those are the canonical, human-readable truth:

- **`docs/model/sources/METHODOLOGY.md`** — the five stages, their gates, and the
  rules every source doc follows. Read it first.
- **`docs/model/sources/SOURCE_TEMPLATE.md`** — the source-README skeleton. Copy
  it; do not reproduce its structure here.
- **`docs/model/sources/CEMS/README.md`** and **`.../Charter/README.md`** — the
  worked reference implementations.

Follow the stages in order. **Do not start a stage until the previous stage's
gate holds.** Ground every claim in a committed fixture (see the rules in
`METHODOLOGY.md`), and obey the invariants in the repo-root `AGENTS.md` — the
hazard-code and `corr_id` ones especially.

## 0. Pick the source

Confirm the target and its current state in `docs/model/sources/sources.yml`. A
source with example collections but no doc (`status: undocumented`) is the
natural candidate — `alerthub` is one. Note the `id`, and the collections that
already exist under `examples/<id>-*/`.

## 1. Familiarisation → `FINDINGS.md` + `api-files/`

Explore the live source hands-on: endpoints/bucket, auth, pagination, the payload
shape, and which single call is the "ETL unit". Capture **real** payloads to
`docs/model/sources/<SOURCE>/api-files/` (trimmed — see the fixture policy in
`METHODOLOGY.md`), and write the raw notes to
`docs/model/sources/<SOURCE>/FINDINGS.md` (use `CEMS/FINDINGS.md` as the model).

**Gate:** you can name every entity Monty will emit, and the fixtures proving it
are committed.

## 2. Mapping → source `README.md`

Copy `SOURCE_TEMPLATE.md` to `docs/model/sources/<SOURCE>/README.md` and fill it
in from the fixtures: collections, object model (+ Mermaid), one field-carriage
table per Monty type, tracking-over-time, cross-source linkage, and the hazard
crosswalk. **Verify every hazard code** with the procedure in
`references/hazard-code-verification.md` before writing the crosswalk. Add the
extra `../` to the template's doc links now that the file is one directory deeper.

Register the source in `sources.yml`, then run
`python scripts/gen_sources_index.py` and add the source to the `mkdocs.yml` nav.

**Gate:** the "Decisions (resolved)" table has no open rows.

## 3. Examples → `examples/<source>-<type>/`

Add a STAC collection and at least one worked item per collection under
`examples/<source>-{events,hazards,impacts,response}/`, each derived from a
stage-1 fixture. These are provisional until regenerated from the transformer.

**Gate:** `npm test` passes.

## 4–5. Transformer → `pystac-monty` / `montandon-etl`

Specify the transformer as an issue in `IFRCGo/pystac-monty` (the stage-2 mapping
restated as an implementation contract), then implement it there and wire it into
`IFRCGo/montandon-etl`. Update the source's `etl` and `status` in `sources.yml`.
These stages happen in the other repos — this skill's deliverables are stages 1–3
in *this* repo.

## Verify before handing back

```bash
npm test
python scripts/gen_sources_index.py --check
```

Both must pass. If you touched `docs/`, also confirm `mkdocs build --strict`.
