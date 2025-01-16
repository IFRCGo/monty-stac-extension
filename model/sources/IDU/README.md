# IDU

API: https://helix-tools-api.idmcdb.org/external-api/
Current Usage: https://www.internal-displacement.org/internal-displacement-updates/

## Collection: `idu-events`

Collection: idu-events
A STAC collection hold all the IDU events.

Name: Internal displacement updates

Code: IDU

Source organization: Internal Displacement Monitoring Center (IDMC)

Source organization type: Regional Intergovernmental Organization

Source organization email: info@idmc.ch

Source code: IDMC

Source URL: https://helix-tools-api.idmcdb.org/external-api/

Source for: event, impact

previous implementation (R): none


| STAC field                         | IDU Field                            | Remarks                        |
| ---------------------------------- | ------------------------------------ | ------------------------------ |
| id                                 | id                                   | Figure id                      |
| collection                         | `idu-events`                         | Collection name for STAC       |
| title                              | event_name                           | Name of the event              |
| description                        | standard_popup_text                  |                                |
| datetime                           | displacement_date                    | Start date of the event        |
| geometry                           | type: "point", coordinates: centroid | centroid of the event location |
| monty:country_codes[0]             | iso3                                 |                                |
| monty:event_codes                  | event_codes                          | Might be empty                 |
| properties.locations               | locations_name                       |                                |
| properties.event_start_date        | event_start_date                     |                                |
| properties.event_end_date          | event_end_date                       |                                |
| properties:displacement_start_date | displacement_start_date              |                                |
| properties:displacement_end_date   | displacement_end_date                |                                | 
| properties.sources                 | sources                              |                                |
| properties.event_id                | event_id                             |                                |
| properties.hazard_subtype          | hazard_subtype                       |                                |
