# STAC-Based Correlation Algorithms

This document describes the dynamic correlation algorithms used to link Events, Hazards, and Impacts in the Monty system using STAC API queries.

## Overview

The Monty system uses **dynamic STAC API queries** to correlate disaster data items rather than relying solely on static correlation identifiers. This approach leverages the powerful filtering capabilities of the STAC API, particularly the CQL2 (Common Query Language) filter extension with array operations.

### Why Dynamic Correlation?

The shift from static [correlation identifiers](../correlation_identifier.md) to dynamic queries offers several advantages:

1. **Flexibility**: Users can adjust correlation criteria based on their specific needs
2. **Multi-hazard support**: Better handles complex events with multiple overlapping hazards
3. **Real-time correlation**: No pre-computation required - correlation happens at query time
4. **Transparency**: Users can see and customize the correlation logic
5. **Standards-based**: Uses STAC API specifications and conventions

### Correlation Criteria

Items in the Monty system can be correlated using the following attributes:

- **Hazard Codes** (`monty:hazard_codes`): Array of [hazard classification codes](../taxonomy.md#hazards) (UNDRR-ISC 2025, EM-DAT, GLIDE)
- **Country Codes** (`monty:country_codes`): Array of ISO 3166-1 alpha-3 country codes
- **Temporal Extent**: `datetime`, `start_datetime`, `end_datetime` properties
- **Spatial Extent**: GeoJSON `geometry` and `bbox` properties
- **Episode Number** (`monty:episode_number`): Distinguishes between episodes of the same event
- **Correlation ID** (`monty:corr_id`): Static identifier for backward compatibility

## Core Correlation Algorithms

### Algorithm 1: Event-to-Event Correlation

**Purpose**: Find all source events that describe the same disaster event from different data sources.

**Criteria**:
- Same or compatible hazard codes
- Same country code(s)
- Overlapping temporal extent
- Optional: Overlapping spatial extent

**CQL2-JSON Example**:

```json
{
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "a_overlaps",
        "args": [
          {"property": "monty:hazard_codes"},
          ["MH0600", "nat-hyd-flo-flo", "FL"]
        ]
      },
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:country_codes"},
          "ESP"
        ]
      },
      {
        "op": "t_intersects",
        "args": [
          {"property": "datetime"},
          {"interval": ["2024-10-27T00:00:00Z", "2024-10-28T00:00:00Z"]}
        ]
      },
      {
        "op": "in",
        "args": [
          "event",
          {"property": "roles"}
        ]
      }
    ]
  }
}
```

**CQL2-Text Example**:

```
roles IN ('event') AND 
a_overlaps(monty:hazard_codes, ARRAY['MH0600', 'nat-hyd-flo-flo', 'FL']) AND 
a_contains(monty:country_codes, 'ESP') AND 
t_intersects(datetime, INTERVAL('2024-10-27T00:00:00Z', '2024-10-28T00:00:00Z'))
```

**Use Cases**:
- Linking GDACS, GLIDE, EM-DAT, and other source events for the same disaster
- Finding all perspectives on a single event
- Data reconciliation and quality assessment

---

### Algorithm 2: Event-to-Hazard Correlation

**Purpose**: Find all hazard items associated with a specific event.

**Criteria**:
- Match by correlation ID if available
- OR match by hazard codes, country, and temporal/spatial overlap

**CQL2-JSON Example (using correlation ID)**:

```json
{
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "=",
        "args": [
          {"property": "monty:corr_id"},
          "20241027-ESP-FL-2-GCDB"
        ]
      },
      {
        "op": "in",
        "args": [
          "hazard",
          {"property": "roles"}
        ]
      }
    ]
  }
}
```

**CQL2-JSON Example (dynamic correlation)**:

```json
{
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "a_overlaps",
        "args": [
          {"property": "monty:hazard_codes"},
          ["MH0600", "nat-hyd-flo-flo"]
        ]
      },
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:country_codes"},
          "ESP"
        ]
      },
      {
        "op": "t_intersects",
        "args": [
          {"property": "datetime"},
          {"interval": ["2024-10-27T00:00:00Z", "2024-10-31T00:00:00Z"]}
        ]
      },
      {
        "op": "in",
        "args": [
          "hazard",
          {"property": "roles"}
        ]
      }
    ]
  }
}
```

**Use Cases**:
- Finding all hazard assessments for a disaster event
- Identifying specific hazards in multi-hazard events
- Analyzing hazard intensity and severity data

---

### Algorithm 3: Event-to-Impact Correlation

**Purpose**: Find all impact items related to a specific event.

**Criteria**:
- Match by correlation ID if available
- OR match by hazard codes, country, and temporal overlap
- Consider temporal lag (impacts may be reported days/weeks after the event)

**CQL2-JSON Example**:

```json
{
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "a_overlaps",
        "args": [
          {"property": "monty:hazard_codes"},
          ["MH0600", "FL"]
        ]
      },
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:country_codes"},
          "ESP"
        ]
      },
      {
        "op": "t_after",
        "args": [
          {"property": "datetime"},
          "2024-10-27T00:00:00Z"
        ]
      },
      {
        "op": "t_before",
        "args": [
          {"property": "datetime"},
          "2024-11-10T00:00:00Z"
        ]
      },
      {
        "op": "in",
        "args": [
          "impact",
          {"property": "roles"}
        ]
      }
    ]
  }
}
```

**Use Cases**:
- Aggregating all impacts from a disaster event
- Tracking impact evolution over time
- Comparing impact estimates from different sources

---

### Algorithm 4: Hazard-to-Impact Correlation

**Purpose**: Find impacts directly caused by specific hazards in multi-hazard events.

**Criteria**:
- Same correlation ID AND same hazard codes
- OR spatial intersection between hazard and impact geometries
- Temporal causality (impact occurs during or after hazard)

**CQL2-JSON Example**:

```json
{
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "=",
        "args": [
          {"property": "monty:corr_id"},
          "20241027-ESP-FL-2-GCDB"
        ]
      },
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:hazard_codes"},
          "MH0603"
        ]
      },
      {
        "op": "in",
        "args": [
          "impact",
          {"property": "roles"}
        ]
      }
    ]
  }
}
```

**Use Cases**:
- Attribution of impacts to specific hazards in cascading disasters
- Understanding which hazard caused which type of impact
- Multi-hazard risk analysis

---

## Array Operators Explained

The STAC Filter extension provides specialized operators for querying array fields:

### `a_equals`
**Exact match**: The array must be exactly equal to the provided array (same elements, same order).

```json
{
  "op": "a_equals",
  "args": [
    {"property": "monty:country_codes"},
    ["ESP"]
  ]
}
```
✅ Matches: `["ESP"]`  
❌ Does NOT match: `["ESP", "FRA"]` or `["FRA", "ESP"]`

### `a_contains`
**Contains element**: The array must contain the specified element(s).

```json
{
  "op": "a_contains",
  "args": [
    {"property": "monty:country_codes"},
    "ESP"
  ]
}
```
✅ Matches: `["ESP"]`, `["ESP", "FRA"]`, `["FRA", "ESP"]`  
❌ Does NOT match: `["FRA"]`, `["ITA"]`

### `a_overlaps`
**Overlaps**: At least one element from the query array must be present in the property array.

```json
{
  "op": "a_overlaps",
  "args": [
    {"property": "monty:hazard_codes"},
    ["MH0600", "MH0603", "FL"]
  ]
}
```
✅ Matches: `["MH0600"]`, `["FL", "nat-hyd-flo-flo"]`, `["MH0603", "MH0801"]`  
❌ Does NOT match: `["MH0801"]`, `["EQ"]`

### `a_containedBy`
**Contained by**: All elements in the property array must be present in the query array.

```json
{
  "op": "a_containedBy",
  "args": [
    {"property": "monty:hazard_codes"},
    ["MH0600", "MH0603", "FL", "nat-hyd-flo-flo"]
  ]
}
```
✅ Matches: `["FL"]`, `["MH0600", "MH0603"]`  
❌ Does NOT match: `["FL", "EQ"]` (EQ is not in the query array)

---

## Practical Examples

See [correlation_examples.md](./correlation_examples.md) for detailed real-world examples including:

- Spain October 2024 floods correlation
- Multi-country event correlation
- Cascading hazards (earthquake → tsunami → flooding)
- Python code examples using pystac-client

---

## Advanced Patterns

### Temporal Tolerance

Allow flexibility in temporal matching by using time windows:

```json
{
  "op": "t_intersects",
  "args": [
    {"property": "datetime"},
    {"interval": ["2024-10-26T00:00:00Z", "2024-10-29T23:59:59Z"]}
  ]
}
```

### Hazard Hierarchy Correlation

Use the 2025 UNDRR-ISC cluster structure to find related hazards:

```json
{
  "op": "or",
  "args": [
    {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "MH0600"]},
    {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "MH0601"]},
    {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "MH0602"]},
    {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "MH0603"]},
    {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "MH0604"]}
  ]
}
```

This finds all flooding types (coastal, estuarine, flash, fluvial, etc.) from the MH-WATER cluster.

### Spatial Tolerance

Use buffer zones for spatial correlation:

```json
{
  "op": "s_intersects",
  "args": [
    {"property": "geometry"},
    {
      "type": "Point",
      "coordinates": [-3.41102534556838, 38.6013316868745]
    }
  ]
}
```

Or use bounding boxes for regional correlation:

```json
{
  "op": "s_intersects",
  "args": [
    {"property": "geometry"},
    {
      "type": "Polygon",
      "coordinates": [[
        [-4.0, 38.0],
        [-3.0, 38.0],
        [-3.0, 39.0],
        [-4.0, 39.0],
        [-4.0, 38.0]
      ]]
    }
  ]
}
```

### Multi-Country Events

Find events affecting multiple countries:

```json
{
  "op": "and",
  "args": [
    {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "ESP"]},
    {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "FRA"]}
  ]
}
```

Or events affecting at least one country from a list:

```json
{
  "op": "a_overlaps",
  "args": [
    {"property": "monty:country_codes"},
    ["ESP", "FRA", "ITA"]
  ]
}
```

---

## Backward Compatibility

The `monty:corr_id` field remains available for:

1. **Legacy systems**: Existing integrations can continue using static correlation IDs
2. **Performance**: Direct ID matching is faster than complex spatial/temporal queries
3. **Deterministic linking**: When exact pairing is required

**Best Practice**: Use both approaches:
1. Generate `monty:corr_id` for reference events using the [existing algorithm](../correlation_identifier.md)
2. Populate this ID on all related items
3. Support dynamic queries for flexible correlation
4. Allow users to choose their preferred correlation method

---

## Implementation Guidance

### Query Performance

1. **Use indexes**: Ensure `monty:hazard_codes`, `monty:country_codes`, and `datetime` are indexed
2. **Filter progressively**: Start with the most selective criteria (e.g., country, date range)
3. **Limit results**: Use pagination for large result sets
4. **Cache results**: For frequently-used correlations, consider caching

### API Usage

The Montandon STAC API endpoint:
```
https://montandon-eoapi-stage.ifrc.org/stac
```

Use the `/search` endpoint with POST requests for complex filters:

```bash
curl -X POST 'https://montandon-eoapi-stage.ifrc.org/stac/search' \
  -H 'Content-Type: application/json' \
  -d '{
    "filter-lang": "cql2-json",
    "filter": { ... },
    "limit": 100
  }'
```

### Error Handling

Common issues and solutions:

1. **Timeout errors**: Simplify the query or add more specific filters
2. **Empty results**: Check that array operators are used correctly for array fields
3. **Unexpected results**: Verify hazard code compatibility across classification systems

---

## References

- [STAC Filter Extension](https://github.com/stac-api-extensions/filter)
- [CQL2 Specification](https://docs.ogc.org/DRAFTS/21-065.html)
- [Monty Taxonomy](../taxonomy.md)
- [Correlation Identifier (Legacy)](../correlation_identifier.md)
- [Query Examples](./correlation_examples.md)
