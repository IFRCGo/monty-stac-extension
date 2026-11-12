# IDMC — Internal Displacement Updates (IDU)

The Internal Displacement Updates (IDU) give near real-time figures on persons who are internally displaced by a `Disaster` or a `Conflict`. The Internal Displacement Monitoring Centre (IDMC) publishes them. IDMC validates the figures later in the [GIDD](../IDMC/README.md).

This page describes the IDU transformer (`pystac_monty/sources/idu.py`) at [`2e31c9c4`](https://github.com/IFRCGo/pystac-monty/commit/2e31c9c4e43243c6adcf8b5542f92829ba79c4d5). Monty maps `Disaster` records only.

## Collections

| Collection         | Content                                 |
| ------------------ | --------------------------------------- |
| `idmc-idu-events`  | One event item for each IDU `event_id`  |
| `idmc-idu-impacts` | One impact item for each IDU record     |

- Source organisation: Internal Displacement Monitoring Centre (IDMC)
- Source organisation type: International NGO
- Source organisation email: <info@idmc.ch>
- Source code: IDMC
- Source URL: <https://helix-tools-api.idmcdb.org/external-api/>
- Current usage: <https://www.internal-displacement.org/internal-displacement-updates/>
- Source data license: None stated by the source (checked 2026-07)
- Source for: event, impact

## Data

The ETL reads `https://helix-tools-api.idmcdb.org/external-api/idus/last-180-days/`. The response is a JSON array. Each element is one displacement record. The fields that the transformer uses:

| IDU field                                         | Meaning                                                          |
| ------------------------------------------------- | ---------------------------------------------------------------- |
| `id`                                              | Identifier of the displacement record                            |
| `event_id`, `event_name`                          | The event that the record belongs to                             |
| `event_start_date`, `event_end_date`              | Dates of the event                                               |
| `displacement_type`                               | `Disaster`, `Conflict` or `Other`                                |
| `displacement_start_date`, `displacement_end_date` | Dates of the displacement                                       |
| `figure`                                          | Number of displaced persons                                      |
| `standard_popup_text`                             | HTML summary. The impact type comes from it                      |
| `role`                                            | `Recommended figure` or `Triangulation`. Not used                |
| `iso3`, `latitude`, `longitude`, `locations_name` | Where                                                            |
| `category`, `subcategory`, `type`, `subtype`      | Hazard classification                                            |
| `sources`, `source_url`                           | Who reported the figure, and a link to the report                |

## Object model

```text
IDU event_id ──► 1 event item   idmc-idu-event-{event_id}
     │
     └─ each record ──► 1 impact item   idmc-idu-impact-{event_id}-{id}-{impact_type}
```

The transformer groups the records by `event_id`. Each group gives one event item and one impact item for each record. IDU has no hazard items.

**The event item is built from the first record of the group.** Each impact item starts as a copy of the event item, and then the transformer sets the record's own dates and figure. See [Known limitations](#known-limitations), item 1.

## Data access

1. The transformer keeps only the records with `displacement_type` = `Disaster`. It skips `Conflict` and `Other` records, and it logs a warning for an unknown type. (This filter applies to file input, which the ETL uses. Memory input is not filtered.)
2. It skips a record that has no `latitude`, `longitude` or `event_id`.
3. If one record of a group fails validation, the transformer drops the **whole group**: the event item and all its impact items. This also occurs when the hazard fields of the first record are not in the [hazard type mapping](#hazard-type-mapping), or map to `Mixed disasters`, which has no UNDRR-ISC 2025 code.

## Event items

| STAC field                                                                                                              | IDU field                                     | Notes                                                              |
| ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                   | `idmc-idu-event-{event_id}`                   |                                                                    |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                   | `idmc-idu-events`                             |                                                                    |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                       | `longitude`, `latitude` of the first record   | A `Point`                                                          |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                               | `longitude`, `latitude` of the first record   | A zero-size box                                                    |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                        | `event_name`                                  |                                                                    |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                  | `standard_popup_text` of the first record     | Converted from HTML to Markdown                                    |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)              | `event_start_date`                            | Midnight UTC                                                       |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)  | `event_start_date`                            | Midnight UTC                                                       |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)    | `event_end_date`                              | Midnight UTC                                                       |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                     | Generated                                     | Hazard profile keywords and the country code                       |
| `location`                                                                                                              | `locations_name` of the first record          |                                                                    |
| `sources`                                                                                                               | `sources` of the first record                 |                                                                    |
| `roles`                                                                                                                 | `["source", "event"]`                         |                                                                    |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                | `[iso3]` of the first record                  | One country only                                                   |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                  | `category`, `subcategory`, `type`, `subtype`  | See [Hazard type mapping](#hazard-type-mapping)                    |
| [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number)                              | —                                             | Always `1`                                                         |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                     | `event_id`                                    |                                                                    |
| [monty:corr_id](https://github.com/IFRCGo/monty-stac-extension#montycorr_id)                                            | Generated                                     | [Correlation identifier](../../correlation_identifier.md), dated from `event_start_date` |
| [processing:version](https://github.com/stac-extensions/processing)                                                     | Generated                                     | Version of the transformer, via the `processing:` extension        |
| [processing:software](https://github.com/stac-extensions/processing)                                                    | Generated                                     | `{"pystac-monty": "<version>"}`, via the `processing:` extension   |
| `assets.report`                                                                                                         | `source_url` of the first record              | Only when `source_url` is set. Typed `application/pdf`, but it is often a web page |
| `via` link                                                                                                              | the source URL                                | Title `IDU Event Data`                                             |
| `related` links                                                                                                         | Generated                                     | One for each impact item of the event, with `roles: ["impact"]`    |

## Impact items

| STAC field                                                                                                              | IDU field                                     | Notes                                                              |
| ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                   | `idmc-idu-impact-{event_id}-{id}-{impact_type}` | Example: `idmc-idu-impact-28064-168623-displaced`. See [Impact type](#impact-type) |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                   | `idmc-idu-impacts`                            |                                                                    |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)              | `displacement_start_date`                     | Midnight UTC                                                       |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)  | `displacement_start_date`                     | Midnight UTC                                                       |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)    | `displacement_end_date`                       | Midnight UTC                                                       |
| `roles`                                                                                                                 | `["source", "impact"]`                        |                                                                    |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail)                                | See [Impact detail](#impact-detail)           |                                                                    |
| `related` link                                                                                                          | Generated                                     | To the event item, with `roles: ["event"]`                         |
| all other fields                                                                                                        | copied from the event item                    | Geometry, bbox, title, description, location, sources, keywords, `monty:*` codes, `assets.report` and the `via` link. **These are the values of the first record of the event.** See [Known limitations](#known-limitations), item 1 |

### Impact type

The transformer reads the impact type from `standard_popup_text`. It takes the **first** text in parentheses. If that text is one of the keys below, it is the impact type. If not, the impact type is `displaced`.

For example, `Spain: 200 displacements (evacuated), 11 November - 11 November` gives `evacuated`. In the reference file, 22 records give `evacuated` and 4 give `sheltered`. One record says `(destroyed housing)`, which is not a key, so it gives `displaced`.

### Impact detail

| Field           | Value                                       |
| --------------- | ------------------------------------------- |
| `category`      | `people`                                    |
| `type`          | From the impact type. See the next table    |
| `value`         | `figure`                                    |
| `unit`          | `count`                                     |
| `estimate_type` | `primary`, always                           |

| Impact type (text in parentheses)  | `type`                |
| ---------------------------------- | --------------------- |
| `evacuated`                        | `evacuated`           |
| `displaced`                        | `displaced_internal`  |
| `relocated`                        | `relocated`           |
| `sheltered`                        | `shelter_emergency`   |
| `homeless`                         | `homeless`            |
| `affected`                         | `affected_total`      |
| `IDPs`, `Internal Displacements`   | `displaced_internal`  |
| `Deaths`                           | `death`               |
| `People displaced across borders`  | `displaced_external`  |
| any other text, or none            | `displaced_internal` (impact type `displaced`) |

## Hazard type mapping

IDU and [GIDD](../IDMC/README.md#hazard-codes) use the same function, `IDMCUtils.hazard_codes_mapping`. Its input is the four hazard fields in lower case. The transformer then orders the codes with the UNDRR-ISC 2025 code first.

| IDU category / subcategory / type / subtype                                         | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Cluster    | Description                 |
| ----------------------------------------------------------------------------------- | ----- | --------------- | ------------------------------ | ---------- | --------------------------- |
| ('geophysical', 'geophysical', 'earthquake', 'earthquake')                          | EQ    | nat-geo-ear-gro | **GH0101**                     | GEO-SEIS   | Earthquake                  |
| ('geophysical', 'geophysical', 'earthquake', 'tsunami')                             | TS    | nat-geo-ear-tsu | **MH0705**                     | MH-MARINE  | Tsunami                     |
| ('geophysical', 'geophysical', 'mass movement', 'dry mass movement')                | LS    | nat-geo-mmd-lan | **GH0300**                     | GEO-GFAIL  | Gravitational Mass Movement |
| ('geophysical', 'geophysical', 'mass movement', 'sinkhole')                         | OT    | nat-geo-mmd-sub | **GH0308**                     | GEO-GFAIL  | Sinkhole                    |
| ('geophysical', 'geophysical', 'volcanic activity', 'volcanic activity')            | VO    | nat-geo-vol-vol | **GH0201**                     | GEO-VOLC   | Lava Flows                  |
| ('mixed disasters', 'mixed disasters', 'mixed disasters', 'mixed disasters')        | —     | —               | — <sup>1</sup>                 | —          | —                           |
| ('weather related', 'climatological', 'desertification', 'desertification')         | OT    | nat-geo-env-des | **EN0206**                     | ENV-FOREST | Desertification             |
| ('weather related', 'climatological', 'drought', 'drought')                         | DR    | nat-cli-dro-dro | **MH0401**                     | MH-PRECIP  | Drought                     |
| ('weather related', 'climatological', 'erosion', 'erosion')                         | OT    | nat-geo-env-soi | **GH0403**                     | GEO-OTHER  | Soil Erosion                |
| ('weather related', 'climatological', 'salinisation', 'salinization')               | OT    | nat-geo-env-slr | **EN0303**                     | ENV-LAND   | Salinity & Sodicity         |
| ('weather related', 'climatological', 'sea level rise', 'sea level rise')           | OT    | nat-geo-env-slr | **EN0303** <sup>2</sup>        | ENV-LAND   | Salinity & Sodicity         |
| ('weather related', 'climatological', 'wildfire', 'wildfire')                       | WF    | nat-cli-wil-wil | **EN0205**                     | ENV-FOREST | Wildfires                   |
| ('weather related', 'hydrological', 'flood', 'dam release flood')                   | FL    | tec-mis-col-col | **TL0205**                     | TECH-STRFAIL | Dam Failure               |
| ('weather related', 'hydrological', 'flood', 'flood')                               | FL    | nat-hyd-flo-flo | **MH0600**                     | MH-WATER   | Flooding (chapeau)          |
| ('weather related', 'hydrological', 'mass movement', 'avalanche')                   | AV    | nat-geo-mmd-ava <sup>3</sup> | **MH0801**        | MH-TERR    | Avalanche                   |
| ('weather related', 'hydrological', 'mass movement', 'landslide/wet mass movement') | LS    | nat-hyd-mmw-lan | **GH0304**                     | GEO-GFAIL  | Slides                      |
| ('weather related', 'hydrological', 'wave action', 'rogue wave')                    | OT    | nat-hyd-wav-rog | **MH0701**                     | MH-MARINE  | Rogue Wave                  |
| ('weather related', 'meteorological', 'extreme temperature', 'cold wave')           | CW    | nat-met-ext-col | **MH0502**                     | MH-TEMP    | Cold Wave                   |
| ('weather related', 'meteorological', 'extreme temperature', 'heat wave')           | HT    | nat-met-ext-hea | **MH0501**                     | MH-TEMP    | Heatwave                    |
| ('weather related', 'meteorological', 'storm', 'hailstorm')                         | ST    | nat-met-sto-hai | **MH0404**                     | MH-PRECIP  | Hail                        |
| ('weather related', 'meteorological', 'storm', 'sand/dust storm')                   | VW    | nat-met-sto-san | **MH0201**                     | MH-PART    | Dust Storm or Sandstorm     |
| ('weather related', 'meteorological', 'storm', 'storm surge')                       | SS    | nat-met-sto-sur | **MH0703**                     | MH-MARINE  | Storm Surge                 |
| ('weather related', 'meteorological', 'storm', 'storm')                             | VW    | nat-met-sto-sto | **MH0301**                     | MH-WIND    | Wind                        |
| ('weather related', 'meteorological', 'storm', 'tornado')                           | TO    | nat-met-sto-tor | **MH0305**                     | MH-WIND    | Tornado                     |
| ('weather related', 'meteorological', 'storm', 'typhoon/hurricane/cyclone')         | TC    | nat-met-sto-tro | **MH0309** <sup>4</sup>        | MH-WIND    | Tropical Cyclone            |
| ('weather related', 'meteorological', 'storm', 'winter storm/blizzard')             | OT    | nat-met-sto-bli | **MH0403**                     | MH-PRECIP  | Blizzard                    |

1. The function returns `mix-mix-mix-mix`, which is not a code of any classification. The transformer cannot derive a UNDRR-ISC 2025 code from it, so it drops the event. See [Data access](#data-access), item 3.
2. `nat-geo-env-slr` maps to `EN0303` in the [EM-DAT crosswalk](../../taxonomy.md) that the transformer follows. `EN0402` (Sea Level Rise) is a closer match. This is an open question for the taxonomy, not for IDU.
3. The IDU type is hydrological (wet) mass movement, which is `nat-hyd-mmw-ava` in EM-DAT. The transformer uses `nat-geo-mmd-ava` (dry). Both map to `MH0801`.
4. The TC code is part of the repository-wide `MH0306`/`MH0309` question in [#94](https://github.com/IFRCGo/monty-stac-extension/issues/94).

## Known limitations

1. **Impact items copy the event item, and the event item comes from the first record of the event.** So an impact item has the geometry, the description, the location and the report link of the first record, not its own. In the reference file, 5 of the 28 impact items have the geometry of another record. Only the dates and `monty:impact_detail` belong to the record.
2. **The impact type depends on free text.** Only the first text in parentheses counts. A summary with an earlier parenthesis, for example a place name, gives `displaced`.
3. **`estimate_type` is always `primary`.** The transformer does not read the IDU `role` field (`Recommended figure` or `Triangulation`). In the reference file, 5 of the 28 records are `Triangulation`.

## Examples

Made with the IDU transformer at [`2e31c9c4`](https://github.com/IFRCGo/pystac-monty/commit/2e31c9c4e43243c6adcf8b5542f92829ba79c4d5), from the reference file below:

- [`examples/idmc-idu-events/idmc-idu-event-28064.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-events/idmc-idu-event-28064.json) and its impact [`idmc-idu-impact-28064-168623-displaced.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-impacts/idmc-idu-impact-28064-168623-displaced.json): a flood in Málaga, Spain, November 2024
- [`examples/idmc-idu-events/idmc-idu-event-28177.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-events/idmc-idu-event-28177.json) and its impact [`idmc-idu-impact-28177-169470-evacuated.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-impacts/idmc-idu-impact-28177-169470-evacuated.json): a wildfire in La Palma, Spain, November 2024

## Reference files

- [`../IDMC/idmc-idu-samples-ESP.json`](../IDMC/idmc-idu-samples-ESP.json): 28 IDU records for Spain. The transformer makes 22 event items and 28 impact items from it.
- [`../IDMC/idu-export.json`](../IDMC/idu-export.json): a larger IDU export (4,623 records)
