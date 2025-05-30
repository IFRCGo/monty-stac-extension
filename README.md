# Monty Extension Specification

- **Title:** Monty
- **Identifier:** <https://ifrcgo.org/monty-stac-extension/v1.0.0/schema.json>
- **Field Name Prefix:** monty
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: @emmanuelmathot

## About Monty

Monty, an abbreviated name for the Montandon - Global Crisis Data Bank, is a database that brings in hazard and impact data for current,
historical and forecasted disasters around the globe.
By combining lots of different sources of information, Monty aims to fill-in-the-gaps
and provide a more complete picture of disaster risk for the National Societies.
For more information about the Montandon project, please check out [this 5-minute video](https://www.youtube.com/watch?v=BEWxqYfrQek).

This document explains the Montandon Extension to the [SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec) (STAC) specification.
It provides a way to include Montandon data from [Montandon model analysis](https://ifrcgo.org/monty-stac-extension/model/) in a STAC Item or Collection.
The specification is organized as follows

- [Fields](#fields): Describes the fields that are added to the STAC Item and Collection objects.
- [Relation types](#relation-types): Describes the relation types that should be used in the Monty extension.
- [Event](#event): Describes the mandatory fields for the event object.
- [Data](#data): Describes the mandatory fields for all data objects.
  - [Hazard](#hazard): Describes the mandatory fields for the hazard object.
  - [Impact](#impact): Describes the mandatory fields for the impact object.
  - [Response](#response): Describes the mandatory fields for the response object.
- [Queryables](https://ifrcgo.org/monty-stac-extension/model/stac-api/queryables.md): Describes the properties that can be used as queryables in a STAC API implementing the Filter Extension.

The specifications of the fields and the objects are grouped by their data types.

## Fields

The fields in the sections below can be used in these parts of STAC documents:

- [ ] Catalogs
- [x] Collections
- [x] [Item Properties](#item-properties) (incl. Summaries in Collections)
- [ ] Assets (for both Collections and Items, incl. Item Asset Definitions in Collections)
- [x] [Links](#link-attributes)
- [ ] Bands

### Item Properties

| Field Name           | Type                                        | Description                                                                                                                                                                                                                                                                   |
| -------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| monty:episode_number | integer                                     | The episode number of the event. It is a unique identifier assigned by the Monty system to the event                                                                                                                                                                          |
| monty:country_codes  | \[string]                                   | **REQUIRED**. The country codes of the countries affected by the event, hazard, impact or response. The country code follows [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard format                                                           |
| monty:corr_id        | string                                      | **REQUIRED**. The unique identifier assigned by the Monty system to the reference event used to "pair" all the items of the same event. The correlation identifier follows a specific convention described in the [event correlation](https://ifrcgo.org/monty-stac-extension/model/correlation_identifier.md) page |
| monty:hazard_codes   | \[string]                                   | **REQUIRED**. The hazard codes of the hazards affecting the event. For interoperability purpose, the array MUST contain at least one code from a [hazard classification system](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#hazards)                                                                  |
| monty:hazard_detail  | [Hazard Detail object](#montyhazard_detail) | The details of the hazard                                                                                                                                                                                                                                                     |
| monty:impact_detail  | [Impact Detail object](#montyimpact_detail) | The details of the impact                                                                                                                                                                                                                                                     |

### Roles

A set of roles are defined to describe the type of the data. The following roles are defined:

| Role      | Description                   |
| --------- | ----------------------------- |
| event     | The data is an event          |
| reference | The data is a reference event |
| source    | The data is a source event    |
| hazard    | The data is a hazard          |
| impact    | The data is an impact         |
| response  | The data is a response        |

The roles are used at the item level in the `roles` field to characterize the data. It is also used in the link object to characterize the linked item. This is useful to find exactly the item needed. For instance, to find the reference event of a data, a link with both `event` and `reference` roles is needed.

### Link Attributes

| Field Name  | Type   | Description                                                                                                        |
| ----------- | ------ | ------------------------------------------------------------------------------------------------------------------ |
| occ_type    | string | The type of the occurrence. It can be one of the following values: `known`, `potential`                            |
| occ_prob    | string | It is a qualitative assessment of the likelihood of the linked hazard occurring with the main hazard (e.g. `high`) |
| occ_probdef | uri    | It is a link to the definition of the probability for the hazard relationship                                      |

#### Additional Field Information

##### monty:episode_number

It is the unique identifier assigned by the Monty system to an episode of the event. An event can have multiple episodes and this number is used to identify them.

##### monty:country_codes

It is a list of country codes of the countries concerned by the item.
It must at least contain the countries intersected by the item's geometry.

##### monty:hazard_codes

It is a list of hazard codes of the hazards concerned by the item. There are multiple various classification systems for hazards so the field is open to any code.

Nevertheless, the field is recommended to follow at least one of the [referenced classification systems](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#hazards) 
and then to include their other system counterparts following the [crosswalk classification systems mapping](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#cross-classification-mapping) to enforce interoperability.

Tables with the possible values are available in the [hazard section of the taxonomy](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#hazards) with:

- [UNDRR-ISC 2020 Hazard Information Profiles](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#undrr-isc-2020-hazard-information-profiles)
- [EM_DAT CRED Classification Key](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#em-dat-cred-classification-tree)
- [GLIDE classification](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#glide-classification)
- [A crosswalk classification systems mapping](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#cross-classification-mapping)

With those codes, it is possible to derive a set of additional properties associated with the hazard:

- The name of the hazard
- The type of the hazard
- The description of the hazard
- The cluster of the hazard

for which a human-readable keyword can be generated and stored in the `keywords` field.

> [!IMPORTANT]
> [Hazard items](#hazard) **MUST** have a **single** `monty:hazard_codes` in the array because the hazard is unique. This is also crucial for
> the event [correlation process](https://ifrcgo.org/monty-stac-extension/model/correlation_identifier.md).

##### monty:corr_id

It is the unique identifier assigned by the Monty system to every item in the system.
This correlation identifier is critical to associate event, hazard, impact and response items together.
Each item *MUST* have one.
More information about the correlation identifier is available in the [event correlation](https://ifrcgo.org/monty-stac-extension/model/correlation_identifier.md) page.

##### monty:hazard_detail

It is an object that contains the details of the hazard. Preferably used only in a Hazard item.
The following defined fields are available in the object:

| Field Name     | Type   | Description                                                                                                          |
| -------------- | ------ | -------------------------------------------------------------------------------------------------------------------- |
| cluster        | string | **REQUIRED** The cluster of the hazard. The possible values are defined in [this table](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#hazards) |
| severity_value | number | **REQUIRED** The estimated maximum hazard intensity/magnitude/severity value, as a number, without the units         |
| severity_unit  | string | **REQUIRED** The unit of the max_value                                                                               |
| estimate_type  | string | The type of the estimate. The possible values are `primary`, `secondary` and `modelled`                              |

Any other field can be added to the object to provide more details about the hazard.
For instance, `category` and  `pressure` can be added to provide the category and the pressure of a cyclone.

##### monty:impact_detail

It is an object that contains the details of the impact estimate. Preferably used only in an Impact item.

| Field Name    | Type   | Description                                                                                                                                                                                                             |
| ------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category      | string | **REQUIRED** The category of impact, which is the specific asset or population demographic that has been impacted by the hazard. The possible values are defined in [this table](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#exposure-category) |
| type          | string | **REQUIRED** The estimated value type of the impact. The possible values are defined in [this table](https://ifrcgo.org/monty-stac-extension/model/taxonomy.md#impact-type)                                                                                   |
| value         | number | **REQUIRED** The estimated impact value, as a number, without the units                                                                                                                                                 |
| unit          | string | The units of the impact estimate                                                                                                                                                                                        |
| estimate_type | string | The type of the estimate. The possible values are `primary`, `secondary` and `modelled`                                                                                                                                 |
| description   | string | The description of the impact                                                                                                                                                                                           |

## Relation types

The following types should be used as applicable `rel` types in the
[Link Object](https://github.com/radiantearth/stac-spec/tree/master/item-spec/item-spec.md#link-object).

| Type                | Description                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ |
| reference-event     | This link points to the reference event                                                                            |
| source-event        | This link points to the source event                                                                               |
| related-hazard      | This link points to a related hazard. For example, a flood related to the event                                    |
| related-impact      | This link points to a related impact. For example, a flood related to the impact                                   |
| triggers-hazard     | This link points to a triggered hazard. For example, an earthquake triggers a landslide                            |
| triggered-by-hazard | This link points to the hazard that triggered this hazard. For example, an earthquake that triggered a landslide   |
| concurrent-hazard   | This link points to a concurrent hazard. For example, thunderstorms can occur together with windstorms or cyclones |
| complex-hazard      | This link points to a complex hazard when the relationship between the hazards is complex                          |

## Event

This section describes the rules and best practises to apply on the STAC core fields for the event object.
More detail on the fields is available in the [Montandon model analysis](https://ifrcgo.org/monty-stac-extension/model#event).

- Examples:
  - [Reference Events Collection example](examples/reference-events/reference-events.json): Shows usage of the extension in a STAC Collection of reference events
  - [Reference Event example](examples/reference-events/20241027T150000-ESP-HM-FLOOD-001-GCDB.json): Shows usage of the extension for a reference event
  - [Source Collection example](examples/gdacs-events/gdacs-events.json): Shows the usage of the extension in a STAC Collection for source events
  - [Source Event example](examples/gdacs-events/1102983-1.json): Shows usage of the extension for a source event
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

### STAC Item fields for event

The table below describes the rules for the core fields in the representation of an event.

| Field Name            | Description                                                                                                                                                                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                    | The unique identifier for the event assigned by the issuer (source) of the event                                                                                                                                                    |
| geometry              | Defines the location of the event, formatted according to RFC 7946. It is highly recommended to use a point                                                                                                                         |
| **properties object** |                                                                                                                                                                                                                                     |
| title                 | The name of the event assigned by the issuer (source) of the event                                                                                                                                                                  |
| roles                 | It MUST include the `event` role. The reference event MUST also contain `reference`                                                                                                                                                 |
| keywords              | A list of keywords that describe the event. This list includes the human-readable names of<br/>- the countries affected by the event<br/>- the hazard types affecting the event<br/>- Any additional useful keyword from the source |

The event class is the core of the Monty model. It represents a disaster event that has occured or is forecasted to occur.
The global crisis data bank records multiple instances of events that are related to a single event:

- One **unique reference** event that is used to "[pair](https://ifrcgo.org/monty-stac-extension/model/correlation_identifier.md)" all the instances of the event
- Multiple instances of the event that are recorded for different sources. Each source event **must** have the following:
  - A link to the reference event with the [relationship](#relation-types) type `reference-event`
  - A link to the resource from which the event was sourced with
    the [relationship](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#using-relation-types) type `via`

## Data

### STAC Item fields for all data objects

The table below describes the rules for the core fields in the representation of a data (Hazard, Impact or Response).

| Field Name            | Description                                                                                                                 |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| id                    | The unique identifier for the data assigned by the issuer (source) of the data                                              |
| geometry              | Defines the location of the data, formatted according to RFC 7946                                                           |
| **properties object** |                                                                                                                             |
| title                 | The name of the data assigned by the issuer (source) of the data                                                            |
| roles                 | It MUST include the data type role: `hazard`, `impact` or `response`                                                        |
| keywords              | A list of keywords that describe the data. This list includes the human-readable names of any codification used in the item |
| created               | The date and time of the creation of the data by the issuer (source) of the data                                            |

### Hazard

This section describes in details the usage of the fields and links for the hazard object.
More detail on the field definition is available in the [Montandon model analysis](https://ifrcgo.org/monty-stac-extension/model#hazard).

- Examples:
  - [Flood Hazard example](examples/gdacs-hazards/1102983-1-affected.json): Shows usage of the extension for a flood hazard

The hazard class represents a process, phenomenon or human activity that may cause loss of life, injury or other health impacts,
property damage, social and economic disruption or environmental degradation. UNDRR - <https://www.undrr.org/terminology/hazard>.

In the Monty model, a hazard is **ALWAYS** linked to one or multiple event(s) and each event **MUST** be linked to at least one hazard.
Therefore, a hazard item **MUST** have at least one link with the [relationship type](#relation-types) `source-event`.
It is also recommended to have a link with the relationship type `source-event` pointing to the event of the same source if available.

An hazard object **MUST** have the [`monty:hazard_detail`](#montyhazard_detail) field with all the details of the hazard.

Hazards may be linked between each others.
This linkage is called "concurrent hazard" and is linking the observed and potentially unobserved hazards together with a `*-hazard` [relationship](#relation-types).
The link may also have specific `occ-*` [attributes](#link-attributes) to describe the occurrence of the linked hazard.

> [!IMPORTANT]
> [Hazard items](#hazard) MUST have a single `monty:hazard_codes` in the array because the hazard is unique. This is also crucial for
> the event correlation process.

### Impact

This section describes in details the usage of the fields and links for the impact object.
More detail on the field definition is available in the [Montandon model analysis](https://ifrcgo.org/monty-stac-extension/model#impact).

- Examples:
  - [Impact for flood in Spain example](examples/gdacs-impacts/gdacs-impact-1102983-2-A-death-Spain-Andalusia.json): Shows usage of the extension for a flood impact

The impact class represents the consequences of a hazard on the affected assets or population.

In the [Monty model](https://ifrcgo.org/monty-stac-extension/model#data-overview), an impact is **ALWAYS** linked to a hazard as a source of the impact, impacts are recorded from multiple [sources](https://ifrcgo.org/monty-stac-extension/model/sources/).

An impact object **MUST** have the [`monty:impact_detail`](#montyimpact_detail) field with all the details of the impact.

### Response

*This section still needs to be defined.*

## Contributing

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
For contributions, please follow the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md) Instructions
for running tests are copied here for convenience.

### Running tests

The same checks that run as checks on PR's are part of the repository and can be run locally to verify that changes are valid.
To run tests locally, you'll need `npm`, which is a standard part of any [node.js installation](https://nodejs.org/en/download/).

First you'll need to install everything with npm once. Just navigate to the root of this repository and on
your command line run:

```bash
npm install
```

Then to check markdown formatting and test the examples against the JSON schema, you can run:

```bash
npm test
```

This will spit out the same texts that you see online, and you can then go and fix your markdown or examples.

If the tests reveal formatting problems with the examples, you can fix them with:

```bash
npm run format-examples
```
