# Migration Guide: Static to Dynamic Correlation

This guide helps you transition from the static correlation identifier system to the dynamic STAC-based correlation approach.

## Overview

The Monty system is evolving from a **static correlation identifier** approach to a **dynamic STAC query-based** correlation system while maintaining backward compatibility.

### What's Changing

| Aspect | Old Approach | New Approach |
|--------|-------------|--------------|
| **Correlation Method** | Pre-generated correlation ID | Dynamic STAC API queries |
| **Flexibility** | Fixed at ingestion time | Flexible at query time |
| **Multi-hazard Support** | Limited | Comprehensive |
| **Query Complexity** | Simple ID match | Complex CQL2 filters |
| **Performance** | Very fast (direct ID lookup) | Fast (indexed queries) |

### What's NOT Changing

- The `monty:corr_id` field remains available and will continue to be populated
- All existing APIs and integrations continue to work
- The data model structure (events, hazards, impacts) remains the same

---

## Why Migrate?

### Benefits of Dynamic Correlation

1. **Flexibility**: Adjust correlation criteria based on your specific needs
   - Different time windows for different hazard types
   - Variable spatial tolerances
   - Custom hazard code mapping

2. **Multi-hazard Events**: Better support for complex disasters
   - Link cascading hazards (earthquake → landslide → flooding)
   - Track concurrent hazards (drought + heatwave)
   - Identify secondary impacts

3. **Cross-classification Support**: Work with multiple hazard taxonomies
   - Query using GLIDE, EM-DAT, or UNDRR-ISC 2025 codes
   - Find events regardless of which classification was used

4. **No Pre-computation**: Correlation happens at query time
   - No need to wait for correlation ID generation
   - Can re-correlate data with different criteria

5. **Transparency**: See exactly how items are being correlated
   - Understand the logic
   - Customize for specific use cases

### When to Use Each Approach

**Use Static Correlation IDs when:**
- ✅ You need maximum performance
- ✅ You need deterministic, reproducible results
- ✅ You're working with already-correlated datasets
- ✅ You need simple integration

**Use Dynamic Queries when:**
- ✅ You need flexibility in correlation criteria
- ✅ You're analyzing multi-hazard events
- ✅ You're working across multiple hazard classifications
- ✅ You need to correlate new/streaming data
- ✅ You want to explore different correlation strategies

---

## Migration Path

### Phase 1: Dual Support (Current)

**Status**: Both systems are fully supported

**What you can do**:
- Continue using `monty:corr_id` for all existing workflows
- Start experimenting with dynamic queries
- Compare results between both approaches
- Test performance for your use cases

**Example - Finding Related Events**:

```python
# Old approach (still works)
def find_related_old(client, corr_id):
    return client.search(
        filter={
            "op": "=",
            "args": [{"property": "monty:corr_id"}, corr_id]
        },
        filter_lang="cql2-json"
    )

# New approach (now available)
def find_related_new(client, country, hazards, start_date, end_date):
    return client.search(
        filter={
            "op": "and",
            "args": [
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, country]},
                {"op": "a_overlaps", "args": [{"property": "monty:hazard_codes"}, hazards]},
                {"op": "t_intersects", "args": [{"property": "datetime"}, {"interval": [start_date, end_date]}]}
            ]
        },
        filter_lang="cql2-json"
    )

# Hybrid approach (recommended for migration)
def find_related_hybrid(client, corr_id=None, country=None, hazards=None, dates=None):
    """
    Try correlation ID first, fall back to dynamic queries.
    """
    if corr_id:
        results = find_related_old(client, corr_id)
        items = list(results.items())
        if items:
            return items
    
    # Fall back to dynamic correlation
    if country and hazards and dates:
        return list(find_related_new(client, country, hazards, dates[0], dates[1]).items())
    
    return []
```

### Phase 2: Enhanced Dynamic Queries (Next 6-12 months)

**Planned enhancements**:
- Optimized indexes for common query patterns
- Query templates for standard correlation scenarios
- Helper libraries in multiple languages
- Performance monitoring and optimization

**What you should do**:
- Start using dynamic queries for new integrations
- Gradually migrate existing workflows
- Provide feedback on query performance
- Report any issues or limitations

### Phase 3: Deprecation Notice (12-24 months)

**Future considerations**:
- `monty:corr_id` will remain available but may not be the primary method
- Documentation will emphasize dynamic queries
- New features will be optimized for dynamic correlation
- Static IDs will still be generated for backward compatibility

**No breaking changes planned** - existing code will continue to work.

---

## Practical Migration Examples

### Example 1: Simple Event Lookup

**Before** (using correlation ID):

```python
def get_event_data(client, corr_id):
    search = client.search(
        filter={
            "op": "=",
            "args": [{"property": "monty:corr_id"}, corr_id]
        },
        filter_lang="cql2-json"
    )
    return list(search.items())

# Usage
items = get_event_data(client, "20241027-ESP-FL-2-GCDB")
```

**After** (using dynamic queries):

```python
def get_event_data(client, country, hazard_type, event_date, tolerance_days=1):
    from datetime import datetime, timedelta
    
    # Parse event date
    dt = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
    start = dt - timedelta(days=tolerance_days)
    end = dt + timedelta(days=tolerance_days)
    
    search = client.search(
        filter={
            "op": "and",
            "args": [
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, country]},
                {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, hazard_type]},
                {
                    "op": "t_intersects",
                    "args": [
                        {"property": "datetime"},
                        {"interval": [start.isoformat(), end.isoformat()]}
                    ]
                }
            ]
        },
        filter_lang="cql2-json"
    )
    return list(search.items())

# Usage
items = get_event_data(client, "ESP", "MH0600", "2024-10-27T00:00:00Z")
```

**Hybrid Approach** (recommended during migration):

```python
def get_event_data(client, country, hazard_type, event_date, corr_id=None, tolerance_days=1):
    # Try correlation ID first if available
    if corr_id:
        search = client.search(
            filter={
                "op": "=",
                "args": [{"property": "monty:corr_id"}, corr_id]
            },
            filter_lang="cql2-json"
        )
        items = list(search.items())
        if items:
            return items
    
    # Fall back to dynamic queries
    return get_event_data_dynamic(client, country, hazard_type, event_date, tolerance_days)
```

---

### Example 2: Impact Analysis

**Before**:

```python
def get_impacts(client, corr_id):
    search = client.search(
        collections=["gdacs-impacts", "emdat-impacts"],
        filter={
            "op": "and",
            "args": [
                {"op": "=", "args": [{"property": "monty:corr_id"}, corr_id]},
                {"op": "in", "args": ["impact", {"property": "roles"}]}
            ]
        },
        filter_lang="cql2-json"
    )
    return list(search.items())
```

**After**:

```python
def get_impacts(client, country, hazard_codes, start_date, end_date, impact_types=None):
    filter_args = [
        {"op": "a_contains", "args": [{"property": "monty:country_codes"}, country]},
        {"op": "a_overlaps", "args": [{"property": "monty:hazard_codes"}, hazard_codes]},
        {
            "op": "t_during",
            "args": [
                {"property": "datetime"},
                {"interval": [start_date, end_date]}
            ]
        },
        {"op": "in", "args": ["impact", {"property": "roles"}]}
    ]
    
    search = client.search(
        collections=["gdacs-impacts", "emdat-impacts", "idmc-gidd-impacts"],
        filter={
            "op": "and",
            "args": filter_args
        },
        filter_lang="cql2-json"
    )
    return list(search.items())
```

---

### Example 3: Multi-Hazard Events

**This scenario was difficult with static IDs**:

```python
# New capability: Find all events where flooding occurred after an earthquake
def find_cascading_events(client, country, primary_event_date, time_window_hours=72):
    from datetime import datetime, timedelta
    
    # First find earthquakes
    eq_date = datetime.fromisoformat(primary_event_date.replace('Z', '+00:00'))
    
    earthquakes = client.search(
        filter={
            "op": "and",
            "args": [
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, country]},
                {"op": "a_contains", "args": [{"property": "monty:hazard_codes"}, "GH0101"]},
                {
                    "op": "t_intersects",
                    "args": [
                        {"property": "datetime"},
                        {"interval": [
                            (eq_date - timedelta(hours=1)).isoformat(),
                            (eq_date + timedelta(hours=1)).isoformat()
                        ]}
                    ]
                },
                {"op": "in", "args": ["event", {"property": "roles"}]}
            ]
        },
        filter_lang="cql2-json"
    )
    
    # Then find subsequent flooding
    floods = client.search(
        filter={
            "op": "and",
            "args": [
                {"op": "a_contains", "args": [{"property": "monty:country_codes"}, country]},
                {"op": "a_overlaps", "args": [{"property": "monty:hazard_codes"}, ["MH0600", "MH0603"]]},
                {
                    "op": "t_during",
                    "args": [
                        {"property": "datetime"},
                        {"interval": [
                            eq_date.isoformat(),
                            (eq_date + timedelta(hours=time_window_hours)).isoformat()
                        ]}
                    ]
                },
                {"op": "in", "args": ["event", {"property": "roles"}]}
            ]
        },
        filter_lang="cql2-json"
    )
    
    return {
        "earthquakes": list(earthquakes.items()),
        "subsequent_floods": list(floods.items())
    }
```

---

## Performance Considerations

### Query Optimization Tips

1. **Use Indexed Fields First**:
   ```python
   # Good - country and datetime are indexed
   {
       "op": "and",
       "args": [
           {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "ESP"]},
           {"op": "t_after", "args": [{"property": "datetime"}, "2024-01-01"]}
       ]
   }
   ```

2. **Limit Result Sets**:
   ```python
   search = client.search(
       filter=filter_dict,
       filter_lang="cql2-json",
       limit=100  # Always set a reasonable limit
   )
   ```

3. **Use Collections Parameter**:
   ```python
   # Good - limits search to specific collections
   search = client.search(
       collections=["gdacs-events", "glide-events"],
       filter=filter_dict
   )
   
   # Less efficient - searches all collections
   search = client.search(filter=filter_dict)
   ```

4. **Cache Common Queries**:
   ```python
   from functools import lru_cache
   from datetime import timedelta
   
   @lru_cache(maxsize=100)
   def get_events_cached(country, hazard, date_str):
       return get_events(client, country, hazard, date_str)
   ```

### Performance Comparison

| Operation | Static ID | Dynamic Query | Notes |
|-----------|-----------|---------------|-------|
| Single event lookup | ~50ms | ~100ms | Dynamic query adds overhead |
| Related items (10-50) | ~100ms | ~150ms | Minimal difference |
| Complex multi-hazard | N/A | ~500ms | New capability |
| Regional analysis (100s) | ~500ms | ~800ms | Dynamic query more flexible |

---

## Testing Your Migration

### Validation Checklist

- [ ] Test basic event lookup with both methods
- [ ] Verify results match between static and dynamic approaches
- [ ] Measure query performance for your use cases
- [ ] Test edge cases (multi-country, multi-hazard events)
- [ ] Validate data completeness
- [ ] Update documentation and code comments
- [ ] Train team members on new approach

### Sample Test Code

```python
def validate_migration(client, test_corr_id, expected_criteria):
    """
    Validate that dynamic queries return the same results as static ID.
    """
    # Get results using correlation ID
    static_results = client.search(
        filter={"op": "=", "args": [{"property": "monty:corr_id"}, test_corr_id]},
        filter_lang="cql2-json"
    )
    static_items = {item.id for item in static_results.items()}
    
    # Get results using dynamic query
    dynamic_filter = {
        "op": "and",
        "args": [
            {"op": "a_contains", "args": [{"property": "monty:country_codes"}, expected_criteria["country"]]},
            {"op": "a_overlaps", "args": [{"property": "monty:hazard_codes"}, expected_criteria["hazards"]]},
            {
                "op": "t_intersects",
                "args": [
                    {"property": "datetime"},
                    {"interval": expected_criteria["date_range"]}
                ]
            }
        ]
    }
    dynamic_results = client.search(
        filter=dynamic_filter,
        filter_lang="cql2-json"
    )
    dynamic_items = {item.id for item in dynamic_results.items()}
    
    # Compare
    print(f"Static ID returned: {len(static_items)} items")
    print(f"Dynamic query returned: {len(dynamic_items)} items")
    print(f"Match: {static_items == dynamic_items}")
    
    if static_items != dynamic_items:
        print(f"Only in static: {static_items - dynamic_items}")
        print(f"Only in dynamic: {dynamic_items - static_items}")
    
    return static_items == dynamic_items

# Test
validate_migration(
    client,
    "20241027-ESP-FL-2-GCDB",
    {
        "country": "ESP",
        "hazards": ["MH0600", "FL", "nat-hyd-flo-flo"],
        "date_range": ["2024-10-27T00:00:00Z", "2024-10-28T23:59:59Z"]
    }
)
```

---

## Getting Help

### Resources

- [Correlation Algorithms Documentation](./correlation_algorithms.md)
- [Practical Examples](./correlation_examples.md)
- [STAC Filter Extension](https://github.com/stac-api-extensions/filter)
- [CQL2 Specification](https://docs.ogc.org/DRAFTS/21-065.html)

### Support Channels

- GitHub Issues: [monty-stac-extension](https://github.com/IFRCGo/monty-stac-extension/issues)
- IFRC GO Platform: [go.ifrc.org](https://go.ifrc.org)
- Development Seed: [developmentseed.org](https://developmentseed.org)

### Common Issues

**Issue**: Queries timing out  
**Solution**: Add more specific filters, reduce time windows, or use collection parameter

**Issue**: Missing results  
**Solution**: Check hazard code compatibility across classification systems

**Issue**: Too many results  
**Solution**: Tighten temporal or spatial criteria

**Issue**: Array operators not working  
**Solution**: Verify you're using `a_contains`, `a_overlaps` etc., not regular equality operators

---

## Next Steps

1. **Experiment**: Try the examples in [correlation_examples.md](./correlation_examples.md)
2. **Test**: Run validation tests on your data
3. **Measure**: Compare performance for your use cases
4. **Migrate**: Gradually move to hybrid approach
5. **Optimize**: Tune queries based on your needs
6. **Feedback**: Report issues and suggestions

The migration is designed to be gradual and non-breaking. Take your time to experiment and find what works best for your use case.
