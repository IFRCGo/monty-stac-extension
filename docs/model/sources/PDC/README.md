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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | `country` field in the list `totalByCountry` | List of country iso3 are pulled from exposure endpoint by iterating `totalByCountry` field |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | type_ID | The hazard codes are generated using the [Hazard Type Mapping](#hazard-type-mapping) |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) | snc_url | Asset with the link to the PDC report |

#### Hazard Type Mapping

PDC (Pacific Disaster Center) tracks a wide range of natural and geopolitical hazards. The **2025 UNDRR-ISC** code is the **reference classification** for the Monty extension:

**Natural Hazards:**

| PDC Type            | GLIDE | EM-DAT              | **UNDRR-ISC 2025** (Reference) | Cluster      | Description                      |
| ------------------- | ----- | ------------------- | ------------------------------ | ------------ | -------------------------------- |
| Avalanche           | AV    | nat-hyd-mmw-ava     | **MH0801**                     | MH-TERR      | Avalanche                        |
| Biomedical          | EP    | nat-bio-epi-dis     | **BI0101**                     | BIO-INFECT   | Infectious Diseases              |
| Drought             | DR    | nat-cli-dro-dro     | **MH0401**                     | MH-PRECIP    | Drought                          |
| Earthquake          | EQ    | nat-geo-ear-gro     | **GH0101**                     | GEO-SEIS     | Earthquake                       |
| Extreme Temperature | HT/CW | nat-met-ext-hea     | **MH0501**                     | MH-TEMP      | Heatwave (or MH0502 for Cold)    |
| Flood               | FL    | nat-hyd-flo-flo     | **MH0600**                     | MH-WATER     | Flooding (chapeau)               |
| High Surf           | OT    | nat-hyd-wav-wav     | **MH0702**                     | MH-MARINE    | Wave Action                      |
| Landslide           | LS    | nat-geo-mmd-lan     | **GH0300**                     | GEO-GFAIL    | Gravitational Mass Movement      |
| Marine              | OT    | nat-hyd-wav-wav     | **MH0700**                     | MH-MARINE    | Marine-related (chapeau)         |
| Severe Weather      | ST    | nat-met-sto-sto     | **MH0103**                     | MH-CONV      | Thunderstorm                     |
| Storm               | ST    | nat-met-sto-sto     | **MH0103**                     | MH-CONV      | Thunderstorm                     |
| Tornado             | TO    | nat-met-sto-tor     | **MH0305**                     | MH-WIND      | Tornado                          |
| Tropical Cyclone    | TC    | nat-met-sto-tro     | **MH0306**                     | MH-WIND      | Tropical Cyclone                 |
| Tsunami             | TS    | nat-geo-ear-tsu     | **MH0705**                     | MH-MARINE    | Tsunami                          |
| Volcano             | VO    | nat-geo-vol-vol     | **GH0201**                     | GEO-VOLC     | Lava Flows                       |
| Wildfire            | WF    | nat-cli-wil-for     | **EN0205**                     | ENV-FOREST   | Wildfires                        |
| Winter Storm        | OT    | nat-met-sto-bli     | **MH0403**                     | MH-PRECIP    | Blizzard                         |

**Geopolitical & Technological Hazards:**

| PDC Type          | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Cluster      | Description                      |
| ----------------- | ----- | --------------- | ------------------------------ | ------------ | -------------------------------- |
| Accident          | AC    | tec-mis-col-col | **TL0200**                     | TECH-STRFAIL | Structural Failure (chapeau)     |
| Active Shooter    | OT    | soc-soc-vio-vio | **SO0201**                     | SOC-CONF     | Armed Conflict                   |
| Civil Unrest      | OT    | soc-soc-vio-vio | **SO0202**                     | SOC-CONF     | Civil Unrest                     |
| Combat            | OT    | soc-soc-vio-vio | **SO0201**                     | SOC-CONF     | Armed Conflict                   |
| Cyber             | OT    | N/A             | **TL0601**                     | TECH-CYBER   | Cyber Incidents                  |
| Man Made          | OT    | tec-tec-tec-tec | **TL0000**                     | TECH         | Technological (general)          |
| Occurrence        | OT    | N/A             | **OT0000**                     | OTHER        | Other/Unspecified                |
| Political Conflict| OT    | soc-soc-vio-vio | **SO0201**                     | SOC-CONF     | Armed Conflict                   |
| Terrorism         | OT    | soc-soc-vio-vio | **SO0203**                     | SOC-CONF     | Terrorism                        |
| Weapons           | OT    | soc-soc-vio-vio | **SO0201**                     | SOC-CONF     | Armed Conflict                   |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event. For "Extreme Temperature", use MH0501 for heat-related events and MH0502 for cold-related events.

This comprehensive mapping ensures standardized hazard categorization for all PDC tracked hazards, including both natural and geopolitical/technological events.

## Hazard Item

A PDC event and the timestamp from exposure endpoint will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard). Here is a table with the STAC fields that are managed from the PDC event to the STAC hazard.

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | `country` field in the list `totalByCountry` | List of country iso3 are pulled from exposure endpoint by iterating `totalByCountry` field |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | type_ID | The hazard codes are generated using the mapping |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) | snc_url | Asset with the link to the PDC report |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) |      |

## Impact item

The PDC events will produce multiple [**Impact STAC Items**](https://github.com/IFRCGo/monty-stac-extension#impact) when impact related data is available through exposure endpoint.

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes) | `country` field in the list `totalByCountry` | List of country iso3 are pulled from exposure endpoint by iterating `totalByCountry` field |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | type_ID | The hazard codes are generated using the mapping |
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
