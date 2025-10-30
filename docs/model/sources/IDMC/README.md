# IDMC

The Internal Displacement Monitoring Centre (IDMC) maintains the Global Internal Displacement Database (GIDD), which provides comprehensive information on global internal displacement events from 2008 onwards.

## Collection: `idmc-events`

A STAC collection holding IDMC disaster-related displacement events.

- Name: Global Internal Displacement Database (GIDD) Events
- Code: `IDMC`
- Source organisation: Internal Displacement Monitoring Centre (IDMC)
- Source code: IDMC
- Source Type: International Non-Governmental Organization
- Source organization email: <info@idmc.ch>
- Source URL: <https://www.internal-displacement.org/database>
- Source Data license: \[TBD]
- Source for: event
- API Documentation: <https://helix-tools-api.idmcdb.org/external-api/>

### Data

- Swagger JSON URL: <https://helix-tools-api.idmcdb.org/external-api/>
- openAPI : <https://helix-tools-api.idmcdb.org/external-api/api-schema/>

#### Disasters Dataset

The [GIDD Disasters Dataset](https://www.internal-displacement.org/database/api-documentation/#gidd-disasters-dataset) provides event information through the `/gidd/disasters/` API endpoint.

Nevertheless, the items in this dataset are not consolidated into a single event. Instead, they are individual records of displacement events. We will focus on the event information provided in the [GIDD disaggregated data](#gidd-disaggregated-data).

#### GIDD disaggregated data

The [GIDD Disaggregated Data](https://www.internal-displacement.org/database/api-documentation/#gidd-disaggregated-data) provides quality-controlled, annually validated data on internal displacement due to conflicts and disasters, disaggregated by caseload. This dataset is disaggregated by caseload, location and event.

Endpoint URL: <<https://helix-tools-api.idmcdb.org/external-api/gidd/disaggregations/disaggregation-geojson/?client_id=><secret>>

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)[0]                              | country_iso3                                                                                 | Yes      | Direct mapping to array                                                            |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                   | {Hazard Category} and {Hazard Type}                                                          | Yes      | Map using the [hazard type mapping](#hazard-type-mapping)                          |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number)                                 |                                                                                              | Yes      | Always 1 (IDMC doesn't track episodes)                                             |
| [monty:corr_id](https://github.com/IFRCGo/monty-stac-extension#montycorr_id)                                             | id                                                                                           | Yes      | Generated following the [event pairing procedure](../../correlation_identifier.md) |

### Displacement items geometry aggregagtion for event geometry

The geometry of the event is derived from the geometry of the displacement items. The geometry of the event is an aggregation of the geometries of all the displacement items associated with the event. The aggregation is done based on the following rules:

1. If all the geometries are points, the event geometry is a MultiPoint geometry.
2. If all the geometries are polygons, the event geometry is a MultiPolygon geometry.
3. If the geometries are a mix of points and polygons, the event geometry is a MultiPolygon geometry with the points converted to polygons.

#### Hazard Type Mapping

IDMC uses the same hazard classification as [EM-DAT CRED](../../taxonomy.md#em-dat-cred-classification-tree) and must follow the **2025 UNDRR-ISC** code is the **reference classification** for the Monty extension:

| IDMC Type           | IDMC SubType                | GLIDE | EM-DAT                             | **UNDRR-ISC 2025** (Reference) | Cluster    | Description                     |
| ------------------- | --------------------------- | ----- | ---------------------------------- | ------------------------------ | ---------- | ------------------------------- |
| Drought             | Drought                     | DR    | nat-cli-drt-drt                    | **MH0401**                     | MH-PRECIP  | Drought                         |
| Earthquake          | Earthquake                  | EQ    | nat-geo-eqt-eqt                    | **GH0101**                     | GEO-SEIS   | Earthquake                      |
| Erosion             | Erosion                     | OT    | nat-geo-env-coa                    | **GH0403**                     | GEO-OTHER  | Erosion                         |
| Extreme Temperature | Cold wave                   | CW    | nat-met-ext-col                    | **MH0502**                     | MH-TEMP    | Extreme Temperature - Cold Wave |
| Flood               | Flood                       | FL    | nat-hyd-flo-flo                    | **MH0600**                     | MH-PRECIP  | Flooding (chapeau)              |
| Flood               | Dam release flood           | FL    | [nat-hyd-flo-flo, tec-mis-col-col] | [**MH0600**, **TL0205**]       | MH-PRECIP  | Dam Break Flood                 |
| Mass Movement       | Landslide/Wet mass movement | LS    | nat-hyd-mmw-lan                    | **GH0300**                     | GEO-GFAIL  | Mass Movement (chapeau)         |
| Mass Movement       | Sinkhole                    | OT    | -                                  | **GH0308**                     | GEO-GFAIL  | Sinkhole                        |
| Sea level Rise      | Sea level rise              | OT    | nat-geo-env-slr                    | **EN0402**                     | ENV-WATER  | Sea Level Rise                  |
| Storm               | Storm                       | VW    | nat-met-sto-sto                    | **MH0310**                     | MH-WIND    | Storm (chapeau)                 |
| Storm               | Tornado                     | TO    | nat-met-sto-tor                    | **MH0305**                     | MH-WIND    | Tornado                         |
| Storm               | Typhoon/Hurricane/Cyclone   | TC    | nat-met-sto-tro                    | **MH0309**                     | MH-WIND    | Tropical Cyclone                |
| Volcanic Activity   | Volcanic activity           | VO    | nat-geo-vol-vol                    | **GH0201**                     | GEO-VOLC   | Volcanic Activity               |
| Wildfire            | Wildfire                    | WF    | nat-cli-wil-for                    | **EN0205**                     | ENV-FOREST | Wildfire                        |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

This mapping enables standardized hazard categorization while preserving IDMC's original classification in the source properties.

### Impact Items

#### Displacement Items (GIDD Disaggregated Data)

The following table shows how IDMC displacement item fields map to STAC Item fields:

| STAC field                                                                                                               | IDMC field                                                                                             | Required | Notes                                                     |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-gidd-impact-`{ID}`-displaced`                                                                    | Yes      | Use format `idmc-impact-{ID}-displaced`                   |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | [feature geometry]                                                                                     | Yes      | Direct mapping from feature geometry                      |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-gidd-impacts`                                                                                    | Yes      |                                                           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | '{Figure category} of {Figure unit} for {Event name} '                                                 | Yes      |                                                           |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | {Start date}                                                                                           | Yes      | Convert to datetime with UTC timezone                     |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | {Start date}                                                                                           | Yes      | Convert to datetime with UTC timezone                     |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | {End date}                                                                                             | Yes      | Convert to datetime with UTC timezone                     |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#basics)                    | [{Locations name}, {Figure category}, {Figure unit}, {Country}, {Geographical region}, {Figure cause}] |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)[0]                              | {ISO3}                                                                                                 | Yes      | Direct mapping to array                                   |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                   | {Hazard Category} and {Hazard Type}                                                                    | Yes      | Map using the [hazard type mapping](#hazard-type-mapping) |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail)                                 | See [Displacement Impact details](#displacement-impact-details)                                        | Yes      |                                                           |

##### Displacement Impact details

The following table shows how IDMC displacement impact fields map to [impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) STAC Item fields:

| STAC field    | IDMC field           | Required | Notes                                                 |
| ------------- | -------------------- | -------- | ----------------------------------------------------- |
| category      | `people`             | Yes      | Always "people" for IDMC impacts                      |
| type          | `displaced_internal` | Yes      | Always "displaced_internal" for IDMC impacts          |
| value         | {Total figures}      | Yes      | Direct mapping                                        |
| unit          | `count`              | Yes      | Always people count (household figures are converted) |
| estimate_type | `primary`            | Yes      | Always "primary" for IDMC impacts                     |

##### Impact Item Generation Rules

1. Each displacement item in the GIDD dataset becomes a separate impact item
2. Geometry is taken directly from the displacement item's feature geometry
3. Dates are converted to UTC timezone
4. Event ID reference uses the format `idmc-gidd-event-{id}`

#### Internal Displacement Updates (IDU) Items

The Internal Displacement Updates (IDU) provide near real-time information about displacement events. Key characteristics include:

##### Impact Item Field Mapping

The following table shows how IDU fields map to STAC Item fields for impact items:

| STAC field                                                                                                               | IDU field                                                  | Required | Notes                                                     |
| ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- | -------- | --------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-idu-impact-`{id}`-displaced`                         | Yes      | Use format `idmc-idu-impact-{id}-displaced`               |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | {latitude}, {longitude}                                    | Yes      | Convert point coordinates to GeoJSON Point geometry       |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-idu-impacts`                                         | Yes      |                                                           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | {displacement_type} displacement for {event_name}          | Yes      |                                                           |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | {displacement_date}                                        | Yes      | Convert to datetime with UTC timezone                     |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | {displacement_start_date}                                  | Yes      | Convert to datetime with UTC timezone                     |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | {displacement_end_date}                                    | Yes      | Convert to datetime with UTC timezone                     |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#basics)                    | [{locations_name}, {displacement_type}, {role}, {sources}] | No       |                                                           |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)[0]                              | {iso3}                                                     | Yes      | Direct mapping to array                                   |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                   | {category}, {type}                                         | Yes      | Map using the [hazard type mapping](#hazard-type-mapping) |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail)                                 | See [IDU Impact details](#idu-impact-details)              | Yes      |                                                           |

##### IDU Impact details

The following table shows how IDU fields map to [impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) STAC Item fields:

| STAC field    | IDU field            | Required | Notes                                                                  |
| ------------- | -------------------- | -------- | ---------------------------------------------------------------------- |
| category      | `people`             | Yes      | Always "people" for IDU impacts                                        |
| type          | `displaced_internal` | Yes      | Always "displaced_internal" for IDU impacts                            |
| value         | {figure}             | Yes      | Direct mapping                                                         |
| unit          | `count`              | Yes      | Always people count                                                    |
| estimate_type | {role}               | Yes      | Maps "Recommended figure" to "primary", "Triangulation" to "secondary" |

##### IDU Impact Item Generation Rules

1. Each IDU record becomes a separate impact item
2. Point geometry is created from latitude/longitude coordinates
3. Dates are converted to UTC timezone
4. Event ID reference uses the format `idmc-idu-event-{event_id}`
5. Role field determines estimate_type in impact_detail

##### Impact Classification

- Type: displaced_internal (internal displacements)
- Category: people (total displaced population)
- Two main categories:
  1. Preventive evacuations (marked in displacement_occurred field)
  2. Forced displacement due to damage/destruction

##### Data Quality Notes

- Provides near real-time updates compared to annually validated GIDD data
- Includes source URLs for verification
- Distinguishes between recommended figures and triangulation
- Specifies accuracy of location information
- Indicates if displacement was preventive or post-disaster
