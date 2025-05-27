# Global Flood Database (GFD)

Global Flood Database(GFD) combines over several years of flood data to create the first comprehensive satellite based resource for global flood risk management and mitigation.

## Collection: `gfd-events`

A STAC collection hold all the GFD events.

- Name: Global Flood Database (GFD)
- Code: GFD
- Source organization:
- Source code:
- Source Type:
- Source organization email: <support@floodbase.com>
- Source URL: <https://global-flood-database.cloudtostreet.ai/>
- Source Data License: UNKNOWN
- Source for: event, hazard, impact

- previous implementation (R): <https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGFD.R>

## Data

The GFD data which is related to Flood is accessible using the Google Earth Engine library. The Image Collection which contains Flood related data is **GLOBAL_FLOOD_DB/MODIS_EVENTS/V1**.

## Event Item

A GFD event will always produce an Event STAC Item.
Here is a table with the fields that are mapped from the GFD event to the STAC event:

| STAC field | GFD Field | Description |
| -----------|-----------|-------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | id | Unique Identifier |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | system:footprint | The data from GFD field `type` gives **LinearRing** which is not supported, so, the geometry is constructed by converting the data to type **Polygon**. |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)  | `gfd-events` |          |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | `coordinates` from system:footprint | Max and min latitude and longitude are calculated from the `coordinates` from system:footprint |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | dfo_main_cause | |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | dfo_main_cause |        |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | system:time_start | |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | cc      | Split the `cc` field to get the list of iso3 |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | List of hazard codes converted following the mapping | Default value is FL as GFD is a flood related source. |

## Hazard Item

A GFD event and episode will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard). Here is a table with the STAC fields that are mapped from the GFD event to the STAC hazad.

| STAC field | GFD Field | Description |
| -----------|-----------|-------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)          | id        | Unique Identifier  |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)    | system:footprint | The data from GFD field `type` gives **LinearRing** which is not supported, so, the geometry is constructed by converting the data to type **Polygon**. |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)  | `gfd-hazards` |          |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)        | `coordinates` from system:footprint | Max and min latitude and longitude are calculated from the `coordinates` from system:footprint |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | dfo_main_cause |    |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | dfo_main_cause |        |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | system:time_start |     |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | cc      | Split the `cc` field to get the list of iso3 |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | List of hazard codes converted following the mapping | Default value is FL as GFD is a flood related source. |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) | Hazard detail based on dfo_severity | Detailed description of the hazard |

### Hazard Detail
The [hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) is constructed using the following fields.

| STAC field | GFD Field | Description |
|------------|-----------|-------------|
| severity_value | dfo_severity | Alert Score |
| severity_unit | GFD Flood Severity Score | Alert level |

## Impact Item

According to the event type and the fields available in the GFD event, one or more [**Impact STAC Items**](https://github.com/IFRCGo/monty-stac-extension#impact) can be created.
The following sections describe the mapping of specific GFD event information to the STAC impact item.

| STAC field | GFD Field | Description |
| -----------|-----------|-------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)          | id        | Unique Identifier  |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | system:footprint | The data from GFD field `type` gives **LinearRing** which is not supported, so, the geometry is constructed by converting the data to type **Polygon**. |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `gfd-impacts` |          |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | `coordinates` from system:footprint | Max and min latitude and longitude are calculated from the `coordinates` from system:footprint |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | dfo_main_cause | |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | dfo_main_cause | |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | system:time_start | |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | `cc`      | Split the `cc` field to get the list of iso3 |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | List of hazard codes converted following the mapping | Default value is FL as GFD is a flood related source. |
| monty:impact_detail | Impact items using *dfo_dead*, *dfo_displaced fields* | Several impact items are created based on *dfo_dead*, *dfo_displaced* fields |

### Impact Details
The following fields are used to create several **Impact Detail** items.
1. DEATHS

|STAC Field | GFD Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ALL_PEOPLE|  |
| type |MontyImpactType.DEATH| |
|value |value from *dfo_dead* |Get the value using the key *dfo_dead*|
| unit | count |     |
|estimate_type|MontyEstimateType.PRIMARY| |

2. DISPLACED

|STAC Field | GFD Field | Description |
|-----------|-----------|-------------|
| category   | MontyImpactExposureCategory.ALL_PEOPLE |  |
|type|MontyImpactType.TOTAL_DISPLACED_PERSONS| |
|value|value from *dfo_displaced* |Get the value using the key *dfo_displaced*|
| unit | count |     |
|estimate_type|MontyEstimateType.PRIMARY| |
