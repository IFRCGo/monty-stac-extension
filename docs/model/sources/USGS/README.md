# USGS Earthquake Catalog

The United States Geological Survey (USGS) Earthquake Hazards Program provides comprehensive earthquake data through their public API. The service offers real-time and historical earthquake information globally, with the most complete coverage for the United States.

## Collection: `usgs-events`

A STAC collection holds all the USGS earthquake events. An example of the USGS collection will be provided in examples/usgs-events/usgs-events.json.

- Name: USGS Earthquake Catalog
- Code: `USGS`
- Source organisation: United States Geological Survey
- Source code: USGS
- Source Type: National Government
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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                               | Derived from coordinates, with a losses-based fallback   | ISO3 code of the country where the event occurred (see note below)    |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | Fixed as earthquake        | Always `GEO-SEIS` for cluster and `GH0101` for code (see [Hazard Type Mapping](#hazard-type-mapping))  |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                      | properties.url             | Link to the USGS event details page                  |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |
| `related` link in [links]                                                                                    | Reference event item       | Link to reference event item with `roles: ["event"]` |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id) | Generated | Generated following the [event correlation](../../correlation_identifier.md) convention |

> [!NOTE]
> `monty:country_codes` first tries to find the country from the epicenter coordinates. If that lookup
> fails, the transformer picks the country with the highest total fatalities in the PAGER losses data.
> If both methods fail, the code is `UNK`.

> [!NOTE]
> `monty:corr_id` is generated **deterministically from this event's own fields** and is intended for
> intra-source pairing / exact lookups. It is **not** a reliable cross-source join key — to find the
> same event in GLIDE, GDACS, EM-DAT, etc., use the
> [dynamic STAC correlation algorithms](../../stac-api/correlation_algorithms.md#overview) rather than
> matching on `corr_id`.

#### Hazard Type Mapping

USGS (United States Geological Survey) exclusively tracks seismic events. The **2025 UNDRR-ISC** code is the **reference classification** for the Monty extension:

| USGS Type  | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Cluster  | Description  |
| ---------- | ----- | --------------- | ------------------------------ | -------- | ------------ |
| Earthquake | EQ    | nat-geo-ear-gro | **GH0101**                     | GEO-SEIS | Earthquake   |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. The 2025 update consolidated multiple earthquake-related HIPs (including tsunami, ground shaking, liquefaction, etc.) into a single Earthquake HIP (GH0101). While USGS data may include tsunami-related events through the `properties.tsunami` field, the primary hazard code remains GH0101 for all earthquake events.

This mapping ensures standardized hazard categorization for seismic events from the USGS Earthquake Catalog.

Additional external links produced for USGS events (not STAC item relationships):

- [`related` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) with `properties.url + "/map"`: Link to the USGS interactive map for this event (external resource, not a STAC item relationship)
- [`related` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) with `properties.url + "/region"`: Link to the USGS regional information for this event (external resource, not a STAC item relationship)

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                               | Inherited from the event            | Same country code as the event — the hazard item is a clone of the event item |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | Inherited from the event            | Always `GEO-SEIS` for cluster and `GH0101` for code — same trio as the event (inherited) |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                      | properties.url                      | Link to the USGS hazard details page                |
| `related` link in [links]                                                                                    | Event item                           | Link to source event item with `roles: ["event"]` |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail)                                               | properties.mag, properties.magType  | Detailed description of the hazard                  |
| [`assets`](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                        | [ShakeMap assets](#shakemap-assets) | Assets from the USGS ShakeMap product               |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |

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

The [PAGER product](https://earthquake.usgs.gov/data/pager/) (Prompt Assessment of Global Earthquakes for Response) of a USGS earthquake event carries two content files that hold loss estimates. They are different kinds of estimate and are mapped differently:

| PAGER content file | What it holds                                                           | Monty mapping                                                               |
| ------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `json/losses.json` | One deterministic modelled total per type, plus a per-country breakdown | Mapped below — the Estimated Fatalities and Estimated Economic Losses items |
| `json/alerts.json` | A probability histogram (a set of alert bins) per type                  | See [Alert data](#alert-data-alertsjson) — representation under review      |

The `losses.json` mapping produces two [**impact STAC items**](https://github.com/IFRCGo/monty-stac-extension#impact) per country:

1. Estimated Fatalities Impact. Examples: [us6000pi9w-fatalities.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000pi9w-fatalities.json), [us6000tjl2-fatalities.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000tjl2-fatalities.json)
2. Estimated Economic Losses Impact. Examples: [us6000pi9w-economic.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000pi9w-economic.json), [us6000tjl2-economic.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000tjl2-economic.json)

The PAGER data is found in the `losspager` product within the USGS event data. Here is a detailed mapping of fields from the USGS PAGER data to the STAC impacts:

| STAC field                                                                                                 | USGS field                        | Source Location & Details                                                                        |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                      | id + "-fatalities" or "-economic" | Append "-fatalities" or "-economic" to the event's properties.id                                 |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                  | bbox                              | Use the event's bbox directly                                                                    |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)          | geometry                          | Use the event's geometry (earthquake epicenter) directly                                         |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)      | `usgs-impacts`                    | Fixed value for all USGS impact items                                                            |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | properties.time                   | Found in event's properties.time, convert from Unix timestamp to ISO 8601                        |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                                               | Derived from coordinates          | Use reverse geocoding on event's geometry.coordinates[0,1] to get ISO3 country code              |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | Fixed as earthquake               | Always `GEO-SEIS` for cluster and `GH0101` for code — same trio as the event (inherited)         |
| [roles](https://github.com/IFRCGo/monty-stac-extension#roles)                                                                          | ["impact", "source"]              | Always `["impact", "source"]` for USGS impact items                                             |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)           | Derived                           | "Estimated Fatalities" or "Estimated Economic Losses" based on impact type                       |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)     | Derived                           | Combine event location and impact type, e.g. "Estimated fatalities for {event.properties.place}" |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |
| `related` link in [links]                                                                                    | Event item                        | Link to source event item with `roles: ["event"]` |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id) | Generated | Generated following the [event correlation](../../correlation_identifier.md) convention |

#### Impact Detail

The [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) field contains specific information about each type of impact.
The values are extracted from the PAGER product data in the USGS event and requires to get an additional content file from the USGS event data
under `json/losses.json`.

For Estimated Fatalities:

```json
{
  "category": "people",
  "type": "death",
  "value": "<from products.losspager.contents['json/losses.json'].empirical_fatality.total_fatalities>",
  "unit": "people",
  "estimate_type": "modelled"
}
```

For Estimated Economic Losses:

```json
{
  "category": "buildings",
  "type": "cost",
  "value": "<from products.losspager.contents['json/losses.json'].empirical_economic.total_dollars>",
  "unit": "usd",
  "estimate_type": "modelled"
}
```

`category` and `type` **MUST** be values from the Monty taxonomy — the
[exposure category](../../taxonomy.md#exposure-category) and
[impact type](../../taxonomy.md#impact-type) tables — not PAGER's own internal codes.

#### Alert data (`alerts.json`)

Besides the deterministic totals in `losses.json`, the `losspager` product carries
`json/alerts.json`. For each type (`fatality`, `economic`) it holds a **probability
histogram**: an ordered set of bins, each `{color, min, max, probability}`, whose
probabilities sum to 1.0. It is the source behind PAGER's headline alert level.

Reference fixtures for the 2026-08-10 M7.4 Colombia earthquake (`us6000tjl2`):
[us6000tjl2-alerts.json](us6000tjl2-alerts.json) and [us6000tjl2-losses.json](us6000tjl2-losses.json).
The two files describe the same event and do not agree on a single number, because they
do not answer the same question: `losses.json` gives one modelled total (961 fatalities),
while `alerts.json` gives the spread of possible outcomes around it.

> [!WARNING]
> For the **economic** type, the bin values are denominated in **millions of USD**,
> even though `alerts.json` labels the field `"units": "USD"`. This is verified against
> PAGER's own published alert thresholds — yellow ≥ \$1M, orange ≥ \$100M, red ≥ \$1B
> ([PAGER Scientific Background](https://earthquake.usgs.gov/data/pager/background.php)):
> the `100`–`1000` bin is colored `orange` in the reference fixture, which only agrees
> with that threshold table if the bin is read as \$100M–\$1B. A transformer that copies
> the source `"units"` string through to `monty:impact_detail.unit` therefore understates
> the value by a factor of one million. The **fatality** type has no such ambiguity: its
> bins and its `"units": "fatalities"` label are both plain counts of people.

That unit correction holds whatever shape the items eventually take.

##### Mapping: one impact item per bin

Emit **one impact item per bin**, not one collapsed value per type. Collapsing the
histogram to a single number discards the information that makes it useful:
anticipatory-action triggers (IFRC DREF) need the spread so they can evaluate their own
threshold, for example *P(economic loss > \$1B)*.

Each bin item reuses the same `category`/`type`/`unit` as the `losses.json` point
estimate above, and adds the range and its probability:

```json
{
  "category": "people",
  "type": "death",
  "value": 550,
  "value_min": 100,
  "value_max": 1000,
  "probability": 0.32364736950411177,
  "unit": "people",
  "estimate_type": "modelled",
  "description": "PAGER alert-level color: orange"
}
```

| Field                     | Fatality bin      | Economic bin                       |
| ------------------------- | ----------------- | ---------------------------------- |
| `category`                | `people`          | `global_currency`                  |
| `type`                    | `death`           | `cost`                             |
| `unit`                    | `people`          | `usd_millions` (see warning above) |
| `value`                   | bin midpoint      | bin midpoint                       |
| `value_min` / `value_max` | bin `min` / `max` | bin `min` / `max`                  |
| `probability`             | bin `probability` | bin `probability`                  |
| `estimate_type`           | `modelled`        | `modelled`                         |

Item `id` is `{event_id}-{fatality|economic}-alert-{iso3}-{bin}`, where `{bin}` is a
2-digit 1-based index in the order `alerts.json` lists its bins. `alerts.json` carries no
country breakdown of its own, so `{iso3}` is the event's resolved country.

Worked examples for `us6000tjl2`:
[fatality bins 01–07](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000tjl2-fatality-alert-COL-01.json)
and [economic bins 01–07](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/usgs-impacts/us6000tjl2-economic-alert-COL-01.json).

Three rules follow from this shape:

- **`value` is a representative point, not a claim of precision.** A consumer that needs
  the real interval, or an exceedance probability, must read `value_min`/`value_max`/`probability`
  — never `value` alone.
- **`type` is not `potentially_affected`.** A bin is still fundamentally a death or cost
  estimate; the uncertainty is carried by the added fields, not by a different `type`.
  `potentially_affected` describes population exposure and already carries other meanings
  elsewhere in Monty (see [Discussion #110](https://github.com/IFRCGo/monty-stac-extension/discussions/110)).
- **`estimate_type` stays `modelled`,** as for the point estimates. This is still a PAGER
  model output, expressed as a distribution rather than a single value.

> [!NOTE]
> `value_min`, `value_max` and `probability` are provisional additions to
> `monty:impact_detail`, under review in
> [#127](https://github.com/IFRCGo/monty-stac-extension/issues/127). The wider question of
> whether a probability distribution — and exposure data generally — belongs in the Impact
> class at all is open in
> [Discussion #110](https://github.com/IFRCGo/monty-stac-extension/discussions/110).
