# GDACS

GDACS is a cooperation framework between the United Nations, the European Commission and disaster managers worldwide to improve alerts, information exchange and coordination in the first phase after major sudden-onset disasters.

## Collection: `gdacs-events`

A STAC collection hold all the GDACS events. An example of the GDACS collection is [here](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events/gdacs-events.json).

- Name: Global Disaster Alert and Coordination System (GDACS)
- Code: `GDACS`
- Source organisation: European Commission - Joint Research Centre (JRC)
- Source code: EC-JRC
- Source Type: Regional Intergovernmental Organisation
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
  1. Episode #1 in the file [gdacs-events/1102983-1.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events/1102983-1.json).
  2. Episode #2 in the file [gdacs-events/1102983-2.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-events/1102983-2.json).

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                                       | properties.iso3                                       | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                              |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                                    | properties.affectedcountries.iso3                     | List of ISO3 codes of the other countries affected by the event                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                             | properties.eventtype                                  | List of hazard codes converted following the [GDACS event type to Hazard profile mapping](#mapping-from-gdacs-event-type-to-hazard-profile) |
| [assets.icon](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                 | properties.icon                                       | Asset with the icon of the event                                                                                                            |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                | properties.url.report                                 | Asset with the link to the GDACS report                                                                                                     |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                      | properties.url.details                                | Link to the GDACS event details page                                                                                                        |
| `related` link in [links]                                                                                              | properties.source and<br\>properties.sourceid         | If the source is present, create a `related` link to the item in the corresponding collection (e.g. GLOFAS-> `glofas-events`)               |
| `related` link in [links]                                                                                              | properties.glide                                      | If the glide number is present, create a `related` link to the item in `glide-events` collection                                            |

### Hazard Item

A GDACS event and episode will **ALWAYS** produce one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard) as in the example for the [flood in Spain from 27 Oct 2024 04 Nov 2024](https://www.gdacs.org/report.aspx?eventid=1102983&episodeid=2&eventtype=FL).

- There are 2 sources for the hazards:
  1. The general event [1102983-1-geteventdata-source.json](1102983-1-geteventdata-source.json) that is the output of the [`geteventdata`](https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983) API endpoint.
  2. the detailed geometries [1102983-1-getgeometry-source.json](1102983-1-getgeometry-source.json) that is the output of the [`getgeometry`](https://www.gdacs.org/gdacsapi/api/polygons/getgeometry?eventtype=FL&eventid=1102983&episodeid=2) API endpoint. This output is a feature collection and can be pretty big as it contains multiple geojson features representing multiple levels of the hazard. The STAC item is created by finding the feature that represent the **affected** areas. It has a property `properties.Class` set to `Poly_Affected`.
- The produced hazard STAC item is in the examples [gdacs-hazards/1102983-1.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/gdacs-hazards/1102983-1.json).

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                                       | properties.iso3                                                                        | ISO3 code of the country where the hazard occurred. Keywords shall also contain the human readable country name         |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                                    | properties.affectedcountries.iso3                                                      | List of ISO3 codes of the other countries affected by the hazard                                                        |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                             | [mappings from properties.eventtype](#mapping-from-gdacs-event-type-to-hazard-profile) | List of hazard codes converted following the GDACS hazard type to Hazard profile mapping                                |
| [assets.icon](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                 | properties.icon                                                                        | Asset with the icon of the hazard                                                                                       |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                | properties.url.report                                                                  | Asset with the link to the GDACS report                                                                                 |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links]                      | properties.url.details                                                                 | Link to the GDACS hazard details page                                                                                   |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail)                                                           | properties.hazard_detail                                                               | Detailed description of the hazard (more details in next section)                                                       |

#### Hazard Detail

The [hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) field is a JSON object that contains the detailed information about the hazard. The object is a mapping of the hazard codes to the detailed information. The detailed information is a JSON object with the following fields:

| STAC field     | GDACS field                  | Description                                               |
| -------------- | ---------------------------- | --------------------------------------------------------- |
| severity_value | properties.episodealertlevel | GDACS alert score                                         |
| severity_unit  | `gdacs`                      | GDACS alert level according to GDCAS event type and model |

##### Mapping from GDACS event type to Hazard profile

GDACS event types map to multiple classification systems for cross-system interoperability. The **2025 UNDRR-ISC** code is the **reference classification** for the Monty extension:

| GDACS Type | GLIDE | EM-DAT | **UNDRR-ISC 2025** (Reference) | Cluster | Description |
|------------|-------|--------|--------------------------------|---------|-------------|
| [FL](https://www.gdacs.org/Knowledge/models_fl.aspx) | FL | nat-hyd-flo-flo | **MH0600** | MH-WATER | Flooding (chapeau) |
| [EQ](https://www.gdacs.org/Knowledge/models_eq.aspx) | EQ | nat-geo-ear-gro | **GH0101** | GEO-SEIS | Earthquake |
| [TC](https://www.gdacs.org/Knowledge/models_tc.aspx) | TC | nat-met-sto-tro | **MH0309** | MH-WIND | Tropical Cyclone |
| [TS](https://www.gdacs.org/Knowledge/models_ts.aspx) | TS | nat-geo-ear-tsu | **MH0705** | MH-MARINE | Tsunami |
| [VO](https://www.gdacs.org/Knowledge/models_vo.aspx) | VO | nat-geo-vol-vol | **GH0201** | GEO-VOLC | Lava Flows |
| [DR](https://www.gdacs.org/Knowledge/models_dr.aspx) | DR | nat-cli-dro-dro | **MH0401** | MH-PRECIP | Drought |

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
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                                       | properties.iso3                                                                                                                                                | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[1..*]                                                    | properties.affectedcountries.iso3                                                                                                                              | List of ISO3 codes of the other countries affected by the event                                                               |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                             | [mappings from properties.eventtype](#mapping-from-gdacs-event-type-to-hazard-profile)                                                                         | List of hazard codes converted following the GDACS event type to Hazard profile mapping                                       |
| [assets.icon](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                 | properties.icon                                                                                                                                                | Asset with the icon of the event                                                                                              |
| [asset.report](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                | properties.url.report                                                                                                                                          | Asset with the link to the GDACS report                                                                                       |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]                       | properties.url.details                                                                                                                                         | Link to the GDACS event details page                                                                                          |
| `related` link in [links]                                                                                              | properties.source and<br\>properties.sourceid                                                                                                                  | If the source is present, create a `related` link to the item in the corresponding collection (e.g. GLOFAS-> `glofas-events`) |
