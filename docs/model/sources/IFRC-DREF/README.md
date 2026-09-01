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

   An event with no field reports (`"field_reports": []`) still passes this filter and
   still produces an event item — it just produces no impact items (see below).

2. For each event:
   - Basic event information is extracted
   - Field reports are used to generate impact items
   - Country information is used for geometry generation, unioning polygons
     across all listed countries when there is more than one

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
            "id": int,  # disambiguates impact item IDs across reports
            "countries": [
                {
                    "name": str,
                    "iso3": str
                }
            ],
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
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | Generated              | Yes      | From country ISO3, unioned across all of the event's countries when there is more than one |
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
| [processing:version](https://github.com/stac-extensions/processing) | Generated | Semantic version of the transformer that generated the item, via the `processing:` extension |
| [processing:software](https://github.com/stac-extensions/processing) | Generated | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension |

### Impact Items

Impact items are generated from **every** field report on the event (not just
the first), with multiple impact types per report:

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

Each field report yields one item per impact type that has at least one
truthy (non-zero, non-empty) source field — a field report where all three
source fields for a type are explicit zeros (e.g. `num_dead: 0`) produces no
item for that type, with:
- ID format: `ifrcevent-impact-{event_id}-{impact_type}-{field_report_id}` —
  the field report ID disambiguates items when more than one report on the
  same event carries a value for the same impact type.
- Geometry generated from the field report's own `countries` (unioned when
  there is more than one), falling back to the parent event's geometry when
  the field report lists no usable country.
- [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) taken from the field report's own `countries[].iso3`, falling back to the parent event's country codes when the field report lists none
- Impact details including:
    - [category](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) ([ALL_PEOPLE](../../../model/taxonomy.md#exposure-category))
    - [type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (specific [impact type](../../../model/taxonomy.md#impact-type))
    - [value](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (first truthy value from the three source fields, in the order shown in the Source Fields column above — the other two are discarded, not cross-checked)
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
| Cyclone             | TC    | nat-met-sto-tro | **MH0306**                     | MH-WIND    | Depression or Cyclone — the **default**, see the cyclone rule below |
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

##### The cyclone rule

GO's `Cyclone` type is not exclusively tropical: sampling 200 of the 476
Cyclone operations on GO (2026-07), 1 is explicitly extratropical (`ARG:
Extratropical Cyclone - Misiones`) and 137 explicitly name a tropical system
(`hurricane`, `typhoon`, `tropical cyclone/storm`, or the `TC`/`TCs`
abbreviation, e.g. `TC Alfred`, `TCs Nika (Toraji) and Ofel`) in the event
**`name`**. The remaining 62 are ambiguous from the name alone — often a bare
storm name (`Cyclone Beryl`, `Cyclone Gamane`) that is almost certainly
tropical but isn't textually marked as such.

So: **default to `MH0306` / `TC` / `nat-met-sto-tro`** (the crosswalk's
"Depression or Cyclone" row), and refine using the event **`name`** only:

- `extratropical` / `extra-tropical` → `MH0307` / `EC` / `nat-met-sto-ext`
- `hurricane`, `typhoon`, `tropical`, or `\bTCs?\b` → `MH0309` / `TC` /
  `nat-met-sto-tro`

Both refinements keep `TC` / `nat-met-sto-tro` as the GLIDE/EM-DAT companions
where the crosswalk pairs them with MH0306 or MH0309 — that pair is not
tropical-specific; the same `TC` / `nat-met-sto-tro` row resolves to MH0306,
MH0308 or MH0309 depending on the UNDRR name, so keeping it on the default row
does not overclaim precision the way the UNDRR code would. Only the
extratropical branch changes the GLIDE/EM-DAT pair, because that's a genuinely
different crosswalk row (`EC` / `nat-met-sto-ext`).

This under-covers the ambiguous 62 — a bare storm name is not detectable
without cross-referencing IBTrACS or another tropical-cyclone track database,
which is out of scope for a string match on `name` — but it never makes an
outcome worse than today's blanket `MH0306`: every event either gains a more
specific code or keeps the default it already had. The repo-wide `MH0306` vs
`MH0309` convention for sources that don't disambiguate at all is still being
settled in [#94](https://github.com/IFRCGo/monty-stac-extension/issues/94);
this rule only changes what IFRC DREF does with information GO already gives it.

##### The fire rule

GO has a single `Fire` type covering both vegetation and structural fires, and
wildfires dominate it — of the 25 most recent, the Greek, French, Spanish,
Algerian, Moroccan, Tunisian, Portuguese, Chilean, Bolivian, Patagonian and
Victorian operations are all wild or forest fires, against four structural ones.
Mapping the whole type to the industrial-fire code would file most DREF fire
operations under the *Technological* family and stop them correlating with the
`EN0205` / `WF` that EM-DAT, CEMS, IDMC, IDU, GLIDE, DesInventar and PDC use for
the same fires.

So: **default to `EN0205` / `WF` / `nat-cli-wil-wil`**, and use `TL0305` / `FR`
instead when the **event `name`** — not `summary` — identifies a structural or
industrial fire:

- `factory`, `industrial`, `plant`, `refinery`, `warehouse` → `TL0305` / `FR` /
  `tec-ind-fir-fir` (Fire, Industrial Failure)
- `landfill`, `market`, `building`, `structural`, `residential`, `apartment`,
  `camp`, `slum` → `TL0305` / `FR` / `tec-mis-fir-fir` (Fire, Miscellaneous
  Failure) — matching the crosswalk's own split between the two EM-DAT fire keys

`summary` is deliberately excluded. GO's `summary` is narrative impact prose,
and it uses exactly these words to describe what a wildfire *destroyed* —
"threatening residential areas" (Greece, Turkey wildfires), "urban-forest
interface" (Patagonia), damage tallies that count "buildings" (a Korean
wildfire that damaged over 200 of them) — not what kind of fire it was.
Checked against every DREF `Fire` operation on GO (225, 2026-07): matching
`name` **and** `summary` produces 15 false positives, all of them genuine
wildfires reclassified as structural because their damage narrative mentions a
building or a neighbourhood; restricting the match to `name` alone produces
**zero** false positives against the same set, because operations that are
actually structural or industrial say so in the title (`Factory Fire in
Daejeon`, `Nairobi Residential Fire`, `AMSA Landfill Fire`, `Hargeisa Market
Fire`) rather than only in the body text. The rule is still a heuristic — GO
gives no field beyond free text to key on — but it is now the version that
survived being checked against the real data, not the first list that seemed
reasonable.

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability, and all three must come from the same crosswalk row — a triplet assembled from different rows resolves inconsistently downstream. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be used following the characteristics of the event, as the volcanic, epidemic and fire rows above describe.

This mapping enables standardized hazard categorization while preserving IFRC's original disaster type classification in the source properties.

## Quality Control Notes

1. Events are filtered to DREF and Emergency Appeal operations (`atype` 0 and 1).
2. Only the 15 [accepted disaster types](#accepted-disaster-types) are processed.
3. Impact values are **not** cross-referenced between sources: for each type,
   the first truthy value among the primary/government/other source fields
   (in that order) is taken as-is, and the other two are silently discarded —
   there is no reconciliation or consistency check between them.
4. Geometry is generated from country codes, unioning polygons across all
   listed countries when there is more than one; impact items fall back to
   the parent event's geometry whenever none of their own field report's
   countries resolves to a geometry (an empty list, or a list where every
   entry fails geocoding).
5. Every field report on an event is processed independently — an event with
   *N* field reports and *M* impact types with a truthy value can produce up
   to *N* × *M* impact items, distinguished by the field report ID in each
   item's ID.
