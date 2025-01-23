# IDMC

The Internal Displacement Monitoring Centre (IDMC) maintains the Global Internal Displacement Database (GIDD), which provides comprehensive information on global internal displacement events from 2008 onwards.

## Collection: `idmc-events`

A STAC collection holding IDMC disaster-related displacement events.

- Name: Global Internal Displacement Database (GIDD) Events
- Code: `IDMC`
- Source organisation: Internal Displacement Monitoring Centre (IDMC)
- Source code: IDMC
- Source Type: International Non-Governmental Organization
- Source organization email: info@idmc.ch
- Source URL: https://www.internal-displacement.org/database
- Source Data license: [TBD]
- Source for: event
- API Documentation: https://helix-tools-api.idmcdb.org/external-api/

### Data

- Swagger JSON URL: https://helix-tools-api.idmcdb.org/external-api/
- openAPI : https://helix-tools-api.idmcdb.org/external-api/api-schema/

#### Disasters Dataset

The [GIDD Disasters Dataset](https://www.internal-displacement.org/database/api-documentation/#gidd-disasters-dataset) provides event information through the `/gidd/disasters/` API endpoint.

Nevertheless, the items in this dataset are not consolidated into a single event. Instead, they are individual records of displacement events. We will focus on the event information provided in the [GIDD disaggregated data](#gidd-disaggregated-data).

#### GIDD disaggregated data

The [GIDD Disaggregated Data](https://www.internal-displacement.org/database/api-documentation/#gidd-disaggregated-data) provides quality-controlled, annually validated data on internal displacement due to conflicts and disasters, disaggregated by caseload. This dataset is disaggregated by caseload, location and event.

Endpoint URL: <https://helix-tools-api.idmcdb.org/external-api/gidd/disaggregations/disaggregation-geojson/?client_id=<secret>>

The returned data is a geojson feature collection. Each feature represents a displacement item that includes the following properties:

- `ID`: IDMC figure unique identifier
- `ISO3`: ISO 3166-1 alpha-3 country code
- `Country`: Country or territory name
- `Geographical region`: IDMC's geographical region classification
- `Figure cause`: Trigger of displacement (e.g., Conflict, Disaster)
- `Year`: Reporting year
- `Figure category`: Type of displacement metric (Internal Displacements or Total Number of IDPs)
- `Figure unit`: Unit of measurement (Person, Household)
- `Reported figures`: Values reported by original source
- `Household size`: Average number of individuals per household
- `Total figures`: Total number of displaced people
- `Hazard category`: Primary hazard classification (e.g., Geophysical, Weather related)
- `Hazard sub category`: Secondary hazard classification
- `Hazard type`: Specific hazard type
- `Hazard sub type`: Detailed hazard classification
- `Start date`: Displacement start date
- `Start date accuracy`: Accuracy of start date
- `End date`: Displacement end date
- `End date accuracy`: Accuracy of end date
- `Stock date`: Date of IDP metric collection (for stock figures)
- `Stock date accuracy`: Accuracy of stock date
- `Stock reporting date`: IDMC reporting year for total IDPs
- `Publishers`: Organizations distributing the data
- `Sources`: Primary data providers
- `Sources type`: Category of data source
- `Event ID`: Unique identifier for events
- `Event name`: Coded event name including location and date
- `Event cause`: Trigger of the event
- `Event main trigger`: Primary hazard or conflict type
- `Event start date`: Event start date
- `Event end date`: Event end date
- `Event start date accuracy`: Accuracy of event start date
- `Event end date accuracy`: Accuracy of event end date
- `Is housing destruction`: Indicates if displacement includes housing destruction
- `Violence type`: Category of violence (for conflict events)
- `Event codes`: External reference codes (e.g., GLIDE numbers)
- `Locations name`: Names of affected locations
- `Locations coordinates`: Geographic coordinates of locations
- `Locations accuracy`: Precision level of reported locations
- `Locations type`: Type of displacement location (Origin/Destination)
- `Displacement occurred`: Indicates if preventive evacuations were reported


### Event Items

The IDMC event items are derived from the GIDD disaggregated data.

> [!IMPORTANT]
> A GIDD geojson is a collection of displacement items. Multiple items can be associated with a single event. The event item is created by consolidating these items into a single event.

The following table shows how IDMC event fields map to STAC Item fields:

| STAC field                                                                                                               | IDMC field                                                                                   | Required | Notes                                                                              |
| ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-event-`{Event ID}                                                                      | Yes      | Use format `idmc-event-{id}`                                                       |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | [feature geometry aggregation](#displacement-items-geometry-aggregagtion-for-event-geometry) | Yes      | Aggregation in multi points or multipolygon of all the items referencing the event |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-events`                                                                                | Yes      |                                                                                    |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | {Event name}                                                                                 | Yes      |                                                                                    |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | {Event start date}                                                                           | Yes      | Convert to datetime with UTC timezone                                              |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | {Event start date}                                                                           | Yes      | Convert to datetime with UTC timezone                                              |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | {Event end date}                                                                             | Yes      | Convert to datetime with UTC timezone                                              |
| [monty:country_codes](../../../README.md#montycountry_codes)\[0]                                                         | country_iso3                                                                                 | Yes      | Direct mapping to array                                                            |
| [monty:hazard_codes](../../../README.md#montyhazard_codes)                                                               | {Hazard Category} and {Hazard Type}                                                          | Yes      | Map using the [hazard type mapping](#hazard-type-mapping)                          |
| [monty:hazard_codes](../../../README.md#montyepisode_number                                                              |                                                                                              | Yes      | Always 1 (IDMC doesn't track episodes)                                             |
| [monty:corr_id](../../../README.md#montycorr_id)                                                                         | id                                                                                           | Yes      | Generated following the [event pairing procedure](../../event_paring.md)           |

### Displacement items geometry aggregagtion for event geometry

The geometry of the event is derived from the geometry of the displacement items. The geometry of the event is an aggregation of the geometries of all the displacement items associated with the event. The aggregation is done based on the following rules:

1. If all the geometries are points, the event geometry is a MultiPoint geometry.
2. If all the geometries are polygons, the event geometry is a MultiPolygon geometry.
3. If the geometries are a mix of points and polygons, the event geometry is a MultiPolygon geometry with the points converted to polygons.

# Hazard Type Mapping 

IDMC uses the same hazard classification as [EM-DAT](../EM-DAT/README.md#mapping-from-em-dat-event-type-to-hazard-profile), mapped to [UNDRR-ISC 2020 Hazard Information Profile](../../taxonomy.md#undrr-isc-2020-hazard-information-profiles) codes following this mapping table:

| Hazard Category | Hazard sub category | Hazard Type           | Hazard sub type | UNDRR-ISC 2020 Hazard Information Profile |
| --------------- | ------------------- | --------------------- | --------------- | ----------------------------------------- |
| Meteorological  | Storm               | Extra-tropical Storm  | -               | MH0031                                    |
| Meteorological  | Storm               | Tropical Cyclone      | -               | MH0057                                    |
| Meteorological  | Storm               | Sand/Dust storm       | -               | MH0015                                    |
| Meteorological  | Storm               | Local Storm           | Tornado         | MH0059                                    |
| Meteorological  | Extreme Temperature | Cold Wave             | -               | MH0040                                    |
| Meteorological  | Extreme Temperature | Heat Wave             | -               | MH0047                                    |
| Meteorological  | Extreme Temperature | Severe Winter         | -               | MH0040, MH0047                            |
| Hydrological    | Flood               | Flash Flood           | -               | MH0006                                    |
| Hydrological    | Flood               | General Flood         | -               | MH0007                                    |
| Hydrological    | Flood               | Storm Surge           | Coastal Flood   | MH0004                                    |
| Hydrological    | Flood               | Ice Jam Flood         | -               | MH0009                                    |
| Climatological  | Drought             | Drought               | -               | MH0035                                    |
| Climatological  | Wildfire            | Forest Fire           | -               | EN0013                                    |
| Climatological  | Wildfire            | Land Fire             | -               | EN0013                                    |
| Climatological  | Wildfire            | Bush/Brush Fire       | -               | EN0013                                    |
| Climatological  | Glacial             | Glacial Lake Outburst | -               | MH0013                                    |
| Geophysical     | Earthquake          | Ground Movement       | -               | GH0004                                    |
| Geophysical     | Earthquake          | Tsunami               | -               | GH0006                                    |
| Geophysical     | Volcanic Activity   | Ash Fall              | -               | GH0010                                    |
| Geophysical     | Volcanic Activity   | Lahar                 | -               | GH0013                                    |
| Geophysical     | Volcanic Activity   | Lava Flow             | -               | GH0009                                    |
| Geophysical     | Volcanic Activity   | Pyroclastic Flow      | -               | GH0012                                    |
| Geophysical     | Mass Movement (dry) | Landslide             | -               | GH0007                                    |
| Geophysical     | Mass Movement (dry) | Rockfall              | -               | GH0032                                    |
| Geophysical     | Mass Movement (dry) | Subsidence            | -               | GH0024                                    |

When implementing the mapping:

1. The primary hazard code is used in the `monty:hazard_codes` field  
2. Original hazard codes are included in `keywords` for improved searchability

This mapping enables standardized hazard categorization while preserving IDMC's original classification in the source properties.