# Monty Extension Specification

- **Title:** Monty
- **Identifier:** <https://IFRCGo.github.io/monty/v1.0.0/schema.json>
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
It provides a way to include Montandon data from [Montandon model analysis](./model/model.md) in a STAC Item or Collection.
The specification is organized as follows

- [Fields](#fields): Describes the fields that are added to the STAC Item and Collection objects.
- [Event](#event): Describes the mandatory fields for the event object.
- [Hazard](#hazard): Describes the mandatory fields for the hazard object.
- [Relation types](#relation-types): Describes the relation types that should be used in the Monty extension.

The specifications of the fields and the objects are grouped by the data types of the

## Fields

The fields in the table below can be used in these parts of STAC documents:

- [ ] Catalogs
- [x] Collections
- [x] Item Properties (incl. Summaries in Collections)
- [ ] Assets (for both Collections and Items, incl. Item Asset Definitions in Collections)
- [ ] Links
- [ ] Bands

| Field Name          | Type                                        | Description                                                                                                                                                                                |
| ------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| monty:country_codes | \[string]                                   | **REQUIRED**. The country codes of the countries affected by the event. The country code follows [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard format.   |
| monty:corr_id       | string                                      | **REQUIRED**. The unique identifier assigned by the Monty system to the reference event used to "pair" all the items of the same event.                                                    |
| monty:hazard_codes  | \[string]                                   | The hazard codes of the hazards affecting the event. The hazard code follows the [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips) identifier. |
| monty:hazard_detail | [Hazard Detail object](#montyhazard_detail) | The details of the hazard.                                                                                                                                                                 |

> [!NOTE]  
> Either `monty:hazard_codes` OR `monty:hazard_detail` MUST be present in the item.

### Additional Field Information

#### monty:country_codes

It is a list of country codes of the countries concerned by the item. 
It must at least contain the countries intersected by the item's geometry.

#### monty:hazard_codes

It is a list of hazard codes of the hazards concerned by the item. 
The hazard code follows the [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips) identifier.
With that identifier, it is possible to derive a set of additional properties associated with the hazard:

- The name of the hazard
- The type of the hazard
- The description of the hazard
- The cluster of the hazard

#### monty:corr_id

It is the unique identifier assigned by the Monty system to the reference event.
This correlation identifier is critical to associate the events to the reference event.
Each source event MUST have one in order to make a search of the source events efficiently.
A source event should also contain a [`reference-event` link](#relation-types) to the reference event.

#### monty:hazard_detail

It is an object that contains the details of the hazard. Preferably used only in a Hazard item.
The following fields are available in the object:

| Field Name    | Type      | Description                                                                                                                                                                                |
| ------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| codes         | \[string] | The hazard codes of the hazards affecting the event. The hazard code follows the [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips) identifier. |
| max_value     | number    | The estimated maximum hazard intensity/magnitude/severity value, as a number, without the units.                                                                                           |
| max_unit      | string    | The unit of the max_value.                                                                                                                                                                 |
| estimate_type | string    | The type of the estimate. It can be one of the following values: `primary`, `secondary`, `modelled`.                                                                                       |

## Event

This section describes the rules and best practises to apply on the STAC core fields for the event object.
More detail on the fields is available in the [Montandon model analysis](./model/model.md#event).

- Examples:
  - [Reference Event example](examples/item-ref-event-flood-PAR.json): Shows usage of the extension for a reference event
  <!-- - [Source Collection example](examples/collection-source-event-GLIDE.json): Shows the usage of the extension in a STAC Collection representing an event data source. -->
  - [Source Event example](examples/item-source-event-flood-PAR-GLIDE.json): Shows usage of the extension for a source event
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

### STAC Item fields for event

The table below describes the **REQUIRED** core fields in the representation of an event.

| Field Name                                   | Description                                                                                                                                                                                                                         |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                                           | The unique identifier for the event assigned by the issuer (source) of the event.                                                                                                                                                   |
| geometry                                     | Defines the location of the event, formatted according to RFC 7946. It is higly recommended to use a point.                                                                                                                         |
| **properties object**                        |                                                                                                                                                                                                                                     |
| title                                        | The name of the event assigned by the issuer (source) of the event.                                                                                                                                                                 |
| roles                                        | It MUST include the `event` role. The reference event MUST also contain `reference`.                                                                                                                                                |
| datetime<br/>start_datetime<br/>end_datetime | Any temporal information of the event                                                                                                                                                                                               |
| keywords                                     | A list of keywords that describe the event. This list includes the human-readable names of<br/>- the countries affected by the event<br/>- the hazard types affecting the event<br/>- Any additional useful keyword from the source |

## Hazard

This section describes the mandatory fields for the hazard object.
More detail on the field rules is available in the [Montandon model analysis](./model/model.md#hazard).

- Examples:
  - [Hazard example](examples/item-hazard-flood-PAR.json): Shows usage of the extension for a flooding hazard

### STAC Item fields for hazard

The table below describes the **REQUIRED** core fields in the representation of a hazard.

| Field Name                                   | Description                                                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| id                                           | The unique identifier for the hazard assigned by the issuer (source) of the hazard.                          |
| geometry                                     | Defines the location of the hazard, formatted according to RFC 7946.                                         |
| **properties object**                        |                                                                                                              |
| title                                        | The name of the hazard assigned by the issuer (source) of the hazard.                                        |
| roles                                        | It MUST include the `hazard` role.                                                                           |
| datetime<br/>start_datetime<br/>end_datetime | Any temporal information of the event                                                                        |
| keywords                                     | A list of keywords that describe the hazard. This list includes the human-readable names of the hazard type. |

## Relation types

The following types should be used as applicable `rel` types in the
[Link Object](https://github.com/radiantearth/stac-spec/tree/master/item-spec/item-spec.md#link-object).

| Type            | Description                             |
| --------------- | --------------------------------------- |
| reference-event | This link points to the reference event |
| source-event    | This link points to the source event    |


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
