# IFRC DREF

The IFRC Disaster Relief Emergency Fund (DREF) provides immediate financial support to National Red Cross and Red Crescent Societies for early action and response to disasters and crises.

## Collection Metadata

- **Name**: IFRC DREF Events
- **Code**: `ifrcevent`
- **Source Organization**:
    - Name: International Federation of Red Cross and Red Crescent Societies (IFRC)
    - Website: <https://www.ifrc.org>
    - Contact: <https://www.ifrc.org/contact-us>
- **Source Type**: International Organization
- **Source Data license**: None stated by the source (checked 2026-07)
- **Source Category**: Event, Impact
- **API Documentation**: <https://goadmin-stage.ifrc.org/api/v2/>

## Data Sourcing

### API Endpoints

- **Base URL**: `https://goadmin-stage.ifrc.org/api/v2/`
- **Events Endpoint**: `/event/`
- **Parameters**:
    - `dtype`: Disaster type filter
    - `appeal_type`: Appeal type filter — GO's `atype` is `0` (DREF) or `1` (Emergency Appeal)
    - `id`: Specific event ID

### Data Retrieval Process

1. Events are filtered based on:
   - Appeal type — an event is kept when *every* one of its appeals is `atype` 0 or 1, so
     the collection covers DREF **and** Emergency Appeal operations despite its name
   - Valid disaster type
   - Presence of field reports

2. For each event:
   - Basic event information is extracted
   - Impact data is collected from field reports
   - Country information is used for geometry generation

## Data Structure

### Event Data Model

```python
{
    "id": int,
    "name": str,
    "summary": str,
    "dtype": {
        "name": str  # Disaster type
    },
    "countries": [
        {
            "name": str,
            "iso3": str
        }
    ],
    "disaster_start_date": datetime,
    "appeals": [
        {
            "atype": int  # Appeal type: 0 = DREF, 1 = Emergency Appeal
        }
    ],
    "field_reports": [
        {
            "num_dead": int,
            "gov_num_dead": int,
            "other_num_dead": int,
            "num_injured": int,
            "gov_num_injured": int,
            "other_num_injured": int,
            # ... similar pattern for other impact metrics
        }
    ]
}
```

### Accepted Disaster Types

GO exposes 24 disaster types (`dtype.name`); Monty ingests the 15 below, matched
on the exact string (including the `Pluvial/` prefix, which is part of the GO
vocabulary):

- Earthquake
- Cyclone
- Volcanic Eruption
- Tsunami
- Flood
- Cold Wave
- Fire
- Heat Wave
- Drought
- Storm Surge
- Landslide
- Pluvial/Flash Flood
- Epidemic
- Civil Unrest
- Insect Infestation

The other 9 are **out of scope**, each for a reason checked against GO's own
appeal counts and event names rather than assumed — full analysis in
[#96](https://github.com/IFRCGo/monty-stac-extension/issues/96):

| GO disaster type       | DREF + EA appeals | Why it's excluded |
| ----------------------- | ---: | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Other                  | 542  | Not a hazard by definition — there is nothing to resolve |
| Population Movement    | 404  | An impact (displacement), not a hazard |
| Food Insecurity        | 128  | An impact, usually of drought (MH0401) |
| Complex Emergency      | 37   | Not one hazard: sampled events mix heat waves, missile strikes, armed conflict and displacement under the same `dtype` |
| Transport Accident     | 10   | Mode-ambiguous: sampled events are road, rail, air and water accidents with no dominant mode to default to |
| Chemical Emergency     | 2    | Category-ambiguous: sampled events are spills, explosions, fires and poisonings, not predominantly one HIP |
| Biological Emergency   | 1    | Category-ambiguous: sampled events include measles and FMD outbreaks alongside water contamination and a poison-gas incident — overlaps `Epidemic` without being a subset of it |
| Radiological Emergency | 0    | No DREF/EA appeals to date; would map to TL0601 if populated |
| Transport Emergency    | 0    | No DREF/EA appeals to date; a duplicate of Transport Accident's ambiguity |

Counts are DREF + Emergency Appeal operations, checked 2026-07-31. This list is
a decision, not a filter of convenience — a type only stays excluded because
either it isn't a hazard or its `dtype` genuinely spans more than one HIP with
no defensible default, not because mapping it was inconvenient.

## Item Mapping

### Event Items

| STAC Field                                                                                                               | IFRC Field             | Required | Notes                                |
| ------------------------------------------------------------------------------------------------------------------------ | ---------------------- | -------- | ------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `ifrcevent-event-{id}` | Yes      | Prefixed ID                          |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | Generated              | Yes      | From country ISO3                    |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | disaster_start_date    | Yes      | Start date of the disaster           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | name                   | Yes      | Event name                           |
| [description](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)            | summary                | No       | Event summary                        |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | disaster_start_date    | Yes      |                                      |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | disaster_start_date    | Yes      | Same as start (no end date provided) |

#### Monty Extension Fields

| Field                                                       | Source           | Notes                           |
| ----------------------------------------------------------- | ---------------- | ------------------------------- |
| [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number) | Fixed value (1)  | DREF doesn't track episodes     |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)     | dtype.name       | Mapped to standard hazard codes |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)   | countries[].iso3 | Array of ISO3 codes             |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |

### Impact Items

Impact items are generated from field reports data, with multiple impact types:

| [Impact Type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) | Source Fields | [Category](https://github.com/IFRCGo/monty-stac-extension#exposure-category) |
| -------------------- | -------------------------------------------------------------------------------------- | ---------- |
| [Death](../../../model/taxonomy.md#impact-type) | num_dead, gov_num_dead, other_num_dead | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Displaced](../../../model/taxonomy.md#impact-type) | num_displaced, gov_num_displaced, other_num_displaced | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Injured](../../../model/taxonomy.md#impact-type) | num_injured, gov_num_injured, other_num_injured | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Missing](../../../model/taxonomy.md#impact-type) | num_missing, gov_num_missing, other_num_missing | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Affected](../../../model/taxonomy.md#impact-type) | num_affected, gov_num_affected, other_num_affected | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Assisted](../../../model/taxonomy.md#impact-type) | num_assisted, gov_num_assisted, other_num_assisted | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Potentially Affected](../../../model/taxonomy.md#impact-type) | num_potentially_affected, gov_num_potentially_affected, other_num_potentially_affected | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Highest Risk](../../../model/taxonomy.md#impact-type) | num_highest_risk, gov_num_highest_risk, other_num_highest_risk | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |

Each impact type gets its own item with:
- ID format: `ifrcevent-impact-{event_id}-{impact_type}`
- Same geometry as parent event
- Impact details including:
    - [category](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) ([ALL_PEOPLE](../../../model/taxonomy.md#exposure-category))
    - [type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (specific [impact type](../../../model/taxonomy.md#impact-type))
    - [value](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (first non-null value from the three source fields)
    - [estimate_type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (PRIMARY)

#### Hazard Type Mapping

GO carries a disaster type name (`dtype.name`) and nothing more granular, so the
mapping below is keyed on that exact string. The **2025 UNDRR-ISC** code is the
**reference classification** for the Monty extension; the GLIDE and EM-DAT codes
are its counterparts from the same row of the
[cross-classification mapping](../../taxonomy.md#cross-classification-mapping)
and are never chosen independently of it.

| IFRC `dtype.name`   | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Cluster    | Notes |
| ------------------- | ----- | --------------- | ------------------------------ | ---------- | ----- |
| Earthquake          | EQ    | nat-geo-ear-gro | **GH0101**                     | GEO-SEIS   | All earthquake phenomena were consolidated into GH0101 in 2025 |
| Cyclone             | TC    | nat-met-sto-tro | **MH0306**                     | MH-WIND    | Depression or Cyclone. GO's `Cyclone` is a mixed container — extratropical and high-latitude systems are filed under it alongside tropical ones — so the broader code is used rather than MH0309 (Tropical Cyclone). The repo-wide convention is being settled in [#94](https://github.com/IFRCGo/monty-stac-extension/issues/94) |
| Volcanic Eruption   | VO    | nat-geo-vol-vol | **GH0201**                     | GEO-VOLC   | Eruption, phenomenon unspecified. HIP 2025 has no volcanic chapeau (GH0201–GH0205 only), so GH0201 carries the general case, per the `VO` / `nat-geo-vol-vol` crosswalk row — *not* because the event is a lava flow. Refine to GH0202 (ash/tephra fall) or GH0204 (lahars) only when the operation names that phenomenon |
| Tsunami             | TS    | nat-geo-ear-tsu | **MH0705**                     | MH-MARINE  | Reclassified from Geological to Meteorological & Hydrological in 2025 |
| Flood               | FL    | nat-hyd-flo-flo | **MH0600**                     | MH-WATER   | Flooding (chapeau) |
| Cold Wave           | CW    | nat-met-ext-col | **MH0502**                     | MH-TEMP    | |
| Fire                | WF    | nat-cli-wil-wil | **EN0205**                     | ENV-FOREST | Wildfires — the **default**, see the fire rule below |
| Heat Wave           | HT    | nat-met-ext-hea | **MH0501**                     | MH-TEMP    | |
| Drought             | DR    | nat-cli-dro-dro | **MH0401**                     | MH-PRECIP  | |
| Storm Surge         | SS    | nat-met-sto-sur | **MH0703**                     | MH-MARINE  | |
| Landslide           | LS    | nat-geo-mmd-lan | **GH0300**                     | GEO-GFAIL  | Gravitational Mass Movement (chapeau), matching the GDACS/EM-DAT/GLIDE convention |
| Pluvial/Flash Flood | FF    | nat-hyd-flo-fla | **MH0603**                     | MH-WATER   | Flash Flooding |
| Epidemic            | EP    | nat-bio-epi-dis | **BI0101**                     | BIO-INFECT | General infectious disease. BIO-INFECT has no chapeau either, so BI0101 carries the unspecified case per the `EP` / `nat-bio-epi-dis` crosswalk row, despite its "Airborne Diseases" label. Refine when the operation names the pathogen: cholera → BI0110, viral haemorrhagic fevers → BI0109, parasitic → BI0105 |
| Civil Unrest        | —     | —               | **SO0103**                     | SOC-CONF   | The [cross-classification mapping](../../taxonomy.md#cross-classification-mapping) has no GLIDE or EM-DAT row for the Societal hazard type, so this triplet is UNDRR-only — a single code is a valid `monty:hazard_codes` value |
| Insect Infestation  | IN    | nat-bio-inf-inf | **BI0401**                     | BIO-INSECT | General infestation. `nat-bio-inf-inf` is used rather than `nat-bio-inf-loc`, whose crosswalk row is inconsistent (it appears twice, once labelled "Insect pest infestation"→BI0401 and once "Locust infestation"→BI0402); refine to BI0402 only when the operation names locusts specifically |

##### The fire rule

GO has a single `Fire` type covering both vegetation and structural fires, and
wildfires dominate it — of the 25 most recent, the Greek, French, Spanish,
Algerian, Moroccan, Tunisian, Portuguese, Chilean, Bolivian, Patagonian and
Victorian operations are all wild or forest fires, against four structural ones.
Mapping the whole type to the industrial-fire code would file most DREF fire
operations under the *Technological* family and stop them correlating with the
`EN0205` / `WF` that EM-DAT, CEMS, IDMC, IDU, GLIDE, DesInventar and PDC use for
the same fires.

So: **default to `EN0205` / `WF` / `nat-cli-wil-wil`**, and use
`TL0305` / `FR` / `tec-ind-fir-fir` (Fire, Industrial Failure) instead when
`name` or `summary` identifies a structural or industrial fire — match on
`factory`, `industrial`, `plant`, `refinery`, `warehouse`, `landfill`, `market`,
`building`, `structural`, `residential`, `apartment`, `camp`, `slum`, `urban`.
The rule is a heuristic because the source category is genuinely ambiguous; it is
documented here so the ambiguity is visible rather than hidden in a lookup table.

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability, and all three must come from the same crosswalk row — a triplet assembled from different rows resolves inconsistently downstream. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be used following the characteristics of the event, as the volcanic, epidemic and fire rows above describe.

This mapping enables standardized hazard categorization while preserving IFRC's original disaster type classification in the source properties.

## Quality Control Notes

1. Events are filtered to DREF and Emergency Appeal operations (`atype` 0 and 1)
2. Only the 13 [accepted disaster types](#accepted-disaster-types) are processed
3. Impact values are cross-referenced between sources (government, other)
4. Geometry is generated from country codes for consistent spatial representation
