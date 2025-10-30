# IDU

The IDU(Internal Displacements Updates) tracks the number of the people who are internally displaced in a region or a country due to `disaster` or `conflict`.

```text
Note: As of now, we only deal with disaster type events.
```

## Data Sources

API: <https://helix-tools-api.idmcdb.org/external-api/>

Current Usage: <https://www.internal-displacement.org/internal-displacement-updates/>

## Collection: `idmc-idu-events`

Collection: idu-events

A STAC collection hold all the IDU events.

Name: Internal displacement updates

Code: IDU

Source organization: Internal Displacement Monitoring Center (IDMC)

Source organization type: Regional Intergovernmental Organization

Source organization email: <info@idmc.ch>

Source code: IDMC

Source URL: <https://helix-tools-api.idmcdb.org/external-api/>

Source for: event, impact

previous implementation (R): none

| STAC field                                                                                                                        | IDU Field                                     | Remarks                                                             |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                             | `idmc-idu-event-{event_id}`                   | Prepend text for uniqueness                                         |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                             | `idmc-idu-events`                             | Collection name for STAC                                            |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                                  | event_name                                    | Name of the event                                                   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                            | standard_popup_text                           |                                                                     |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)                        | displacement_date                             | Start date of the event                                             |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                                 | type: "point", coordinates: centroid          | centroid of the event location                                      |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                                         | latitude, longitude                           | Use latitude and longitude                                          |
| [monty:country_codes[0]](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                                                   | iso3                                          |                                                                     |
| monty:event_codes                                                                                                                 | event_codes                                   | Might be empty                                                      |
| monty:episode_number                                                                                                              | episode_number                                | This is a fixed value (1)                                           |
| [monty.hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                                        | Based on category, subcategory, type, subtype | List of hazard codes converted following the Hazard profile mapping |
| properties.locations                                                                                                              | locations_name                                |                                                                     |
| [properties.start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | event_start_date                              |                                                                     |
| [properties.end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | event_end_date                                |                                                                     |
| properties.sources                                                                                                                | sources                                       |                                                                     |
| properties.roles                                                                                                                  | [`source`, `event`]                           |                                                                     |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                           | source_url                                    |                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                                 | main source url                               | Link to the main source url                                         |

#### Hazard Type Mapping

IDU uses EM-DAT classification and must follow the **2025 UNDRR-ISC** code as the **reference classification** for the Monty extension:

| IDU Category/Subcategory/Type/Subtype                                                | GLIDE | EM-DAT              | **UNDRR-ISC 2025** (Reference) | Cluster    | Description                         |
| ------------------------------------------------------------------------------------ | ----- | ------------------- | ------------------------------ | ---------- | ----------------------------------- |
| ('geophysical', 'geophysical', 'earthquake', 'earthquake')                           | EQ    | nat-geo-ear-gro     | **GH0101**                     | GEO-SEIS   | Earthquake                          |
| ('geophysical', 'geophysical', 'earthquake', 'tsunami')                              | TS    | nat-geo-ear-tsu     | **MH0705**                     | MH-MARINE  | Tsunami                             |
| ('geophysical', 'geophysical', 'mass movement', 'dry mass movement')                 | LS    | nat-geo-mmd-lan     | **GH0300**                     | GEO-GFAIL  | Gravitational Mass Movement         |
| ('geophysical', 'geophysical', 'mass movement', 'sinkhole')                          | OT    | nat-geo-mmd-sub     | **GH0308**                     | GEO-GFAIL  | Sinkhole                            |
| ('geophysical', 'geophysical', 'volcanic activity', 'volcanic activity')             | VO    | nat-geo-vol-vol     | **GH0201**                     | GEO-VOLC   | Lava Flows                          |
| ('weather related', 'climatological', 'desertification', 'desertification')          | OT    | nat-geo-env-des     | **EN0206**                     | ENV-FOREST | Desertification                     |
| ('weather related', 'climatological', 'drought', 'drought')                          | DR    | nat-cli-dro-dro     | **MH0401**                     | MH-PRECIP  | Drought                             |
| ('weather related', 'climatological', 'erosion', 'erosion')                          | OT    | nat-geo-env-soi     | **GH0403**                     | GEO-OTHER  | Soil Erosion                        |
| ('weather related', 'climatological', 'salinisation', 'salinization')                | OT    | nat-geo-env-slr     | **EN0303**                     | ENV-LAND   | Salinity & Sodicity                 |
| ('weather related', 'climatological', 'sea level rise', 'sea level rise')            | OT    | nat-geo-env-slr     | **EN0402**                     | ENV-WATER  | Sea Level Rise                      |
| ('weather related', 'climatological', 'wildfire', 'wildfire')                        | WF    | nat-cli-wil-wil     | **EN0205**                     | ENV-FOREST | Wildfires                           |
| ('weather related', 'hydrological', 'flood', 'dam release flood')                    | FL    | tec-mis-col-col     | **TL0205**                     | TECH-STRFAIL | Dam Failure                       |
| ('weather related', 'hydrological', 'flood', 'flood')                                | FL    | nat-hyd-flo-flo     | **MH0600**                     | MH-WATER   | Flooding (chapeau)                  |
| ('weather related', 'hydrological', 'mass movement', 'avalanche')                    | AV    | nat-hyd-mmw-ava     | **MH0801**                     | MH-TERR    | Avalanche                           |
| ('weather related', 'hydrological', 'mass movement', 'landslide/wet mass movement')  | LS    | nat-hyd-mmw-lan     | **GH0304**                     | GEO-GFAIL  | Slides                              |
| ('weather related', 'hydrological', 'wave action', 'rogue wave')                     | OT    | nat-hyd-wav-rog     | **MH0701**                     | MH-MARINE  | Rogue Wave                          |
| ('weather related', 'meteorological', 'extreme temperature', 'cold wave')            | CW    | nat-met-ext-col     | **MH0502**                     | MH-TEMP    | Cold Wave                           |
| ('weather related', 'meteorological', 'extreme temperature', 'heat wave')            | HT    | nat-met-ext-hea     | **MH0501**                     | MH-TEMP    | Heatwave                            |
| ('weather related', 'meteorological', 'storm', 'hailstorm')                          | ST    | nat-met-sto-hai     | **MH0404**                     | MH-PRECIP  | Hail                                |
| ('weather related', 'meteorological', 'storm', 'sand/dust storm')                    | VW    | nat-met-sto-san     | **MH0201**                     | MH-PART    | Dust Storm or Sandstorm             |
| ('weather related', 'meteorological', 'storm', 'storm surge')                        | SS    | nat-met-sto-sur     | **MH0703**                     | MH-MARINE  | Storm Surge                         |
| ('weather related', 'meteorological', 'storm', 'storm')                              | ST    | nat-met-sto-sto     | **MH0103**                     | MH-CONV    | Thunderstorm                        |
| ('weather related', 'meteorological', 'storm', 'tornado')                            | TO    | nat-met-sto-tor     | **MH0305**                     | MH-WIND    | Tornado                             |
| ('weather related', 'meteorological', 'storm', 'typhoon/hurricane/cyclone')          | TC    | nat-met-sto-tro     | **MH0309**                     | MH-WIND    | Tropical Cyclone                    |
| ('weather related', 'meteorological', 'storm', 'winter storm/blizzard')              | OT    | nat-met-sto-bli     | **MH0403**                     | MH-PRECIP  | Blizzard                            |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

This mapping enables standardized hazard categorization while preserving IDU's original classification in the source properties.

### Impact Item

According to the event type and the fields available in the IDU event, an impact STAC Item can be created.
Here is the table with the STAC fields that are mapped from IDU event to the STAC.
| STAC field                                                                                                                        | IDU Field                                     | Remarks                                                             |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | `idmc-idu-impact-{id}-{impact_type}` | Prepend text for uniqueness, Note that `impact_type` is extracted from the `description` field. If the proper `impact_type` is not found, the default value `displaced` is used. |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                             | `idmc-idu-impacts`                            | Collection name for STAC                                            |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                                  | event_name                                    | Name of the event                                                   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                            | standard_popup_text                           |                                                                     |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)                        | displacement_date                             | Start date of the event                                             |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                                 | type: "point", coordinates: centroid          | centroid of the event location                                      |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                                         | latitude, longitude                           | Use latitude and longitude                                          |
| [monty:country_codes[0]](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                                                   | iso3                                          |                                                                     |
| monty:event_codes                                                                                                                 | event_codes                                   | Might be empty                                                      |
| monty:episode_number                                                                                                              | episode_number                                | This is a fixed value (1)                                           |
| [monty.hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                                        | Based on category, subcategory, type, subtype | List of hazard codes converted following the Hazard profile mapping |
| properties.locations                                                                                                              | locations_name                                |                                                                     |
| [properties.start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | event_start_date                              |                                                                     |
| [properties.end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | event_end_date                                |                                                                     |
| properties.sources                                                                                                                | sources                                       |                                                                     |
| properties.roles                                                                                                                  | [`source`, `impact`]                          |                                                                     |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                           | source_url                                    |                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                                 | main source url                               | Link to the main source url                                         |
| monty.impact_detail                                                                                                               | impact_detail                                 | As shown in impact_detail below                                     |

#### Impact Detail

The following mappings are used to create ImpactDetail objects.
| impact_type   | Monty Impact Exposure Category         | Monty Impact Type |
| ------------- | -------------------------------------- | ----------------- |
| evacuated     | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.EVACUATED |
| displaced     | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.INTERNALLY_DISPLACED_PERSONS |
| relocated     | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.RELOCATED |
| sheltered     | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.EMERGENCY_SHELTERED |
| homeless      | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.HOMELESS |
| affected      | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.TOTAL_AFFECTED |
| IDPs          | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.INTERNALLY_DISPLACED_PERSONS |
| Internal Displacements | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.INTERNALLY_DISPLACED_PERSONS |
| Deaths | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.DEATH |
| evacuated | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.EVACUATED |
| People displaced across borders | MontyImpactExposureCategory.ALL_PEOPLE | MontyImpactType.EXTERNALLY_DISPLACED_PERSONS |

Below is an example to construct the ImpactDetail object:

| Key           | Value                                        |
| ------------- | -------------------------------------------- |
| category      | MontyImpactExposureCategory.ALL_PEOPLE       |
| type          | MontyImpactType.INTERNALLY_DISPLACED_PERSONS |
| value         | figure field from IDU data                   |
| unit          | `count`                                      |
| estimate_type | MontyEstimateType.PRIMARY                    |
