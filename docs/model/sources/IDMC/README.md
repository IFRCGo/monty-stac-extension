# IDMC

The Internal Displacement Monitoring Centre (IDMC) maintains the Global Internal Displacement Database (GIDD), which provides comprehensive information on global internal displacement events from 2008 onwards.

## Collections: `idmc-gidd-events` and `idmc-gidd-impacts`

Two STAC collections hold the GIDD data: one for the disaster events, and one for the displacement figures of each event.

The Internal Displacement Updates (IDU) of IDMC are a different source with their own collections. See the [IDU source doc](../IDU/README.md).

- Name: Global Internal Displacement Database (GIDD) Events
- Code: `IDMC`
- Source organisation: Internal Displacement Monitoring Centre (IDMC)
- Source code: IDMC
- Source Type: International NGO
- Source organization email: <info@idmc.ch>
- Source URL: <https://www.internal-displacement.org/database>
- Source Data license: None stated by the source (checked 2026-07)
- Source for: event, impact
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

### Which records are ingested

- Only the features with `Figure cause` = `Disaster` are ingested. `Conflict` and `Other` figures are ignored.
- The transformer groups the features by `Event ID`. Each group gives one event item, and one impact item for each feature of the group.
- If one feature of a group is not valid, or the hazard of the event is not in the [hazard type mapping](#hazard-type-mapping), the transformer skips all the group and counts its records as failed. It continues with the next group.

On the reference file [`IDMC_GIDD_Internal_Displacement_Disaggregated.geojson`](./IDMC_GIDD_Internal_Displacement_Disaggregated.geojson) (100 features, 97 of them `Disaster`), the transformer gives 43 event items and 97 impact items.

### Event Items

The GIDD event items are derived from the GIDD disaggregated data.

> [!IMPORTANT]
> A GIDD geojson is a collection of displacement figures. Several figures can refer to the same event. The event item is built from the **first figure** of the event. Only `monty:country_codes` uses all the figures.

The following table shows how GIDD fields map to STAC Item fields:

| STAC field                                                                                                               | GIDD field                               | Required | Notes                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-gidd-event-`{Event ID}             | Yes      | For example `idmc-gidd-event-22194`                                                                     |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | feature geometry of the first figure     | Yes      | See [Event geometry](#event-geometry). `bbox` is computed from it                                      |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-gidd-events`                       | Yes      |                                                                                                         |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | {Event name}                             | Yes      |                                                                                                         |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | {Event start date}                       | Yes      | Convert to datetime with UTC timezone                                                                   |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | {Event start date}                       | Yes      | Convert to datetime with UTC timezone                                                                   |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | {Event end date}                         | Yes      | Convert to datetime with UTC timezone                                                                   |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#basics)                    | Generated                                | No       | The keywords of the hazard profile, then the country codes                                              |
| `location`, `location_accuracy`, `location_type`                                                                         | {Locations name}, {Locations accuracy}, {Locations type} | No | Lists, copied from the first figure                                                      |
| `displacement_occured`                                                                                                   | {Displacement occurred}                  | No       | The property name has one `r`. That is the name the transformer writes                                  |
| `sources`, `publishers`                                                                                                  | {Sources}, {Publishers}                  | No       | Lists, copied from the first figure                                                                     |
| `roles`                                                                                                                  | `["source", "event"]`                    | Yes      |                                                                                                         |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                 | {ISO3} of all the figures of the event   | Yes      | No duplicates. The country of the first figure is first, because `monty:corr_id` uses the first code   |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                   | {Hazard category}, {Hazard sub category}, {Hazard type}, {Hazard sub type} | Yes | Map using the [hazard type mapping](#hazard-type-mapping)                       |
| [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number)                               | Generated                                | Yes      | Always 1 (IDMC does not track episodes)                                                                 |
| [monty:corr_id](https://github.com/IFRCGo/monty-stac-extension#montycorr_id)                                             | Generated                                | Yes      | Generated following the [event pairing procedure](../../correlation_identifier.md)                      |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                      | {Event ID}                               | Yes      | The source identifier of the event, as a string                                                         |
| [processing:version](https://github.com/stac-extensions/processing)                                                      | Generated                                | No       | Semantic version of the transformer that generated the item, via the `processing:` extension            |
| [processing:software](https://github.com/stac-extensions/processing)                                                     | Generated                                | No       | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension          |
| `assets.source`                                                                                                          | URL of the source file                   | Yes      | `application/geo+json`, role `source`                                                                   |
| `links[rel=via]`                                                                                                         | URL of the source file                   | Yes      |                                                                                                         |
| `links[rel=related]`                                                                                                     | each impact item of the event            | Yes      | `roles: ["impact"]`                                                                                     |

### Event geometry

The transformer copies the geometry of the first figure of the event. It does not aggregate the geometries of the other figures. For the event `22194` (26 figures in Syria and Türkiye), the event item has the one point of its first figure (Aleppo).

The target is an aggregation of the geometries of all the figures of the event:

1. If all the geometries are points, the event geometry is a MultiPoint geometry.
2. If all the geometries are polygons, the event geometry is a MultiPolygon geometry.
3. If the geometries are a mix of points and polygons, the event geometry is a MultiPolygon geometry with the points converted to polygons.

The transformer does not do this aggregation yet. The dates have the same limit: `Event start date` and `Event end date` come from the first figure.

#### Hazard Type Mapping

The IDMC hazard classification has four levels. The **UNDRR-ISC 2025** code is the **reference classification** for the Monty extension. GIDD and [IDU](../IDU/README.md) use the same mapping:

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

IDMC's `typhoon/hurricane/cyclone` category states a tropical system, so it takes the
Tropical Cyclone row (`MH0309`), not the generic storm row (`MH0301`). This follows the rule
of the [Cross-Classification Mapping](../../taxonomy.md#cross-classification-mapping): pick the row at
the granularity that the source states, as decided in [#94](https://github.com/IFRCGo/monty-stac-extension/issues/94).

The comparison is not case-sensitive. The transformer writes the three codes in the order
UNDRR-ISC 2025, GLIDE, EM-DAT, for example `["MH0600", "FL", "nat-hyd-flo-flo"]`.

A hazard that is not in this table gives no item: the transformer skips all the records of
that event and counts them as failed. This includes `Mixed disasters`. The transformer has a
row for it (`mix-mix-mix-mix`), but that value has no UNDRR-ISC 2025 code, so the event fails.

### Impact Items

Each `Disaster` figure of the GIDD dataset gives one impact item. The transformer starts from a copy of the event item, and then sets the fields of the figure. So an impact item also has the `monty:corr_id`, `monty:hazard_codes`, `monty:episode_number` and `monty:src_event_id` of its event.

| STAC field                                                                                                               | GIDD field                                                  | Required | Notes                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-gidd-impact-`{Event ID}`-`{ID}`-`{figure category}    | Yes      | See [Impact item id](#impact-item-id)                                                        |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | feature geometry of the figure                              | Yes      | Direct copy. `bbox` is computed from it                                                      |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-gidd-impacts`                                         | Yes      |                                                                                              |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | {Figure category}`-`{Figure unit}`-`{Event name}            | Yes      | For example `Internal Displacements-Household-Syria, Türkiye: Earthquake - 06/02/2023`       |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | {Start date}, else {Stock date}                             | Yes      | UTC. A figure with none of the two dates makes its event fail                                |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | {Start date}, else {Stock date}                             | Yes      | UTC                                                                                          |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | {End date}, else {Stock reporting date}                     | No       | UTC                                                                                          |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#basics)                    | Generated                                                   | No       | The keywords of the hazard profile, then the country code of the figure                      |
| `figure_category`, `figure_unit`, `figure_cause`                                                                         | {Figure category}, {Figure unit}, {Figure cause}            | No       | Direct copy                                                                                  |
| `geographical_region`, `country`                                                                                         | {Geographical region}, {Country}                            | No       | Direct copy                                                                                  |
| `location`, `location_accuracy`, `location_type`, `displacement_occured`, `sources`, `publishers`                        | same fields as the event item                               | No       | From the figure, not from the first figure of the event                                      |
| `roles`                                                                                                                  | `["source", "impact"]`                                      | Yes      |                                                                                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                 | {ISO3}                                                      | Yes      | One code: the country of the figure                                                          |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail)                                 | See [Displacement Impact details](#displacement-impact-details) | Yes  |                                                                                              |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                      | {Event ID}                                                  | Yes      | The identifier of the event, not of the figure                                               |
| [processing:version](https://github.com/stac-extensions/processing)                                                      | Generated                                                   | No       | Semantic version of the transformer that generated the item, via the `processing:` extension |
| [processing:software](https://github.com/stac-extensions/processing)                                                     | Generated                                                   | No       | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension |
| `links[rel=related]`                                                                                                     | the event item                                              | Yes      | `roles: ["event"]`                                                                           |

##### Impact item id

The id is `idmc-gidd-impact-{Event ID}-{ID}-{figure category}`:

- `{Event ID}` is the identifier of the event, and `{ID}` is the identifier of the figure.
- `{figure category}` is the `Figure category` in lower case, with each space replaced by a hyphen: `Internal Displacements` gives `internal-displacements`, and `IDPs` gives `idps`. If the figure has no `Figure category`, the value is `displaced`.

Example: `idmc-gidd-impact-22194-107479-internal-displacements`.

> [!IMPORTANT]
> Before [IFRCGo/pystac-monty#268](https://github.com/IFRCGo/pystac-monty/pull/268), this doc and its examples gave the id as `idmc-gidd-impact-{ID}-displaced`. No transformer release wrote that form.

##### Displacement Impact details

The following table shows how GIDD fields map to [impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail):

| STAC field    | GIDD field        | Required | Notes                                                              |
| ------------- | ----------------- | -------- | ------------------------------------------------------------------ |
| category      | `people`          | Yes      | From the table below                                               |
| type          | {Figure category} | Yes      | From the table below. The default is `displaced_internal`          |
| value         | {Total figures}   | Yes      | Direct mapping. `Total figures` is a count of people, also when `Figure unit` is `Household` |
| unit          | `count`           | Yes      | Always `count`                                                     |
| estimate_type | `primary`         | Yes      | Always `primary`                                                   |

The `type` comes from the `Figure category`. The comparison ignores the case, and a space is equal to a hyphen:

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

The GIDD disaggregated data has two `Figure category` values today: `Internal Displacements` and `IDPs`. The two give `displaced_internal`. The other rows are in the table because GIDD and IDU share it.

> [!NOTE]
> `Internal Displacements` is a flow (movements in a period), and `IDPs` is a stock (people displaced at a date). The two map to the same `type`. The `figure_category` property and the item id keep the difference. Do not add them together.

### Examples

The examples are the output of the transformer for the reference file. Only the links are adapted to the layout of `examples/`.

- [`idmc-gidd-event-22194`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-events/idmc-gidd-event-22194.json): an event in two countries (`["SYR", "TUR"]`)
- [`idmc-gidd-impact-22194-107479-internal-displacements`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts/idmc-gidd-impact-22194-107479-internal-displacements.json): one figure of that event (193 245 people, `SYR`)
- [`idmc-gidd-impact-22194-136080-idps`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts/idmc-gidd-impact-22194-136080-idps.json): a stock figure (`IDPs`) of the same event (132 168 people, `TUR`)
- [`idmc-gidd-event-15487`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-events/idmc-gidd-event-15487.json) and [`idmc-gidd-impact-15487-107555-internal-displacements`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts/idmc-gidd-impact-15487-107555-internal-displacements.json): a flood
- [`idmc-gidd-event-15607`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-events/idmc-gidd-event-15607.json) and [`idmc-gidd-impact-15607-108364-internal-displacements`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts/idmc-gidd-impact-15607-108364-internal-displacements.json): a generic storm (`MH0301`)

In a deployment, the `related` hrefs have the form `{eoapi_url}/collections/{collection}/items/{item_id}`.

### Internal Displacement Updates (IDU)

The IDU items are documented in the [IDU source doc](../IDU/README.md). The files `idu-export.json` and `idmc-idu-samples-ESP.json` in this folder are the reference files of that source.
