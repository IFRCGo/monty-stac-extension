# Correlation Algorithm Examples

This document provides practical, real-world examples of using the STAC-based correlation algorithms described in [correlation_algorithms.md](./correlation_algorithms.md).

## Example 1: Spain October 2024 Floods

### Scenario

On October 27, 2024, severe flooding struck Spain, primarily affecting the Valencia region. Multiple data sources recorded this event:
- **GLIDE**: FL-2024-000199-ESP
- **GDACS**: Event ID 1102983 (multiple episodes)
- **EM-DAT**: Event 2024-0796-ESP (potentially)

We want to correlate all events, hazards, and impacts related to this disaster.

---

### Step 1: Find All Related Events

**Goal**: Find all source events from different collections describing this flood.

**Known Information**:
- Event occurred on 2024-10-27
- Country: Spain (ESP)
- Hazard: Flood (MH0600, nat-hyd-flo-flo, FL)

**CQL2-JSON Query**:

```json
{
  "collections": [
    "glide-events",
    "gdacs-events",
    "emdat-events",
    "reference-events"
  ],
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:country_codes"},
          "ESP"
        ]
      },
      {
        "op": "a_overlaps",
        "args": [
          {"property": "monty:hazard_codes"},
          ["MH0600", "nat-hyd-flo-flo", "FL"]
        ]
      },
      {
        "op": "t_intersects",
        "args": [
          {"property": "datetime"},
          {"interval": ["2024-10-27T00:00:00Z", "2024-10-28T23:59:59Z"]}
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
  },
  "limit": 100
}
```

**Python Example using pystac-client**:

```python
from pystac_client import Client
from datetime import datetime

# Connect to Montandon STAC API
client = Client.open("https://montandon-eoapi-stage.ifrc.org/stac")

# Define the filter
filter_dict = {
    "op": "and",
    "args": [
        {
            "op": "a_contains",
            "args": [
                {"property": "monty:country_codes"},
                "ESP"
            ]
        },
        {
            "op": "a_overlaps",
            "args": [
                {"property": "monty:hazard_codes"},
                ["MH0600", "nat-hyd-flo-flo", "FL"]
            ]
        },
        {
            "op": "t_intersects",
            "args": [
                {"property": "datetime"},
                {"interval": ["2024-10-27T00:00:00Z", "2024-10-28T23:59:59Z"]}
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

# Search for events
search = client.search(
    collections=["glide-events", "gdacs-events", "emdat-events", "reference-events"],
    filter=filter_dict,
    filter_lang="cql2-json",
    limit=100
)

# Retrieve all matching items
events = list(search.items())

print(f"Found {len(events)} related events:")
for event in events:
    print(f"  - {event.id} from {event.collection_id}")
    print(f"    Correlation ID: {event.properties.get('monty:corr_id', 'N/A')}")
    print(f"    Date: {event.properties.get('datetime')}")
```

**Expected Results**:
- `glide-event-FL-2024-000199-ESP` (GLIDE event)
- `gdacs-event-1102983-1` (GDACS episode 1)
- `gdacs-event-1102983-2` (GDACS episode 2)
- Potentially EM-DAT and reference events

**Result Analysis**:
All events should share similar correlation IDs (e.g., `20241027-ESP-FL-1-GCDB` or `20241027-ESP-FL-2-GCDB` depending on episode).

---

### Step 2: Find All Hazards for the Event

**Goal**: Once we've identified the events, find all hazard assessments.

**Using correlation ID** (if known):

```json
{
  "collections": ["glide-hazards", "gdacs-hazards", "usgs-hazards"],
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

**Dynamic correlation** (without correlation ID):

```json
{
  "collections": ["glide-hazards", "gdacs-hazards", "ifrcevent-hazards"],
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:country_codes"},
          "ESP"
        ]
      },
      {
        "op": "a_overlaps",
        "args": [
          {"property": "monty:hazard_codes"},
          ["MH0600", "MH0603", "nat-hyd-flo-flo", "nat-hyd-flo-fla", "FL", "FF"]
        ]
      },
      {
        "op": "t_intersects",
        "args": [
          {"property": "datetime"},
          {"interval": ["2024-10-27T00:00:00Z", "2024-10-31T23:59:59Z"]}
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

**Python Example**:

```python
def find_hazards_for_event(client, country_code, hazard_codes, start_date, end_date):
    """
    Find all hazards matching the given criteria.
    
    Args:
        client: pystac_client.Client instance
        country_code: ISO 3166-1 alpha-3 country code
        hazard_codes: List of hazard codes to search for
        start_date: Start datetime as ISO string
        end_date: End datetime as ISO string
    
    Returns:
        List of pystac.Item objects
    """
    filter_dict = {
        "op": "and",
        "args": [
            {
                "op": "a_contains",
                "args": [
                    {"property": "monty:country_codes"},
                    country_code
                ]
            },
            {
                "op": "a_overlaps",
                "args": [
                    {"property": "monty:hazard_codes"},
                    hazard_codes
                ]
            },
            {
                "op": "t_intersects",
                "args": [
                    {"property": "datetime"},
                    {"interval": [start_date, end_date]}
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
    
    search = client.search(
        collections=["glide-hazards", "gdacs-hazards", "ifrcevent-hazards", "usgs-hazards"],
        filter=filter_dict,
        filter_lang="cql2-json",
        limit=100
    )
    
    return list(search.items())

# Usage
hazards = find_hazards_for_event(
    client,
    "ESP",
    ["MH0600", "MH0603", "nat-hyd-flo-flo", "FL"],
    "2024-10-27T00:00:00Z",
    "2024-10-31T23:59:59Z"
)

print(f"Found {len(hazards)} related hazards:")
for hazard in hazards:
    detail = hazard.properties.get("monty:hazard_detail", {})
    print(f"  - {hazard.id}")
    print(f"    Severity: {detail.get('severity_value')} {detail.get('severity_unit')}")
```

**Expected Results**:
- Hazard assessments from GLIDE, GDACS, and potentially other sources
- Each hazard item contains severity/magnitude information

---

### Step 3: Find All Impacts

**Goal**: Find all impact estimates (casualties, damages, displacement) for the event.

**Query** (allowing for reporting delays):

```json
{
  "collections": ["gdacs-impacts", "emdat-impacts", "idmc-gidd-impacts", "idmc-idu-impacts"],
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "a_contains",
        "args": [
          {"property": "monty:country_codes"},
          "ESP"
        ]
      },
      {
        "op": "a_overlaps",
        "args": [
          {"property": "monty:hazard_codes"},
          ["MH0600", "FL", "nat-hyd-flo-flo"]
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
          "2024-11-15T00:00:00Z"
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

**Python Example with Impact Analysis**:

```python
def aggregate_impacts(impacts):
    """
    Aggregate impact data by type and category.
    
    Args:
        impacts: List of pystac.Item objects with impact data
    
    Returns:
        Dictionary with aggregated impact statistics
    """
    aggregated = {}
    
    for impact in impacts:
        detail = impact.properties.get("monty:impact_detail", {})
        category = detail.get("category", "unknown")
        impact_type = detail.get("type", "unknown")
        value = detail.get("value", 0)
        
        key = f"{category}_{impact_type}"
        if key not in aggregated:
            aggregated[key] = {
                "category": category,
                "type": impact_type,
                "total": 0,
                "sources": []
            }
        
        aggregated[key]["total"] += value
        aggregated[key]["sources"].append({
            "id": impact.id,
            "value": value,
            "source": impact.properties.get("source", "unknown"),
            "datetime": impact.properties.get("datetime")
        })
    
    return aggregated

# Find impacts
def find_impacts_for_event(client, country_code, hazard_codes, start_date, end_date):
    filter_dict = {
        "op": "and",
        "args": [
            {"op": "a_contains", "args": [{"property": "monty:country_codes"}, country_code]},
            {"op": "a_overlaps", "args": [{"property": "monty:hazard_codes"}, hazard_codes]},
            {"op": "t_after", "args": [{"property": "datetime"}, start_date]},
            {"op": "t_before", "args": [{"property": "datetime"}, end_date]},
            {"op": "in", "args": ["impact", {"property": "roles"}]}
        ]
    }
    
    search = client.search(
        collections=["gdacs-impacts", "emdat-impacts", "idmc-gidd-impacts", "idmc-idu-impacts"],
        filter=filter_dict,
        filter_lang="cql2-json",
        limit=500
    )
    
    return list(search.items())

impacts = find_impacts_for_event(
    client,
    "ESP",
    ["MH0600", "FL"],
    "2024-10-27T00:00:00Z",
    "2024-11-15T00:00:00Z"
)

# Aggregate
aggregated = aggregate_impacts(impacts)

print("Impact Summary:")
for key, data in aggregated.items():
    print(f"\n{data['category']} - {data['type']}:")
    print(f"  Total: {data['total']}")
    print(f"  Sources: {len(data['sources'])}")
    for source in data['sources']:
        print(f"    - {source['source']}: {source['value']} (reported {source['datetime']})")
```

**Expected Results**:
- Death counts from multiple sources
- Missing persons estimates
- Displaced/evacuated populations
- Economic losses
- Infrastructure damage

---

### Step 4: Correlation by Static ID

**Goal**: Use the correlation ID for deterministic linking.

**Query**:

```python
def find_all_related_by_corr_id(client, corr_id):
    """
    Find all items (events, hazards, impacts) with a specific correlation ID.
    
    Args:
        client: pystac_client.Client instance
        corr_id: Correlation ID string (e.g., "20241027-ESP-FL-2-GCDB")
    
    Returns:
        Dictionary with items grouped by type
    """
    filter_dict = {
        "op": "=",
        "args": [
            {"property": "monty:corr_id"},
            corr_id
        ]
    }
    
    search = client.search(
        filter=filter_dict,
        filter_lang="cql2-json",
        limit=500
    )
    
    items = list(search.items())
    
    # Group by roles
    grouped = {
        "events": [],
        "hazards": [],
        "impacts": [],
        "responses": []
    }
    
    for item in items:
        roles = item.properties.get("roles", [])
        if "event" in roles:
            grouped["events"].append(item)
        if "hazard" in roles:
            grouped["hazards"].append(item)
        if "impact" in roles:
            grouped["impacts"].append(item)
        if "response" in roles:
            grouped["responses"].append(item)
    
    return grouped

# Usage
corr_id = "20241027-ESP-FL-2-GCDB"
related = find_all_related_by_corr_id(client, corr_id)

print(f"Items with correlation ID {corr_id}:")
print(f"  Events: {len(related['events'])}")
print(f"  Hazards: {len(related['hazards'])}")
print(f"  Impacts: {len(related['impacts'])}")
print(f"  Responses: {len(related['responses'])}")
```

---

## Example 2: Multi-Hazard Event (Earthquake → Tsunami)

### Scenario

A magnitude 7.5 earthquake strikes near Japan, triggering a tsunami that affects multiple countries.

**Primary Hazard**: Earthquake (GH0101)  
**Secondary Hazard**: Tsunami (MH0705)  
**Countries**: Japan (JPN), potentially others

### Find Primary Event

```python
# Find the earthquake event
earthquake_filter = {
    "op": "and",
    "args": [
        {
            "op": "a_contains",
            "args": [{"property": "monty:hazard_codes"}, "GH0101"]
        },
        {
            "op": "a_contains",
            "args": [{"property": "monty:country_codes"}, "JPN"]
        },
        {
            "op": "t_after",
            "args": [{"property": "datetime"}, "2024-01-01T00:00:00Z"]
        },
        {
            "op": "in",
            "args": ["event", {"property": "roles"}]
        }
    ]
}
```

### Find Triggered Hazards

```python
# Find tsunami hazards that occurred after the earthquake
tsunami_filter = {
    "op": "and",
    "args": [
        {
            "op": "a_contains",
            "args": [{"property": "monty:hazard_codes"}, "MH0705"]
        },
        {
            "op": "or",
            "args": [
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "JPN"]},
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "RUS"]},
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "USA"]}
            ]
        },
        {
            "op": "t_after",
            "args": [{"property": "datetime"}, "2024-01-01T00:00:00Z"]
        },
        {
            "op": "t_before",
            "args": [{"property": "datetime"}, "2024-01-01T06:00:00Z"]  # Within 6 hours
        },
        {
            "op": "in",
            "args": ["hazard", {"property": "roles"}]
        }
    ]
}
```

### Analyze Cascading Impacts

```python
def find_cascading_impacts(client, primary_corr_id, secondary_hazard_codes, time_window_hours=48):
    """
    Find impacts from cascading hazards.
    """
    # First, find the primary event datetime
    primary_search = client.search(
        filter={
            "op": "and",
            "args": [
                {"op": "=", "args": [{"property": "monty:corr_id"}, primary_corr_id]},
                {"op": "in", "args": ["event", {"property": "roles"}]}
            ]
        },
        filter_lang="cql2-json",
        limit=1
    )
    
    primary_event = next(primary_search.items())
    primary_datetime = primary_event.properties["datetime"]
    
    # Calculate end time for search window
    from datetime import datetime, timedelta
    start = datetime.fromisoformat(primary_datetime.replace('Z', '+00:00'))
    end = start + timedelta(hours=time_window_hours)
    
    # Find impacts from secondary hazards
    impact_filter = {
        "op": "and",
        "args": [
            {
                "op": "a_overlaps",
                "args": [{"property": "monty:hazard_codes"}, secondary_hazard_codes]
            },
            {
                "op": "t_during",
                "args": [
                    {"property": "datetime"},
                    {"interval": [primary_datetime, end.isoformat()]}
                ]
            },
            {"op": "in", "args": ["impact", {"property": "roles"}]}
        ]
    }
    
    search = client.search(
        filter=impact_filter,
        filter_lang="cql2-json",
        limit=500
    )
    
    return list(search.items())
```

---

## Example 3: Regional Multi-Country Event

### Scenario

Flooding affects multiple countries in Southeast Asia during monsoon season.

**Countries**: Thailand (THA), Vietnam (VNM), Cambodia (KHM)  
**Hazard**: Flooding (MH0600 series)  
**Time Period**: July-September 2024

### Find All Events in the Region

```python
def find_regional_events(client, country_codes, hazard_codes, start_date, end_date):
    """
    Find events affecting multiple countries in a region.
    """
    filter_dict = {
        "op": "and",
        "args": [
            {
                "op": "a_overlaps",
                "args": [
                    {"property": "monty:country_codes"},
                    country_codes
                ]
            },
            {
                "op": "a_overlaps",
                "args": [
                    {"property": "monty:hazard_codes"},
                    hazard_codes
                ]
            },
            {
                "op": "t_during",
                "args": [
                    {"property": "datetime"},
                    {"interval": [start_date, end_date]}
                ]
            },
            {"op": "in", "args": ["event", {"property": "roles"}]}
        ]
    }
    
    search = client.search(
        filter=filter_dict,
        filter_lang="cql2-json",
        limit=500
    )
    
    return list(search.items())

# Usage
events = find_regional_events(
    client,
    ["THA", "VNM", "KHM"],
    ["MH0600", "MH0603", "MH0604", "FL"],
    "2024-07-01T00:00:00Z",
    "2024-09-30T23:59:59Z"
)

# Group by country
by_country = {}
for event in events:
    countries = event.properties.get("monty:country_codes", [])
    for country in countries:
        if country not in by_country:
            by_country[country] = []
        by_country[country].append(event)

for country, country_events in by_country.items():
    print(f"{country}: {len(country_events)} events")
```

---

## Example 4: Complete Correlation Workflow

This comprehensive example demonstrates a complete correlation workflow from event discovery to impact analysis.

```python
from pystac_client import Client
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class MontyCorrelator:
    """
    Helper class for correlating disaster events, hazards, and impacts.
    """
    
    def __init__(self, stac_url: str = "https://montandon-eoapi-stage.ifrc.org/stac"):
        self.client = Client.open(stac_url)
    
    def find_events(
        self,
        country_codes: List[str],
        hazard_codes: List[str],
        start_date: str,
        end_date: str,
        collections: List[str] = None
    ) -> List[Any]:
        """Find events matching criteria."""
        if collections is None:
            collections = [
                "glide-events", "gdacs-events", "emdat-events",
                "reference-events", "ifrcevent-events"
            ]
        
        filter_dict = {
            "op": "and",
            "args": [
                {
                    "op": "a_overlaps",
                    "args": [{"property": "monty:country_codes"}, country_codes]
                },
                {
                    "op": "a_overlaps",
                    "args": [{"property": "monty:hazard_codes"}, hazard_codes]
                },
                {
                    "op": "t_intersects",
                    "args": [
                        {"property": "datetime"},
                        {"interval": [start_date, end_date]}
                    ]
                },
                {"op": "in", "args": ["event", {"property": "roles"}]}
            ]
        }
        
        search = self.client.search(
            collections=collections,
            filter=filter_dict,
            filter_lang="cql2-json",
            limit=100
        )
        
        return list(search.items())
    
    def find_hazards_for_correlation_id(self, corr_id: str) -> List[Any]:
        """Find all hazards for a specific correlation ID."""
        filter_dict = {
            "op": "and",
            "args": [
                {"op": "=", "args": [{"property": "monty:corr_id"}, corr_id]},
                {"op": "in", "args": ["hazard", {"property": "roles"}]}
            ]
        }
        
        search = self.client.search(
            filter=filter_dict,
            filter_lang="cql2-json",
            limit=100
        )
        
        return list(search.items())
    
    def find_impacts_for_correlation_id(
        self,
        corr_id: str,
        impact_categories: List[str] = None
    ) -> List[Any]:
        """Find impacts for a specific correlation ID."""
        filter_args = [
            {"op": "=", "args": [{"property": "monty:corr_id"}, corr_id]},
            {"op": "in", "args": ["impact", {"property": "roles"}]}
        ]
        
        filter_dict = {
            "op": "and",
            "args": filter_args
        }
        
        search = self.client.search(
            filter=filter_dict,
            filter_lang="cql2-json",
            limit=500
        )
        
        return list(search.items())
    
    def get_complete_event_data(self, corr_id: str) -> Dict[str, Any]:
        """
        Get complete data for an event including all related items.
        
        Returns:
            Dictionary with events, hazards, impacts, and responses
        """
        # Find all items with this correlation ID
        filter_dict = {
            "op": "=",
            "args": [{"property": "monty:corr_id"}, corr_id]
        }
        
        search = self.client.search(
            filter=filter_dict,
            filter_lang="cql2-json",
            limit=1000
        )
        
        items = list(search.items())
        
        # Group by type
        result = {
            "correlation_id": corr_id,
            "events": [],
            "hazards": [],
            "impacts": [],
            "responses": []
        }
        
        for item in items:
            roles = item.properties.get("roles", [])
            
            if "event" in roles:
                result["events"].append(self._extract_item_info(item))
            if "hazard" in roles:
                result["hazards"].append(self._extract_hazard_info(item))
            if "impact" in roles:
                result["impacts"].append(self._extract_impact_info(item))
            if "response" in roles:
                result["responses"].append(self._extract_item_info(item))
        
        return result
    
    def _extract_item_info(self, item: Any) -> Dict[str, Any]:
        """Extract basic information from an item."""
        return {
            "id": item.id,
            "collection": item.collection_id,
            "datetime": item.properties.get("datetime"),
            "countries": item.properties.get("monty:country_codes", []),
            "hazards": item.properties.get("monty:hazard_codes", []),
            "source": item.properties.get("source", "unknown")
        }
    
    def _extract_hazard_info(self, item: Any) -> Dict[str, Any]:
        """Extract hazard-specific information."""
        info = self._extract_item_info(item)
        detail = item.properties.get("monty:hazard_detail", {})
        info.update({
            "severity_value": detail.get("severity_value"),
            "severity_unit": detail.get("severity_unit"),
            "estimate_type": detail.get("estimate_type")
        })
        return info
    
    def _extract_impact_info(self, item: Any) -> Dict[str, Any]:
        """Extract impact-specific information."""
        info = self._extract_item_info(item)
        detail = item.properties.get("monty:impact_detail", {})
        info.update({
            "category": detail.get("category"),
            "type": detail.get("type"),
            "value": detail.get("value"),
            "unit": detail.get("unit")
        })
        return info

# Example usage
if __name__ == "__main__":
    correlator = MontyCorrelator()
    
    # Find Spain floods
    print("Finding Spain flood events...")
    events = correlator.find_events(
        country_codes=["ESP"],
        hazard_codes=["MH0600", "FL", "nat-hyd-flo-flo"],
        start_date="2024-10-27T00:00:00Z",
        end_date="2024-10-28T23:59:59Z"
    )
    
    print(f"Found {len(events)} events")
    
    # Get complete data for first event
    if events:
        corr_id = events[0].properties.get("monty:corr_id")
        if corr_id:
            print(f"\nGetting complete data for correlation ID: {corr_id}")
            complete_data = correlator.get_complete_event_data(corr_id)
            
            print(json.dumps(complete_data, indent=2))
```

---

## Additional Resources

- [Correlation Algorithms Overview](./correlation_algorithms.md)
- [pystac-monty](https://github.com/IFRCGo/pystac-monty)
- [STAC Filter Extension Documentation](https://github.com/stac-api-extensions/filter)
- [CQL2 Specification](https://docs.ogc.org/DRAFTS/21-065.html)
- [Monty Data Model](../README.md)
