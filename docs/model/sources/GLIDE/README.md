# GLIDE

GLIDE is a globally common Unique ID code for disasters and emergencies. It is a unique identifier that is assigned to each disaster event by the Asian Disaster Reduction Center (ADRC).

## Collection: `glide-events`

A STAC collection hold all the GLIDE events. An example of the GLIDE collection is [here](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/glide-events/glide-events.json).

- Name: GLobal IDEntifier Number (GLIDE)
- Code: GLIDE
- Source organisation: Asian Disaster Reduction Center (ADRC)
- Source code: ADRC
- Source Type: Regional Intergovernmental Organisation
- Source organization email: <gliderep@adrc.asia>
- Source URL: <https://glidenumber.net>
- Source Data license: ?
- Source for: event, hazard

- previous implementation (R): <https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGLIDEnumber.R>

### Data

Accessible data is a set of GLIDE entries. Each entry is a disaster event. The event data list is available in the form of a array called "glideset" via the API endpoint `https://www.glidenumber.net/glide/jsonglideset.jsp`.

- Documentation: <https://glidenumber.net/glide/public/GLIDEnumber%20API.docx>

> [!IMPORTANT]
> Despite what's described in the documentation, the API endpoint `https://www.glidenumber.net/glide/jsonglideset.jsp` cannot retrieve individual events. It is necessary to add other filter to narrow down the search (e.g. h`ttps://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199`)

### Event Item

A GLIDE event and episode will **ALWAYS** produce an [**event STAC item**](https://github.com/IFRCGo/monty-stac-extension#event) as in the example for the [flood in Spain](https://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199).

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                            | geocode                                                                      | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                         | geocode                                                                      | List of ISO3 codes of the other countries affected by the event                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | event                                                                        | List of hazard codes converted following the [GLIDE event type to Hazard profile mapping](#mapping-from-glide-event-type-to-hazard-profile) |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                    | `https://www.glidenumber.net/glide/public/search/details.jsp?glide=` + docid | Asset with the link to the GDACS report                                                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]           | source url                                                                   | Link to the GDACS event details page                                                                                                        |

### Hazard Item

A GLIDE event and episode will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard) as in the example for the [flood in Spain](https://www.glidenumber.net/glide/jsonglideset.jsp?level1=ESP&fromyear=2024&toyear=2024&events=FL&number=2024-000199).

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                            | geocode                                                                      | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                         | geocode                                                                      | List of ISO3 codes of the other countries affected by the event                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                 | event                                                                        | List of hazard codes converted following the [GLIDE event type to Hazard profile mapping](#mapping-from-glide-event-type-to-hazard-profile) |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                    | `https://www.glidenumber.net/glide/public/search/details.jsp?glide=` + docid | Asset with the link to the GDACS report                                                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]           | source url                                                                   | Link to the GDACS event details page                                                                                                        |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail)                                               | ?                                                                            | Detailed description of the hazard (more details in next section)                                                                           |

#### Hazard Detail

The [hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) field is a JSON object that contains the detailed information about the hazard. The object is a mapping of the hazard codes to the detailed information. The detailed information is a JSON object with the following fields:

| STAC field     | GLIDE field | Description            |
| -------------- | ----------- | ---------------------- |
| clusters       | event       | Hazard clusters codes  |
| severity_unit  | `glide`     | GLIDE alert level      |
| severity_value | magnitude   | Magnitude of the event |

##### Mapping from GLIDE event type to Hazard profile

There is not straightforward mapping from the GDACS event type to the [hazard profile](../../taxonomy.md#undrr-isc-2020-hazard-information-profiles). The current mapping only considers
setting the clusters field as the following:

| GLIDE event type               | Hazard profile cluster | Hazard Profile codes |
| ------------------------------ | ---------------------- | -------------------- |
| **CW** (Cold Wave)             | `HM-TEMP`              | `MH0040`             |
| **CE** (Complex Emergency)     |                        |                      |
| **DR** (Drought)               | `HM-PRECIP`            | `MH0035`             |
| **EQ** Eartquake**             | `GEO-SEIS`             | `GH0004`             |
| **EP** (Epidemic)              | `BIO-INFDISPL`         | `BI0014`             |
| **EC** (Extratropical Cyclone) | `HM-PRESS`             | `MH0031`             |
| **FR** (Fire)                  | `ENV-DEG`              | `EN0013`             |
| **FF** (Flash Flood)           | `HM-FLOOD`             | `MH0006`             |
| **FL** (Flood)                 | `HM-FLOOD`             |                      |
| **HT** (Heat Wave)             | `HM-TEMP`              | `MH0047`             |
| **IN** (Insect Infestation)    | `BIO-INFEST`           | `BI0002`             |
| **LS** (Land Slide)            |                        |                      |

More specific [hazard codes](../../taxonomy.md#undrr-isc-2020-hazard-information-profiles) can be added to the `codes` field following the characteristics of the event.

##### Hazard Magnitude and Units

?
