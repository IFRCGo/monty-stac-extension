# IDU

The IDU(Internal Displacements Updates) tracks the number of the people who are internally displaced in a region or a country due to `disaster` or `conflict`.

## Data Sources

API: https://helix-tools-api.idmcdb.org/external-api/

Current Usage: https://www.internal-displacement.org/internal-displacement-updates/

## Collection: `idu-events`

Collection: idu-events

A STAC collection hold all the IDU events.

Name: Internal displacement updates

Code: IDU

Source organization: Internal Displacement Monitoring Center (IDMC)

Source organization type: Regional Intergovernmental Organization

Source organization email: info@idmc.ch

Source code: IDMC

Source URL: https://helix-tools-api.idmcdb.org/external-api/

Source for: event, impact

previous implementation (R): none


| STAC field                         | IDU Field                            | Remarks                        |
| ---------------------------------- | ------------------------------------ | ------------------------------ |
| id                                 | event_id                             | Prepend text for uniqueness             |
| collection                         | `idu-events`                         | Collection name for STAC       |
| title                              | event_name                           | Name of the event              |
| description                        | standard_popup_text                  |                                |
| datetime                           | displacement_date                    | Start date of the event        |
| geometry                           | type: "point", coordinates: centroid | centroid of the event location |
| bbox                               | latitude, longitude                  | Use latitude and longitude     |
| monty:country_codes[0]             | iso3                                 |                                |
| monty:event_codes                  | event_codes                          | Might be empty                 |
| monty:episode_number               | episode_number                       | This is a fixed value (1)      |
| monty.hazard_codes                 | Based on category, subcategory, type, subtype | List of hazard codes converted following the Hazard profile mapping |
| properties.locations               | locations_name                       |                                |
| properties.start_datetime          | event_start_date                     |                                |
| properties.end_datetime            | event_end_date                       |                                |
| properties.sources                 | sources                              |                                |
| properties.roles                   | [`source`, `event`]                  |                                |
| asset.report                       | source_url                           |                                |
| `via` link                         | main source url                      | Link to the main source url    |


### Hazard Codes
For the Hazard codes, the following mappings are being considered.

| Tuple of Category, Subcategory, Type, Subtype | Hazard code |
| --------------------------------------------- | ----------- |
| ('geophysical', 'geophysical', 'earthquake', 'earthquake') | ["GH0001", "GH0004"] |
| ('geophysical', 'geophysical', 'earthquake', 'tsunami') | ["GH0006"] |
| ('geophysical', 'geophysical', 'mass movement', 'dry mass movement') | ["GH0007", "GH0014"] |
| ('geophysical', 'geophysical', 'mass movement', 'sinkhole') | ["GH0026"] |
| ('geophysical', 'geophysical', 'volcanic activity', 'volcanic activity') | ["GH0020"] |
| ('mixed disasters', 'mixed disasters', 'mixed disasters', 'mixed disasters') | ["Mixed Disaster"] |
| ('weather related', 'climatological', 'desertification', 'desertification') | ["EN0014"] |
| ('weather related', 'climatological', 'drought', 'drought') | ["MH0035"] |
| ('weather related', 'climatological', 'erosion', 'erosion') | ["EN0019"] |
| ('weather related', 'climatological', 'salinisation', 'salinization') | ["Salinization"] |
| ('weather related', 'climatological', 'sea level rise', 'sea level rise') | ["EN0023"] |
| ('weather related', 'climatological', 'wildfire', 'wildfire') | ["EN0013"] |
| ('weather related', 'hydrological', 'flood', 'dam release flood') | ["TL0009"] |
| ('weather related', 'hydrological', 'flood', 'flood') | ["FL"] |
| ('weather related', 'hydrological', 'mass movement', 'avalanche') | ["MH0050"] |
| ('weather related', 'hydrological', 'mass movement', 'landslide/wet mass movement') | ["MH0051"] |
| ('weather related', 'hydrological', 'wave action', 'rogue wave') | ["MH0027"] |
| ('weather related', 'meteorological', 'extreme temperature', 'cold wave') | ["MH0040"] |
| ('weather related', 'meteorological', 'extreme temperature', 'heat wave') | ["MH0047"] |
| ('weather related', 'meteorological', 'storm', 'hailstorm') | ["MH0036"] |
| ('weather related', 'meteorological', 'storm', 'sand/dust storm') | ["MH0015"] |
| ('weather related', 'meteorological', 'storm', 'storm surge') | ["MH0027"] |
| ('weather related', 'meteorological', 'storm', 'storm') | ["MH0058"] |
| ('weather related', 'meteorological', 'storm', 'tornado') | ["MH0059"] |
| ('weather related', 'meteorological', 'storm', 'typhoon/hurricane/cyclone') | ["MH0057"] |
| ('weather related', 'meteorological', 'storm', 'winter storm/blizzard') | ["MH0034"] |

### Impact Item

According to the event type and the fields available in the IDU event, an impact STAC Item can be created.
Here is the table with the STAC fields that are mapped from IDU event to the STAC.
| STAC field                         | IDU Field                            | Remarks                        |
| ---------------------------------- | ------------------------------------ | ------------------------------ |
| id                                 | event_id                             | Prepend text for uniqueness             |
| collection                         | `idu-impact`                         | Collection name for STAC       |
| title                              | event_name                           | Name of the event              |
| description                        | standard_popup_text                  |                                |
| datetime                           | displacement_date                    | Start date of the event        |
| geometry                           | type: "point", coordinates: centroid | centroid of the event location |
| bbox                               | latitude, longitude                  | Use latitude and longitude     |
| monty:country_codes[0]             | iso3                                 |                                |
| monty:event_codes                  | event_codes                          | Might be empty                 |
| monty:episode_number               | episode_number                       | This is a fixed value (1)      |
| monty.hazard_codes                 | Based on category, subcategory, type, subtype | List of hazard codes converted following the Hazard profile mapping |
| properties.locations               | locations_name                       |                                |
| properties.start_datetime          | displacement_start_date              |                                |
| properties.end_datetime            | displacement_end_date                |                                |
| properties.sources                 | sources                              |                                |
| properties.roles                   | [`source`, `impact`]                 |                                |
| asset.report                       | source_url                           |                                |
| `via` link                         | main source url                      | Link to the main source url    |
| monty.impact_detail                | impact_detail                        | As shown in impact_detail below|

#### Impact Detail
The ImpactDetail is constructed using the following
| Key                   | Value                 |
| --------------------- | --------------------- |
| category              | MontyImpactExposureCategory.ALL_PEOPLE    |
| type                  | MontyImpactType.INTERNALLY_DISPLACED_PERSONS |
| value                 | figure field from IDU data |
| unit                  | `count`                   |
| estimate_type         | MontyEstimateType.PRIMARY |