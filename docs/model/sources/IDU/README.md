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

### Hazard Codes
For the Hazard codes, the following mappings are being considered.

| Tuple of Category, Subcategory, Type, Subtype                                       | Hazard code                   |
| ----------------------------------------------------------------------------------- | ----------------------------- |
| ('geophysical', 'geophysical', 'earthquake', 'earthquake')                          | ["nat-geo-ear-gro"]           |
| ('geophysical', 'geophysical', 'earthquake', 'tsunami')                             | ["nat-geo-ear-tsu"]           |
| ('geophysical', 'geophysical', 'mass movement', 'dry mass movement')                | ["nat-geo-mmd-lan"]           |
| ('geophysical', 'geophysical', 'mass movement', 'sinkhole')                         | ["nat-geo-mmd-sub"]           |
| ('geophysical', 'geophysical', 'volcanic activity', 'volcanic activity')            | ["nat-geo-vol-vol"]           |
| ('mixed disasters', 'mixed disasters', 'mixed disasters', 'mixed disasters')        | ["mix-mix-mix-mix"]           |
| ('weather related', 'climatological', 'desertification', 'desertification')         | ["EN0006", "nat-geo-env-des"] |
| ('weather related', 'climatological', 'drought', 'drought')                         | ["nat-cli-dro-dro"]           |
| ('weather related', 'climatological', 'erosion', 'erosion')                         | ["EN0019", "nat-geo-env-soi"] |
| ('weather related', 'climatological', 'salinisation', 'salinization')               | ["EN0007", "nat-geo-env-slr"] |
| ('weather related', 'climatological', 'sea level rise', 'sea level rise')           | ["EN0023", "nat-geo-env-slr"] |
| ('weather related', 'climatological', 'wildfire', 'wildfire')                       | ["nat-cli-wil-wil"]           |
| ('weather related', 'hydrological', 'flood', 'dam release flood')                   | ["tec-mis-col-col"]           |
| ('weather related', 'hydrological', 'flood', 'flood')                               | ["nat-hyd-flo-flo"]           |
| ('weather related', 'hydrological', 'mass movement', 'avalanche')                   | ["nat-hyd-mmw-ava"]           |
| ('weather related', 'hydrological', 'mass movement', 'landslide/wet mass movement') | ["nat-hyd-mmw-lan"]           |
| ('weather related', 'hydrological', 'wave action', 'rogue wave')                    | ["nat-hyd-wav-rog"]           |
| ('weather related', 'meteorological', 'extreme temperature', 'cold wave')           | ["nat-met-ext-col"]           |
| ('weather related', 'meteorological', 'extreme temperature', 'heat wave')           | ["nat-met-ext-hea"]           |
| ('weather related', 'meteorological', 'storm', 'hailstorm')                         | ["nat-met-sto-hai"]           |
| ('weather related', 'meteorological', 'storm', 'sand/dust storm')                   | ["nat-met-sto-san"]           |
| ('weather related', 'meteorological', 'storm', 'storm surge')                       | ["nat-met-sto-sur"]           |
| ('weather related', 'meteorological', 'storm', 'storm')                             | ["nat-met-sto-sto"]           |
| ('weather related', 'meteorological', 'storm', 'tornado')                           | ["nat-met-sto-tor"]           |
| ('weather related', 'meteorological', 'storm', 'typhoon/hurricane/cyclone')         | ["nat-met-sto-tro"]           |
| ('weather related', 'meteorological', 'storm', 'winter storm/blizzard')             | ["nat-met-sto-bli"]           |

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
