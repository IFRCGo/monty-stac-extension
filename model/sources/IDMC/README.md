# IDMC

The Internal Displacement Monitoring Centre (IDMC) maintains the Global Internal Displacement Database (GIDD), which provides comprehensive information on global internal displacement events from 2008 onwards.

## Collection: `idmc-events`

A STAC collection holding IDMC disaster-related displacement events.

- Name: Global Internal Displacement Database (GIDD) Events
- Code: `IDMC`
- Source organisation: Internal Displacement Monitoring Centre (IDMC)
- Source code: IDMC
- Source Type: International Non-Governmental Organization
- Source organization email: info@idmc.ch
- Source URL: https://www.internal-displacement.org/database
- Source Data license: [TBD]
- Source for: event
- API Documentation: https://helix-tools-api.idmcdb.org/external-api/

### Data

#### Disasters Dataset

The [GIDD Disasters Dataset](https://www.internal-displacement.org/database/api-documentation/#gidd-disasters-dataset) provides event information through the `/gidd/disasters/` API endpoint.
The disasters dataset provides information on disaster events that are used to reference both GIDD and IDU data. Each disaster record contains the following fields:

Each event record contains the following fields:

```json
{
  "id": 32145, // Unique identifier for events as assigned by IDMC.
  "event_name": "Tropical Cyclone Seroja",
  "country_iso3": "IDN",
  "country_name": "Indonesia", 
  "year": 2021,
  "event_start_date": "2021-04-04",
  "event_end_date": "2021-04-05",
  "hazard_category": "Weather related",
  "hazard_sub_category": "Storm",
  "hazard_type": "Tropical cyclone",
  "new_displacements": 17882
}
```

### Event Field Mapping

The following table shows how IDMC event fields map to STAC Item fields:

| STAC field                                                                                                               | IDMC field       | Required | Notes                                     |
| ------------------------------------------------------------------------------------------------------------------------ | ---------------- | -------- | ----------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | id               | Yes      | Use format `idmc-event-{id}`              |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | geometry         | Yes      | Derive from country boundaries            |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                    | `idmc-events`    | Yes      |                                           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | event_name       | Yes      | Direct mapping                            |
| [description](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)            | Generated        | Yes      | Combine event_name, country_name and date |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | event_start_date | Yes      | Convert to datetime with UTC timezone     |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | event_start_date | No       | Convert to datetime with UTC timezone     |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | event_end_date   | No       | Convert to datetime with UTC timezone     |

### Monty Extension Field Mapping

| Monty Extension field                                            | IDMC field   | Required | Notes                                                                    |
| ---------------------------------------------------------------- | ------------ | -------- | ------------------------------------------------------------------------ |
| [monty:country_codes](../../../README.md#montycountry_codes)\[0] | country_iso3 | Yes      | Direct mapping to array                                                  |
| [monty:hazard_codes](../../../README.md#montyhazard_codes)       | hazard_type  | Yes      | Map using the [hazard type mapping](#hazard-type-mapping)                |
| [monty:hazard_codes](../../../README.md#montyepisode_number      |              | Yes      | Always 1 (IDMC doesn't track episodes)                                   |
| [monty:corr_id](../../../README.md#montycorr_id)                 | id           | Yes      | Generated following the [event pairing procedure](../../event_paring.md) |

### Country-based Geometry Strategy

Since IDMC provides country-level data, geometry must be derived:

1. Primary Method
   - Use country ISO3 code to get boundary
   - Simplify geometry for efficiency
   - Store original country code

2. Geometry Considerations
   - Country-level precision only
   - No sub-national data available
   - Single country per event

### Hazard Type Mapping 

IDMC hazard types are mapped to [UNDRR-ISC 2020 Hazard Information Profile](../../taxonomy.md#undrr-isc-2020-hazard-information-profiles) codes following this mapping table:

| IDMC Hazard Type  | Hazard Profile Codes           | Notes                                               |
| ----------------- | ------------------------------ | --------------------------------------------------- |
| Avalanche         | MH0050                         | Direct mapping                                      |
| Cold wave         | MH0040                         | Direct mapping                                      |
| Drought           | MH0035                         | Direct mapping                                      |
| Earthquake        | GH0001, GH0002                 | Includes both earthquake and ground shaking effects |
| Flash flood       | MH0006                         | Direct mapping                                      |
| Flood             | MH0007                         | Maps to riverine/fluvial flood                      |
| Forest fire       | EN0013                         | Direct mapping                                      |
| Heatwave          | MH0047                         | Direct mapping                                      |
| Landslide         | GH0007                         | Direct mapping                                      |
| Storm surge       | MH0027                         | Direct mapping                                      |
| Subsidence        | GH0024                         | Maps to subsidence and uplift changes               |
| Tornado           | MH0059                         | Direct mapping                                      |
| Tropical cyclone  | MH0057                         | Maps to cyclonic wind, rain and storm surge effects |
| Tsunami           | MH0029                         | Direct mapping                                      |
| Volcanic eruption | GH0009, GH0010, GH0011, GH0012 | Multiple codes for different volcanic hazards       |
| Wildfire          | EN0013                         | Direct mapping                                      |

When implementing the mapping:

1. The primary hazard code is used in the `monty:hazard_codes` field
2. Original hazard codes are included in `keywords` for improved searchability

This mapping enables standardized hazard categorization while preserving IDMC's original classification in the source properties.