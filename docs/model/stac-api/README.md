# STAC API Documentation

This directory contains documentation for querying and correlating disaster data using the Montandon STAC API.

## Overview

The Montandon system uses STAC (SpatioTemporal Asset Catalog) API with the Filter extension (CQL2) to provide powerful querying capabilities for disaster events, hazards, and impacts data.

**STAC API Endpoint**: `https://montandon-eoapi-stage.ifrc.org/stac`

> [!Note]
> This is a staging endpoint. Production endpoint will be provided upon release.

## Documentation Files

### [correlation_algorithms.md](./correlation_algorithms.md)
**Main algorithm specification document**

Describes the dynamic correlation algorithms for linking events, hazards, and impacts using STAC API queries.

**Contents**:
- Overview of dynamic vs. static correlation
- Core correlation algorithms (Event-to-Event, Event-to-Hazard, Event-to-Impact, Hazard-to-Impact)
- Array operators explained (`a_contains`, `a_overlaps`, etc.)
- Advanced patterns (temporal tolerance, hazard hierarchy, spatial correlation)
- Performance considerations

**Audience**: Developers implementing correlation logic, data analysts designing queries

---

### [correlation_examples.md](./correlation_examples.md)
**Practical examples with complete code**

Real-world correlation examples with working Python code using pystac-client.

**Contents**:
- Spain October 2024 floods (complete workflow)
- Multi-hazard cascading events (earthquake → tsunami)
- Regional multi-country events (Southeast Asia floods)
- Complete correlation workflow with helper classes
- Impact aggregation and analysis

**Audience**: Developers integrating with Montandon API, data scientists analyzing disaster data

---

### [migration_guide.md](./migration_guide.md)
**Transition guide from static to dynamic correlation**

Helps users migrate from the legacy static correlation identifier system to the new dynamic approach.

**Contents**:
- Migration path and phases
- When to use each approach
- Practical migration examples
- Performance comparisons
- Testing and validation
- Common issues and solutions

**Audience**: Existing Montandon users, system integrators, project managers

---

### [queryables.md](./queryables.md)
**Queryable properties reference**

Lists all queryable properties available in the Montandon STAC API and how to use them.

**Contents**: *(To be created)*
- Standard STAC properties
- Montandon extension properties
- Property types and schemas
- Usage examples

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pystac-client
```

### 2. Connect to API

```python
from pystac_client import Client

client = Client.open("https://montandon-eoapi-stage.ifrc.org/stac")
```

### 3. Find Events for a Country and Hazard

```python
# Find flood events in Spain during October 2024
search = client.search(
    collections=["glide-events", "gdacs-events"],
    filter={
        "op": "and",
        "args": [
            {
                "op": "a_contains",
                "args": [{"property": "monty:country_codes"}, "ESP"]
            },
            {
                "op": "a_contains",
                "args": [{"property": "monty:hazard_codes"}, "MH0600"]
            },
            {
                "op": "t_during",
                "args": [
                    {"property": "datetime"},
                    {"interval": ["2024-10-01T00:00:00Z", "2024-10-31T23:59:59Z"]}
                ]
            }
        ]
    },
    filter_lang="cql2-json",
    limit=100
)

for item in search.items():
    print(f"{item.id}: {item.properties.get('title')}")
```

### 4. Find Related Hazards and Impacts

```python
# Get correlation ID from an event
corr_id = item.properties.get("monty:corr_id")

# Find all related hazards
hazards = client.search(
    filter={
        "op": "and",
        "args": [
            {"op": "=", "args": [{"property": "monty:corr_id"}, corr_id]},
            {"op": "in", "args": ["hazard", {"property": "roles"}]}
        ]
    },
    filter_lang="cql2-json"
)

# Find all related impacts
impacts = client.search(
    filter={
        "op": "and",
        "args": [
            {"op": "=", "args": [{"property": "monty:corr_id"}, corr_id]},
            {"op": "in", "args": ["impact", {"property": "roles"}]}
        ]
    },
    filter_lang="cql2-json"
)
```

For complete examples, see [correlation_examples.md](./correlation_examples.md).

---

## Key Concepts

### Array Operators

The STAC Filter extension provides specialized operators for array fields like `monty:hazard_codes` and `monty:country_codes`:

| Operator | Description | Example |
|----------|-------------|---------|
| `a_contains` | Array contains element | `["MH0600", "FL"]` contains `"MH0600"` ✅ |
| `a_overlaps` | Arrays share at least one element | `["MH0600"]` overlaps `["MH0600", "MH0603"]` ✅ |
| `a_equals` | Arrays are exactly equal | `["ESP"]` equals `["ESP"]` ✅, not `["ESP", "FRA"]` ❌ |
| `a_containedBy` | All elements are in the other array | `["FL"]` contained by `["FL", "MH0600"]` ✅ |

**Important**: Use array operators for array fields. Regular `=` operator only works for exact array matching.

### Temporal Operators

| Operator | Description |
|----------|-------------|
| `t_intersects` | Time ranges overlap |
| `t_during` | Item time is within period |
| `t_after` | Item time is after point |
| `t_before` | Item time is before point |

### Spatial Operators

| Operator | Description |
|----------|-------------|
| `s_intersects` | Geometries intersect |
| `s_contains` | Geometry contains another |
| `s_within` | Geometry is within another |

---

## Common Patterns

### Pattern 1: Find Events by Location and Hazard Type

```python
search = client.search(
    filter={
        "op": "and",
        "args": [
            {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "ESP"]},
            {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "MH0600"]},
            {"op": "in", "args": ["event", {"property": "roles"}]}
        ]
    },
    filter_lang="cql2-json"
)
```

### Pattern 2: Find All Data for a Correlation ID

```python
search = client.search(
    filter={
        "op": "=",
        "args": [{"property": "monty:corr_id"}, "20241027-ESP-FL-2-GCDB"]
    },
    filter_lang="cql2-json"
)
```

### Pattern 3: Multi-Hazard Query

```python
# Find events with either flooding or landslides
search = client.search(
    filter={
        "op": "and",
        "args": [
            {
                "op": "a_overlaps",
                "args": [
                    {"property": "monty:hazard_codes"},
                    ["MH0600", "GH0300", "nat-hyd-flo-flo", "nat-geo-mmd-lan"]
                ]
            },
            {"op": "in", "args": ["event", {"property": "roles"}]}
        ]
    },
    filter_lang="cql2-json"
)
```

### Pattern 4: Regional Analysis

```python
# Find disasters affecting multiple countries
search = client.search(
    filter={
        "op": "and",
        "args": [
            {
                "op": "a_overlaps",
                "args": [
                    {"property": "monty:country_codes"},
                    ["THA", "VNM", "KHM", "LAO"]
                ]
            },
            {
                "op": "t_during",
                "args": [
                    {"property": "datetime"},
                    {"interval": ["2024-06-01T00:00:00Z", "2024-09-30T23:59:59Z"]}
                ]
            }
        ]
    },
    filter_lang="cql2-json"
)
```

---

## Collections

The Montandon STAC API organizes data into collections by source and data type:

### Event Collections
- `glide-events` - GLIDE source events
- `gdacs-events` - GDACS source events
- `emdat-events` - EM-DAT source events
- `usgs-events` - USGS earthquake events
- `ibtracs-events` - IBTrACS tropical cyclone events
- `idmc-gidd-events` - IDMC GIDD displacement events
- `idmc-idu-events` - IDMC IDU displacement events
- `ifrcevent-events` - IFRC events
- `reference-events` - Reference correlation events

### Hazard Collections
- `glide-hazards` - GLIDE hazard assessments
- `gdacs-hazards` - GDACS hazard assessments
- `usgs-hazards` - USGS earthquake hazards (shakemaps)
- `ibtracs-hazards` - IBTrACS cyclone hazards
- `ifrcevent-hazards` - IFRC hazard data

### Impact Collections
- `gdacs-impacts` - GDACS impact estimates
- `emdat-impacts` - EM-DAT impact data
- `idmc-gidd-impacts` - IDMC GIDD displacement impacts
- `idmc-idu-impacts` - IDMC IDU displacement impacts
- `usgs-impacts` - USGS earthquake impacts
- `desinventar-impacts` - DesInventar impact data
- `ifrcevent-impacts` - IFRC impact data

---

## Resources

### External Documentation
- [STAC Specification](https://stacspec.org/)
- [STAC Filter Extension](https://github.com/stac-api-extensions/filter)
- [CQL2 Specification](https://docs.ogc.org/DRAFTS/21-065.html)
- [pystac-client Documentation](https://pystac-client.readthedocs.io/)

### Montandon Documentation
- [Data Model](../README.md)
- [Taxonomy](../taxonomy.md)
- [Legacy Correlation Identifier](../correlation_identifier.md)

### Support
- GitHub: [IFRCGo/monty-stac-extension](https://github.com/IFRCGo/monty-stac-extension)
- IFRC GO: [go.ifrc.org](https://go.ifrc.org)

---

## Examples by Use Case

| Use Case | Document | Section |
|----------|----------|---------|
| Find all data for a disaster | [correlation_examples.md](./correlation_examples.md) | Example 1: Spain October 2024 Floods |
| Track cascading hazards | [correlation_examples.md](./correlation_examples.md) | Example 2: Multi-Hazard Event |
| Regional disaster analysis | [correlation_examples.md](./correlation_examples.md) | Example 3: Regional Multi-Country Event |
| Migrate from old system | [migration_guide.md](./migration_guide.md) | Migration Path |
| Build custom correlation | [correlation_algorithms.md](./correlation_algorithms.md) | Advanced Patterns |
| Optimize query performance | [migration_guide.md](./migration_guide.md) | Performance Considerations |

---

## Contributing

To contribute to this documentation:

1. Review existing algorithms and examples
2. Test queries against the staging API
3. Submit pull requests with improvements
4. Report issues or request features

---

Last Updated: November 2025
