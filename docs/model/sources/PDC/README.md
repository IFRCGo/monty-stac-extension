# Pacific Disaster Center (PDC)

The Pacific Disaster Center (PDC) tracks a wide range of natural and human made hazards viz. **Tropical Cyclone**, **Earthquake**, **Flood**, **Landslides**, **Wildfire**, **Drought**, **Volcanic Eruptions** etc to support disaster preparedness, response, and risk reduction efforts.

This document describes the PDC transformer at
[IFRCGo/pystac-monty@b831436](https://github.com/IFRCGo/pystac-monty/commit/b831436a02deedbee6effaf5a3d1a1d76ddd3000)
(`pystac_monty/sources/pdc.py`). Each statement about the items was checked by a run of that
transformer on the upstream fixtures in
[`tests/data/pdc/`](https://github.com/IFRCGo/pystac-monty/tree/b831436a02deedbee6effaf5a3d1a1d76ddd3000/tests/data/pdc)
(hazard `313159`, a landslide warning in Peru), and on variants of them: no exposure data, two snapshots,
two countries and an unknown hazard type. The examples and the sample data of this repository use
hazard `352320`, an observed volcano in Mexico, because the transformer now makes no item for a
warning (see [Observed hazards only](#observed-hazards-only-temporary-rule)).

## Collection: `pdc-events`

A STAC collection hold all the PDC events.

- Name: Pacific Disaster Center
- Code: PDC
- Source organization: Pacific Disaster Center
- Source code:
- Source type: International Organization
- Source organization email: <info@pdc.org>
- Source URL: <https://www.pdc.org/>
- Source Data License: Restricted — disaster/emergency management use only, no redistribution without authorization (PDC Terms & Conditions)
- Source for: event, hazard, impact

The three PDC collections (`pdc-events`, `pdc-hazards`, `pdc-impacts`) are marked private
([#195](https://github.com/IFRCGo/monty-stac-extension/pull/195)), because of this license.

Examples: the transformer output for the sample data of this folder, with the `self`, `collection` and
`related` links changed to point into this repository, and only two of the 19 impact items:

- Event: [pdc-event-62006159-a6da-45d8-b739-8d0940876fa1-352320.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-events/pdc-event-62006159-a6da-45d8-b739-8d0940876fa1-352320.json)
- Hazard: [pdc-hazard-62006159-a6da-45d8-b739-8d0940876fa1-352320.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-hazards/pdc-hazard-62006159-a6da-45d8-b739-8d0940876fa1-352320.json)
- Impact, total population: [pdc-impact-…-population-total-MEX-0.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-impacts/pdc-impact-62006159-a6da-45d8-b739-8d0940876fa1-352320-1751032040986-1-population-total-MEX-0.json)
- Impact, capital: [pdc-impact-…-capital-total-MEX-0.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/pdc-impacts/pdc-impact-62006159-a6da-45d8-b739-8d0940876fa1-352320-1751032040986-1-capital-total-MEX-0.json)

The fixture is in this folder, as sample data: the hazard record
[352320-hazard_data.json](352320-hazard_data.json) and the exposure snapshot
[352320-exposure_detail.json](352320-exposure_detail.json). The bundle
[352320-bundle.json](352320-bundle.json) names the two files for the batch exporter `pdc`.
`scripts/check_example_drift.py` runs the transformer on the bundle and compares the result with
the four examples.

## Observed hazards only (temporary rule)

PDC publishes two kinds of hazard record with the same fields:

- an **observed hazard**: the hazard occurred, or an instrument or a person detected or reported it
  (an earthquake, a fire that a satellite detected, volcanic activity that was reported);
- a **warning**: an agency or a model says that a hazard is expected or possible (a flood watch, a
  fire weather statement, a landslide warning from a model, a tropical cyclone forecast).

Monty has no field that says "this is a forecast", and no class for exposure
([Discussion #110](https://github.com/IFRCGo/monty-stac-extension/discussions/110),
[Discussion #168](https://github.com/IFRCGo/monty-stac-extension/discussions/168)). Before this rule,
the transformer wrote a warning as an observed event and hazard. So, as a temporary rule, **the
transformer makes items only for an observed hazard**. A warning gives no item. The decision, the
evidence and the evaluation are in [#232](https://github.com/IFRCGo/monty-stac-extension/issues/232).

No PDC field tells the two kinds apart: `severity_ID` is a threat level (`WARNING` means "imminent or
occurring"), and `category_ID` and `status` are the same for the two. The transformer reads the
**first sentence of `description`**, which PDC writes from one template for each product:

| First sentence (pattern) | Example | Status |
| --- | --- | --- |
| `has occurred` | "An earthquake with a magnitude of 5.5 … has occurred …, as reported by … USGS" | observed |
| `has been detected` | "A Potential Large and/or Intense Wildfire has been detected for …" | observed |
| `reports … activity` | "National Interagency Fire Center (NIFC) reports Wildfire activity for …" | observed |
| `has been reported`, `have been reported` | "Volcanic activity has been reported for Popocatepetl in Mexico, by …" | observed |
| issuer `National Bushfire Extents` | "Geoscience Australia National Bushfire Extents (NRT) has issued a Wildfire warning" (the mapped extent of an active fire) | observed |
| `forecast has been issued` | "A tropical cyclone forecast has been issued by National Hurricane Center (NHC) …" | warning |
| `has been indicated by` | "A Landslide Warning has been indicated by the Landslide Hazard Assessment Model (LHASA) …" | warning |
| `has issued`, `have issued` | "NWS Miami FL has issued a FA Watch for …" | warning |
| `was issued`, `were issued`, `has been issued`, `have been issued` | "A Mekong River Commission (MRC) Riverine Flood Warning was issued for …" | warning |
| no pattern | | unknown |

The patterns are tried in this order, so the observed patterns come first. One more check uses the
dates: when `start_Date` is after `create_Date`, the status is `warning`. The reverse is not a sign
of an observed hazard, because most warnings start on the day of their creation.

Only the status `observed` gives items. A `warning` or an `unknown` record is skipped, and the
transform summary counts it in `skipped_rows` (not in `failed_rows`). An `unknown` record also gives a
warning in the log, so a new PDC template shows as a count that rises.

> [!WARNING]
> **Limits of this rule.**
>
> - It reads text templates. PDC can change them.
> - The patterns come from 197 records of four hazard types (flood, wildfire, earthquake, tropical
>   cyclone), one landslide and one volcano. On these records, no warning is kept as observed. One
>   observed record and 10 records that are both observed and forecast are skipped: 7 flood warnings
>   where flooding already occurs, 2 tropical cyclones (an observed position and a forecast) and 1
>   fire weather statement.
> - Most floods and all tropical cyclones of PDC give no item with this rule.
> - Most observed wildfire records are satellite heat detections that PDC calls "potential". The
>   heat can come from an industrial source or from agricultural burning.
> - The population and capital figures of an observed hazard are still exposure from a model, not
>   observed impacts (see [Impact Detail](#impact-detail)).

## Data flow

The ETL ([montandon-etl](https://github.com/IFRCGo/montandon-etl), `apps/etl/etl_tasks/pdc.py` and
`apps/etl/extraction/sources/pdc/extract.py`) uses these PDC Sentry endpoints:

1. **Hazard list:** `POST https://sentry.pdc.org/hp_srv/services/hazards/t/json/search_hazard`, with a
   `createDate` window. The window starts at `PDC_START_DATE` (default: the first day of the current
   month) and ends now.
2. **Exposure list** of each hazard: `https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure`.
   It gives the timestamps of the exposure snapshots.
3. **Exposure detail** of each snapshot: `https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/{timestamp}`.
4. **Hazard area** (GeoJSON): `https://sentry.pdc.org/hp_srv/services/mags/1/json/get_mags?hazard_id={hazard_ID}`.

The ETL keeps a hash of each exposure detail, without its timestamp. A snapshot with the same
content as the one before it is not sent again to the transformer.

### Transformer input

`PDCDataSource` takes a `PDCDataSourceType`:

```python
PDCDataSourceType(
    source_url: str,
    uuid: str,                                   # the PDC hazard uuid
    hazard_data: File | Memory,                  # the hazard list (search_hazard response)
    exposure_detail_data: list[File | Memory],   # zero, one or more snapshots of this hazard
    geojson_path: str,                           # where the hazard area GeoJSON is stored
)
```

`exposure_detail_data` can be empty. A single `File` or `Memory` is also accepted.

## Items made for one PDC hazard

| Item | Number | Condition |
| --- | --- | --- |
| Event | 1 | When the hazard is [observed](#observed-hazards-only-temporary-rule) and `type_ID` is in the [Hazard Type Mapping](#hazard-type-mapping) |
| Hazard | 1 | Same as the event |
| Impact | One per snapshot × [impact field](#impact-detail) × `totalByAdmin` row | Only for a valid snapshot, and only when the field has a value |

For the sample data (one snapshot, one `totalByAdmin` row), the transformer makes 21 items: the
event, the hazard and 19 impact items. With a second snapshot that has three `totalByAdmin` rows,
it makes 78 items: the event, the hazard, 19 impact items for the first snapshot and 57 for the
second.

## Event Item

| STAC field | PDC field | Description |
| --- | --- | --- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | `uuid`, `hazard_ID` | `pdc-event-{uuid}-{hazard_ID}`, e.g. `pdc-event-62006159-a6da-45d8-b739-8d0940876fa1-352320`. The id does not change when a new snapshot comes |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | `latitude`, `longitude` | Point |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | `longitude`, `latitude` | The bbox of the point |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `pdc-events` | |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | `start_Date` | Milliseconds since epoch, converted to UTC |
| [start_datetime, end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | `start_Date`, `end_Date` | Milliseconds since epoch, converted to UTC |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | `hazard_Name` | |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | `description` | HTML converted to Markdown. `NA` when it is empty |
| roles | Fixed | `["source", "event"]` |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | `totalByCountry[].country` of all the snapshots | The ISO3 codes of all the snapshots, earliest snapshot first, in source order, with no duplicates. Without exposure data, the country of the hazard point from the geocoder, else `UNK` |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | `type_ID` | The three codes of the [Hazard Type Mapping](#hazard-type-mapping), e.g. `["GH0300", "LS", "nat-geo-mmd-lan"]` |
| [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number) | Fixed | Always `1`. PDC has no episode number |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | `hazard_ID` | e.g. `352320` |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id) | Generated | Generated following the [event correlation](../../correlation_identifier.md) convention, with the first country code, e.g. `20250627-MEX-979608-GH0201-1-GCDB` |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Derived | The hazard keywords, then the `admin0` names of `totalByCountry` of all the snapshots, with no duplicates, e.g. `["Geological", "Lava Flows (Lava Domes)", "Volcanic", "Mexico"]`. Without exposure data, no country name |
| `Maps` asset | `geojson_path` | The hazard area GeoJSON, with `type: geojson`. The ETL stores a copy of the `get_mags` response and gives its URL. The examples use the PDC `get_mags` URL |
| `report` asset | `snc_url` | The PDC report page, with `type: html`. Only when `snc_url` has a value |
| `related` links | Generated | To the hazard item and to each impact item |
| [processing:version](https://github.com/stac-extensions/processing) | Generated | Semantic version of the transformer that generated the item, via the `processing:` extension |
| [processing:software](https://github.com/stac-extensions/processing) | Generated | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension |

> [!NOTE]
> The earliest snapshot comes first, so a new snapshot can only add countries at the end of
> `monty:country_codes`. The first code, and so `monty:corr_id`, stays the same
> ([IFRCGo/pystac-monty#273](https://github.com/IFRCGo/pystac-monty/pull/273),
> [#276](https://github.com/IFRCGo/pystac-monty/pull/276)). The rules for multi-country items are in
> [`monty:country_codes`](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes).

### Hazard Type Mapping

PDC (Pacific Disaster Center) tracks a wide range of natural and geopolitical hazards. The **2025 UNDRR-ISC** code is the **reference classification** for the Monty extension. The transformer maps the `type_ID` value of the hazard:

**Natural Hazards:**

| PDC Type            | `type_ID`            | GLIDE | EM-DAT              | **UNDRR-ISC 2025** (Reference) | Cluster      | Description                      |
| ------------------- | -------------------- | ----- | ------------------- | ------------------------------ | ------------ | -------------------------------- |
| Avalanche           | `AVALANCHE`          | AV    | nat-hyd-mmw-ava     | **MH0801**                     | MH-TERR      | Avalanche                        |
| Biomedical          | `BIOMEDICAL`         | EP    | nat-bio-epi-dis     | **BI0101**                     | BIO-INFECT   | Infectious Diseases              |
| Drought             | `DROUGHT`            | DR    | nat-cli-dro-dro     | **MH0401**                     | MH-PRECIP    | Drought                          |
| Earthquake          | `EARTHQUAKE`         | EQ    | nat-geo-ear-gro     | **GH0101**                     | GEO-SEIS     | Earthquake                       |
| Extreme Temperature | `EXTREMETEMPERATURE` | HT    | nat-met-ext-hea     | **MH0501**                     | MH-TEMP      | Heatwave (also for cold, see the note) |
| Flood               | `FLOOD`              | FL    | nat-hyd-flo-flo     | **MH0600**                     | MH-WATER     | Flooding (chapeau)               |
| High Wind           | `HIGHWIND`           | VW    | nat-met-sto-sto     | **MH0301**                     | MH-WIND      | Wind (general)                   |
| Landslide           | `LANDSLIDE`          | LS    | nat-geo-mmd-lan     | **GH0300**                     | GEO-GFAIL    | Gravitational Mass Movement      |
| Severe Weather      | `SEVEREWEATHER`      | ST    | nat-met-sto-sto     | **MH0103**                     | MH-CONV      | Thunderstorm                     |
| Storm               | `STORM`              | ST    | nat-met-sto-sto     | **MH0103**                     | MH-CONV      | Thunderstorm                     |
| Tornado             | `TORNADO`            | TO    | nat-met-sto-tor     | **MH0305**                     | MH-WIND      | Tornado                          |
| Tropical Cyclone    | `CYCLONE`            | TC    | nat-met-sto-tro     | **MH0306**                     | MH-WIND      | Tropical Cyclone                 |
| Tsunami             | `TSUNAMI`            | TS    | nat-geo-ear-tsu     | **MH0705**                     | MH-MARINE    | Tsunami                          |
| Volcano             | `VOLCANO`            | VO    | nat-geo-vol-vol     | **GH0201**                     | GEO-VOLC     | Lava Flows                       |
| Wildfire            | `WILDFIRE`           | WF    | nat-cli-wil-wil     | **EN0205**                     | ENV-FOREST   | Wildfires                        |
| Winter Storm        | `WINTERSTORM`        | OT    | nat-met-sto-bli     | **MH0403**                     | MH-PRECIP    | Blizzard                         |

**Geopolitical Hazards:**

| PDC Type          | `type_ID`           | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Cluster      | Description                      |
| ----------------- | ------------------- | ----- | --------------- | ------------------------------ | ------------ | -------------------------------- |
| Active Shooter    | `ACTIVESHOOTER`     | OT    |                 | **SO0301**                     | SOC-BEH      | Violence                         |
| Civil Unrest      | `CIVILUNREST`       | CE    |                 | **SO0103**                     | SOC-CONF     | Civil Unrest                     |
| Political Conflict| `POLITICALCONFLICT` | CE    |                 | **SO0103**                     | SOC-CONF     | Civil Unrest (nearest code)      |
| Terrorism         | `TERRORISM`         | OT    |                 | **SO0301**                     | SOC-BEH      | Violence                         |

> [!NOTE]
> The codes of a type come from one row of the [Cross-Classification Mapping](../../taxonomy.md#cross-classification-mapping). The four geopolitical types have no EM-DAT code in that table, so they get only two codes. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.
>
> **Extreme Temperature:** the transformer always uses `MH0501` (Heatwave) and `HT`, also for a cold event. The correct codes for a cold event are `MH0502` and `CW`. PDC gives no field that tells heat from cold, so this is not fixed yet.
>
> **Unknown `type_ID`:** the transformer logs a warning, makes no item for the hazard, and counts the hazard as a failed row.
>
> **Types with no UNDRR-ISC 2025 code:** the transformer makes no item for the eight types below, logs a warning, and counts the hazard as a failed row. A hazard item must have one UNDRR-ISC 2025 code, and the 2025 profiles have no code at the granularity that PDC states for these types. A specific code would add precision that PDC does not give ([pystac-monty#296](https://github.com/IFRCGo/pystac-monty/issues/296)).
>
> | PDC Type   | `type_ID`    | Why no code fits                                                                      |
> | ---------- | ------------ | ------------------------------------------------------------------------------------- |
> | Accident   | `ACCIDENT`   | General accident. The Technological type has no general code.                         |
> | Combat     | `COMBAT`     | The type does not say if the conflict is international (`SO0101`) or not (`SO0102`).  |
> | Cyber      | `CYBER`      | The Cyberhazards cluster has seven specific codes and no general code.                |
> | High Surf  | `HIGHSURF`   | The 2025 profiles have no code for wave action.                                       |
> | Man Made   | `MANMADE`    | General man-made hazard. The Technological type has no general code.                  |
> | Marine     | `MARINE`     | The Marine-related cluster has no general code.                                       |
> | Occurrence | `OCCURRENCE` | The type has no hazard meaning.                                                       |
> | Weapons    | `WEAPONS`    | The type does not say which weapon or which use.                                      |
>
> **Scope decision — `HIGHWIND` ([pystac-monty#196](https://github.com/IFRCGo/pystac-monty/issues/196)):** PDC issues `HighWind` from NWS High Wind Warnings/Advisories — sustained wind of 40 mph (35 kt) or more for 1 hour or more, or gusts of 58 mph (50 kt) or more, when no tropical cyclone or thunderstorm is present. This is a general wind event, not a Beaufort-scale term. So it maps to **MH0301 (Wind)**, not **MH0303 (Gale)**. This choice follows the existing GLIDE↔EM-DAT↔UNDRR crosswalk in [taxonomy.md](../../taxonomy.md#complete-2025-hazard-list) (`VW` → `nat-met-sto-sto` → `MH0301`).

## Hazard Item

The hazard item is a copy of the event item, with these differences:

| STAC field | Value | Description |
| --- | --- | --- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | `pdc-hazard-{uuid}-{hazard_ID}` | The event id with the `pdc-hazard-` prefix |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `pdc-hazards` | |
| roles | Fixed | `["source", "hazard"]` |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | Derived | The UNDRR-ISC 2025 code only, e.g. `["GH0300"]` |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) | `severity_ID` | See below |
| `related` links | Generated | To the event item and to each impact item |

All the other fields (geometry, datetime, `monty:country_codes`, `monty:corr_id`, keywords, assets)
are the same as the event.

```json
{
  "severity_value": 0.1,
  "severity_unit": "PDC Severity Score",
  "severity_label": "<severity_ID, e.g. WARNING>",
  "estimate_type": "primary"
}
```

> [!WARNING]
> `severity_value` is always `0.1`. It is a placeholder, because the schema requires a value and PDC
> gives no number. Do not use it. The PDC severity is in `severity_label`.

## Impact item

The transformer makes one impact item for each snapshot, each [impact field](#impact-detail) and each
row of `totalByAdmin`, when the field has a value in that row. A field without a value gives no item.
An invalid snapshot is skipped with a warning; the event and the hazard are still made. When two
snapshots have the same timestamp, the transformer keeps the last one.

The impact item is a copy of the event item, with these differences:

| STAC field | Value | Description |
| --- | --- | --- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | Generated | `pdc-impact-{uuid}-{hazard_ID}-{timestamp_ms}-{episode}-{group}-{field}-{admin}`, see below |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `pdc-impacts` | |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | `timestamp` of the snapshot | Converted to UTC. `start_datetime` and `end_datetime` stay the same as the event |
| roles | Fixed | `["source", "impact"]` |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Generated | The title of the event, then the title text of the [impact field](#impact-detail), then the place of the row in parentheses (`admin2`, `admin1`, `country`, when they have a value): `Volcano - Popocatepetl, Mexico - Total population (MEX)` |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Generated | The keywords of the event, then the label of the impact type and the label of the exposure category from the [taxonomy](../../taxonomy.md#impact): `["Geological", "Lava Flows (Lava Domes)", "Volcanic", "Mexico", "Total Affected", "People (All Demographics)"]` |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | `totalByAdmin[].country` | The country of the row. One code |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) | The field | See [Impact Detail](#impact-detail) |
| `related` links | Generated | To the event item and to the hazard item |

The geometry (the hazard point), `monty:hazard_codes` (all three codes), `monty:corr_id` and the
assets are the same as the event. The first keywords are those of the event, so the keywords of an
impact item can name other countries than its `monty:country_codes`.

The parts of the impact id:

- `{timestamp_ms}`: the snapshot `timestamp` in milliseconds. PDC sends milliseconds or seconds
  with decimals (`1751032040.9863468` in the fixture). A value below 10¹¹ is read as seconds.
- `{episode}`: always `1`.
- `{group}-{field}`: the impact field, e.g. `population-total0_4`, `capital-total`.
- `{admin}`: the `country` of the row, then `admin1` and `admin2` when they have a value, in
  lowercase ASCII (`San Martín` → `san-martin`), then `-0`. When a row has the same
  `country`/`admin1`/`admin2` as a row before it, `-0` becomes the row index (`-1`, `-2`, …).

Example: `pdc-impact-62006159-a6da-45d8-b739-8d0940876fa1-352320-1751032040986-1-population-total-MEX-0`.

### Impact Detail

Each impact field is read from `totalByAdmin[].{group}.{field}.value`. `estimate_type` is always
`modelled`. `unit` is `count` for the 18 people and asset counts. `capital.total` has no `unit`.

| `{group}.{field}` | Title text | category | type |
| --- | --- | --- | --- |
| `population.total0_4` | Population aged 0 to 4 | `children_0_4` | `potentially_affected` |
| `population.total5_9` | Population aged 5 to 9 | `children_5_9` | `potentially_affected` |
| `population.total10_14` | Population aged 10 to 14 | `children_10_14` | `potentially_affected` |
| `population.total15_19` | Population aged 15 to 19 | `children_15_19` | `potentially_affected` |
| `population.total20_24` | Population aged 20 to 24 | `adult_20_24` | `potentially_affected` |
| `population.total25_29` | Population aged 25 to 29 | `adult_25_29` | `potentially_affected` |
| `population.total30_34` | Population aged 30 to 34 | `adult_30_34` | `potentially_affected` |
| `population.total35_39` | Population aged 35 to 39 | `adult_35_39` | `potentially_affected` |
| `population.total40_44` | Population aged 40 to 44 | `adult_40_44` | `potentially_affected` |
| `population.total45_49` | Population aged 45 to 49 | `adult_45_49` | `potentially_affected` |
| `population.total50_54` | Population aged 50 to 54 | `adult_50_54` | `potentially_affected` |
| `population.total55_59` | Population aged 55 to 59 | `adult_55_59` | `potentially_affected` |
| `population.total60_64` | Population aged 60 to 64 | `adult_60_64` | `potentially_affected` |
| `population.total65_Plus` | Population aged 65 and over | `elderly` | `potentially_affected` |
| `population.total` | Total population | `people` | `potentially_affected` |
| `population.households` | Households | `households` | `potentially_affected` |
| `capital.total` | Total capital | `global_currency` | `cost` |
| `capital.school` | School capital | `schools` | `potentially_affected` |
| `capital.hospital` | Hospital capital | `hospitals` | `potentially_affected` |

For the fixture, `capital.total` gives `{"category": "global_currency", "type": "cost", "value": 39725685500.0, "estimate_type": "modelled"}`.

> [!NOTE]
> These values are PDC **exposure** estimates from a model: the people and the assets in the hazard
> area. They are not observed impacts, and for a warning they describe an area where the hazard can
> still occur. Until Monty has a class for exposure and a forecast qualifier
> ([#169](https://github.com/IFRCGo/monty-stac-extension/issues/169),
> [Discussion #110](https://github.com/IFRCGo/monty-stac-extension/discussions/110)), the items say
> this with two existing values: `estimate_type` is `modelled`, and the type of the people and
> asset counts is `potentially_affected`. GDACS uses the same two values for its exposure figures.
> Do not add these values to observed impacts. The `capital.total` value is the replacement value
> of the assets in the area, in USD; its type stays `cost`. The payload does not name the currency,
> so the item has no `unit`.

## Limitations and exclusions

- **Hazards without exposure data.** Such a hazard gives an event item and a hazard item, but no
  impact item ([IFRCGo/pystac-monty#274](https://github.com/IFRCGo/pystac-monty/pull/274)).
- **Historical hazards.** For most old hazards (e.g. 2010 or 2015), the exposure list endpoint
  returns `404 Not Found` ([IFRCGo/montandon-etl#425](https://github.com/IFRCGo/montandon-etl/issues/425)).
  There is no other endpoint for this data. These hazards can have event and hazard items only. PDC
  offered targeted exports of its historical database on request.
- **Unchanged snapshots.** The ETL does not send a snapshot that has the same content as the one
  before it, so such a snapshot gives no impact item.
- **Warnings.** A hazard that is not observed gives no item (see
  [Observed hazards only](#observed-hazards-only-temporary-rule)).
- **Unknown hazard types.** A `type_ID` that is not in the [Hazard Type Mapping](#hazard-type-mapping)
  gives no item. The eight types with no UNDRR-ISC 2025 code give no item too.
- **Fields not mapped.** A `totalByAdmin` row has more fields than the 19 in [Impact Detail](#impact-detail).
  These are not mapped: the other `population` groups (`total0_14`, `total15_64`, `total65_69` to
  `total95_99`, `total100AndOver`, `vulnerable`, `vulnerable0_14`, `vulnerable15_64`,
  `vulnerable65_Plus`), and the needs (`foodNeeds`, `waterNeeds`, `wasteNeeds`, `shelterNeeds`)
  with their units. `total65_Plus` (mapped) and `total65_69` to `total100AndOver` (not mapped)
  overlap.
- **No polygon geometry.** All the items have the hazard point as geometry. The hazard area is only
  in the `Maps` asset.
