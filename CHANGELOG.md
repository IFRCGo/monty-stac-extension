# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `docs/model/response-impact-boundary.md` — source-agnostic Response ↔ Impact boundary rules: data-pattern catalogue (P1–P9), decision tree, ETL splitting algorithm + exact `derived_from` link block, and CQL2 query patterns for re-pairing Response and Impact items
- Synthetic illustrative fixture under `examples/_response-impact-pairing/` — one `eo-gra` Response item split into two thematic Impact items (pattern P4), linked via shared `monty:corr_id` and `rel: derived_from`
- Cross-links to the boundary-rules doc from `docs/model/response-best-practices.md`, `docs/model/README.md`, and `README.md`

### Changed

- Promoted `docs/model/response-taxonomy.md` from a working document to the canonical Monty Response taxonomy reference for v1.3.0: dropped the working-document/pending-review status header, foregrounded the adopted response type codes and classification rules, aligned the `monty:response_detail` field reference with the shipped schema, and moved the framework survey to an appendix

### Fixed

- Hazard code crosswalks in `docs/model/sources/CEMS/README.md` and `docs/model/sources/Charter/README.md` corrected against `docs/model/taxonomy.md` — several codes were either nonexistent (`MH0901`, `MH1301`, `MH1201`, `MH1202`, `TH0300`, `TH0600`, `MH0400`) or wrong (`MH0403` is *Blizzard*, not Tropical Cyclone; `GH0301` is *Falls*, not Tsunami; `MH0801` is *Avalanche*, not ice/cold). Corrected values now match the convention already used by GDACS, EM-DAT, GLIDE and GFD (`MH0306` tropical cyclone, `GH0300` landslide chapeau, `EN0205` wildfire, `MH0705` tsunami). Propagated into affected `examples/cems-*` and `examples/charter-*` items, including `monty:corr_id` where the wrong code was embedded [#61](https://github.com/IFRCGo/monty-stac-extension/issues/61)

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
