# USGS Earthquake Catalog

The United States Geological Survey (USGS) Earthquake Hazards Program provides comprehensive earthquake data through their public API. The service offers real-time and historical earthquake information globally, with the most complete coverage for the United States.

## Collection: `usgs-events`

A STAC collection holds all the USGS earthquake events. An example of the USGS collection will be provided in examples/usgs-events/usgs-events.json.

- Name: USGS Earthquake Catalog
- Code: `USGS`
- Source organisation: United States Geological Survey
- Source code: USGS
- Source Type: National Government Organization
- Source organization email: <earthquakeinfo@usgs.gov>
- Source URL: <https://earthquake.usgs.gov>
- Source Data license: [Public Domain](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits)
- Source for: event, hazard

### Data

The USGS Earthquake Catalog provides earthquake data through various feeds and APIs. The data is available in multiple formats including GeoJSON, CSV, and KML.

#### GeoJSON Summary Feeds

Real-time feeds are available at different time intervals:

- Past hour: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson>
- Past day: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson>
- Past 7 days: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson>
- Past 30 days: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson>

Magnitude filters are also available:

- M1.0+ earthquakes
- M2.5+ earthquakes
- M4.5+ earthquakes
- Significant earthquakes

#### Query API

The USGS provides a comprehensive GeoJSON/API feed:

- Documentation: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php>

The feed provides real-time access to earthquake data in GeoJSON format. Each event (feature) in the feed contains:

- Detailed event metadata (time, location, magnitude, etc.)
- Geographic information (coordinates, depth)
- Impact data (felt reports, damage estimates)
- Links to additional resources (event page, maps, technical data)
- Real-time updates and revisions

More detailed information about a specific event can be accessed using the detail API endpoint:

```console
https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/<event_id>.geojson
```

where `<event_id>` is the unique identifier of the event. This endpoint provides comprehensive information including:

- Detailed event parameters
- PAGER impact estimates
- ShakeMap data
- Moment tensor solutions
- Felt reports and testimonials

Example of a detailed event feed: [us6000pi9w.geojson](us6000pi9w.geojson)

#### Products

The USGS can provide several products for each earthquake event.
The following supported ones are linked to the section where the information must be transformed into a STAC item.

- [ShakeMap](#hazard-item-from-shakemap): A map of ground shaking intensity. This product is the base for the related hazard item.
- [Pager](#impact-items-from-pager) : Prompt Assessment of Global Earthquakes for Response. This product provides estimates of the impact of the earthquake on human life and the economy. This product is the base for the related impact items.

### Event Item

A USGS earthquake event will **ALWAYS** produce an [**event STAC item**](https://github.com/IFRCGo/monty-stac-extension#event).

Example of generated STAC item: [examples/usgs-events/us6000pi9w.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-events/us6000pi9w.json)

Here is a table with the fields that are mapped from the USGS event to the STAC event:

| STAC field                                                                                                 | USGS field                 | Description                                          |
| ---------------------------------------------------------------------------------------------------------- | -------------------------- | ---------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                      | id                         | Unique identifier for the event                      |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                  | bbox                       | Bounding box of the event                            |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)          | geometry                   | Point geometry of the earthquake epicenter           |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)      | `usgs-events`              | The collection for USGS events                       |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)           | properties.title           | Title of the event                                   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)     | properties.place           | Description of the event location                    |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | properties.time            | Time of the event in UTC ISO 8601 format             |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                               | Derived from coordinates   | ISO3 code of the country where the event occurred    |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | Fixed as earthquake        | Always `GEO-SEIS` for cluster and `GH0101` for code (2025: Earthquake)  |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                      | properties.url             | Link to the USGS event details page                  |
| [`related` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                  | properties.url + "/map"    | Link to the USGS interactive map for this event      |
| [`related` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                  | properties.url + "/region" | Link to the USGS regional information for this event |

### Hazard Item (from ShakeMap)

The [Shakemap product](https://earthquake.usgs.gov/data/shakemap/) of a USGS earthquake event will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard) that implements the [STAC Earthquake Extension](https://github.com/stac-extensions/earthquake).

Example of generated STAC item: [examples/usgs-hazards/us6000pi9w-shakemap.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-hazards/us6000pi9w-shakemap.json)

Here is a table with the STAC fields that are mapped from the USGS event to the STAC hazard:

| STAC field                                                                                                 | USGS field                          | Description                                         |
| ---------------------------------------------------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                      | id + `-shakemap`                    | Unique identifier for the hazard                    |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                  | bbox                                | Bounding box of the hazard                          |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)          | geometry                            | Point geometry of the earthquake epicenter          |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)      | `usgs-hazards`                      | The collection for USGS hazards                     |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)           | properties.title                    | Title of the hazard                                 |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)     | properties.place                    | Description of the hazard location                  |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | properties.time                     | Time of the hazard in UTC ISO 8601 format           |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                               | Derived from coordinates            | ISO3 code of the country where the hazard occurred  |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | Fixed as earthquake                 | Always `GEO-SEIS` for cluster and `GH0101` for code (2025: Earthquake) |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                      | properties.url                      | Link to the USGS hazard details page                |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail)                                               | properties.mag, properties.magType  | Detailed description of the hazard                  |
| [`assets`](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                        | [ShakeMap assets](#shakemap-assets) | Assets from the USGS ShakeMap product               |

#### ShakeMap Assets

The following assets from the USGS ShakeMap product are included:

| Asset Key         | USGS Source                                               | Description                               |
| ----------------- | --------------------------------------------------------- | ----------------------------------------- |
| intensity_map     | products.shakemap.contents.download/intensity.jpg         | Intensity map showing MMI values          |
| intensity_overlay | products.shakemap.contents.download/intensity_overlay.png | Transparent intensity overlay for mapping |
| pga_map           | products.shakemap.contents.download/pga.jpg               | Peak Ground Acceleration (PGA) map        |
| pgv_map           | products.shakemap.contents.download/pgv.jpg               | Peak Ground Velocity (PGV) map            |
| mmi_contours      | products.shakemap.contents.download/cont_mi.json          | MMI contours in GeoJSON format            |
| grid              | products.shakemap.contents.download/grid.xml              | Complete grid of ground motion values     |
| uncertainty       | products.shakemap.contents.download/uncertainty.xml       | Grid of uncertainty values                |
| stations          | products.shakemap.contents.download/stationlist.json      | List of seismic stations and observations |
| rupture           | products.shakemap.contents.download/rupture.json          | Fault rupture information                 |

#### Earthquake Extension Fields

The following fields from the [STAC Earthquake Extension](https://github.com/stac-extensions/earthquake) are used:

| STAC field        | USGS field         | Description                                                                                      |
| ----------------- | ------------------ | ------------------------------------------------------------------------------------------------ |
| eq:magnitude      | properties.mag     | The magnitude value of the earthquake                                                            |
| eq:magnitude_type | properties.magType | The type of magnitude measurement (e.g., "ml" for local magnitude, "mb" for body wave magnitude) |
| eq:depth          | properties.depth   | Depth of the earthquake in kilometers                                                            |
| eq:status         | properties.status  | Status of the event (reviewed, automatic)                                                        |
| eq:tsunami        | properties.tsunami | Whether a tsunami was generated (0 = no, 1 = yes)                                                |
| eq:significance   | properties.sig     | A number that describes how significant the event is (used to prioritize event display)          |
| eq:alert          | properties.alert   | The alert level from the PAGER earthquake impact scale (green, yellow, orange, red)              |

#### Hazard Detail

The [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) field contains detailed information about the earthquake:

| Field          | USGS field         | Description                                                                                  |
| -------------- | ------------------ | -------------------------------------------------------------------------------------------- |
| clusters       | Fixed value        | Always `GEO-SEIS`                                                                            |
| severity_value | properties.mag     | Magnitude of the earthquake                                                                  |
| severity_unit  | properties.magType | Type of magnitude measurement (e.g., "ml" for local magnitude, "mb" for body wave magnitude) |

### Impact Items (from PAGER)

The [PAGER product](https://earthquake.usgs.gov/data/pager/) (Prompt Assessment of Global Earthquakes for Response) of a USGS earthquake event will produce two [**impact STAC items**](https://github.com/IFRCGo/monty-stac-extension#impact):

1. Estimated Fatalities Impact. Example of generated STAC item: [examples/usgs-impacts/us6000pi9w-fatalities.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000pi9w-fatalities.json)
2. Estimated Economic Losses Impact. Example of generated STAC item: [examples/usgs-impacts/us6000pi9w-economic.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000pi9w-economic.json)

The PAGER data is found in the `losspager` product within the USGS event data. Here is a detailed mapping of fields from the USGS PAGER data to the STAC impacts:

| STAC field                                                                                                 | USGS field                        | Source Location & Details                                                                        |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                      | id + "-fatalities" or "-economic" | Append "-fatalities" or "-economic" to the event's properties.id                                 |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                  | bbox                              | Use the event's bbox directly                                                                    |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)          | geometry                          | Use the event's geometry (earthquake epicenter) directly                                         |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)      | `usgs-impacts`                    | Fixed value for all USGS impact items                                                            |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | properties.time                   | Found in event's properties.time, convert from Unix timestamp to ISO 8601                        |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                               | Derived from coordinates          | Use reverse geocoding on event's geometry.coordinates[0,1] to get ISO3 country code              |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | [`GEO-SEIS`]                      | Always `GEO-SEIS` for all earthquake impacts                                                     |
| [roles](https://github.com/IFRCGo/monty-stac-extension#roles)                                                                          | ["impact", "source"]              | Always `["impact"]` for all impact items                                                         |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)           | Derived                           | "Estimated Fatalities" or "Estimated Economic Losses" based on impact type                       |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)     | Derived                           | Combine event location and impact type, e.g. "Estimated fatalities for {event.properties.place}" |

#### Impact Detail

The [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) field contains specific information about each type of impact. 
The values are extracted from the PAGER product data in the USGS event and requires to get an additional content file from the USGS event data
under `json/losses.json`.

For Estimated Fatalities:

```json
{
  "category": "expspec_allpeop",
  "type": "imptypdeat",
  "value": "<from products.losspager.contents['json/losses.json'].empirical_fatality.total_fatalities>",
  "unit": "people",
  "estimate_type": "modelled"
}
```

For Estimated Economic Losses:

```json
{
  "category": "expspec_build",
  "type": "imptypcost", 
  "value": "<from products.losspager.contents['json/losses.json'].empirical_economic.total_dollars>",
  "unit": "usd",
  "estimate_type": "modelled"
}
```
