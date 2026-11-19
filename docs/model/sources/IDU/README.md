# IDU

The IDU(Internal Displacements Updates) tracks the number of the people who are internally displaced in a region or a country due to `disaster` or `conflict`.

```text
Note: As of now, we only deal with disaster type events.
```

## Data Sources

API: <https://helix-tools-api.idmcdb.org/external-api/>

Current Usage: <https://www.internal-displacement.org/internal-displacement-updates/>

## Collection: `idmc-idu-events`

Collections: `idmc-idu-events` and `idmc-idu-impacts`

Two STAC collections hold the IDU data: one for the events, and one for the displacement figures of each event.

Name: Internal displacement updates

Code: IDU

Source organization: Internal Displacement Monitoring Center (IDMC)

Source organization type: International NGO

Source organization email: <info@idmc.ch>

Source code: IDMC

Source URL: <https://helix-tools-api.idmcdb.org/external-api/>

Source Data license: None stated by the source (checked 2026-07)

Source for: event, impact

previous implementation (R): none

### Which records are ingested

The reference files are in the IDMC folder: [`idu-export.json`](../IDMC/idu-export.json) (a full export) and [`idmc-idu-samples-ESP.json`](../IDMC/idmc-idu-samples-ESP.json) (the records of Spain).

- Only the records with `displacement_type` = `Disaster` are ingested. `Conflict` and `Other` records are ignored.
- A record must have the fields `latitude`, `longitude` and `event_id`. A record without one of them is ignored, with a warning.
- The `role` field is not used. The `Recommended figure` records and the `Triangulation` records are all ingested, and all get `estimate_type: primary`.
- The transformer groups the records by `event_id`. Each group gives one event item, and one impact item for each record of the group.
- If one record of a group is not valid, or the hazard of the event is not in the [hazard type mapping](#hazard-type-mapping), the transformer skips all the group and counts its records as failed. It continues with the next group.

On `idu-export.json` (4623 records, 2586 of them `Disaster`), the transformer gives 1673 event items and 2585 impact items. One record fails: its hazard is `Mixed disasters`.

### Event Item

The event item is built from the **first record** of the event. Only `monty:country_codes` uses all the records.

| STAC field                                                                                                                        | IDU Field                                     | Remarks                                                                                              |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                             | `idmc-idu-event-{event_id}`                   | Prepend text for uniqueness                                                                          |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                             | `idmc-idu-events`                             | Collection name for STAC                                                                             |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                                  | event_name                                    | Name of the event                                                                                    |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                            | standard_popup_text                           | Converted from HTML to Markdown                                                                      |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)                        | event_start_date                              | Start date of the event, UTC                                                                         |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                                 | longitude, latitude                           | A Point. The location of the first record of the event                                               |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                                         | longitude, latitude                           | The same point                                                                                       |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                          | iso3 of all the records of the event          | No duplicates. The country of the first record is first, because `monty:corr_id` uses the first code |
| [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number)                                        | Generated                                     | This is a fixed value (1)                                                                            |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                            | Based on category, subcategory, type, subtype | List of hazard codes, from the [hazard type mapping](#hazard-type-mapping)                           |
| [monty:corr_id](https://github.com/IFRCGo/monty-stac-extension#montycorr_id)                                                      | Generated                                     | Generated following the [event pairing procedure](../../correlation_identifier.md)                   |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                               | event_id                                      | The source identifier of the event, as a string                                                      |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                               | Generated                                     | The keywords of the hazard profile, then the country codes                                           |
| properties.location                                                                                                               | locations_name                                | One string. The name is `location`, without `s`                                                      |
| [properties.start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | event_start_date                              |                                                                                                      |
| [properties.end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | event_end_date                                |                                                                                                      |
| properties.sources                                                                                                                | sources                                       |                                                                                                      |
| properties.roles                                                                                                                  | [`event`, `source`]                           | Include both `event` and `source` roles (order does not matter)                                      |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                           | source_url                                    | Only when the record has a `source_url`. The media type is always `application/pdf`                  |
| `via` link in \[links]                                                                                                            | URL of the source data                        | The URL that the data came from, not the `source_url` of the record                                  |
| `related` links in \[links]                                                                                                       | each impact item of the event                 | `roles: ["impact"]`                                                                                  |
| [processing:version](https://github.com/stac-extensions/processing)                                                               | Generated                                     | Semantic version of the transformer that generated the item, via the `processing:` extension         |
| [processing:software](https://github.com/stac-extensions/processing)                                                              | Generated                                     | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension       |

The transformer does not write `monty:event_codes`. The IDU field `event_codes` is not mapped.

### Hazard Type Mapping

The IDMC hazard classification has four levels. The **UNDRR-ISC 2025** code is the **reference classification** for the Monty extension. IDU and [GIDD](../IDMC/README.md) use the same mapping:

| IDMC category / sub category / type / sub type                                       | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Description                 |
| ----------------------------------------------------------------------------------- | ----- | --------------- | ------------------------------ | --------------------------- |
| ('geophysical', 'geophysical', 'earthquake', 'earthquake')                          | EQ    | nat-geo-ear-gro | **GH0101**                     | Earthquake                  |
| ('geophysical', 'geophysical', 'earthquake', 'tsunami')                             | TS    | nat-geo-ear-tsu | **MH0705**                     | Tsunami                     |
| ('geophysical', 'geophysical', 'mass movement', 'dry mass movement')                | LS    | nat-geo-mmd-lan | **GH0300**                     | Gravitational Mass Movement |
| ('geophysical', 'geophysical', 'mass movement', 'sinkhole')                         | OT    | nat-geo-mmd-sub | **GH0308**                     | Sinkhole                    |
| ('geophysical', 'geophysical', 'volcanic activity', 'volcanic activity')            | VO    | nat-geo-vol-vol | **GH0201**                     | Lava Flows                  |
| ('weather related', 'climatological', 'desertification', 'desertification')         | OT    | nat-geo-env-des | **EN0206**                     | Desertification             |
| ('weather related', 'climatological', 'drought', 'drought')                         | DR    | nat-cli-dro-dro | **MH0401**                     | Drought                     |
| ('weather related', 'climatological', 'erosion', 'erosion')                         | OT    | nat-geo-env-soi | **GH0403**                     | Soil Erosion                |
| ('weather related', 'climatological', 'salinisation', 'salinization')               | OT    | nat-geo-env-slr | **EN0303**                     | Salinity & Sodicity         |
| ('weather related', 'climatological', 'sea level rise', 'sea level rise')           | OT    | nat-geo-env-slr | **EN0402**                     | Sea Level Rise              |
| ('weather related', 'climatological', 'wildfire', 'wildfire')                       | WF    | nat-cli-wil-wil | **EN0205**                     | Wildfires                   |
| ('weather related', 'hydrological', 'flood', 'dam release flood')                   | FL    | tec-mis-col-col | **TL0205**                     | Dam Failure                 |
| ('weather related', 'hydrological', 'flood', 'flood')                               | FL    | nat-hyd-flo-flo | **MH0600**                     | Flooding (chapeau)          |
| ('weather related', 'hydrological', 'mass movement', 'avalanche')                   | AV    | nat-hyd-mmw-ava | **MH0801**                     | Avalanche                   |
| ('weather related', 'hydrological', 'mass movement', 'landslide/wet mass movement') | LS    | nat-hyd-mmw-lan | **GH0304**                     | Slides                      |
| ('weather related', 'hydrological', 'wave action', 'rogue wave')                    | OT    | nat-hyd-wav-rog | **MH0701**                     | Rogue Wave                  |
| ('weather related', 'meteorological', 'extreme temperature', 'cold wave')           | CW    | nat-met-ext-col | **MH0502**                     | Cold Wave                   |
| ('weather related', 'meteorological', 'extreme temperature', 'heat wave')           | HT    | nat-met-ext-hea | **MH0501**                     | Heatwave                    |
| ('weather related', 'meteorological', 'storm', 'hailstorm')                         | ST    | nat-met-sto-hai | **MH0404**                     | Hail                        |
| ('weather related', 'meteorological', 'storm', 'sand/dust storm')                   | VW    | nat-met-sto-san | **MH0201**                     | Dust Storm or Sandstorm     |
| ('weather related', 'meteorological', 'storm', 'storm surge')                       | SS    | nat-met-sto-sur | **MH0703**                     | Storm Surge                 |
| ('weather related', 'meteorological', 'storm', 'storm')                             | VW    | nat-met-sto-sto | **MH0301**                     | Storm (generic)             |
| ('weather related', 'meteorological', 'storm', 'tornado')                           | TO    | nat-met-sto-tor | **MH0305**                     | Tornado                     |
| ('weather related', 'meteorological', 'storm', 'typhoon/hurricane/cyclone')         | TC    | nat-met-sto-tro | **MH0309**                     | Tropical Cyclone            |
| ('weather related', 'meteorological', 'storm', 'winter storm/blizzard')             | OT    | nat-met-sto-bli | **MH0403**                     | Blizzard                    |

The comparison is not case-sensitive. The transformer writes the three codes in the order
UNDRR-ISC 2025, GLIDE, EM-DAT, for example `["MH0600", "FL", "nat-hyd-flo-flo"]`.

A hazard that is not in this table gives no item: the transformer skips all the records of
that event and counts them as failed. This includes `Mixed disasters`. The transformer has a
row for it (`mix-mix-mix-mix`), but that value has no UNDRR-ISC 2025 code, so the event fails.

### Impact Item

Each `Disaster` record gives one impact item. The transformer starts from a copy of the event item, and then sets the fields of the record. So an impact item also has the `title`, `monty:corr_id`, `monty:hazard_codes`, `monty:episode_number` and `monty:src_event_id` of its event.

| STAC field                                                                                                                        | IDU Field                                       | Remarks                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                             | `idmc-idu-impact-{event_id}-{id}-{impact_type}` | See [Impact item id](#impact-item-id)                                                            |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                             | `idmc-idu-impacts`                              | Collection name for STAC                                                                         |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                                  | event_name                                      | Name of the event. All the impact items of an event have the same title                          |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                            | standard_popup_text                             | Of the record. Converted from HTML to Markdown                                                   |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)                        | displacement_start_date                         | UTC                                                                                              |
| [properties.start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | displacement_start_date                         |                                                                                                  |
| [properties.end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | displacement_end_date                           |                                                                                                  |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                                 | longitude, latitude                             | A Point. The location of the record                                                              |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                                         | longitude, latitude                             | The same point                                                                                   |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                          | iso3                                            | One code: the country of the record                                                              |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                               | Generated                                       | The keywords of the hazard profile, then the country code of the record                          |
| properties.location                                                                                                               | locations_name                                  | Of the record                                                                                    |
| properties.sources                                                                                                                | sources                                         | Of the record                                                                                    |
| properties.roles                                                                                                                  | [`impact`, `source`]                            | Include both `impact` and `source` roles (order does not matter)                                 |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                           | source_url                                      | Of the record. No asset when the record has no `source_url`                                      |
| `via` link in \[links]                                                                                                            | URL of the source data                          | Same as the event item                                                                           |
| `related` link in \[links]                                                                                                        | the event item                                  | `roles: ["event"]`                                                                               |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail)                                          | impact_detail                                   | As shown in [Impact Detail](#impact-detail) below                                                |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                               | event_id                                        | The identifier of the event, not of the record                                                   |
| [processing:version](https://github.com/stac-extensions/processing)                                                               | Generated                                       | Semantic version of the transformer that generated the item, via the `processing:` extension     |
| [processing:software](https://github.com/stac-extensions/processing)                                                              | Generated                                       | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension   |

#### Impact item id

The id is `idmc-idu-impact-{event_id}-{id}-{impact_type}`:

- `{event_id}` is the identifier of the event, and `{id}` is the identifier of the record.
- `{impact_type}` comes from `standard_popup_text`. The transformer takes the **first** text between parentheses. If that text is a label of the [Impact Detail](#impact-detail) table, it is the `impact_type`. If not, or if there are no parentheses, the `impact_type` is `displaced`.

Example: the text `200 displacements (evacuated), 11 November - 11 November` gives `idmc-idu-impact-28177-169470-evacuated`.

> [!IMPORTANT]
> The id has a hyphen between `{event_id}` and `{id}` since [IFRCGo/pystac-monty#268](https://github.com/IFRCGo/pystac-monty/pull/268). Before that change the transformer wrote the two numbers with no separator (`idmc-idu-impact-28177169470-evacuated`). This doc and its examples gave a third form, `idmc-idu-impact-{id}-displaced`, which no transformer release wrote.

#### Impact Detail

The `impact_type` gives the `category` and the `type` of `monty:impact_detail`. The comparison is case-sensitive:

| Label                             | `category` | `type`               |
| --------------------------------- | ---------- | -------------------- |
| `evacuated`                       | `people`   | `evacuated`          |
| `displaced`                       | `people`   | `displaced_internal` |
| `relocated`                       | `people`   | `relocated`          |
| `sheltered`                       | `people`   | `shelter_emergency`  |
| `homeless`                        | `people`   | `homeless`           |
| `affected`                        | `people`   | `affected_total`     |
| `IDPs`                            | `people`   | `displaced_internal` |
| `Internal Displacements`          | `people`   | `displaced_internal` |
| `Deaths`                          | `people`   | `death`              |
| `People displaced across borders` | `people`   | `displaced_external` |

An `impact_type` that is not in the table gives `people` / `displaced_internal`.

| Key           | Value                        |
| ------------- | ---------------------------- |
| category      | from the table above         |
| type          | from the table above         |
| value         | `figure` field of the record |
| unit          | `count`                      |
| estimate_type | `primary`, for all records   |

### Examples

The examples are the output of the transformer for `idmc-idu-samples-ESP.json`. Only the links are adapted to the layout of `examples/`.

- [`idmc-idu-event-28064`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-events/idmc-idu-event-28064.json) and [`idmc-idu-impact-28064-168623-displaced`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-impacts/idmc-idu-impact-28064-168623-displaced.json): a flood in Andalusia, 4 210 people displaced
- [`idmc-idu-event-28177`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-events/idmc-idu-event-28177.json) and [`idmc-idu-impact-28177-169470-evacuated`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-idu-impacts/idmc-idu-impact-28177-169470-evacuated.json): a wildfire in the Canary Islands, 200 people evacuated

In a deployment, the `related` hrefs have the form `{eoapi_url}/collections/{collection}/items/{item_id}`.
