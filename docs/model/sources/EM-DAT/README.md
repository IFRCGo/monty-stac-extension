# EM-DAT

EM-DAT is a global database on natural and technological disasters, containing essential core data on the occurrence and effects of more than 22,000 disasters in the world, from 1900 to the present day. The database is compiled from various sources, including UN agencies, non-governmental organizations, insurance companies, research institutes, and press agencies. The main objective of the database is to serve the purposes of humanitarian action at national and international levels. It is maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at the School of Public Health of the Université catholique de Louvain (UCLouvain) in Brussels, Belgium.

## Collection: `emdat-events`

A STAC collection hold all the EM-DAT events. An example of the EM-DAT collection is [here](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-events/emdat-events.json).

- Name: Global Disaster Events from the Emergency Events Database (EM-DAT)
- Code: `EM-DAT`
- Source organisation: Centre for Research on the Epidemiology of Disasters (CRED)
- Source code: CRED
- Source Type: Academic / Research
- Source organization email: <contact@cred.be>
- Source URL: <https://www.emdat.be/>
- Source Data license: [proprietary license](https://doc.emdat.be/docs/legal/terms-of-use/)
- Source for: event, hazard, impact

- previous implementation (R): <https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyImpactData/GetEMDAT.R>

### Data

After registration and login, the data can be downloaded using the EM-DAT “Access Data” Tab or Toolbox as a flat table in Microsoft Excel format (.xlsx). The EM-DAT database is described in the [Data Structure Description](https://doc.emdat.be/docs/data-structure-and-content/) section. In particular, the [Column Description](https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/#column-description) section contains the description of each column of the public table found in the Excel file.

- Documentation: <https://doc.emdat.be/docs/>

#### GraphQL API

- EM-DAT Public Table: <https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/>
- For shapefiles tutorial: <https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/>
- API cookbook: <https://files.emdat.be/docs/emdat_api_cookbook.pdf>
- EM-DAT GraphQL API: <https://files.emdat.be/docs/emdat_api_python.pdf>
- EM-DAT R API: <https://files.emdat.be/docs/emdat_api_rlang.pdf>
- GraphiQL: <https://api.emdat.be/>
API Key as JSON header: (Mention this in Headers to access queries)

```json
{"Authorization": "secret"}
```

##### Query Example

```graphql
query monty {
      api_version
      public_emdat(
        cursor: {limit: -1}
      ) {
        total_available
        info {
          timestamp
          filters
          cursor
        }
        data {
          disno
          classif_key
          group
          subgroup
          type
          subtype
          external_ids
          name
          iso
          country
          subregion
          region
          location
          origin
          associated_types
          ofda_response
          appeal
          declaration
          aid_contribution
          magnitude
          magnitude_scale
          latitude
          longitude
          river_basin
          start_year
          start_month
          start_day
          end_year
          end_month
          end_day
          total_deaths
          no_injured
          no_affected
          no_homeless
          total_affected
          reconstr_dam
          reconstr_dam_adj
          insur_dam
          insur_dam_adj
          total_dam
          total_dam_adj
          cpi
          admin_units
          entry_date
          last_update
        }
      }
    }
```

##### Filters in graphql

`from`: Int
Filter records with a start_year field greater or equal to the value, excluding others.

`to`: Int
Filter records with a start_year field lower or equal to the value, ecluding others.

`iso`: \[String!]
Filter records which occurred in the list of countries passed (passed as 3-letter codes as in the iso field of the Data type).

`region_code`: \[Int!]
Filter records which occurred in the list of regions selected, passed as codes based on the [UN M49 Standard](https://unstats.un.org/unsd/methodology/m49/).

`subregion_code`: \[Int!]
Filter records which occurred in the list of subregions selected, passed as codes based on the [UN M49 Standard](https://unstats.un.org/unsd/methodology/m49/).

`classif`: \[String!]
Return records with matching classif_key, to include all categories under a specific level, the end of the classif_key can be omitted or replaced by -*. This wildcard/omit pattern only works from left to right.
example (pattern): \["nat-*"] ...will return all natural events.
Classifications can be inclusively added to the filter but broader classifications will override more specific definitions.
example (inclusive): \["nat-geo-mmd-*", "nat-hyd-mmw-*"] ...will return events from the "Mass movement (dry)" and "Mass movement (wet)" types altogether.
example (override): \["nat-cli-dro-dro", "nat-cli-*"]... will ignore the first key and return all events from the "Climatological" subgroup.

`include_hist`: Boolean
Include historical events in the results (they are by default excluded unless this parameter is passed as true).

> [!IMPORTANT]  
> It is important to note that EM-DAT has its [own specific models](https://doc.emdat.be/docs/data-structure-and-content/core-structure-of-the-database/) to classify the events and impacts.

### Event Item

A [EM-DAT disaster](https://doc.emdat.be/docs/data-structure-and-content/general-definitions-and-concepts/) will **ALWAYS** produce an [**event STAC item**](https://github.com/IFRCGo/monty-stac-extension#event) as in the example for the [flood in Spain from 27 Oct 2024 04 Nov 2024](../EM-DAT/public_emdat_custom_request_2025-01-13_4cf1ccf1-9f6e-41a3-9aec-0a19903febae.xlsx).

- The source events is the output of the [`data`](https://public.emdat.be/data) API endpoint. The example is [public_emdat_custom_request_2025-01-13_4cf1ccf1-9f6e-41a3-9aec-0a19903febae.xlsx](../EM-DAT/public_emdat_custom_request_2025-01-13_4cf1ccf1-9f6e-41a3-9aec-0a19903febae.xlsx) and the STAC item is [emdat-events/emdat-event-2024-0796-ESP.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-events/emdat-event-2024-0796-ESP.json).

> [!IMPORTANT]  
> As there is no permanent link to the EM-DAT event, the URl used to trace back the event should be composed with `https://public.emdat.be/data/` + the disaster ID. In the example, the URL is `https://public.emdat.be/data/2024-0796-ESP`.

Here is a table with the fields that are mapped from the EM-DAT event to the STAC event:

| STAC field                                                                                                             | EM-DAT [column](https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/#column-description) | Description                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | DisNo. | `emdat-event-` + the disaster number: `emdat-event-2024-0796-ESP` |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | Admin Units                                                                                                  | Bounding box of the disaster [geocoded from Natural Earth Data (NED)](https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/)                                                                                           |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | Admin Units                                                                                                  | Level 1 Admin boundaries polygons of the disaster [geocoded from Natural Earth Data (NED)](https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/). Note: Discard the items that has neither lat lng nor the shapefiles |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `emdat-events`                                                                                               | The collection for EM-DAT events                                                                                                                                                                                                                           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Event Name, or Disaster Subtype + Country; then Start Month + Start Year | The Event Name when EM-DAT gives one, then the month and year of the start: `Hurricane 'Milton' of October 2024`. Most records have no name. The title is then the disaster subtype and the country, with the same date: `Flood (General) in Spain of October 2024`. It uses the disaster type when there is no subtype, and only the year when there is no start month |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Disaster Type, Disaster Subtype, Location, Country, Start Month, Start Year | A generated text: `<type> (<subtype>) in <location>, <country> of <month> <year>`. The subtype is shown only when it is different from the type. EM-DAT has no description field |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Derived from Classification Key and Country | The hazard keywords of `monty:hazard_codes` in alphabetical order, then the country name from the `Country` field (not the ISO3 code), with no duplicates: `["Flooding", "Meteorological & Hydrological", "Water-related", "Spain"]`. The hazard item of the event has the same list. An [impact item](#impact-item) adds two keywords |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | start year + start month + start day                                                                         | Date and time of the disaster converted in UTC ISO 8601 format. Start year is mandatory while month and day might not always be available. If no start day, keep 1 (start of the month) and set the flag missing_startday to true.                         |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | start year + start month + start day                                                                         | Start date of the disaster converted in UTC ISO 8601 format. Start year is mandatory while month and day might not always be available. If no start day, keep 1 (start of the month) and set the flag missing_startday to true.                            |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | start year + start month + start day                                                                         | End date of the event converted in UTC ISO 8601 format. A missing month or day is set to 1. If the start date is then later than the end date, the record fails and gives no item                                                                                                                                                                                                     |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                                       | iso                                                                                                          | ISO3 code of the country where the event occurred.                                                                                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                             | Classification Key                                                                                           | List of hazard codes converted following the [Hazard Type Mapping](#hazard-type-mapping)                                                                                                                                                                   |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]                       | graphql request                                                                                              | Link to the EM-DAT event details page                                                                                                                                                                                                                      |
| [monty:src_event_id](https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json#monty:src_event_id) | DisNo. | The full disaster number: `2024-0796-ESP` |
| [processing:version](https://github.com/stac-extensions/processing) | Generated | Semantic version of the transformer that generated the item, via the `processing:` extension |
| [processing:software](https://github.com/stac-extensions/processing) | Generated | Dependency/provenance chain (`{"pystac-monty": "<version>"}`), via the `processing:` extension |
#### Hazard Type Mapping

EM-DAT uses the [EM-DAT CRED Classification Tree](../../taxonomy.md#em-dat-cred-classification-tree) and must be mapped to the **2025 UNDRR-ISC** code as the **reference classification** for the Monty extension. The full cross-classification mapping is available in the [taxonomy documentation](../../taxonomy.md#cross-classification-mapping).

The EM-DAT Classification Key (e.g., `nat-hyd-flo-flo`) should be used along with the corresponding 2025 UNDRR-ISC code (e.g., `MH0600`) for maximum interoperability.

**Example mappings:**

| EM-DAT Classification Key | GLIDE | **UNDRR-ISC 2025** (Reference) | Cluster    | Description             |
| ------------------------- | ----- | ------------------------------ | ---------- | ----------------------- |
| nat-hyd-flo-flo           | FL    | **MH0600**                     | MH-WATER   | Flooding (chapeau)      |
| nat-geo-ear-gro           | EQ    | **GH0101**                     | GEO-SEIS   | Earthquake              |
| nat-met-sto-tro           | TC    | **MH0309**                     | MH-WIND    | Tropical Cyclone        |
| nat-cli-dro-dro           | DR    | **MH0401**                     | MH-PRECIP  | Drought                 |
| nat-geo-vol-vol           | VO    | **GH0201**                     | GEO-VOLC   | Lava Flows              |
| nat-geo-ear-tsu           | TS    | **MH0705**                     | MH-MARINE  | Tsunami                 |
| nat-cli-wil-wil           | WF    | **EN0205**                     | ENV-FOREST | Wildfires (general)     |
| nat-cli-wil-for           | WF    | **EN0205**                     | ENV-FOREST | Wildfires (forest fire) |
| nat-cli-wil-lan           | WF    | **EN0205**                     | ENV-FOREST | Wildfires (land fire)   |
| nat-met-ext-hea           | HT    | **MH0501**                     | MH-TEMP    | Heatwave                |
| nat-met-ext-col           | CW    | **MH0502**                     | MH-TEMP    | Cold Wave               |
| nat-geo-mmd-lan           | LS    | **GH0300**                     | GEO-GFAIL  | Gravitational Mass Movement (chapeau) |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. The complete mapping table with all EM-DAT disaster types is available in the [taxonomy cross-classification mapping](../../taxonomy.md#cross-classification-mapping). More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

This mapping enables standardized hazard categorization while preserving EM-DAT's original classification in the source properties.

### Hazard Item

An EM-DAT disaster **ALWAYS** produces one [**hazard STAC item**](https://github.com/IFRCGo/monty-stac-extension#hazard) with its event item. The example is [emdat-hazards/emdat-hazard-2024-0796-ESP.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-hazards/emdat-hazard-2024-0796-ESP.json).

The hazard item is a copy of the [event item](#event-item). It has the same geometry, dates, title, description, keywords, country codes and correlation identifier. These fields are different:

| STAC field | EM-DAT column | Description |
| ---------- | ------------- | ----------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | DisNo. | `emdat-hazard-` + the disaster number: `emdat-hazard-2024-0796-ESP` |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `emdat-hazards` | The collection for EM-DAT hazards |
| roles | Generated | `["source", "hazard"]` |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | Classification Key | Only the UNDRR-ISC 2025 code of the [Hazard Type Mapping](#hazard-type-mapping): `["MH0600"]`. The event item has the three codes |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail).severity_value | Magnitude | The magnitude of the disaster: `56.0`. When EM-DAT gives no magnitude, the value is `-1` |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail).severity_unit | Magnitude Scale | The unit of the magnitude: `Km2`. When EM-DAT gives no scale, the value is `emdat` |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail).estimate_type | Generated | Always `primary` |

### Impact Item

An EM-DAT disaster produces one [**impact STAC item**](https://github.com/IFRCGo/monty-stac-extension#impact) for each impact column that has a value higher than 0. A disaster can thus have from zero to six impact items. The example disaster has four: [total_deaths](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-impacts/emdat-impact-2024-0796-ESP-total_deaths.json), [no_affected](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-impacts/emdat-impact-2024-0796-ESP-no_affected.json), [total_affected](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-impacts/emdat-impact-2024-0796-ESP-total_affected.json) and [total_dam](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-impacts/emdat-impact-2024-0796-ESP-total_dam.json).

The impact item is a copy of the [event item](#event-item), with the three hazard codes. These fields are different:

| STAC field | EM-DAT column | Description |
| ---------- | ------------- | ----------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | DisNo. | `emdat-impact-` + the disaster number + `-` + the field name of the [Impact Field Mapping](#impact-field-mapping): `emdat-impact-2024-0796-ESP-total_deaths` |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `emdat-impacts` | The collection for EM-DAT impacts |
| roles | Generated | `["source", "impact"]` |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Generated | The title of the event item + ` - ` + the title text of the [Impact Field Mapping](#impact-field-mapping): `Flood (General) in Spain of October 2024 - Total deaths` |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | Generated | The keywords of the event item, then the label of the impact type and the label of the exposure category from the [taxonomy](../../taxonomy.md#impact): `["Flooding", "Meteorological & Hydrological", "Water-related", "Spain", "Death", "People (All Demographics)"]` |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail).category | Generated | See the [Impact Field Mapping](#impact-field-mapping) |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail).type | Generated | See the [Impact Field Mapping](#impact-field-mapping) |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail).value | The impact column | The value of the column. Total Damage is multiplied by 1000 |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail).unit | Generated | `count` for the people columns, `USD` for Total Damage |
| [monty:impact_detail](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail).estimate_type | Generated | Always `primary` |

#### Impact Field Mapping

| EM-DAT column | Field name (in the id) | Title text | Category | Type |
| ------------- | --------------------- | ---------- | -------- | ---- |
| Total Deaths | `total_deaths` | Total deaths | `people` | `death` |
| No. Injured | `no_injured` | Injured | `people` | `injured` |
| No. Affected | `no_affected` | Affected | `people` | `affected_direct` |
| No. Homeless | `no_homeless` | Homeless | `people` | `displaced_total` |
| Total Affected | `total_affected` | Total affected | `people` | `affected_total` |
| Total Damage ('000 US$) | `total_dam` | Total damage | `global_currency` | `cost` |

The transformer does not map the other impact columns of EM-DAT: the reconstruction costs, the insured damage, and the adjusted values.

> [!NOTE]
> **Total Damage.** EM-DAT gives this column in thousands of US dollars. The transformer multiplies the value by 1000 and writes it in `USD`. The example disaster has `11000000` in EM-DAT, and the item has `value: 11000000000` with `unit: USD`.
>
> **No. Affected and Total Affected.** In EM-DAT, No. Affected is the number of people who need immediate assistance, and Total Affected is the sum of No. Injured, No. Affected and No. Homeless. The two columns thus give two types: `affected_direct` and `affected_total`. Do not add the two values.
