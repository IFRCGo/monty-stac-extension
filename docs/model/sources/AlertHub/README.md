# AlertHub

The aim of IFRC Alert Hub is to provide timely and effective emergency alerts to communities worldwide, empowering them to protect their lives and livelihoods.

## Collection: `alerthub-events`

A STAC collection hold all the AlertHub events. An example of the AlertHub collection is [here](https://github.com/IFRCGo/monty-stac-extension/blob/main/examples/alerthub-events/alerthub-events.json)

- Name: AlertHub
- Code: `AlertHub`
- Source organisation: IFRC
- Source code: alerthub
- Source type: IFRC
- Source organization email: im@ifrc.org
- Source URL: <alerthub.ifrc.org>
- Source Data license: MIT License
- Source for: event, hazard

### Data

The data from Alerthub can be accessed using the GraphQL queries. The data is currently fetched using the query `Alerts` from the following [data source](https://alerthub-api.ifrc.org/graphql/).

### Event Item

An AlertHub event and episode will **ALWAYS** produce and [event STAC item](https://github.com/IFRCGo/monty-stac-extension#event). Here is a table with the fields that are mapped from the AlertHub event to the STAC event.

| STAC field | AlertHub | Field Description |
|------------|----------|--------------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | alert.id | Unique identifier for the event |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | alert.info.areas | Geometry of the event |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | From geometry | Bbox is constructed using geometry data using bounds |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `alerthub-events` | The collection for AlertHub events |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | alert.headline | Short description of the event |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | alert.description | Description of the event |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | alert.effective | Date and time of the event converted in UTC ISO 8601 format |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | alert.effective | Date and time of the event converted in UTC ISO 8601 format |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | alert.expires | End date of the event converted in UTC ISO 8601 format |
| [monty:episode_number](https://ifrcgo.org/monty-stac-extension/v1.0.0/schema.json#monty:episode_number) | 1 | Set to 1 as there is no proper episodes handling mechanism |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0] | alert.country.iso3 | ISO3 of the country |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | alert.category, alert.event | List of hazard codes |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links] | alert.url | Link to the GDACS event details page |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.1.1/schema.json#monty:corr_id)                                   | Generated                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |
| [monty:guid](https://ifrcgo.org/monty-stac-extension/v1.1.1/schema.json#monty:guid) | Generated | Generated following the [guid string](../../global_identififer.md) convention |


### Hazard Item

An AlertHub will **ALWAYS** produce one [**hazard STAC item**] (https://github.com/IFRCGo/monty-stac-extension#hazard).

Here is a table with the STAC fields that are mapped from the AlertHub event to STAC hazard.

| STAC field | AlertHub | Field Description |
|------------|----------|--------------------|
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id) | alert.id | Unique identifier for the event |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry) | alert.info.areas | Geometry of the event |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox) | From geometry | Bbox is constructed using geometry data using bounds |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection) | `alerthub-hazards` | The collection for AlertHub events |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | alert.headline | Short description of the event |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics) | alert.description | Description of the event |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time) | alert.effective | Date and time of the event converted in UTC ISO 8601 format |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | alert.effective | Date and time of the event converted in UTC ISO 8601 format |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | alert.expires | End date of the event converted in UTC ISO 8601 format |
| [monty:episode_number](https://ifrcgo.org/monty-stac-extension/v1.0.0/schema.json#monty:episode_number) | 1 | Set to 1 as there is no proper episodes handling mechanism |
| [monty:country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)\[0] | alert.country.iso3 | ISO3 of the country |
| [monty:hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes) | alert.category, alert.event | List of hazard codes |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md) in \[links] | alert.url | Link to the GDACS event details page |
| [monty:corr_id](https://ifrcgo.org/monty-stac-extension/v1.1.1/schema.json#monty:corr_id)                                   | Generated                                          | Generated following the [event correlation](../../correlation_identifier.md) convention |
| [monty:guid](https://ifrcgo.org/monty-stac-extension/v1.1.1/schema.json#monty:guid) | Generated | Generated following the [guid string](../../global_identififer.md) convention |
| [monty:hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) | alert.info.severity | Severity Info |


#### Hazard Detail

The [hazard_detail](https://github.com/IFRCGo/monty-stac-extension#montyhazard_detail) field is a JSON object that contains the detailed information about the hazard. The object is a mapping of the hazard codes to the detailed information. The detailed information is a JSON object with the following fields:

| STAC field     | AlertHub field                  | Description                                               |
| -------------- | ---------------------------- | --------------------------------------------------------- |
| severity_value | Uses a severity mappings | Five enums are mapped to a numeric value |
| severity_unit  | `alerthub`                      | AlertHub alert level |
| estimate_type  | MontyEstimateType.PRIMARY | Use a fixed value |