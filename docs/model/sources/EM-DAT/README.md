# EM-DAT

EM-DAT is a global database on natural and technological disasters, containing essential core data on the occurrence and effects of more than 22,000 disasters in the world, from 1900 to the present day. The database is compiled from various sources, including UN agencies, non-governmental organizations, insurance companies, research institutes, and press agencies. The main objective of the database is to serve the purposes of humanitarian action at national and international levels. It is maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at the School of Public Health of the Université catholique de Louvain (UCLouvain) in Brussels, Belgium.

## Collection: `emdat-events`

A STAC collection hold all the EM-DAT events. An example of the EM-DAT collection is [here](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-events/emdat-events.json).

- Name: Global Disaster Events from the Emergency Events Database (EM-DAT)
- Code: `EM-DAT`
- Source organisation: Centre for Research on the Epidemiology of Disasters (CRED)
- Source code: CRED
- Source Type: Regional Intergovernmental Organisation
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

- The source events is the output of the [`data`](https://public.emdat.be/data) API endpoint. The example is [public_emdat_custom_request_2025-01-13_4cf1ccf1-9f6e-41a3-9aec-0a19903febae.xlsx](../EM-DAT/public_emdat_custom_request_2025-01-13_4cf1ccf1-9f6e-41a3-9aec-0a19903febae.xlsx) and the STAC item is [emdat-events/2024-0796-ESP.json](https://github.com/IFRCGo/monty-stac-extension/tree/main/examples/emdat-events/2024-0796-ESP.json).

> [!IMPORTANT]  
> As there is no permanent link to the EM-DAT event, the URl used to trace back the event should be composed with `https://public.emdat.be/data/` + the disaster ID. In the example, the URL is `https://public.emdat.be/data/2024-0796-ESP`.

Here is a table with the fields that are mapped from the EM-DAT event to the STAC event:

| STAC field                                                                                                             | EM-DAT [column](https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/#column-description) | Description                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | DisNo.                                                                                                       | Unique identifier for the event                                                                                                                                                                                                                            |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | Admin Units                                                                                                  | Bounding box of the disaster [geocoded from Natural Earth Data (NED)](https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/)                                                                                           |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | Admin Units                                                                                                  | Level 1 Admin boundaries polygons of the disaster [geocoded from Natural Earth Data (NED)](https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/). Note: Discard the items that has neither lat lng nor the shapefiles |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `emdat-events`                                                                                               | The collection for EM-DAT events                                                                                                                                                                                                                           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | Event Name                                                                                                   | Name of the disaster. Not always available                                                                                                                                                                                                                 |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                 | properties.description<br/>properties.htmldescription                                                        | Description of the event. HTML description should be privileged over plain text description and translated to markdown                                                                                                                                     |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | start year + start month + start day                                                                         | Date and time of the disaster converted in UTC ISO 8601 format. Start year is mandatory while month and day might not always be available. If no start day, keep 1 (start of the month) and set the flag missing_startday to true.                         |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | start year + start month + start day                                                                         | Start date of the disaster converted in UTC ISO 8601 format. Start year is mandatory while month and day might not always be available. If no start day, keep 1 (start of the month) and set the flag missing_startday to true.                            |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | start year + start month + start day                                                                         | End date of the event converted in UTC ISO 8601 format                                                                                                                                                                                                     |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0]                                                       | iso                                                                                                          | ISO3 code of the country where the event occurred. Keywords shall also contain the human readable country name                                                                                                                                             |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)                                                             | Classification Key                                                                                           | List of hazard codes converted following the [Hazard Type Mapping](#hazard-type-mapping)                                                                                                                                                                   |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in [links]                       | graphql request                                                                                              | Link to the EM-DAT event details page                                                                                                                                                                                                                      |

#### Hazard Type Mapping

EM-DAT uses the [EM-DAT CRED Classification Tree](../../taxonomy.md#em-dat-cred-classification-tree) and must be mapped to the **2025 UNDRR-ISC** code as the **reference classification** for the Monty extension. The full cross-classification mapping is available in the [taxonomy documentation](../../taxonomy.md#cross-classification-mapping).

The EM-DAT Classification Key (e.g., `nat-hyd-flo-flo`) should be used along with the corresponding 2025 UNDRR-ISC code (e.g., `MH0600`) for maximum interoperability.

**Example mappings:**

| EM-DAT Classification Key | GLIDE | **UNDRR-ISC 2025** (Reference) | Cluster    | Description             |
| ------------------------- | ----- | ------------------------------ | ---------- | ----------------------- |
| nat-hyd-flo-flo           | FL    | **MH0600**                     | MH-WATER   | Flooding (chapeau)      |
| nat-geo-ear-gro           | EQ    | **GH0101**                     | GEO-SEIS   | Earthquake              |
| nat-met-sto-tro           | TC    | **MH0306**                     | MH-WIND    | Cyclone or Depression   |
| nat-cli-dro-dro           | DR    | **MH0401**                     | MH-PRECIP  | Drought                 |
| nat-geo-vol-vol           | VO    | **GH0201**                     | GEO-VOLC   | Lava Flows              |
| nat-geo-ear-tsu           | TS    | **MH0705**                     | MH-MARINE  | Tsunami                 |
| nat-cli-wil-for           | WF    | **EN0205**                     | ENV-FOREST | Wildfires               |
| nat-met-ext-hea           | HT    | **MH0501**                     | MH-TEMP    | Heatwave                |
| nat-met-ext-col           | CW    | **MH0502**                     | MH-TEMP    | Cold Wave               |
| nat-geo-mmd-lan           | LS    | **GH0300**                     | GEO-GFAIL  | Gravitational Mass Movement (chapeau) |

> [!NOTE]
> All three classification codes (GLIDE, EM-DAT, UNDRR-ISC 2025) should be included in the `monty:hazard_codes` array for maximum interoperability. The complete mapping table with all EM-DAT disaster types is available in the [taxonomy cross-classification mapping](../../taxonomy.md#cross-classification-mapping). More specific [hazard codes](../../taxonomy.md#complete-2025-hazard-list) can be added following the characteristics of the event.

This mapping enables standardized hazard categorization while preserving EM-DAT's original classification in the source properties.
