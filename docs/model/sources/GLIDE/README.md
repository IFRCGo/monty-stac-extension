# GLIDE

GLIDE is a globally common Unique ID code for disasters and emergencies. It is a unique identifier that is assigned to each disaster event by the Asian Disaster Reduction Center (ADRC).

## Collection: `glide-events`

A STAC collection hold all the GLIDE events. An example of the GLIDE collection is [here](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/glide-events/glide-events.json).

- Name: GLobal IDEntifier Number (GLIDE)
- Code: GLIDE
- Source organisation: Asian Disaster Reduction Center (ADRC)
- Source code: ADRC
- Source Type: Regional Intergovernmental Organization
- Source organization email: <gliderep@adrc.asia>
- Source URL: <https://glidenumber.net>
- Source Data license: None stated by the source (checked 2026-07)
- Source for: event, hazard

- previous implementation (R): <https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGLIDEnumber.R>

### Data

Accessible data is a set of GLIDE entries. Each entry is a disaster event. The event data list is available in the form of a array called "glideset" via the API endpoint `https://www.glidenumber.net/glide/jsonglideset.jsp`.

- Documentation: <https://glidenumber.net/glide/public/GLIDEnumber%20API.docx>

> [!IMPORTANT]
> Despite what's described in the documentation, the API endpoint `https://www.glidenumber.net/glide/jsonglideset.jsp` cannot retrieve individual events. It is necessary to add other filter to narrow down the search (e.g. h`ttps://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199`)

### Event Item

A GLIDE event and episode will **ALWAYS** produce an [**event STAC item**](https://github.com/IFRCGo/monty-stac-extension#event) as in the example for the [flood in Spain](https://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199) — provided its `event` type resolves to at least one hazard code (see the [classification-failure caveat](#classification-failure-and-item-cardinality) below).

- The source events is in the file [FL-2024-000199-ESP.json](FL-2024-000199-ESP.json) and is the output of the [`jsonglideset`](https://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199) API endpoint.
- The produced event STAC items is in the file [glide-events/FL-2024-000199-ESP.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/glide-events/FL-2024-000199-ESP.json).

The event URL of the `jsonglideset` API endpoint is stored in the `links` field of the STAC item with the `via` relation.

Here is a table with the fields that are mapped from the GDACS event to the STAC event:

| STAC field                                                                                                 | GLIDE field                                                                  | Description                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                      | event + number + geocode                                                     | Unique identifier for the event                                                                                                             |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)          | longitude + latitude as geojson POINT                                        | Geometry of the event (POINT)                                                                                                               |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)      | `glide-events`                                                               | The collection for GDACS events                                                                                                             |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)           | humaran readable from event, location, year, month, day                      | Name of the event                                                                                                                           |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)     | comments                                                                     | Description of the event. HTML description should be privileged over plain text description and translated to markdown                      |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | year + month + date                                                          | Date and time of the event converted in UTC ISO 8601 format                                                                                 |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                            | geocode (fallback: reverse-geocoded point)                                                                      | ISO3 code from `geocode`. When GLIDE reports the sentinel `---` (unresolved) and a geocoder is configured, the transformer instead reverse-geocodes the event's lat/lon point via `MontyGeoCoder.get_iso3_from_point`. If no geocoder is configured, `monty:country_codes` is an empty list; if a geocoder is configured but the point does not resolve to any country, the list is `[null]`. `keywords` is always built from the raw `geocode` value (e.g. `---`), even when `monty:country_codes` was reverse-geocoded — the two fields can diverge                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                         | geocode                                                                      | List of ISO3 codes of the other countries affected by the event                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | event                                                                        | List of hazard codes converted following the [GLIDE event type to Hazard profile mapping](#mapping-from-glide-event-type-to-hazard-profile) |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                    | `https://www.glidenumber.net/glide/public/search/details.jsp?glide=` + docid | Asset with the link to the GDACS report                                                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]           | source url                                                                   | Link to the GDACS event details page                                                                                                        |
| [processing:version](https://github.com/stac-extensions/processing) | Generated | Semantic version of the transformer that generated the item, via the `processing:` extension |
| [processing:software](https://github.com/stac-extensions/processing) | Generated | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension |

### Hazard Item

A GLIDE event and episode will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard) as in the example for the [flood in Spain](https://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199) — subject to the same classification-failure caveat as the event item.

- The source events is in the file [FL-2024-000199-ESP.json](FL-2024-000199-ESP.json) and is the output of the [`jsonglideset`](https://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199) API endpoint.
- The produced hazard STAC item is in the examples [glide-hazards/FL-2024-000199-ESP.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/glide-hazards/FL-2024-000199-ESP.json).

Here is a table with the STAC fields that are mapped from the GDACS event to the STAC hazard:

| STAC field                                                                                                 | GLIDE field                                                                  | Description                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                      | event + number + geocode                                                     | Unique identifier for the event                                                                                                             |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)          | longitude + latitude as geojson POINT                                        | Geometry of the event (POINT)                                                                                                               |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)      | `glide-events`                                                               | The collection for GDACS events                                                                                                             |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)           | humaran readable from event, location, year, month, day                      | Name of the event                                                                                                                           |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)     | comments                                                                     | Description of the event. HTML description should be privileged over plain text description and translated to markdown                      |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | year + month + date                                                          | Date and time of the event converted in UTC ISO 8601 format                                                                                 |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                            | geocode (fallback: reverse-geocoded point)                                                                      | ISO3 code from `geocode`. When GLIDE reports the sentinel `---` (unresolved) and a geocoder is configured, the transformer instead reverse-geocodes the event's lat/lon point via `MontyGeoCoder.get_iso3_from_point`. If no geocoder is configured, `monty:country_codes` is an empty list; if a geocoder is configured but the point does not resolve to any country, the list is `[null]`. `keywords` is always built from the raw `geocode` value (e.g. `---`), even when `monty:country_codes` was reverse-geocoded — the two fields can diverge                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                         | geocode                                                                      | List of ISO3 codes of the other countries affected by the event                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | event                                                                        | List of hazard codes converted following the [GLIDE event type to Hazard profile mapping](#mapping-from-glide-event-type-to-hazard-profile) |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                    | `https://www.glidenumber.net/glide/public/search/details.jsp?glide=` + docid | Asset with the link to the GDACS report                                                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]           | source url                                                                   | Link to the GDACS event details page                                                                                                        |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail)                                               | ?                                                                            | Detailed description of the hazard (more details in next section)                                                                           |
| [processing:version](https://github.com/stac-extensions/processing) | Generated | Semantic version of the transformer that generated the item, via the `processing:` extension |
| [processing:software](https://github.com/stac-extensions/processing) | Generated | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension |

#### Hazard Detail

The [hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) field is a JSON object that contains the detailed information about the hazard. The object is a mapping of the hazard codes to the detailed information. The detailed information is a JSON object with the following fields:

| STAC field     | GLIDE field | Description            |
| -------------- | ----------- | ---------------------- |
| clusters       | event       | Hazard clusters codes  |
| severity_unit  | `glide`     | GLIDE alert level      |
| severity_value | magnitude   | Magnitude of the event |

##### Mapping from GLIDE event type to Hazard profile

There is not straightforward mapping from the GLIDE event type to the [hazard profile](../../taxonomy.md#2025-update). Most GLIDE `event` types resolve to a fixed UNDRR-ISC 2025 / EM-DAT / GLIDE triple in `GlideTransformer.get_hazard_codes`:

| GLIDE event type               | Hazard profile cluster (2025) | Hazard Profile codes (2025) |
| ------------------------------ | ----------------------------- | --------------------------- |
| **CW** (Cold Wave)             | `MH-TEMP`                     | `MH0502` (Cold Wave)        |
| **DR** (Drought)               | `MH-PRECIP`                   | `MH0401` (Drought)          |
| **EQ** (Earthquake)            | `GEO-SEIS`                    | `GH0101` (Earthquake)       |
| **EP** (Epidemic)              | `BIO-INFECT`                  | `BI0101` (Infectious Diseases, general) |
| **EC** (Extratropical Cyclone) | `MH-WIND`                     | `MH0307` (Extra-tropical Cyclone) |
| **FR** (Fire)                  | `TECH-INDFAIL`                | `TL0305` (Fire)             |
| **FF** (Flash Flood)           | `MH-WATER`                    | `MH0603` (Flash Flooding)   |
| **FL** (Flood)                 | `MH-WATER`                    | `MH0600` (Flooding chapeau) |
| **HT** (Heat Wave)             | `MH-TEMP`                     | `MH0501` (Heatwave)         |
| **LS** (Land Slide)            | `GEO-GFAIL`                   | `GH0300` (Gravitational Mass Movement) |
| **MS** (Mud Slide)             | `GEO-GFAIL`                   | `GH0303` (Flows)            |
| **ST** (Storm)                 | `MH-CONV`                     | `MH0102` (Lightning (electrical storm)) |
| **TC** (Tropical Cyclone)      | `MH-WIND`                     | `MH0309` (Tropical Cyclone) |
| **TS** (Tsunami)               | `MH-MARINE`                   | `MH0705` (Tsunami)          |
| **TO** (Tornado)                | `MH-WIND`                     | `MH0305` (Tornado)          |
| **AV** (Avalanche)             | `MH-TERR`                     | `MH0801` (Avalanche)        |
| **SS** (Storm Surge)           | `MH-MARINE`                   | `MH0703` (Storm Surge)      |
| **VW** (Violent Wind)          | `MH-WIND`                     | `MH0301` (Wind)             |
| **VO** (Volcano)               | `GEO-VOLC`                    | `GH0201` (Lava Flows — the general/unspecified-eruption stand-in, see the [volcanic note](../IFRC-DREF/README.md#hazard-type-mapping) on why HIP 2025 has no volcanic chapeau) |
| **WF** (Wild Fire)             | `ENV-FOREST`                  | `EN0205` (Wildfires)        |

`SL` (Slide) and `WV` (Wave/Surge) are not looked up directly: `get_hazard_codes` remaps `SL` to `LS` and `WV` to `SS` before the table lookup above, so both resolve to the same codes as their target row.

More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added to the `codes` field following the characteristics of the event.

> [!WARNING]
> **`IN` (Insect Infestation) has no mapping.** It is a valid GLIDE `event` value (the source validator accepts it), but it is not a key in `get_hazard_codes`'s mapping table, so it falls through to an empty `hazard_codes` list — which is the classification-failure case described [below](#classification-failure-and-item-cardinality). No `IN` event has ever produced a STAC item.

###### `AC` (Accident): sub-classified from `comments`

GLIDE's `AC` type covers several distinct technological hazards (transport accidents, industrial fires, explosions, structural collapses, etc.), so `get_hazard_codes` routes it to `get_ac_hazard_codes(comments)` instead of a static row. That method tries two strategies, in order:

1. **Structured tag.** If `comments` ends with a parenthesised tag such as `(Road)` or `(Ind: Gas leak)`, the category (and optional `Category: Subcategory`) is looked up in a fixed table:

   | Tag key               | Hazard Profile codes (2025) |
   | ---------------------- | ---------------------------- |
   | `road`                 | `TL0405` (Road Traffic Accident) |
   | `rail`                 | `TL0404` (Rail Accident)     |
   | `water`                | `TL0402` (Inland Water Way Accidents) |
   | `air`                  | `TL0401` (Air Transportation Accident) |
   | `misc:fire`, `ind:fire`         | `TL0305` (Fire)     |
   | `misc:explosion`, `ind:explosion` | `TL0304` (Explosion) |
   | `misc:collapse`, `ind:collapse`  | `TL0201` (Building Collapse) |
   | `ind:gas leak`, `ind:chemical spill` | `TL0301` (Leaks and Spills) |
   | `ind:other`            | `TL0207` (Critical Infrastructure Failure) |

   `misc:other` is deliberately absent — it covers cases like stampedes and poisonings that have no clear technological hazard code.

2. **Free-text fallback.** If there is no recognised tag (or its key isn't in the table above), `comments` is matched against a series of keyword regexes for aircraft/ship/train/road-vehicle accidents, structural collapse, explosion, and fire, in that order, each mapping to the same codes as the table above.

   If neither strategy matches, `get_ac_hazard_codes` returns an empty list — see the [classification-failure caveat](#classification-failure-and-item-cardinality) below.

###### `ET` (Extreme Temperature): sub-classified from `comments`

`ET` has no row of its own in `HazardProfiles.csv` — GLIDE conflates what UNDRR-ISC 2025 splits into Heatwave (`MH0501`/`HT`) and Cold Wave (`MH0502`/`CW`) — so `get_hazard_codes` routes it to `get_et_hazard_codes(comments)`, which uses the same two-strategy approach as `AC`: a trailing tag (`(cold wave)` or `(heat wave)`) looked up first, then a free-text `heat wave` / `cold wave` regex fallback. If neither matches, it also returns an empty list.

###### Classification failure and item cardinality

`make_source_event_items` calls `get_hazard_codes` and then immediately overwrites the result with `hazard_profiles.get_canonical_hazard_codes(item)`, which raises `ValueError` if the item carries no hazard codes at all. Both `get_stac_items_from_file` and `get_stac_items_from_memory` catch that exception per-row, log a warning, and increment the failed-row counter — they do **not** yield an event or hazard item for that row. In practice this means:

- Every `IN` record is dropped (no mapping exists at all).
- An `AC` or `ET` record is dropped if its `comments` field carries neither a recognisable tag nor a matching free-text keyword.
- Every other GLIDE `event` type always produces its event/hazard item pair, since its codes are a fixed, non-empty triple.

> [!NOTE]
> **`FR` is not the wildfire code — `WF` is.** GLIDE's vocabulary carries both
> (`FR - Fire`, `WF - Wild fire`), and it flags its deprecated types explicitly
> (`FA - Famine(use other HAZARD instead)`, `SL - SLIDE (use LS/AV/MS instead)`,
> `WV - Wave/Surge(use TS/SS instead)`); `FR` carries no such flag, so both are
> live. GLIDE publishes no definition beyond those labels, but its records show
> what `FR` is used for: settlement, structural and camp fires — the Kočani
> nightclub (`FR-2025-000034-MKD`), the Cox's Bazar refugee camp
> (`FR-2023-000031-BGD`), Hargeisa's main market (`FR-2022-000191-SOM`),
> Sandakan (`FR-2026-000064-MYS`) — against `WF` records that are consistently
> vegetation fires, many of them GDACS-fed. That is EM-DAT's `tec-mis-fir-fir`
> (Fire, Miscellaneous) as much as `tec-ind-fir-fir` (Fire, Industrial), and
> [both resolve to `TL0305`](../../taxonomy.md#cross-classification-mapping)
> despite the cluster's *Industrial Failure* name. A few `FR` records are
> vegetation fires that should have been coded `WF` at the source; the mapping
> follows the vocabulary, not the miscodings.

##### Hazard Magnitude and Units

?
