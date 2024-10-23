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
It provides a way to include Montandon data in a STAC Item or Collection.

The specifications of the fields and the objects are grouped by the data types of the [Montandon model analysis](./model/model.md).

## Event

This section describes the mandatory fields for the event object.
More detail on the field rules is available in the [Montandon model analysis](./model/model.md#event).

- Examples:
  - [Reference Event example](examples/item-ref-event-flood-PAR.json): Shows usage of the extension for a reference event
  <!-- - [Source Collection example](examples/collection-source-event-GLIDE.json): Shows the usage of the extension in a STAC Collection representing an event data source. -->
  - [Source Event example](examples/item-source-event-flood-PAR-GLIDE.json): Shows usage of the extension for a source event
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

### Event Fields

The fields described in this section are exclusively used in :

- [x] Item Properties (incl. Summaries in Collections)

#### STAC Item core fields best practises for event

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

The following field are specific to the Montandon model:

| Field Name          | Type      | Description                                                                                                                                                                                              |
| ------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| monty:country_codes | \[string] | **REQUIRED**. The country codes of the countries affected by the event. The country code follows [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard format.                 |
| monty:hazard_codes  | \[string] | **REQUIRED**. The hazard codes of the hazards affecting the event. The hazard code follows the [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips) identifier. |
| monty:corr_id       | string    | **REQUIRED**. The unique identifier assigned by the Monty system to the reference event used to "pair" all the instances of the same event.                                                              |

### Additional Field Information

#### monty:corr_id

It is the unique identifier assigned by the Monty system to the reference event.
This correlation identifier is critical to associate the events to the reference event.
Each source event MUST have one in order to make a search of the source events efficiently.
A source event should also contain a [`reference-event` link](#relation-types) to the reference event.

## Hazard

This section describes the mandatory fields for the hazard object.
More detail on the field rules is available in the [Montandon model analysis](./model/model.md#hazard).

- Examples:
  - [Hazard example](examples/item-hazard-flood-PAR.json): Shows usage of the extension for a flooding hazard

### Hazard Fields

The fields described in this section are exclusively used in :

- [x] Item Properties (incl. Summaries in Collections)

#### STAC Item core fields best practises for hazard

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

The following field are specific to the Montandon model:

| Field Name          | Type      | Description                                                                                                                                                                                              |
| ------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| monty:hazards_codes   | string    | **REQUIRED**. The hazard type of the hazard. The hazard type follows the [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips) identifier.                 |

## Relation types

The following types should be used as applicable `rel` types in the
[Link Object](https://github.com/radiantearth/stac-spec/tree/master/item-spec/item-spec.md#link-object).

| Type            | Description                           |
| --------------- | ------------------------------------- |
| reference-event | This link points to the the reference |

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
