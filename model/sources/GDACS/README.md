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

A GDACS event will **ALWAYS** produce an event STAC item as in the example [GDACS-2021-000001-IND](../examples/gdacs-events/GDACS-2021-000001-IND.json).

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




