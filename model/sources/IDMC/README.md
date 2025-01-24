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
- Source Data license: [TBD]
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
| [monty:country_codes](../../../README.md#montycountry_codes)\[0]                                                         | country_iso3                                                                                 | Yes      | Direct mapping to array                                                            |
| [monty:hazard_codes](../../../README.md#montyhazard_codes)                                                               | {Hazard Category} and {Hazard Type}                                                          | Yes      | Map using the [hazard type mapping](#hazard-type-mapping)                          |
| [monty:hazard_codes](../../../README.md#montyepisode_number                                                              |                                                                                              | Yes      | Always 1 (IDMC doesn't track episodes)                                             |
| [monty:corr_id](../../../README.md#montycorr_id)                                                                         | id                                                                                           | Yes      | Generated following the [event pairing procedure](../../event_paring.md)           |

### Displacement items geometry aggregagtion for event geometry

The geometry of the event is derived from the geometry of the displacement items. The geometry of the event is an aggregation of the geometries of all the displacement items associated with the event. The aggregation is done based on the following rules:

1. If all the geometries are points, the event geometry is a MultiPoint geometry.
2. If all the geometries are polygons, the event geometry is a MultiPolygon geometry.
3. If the geometries are a mix of points and polygons, the event geometry is a MultiPolygon geometry with the points converted to polygons.

#### Hazard Type Mapping 

IDMC uses the same hazard classification as [EM-DAT CRED](../../taxonomy.md#em-dat-cred-classification-tree) and must follow the general rule for hazard code generation.

This mapping enables standardized hazard categorization while preserving IDMC's original classification in the source properties.