# Monty STAC Extension Examples

This directory contains example STAC collections and items that demonstrate the implementation of the Monty STAC extension. These examples serve as reference implementations for various disaster data sources and showcase the proper structure and usage of the extension.

## Collections

The collections below are grouped by Monty type and link to their example
directory. This listing is generated from
[`docs/model/sources/sources.yml`](../docs/model/sources/sources.yml) by
[`scripts/gen_sources_index.py`](../scripts/gen_sources_index.py), and the
published [Examples page](../docs/examples/index.md) includes it verbatim — so a
new collection appears in both places from a single edit to `sources.yml`.

<!-- --8<-- [start:collections] -->
<!-- gen_sources_index.py: BEGIN examples-collections -->
### Events

- [alerthub-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/alerthub-events) — AlertHub
- [cems-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/cems-events) — Copernicus Emergency Management Service — Rapid Mapping
- [charter-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/charter-events) — International Charter on Space and Major Disasters
- [desinventar-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/desinventar-events) — DesInventar
- [emdat-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-events) — EM-DAT
- [gdacs-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events) — GDACS
- [gfd-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gfd-events) — Global Flood Database (GFD)
- [glide-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/glide-events) — GLIDE
- [ibtracs-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/ibtracs-events) — IBTrACS
- [idmc-gidd-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-events) — IDMC — Global Internal Displacement Database (GIDD)
- [idmc-idu-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-events) — IDMC — Internal Displacement Updates (IDU)
- [ifrcevent-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/ifrcevent-events) — IFRC DREF
- [pdc-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-events) — Pacific Disaster Center (PDC)
- [reference-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/reference-events) — Reference Events
- [usgs-events](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-events) — USGS Earthquake Catalog

### Hazards

- [alerthub-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/alerthub-hazards) — AlertHub
- [cems-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/cems-hazards) — Copernicus Emergency Management Service — Rapid Mapping
- [charter-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/charter-hazards) — International Charter on Space and Major Disasters
- [emdat-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-hazards) — EM-DAT
- [gdacs-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-hazards) — GDACS
- [gfd-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gfd-hazards) — Global Flood Database (GFD)
- [glide-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/glide-hazards) — GLIDE
- [ibtracs-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/ibtracs-hazards) — IBTrACS
- [ifrcevent-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/ifrcevent-hazards) — IFRC DREF
- [pdc-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-hazards) — Pacific Disaster Center (PDC)
- [usgs-hazards](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-hazards) — USGS Earthquake Catalog

### Impacts

- [cems-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/cems-impacts) — Copernicus Emergency Management Service — Rapid Mapping
- [desinventar-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/desinventar-impacts) — DesInventar
- [emdat-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-impacts) — EM-DAT
- [gdacs-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-impacts) — GDACS
- [gfd-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gfd-impacts) — Global Flood Database (GFD)
- [idmc-gidd-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts) — IDMC — Global Internal Displacement Database (GIDD)
- [idmc-idu-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-impacts) — IDMC — Internal Displacement Updates (IDU)
- [ifrcevent-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/ifrcevent-impacts) — IFRC DREF
- [pdc-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-impacts) — Pacific Disaster Center (PDC)
- [usgs-impacts](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts) — USGS Earthquake Catalog

### Response

- [cems-response](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/cems-response) — Copernicus Emergency Management Service — Rapid Mapping
- [charter-response](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/charter-response) — International Charter on Space and Major Disasters
<!-- gen_sources_index.py: END examples-collections -->
<!-- --8<-- [end:collections] -->

## Usage

These examples demonstrate:

1. **Proper STAC Collection Structure** - How to structure collections according to the STAC specification
2. **Monty Extension Implementation** - Correct usage of Monty extension fields and properties
3. **Data Source Integration** - How different disaster data sources can be represented in STAC
4. **Relationship Modeling** - How events, hazards, and impacts relate to each other
5. **Taxonomy Usage** - Implementation of standardized disaster taxonomies

## Collection Types

### Events

Event collections represent discrete disaster occurrences with temporal and spatial bounds. They typically include:

- Event identification and classification
- Temporal information (start/end dates)
- Spatial information (affected areas)
- Links to related hazards and impacts

### Hazards

Hazard collections contain data about the physical phenomena that can cause disasters:

- Hazard type and classification
- Intensity and severity measures
- Temporal evolution
- Spatial extent and characteristics

### Impacts

Impact collections document the consequences of disasters:

- Human impacts (casualties, displacement)
- Economic impacts (damages, losses)
- Social and environmental impacts
- Recovery and response metrics

## Validation

All examples in this directory are validated against:

- [STAC Specification](https://stacspec.org/)
- [Monty STAC Extension Schema](../json-schema/schema.json)
- Taxonomy requirements defined in the [model documentation](../docs/model/)

## Contributing

When adding new examples:

1. Follow the existing directory structure
2. Ensure compliance with the Monty extension schema
3. Include both collection and item examples where applicable
4. Declare the collection in [`sources.yml`](../docs/model/sources/sources.yml) and run `python scripts/gen_sources_index.py` to refresh the listing above
5. Validate examples using the provided schema

For more information about the Monty extension and its usage, see the [documentation](../docs/).
