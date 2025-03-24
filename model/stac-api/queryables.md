# Queryables for Monty STAC Extension

This document describes the properties that can be used as queryables in a STAC API implementing the [Filter Extension](https://github.com/stac-api-extensions/filter) with the Monty STAC Extension.

## Overview

Queryables are a mechanism that allows clients to discover what terms are available for use when writing filter expressions in a STAC API. The Filter Extension enables clients to filter collections and items based on their properties using the Common Query Language (CQL2).

A STAC API implementing the Filter Extension exposes queryables via a JSON Schema document retrieved from the `/queryables` endpoint. This document describes the names and types of terms that may be used in filter expressions.

## Monty Extension Queryables

The following properties from the Monty STAC Extension can be used as queryables:

### Core Queryables

| Field Name           | Type          | Description                                                                                                                                                                                                                                                      |
| -------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| monty:episode_number | integer       | The episode number of the event. It is a unique identifier assigned by the Monty system to the event                                                                                                                                                             |
| monty:country_codes  | array[string] | The country codes of the countries affected by the event, hazard, impact or response. The country code follows [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard format                                                            |
| monty:corr_id        | string        | The unique identifier assigned by the Monty system to the reference event used to "pair" all the items of the same event. The correlation identifier follows a specific convention described in the [event correlation](../correlation_identifier.md) page |
| monty:hazard_codes   | array[string] | The hazard codes of the hazards affecting the event. For interoperability purpose, the array MUST contain at least one code from a [hazard classification system](../taxonomy.md#hazards)                                                                  |
| roles                | array[string] | The roles of the item. Used to identify the type of data (event, reference, source, hazard, impact, response)                                                                                                                                                    |

### Hazard Detail Queryables

The following properties from the `monty:hazard_detail` object can be used as queryables:

| Field Name                         | Type   | Description                                                                                              |
| ---------------------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| monty:hazard_detail.cluster        | string | The cluster of the hazard. The possible values are defined in [this table](../taxonomy.md#hazards) |
| monty:hazard_detail.severity_value | number | The estimated maximum hazard intensity/magnitude/severity value, as a number, without the units          |
| monty:hazard_detail.severity_unit  | string | The unit of the max_value                                                                                |
| monty:hazard_detail.estimate_type  | string | The type of the estimate. The possible values are `primary`, `secondary` and `modelled`                  |

### Impact Detail Queryables

The following properties from the `monty:impact_detail` object can be used as queryables:

| Field Name                        | Type   | Description                                                                                                                                                                                                 |
| --------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| monty:impact_detail.category      | string | The category of impact, which is the specific asset or population demographic that has been impacted by the hazard. The possible values are defined in [this table](../taxonomy.md#exposure-category) |
| monty:impact_detail.type          | string | The estimated value type of the impact. The possible values are defined in [this table](../taxonomy.md#impact-type)                                                                                   |
| monty:impact_detail.value         | number | The estimated impact value, as a number, without the units                                                                                                                                                  |
| monty:impact_detail.unit          | string | The units of the impact estimate                                                                                                                                                                            |
| monty:impact_detail.estimate_type | string | The type of the estimate. The possible values are `primary`, `secondary` and `modelled`                                                                                                                     |
| monty:impact_detail.description   | string | The description of the impact                                                                                                                                                                               |

## Example Queryables Definition

Below is an example of a queryables definition for a STAC API implementing the Monty STAC Extension:

```json
{
  "$schema": "https://json-schema.org/draft/2019-09/schema",
  "$id": "https://example.com/stac/queryables",
  "type": "object",
  "title": "Queryables for Monty STAC API",
  "description": "Queryable names for the Monty STAC API",
  "properties": {
    "id": {
      "description": "Item identifier",
      "type": "string"
    },
    "collection": {
      "description": "Collection identifier",
      "type": "string"
    },
    "datetime": {
      "description": "Datetime",
      "type": "string",
      "format": "date-time"
    },
    "geometry": {
      "description": "Geometry",
      "type": "object"
    },
    "monty:episode_number": {
      "description": "The episode number of the event",
      "type": "integer"
    },
    "monty:country_codes": {
      "description": "The country codes of the countries affected by the event, hazard, impact or response",
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^([A-Z]{3})|AB9$"
      }
    },
    "monty:corr_id": {
      "description": "The unique identifier assigned by the Monty system to the reference event",
      "type": "string"
    },
    "monty:hazard_codes": {
      "description": "The hazard codes of the hazards affecting the event",
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^([A-Z]{2}(?:\\d{4}$){0,1})|([a-z]{3}-[a-z]{3}-[a-z]{3}-[a-z]{3})|([A-Z]{2})$"
      }
    },
    "roles": {
      "description": "The roles of the item",
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["event", "reference", "source", "hazard", "impact", "response"]
      }
    },
    "monty:hazard_detail.cluster": {
      "description": "The cluster of the hazard",
      "type": "string"
    },
    "monty:hazard_detail.severity_value": {
      "description": "The estimated maximum hazard intensity/magnitude/severity value",
      "type": "number"
    },
    "monty:hazard_detail.severity_unit": {
      "description": "The unit of the severity value",
      "type": "string"
    },
    "monty:hazard_detail.estimate_type": {
      "description": "The type of the estimate",
      "type": "string",
      "enum": ["primary", "secondary", "modelled"]
    },
    "monty:impact_detail.category": {
      "description": "The category of impact",
      "type": "string",
      "enum": [
        "people", "crops", "women", "men", "children_0_4", "children_5_9", 
        "children_10_14", "children_15_19", "adult_20_24", "adult_25_29", 
        "adult_30_34", "adult_35_39", "adult_40_44", "adult_45_49", 
        "adult_50_54", "adult_55_59", "adult_60_64", "elderly", 
        "wheelchair_users", "roads", "railways", "vulnerable_employment", 
        "buildings", "reconstruction_costs", "hospitals", "schools", 
        "local_currency", "global_currency", "local_currency_adj", 
        "global_currency_adj", "usd_uncertain", "cattle", "aid_general", 
        "ifrc_contribution", "ifrc_requested", "alertscore", "households"
      ]
    },
    "monty:impact_detail.type": {
      "description": "The estimated value type of the impact",
      "type": "string",
      "enum": [
        "unspecified", "unaffected", "damaged", "destroyed", "potentially_damaged", 
        "affected_total", "affected_direct", "affected_indirect", "death", 
        "missing", "injured", "evacuated", "relocated", "assisted", 
        "shelter_emergency", "shelter_temporary", "shelter_longterm", "in_need", 
        "targeted", "disrupted", "cost", "homeless", "displaced_internal", 
        "displaced_external", "displaced_total", "alertscore", "potentially_affected", 
        "highest_risk"
      ]
    },
    "monty:impact_detail.value": {
      "description": "The estimated impact value",
      "type": "number"
    },
    "monty:impact_detail.unit": {
      "description": "The units of the impact estimate",
      "type": "string"
    },
    "monty:impact_detail.estimate_type": {
      "description": "The type of the estimate",
      "type": "string",
      "enum": ["primary", "secondary", "modelled"]
    },
    "monty:impact_detail.description": {
      "description": "The description of the impact",
      "type": "string"
    }
  },
  "additionalProperties": true
}
```

## Usage Examples

Here are some examples of CQL2 filter expressions using the Monty STAC Extension queryables:

**Find all items related to a specific event**

```console
monty:corr_id = '20241027T150000-ESP-HM-FLOOD-001-GCDB'
```

**Find all items related to events in a specific country**

```console
'ESP' IN monty:country_codes
```

**Find all items with a specific hazard code**

```console
'FL' IN monty:hazard_codes
```

**Find all reference events**

```console
'event' IN roles AND 'reference' IN roles
```

**Find all hazard items with high severity**

```console
'hazard' IN roles AND monty:hazard_detail.severity_value > 5
```

**Find all impact items with deaths**

```console
'impact' IN roles AND monty:impact_detail.type = 'death'
```

**Find all impact items with a specific category and above a certain value**

```console
'impact' IN roles AND monty:impact_detail.category = 'people' AND monty:impact_detail.value > 100
```

## Implementation Notes

When implementing queryables for the Monty STAC Extension in a STAC API:

1. The queryables endpoint should be available at `/queryables` for the entire catalog and at `/collections/{collectionId}/queryables` for specific collections.

2. The `additionalProperties` attribute in the queryables definition can be set to `true` to allow any syntactically-valid term for a property to be accepted. This is useful for STAC APIs with highly variable and dynamic content.

3. Fields in Item Properties should be exposed with their un-prefixed names, and not require expressions to prefix them with `properties`.

4. The Landing Page endpoint (`/`) should have a Link with rel `http://www.opengis.net/def/rel/ogc/1.0/queryables` with an href to the endpoint `/queryables`.

5. Each Collection resource should have a Link to the queryables resource for that collection, e.g., `/collections/collection1/queryables`.
