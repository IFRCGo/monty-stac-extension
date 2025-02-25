# Pacific Disaster Center (PDC)

The Pacific Disaster Center (PDC) tracks a wide range of natural and human made hazards viz. **Tropical Cyclone**, **Earthquake**, **Flood**, **Landslides**, **Wildfire**, **Drought**, **Volcanic Eruptions** etc to support disaster preparedness, response, and risk reduction efforts.

## Collection: `pdc-events`

A STAC collection hold all the PDC events.

- Name: Pacific Disaster Center
- Code: PDC
- Source organization:
- Source code:
- Source type:
- Source organization email: <info@pdc.org>
- Source URL: <https://www.pdc.org/>
- Source Data License: UNKNOWN
- Source for: event, hazard, impact

## Endpoints for Extraction
To get the relevant PDC data, we use the following endpoints:

1. Get a list of Active Hazards: <https://sentry.pdc.org/hp_srv/services/hazards/t/json/get_active_hazards>
2. Get exposure list for each Hazard: <https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure>
3. Get exposure details for each exposure: <https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/{timestamp}>

## Data Schema
The `PDCDataSource` class when instantiated takes two parameters viz. `source_url: str` and `data: Any`.

The `data` parameter primarily takes a json object of the following format.
```json
{
    "hazards_file_path": str,
    "exposure_timestamp": str,
    "uuid": str,
    "exposure_detail_file_path": str,
    "geojson_file_path": Optional[str]
}
```

## Event Item

A PDC event will always produce an Event STAC Item. Here is a table with the fields that are mapped from the PDC event to the STAC event:

| STAC field | PDC Field | Description |
| -----------|-----------|-------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | id | Unique Identifier |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | latitude, longitude | Geometric point using latitude and longitude |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `pdc-events` | |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | longitude, latitude, longitude, latitude |  |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | create_Date |     |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | hazard_Name |   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | description |   |
| roles | ["source", "event"] | Default roles for event item |   |
| [monty:country_codes](../../../README.md#montycountry_codes) | `country` field in the list `totalByCountry` | List of country iso3 are pulled from exposure endpoint by iterating `totalByCountry` field |
| [monty:hazard_codes](../../../README.md#montyhazard_codes) | type_ID | The hazard codes are generated using the mapping |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) | snc_url | Asset with the link to the PDC report |

## Hazard Item

A PDC event and the timestamp from exposure endpoint will **ALWAYS** produce one [**hazard STAC item**](../../../README.md#hazard). Here is a table with the STAC fields that are managed from the PDC event to the STAC hazard.

| STAC field | PDC Field | Description |
| -----------|-----------|-------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | id | Unique Identifier |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | latitude, longitude | Geometric point using latitude and longitude |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `pdc-hazards` | |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | longitude, latitude, longitude, latitude |  |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | create_Date |     |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | hazard_Name |   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | description |   |
| roles | ["source", "hazard"] | Default roles for hazard item |    |
| [monty:country_codes](../../../README.md#montycountry_codes) | `country` field in the list `totalByCountry` | List of country iso3 are pulled from exposure endpoint by iterating `totalByCountry` field |
| [monty:hazard_codes](../../../README.md#montyhazard_codes) | type_ID | The hazard codes are generated using the mapping |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) | snc_url | Asset with the link to the PDC report |
| [monty:hazard_detail](../../../README.md#montyhazard_detail) |      |

## Impact item

The PDC events will produce multiple [**Impact STAC Items**](../../../README.md#impact) when impact related data is available through exposure endpoint.

The following table shows the mapping of PDC impact fields to STAC items.

| STAC field | PDC Field | Description |
| -----------|-----------|-------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | id | Unique Identifier |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | latitude, longitude | Geometric point using latitude and longitude |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `pdc-impacts` | |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | longitude, latitude, longitude, latitude |  |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | create_Date |     |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | hazard_Name |   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | description |   |
| roles | ["source", "impact"] | Default roles for impact item |    |
| [monty:country_codes](../../../README.md#montycountry_codes) | `country` field in the list `totalByCountry` | List of country iso3 are pulled from exposure endpoint by iterating `totalByCountry` field |
| [monty:hazard_codes](../../../README.md#montyhazard_codes) | type_ID | The hazard codes are generated using the mapping |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) | snc_url | Asset with the link to the PDC report |
| [monty:impact_detail] | Impact items using different fields | Several impact items are created based on several fields available from the exposure endpoint |

### Impact Details
The following fields are used to create several **Impact Details** items.

1. Population -> Age group 0 - 4

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.CHILDREN_0_4|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total0_4]` |Get the value using the key `[population][total0_4]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

2. Population -> Age group 5 - 9

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.CHILDREN_5_9|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total5_9]` |Get the value using the key `[population][total5_9]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

3. Population -> Age group 10 - 14

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.CHILDREN_10_14|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total10_14]` |Get the value using the key `[population][total10_14]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

4. Population -> Age group 15 - 19

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.CHILDREN_15_19|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total15_19]` |Get the value using the key `[population][total15_19]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

5. Population -> Age group 20 - 24

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_20_24|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total20_24]` |Get the value using the key `[population][total20_24]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

6. Population -> Age group 25 - 29

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_25_29|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total25_29]` |Get the value using the key `[population][total25_29]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

7. Population -> Age group 30 - 34

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_30_34|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total30_34]` |Get the value using the key `[population][total30_34]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

8. Population -> Age group 35 - 39

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_35_39|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total35_39]` |Get the value using the key `[population][total35_39]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

9. Population -> Age group 40 - 44

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_40_44|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total40_44]` |Get the value using the key `[population][total40_44]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

10. Population -> Age group 45 - 49

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_45_49|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total45_49]` |Get the value using the key `[population][total45_49]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

11. Population -> Age group 50 - 54

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_50_54|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total50_54]` |Get the value using the key `[population][total50_54]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

12. Population -> Age group 55 - 59

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_55_59|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total55_59]` |Get the value using the key `[population][total55_59]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

13. Population -> Age group 60 - 64

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ADULT_60_64|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total60_64]` |Get the value using the key `[population][total60_64]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

14. Population -> Age group 65 and plus

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ELDERLY|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total65_plus]`|Get the value using the key `[population][total65_plus]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

15. Population -> Total population

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.ALL_PEOPLE|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][total]` |Get the value using the key `[population][total]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

16. Population -> Households

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.HOUSEHOLDS|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[population][houselholds]`|Get the value using the key `[population][households]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

17. Capital -> Total

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.GLOBAL_CURRENCY|  |
| type |MontyImpactType.LOSS_COUNT| |
|value |value from `[capital][total]` |Get the value using the key `[capital][total]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

18. Capital -> School

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.SCHOOLS|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[capital][school]` |Get the value using the key `[capital][school]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |

19. Capital -> Hospital

|STAC Field | PDC Field | Description |
|-----------|-----------|-------------|
| category |MontyImpactExposureCategory.HOSPITALS|  |
| type |MontyImpactType.TOTAL_AFFECTED| |
|value |value from `[capital][hospital]` |Get the value using the key `[capital][hospital]`|
| unit | None |     |
|estimate_type|MontyEstimateType.PRIMARY| |
