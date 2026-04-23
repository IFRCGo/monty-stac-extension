# International Charter on Space and Major Disasters

The International Charter on Space and Major Disasters coordinates satellite data delivery for disaster response worldwide. Charter activations provide satellite imagery and analysis products to assist civil protection authorities.

## Collections

Charter data maps to three Monty collections:

- **Name**: International Charter - Events
- **Code**: `charter-events`
- **Source organisation**: International Charter on Space and Major Disasters
- **Source organisation code**: CHARTER
- **Source URL**: <https://disasterscharter.org>
- **STAC Catalog**: <https://supervisor.disasterscharter.org/api/>
- **Data License**: Charter Activation Data License (public for Events/Hazards; partner access for Response)
- **Source for**: event, hazard, response
- **Temporal Coverage**: 2000-11-05 onwards (Charter formation)

## Data Access

### API Endpoints

```bash
# Activation (Event source) - use direct pattern
https://supervisor.disasterscharter.org/api/activations/act-{activationID}

# Example: Multi-hazard (flood + landslide) in Brazil
curl -s https://supervisor.disasterscharter.org/api/activations/act-1019 | jq

# Area (Hazard source) - links from activations work
https://supervisor.disasterscharter.org/api/activations/act-{id}/areas/{area_slug}.json
```

> [!IMPORTANT]
> Known API quirks:
> - Calls/Activations catalog endpoints are slow (dynamically generated)
> - Activation catalog `self` links point to `.json` suffix but return HTTP 500 - omit suffix
> - Direct activation pattern above is reliable
> - Area links from activation items work correctly

**Alternative browsing**: [STAC Index](https://stacindex.org/catalogs/disasters-charter-mapper-catalog)

### Discover Available Fields

Audit upstream `properties` keys across activation range (requires [jq](https://jqlang.github.io/jq/)):

```bash
for i in $(seq 900 1020); do
  curl -s --max-time 5 "https://supervisor.disasterscharter.org/api/activations/act-$i" \
    | jq -r '.properties | keys[]?' 2>/dev/null
done | sort -u
```

## Entity Mapping

| Charter Entity | Monty Type | ID Pattern | Collection | Status |
|----------------|------------|------------|------------|--------|
| Activation | Event | `charter-event-{activation_id}` | `charter-events` | ✅ Ready |
| Area (AoI) | Hazard | `charter-hazard-{activation_id}-{area_slug}-{type}` | `charter-hazards` | ✅ Ready |
| Acquisition/Dataset/VAP | Response | `charter-response-{activation_id}-*` | `charter-response` | ⚠️ S3 access TBD |



### Activation → Event

| Charter Field | Monty Field | Notes |
|--------------|-------------|-------|
| `id: "act-1019"` | `id: "charter-event-1019"` | Prefix with `charter-event-` |
| — | `collection: "charter-events"` | **Required** for STAC compliance |
| `properties["
disaster:type"]` | `monty:hazard_codes` | Map via [hazard codes table](#hazard-codes), apply `hazard_profiles.get_canonical_hazard_codes()` |
| `properties["disaster:country"]` | `monty:country_codes[0]` | Already ISO 3166-1 alpha-3 |
| `properties.title` | `title` | Direct copy |
| `properties.datetime` | `datetime` | Event onset time |
| `geometry` (Point) | `geometry` | Direct copy |
| `links[rel=self]` | `links[rel=via]` | Source reference |

> [!IMPORTANT]
> **Onset datetime**: Use `properties.datetime` as the canonical event time. This field equals `properties.created` and matches the embedded `<disasterDate>` in `cpe:cos2_xml`. Do **not** use `properties.updated` - it reflects processing close date (often weeks later).

**Multi-hazard events**: If `disaster:type: ["flood", "landslide"]`, include all hazard codes in the Event item (e.g., both MH0600/FL/nat-hyd-flo-flo and MH0901/LS/nat-geo-mmd-lan).

**Correlation ID**: Generate using standard Monty algorithm from event time, ISO3 country, primary hazard, spatial block, and episode - not Charter `activation_id`.

### Area → Hazard

| Charter Field | Monty Field | Notes |
|--------------|-------------|-------|
| Area `id` | `id` | Pattern: `charter-hazard-{activation_id}-{area_slug}-{type}` |
| — | `collection: "charter-hazards"` | **Required** for STAC compliance |
| `geometry` (Polygon) | `geometry` | Full AoI polygon |
| `properties["disaster:type"]` | `monty:hazard_codes` | **One code per item** (see multi-hazard note below) |
| `properties.title` | `title` | Area name (e.g., "Juiz de Fora") |
| `properties.datetime` | `datetime` | Inherit from parent Activation |
| `properties.description` | `monty:hazard_detail`, `charter:area_priority` | Parse radius and priority from description text |
| Parent Activation | `links[rel=derived_from]` | Link to parent Event: `../charter-events/charter-event-{id}.json` |

> [!IMPORTANT]
> **Multi-hazard strategy**: Create **one Hazard item per disaster type** (following GDACS precedent). For an Area with `disaster:type: ["flood", "landslide"]`:
> - `charter-hazard-1019-juiz-de-fora-flood` with codes MH0600, FL, nat-hyd-flo-flo
> - `charter-hazard-1019-juiz-de-fora-landslide` with codes MH0901, LS, nat-geo-mmd-lan
>
> Same geometry, different `monty:hazard_codes`. This satisfies the Monty schema requirement of exactly one UNDRR-ISC 2025 code per Hazard item.

#### Hazard Detail

Parse Area `description` field for severity and metadata:

| Pattern | Monty Field | Example |
|---------|-------------|---------|
| `Radius (km): X` | `monty:hazard_detail.severity_value: X` | `8` |
| `Radius (km): X` | `monty:hazard_detail.severity_unit: "km"` | `"km"` |
| `Radius (km): X` | `monty:hazard_detail.severity_label: "Area radius"` | `"Area radius"` |
| `Priority: N` | `charter:area_priority: N` | `1` (not a severity metric) |

**CPE Status Mapping**: Charter Areas may include `cpe:status.stage` field. Map to `monty:hazard_detail.estimate_type`:

| CPE Stage | Estimate Type | Notes |
|-----------|---------------|-------|
| `notificationNew` | `primary` | First-pass AoI / notification phase |
| `readyToDeliver` | `secondary` | Delivered-handoff items |
| `readyToArchive` | `secondary` | Archived items |
| *(unknown)* | `primary` | Default for unrecognized stages |

This is an interim mapping pending full CPE stage documentation.

### Response Items

**Source**: Acquisition, Dataset, and Value-Added Product (VAP) items in Charter catalog
**Status**: ⚠️ Requires S3 access or partner credentials - implementation pending

Response items will link to parent Event/Hazard via `monty:corr_id`. Contact Zachary Foltz (zachary.foltz@acri-st.fr) for access details.

## Hazard Codes

Charter `disaster:type` values map to Monty hazard codes:

| Charter Type | UNDRR-ISC 2025 | GLIDE | EM-DAT | Notes |
|--------------|----------------|-------|---------|-------|
| flood | MH0600 | FL | nat-hyd-flo-flo | Flooding (refine to MH0603/MH0604 if flash/riverine) |
| fire | MH1301 | WF | nat-cli-wil-for | Wildfire / forest fire |
| earthquake | GH0101 | EQ | nat-geo-ear-gro | Ground shaking |
| volcano | GH0201 | VO | nat-geo-vol | Volcanic eruption |
| storm_hurricane | MH0400 | ST | nat-met-sto | Generic storm (refine to MH0403 if tropical) |
| cyclone | MH0403 | TC | nat-met-sto-tro | Tropical cyclone |
| tsunami | GH0301 | TS | nat-geo-ear-tsu | |
| landslide | MH0901 | LS | nat-geo-mmd-lan | |
| snow_hazard | MH1202 | SW | nat-met-ext-col | Snow/winter hazard |
| ice | MH0801 | CW | nat-met-ext-col | Ice storm/icing |
| oil_spill | TH0300 | — | tec-ind-che | Chemical spill (technological) |
| explosive_event | TH0600 | — | tec-ind-exp | Explosion (technological) |
| other | — | OT | — | Requires manual review - no UNDRR code |

**Deprecated types** (older activations):
- `storm_hurricane_rural`, `storm_hurricane_urban` → map as `storm_hurricane`
- `flood_large` → MH0604, `flood_flash` → MH0603

> [!NOTE]
> - UNDRR-ISC 2025 code is **required** for Hazard items (exactly one per item)
> - GLIDE and EM-DAT codes are optional but recommended for interoperability
> - `other` has no UNDRR code - manual review required before producing Hazard item
> - Deprecated types (`storm_hurricane_rural`, `flood_large`, etc.) mapped in CSV
> - Apply `hazard_profiles.get_canonical_hazard_codes()` after mapping for standard format

## Implementation Guide

### Step 1: Fetch and Map Activation

```bash
# Fetch activation
curl -s https://supervisor.disasterscharter.org/api/activations/act-1019 > act-1019.json

# Extract fields
cat act-1019.json | jq '{
  activation_id: .properties["disaster:activation_id"],
  types: .properties["disaster:type"],
  country: .properties["disaster:country"],
  datetime: .properties.datetime,
  geometry: .geometry
}'
```

Create Event item:

```json
{
  "stac_version": "1.0.0",
  "stac_extensions": ["https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json"],
  "type": "Feature",
  "id": "charter-event-1019",
  "collection": "charter-events",
  "geometry": {"type": "Point", "coordinates": [-43.202, -21.547]},
  "properties": {
    "title": "[Act-1019/Call-1166] Flood in Brazil",
    "datetime": "2026-02-24T17:09:00Z",
    "monty:country_codes": ["BRA"],
    "monty:hazard_codes": ["MH0600", "FL", "nat-hyd-flo-flo", "MH0901", "LS", "nat-geo-mmd-lan"],
    "monty:corr_id": "20260224T170900-BRA-HM-FLOOD-001-GCDB",
    "roles": ["event", "source"]
  },
  "links": [
    {"rel": "via", "href": "https://supervisor.disasterscharter.org/api/activations/act-1019"}
  ]
}
```

### Step 2: Fetch and Map Areas

```bash
# Extract area links
cat act-1019.json | jq -r '.links[] |
  select(.rel == "related" and .title | startswith("[Area]")) |
  .href'

# Fetch area
curl -s "https://supervisor.disasterscharter.org/api/activations/act-1019/areas/Juiz_de_Fora-QVwJEJDB0IZNzAO3SVGtOw__.json" > area.json
```

Create Hazard item (one per disaster type):

```json
{
  "stac_version": "1.0.0",
  "stac_extensions": ["https://ifrcgo.org/monty-stac-extension/v1.1.0/schema.json"],
  "type": "Feature",
  "id": "charter-hazard-1019-juiz-de-fora-flood",
  "collection": "charter-hazards",
  "geometry": {"type": "Polygon", "coordinates": [[[-43.3, -21.6], ...]]},
  "properties": {
    "title": "Juiz de Fora",
    "datetime": "2026-02-24T17:09:00Z",
    "monty:country_codes": ["BRA"],
    "monty:hazard_codes": ["MH0600", "FL", "nat-hyd-flo-flo"],
    "monty:corr_id": "20260224T170900-BRA-HM-FLOOD-001-GCDB",
    "monty:hazard_detail": {
      "severity_value": 8,
      "severity_unit": "km",
      "severity_label": "Area radius"
    },
    "charter:area_priority": 1,
    "roles": ["hazard", "source"]
  },
  "links": [
    {"rel": "derived_from", "href": "../charter-events/charter-event-1019.json"}
  ]
}
```

### Step 3: Validate

```bash
npm run check-examples
```

## Examples

| Activation | Type | Country | Date | Files |
|------------|------|---------|------|-------|
| Act-896 | Earthquake | ECU | Apr 2016 | [charter-event-896.json](../../../../examples/charter-events/charter-event-896.json) |
| Act-1019 | Flood + Landslide | BRA | Feb 2026 | Multi-hazard example (implementation reference) |

## Reference Files

Upstream data examples (actual Charter API responses):
- [act-1000-activation.json](./act-1000-activation.json) - Single hazard activation (earthquake)
- [act-1000-area-epi.json](./act-1000-area-epi.json) - Earthquake area example
- [act-1019-activation.json](./act-1019-activation.json) - Multi-hazard activation (flood + landslide)
- [act-1019-area-juiz-de-fora.json](./act-1019-area-juiz-de-fora.json) - Flood area example

## Resources

- [International Charter Website](https://disasterscharter.org/)
- [STAC Index - Charter Catalog](https://stacindex.org/catalogs/disasters-charter-mapper-catalog)
- [Disaster STAC Extension](https://github.com/Terradue/stac-extensions-disaster)
- [Monty STAC Extension Spec](../../../../README.md)
