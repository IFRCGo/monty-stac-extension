# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- GDACS `properties.impacts[]` documented in `docs/model/sources/GDACS/README.md` — the TC advisory timeline (`resource.timeline` → `gettimeline`) and the WF population exposure (`resource.impact` → `getimpact`), which have driven the `gdacs-impacts` collection since [IFRCGo/pystac-monty@7f3b5f91](https://github.com/IFRCGo/pystac-monty/commit/7f3b5f91) but existed only in the transformer. The Impact Item section now routes by event type (FL → `sendai`, TC → `timeline`, WF → `impact`, EQ/DR/TS/VO → none), and three properties of the timeline verified against live episodes 9 and 13 of cyclone NOUL-26 (`eventid=1001294`) drive the mapping rules: the timeline is **cumulative** — each episode repeats every earlier advisory entry byte-for-byte, keeping its `id`, so keying the impact item on the episode manufactures one duplicate per later episode; `advisory_number` is **neither unique nor dense** — the current advisory appears once observed plus once per forecast lead time (advisory 13 appears 4 times, advisory 12 not at all), leaving `id` as the only safe key; and `pop` is **not a total** — it reads 0 where `pop39` counts 75 million people, and 19 million where `pop39` is 0, so the mapping takes `pop39`/`pop74`/`popstormsurge`, one impact item per non-zero band, and leaves `pop` unmapped pending a definition from JRC. Trimmed fixtures for both episodes added under `docs/model/sources/GDACS/api-files/`. Also documents that `impacts[]` must be read from `getepisodedata`, since `geteventdata` ignores `episodeid` and returns the current episode (the ETL already follows `properties.episodes[].details`, which is the right URL) [#89](https://github.com/IFRCGo/monty-stac-extension/issues/89)
- `docs/model/response-impact-boundary.md` — source-agnostic Response ↔ Impact boundary rules: data-pattern catalogue (P1–P9), decision tree, ETL splitting algorithm + exact `derived_from` link block, and CQL2 query patterns for re-pairing Response and Impact items
- Synthetic illustrative fixture under `examples/_response-impact-pairing/` — one `eo-gra` Response item split into two thematic Impact items (pattern P4), linked via shared `monty:corr_id` and `rel: derived_from`
- Cross-links to the boundary-rules doc from `docs/model/response-best-practices.md`, `docs/model/README.md`, and `README.md`
- `examples/gdacs-events/1001230-41.json` and `examples/gdacs-hazards/1001230-41.json` — real GDACS Event/Hazard items for Tropical Cyclone Melissa (built from live `geteventdata`/`getgeometry` API responses), completing the CEMS↔GDACS cross-source `related` link that `cems-event-EMSR847.json` already declares. Their `monty:corr_id` is computed with the real `geo_blocks-0.2.parquet` lookup and deliberately does not match CEMS's — a fixture-verified illustration of the per-source `corr_id` caveat in #57
- `scripts/check_hazard_codes.py` (wired into `npm test` as `check-hazard-codes`) — validates every `monty:hazard_codes` value in `examples/` against the GLIDE, EM-DAT, and UNDRR-ISC 2025 code tables in `docs/model/taxonomy.md`, with a documented waiver list for deliberate exceptions (`BH0001`). Deliberately not a JSON Schema `enum` — see the script docstring. Guards against a repeat of [#61](https://github.com/IFRCGo/monty-stac-extension/issues/61) [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `mkdocs-strict-build` job in `.github/workflows/test.yaml` running `mkdocs build --strict`, plus `validation.nav.omitted_files: warn` and a `not_in_nav` waiver (`CEMS/FINDINGS.md`) in `mkdocs.yml`, so a doc left out of the `nav` fails CI instead of silently going unpublished [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `docs/model/response-taxonomy.md`, `response-best-practices.md`, `response-impact-boundary.md`, and the CEMS/Charter/IDU source docs added to the `mkdocs.yml` nav — previously built but unreachable from the published site [#64](https://github.com/IFRCGo/monty-stac-extension/issues/64)
- `docs/model/sources/sources.yml` — single source of truth for the 15 Monty data sources (id, name, org, url, license, `status` maturity stage, `types`, `collections`, `doc`, `etl`), and `scripts/gen_sources_index.py` to regenerate the `## Available Sources` / `## Data Types by Source` tables in `docs/model/sources/README.md` from it and publish `docs/sources.json` (consumed by `montandon-website`). `--check` mode is wired into the `mkdocs-strict-build` CI job and fails on drift, on a doc missing from `mkdocs.yml` nav, or on `collections` not matching the actual `examples/<collection>/` directories. CEMS, Charter and IDU now carry a `Response`/`Impact` column in the generated table alongside the rest; `alerthub-*` and `reference-events` are recorded with `status: undocumented` since they have example collections but no source doc yet [#65](https://github.com/IFRCGo/monty-stac-extension/issues/65)
- `org_type` and `contact` fields on every `docs/model/sources/sources.yml` entry, published in `docs/sources.json`. These are the last two facts `montandon-website`'s hand-maintained source table needed that the manifest didn't carry, so its *Type* column and per-source contacts can now be generated rather than kept in a parallel copy. `org_type` is a closed vocabulary (`International Organization`, `Regional Intergovernmental Organization`, `National Government`, `International NGO`, `Academic / Research`, `Private Sector`, `Interagency Consortium`) validated by `gen_sources_index.py`, with display-ready values so consumers print them verbatim instead of maintaining a slug→label map; `contact` accepts an email address or an http(s) URL for sources offering only a contact form (IFRC DREF). Both are also validated for presence: every entry must carry every field, using `null` where one doesn't apply [#71](https://github.com/IFRCGo/monty-stac-extension/issues/71)
- `CONTRIBUTING.md` — code of conduct pointer, contribution paths for the spec/model/a source, and the running-tests / building-the-docs-site instructions moved out of `README.md` and folded in from `DOCS.md` [#67](https://github.com/IFRCGo/monty-stac-extension/issues/67)
- Governance layer: `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1, adopted directly, reporting via GitHub's private "Report content" flow rather than a hardcoded inbox); structured issue forms under `.github/ISSUE_TEMPLATE/` (`new-source.yml` mirroring the `sources.yml` manifest fields and status lifecycle, `model-change.yml`, `bug.yml`, plus `config.yml`); and `.github/PULL_REQUEST_TEMPLATE.md` with per-path checklists (source / schema / model). `CONTRIBUTING.md` gains a `## Cutting a release` section documenting the previously-tribal four-file version bump and the tag → release → `publish.yaml` flow, and notes that review is not auto-assigned (no `CODEOWNERS`) [#68](https://github.com/IFRCGo/monty-stac-extension/issues/68)
- `docs/model/sources/SOURCE_TEMPLATE.md` and `docs/model/sources/METHODOLOGY.md` — the source-analysis template and methodology, promoted from what the CEMS and Charter docs converged on but was written down nowhere. `SOURCE_TEMPLATE.md` is the source-README skeleton (Collections → Object model + Mermaid → per-type field-carriage tables → Tracking over time → Cross-source linkage → Hazard codes → Examples → Reference files → Decisions → Resources); `METHODOLOGY.md` documents the five-stage pipeline (familiarisation → mapping → examples → transformer spec → deployment) with each stage's output/home/gate, the rules every source doc follows (taxonomy-first gate, fixture grounding, provisional hand-written examples, verbatim schema/README descriptions, hazard-code verification against `taxonomy.md`), and the fixture size/placement policy. Both added to the `mkdocs.yml` nav [#69](https://github.com/IFRCGo/monty-stac-extension/issues/69)
- `docs/model/sources/IFRC-DREF/README.md` now accepts 2 more of GO's 24 disaster types — `Civil Unrest` → `SO0103` (a single-code triplet: the Societal hazard type has no GLIDE/EM-DAT row in the crosswalk) and `Insect Infestation` → `BI0401` via the `nat-bio-inf-inf` crosswalk row — and turns the remaining 9 exclusions from an unexplained filter list into a table with a checked reason each: appeal counts (0–542) and, for the 4 genuinely ambiguous types (`Complex Emergency`, `Transport Accident`, `Chemical Emergency`, `Biological Emergency`), a sample of their actual event names showing no dominant hazard to default to — correcting the "mappable in principle" read given to the latter two when [#96](https://github.com/IFRCGo/monty-stac-extension/issues/96) was filed. Also surfaced a pre-existing defect in `taxonomy.md`'s cross-classification mapping while sourcing the `Insect Infestation` code: the `nat-bio-inf-loc` EM-DAT key appears twice, once as "Insect pest infestation" → BI0401 and once as "Locust infestation" → BI0402 — worked around by using the unambiguous `nat-bio-inf-inf` row instead of fixing the crosswalk itself, which is shared by every source and out of scope here [#96](https://github.com/IFRCGo/monty-stac-extension/issues/96)

### Changed

- Reconciled the source-metadata blocks in the per-source READMEs against `sources.yml`, which is authoritative for them. GFD and PDC still read `Source Data License: UNKNOWN` while the manifest had carried `CC BY-NC-ND 4.0` and the PDC restricted terms since [#78](https://github.com/IFRCGo/monty-stac-extension/pull/78); EM-DAT was typed `Regional Intergovernmental Organisation` (CRED is a UCLouvain research centre — now `Academic / Research`); IDU had IDMC as `Regional Intergovernmental Organization` rather than an NGO; GFD and PDC had blank `Source organization` / `Source Type` lines. Remaining org-type wordings were normalised onto the `org_type` vocabulary. `SOURCE_TEMPLATE.md` now carries `Organisation type` and `Contact` rows and states that `sources.yml` wins if the two disagree [#71](https://github.com/IFRCGo/monty-stac-extension/issues/71)
- Documented `license: null` in `sources.yml` as a positive statement — *the source publishes no explicit license or reuse terms* — rather than an unfilled gap, so consumers render it as "not stated by the source" instead of "Unknown". Verified 2026-07: GLIDE publishes no terms at all, and IDMC (GIDD and IDU) and IFRC DREF have terms-of-use pages granting no identifiable reuse license. The four source docs now say so explicitly instead of `?` / `[TBD]` / nothing [#71](https://github.com/IFRCGo/monty-stac-extension/issues/71)
- Reconciled the two divergent example indexes: the `## Collections` listing in `examples/index.md` (grouped by Monty type, one link per `examples/<collection>/`) is now generated from `docs/model/sources/sources.yml` by `scripts/gen_sources_index.py`, and the published `docs/examples/index.md` pulls that same listing in verbatim via a `pymdownx.snippets` section include (`--8<-- "examples/index.md:collections"`) while keeping its editorial prose and CI mermaid diagram. Adding a collection to `sources.yml` now surfaces on the published Examples page with no second edit; `gen_sources_index.py --check` (already in the `mkdocs-strict-build` CI job) fails on drift [#66](https://github.com/IFRCGo/monty-stac-extension/issues/66)
- Promoted `docs/model/response-taxonomy.md` from a working document to the canonical Monty Response taxonomy reference for v1.3.0: dropped the working-document/pending-review status header, foregrounded the adopted response type codes and classification rules, aligned the `monty:response_detail` field reference with the shipped schema, and moved the framework survey to an appendix
- Restructured `README.md` to lead with orientation instead of diving straight into the normative field spec: a new `## The Three Pillars` section surfaces the Model (`docs/model/`) and Sources (`docs/model/sources/`, with the documented-source count now generated from `sources.yml` by `scripts/gen_sources_index.py`), plus `## Quick Start` and `## Repository Map` sections and a `## Also See` pointer to `CONTRIBUTING.md`, `CHANGELOG.md` and the published site. The normative reference itself (Fields through Response) is unchanged; the 33-line `## Contributing` section is now a two-line pointer to `CONTRIBUTING.md` [#67](https://github.com/IFRCGo/monty-stac-extension/issues/67)
- Retired the legacy five-section source template in `docs/model/sources/README.md` (`### 1. Source Description` … `### 5. Item Mapping`, which nominated IDMC as the exemplar and was followed by only one source): the `## Source Analysis Process` section now points at `METHODOLOGY.md` and `SOURCE_TEMPLATE.md`, with CEMS/Charter as the worked references — ending the three-way template ambiguity. `CONTRIBUTING.md` and the `new-source.yml` issue form now point at the same two docs [#69](https://github.com/IFRCGo/monty-stac-extension/issues/69)

### Removed

- `DOCS.md` — its docs-site build instructions moved into `CONTRIBUTING.md` [#67](https://github.com/IFRCGo/monty-stac-extension/issues/67)

### Fixed

- IFRC DREF source doc corrected against the actual transformer code, closing [etl-drift issue #101](https://github.com/IFRCGo/monty-stac-extension/issues/101) raised after [IFRCGo/pystac-monty#181](https://github.com/IFRCGo/pystac-monty/pull/181) and [#187](https://github.com/IFRCGo/pystac-monty/pull/187). `docs/model/sources/IFRC-DREF/README.md` now documents: impact items generated from **every** field report on an event, not just the first, so an event with *N* field reports and *M* impact types carrying a truthy value can produce up to *N* × *M* impact items (a type whose three source fields are all explicit zeros produces no item, since the transformer checks truthiness, not null-ness, and doesn't cross-reference the three values against each other); the impact item ID format gained a field-report-id suffix (`ifrcevent-impact-{event_id}-{impact_type}-{field_report_id}`) to keep those items unique across reports; geometry generation unions polygons across multiple countries for both event and impact items, with impact items falling back to the parent event's geometry whenever none of their own field report's countries resolves to a geometry; and impact items now carry their own `monty:country_codes` from the field report's `countries[].iso3`, falling back to the event's country codes when the field report has none. `sources.ifrcevent.reviewed` bumped to [`2c5f06ae`](https://github.com/IFRCGo/pystac-monty/commit/2c5f06ae46c6c4ed3b91c1c31588812d5c7fc651) in `.github/etl-watch.yml`, per the issue's own resolution instructions. Not fixed here: cross-checking the hazard table against upstream `HazardProfiles.csv` surfaced that `Civil Unrest`'s claimed "no GLIDE or EM-DAT row" is only half right — `taxonomy.md`'s own cross-classification table pairs GLIDE `CE` with `SO0103` (EM-DAT is genuinely absent) — but the transformer doesn't emit `CE` either, so correcting the doc's claim without a matching upstream code change would just relocate the drift; left for a follow-up issue
- USGS source doc corrected against the actual transformer code, closing [etl-drift issue #92](https://github.com/IFRCGo/monty-stac-extension/issues/92) raised after [IFRCGo/pystac-monty#171](https://github.com/IFRCGo/pystac-monty/pull/171) and [#177](https://github.com/IFRCGo/pystac-monty/pull/177). `docs/model/sources/USGS/README.md` now states the real `monty:country_codes` fallback in `make_source_event_item`: reverse-geocode the epicenter first, then — since #177 — fall back to the country with the highest total PAGER fatality estimate, then `UNK` if both fail. The Hazard Item table's `monty:hazard_codes` and `monty:country_codes` rows are corrected to say they are inherited unchanged from the event: `make_hazard_event_item` used to overwrite `hazard_codes` down to one UNDRR-2025 code, a line #171 removed, so the hazard item now carries the same three-code trio as the event, matching what the committed examples already show. The Event Item's `monty:hazard_codes` value itself did not change (`GH0101`/`nat-geo-ear-gro`/`EQ`, as already documented) — #171 replaced the dead-code path that computed it with a direct assignment — so no doc correction was needed there. `sources.usgs.reviewed` in `.github/etl-watch.yml` was already at the target sha (set when the drift tooling's baseline was bootstrapped, after this issue was filed), so no bump was needed. Not fixed here: `make_impact_items` already emitted one impact item per PAGER-listed country per type, and a second, undocumented impact-item type from the alert product — both predate this issue's baseline and are a separate, larger doc gap
- CEMS and Charter source docs corrected against the actual transformer code, closing [etl-drift issues #102–#106](https://github.com/IFRCGo/monty-stac-extension/issues/102) raised after [IFRCGo/pystac-monty#187](https://github.com/IFRCGo/pystac-monty/pull/187). The CEMS doc's `subCategory` refinement column claimed five refinements that don't exist in the transformer: wildfire's `Forest fire`/land-fire split (subCategory `forest fire` resolves to the same general `nat-cli-wil-wil` key, not a distinct code), mass movement's rockfall/subsidence split, volcanic activity's ashfall/lahar split, industrial accident's `gas leak` key and `TL0309` "general" fallback (the real fallback is `TL0301`), and transport accident's per-mode codes (the category is in the manual-review set and receives no automatic code at all). Charter had the same class of error for `storm_hurricane` (claimed to refine to MH0306 if tropical; it's manual-review only, unrelated to the separate `cyclone` type) and `ice` (claimed refinement to MH0509/MH0506; always resolves to the flat `MH0502`). None of this was introduced by the recent upstream changes — it predates the drift watcher's baseline and was only surfaced by re-reading the transformer code line for line while investigating the flagged diffs, so the drift issues undersold the size of the correction. Also: DesInventar's `FIRE` (general) event type, mapped in code since before the review baseline but never documented, gets a table row; GLIDE's `VO` (Volcano) row, similarly undocumented despite the code correctly mapping it to `GH0201`, gets one too, alongside fixing `EP`'s description from a vague "Multiple codes" to the actual `BI0101` the code emits. A round of Copilot review then caught two more classes of error in the same tables: CEMS's and Charter's Volcanic Activity/`volcano` rows carried the truncated EM-DAT key `nat-geo-vol`, which isn't a real key in `taxonomy.md` at all (only the `-ash`/`-lah`/`-lav`/`-pyr`/`-vol`-suffixed variants are; the transformers already use the correct `nat-geo-vol-vol`); and every manual-review row across both docs (CEMS's Transport accident, Humanitarian Crisis, Other; Charter's `storm_hurricane`) still listed a GLIDE and/or EM-DAT companion code even though the transformer's manual-review short-circuit means **nothing** is emitted for them — for Humanitarian Crisis and Other, the `["CE"]`/`["OT"]` dict entries those columns were describing are unreachable code, since the manual-review check runs before either is ever consulted. `sources.{cems,charter,desinventar,glide,pdc}.reviewed` bumped to [`e4fc88b3`](https://github.com/IFRCGo/pystac-monty/commit/e4fc88b3d30c2e7d7d0ac359de6bd24096e972cd) in `.github/etl-watch.yml`
- Wildfire EM-DAT keys harmonised across the source docs, on a rule now stated in `docs/model/taxonomy.md`: pick the crosswalk row at the granularity the source actually states. A source whose category is a general wildfire takes `nat-cli-wil-wil` — CEMS (`Wildfire`), Charter (`fire`), IDMC (`Wildfire`) and PDC (`Wildfire`) now do, joining IDU which already did — while DesInventar keeps `nat-cli-wil-for` because its event type is literally `FOREST FIRE`. The EM-DAT source doc lists all three wildfire keys against `EN0205` rather than only `nat-cli-wil-for`. Not cosmetic: `HazardProfiles.csv` upstream carries only `nat-cli-wil-wil` on the `EN0205` row, so `get_canonical_hazard_codes()` silently drops `nat-cli-wil-for` and the emitted item loses its EM-DAT code — verified against `IFRCGo/pystac-monty@fix/ifrc-event-stac-item`, with the CSV drift itself tracked in [IFRCGo/pystac-monty#184](https://github.com/IFRCGo/pystac-monty/issues/184). Propagated into the eight affected collection summaries (`gdacs-*`, `glide-*`, `idmc-idu-*`, `pdc-impacts`) and into `examples/idmc-idu-impacts/idmc-idu-impact-169470-displaced.json`, whose `monty:corr_id` embedded the dropped key (and misspelled the `GCDB` suffix). Also corrects the GLIDE source doc's `FR` (Fire) row, which claimed `EN0205` (Wildfires): GLIDE distinguishes `FR` from `WF`, and the crosswalk maps `FR` to `TL0305` (Fire, Industrial Failure) — a `WF` (Wild Fire) → `EN0205` row is added alongside it [#95](https://github.com/IFRCGo/monty-stac-extension/issues/95)
- IFRC DREF hazard type mapping in `docs/model/sources/IFRC-DREF/README.md`, reconciled against `docs/model/taxonomy.md` and the live GO disaster-type vocabulary. `Fire` now defaults to `EN0205`/`WF`/`nat-cli-wil-wil`: GO has a single `Fire` type dominated by wildfires, and mapping the whole type to the industrial-fire code filed most DREF fire operations under the *Technological* family, where they could not correlate with the `EN0205` that EM-DAT, CEMS, IDMC, IDU, GLIDE, DesInventar and PDC use for the same fires — `TL0305`/`FR`/`tec-ind-fir-fir` is now a documented refinement for structural and industrial fires. `Volcanic Eruption` keeps `GH0201` but as the explicit stand-in for an eruption whose phenomenon is unspecified (HIP 2025 has no volcanic chapeau), not as a claim of lava flows; `Epidemic` keeps `BI0101` per the `EP`/`nat-bio-epi-dis` crosswalk row; `Cyclone` keeps `MH0306` because GO's `Cyclone` files extratropical systems alongside tropical ones, with the repo-wide `MH0306` vs `MH0309` convention deferred to [#94](https://github.com/IFRCGo/monty-stac-extension/issues/94). Also: the disaster-type key `Flash Flood` corrected to GO's actual `Pluvial/Flash Flood`, `atype: 1` documented as *Emergency Appeal* rather than DREF (the collection covers both), and the exclusion of 11 of GO's 24 disaster types — roughly 1300 DREF and Emergency Appeal operations — recorded as a deliberate scope decision linking [#96](https://github.com/IFRCGo/monty-stac-extension/issues/96). Raised from [IFRCGo/pystac-monty#182](https://github.com/IFRCGo/pystac-monty/issues/182)
- Two of the IFRC DREF rules above, tightened after [#97](https://github.com/IFRCGo/monty-stac-extension/pull/97) review found real false-positive risk in both keyword heuristics, checked against live GO data rather than assumed. The fire rule's structural/industrial keywords now match only the event `name`, not `summary`: `summary` is narrative impact prose that uses the same words to describe what a wildfire *destroyed* ("threatening residential areas", "urban-forest interface", damage tallies that count "buildings"), and matching it produced 15 false positives — genuine wildfires reclassified as structural — across the 225 DREF `Fire` operations on GO, against zero when restricted to `name`; the rule also now splits `TL0305`'s EM-DAT companion between `tec-ind-fir-fir` and `tec-mis-fir-fir` per the crosswalk's own two fire rows. `Cyclone` gains a corresponding `name`-only rule refining the `MH0306` default to `MH0307`/`EC`/`nat-met-sto-ext` on an explicit extratropical signal or `MH0309`/`TC`/`nat-met-sto-tro` on an explicit tropical one (137 of 200 sampled Cyclone operations name a tropical system in `name`, 1 an extratropical one) — deliberately scoped to what GO's own text states rather than resolving the repo-wide `MH0306` vs `MH0309` question tracked in #94
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
