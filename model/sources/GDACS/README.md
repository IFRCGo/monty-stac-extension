# GDACS

GDACS is a cooperation framework between the United Nations, the European Commission and disaster managers worldwide to improve alerts, information exchange and coordination in the first phase after major sudden-onset disasters.

## Collection: `gdacs-events`

A STAC collection hold all the GDACS events. An example of the GDACS collection is [here](../collections/gdacs-events.json).

* Name: Global Disaster Alert and Coordination System (GDACS)
* Code: GDACS
* Source organisation: European Commission - Joint Research Centre (JRC)
* Source code: EC-JRC
* Source Type: Regional Intergovernmental Organisation
* Source organization email: coordination@gdacs.org
* Source URL: https://www.gdacs.org
* Source Data license: MIT License
* Source for: event, hazard, impact

* implementation (R): https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGDACS.R

### Data

Accessible data is a set of GDACS entries. Each entry is a disaster event. The data is available in the form of a geojson collections via the API endpoint `https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?`.
Individual events can be accessed via the API endpoint `https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983`.

* Documentation: https://www.gdacs.org/floodmerge/data_v2.aspx
* Python lib: https://github.com/Kamparia/gdacs-api

### Event

A GDACS event will **ALWAYS** produce an **event STAC item** as in the example for the [flood in Spain from 27 Oct 2024 04 Nov 2024](https://www.gdacs.org/report.aspx?eventid=1102983&episodeid=2&eventtype=FL).

- The source event is in the file [1102983-geteventdata-source.json](1102983-geteventdata-source.json) and is the output of the [`geteventdata`](https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983) API endpoint.
- The produced event STAC item is in the examples [gdacs-events/1102983.json](../../../examples/gdacs-events/1102983.json).

The event URL of the `geteventdata` API endpoint is stored in the `links` field of the STAC item with the `via` relation.

Here is a table with the fields that are mapped from the GDACS event to the STAC event:

| GDACS field                                           | STAC field                | Description                                                                                                                   |
| ----------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| bbox                                                  | bbox                      | Bounding box of the event                                                                                                     |
| geometry                                              | geometry                  | Geometry of the event                                                                                                         |
| properties.eventtype                                  | monty:hazard_codes        | List of hazard codes converted following the GDACS event type to Hazard profile mapping                                       |
| properties.eventid                                    | id                        | Unique identifier for the event                                                                                               |
| properties.episodeid                                  | ?                         | *Should we tkae the episode as a separate event?*                                                                             |
| properties.glide                                      | `related` link in [links] | If the glide number is present, create a `related` link to the item in `glide-events` collection                              |
| properties.name                                       | title                     | Name of the event                                                                                                             |
| properties.description<br/>properties.htmldescription | description               | Description of the event. HTML description should be privileged over plain text description and translated to markdown        |
| properties.icon                                       | assets.icon               | Asset with the icon of the event                                                                                              |
| properties.url.report                                 | asset.report              | Asset with the link to the GDACS report                                                                                       |
| properties.url.details                                | `via` link in [links]     | Link to the GDACS event details page                                                                                          |
| properties.fromdate                                   | start_datetime            | Start date of the event converted in UTC ISO 8601 format                                                                      |
| properties.todate                                     | end_datetime              | End date of the event converted in UTC ISO 8601 format                                                                        |
| properties.iso3                                       | monty:country_codes[0]    | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                |
| properties.source and<br\>properties.sourceid         | `related` link in [links] | If the source is present, create a `related` link to the item in the corresponding collection (e.g. GLOFAS-> `glofas-events`) |
| properties.affectedcountries.iso3                     | monty:country_codes[1..*] | List of ISO3 codes of the other countries affected by the event                                                               |

### Hazard

A GDACS event will **ALWAYS** produce one **hazard STAC item** as in the example for the [flood in Spain from 27 Oct 2024 04 Nov 2024](https://www.gdacs.org/report.aspx?eventid=1102983&episodeid=2&eventtype=FL).

- There are 2 sources for the hazards:
    1. The general event [1102983-geteventdata-source.json](1102983-geteventdata-source.json) that is the output of the [`geteventdata`](https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983) API endpoint.
    2. the detailed geometries [1102983-getgeometry-source.json](1102983-getgeometry-source.json) that is the output of the [`getgeometry`](https://www.gdacs.org/gdacsapi/api/polygons/getgeometry?eventtype=FL&eventid=1102983&episodeid=2) API endpoint. This output is a feature collection and can be pretty big as it contains multiple geojson features representing multiple levels of the hazard. The STAC item is created by finding the feature that represent the **affected** areas. It has a property `properties.Class` set to `Poly_Affected`.
- The produced hazard STAC item is in the examples [gdacs-hazards/1102983-affected.json](../../../examples/gdacs-hazards/1102983-affected.json).

Here is a table with the STAC fields that are mapped from the GDACS event to the STAC hazard:

| STAC field                                                   | GDACS field                                           | Description                                                                                                                   |
| ------------------------------------------------------------ | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| bbox                                                         | bbox                                                  | Bounding box of the event                                                                                                     |
| geometry                                                     | geometry                                              | Geometry of the event                                                                                                         |
| monty:hazard_codes                                           | properties.eventtype                                  | List of hazard codes converted following the GDACS event type to Hazard profile mapping                                       |
| id                                                           | properties.eventid                                    | Unique identifier for the event                                                                                               |
| ?                                                            | properties.episodeid                                  | *Should we take the episode as a separate event?*                                                                             |
| `related` link in [links]                                    | properties.glide                                      | If the glide number is present, create a `related` link to the item in `glide-events` collection                              |
| title                                                        | properties.name                                       | Name of the event                                                                                                             |
| description                                                  | properties.description<br/>properties.htmldescription | Description of the event. HTML description should be privileged over plain text description and translated to markdown        |
| assets.icon                                                  | properties.icon                                       | Asset with the icon of the event                                                                                              |
| asset.report                                                 | properties.url.report                                 | Asset with the link to the GDACS report                                                                                       |
| `via` link in [links]                                        | properties.url.details                                | Link to the GDACS event details page                                                                                          |
| start_datetime                                               | properties.fromdate                                   | Start date of the event converted in UTC ISO 8601 format                                                                      |
| end_datetime                                                 | properties.todate                                     | End date of the event converted in UTC ISO 8601 format                                                                        |
| monty:country_codes[0]                                       | properties.iso3                                       | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                |
| `related` link in [links]                                    | properties.source and<br\>properties.sourceid         | If the source is present, create a `related` link to the item in the corresponding collection (e.g. GLOFAS-> `glofas-events`) |
| monty:country_codes[1..*]                                    | properties.affectedcountries.iso3                     | List of ISO3 codes of the other countries affected by the event                                                               |
| [monty:hazard_detail](../../../README.md#montyhazard_detail) | properties.hazard_detail                              | Detailed description of the hazard (more details in next section)                                                             |

#### Hazard Detail

The `properties.hazard_detail` field is a JSON object that contains the detailed information about the hazard. The object is a mapping of the hazard codes to the detailed information. The detailed information is a JSON object with the following fields:

| STAC field  | GDACS field           | Description          |
| ----------- | --------------------- | -------------------- |
| codes       | properties.eventtype  | List of hazard codes |
| max_value   | properties.alertscore | GDACS alert score    |
| max_unit       | `gdacs` | GDACS alert level    |