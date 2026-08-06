# GDACS

GDACS is a cooperation framework between the United Nations, the European Commission and disaster managers worldwide to improve alerts, information exchange and coordination in the first phase after major sudden-onset disasters.

## Collection: `gdacs-events`

A STAC collection hold all the GDACS events. An example of the GDACS collection is [here](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events/gdacs-events.json).

- Name: Global Disaster Alert and Coordination System (GDACS)
- Code: `GDACS`
- Source organisation: European Commission - Joint Research Centre (JRC)
- Source code: EC-JRC
- Source Type: Regional Intergovernmental Organization
- Source organization email: <coordination@gdacs.org>
- Source URL: <https://www.gdacs.org>
- Source Data license: MIT License
- Source for: event, hazard, impact

- previous implementation (R): <https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGDACS.R>

### Data

Accessible data is a set of GDACS entries. Each entry is a disaster event. The event data list is available in the form of a geojson collections via the API endpoint `https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?`.
Individual events can be accessed via the API endpoint `https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983`.

- Documentation: <https://www.gdacs.org/floodmerge/data_v2.aspx>

> [!IMPORTANT]  
> It is important to note that GDACS has its [own specific models](https://www.gdacs.org/Knowledge/models_eq.aspx) according to the type of event. This must be taken into account when mapping the data to the STAC model. When necessary, the present document will provide the specific mapping for each type of event.

### Event Item

A GDACS event and episode will **ALWAYS** produce an [**event STAC item**](https://github.com/IFRCGo/monty-stac-extension#event) as in the example for the [flood in Spain from 27 Oct 2024 04 Nov 2024](https://www.gdacs.org/report.aspx?eventid=1102983&episodeid=1&eventtype=FL).

- The source events are
  1. Episode #1 in the file [1102983-1-geteventdata-source.json](1102983-1-geteventdata-source.json) and is the output of the [`geteventdata`](https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983&episodeid=1) API endpoint.
  2. Episode #2 in the file [1102983-2-geteventdata-source.json](1102983-2-geteventdata-source.json) and is the output of the [`geteventdata`](https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983&episodeid=2) API endpoint.
- The produced event STAC items are
  1. Episode #1 in the file [gdacs-events/gdacs-event-1102983-1.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events/gdacs-event-1102983-1.json).
  2. Episode #2 in the file [gdacs-events/gdacs-event-1102983-2.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events/gdacs-event-1102983-2.json).

The event URL of the `geteventdata` API endpoint is stored in the `links` field of the STAC item with the `via` relation.

Here is a table with the fields that are mapped from the GDACS event to the STAC event:

| STAC field                                                                                                             | GDACS field                                           | Description                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | properties.eventid + properties.episodeid             | Unique identifier for the event per episode                                                                                                 |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | bbox                                                  | Bounding box of the event                                                                                                                   |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | geometry                                              | Geometry of the event                                                                                                                       |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `gdcas-events`                                        | The collection for GDACS events                                                                                                             |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | properties.name                                       | Name of the event                                                                                                                           |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                 | properties.description<br/>properties.htmldescription | Description of the event. HTML description should be privileged over plain text description and translated to markdown                      |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | properties.fromdate                                   | Date and time of the event converted in UTC ISO 8601 format                                                                                 |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | properties.fromdate                                   | Start date of the event converted in UTC ISO 8601 format                                                                                    |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | properties.todate                                     | End date of the event converted in UTC ISO 8601 format                                                                                      |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                           | properties.iso3                                       | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                        | properties.affectedcountries.iso3                     | List of ISO3 codes of the other countries affected by the event                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                 | properties.eventtype                                  | List of hazard codes converted following the [GDACS event type to Hazard profile mapping](#mapping-from-gdacs-event-type-to-hazard-profile) |
| [assets.icon](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                 | properties.icon                                       | Asset with the icon of the event                                                                                                            |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                | properties.url.report                                 | Asset with the link to the GDACS report                                                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                      | properties.url.details                                | Link to the GDACS event details page                                                                                                        |
| `related` link in [links]                                                                                              | properties.source and<br\>properties.sourceid         | If the source is present, create a `related` link to the item in the corresponding collection (e.g. GLOFAS-> `glofas-events`) with `roles: ["event"]` |
| `related` link in [links]                                                                                              | properties.glide                                      | If the glide number is present, create a `related` link to the item in `glide-events` collection with `roles: ["event"]`                 |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id)                                   | Generated                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |

### Hazard Item

A GDACS event and episode will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard) as in the example for the [flood in Spain from 27 Oct 2024 04 Nov 2024](https://www.gdacs.org/report.aspx?eventid=1102983&episodeid=2&eventtype=FL).

- There are 2 sources for the hazards:
  1. The general event [1102983-1-geteventdata-source.json](1102983-1-geteventdata-source.json) that is the output of the [`geteventdata`](https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983) API endpoint.
  2. the detailed geometries [1102983-1-getgeometry-source.json](1102983-1-getgeometry-source.json) that is the output of the [`getgeometry`](https://www.gdacs.org/gdacsapi/api/polygons/getgeometry?eventtype=FL&eventid=1102983&episodeid=2) API endpoint. This output is a feature collection and can be pretty big as it contains multiple geojson features representing multiple levels of the hazard. The STAC item is created by finding the feature that represent the **affected** areas. It has a property `properties.Class` set to `Poly_Affected`.
- The produced hazard STAC item is in the examples [gdacs-hazards/gdacs-hazard-1102983-1.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-hazards/gdacs-hazard-1102983-1.json).

Here is a table with the STAC fields that are mapped from the GDACS event to the STAC hazard:

| STAC field                                                                                                             | GDACS field                                                                            | Description                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | properties.eventid + properties.episodeid                                              | Unique identifier for the hazard per episode                                                                            |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | bbox                                                                                   | Bounding box of the hazard                                                                                              |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | geometry                                                                               | Geometry of the hazard                                                                                                  |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `gdcas-hazards`                                                                        | The collection for GDACS hazards                                                                                        |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | properties.name                                                                        | Name of the hazard                                                                                                      |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                 | properties.description<br/>properties.htmldescription                                  | Description of the hazard. HTML description should be privileged over plain text description and translated to markdown |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | properties.fromdate                                                                    | Date and time of the hazard converted in UTC ISO 8601 format                                                            |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | properties.fromdate                                                                    | Start date of the hazard converted in UTC ISO 8601 format                                                               |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | properties.todate                                                                      | End date of the hazard converted in UTC ISO 8601 format                                                                 |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                           | properties.iso3                                                                        | ISO3 code of the country where the hazard occurred. Keywords shall also contain the human readable country name         |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                        | properties.affectedcountries.iso3                                                      | List of ISO3 codes of the other countries affected by the hazard                                                        |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                 | [mappings from properties.eventtype](#mapping-from-gdacs-event-type-to-hazard-profile) | List of hazard codes converted following the GDACS hazard type to Hazard profile mapping                                |
| [assets.icon](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                 | properties.icon                                                                        | Asset with the icon of the hazard                                                                                       |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                | properties.url.report                                                                  | Asset with the link to the GDACS report                                                                                 |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                      | properties.url.details                                                                 | Link to the GDACS hazard details page                                                                                   |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail)                               | properties.hazard_detail                                                               | Detailed description of the hazard (more details in next section)                                                       |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |

#### Hazard Detail

The [hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) field is a JSON object that contains the detailed information about the hazard. The object is a mapping of the hazard codes to the detailed information. The detailed information is a JSON object with the following fields:

| STAC field     | GDACS field                  | Description                                               |
| -------------- | ---------------------------- | --------------------------------------------------------- |
| severity_value | properties.episodealertlevel | GDACS alert score                                         |
| severity_unit  | `gdacs`                      | GDACS alert level according to GDCAS event type and model |

##### Mapping from GDACS event type to Hazard profile

GDACS event types map to multiple classification systems for cross-system interoperability. The **2025 UNDRR-ISC** code is the **reference classification** for the Monty extension:

| GDACS Type                                           | GLIDE | EM-DAT          | **UNDRR-ISC 2025** (Reference) | Cluster   | Description           |
| ---------------------------------------------------- | ----- | --------------- | ------------------------------ | --------- | --------------------- |
| [FL](https://www.gdacs.org/Knowledge/models_fl.aspx) | FL    | nat-hyd-flo-flo | **MH0600**                     | MH-WATER  | Flooding (chapeau)    |
| [EQ](https://www.gdacs.org/Knowledge/models_eq.aspx) | EQ    | nat-geo-ear-gro | **GH0101**                     | GEO-SEIS  | Earthquake            |
| [TC](https://www.gdacs.org/Knowledge/models_tc.aspx) | TC    | nat-met-sto-tro | **MH0306**                     | MH-WIND   | Cyclone or Depression |
| [TS](https://www.gdacs.org/Knowledge/models_ts.aspx) | TS    | nat-geo-ear-tsu | **MH0705**                     | MH-MARINE | Tsunami               |
| [VO](https://www.gdacs.org/Knowledge/models_vo.aspx) | VO    | nat-geo-vol-vol | **GH0201**                     | GEO-VOLC  | Lava Flows            |
| [DR](https://www.gdacs.org/Knowledge/models_dr.aspx) | DR    | nat-cli-dro-dro | **MH0401**                     | MH-PRECIP | Drought               |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

##### Hazard Magnitude and Units

In GDACS, the alert level is a score that is calculated based on the event type. Each event ype uses a specific model to calculate the alert level. The alert level is a score that is used to determine the magnitude of the event.
The following table shows the magnitude scale and unit to be used for each event type:

| GDACS event type                                                                                                                         | Magnitude scale | Magnitude unit               |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---------------------------- |
| [Flood [FL]](https://www.gdacs.org/Knowledge/models_fl.aspx) event type uses a severity score based on the Global Flood Detection System | 1-3             | `GDACS Flood Severity Score` |

### Impact Item

According to the event type and the fields available in the GDACS event, one or more [**impact STAC items**](https://github.com/IFRCGo/monty-stac-extension#impact) can be created.
The following sections describe the mapping of specific GDACS event information to the STAC impact item.

GDACS carries impact data in two different places. The mapping to use depends on the event type:

| GDACS event type | Source field                        | Section                                                                     |
| ---------------- | ----------------------------------- | --------------------------------------------------------------------------- |
| FL               | `properties.sendai`                 | [Sendai indicators](#sendai-indicators)                                     |
| TC               | `properties.impacts[].resource.timeline` | [Tropical cyclone advisory timeline](#tropical-cyclone-advisory-timeline) |
| WF               | `properties.impacts[].resource.impact`   | [Wildfire population exposure](#wildfire-population-exposure)             |
| EQ, DR, TS, VO   | none                                | No impact item is produced. See [Event types without an impact mapping](#event-types-without-an-impact-mapping) |

> [!IMPORTANT]
> The `impacts[]` figures are **exposure estimates**, not observed losses. GDACS
> computes them with a model. It counts the population inside a hazard footprint.
> It does not count the persons that the hazard harmed. All impact items built from
> `impacts[]` therefore use `type: potentially_affected` and
> `estimate_type: modelled`. See [Decision: exposure is not impact](#decision-exposure-is-not-impact).

#### Sendai indicators

When the `sendai` field is present in the GDACS [event](#event-item), it contains an array of Sendai indicators.
Each Sendai indicator is a JSON object that shall produce an [impact item](https://github.com/IFRCGo/monty-stac-extension#impact).
The impact item shall have the following fields from both the GDACS event and the Sendai indicator:

| STAC field                                                                                                             | GDACS field                                                                                                                                                    | Description                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | properties.eventid + properties.episodeid + properties.sendai.sendaitype + properties.sendai.sendainame + properties.sendai.country + properties.sendai.region | Unique identifier for the impact                                                                                              |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | bbox of the geocoding of the properties.sendai.country + properties.sendai.region                                                                              | Bounding box of the impact                                                                                                    |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | geometry of the geocoding of the properties.sendai.country + properties.sendai.region                                                                          | Geometry of the impact                                                                                                        |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `gdcas-impacts`                                                                                                                                                | The collection for GDACS impacts                                                                                              |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | properties.name + properties.sendai.sendaitype + properties.sendai.sendainame + properties.sendai.country + properties.sendai.region                           | Name of the impact                                                                                                            |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                 | properties.sendai.description                                                                                                                                  | Description of the impact. HTML description should be privileged over plain text description and translated to markdown       |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | properties.sendai.onset_date                                                                                                                                   | Date and time of the event converted in UTC ISO 8601 format                                                                   |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | properties.sendai.onset_date                                                                                                                                   | Start date of the event converted in UTC ISO 8601 format                                                                      |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | properties.sendai.expires_date                                                                                                                                 | End date of the event converted in UTC ISO 8601 format                                                                        |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                           | properties.iso3                                                                                                                                                | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                        | properties.affectedcountries.iso3                                                                                                                              | List of ISO3 codes of the other countries affected by the event                                                               |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                 | [mappings from properties.eventtype](#mapping-from-gdacs-event-type-to-hazard-profile)                                                                         | List of hazard codes converted following the GDACS event type to Hazard profile mapping                                       |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | Source event ID | Unique identifier of the event |
| [assets.icon](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                 | properties.icon                                                                                                                                                | Asset with the icon of the event                                                                                              |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                | properties.url.report                                                                                                                                          | Asset with the link to the GDACS report                                                                                       |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]                       | properties.url.details                                                                                                                                         | Link to the GDACS event details page                                                                                          |
| `related` link in [links]                                                                                              | properties.source and<br\>properties.sourceid                                                                                                                  | If the source is present, create a `related` link to the item in the corresponding collection (e.g. GLOFAS-> `glofas-events`) with `roles: ["event"]` |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id)                                   | Generated                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |

#### The `impacts` field

For tropical cyclones and wildfires, GDACS does not put the impact figures in the
episode payload. It puts links to them in `properties.impacts[]`. Each entry has a
`source` field that names the advisory agency, and a `resource` object of URLs:

```json
"impacts": [
  {
    "source": "JTWC",
    "resource": {
      "buffer39": "https://www.gdacs.org/gdacsapi/api/export/getimpact?id=769814",
      "buffer74": "https://www.gdacs.org/gdacsapi/api/export/getimpact?id=769813",
      "timeline": "https://www.gdacs.org/gdacsapi/api/export/gettimeline?id=769812",
      "locations": "https://www.gdacs.org/gdacsapi/api/export/getlocations?id=769738"
    }
  }
]
```

The set of resource keys depends on the event type:

| Resource key | Endpoint       | Event type | Content                                                                                | Mapped |
| ------------ | -------------- | ---------- | -------------------------------------------------------------------------------------- | ------ |
| `timeline`   | `gettimeline`  | TC         | One entry for each advisory point. Track position, wind speed and population exposure. | Yes    |
| `buffer39`   | `getimpact`    | TC         | Total exposure in the 39 kt wind buffer, with exposed countries and infrastructure.    | No     |
| `buffer74`   | `getimpact`    | TC         | The same for the 74 kt wind buffer.                                                    | No     |
| `locations`  | `getlocations` | TC         | Named places along the track.                                                          | No     |
| `impact`     | `getimpact`    | WF         | Population exposure for the burnt area.                                                | Yes    |

> [!NOTE]
> Read the `impacts[]` field from `getepisodedata`, not from `geteventdata`.
> `geteventdata` ignores the `episodeid` parameter and always returns the current
> episode. GDACS publishes the correct per-episode URL in
> `properties.episodes[].details`.

#### Tropical cyclone advisory timeline

The `timeline` resource returns `channel.item[]`. Each entry describes one point on
the storm track, as issued by the advisory agency (for example JTWC).

| GDACS field         | Type   | Meaning                                                                     |
| ------------------- | ------ | ----------------------------------------------------------------------------- |
| `id`                | string | Identifier of the timeline entry. It is unique, and stable across episodes. |
| `advisory_number`   | string | Advisory sequence number from the advisory agency.                          |
| `actual`            | string | `"True"` for an observed position. `"False"` for a forecast position.       |
| `current`           | string | `"true"` on the entry that the current advisory observed.                   |
| `advisory_datetime` | string | Validity time of the entry, in UTC, format `%d %b %Y %H:%M`.                |
| `coordinates`       | string | `"<longitude> , <latitude>"` of the track point.                            |
| `wind_speed`        | string | Maximum sustained wind, in m/s.                                             |
| `pop39`             | string | Population in the wind field of 39 kt or more.                              |
| `pop74`             | string | Population in the wind field of 74 kt or more.                              |
| `popstormsurge`     | string | Population in the storm surge zone.                                         |
| `pop`               | string | Meaning not confirmed. **Do not map this field.** See rule 3 below.         |
| `alertscore`        | string | GDACS alert score at this track point.                                      |

Reference files, trimmed to the mapped fields:

- [`api-files/1001294-9-gettimeline-source.json`](api-files/1001294-9-gettimeline-source.json) — cyclone NOUL-26, episode 9.
- [`api-files/1001294-13-gettimeline-source.json`](api-files/1001294-13-gettimeline-source.json) — the same cyclone, episode 13.

##### Three properties of the timeline that control the mapping

**1. The timeline is cumulative, and it repeats.** Each episode returns every earlier
advisory entry again, unchanged. The 9 observed entries of episode 9 are identical to
the same 9 entries of episode 13, and they keep the same `id`. A transformer that keys
the impact item on the episode therefore creates one duplicate for each later episode.

**2. `advisory_number` is not unique.** The current advisory appears once as an
observed position, then once more for each forecast lead time. In episode 13 below,
advisory 13 appears 4 times. Advisory 12 is absent. `advisory_number` is therefore
neither unique nor dense. Only `id` is a safe key.

**3. `pop` is not a total.** The table below is the timeline of episode 13. In advisory
9, `pop` is 0 while `pop39` counts 75 million people. In the last forecast entry, `pop`
counts 19 million while `pop39` is 0. `pop` is therefore not the sum of the wind bands,
and it is not a headline figure. Its definition is not published. Until JRC confirms
it, use `pop39` and `pop74`, which the GDACS
[tropical cyclone model](https://www.gdacs.org/Knowledge/models_tc.aspx) defines.

| advisory | `actual` | `current` | `advisory_datetime` | `wind_speed` | `pop`      | `pop39`     | `pop74`    |
| -------: | :------- | :-------- | :------------------ | -----------: | ---------: | ----------: | ---------: |
|        8 | True     | false     | 25 Jul 2026 00:00   |       36.008 |          0 |  18,897,670 |          0 |
|        9 | True     | false     | 25 Jul 2026 06:00   |        38.58 |          0 |  75,490,475 |    614,941 |
|       10 | True     | false     | 25 Jul 2026 12:00   |       41.152 |          0 |  94,850,067 |  6,094,547 |
|       11 | True     | false     | 25 Jul 2026 18:00   |       43.724 | 12,226,693 | 103,014,755 | 11,167,854 |
|       13 | True     | **true**  | 26 Jul 2026 00:00   |        38.58 | 38,543,219 |  80,042,232 | 10,640,921 |
|       13 | False    | false     | 26 Jul 2026 12:00   |       23.148 |  7,488,955 |  14,518,892 |          0 |
|       13 | False    | false     | 27 Jul 2026 00:00   |       15.432 |  8,596,681 |           0 |          0 |
|       13 | False    | false     | 27 Jul 2026 12:00   |       10.288 | 19,811,513 |           0 |          0 |

##### Mapping

Each timeline entry shall produce **one impact item for each non-zero exposure band**.
An entry with `pop39` and `pop74` both above zero therefore produces 2 items. An entry
with every band at zero produces none.

| STAC field                                                                                                             | GDACS field                                                       | Description                                                                    |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | `gdacs-impact-` + properties.eventid + `-` + item.id + `-` + band  | Band is `pop39`, `pop74` or `surge`. **The episode is not part of the id.** See rule 1 |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | Point built from item.coordinates                                  | Position of the track point                                                    |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `gdacs-impacts`                                                    | The collection for GDACS impacts                                               |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | item.advisory_datetime                                             | Validity time of the advisory point, converted to UTC ISO 8601                 |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | item.advisory_datetime                                             | The same value. The entry describes an instant, not a period                   |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | item.advisory_datetime                                             | The same value                                                                 |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | item.name + advisory number + band                                 | For example `NOUL-26 advisory 13, population in 39 kt wind field`              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)                               | properties.iso3 and properties.affectedcountries.iso3              | Taken from the episode. The timeline entry has no reliable country field       |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                 | [mappings from properties.eventtype](#mapping-from-gdacs-event-type-to-hazard-profile) | `TC` maps to `MH0306`                                      |
| [monty:episode_number](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:episode_number)                | properties.episodeid                                               | The episode being processed. See rule 5                                        |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id)                    | properties.eventid                                                 | Unique identifier of the event                                                 |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:corr_id)                              | Generated                                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                      | the `timeline` URL of the episode                                  | The URL changes with each episode. Consumers shall not use it as identity      |

The `monty:impact_detail` object:

| Field           | Value                                                                            |
| --------------- | ---------------------------------------------------------------------------------- |
| `category`      | `people`                                                                          |
| `type`          | `potentially_affected`                                                            |
| `value`         | `pop39`, `pop74` or `popstormsurge`, as an integer, for the band of the item      |
| `unit`          | `count`                                                                           |
| `estimate_type` | `modelled`                                                                        |
| `description`   | The band, in words. For example `Population in the wind field of 39 kt or more`   |

Rules:

1. **Key the item on `item.id`, not on the episode.** The identifier is stable across
   episodes. Re-ingestion of a later episode then updates the same item, instead of
   creating a duplicate.
2. **Ingest every entry, of every episode.** Forecast entries of an earlier episode
   carry their own `id`, so they stay as a record of what GDACS forecast at the time.
   Observed entries collapse onto the item that an earlier episode already created.
3. **`estimate_type` is always `modelled`.** The `actual` field describes the track
   position, not the exposure figure. GDACS models the exposure for observed positions
   in the same way as for forecast positions.
4. **`type` is always `potentially_affected`.** See
   [Decision: exposure is not impact](#decision-exposure-is-not-impact).
5. **`monty:episode_number` is the episode being processed.** Because observed entries
   repeat, this field can change on re-ingestion. It carries the last episode that
   published the entry, not the first.

> [!WARNING]
> Monty has no field that marks an estimate as a forecast. `estimate_type` describes
> where a figure comes from. It does not say whether the figure is about the future. A
> cyclone forecast and a post-event model run both map to `modelled`. A consumer can
> therefore tell a forecast entry from an observed entry only by its datetime. See
> [Open questions](#open-questions-raised-by-this-mapping).

#### Wildfire population exposure

For wildfires, `properties.impacts[].resource.impact` returns a `getimpact` document.
The `source` is `GWIS`. The document has this shape:

| GDACS field                                              | Meaning                                                    |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| `modelname`                                              | `WF`                                                       |
| `modelrun`                                               | Timestamp of the model run                                 |
| `modelstatus`                                            | Status of the model run, for example `info: processing ok` |
| `datums[].datum[]` with `datasource: "POP"`              | The population scalars                                     |
| `datums[].datum[]` with `datasource: "country"`          | Exposed countries, with `ISO_3DIGIT`                       |
| `datums[].datum[]` with `datasource: "INPUT PARAMETERS"` | The burnt area, as a WKT `MULTIPOLYGON` in `Shape`         |

The `POP` datum carries a series of scalars:

| Scalar        | Meaning                                            |
| ------------- | ---------------------------------------------------- |
| `POPAFFECTED` | Population in the burnt area. Equal to `SUMPOP0.0`  |
| `SUMPOP1.0`   | Population within 1 km of the burnt area            |
| `SUMPOP2.0`   | Population within 2 km                              |
| `SUMPOP5.0`   | Population within 5 km                              |
| `SUMPOP10.0`  | Population within 10 km                             |

Each `getimpact` document shall produce **one impact item** from `POPAFFECTED`.

| STAC field | GDACS field                                                                       | Description                                                          |
| ---------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| id         | `gdacs-impact-` + properties.eventid + `-` + properties.episodeid + `-popaffected` | The impact document has no identifier of its own                     |
| geometry   | the `Shape` WKT of the `INPUT PARAMETERS` datum                                    | The burnt area. Fall back to the event geometry if `Shape` is absent |
| datetime   | properties.fromdate of the episode                                                 | The document has no observation time, only a model run time          |
| collection | `gdacs-impacts`                                                                    | The collection for GDACS impacts                                     |

The `monty:impact_detail` object:

| Field           | Value                          |
| --------------- | -------------------------------- |
| `category`      | `people`                        |
| `type`          | `potentially_affected`          |
| `value`         | `POPAFFECTED`, as an integer    |
| `unit`          | `count`                         |
| `estimate_type` | `modelled`                      |
| `description`   | `Population in the burnt area`  |

The `modelname`, `modelrun` and `modelstatus` fields show that GDACS derived this
figure from a model. `estimate_type` is therefore `modelled`, and never `primary`.

#### Event types without an impact mapping

GDACS publishes no usable impact figures for EQ, DR, TS and VO. These event types
produce an [event item](#event-item) and a [hazard item](#hazard-item) only. For EQ,
the alert score and the population exposure appear in the event description text, not
in a structured field. A mapping from free text is not reliable enough to specify here.

#### Decision: exposure is not impact

`pop39`, `pop74` and `POPAFFECTED` count the persons inside a hazard footprint. They do
not count the persons that the hazard harmed. UNDRR keeps these two concepts apart:
*exposure* is the presence of persons or assets in hazard-prone areas, and *impact* is
the effect of the hazard on them.

Monty has no exposure class. The nearest impact type is `potentially_affected`, and
this document uses it for every figure that comes from `impacts[]`. The choice is
deliberate, and it is a compromise. A consumer that sums `affected_total` across
sources does not pick up these figures, which is the intended behaviour. A consumer
that wants the exposure figures shall filter on `type = potentially_affected`.

#### Open questions raised by this mapping

Two questions in this mapping belong to the Monty model, not to GDACS. They are open
for the Montandon Technical Working Group:

1. **Should Monty mark an estimate as a forecast?** `estimate_type` describes
   provenance. It cannot say whether an estimate is about the future.
2. **Should exposure be a class of its own?** `potentially_affected` carries the
   exposure figures today, and it also carries other meanings for other sources.

Until the group settles these questions, the rules above hold.
