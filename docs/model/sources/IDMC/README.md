# IDMC — Global Internal Displacement Database (GIDD)

The Internal Displacement Monitoring Centre (IDMC) maintains the Global Internal Displacement Database (GIDD). GIDD gives quality-controlled data on internal displacement from 2008 onwards. IDMC validates it every year.

This page describes the **GIDD** transformer (`pystac_monty/sources/gidd.py`). The IDMC **Internal Displacement Updates** (IDU) feed has its own transformer and its own page: [IDU](../IDU/README.md).

> [!NOTE]
> This page describes the transformer at [IFRCGo/pystac-monty#268](https://github.com/IFRCGo/pystac-monty/pull/268). That PR corrects the impact item id and the impact type. Until it is merged and deployed, the transformer behaves as described in [Known limitations](#known-limitations), item 1.

## Collections

| Collection          | Content                                   |
| ------------------- | ----------------------------------------- |
| `idmc-gidd-events`  | One event item for each GIDD `Event ID`   |
| `idmc-gidd-impacts` | One impact item for each GIDD disaster record |

- Source organisation: Internal Displacement Monitoring Centre (IDMC)
- Source code: IDMC
- Source type: International NGO
- Source organisation email: <info@idmc.ch>
- Source URL: <https://www.internal-displacement.org/database>
- Source data license: None stated by the source (checked 2026-07)
- Source for: event, impact
- API documentation: <https://helix-tools-api.idmcdb.org/external-api/>

## Data

- Swagger JSON URL: <https://helix-tools-api.idmcdb.org/external-api/>
- OpenAPI: <https://helix-tools-api.idmcdb.org/external-api/api-schema/>

### GIDD disaggregated data

The transformer reads the [GIDD Disaggregated Data](https://www.internal-displacement.org/database/api-documentation/#gidd-disaggregated-data). The data is disaggregated by caseload, location and event.

Endpoint: `https://helix-tools-api.idmcdb.org/external-api/gidd/disaggregations/disaggregation-geojson/?client_id=<secret>`

The response is a GeoJSON feature collection. Each feature is one displacement record, with these properties:

- `ID`: IDMC figure unique identifier
- `ISO3`: ISO 3166-1 alpha-3 country code
- `Country`: Country or territory name
- `Geographical region`: IDMC's geographical region classification
- `Figure cause`: Trigger of displacement (`Disaster`, `Conflict`, `Other`)
- `Year`: Reporting year
- `Figure category`: Type of displacement metric (`Internal Displacements`, `IDPs`, …)
- `Figure unit`: Unit of measurement (`Person`, `Household`)
- `Reported figures`: Value reported by the original source
- `Household size`: Average number of persons for each household
- `Total figures`: Total number of persons. For a `Household` figure, IDMC multiplies `Reported figures` by `Household size`
- `Hazard category`, `Hazard sub category`, `Hazard type`, `Hazard sub type`: hazard classification
- `Start date`, `End date` (and their accuracy): displacement dates, for flow figures
- `Stock date`, `Stock reporting date` (and their accuracy): dates of stock figures (`IDPs`)
- `Publishers`: Organisations that distribute the data
- `Sources`, `Sources type`: Primary data providers
- `Event ID`, `Event name`, `Event cause`, `Event main trigger`
- `Event start date`, `Event end date` (and their accuracy)
- `Is housing destruction`: Whether the displacement includes housing destruction
- `Violence type`: Category of violence (conflict records only)
- `Event codes (Code:Type)`: External reference codes (for example GLIDE numbers)
- `Locations name`, `Locations coordinates`, `Locations accuracy`, `Locations type` (`Origin` or `Destination`)
- `Displacement occurred`: Whether preventive evacuations were reported

The [GIDD Disasters Dataset](https://www.internal-displacement.org/database/api-documentation/#gidd-disasters-dataset) (`/gidd/disasters/`) is not used. Its records are not grouped by event.

## Object model

```text
GIDD Event ID ──► 1 event item   idmc-gidd-event-{Event ID}
      │
      └─ each disaster record ──► 1 impact item   idmc-gidd-impact-{Event ID}-{ID}-{figure-category}
```

The transformer groups the records by `Event ID`. Each group gives one event item and one impact item for each record in the group. GIDD has no hazard items.

**The event item is built from the first record of the group.** Each impact item starts as a copy of the event item, and then the transformer sets the record's own fields. See [Known limitations](#known-limitations), item 2.

## Data access

1. The transformer keeps only the records with `Figure cause` = `Disaster`. It skips `Conflict` and `Other` records, and it logs a warning for an unknown cause. (This filter applies to file input, which the ETL uses. Memory input is not filtered.)
2. If one record of a group fails validation, or has no `Start date` and no `Stock date`, the transformer drops the **whole group**: the event item and all its impact items.

## Event items

| STAC field                                                                                                               | GIDD field                                | Notes                                                                       |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- | --------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-gidd-event-{Event ID}`              |                                                                             |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-gidd-events`                        |                                                                             |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | feature `geometry` of the first record    | Not an aggregation of all records                                           |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                                | coordinates of the first record           |                                                                             |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                         | `Event name`                              |                                                                             |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)               | `Event start date`                        | Midnight UTC                                                                |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | `Event start date`                        | Midnight UTC                                                                |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)     | `Event end date`                          | Midnight UTC                                                                |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                      | Generated                                 | Hazard profile keywords and the country code                                |
| `location`, `location_accuracy`, `location_type`                                                                         | `Locations name`, `Locations accuracy`, `Locations type` of the first record |                                      |
| `displacement_occured`                                                                                                   | —                                         | Always `null`. See [Known limitations](#known-limitations), item 3          |
| `sources`, `publishers`                                                                                                  | `Sources`, `Publishers` of the first record |                                                                           |
| `roles`                                                                                                                  | `["source", "event"]`                     |                                                                             |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                 | `[ISO3]` of the first record              | One country only                                                            |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                   | the four `Hazard …` fields                | See [Hazard codes](#hazard-codes)                                           |
| [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number)                               | —                                         | Always `1`. GIDD has no episodes                                            |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                      | `Event ID`                                |                                                                             |
| [monty:corr_id](https://github.com/IFRCGo/monty-stac-extension#montycorr_id)                                             | Generated                                 | [Correlation identifier](../../correlation_identifier.md), dated from `Event start date` |
| [processing:version](https://github.com/stac-extensions/processing)                                                      | Generated                                 | Version of the transformer, via the `processing:` extension                 |
| [processing:software](https://github.com/stac-extensions/processing)                                                     | Generated                                 | `{"pystac-monty": "<version>"}`, via the `processing:` extension            |
| `assets.source`                                                                                                          | the source URL                            | `application/geo+json`, title `GIDD GeoJson Source`                         |
| `via` link                                                                                                               | the source URL                            | Title `GIDD Event Data`                                                     |
| `related` links                                                                                                          | Generated                                 | One for each impact item of the event, with `roles: ["impact"]`             |

## Impact items

| STAC field                                                                                                               | GIDD field                                        | Notes                                                              |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- | ------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `idmc-gidd-impact-{Event ID}-{ID}-{figure-category}` | `figure-category` is `Figure category` in lower case, with `-` for spaces. Example: `idmc-gidd-impact-22194-107479-internal-displacements` |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-gidd-impacts`                               |                                                                    |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry), [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | copied from the event item | **Not the record's own geometry.** See [Known limitations](#known-limitations), item 2 |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                         | `{Figure category}-{Figure unit}-{Figure unit}-{Event name}` | The unit appears twice. See [Known limitations](#known-limitations), item 5 |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)               | `Start date`, else `Stock date`                   | Midnight UTC                                                       |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | `Start date`, else `Stock date`                   | Midnight UTC                                                       |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)     | `End date`, else `Stock reporting date`           | Midnight UTC, or `null`                                            |
| `figure_category`, `figure_unit`, `figure_cause`, `geographical_region`, `country` | `Figure category`, `Figure unit`, `Figure cause`, `Geographical region`, `Country` | The record's own values |
| `location`, `location_accuracy`, `location_type`, `sources`, `publishers`, `keywords` | copied from the event item | Values of the first record of the event |
| `roles`                                                                                                                  | `["source", "impact"]`                            |                                                                    |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes), [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes), [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id), [monty:episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number), [monty:corr_id](https://github.com/IFRCGo/monty-stac-extension#montycorr_id) | copied from the event item | The impact item has the same `monty:corr_id` as its event |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail)                                 | See [Impact detail](#impact-detail)               |                                                                    |
| `processing:version`, `processing:software`, `assets.source`, `via` link | as on the event item |  |
| `related` link                                                                                                           | Generated                                         | To the event item, with `roles: ["event"]`                         |

### Impact detail

| Field           | Value                                                                   |
| --------------- | ----------------------------------------------------------------------- |
| `category`      | `people`                                                                |
| `type`          | From `Figure category`. See the next table                              |
| `value`         | `Total figures`. Household figures are already converted to persons by IDMC |
| `unit`          | `count`                                                                 |
| `estimate_type` | `primary`                                                               |

| `Figure category`                 | Normalised (in the id)            | `type`                |
| --------------------------------- | --------------------------------- | --------------------- |
| `Internal Displacements`          | `internal-displacements`          | `displaced_internal`  |
| `IDPs`                            | `idps`                            | `displaced_internal`  |
| `Deaths`                          | `deaths`                          | `death`               |
| `People displaced across borders` | `people-displaced-across-borders` | `displaced_external`  |
| any other value                   | normalised the same way           | `displaced_internal` (default) |

> [!WARNING]
> `Internal Displacements` is a **flow**: the number of displacement movements in a period. `IDPs` is a **stock**: the number of persons who are displaced at a date. Both map to `displaced_internal`. Do not add them together. Use `figure_category` to tell them apart.

## Hazard codes

GIDD and IDU use the same mapping function (`IDMCUtils.hazard_codes_mapping`). Its input is the four hazard fields: `(Hazard category, Hazard sub category, Hazard type, Hazard sub type)`. The table is on the IDU page: [Hazard type mapping](../IDU/README.md#hazard-type-mapping). The transformer sets hazard codes only for `Disaster` records.

## Known limitations

1. **Before [IFRCGo/pystac-monty#268](https://github.com/IFRCGo/pystac-monty/pull/268) is deployed:**
   - The impact id has no `-` between `Event ID` and `ID`. Example: `idmc-gidd-impact-22194107479-internal-displacements`. Two different pairs can give the same id.
   - Every figure category maps to `displaced_internal`. A `Deaths` record is published as displaced persons.
2. **Impact items copy the event item, and the event item comes from the first record of the event.** So an impact item has the geometry, the bbox and the location names of the first record, not its own. In the reference file, 46 of the 97 impact items have the geometry of another record. The event geometry is also the geometry of one record only, and `monty:country_codes` has one country only, even when the event covers more.
3. **`displacement_occured` is always `null`** (and the name has a spelling error). The validator has no alias for the source field `Displacement occurred`.
4. **One bad record drops the whole event.** See [Data access](#data-access), item 2.
5. **The impact title repeats the unit**, for example `Internal Displacements-Household-Household-Syria, Türkiye: Earthquake - 06/02/2023`. This question is open in [IFRCGo/pystac-monty#268](https://github.com/IFRCGo/pystac-monty/pull/268).

## Examples

Made with the GIDD transformer at [IFRCGo/pystac-monty#268](https://github.com/IFRCGo/pystac-monty/pull/268), from the reference file below. Event 22194 is the 2023 Syria and Türkiye earthquake. Its `related` links are limited to the impact items in this folder.

- [`examples/idmc-gidd-events/idmc-gidd-event-22194.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-events/idmc-gidd-event-22194.json)
- [`examples/idmc-gidd-impacts/idmc-gidd-impact-22194-107479-internal-displacements.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts/idmc-gidd-impact-22194-107479-internal-displacements.json): a flow figure, in households
- [`examples/idmc-gidd-impacts/idmc-gidd-impact-22194-136080-idps.json`](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/idmc-gidd-impacts/idmc-gidd-impact-22194-136080-idps.json): a stock figure

## Reference files

- [`IDMC_GIDD_Internal_Displacement_Disaggregated.geojson`](./IDMC_GIDD_Internal_Displacement_Disaggregated.geojson): 100 GIDD records (97 `Disaster`, 3 `Conflict`). The transformer makes 43 event items and 97 impact items from it.
- [`IDMC API documentation.pdf`](./IDMC%20API%20documentation.pdf), [`IDMC Database.pdf`](./IDMC%20Database.pdf)
