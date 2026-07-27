# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `docs/model/response-impact-boundary.md` — source-agnostic Response ↔ Impact boundary rules: data-pattern catalogue (P1–P9), decision tree, ETL splitting algorithm + exact `derived_from` link block, and CQL2 query patterns for re-pairing Response and Impact items
- Synthetic illustrative fixture under `examples/_response-impact-pairing/` — one `eo-gra` Response item split into two thematic Impact items (pattern P4), linked via shared `monty:corr_id` and `rel: derived_from`
- Cross-links to the boundary-rules doc from `docs/model/response-best-practices.md`, `docs/model/README.md`, and `README.md`
- `examples/gdacs-events/1001230-41.json` and `examples/gdacs-hazards/1001230-41.json` — real GDACS Event/Hazard items for Tropical Cyclone Melissa (built from live `geteventdata`/`getgeometry` API responses), completing the CEMS↔GDACS cross-source `related` link that `cems-event-EMSR847.json` already declares. Their `monty:corr_id` is computed with the real `geo_blocks-0.2.parquet` lookup and deliberately does not match CEMS's — a fixture-verified illustration of the per-source `corr_id` caveat in #57
- `scripts/check_hazard_codes.py` (wired into `npm test` as `check-hazard-codes`) — validates every `monty:hazard_codes` value in `examples/` against the GLIDE, EM-DAT, and UNDRR-ISC 2025 code tables in `docs/model/taxonomy.md`, with a documented waiver list for deliberate exceptions (`BH0001`). Deliberately not a JSON Schema `enum` — see the script docstring. Guards against a repeat of [#61](https://github.com/IFRCGo/monty-stac-extension/issues/61) [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `mkdocs-strict-build` job in `.github/workflows/test.yaml` running `mkdocs build --strict`, plus `validation.nav.omitted_files: warn` and a `not_in_nav` waiver (`CEMS/FINDINGS.md`) in `mkdocs.yml`, so a doc left out of the `nav` fails CI instead of silently going unpublished [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `docs/model/response-taxonomy.md`, `response-best-practices.md`, `response-impact-boundary.md`, and the CEMS/Charter/IDU source docs added to the `mkdocs.yml` nav — previously built but unreachable from the published site [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `docs/model/sources/sources.yml` — single source of truth for the 15 Monty data sources (id, name, org, url, license, `status` maturity stage, `types`, `collections`, `doc`, `etl`), and `scripts/gen_sources_index.py` to regenerate the `## Available Sources` / `## Data Types by Source` tables in `docs/model/sources/README.md` from it and publish `docs/sources.json` (consumed by `montandon-website`). `--check` mode is wired into the `mkdocs-strict-build` CI job and fails on drift, on a doc missing from `mkdocs.yml` nav, or on `collections` not matching the actual `examples/<collection>/` directories. CEMS, Charter and IDU now carry a `Response`/`Impact` column in the generated table alongside the rest; `alerthub-*` and `reference-events` are recorded with `status: undocumented` since they have example collections but no source doc yet [#65](https://github.com/IFRCGo/monty-stac-extension/issues/65)
- `CONTRIBUTING.md` — code of conduct pointer, contribution paths for the spec/model/a source, and the running-tests / building-the-docs-site instructions moved out of `README.md` and folded in from `DOCS.md` [#67](https://github.com/IFRCGo/monty-stac-extension/issues/67)

### Changed

- Reconciled the two divergent example indexes: the `## Collections` listing in `examples/index.md` (grouped by Monty type, one link per `examples/<collection>/`) is now generated from `docs/model/sources/sources.yml` by `scripts/gen_sources_index.py`, and the published `docs/examples/index.md` pulls that same listing in verbatim via a `pymdownx.snippets` section include (`--8<-- "examples/index.md:collections"`) while keeping its editorial prose and CI mermaid diagram. Adding a collection to `sources.yml` now surfaces on the published Examples page with no second edit; `gen_sources_index.py --check` (already in the `mkdocs-strict-build` CI job) fails on drift [#66](https://github.com/IFRCGo/monty-stac-extension/issues/66)
- Promoted `docs/model/response-taxonomy.md` from a working document to the canonical Monty Response taxonomy reference for v1.3.0: dropped the working-document/pending-review status header, foregrounded the adopted response type codes and classification rules, aligned the `monty:response_detail` field reference with the shipped schema, and moved the framework survey to an appendix
- Restructured `README.md` to lead with orientation instead of diving straight into the normative field spec: a new `## The Three Pillars` section surfaces the Model (`docs/model/`) and Sources (`docs/model/sources/`, with the documented-source count now generated from `sources.yml` by `scripts/gen_sources_index.py`), plus `## Quick Start` and `## Repository Map` sections and a `## Also See` pointer to `CONTRIBUTING.md`, `CHANGELOG.md` and the published site. The normative reference itself (Fields through Response) is unchanged; the 33-line `## Contributing` section is now a two-line pointer to `CONTRIBUTING.md` [#67](https://github.com/IFRCGo/monty-stac-extension/issues/67)

### Removed

- `DOCS.md` — its docs-site build instructions moved into `CONTRIBUTING.md` [#67](https://github.com/IFRCGo/monty-stac-extension/issues/67)

### Fixed

- Hazard code crosswalks in `docs/model/sources/CEMS/README.md` and `docs/model/sources/Charter/README.md` corrected against `docs/model/taxonomy.md` — several codes were either nonexistent (`MH0901`, `MH1301`, `MH1201`, `MH1202`, `TH0300`, `TH0600`, `MH0400`) or wrong (`MH0403` is *Blizzard*, not Tropical Cyclone; `GH0301` is *Falls*, not Tsunami; `MH0801` is *Avalanche*, not ice/cold). Corrected values now match the convention already used by GDACS, EM-DAT, GLIDE and GFD (`MH0306` tropical cyclone, `GH0300` landslide chapeau, `EN0205` wildfire, `MH0705` tsunami). Propagated into affected `examples/cems-*` and `examples/charter-*` items, including `monty:corr_id` where the wrong code was embedded [#61](https://github.com/IFRCGo/monty-stac-extension/issues/61)
- `related` / `derived_from` links whose target is a STAC Item now use `application/geo+json` instead of `application/json`, across `examples/_response-impact-pairing`, `charter-hazards`, `gdacs-events`, `gdacs-hazards`, `glide-events`, `ibtracs-hazards` and `reference-events`, plus the matching `derived_from` link block documented in `docs/model/response-impact-boundary.md`. Added `scripts/check-link-types.mjs` (wired into `npm test`) to catch regressions, since the JSON Schema and `stac-node-validator` don't constrain link `type` [#55](https://github.com/IFRCGo/monty-stac-extension/issues/55)
- Relative links in `docs/model/sources/CEMS/README.md`, `docs/model/sources/Charter/README.md`, and `docs/model/response-taxonomy.md` that pointed at `examples/`, `README.md`, `AGENTS.md`, and `json-schema/schema.json` (all outside `docs_dir`, so unresolvable by MkDocs) now use absolute GitHub URLs, matching the convention already used by the GDACS/GLIDE source docs [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `.github/workflows/deploy_mkdocs.yml` path filters: `CHANGES.md` → `CHANGELOG.md` (the file has always been named `CHANGELOG.md`, so edits to it never triggered a docs rebuild), added `mkdocs.yml` (nav/config edits didn't trigger a rebuild either), dropped `README.md` (not part of the MkDocs nav, so it was a no-op trigger) [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `docs/model/generate_taxonomy_tables.py` documented as a manual, un-wired legacy script — it regenerates from a `Montandon_Schema_V1-00.json` snapshot that predates the hand-maintained GLIDE/EM-DAT/UNDRR-ISC 2025 tables, so running it today would overwrite `taxonomy.md` with stale content [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)

## [1.3.0] - 2026-06-11

### Added

- `monty:response_detail` object on Response Items with `type` (required, response-taxonomy regex), `source_id`, `status`, `monitoring_number`, `producer`, `methodology`, `sendai_targets`, `sectors` [#46](https://github.com/IFRCGo/monty-stac-extension/pull/46)
- `response` role added to the `roles` `oneOf` branch and to the `typed_related_link.roles` enum (so `rel: related` can target Response items) [#46](https://github.com/IFRCGo/monty-stac-extension/pull/46)
- `related-response` relation type [#46](https://github.com/IFRCGo/monty-stac-extension/pull/46)
- `docs/model/response-best-practices.md` — extension-layering matrix, per-source mapping tables (CEMS, International Charter, UNOSAT), worked snippets, anti-patterns, and linkage summary [#46](https://github.com/IFRCGo/monty-stac-extension/pull/46)
- Response section in `docs/model/README.md` (with updated class diagram) and in `README.md`, including the per-source collection partitioning guidance and the Impact→Response `derived_from` provenance convention [#46](https://github.com/IFRCGo/monty-stac-extension/pull/46)

## [1.2.0] - 2026-05-11

### Added

- `monty:src_event_id` property to group items belonging to the same source event (e.g. across GDACS episodes) [#45](https://github.com/IFRCGo/monty-stac-extension/pull/45)

## [1.1.0] - 2025-11-06

### Added

- New dynamic correlation algorithms using STAC API and CQL2 filters [#33](https://github.com/IFRCGo/monty-stac-extension/pull/33)

### Changed

- Updated taxonomy for 2025 UNDRR-ISC Hazard Information Profiles [#32](https://github.com/IFRCGo/monty-stac-extension/pull/32)
- Deprecating static correlation_id in favor of dynamic STAC-based correlation [#33](https://github.com/IFRCGo/monty-stac-extension/pull/33)

### Fixed

- Mandatory severity_value and severity_unit fields in hazard_detail reflected in json schema [#32](https://github.com/IFRCGo/monty-stac-extension/pull/32)

### Removed

- Removed cluster code from hazard detail as we have chapeau hazard codes now [#32](https://github.com/IFRCGo/monty-stac-extension/pull/32)

## [1.0.0] - 2025-05-27

Initial release of the Monty STAC Extension specification.

### Added

- Core STAC extension specification for Monty (Global Crisis Data Bank)
  - Field definitions for Items and Collections
  - Relation type specifications
  - Link attribute definitions

- Comprehensive data model documentation
  - Event object specification
  - Hazard object specification
  - Impact object specification
  - Source analysis templates and guidelines

- Integration with major disaster data sources:
  - DesInventar - National disaster loss database
  - EM-DAT - International disaster database
  - GDACS - Global Disaster Alert and Coordination System
  - GFD - Global Flood Database
  - GLIDE - Global unique disaster identifier
  - IBTrACS - International Best Track Archive for Climate Stewardship
  - IDMC - Internal Displacement Monitoring Centre
  - IFRC-DREF - Disaster Relief Emergency Fund
  - PDC - Pacific Disaster Center
  - USGS - United States Geological Survey

- Common taxonomy and classification systems
  - Standardized hazard codes
  - Impact types and categories
  - Country code normalization
  - Cross-classification mappings

- Reference implementations
  - Example collections for all supported sources
  - Event correlation examples
  - Impact aggregation examples

- Developer tools and documentation
  - JSON Schema for validation
  - Documentation website using MkDocs
  - Source integration guidelines
  - Querying capabilities documentation

### Supported Features

- Event correlation across multiple sources
- Hazard classification standardization
- Impact data aggregation
- Spatial and temporal querying
- STAC API integration support
- Collection-level metadata
- Source-specific field mappings

### Notes

- This is the initial release for evaluation and feedback
- The specification is currently in proposal status
- Some features may be subject to change based on community feedback
- Additional sources may be added in future releases

[Unreleased]: https://github.com/IFRCGo/monty-stac-extension/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/IFRCGo/monty-stac-extension/releases/tag/v1.3.0
[1.2.0]: https://github.com/IFRCGo/monty-stac-extension/releases/tag/v1.2.0
[1.1.0]: https://github.com/IFRCGo/monty-stac-extension/releases/tag/v1.1.0
[1.0.0]: https://github.com/IFRCGo/monty-stac-extension/releases/tag/v1.0.0
