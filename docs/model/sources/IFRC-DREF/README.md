# IFRC DREF

The IFRC Disaster Relief Emergency Fund (DREF) provides immediate financial support to National Red Cross and Red Crescent Societies for early action and response to disasters and crises.

## Collection Metadata

- **Name**: IFRC DREF Events
- **Code**: `ifrcevent`
- **Source Organization**:
    - Name: International Federation of Red Cross and Red Crescent Societies (IFRC)
    - Website: <https://www.ifrc.org>
    - Contact: <https://www.ifrc.org/contact-us>
- **Source Type**: International Organization
- **Source Category**: Event, Impact
- **API Documentation**: <https://goadmin-stage.ifrc.org/api/v2/>

## Data Sourcing

### API Endpoints

- **Base URL**: `https://goadmin-stage.ifrc.org/api/v2/`
- **Events Endpoint**: `/event/`
- **Parameters**:
    - `dtype`: Disaster type filter
    - `appeal_type`: Appeal type filter (0, 1 for DREF)
    - `id`: Specific event ID

### Data Retrieval Process

1. Events are filtered based on:
   - Appeal type (DREF operations)
   - Valid disaster type
   - Presence of field reports

2. For each event:
   - Basic event information is extracted
   - Impact data is collected from field reports
   - Country information is used for geometry generation

## Data Structure

### Event Data Model

```python
{
    "id": int,
    "name": str,
    "summary": str,
    "dtype": {
        "name": str  # Disaster type
    },
    "countries": [
        {
            "name": str,
            "iso3": str
        }
    ],
    "disaster_start_date": datetime,
    "appeals": [
        {
            "atype": int  # Appeal type (0, 1 for DREF)
        }
    ],
    "field_reports": [
        {
            "num_dead": int,
            "gov_num_dead": int,
            "other_num_dead": int,
            "num_injured": int,
            "gov_num_injured": int,
            "other_num_injured": int,
            # ... similar pattern for other impact metrics
        }
    ]
}
```

### Accepted Disaster Types

- Earthquake
- Cyclone
- Volcanic Eruption
- Tsunami
- Flood
- Cold Wave
- Fire
- Heat Wave
- Drought
- Storm Surge
- Landslide
- Flash Flood
- Epidemic

## Item Mapping

### Event Items

| STAC Field                                                                                                               | IFRC Field             | Required | Notes                                |
| ------------------------------------------------------------------------------------------------------------------------ | ---------------------- | -------- | ------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                    | `ifrcevent-event-{id}` | Yes      | Prefixed ID                          |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                        | Generated              | Yes      | From country ISO3                    |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time)             | disaster_start_date    | Yes      | Start date of the disaster           |
| [title](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)                  | name                   | Yes      | Event name                           |
| [description](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#item-fields)            | summary                | No       | Event summary                        |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range) | disaster_start_date    | Yes      |                                      |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/item-spec/common-metadata.md#date-and-time-range)   | disaster_start_date    | Yes      | Same as start (no end date provided) |

#### Monty Extension Fields

| Field                                                       | Source           | Notes                           |
| ----------------------------------------------------------- | ---------------- | ------------------------------- |
| [episode_number](https://github.com/IFRCGo/monty-stac-extension#montyepisode_number) | Fixed value (1)  | DREF doesn't track episodes     |
| [hazard_codes](https://github.com/IFRCGo/monty-stac-extension#montyhazard_codes)     | dtype.name       | Mapped to standard hazard codes |
| [country_codes](https://github.com/IFRCGo/monty-stac-extension#montycountry_codes)   | countries[].iso3 | Array of ISO3 codes             |

### Impact Items

Impact items are generated from field reports data, with multiple impact types:

| [Impact Type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) | Source Fields | [Category](https://github.com/IFRCGo/monty-stac-extension#exposure-category) |
| -------------------- | -------------------------------------------------------------------------------------- | ---------- |
| [Death](../../../model/taxonomy.md#impact-type) | num_dead, gov_num_dead, other_num_dead | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Displaced](../../../model/taxonomy.md#impact-type) | num_displaced, gov_num_displaced, other_num_displaced | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Injured](../../../model/taxonomy.md#impact-type) | num_injured, gov_num_injured, other_num_injured | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Missing](../../../model/taxonomy.md#impact-type) | num_missing, gov_num_missing, other_num_missing | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Affected](../../../model/taxonomy.md#impact-type) | num_affected, gov_num_affected, other_num_affected | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Assisted](../../../model/taxonomy.md#impact-type) | num_assisted, gov_num_assisted, other_num_assisted | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Potentially Affected](../../../model/taxonomy.md#impact-type) | num_potentially_affected, gov_num_potentially_affected, other_num_potentially_affected | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |
| [Highest Risk](../../../model/taxonomy.md#impact-type) | num_highest_risk, gov_num_highest_risk, other_num_highest_risk | [ALL_PEOPLE](../../../model/taxonomy.md#exposure-category) |

Each impact type gets its own item with:
- ID format: `ifrcevent-impact-{event_id}-{impact_type}`
- Same geometry as parent event
- Impact details including:
    - [category](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) ([ALL_PEOPLE](../../../model/taxonomy.md#exposure-category))
    - [type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (specific [impact type](../../../model/taxonomy.md#impact-type))
    - [value](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (first non-null value from the three source fields)
    - [estimate_type](https://github.com/IFRCGo/monty-stac-extension#montyimpact_detail) (PRIMARY)

### Hazard Code Mapping

Example mappings from IFRC disaster types to standard codes:

```python
{
    "Earthquake": ["GH0001", "GH0002", "GH0003", "GH0004", "GH0005"],
    "Cyclone": ["MH0030", "MH0031", "MH0032"],
    "Flood": ["FL"],
    "Tsunami": ["MH0029", "GH0006"],
    # ... other mappings
}
```

## Quality Control Notes

1. Events are filtered to include only DREF operations
2. Only events with valid disaster types are processed
3. Impact values are cross-referenced between sources (government, other)
4. Geometry is generated from country codes for consistent spatial representation
