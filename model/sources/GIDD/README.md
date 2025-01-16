# GIDD

API Key: IDMCWSHSOLO009
Swagger: https://helix-tools-api.idmcdb.org/external-api/#/gidd/

Note: GIDD provides only disaggregation data, so the only geometry we have is the country polygon. This needs to be downloaded separately and then referenced to the `event-item`

## Collection: `gidd-events`
Collection: gidd-events
A STAC collection hold all the GIDD events.

Name: Global Internal Displacement Database

Code: GIDD

Source organisation: Internal Displacement Monitoring Center (IDMC)

Source code: IDMC

Source Type: Regional Intergovernmental Organization

Source organization email: info@idmc.ch

Source URL: https://helix-tools-api.idmcdb.org/external-api/

Source for: event, impact

previous implementation (R): https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyImpactData/GetGIDD.R

### GIDD events

Endpoint: https://helix-tools-api.idmcdb.org/external-api/#/gidd/gidd_disaggregations_disaggregation_geojson_list

cause (string): (CONFLICT - Conflict, DISASTER - Disaster, conflict - Conflict, disaster - Disaster)
client_id * (string): 
disaster_type__in (array[integer]): Multiple values may be separated by commas
iso3__in (array[string]): Multiple values may be separated by commas
release_environment (string): (PRE_RELEASE - Pre Release, RELEASE - Release, pre_release - Pre Release,  release - Release)


| STAC field                | GIDD Field       | Remarks                  |
| ------------------------- | ---------------- | ------------------------ |
| id                        | id               | Figure id                |
| collection                | `gidd-events`    | Collection name for STAC |
| title                     | event_name       | Name of the event        |
| datetime                  | event_start_date | Start date of the event  |
| geometry                  | geometry         |                          |
| monty:start_date          | event_start_date |                          |
| monty:end_date            | event_end_date   |                          |
| monty:country_codes[0]    | iso3             |                          |
| monty:event_codes         | event_codes      | Might be empty           |
| properties.locations      | locations_name   |                          |
| properties.sources        | sources          |                          |
| properties.event_id       | event_id         |                          |
| properties.hazard_subtype | hazard_subtype   |                          |

