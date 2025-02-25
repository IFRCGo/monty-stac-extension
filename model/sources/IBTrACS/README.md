# NOAA IBTrACS

The International Best Track Archive for Climate Stewardship (IBTrACS) is a global database of tropical cyclone best track data. It provides a centralized repository of tropical cyclone position and intensity information from multiple agencies worldwide. IBTrACS combines data from numerous sources to create a comprehensive global dataset of tropical cyclone tracks and intensities, making it valuable for climate research, risk assessment, and historical analysis of tropical cyclone activity.

## Collection: `ibtracs-events`

A STAC collection holds all the IBTrACS events. An example of the IBTrACS collection is [here](../../../examples/ibtracs-events/ibtracs-events.json).

- Name: International Best Track Archive for Climate Stewardship (IBTrACS)
- Code: `IBTrACS`
- Source organisation: National Oceanic and Atmospheric Administration (NOAA)
- Source code: NOAA
- Source Type: National Government Organization
- Source organization email: <IBTrACS.Team@noaa.gov>
- Source URL: <https://www.ncei.noaa.gov/products/international-best-track-archive>
- Source Data license: [Public Domain](https://www.noaa.gov/information-technology/open-data-dissemination)
- Source for: event, hazard

### Data

IBTrACS provides tropical cyclone data in multiple formats:

1. **Comma Separated Value (CSV)** - Text files for general use (e.g., in Excel, databases)
2. **Network Common Data Format (netCDF)** - Binary files that can be read by numerous programming languages
3. **Shapefiles** - Files used by the geospatial community (e.g., ArcGIS)

The data can be accessed from:
- CSV files: <https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/>
- NetCDF files: <https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/netcdf/>
- Shapefiles: <https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/shapefile/>

Documentation:
- Technical Details: <https://www.ncei.noaa.gov/sites/g/files/anmtlf171/files/2024-07/IBTrACS_version4r01_Technical_Details.pdf>
- Best Track Report: <https://www.metoc.navy.mil/jtwc/products/best-tracks/tc-bt-report.html>

#### Data Subsets

In addition to global data files that contain all storms available in IBTrACS, several subsets are provided:

- **Basin subsets**: All storms that have at least one position in a specific basin:
  - NA - North Atlantic
  - SA - South Atlantic
  - EP - Eastern North Pacific (including Central Pacific)
  - WP - Western North Pacific
  - SP - South Pacific
  - SI - South Indian
  - NI - North Indian

- **Time subsets**:
  - Since 1980 - The modern satellite era
  - Last 3 years - Recent storms
  - Active - Storms active within the last 7 days

#### Data Coverage

- **Spatial coverage**: 70°N to 70°S and 180°W to 180°E
- **Temporal coverage**: 1841 to present (though not all storms are captured in earlier years)
- **Temporal resolution**: Interpolated to 3-hourly (most data reported at 6-hourly)
- **Spatial resolution**: 0.1° (~10 km)

### Event Item

An IBTrACS tropical cyclone will **ALWAYS** produce an [**event STAC item**](../../../README.md#event). Unlike the hazard items which create a new item for each position, the event item is a single item that is **continuously updated** with the latest storm information as new data becomes available.

#### Implementation Approach

For an ongoing tropical cyclone:
1. Create an event item when the storm is first identified
2. As new positions become available, update the event item to reflect:
   - Extended time range (update end_datetime)
   - Complete track geometry (include all positions)
   - Additional affected countries
   - Updated maximum intensity information
   - Any changes to the storm name or other metadata

This approach ensures that the event item always represents the complete, up-to-date information about the entire lifecycle of the tropical cyclone.

#### Event Item Mapping

Here is a table with the fields that are mapped from the IBTrACS data to the STAC event:

| STAC field                                                                                                             | IBTrACS field                | Description                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | SID                          | Unique storm identifier assigned by IBTrACS algorithm                                                  |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | Derived from track positions | Bounding box of the complete storm track (updated as new positions are added)                          |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | LAT, LON                     | LineString geometry of the complete storm track (updated as new positions are added)                   |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `ibtracs-events`             | The collection for IBTrACS events                                                                      |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | NAME                         | Name of the storm if available (updated if the storm is named after creation)                          |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                 | Derived                      | Description of the storm including basin, season, and maximum intensity (updated as intensity changes) |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | ISO_TIME (first position)    | Time of the first observation in UTC ISO 8601 format                                                   |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | ISO_TIME (first position)    | Start time of the storm in UTC ISO 8601 format                                                         |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | ISO_TIME (latest position)   | End time of the storm in UTC ISO 8601 format (updated as new positions are added)                      |
| [monty:country_codes](../../../README.md#montycountry_codes)                                                           | Derived from track positions | ISO3 codes of countries affected by the storm track (updated as new countries are affected)            |
| [monty:hazard_codes](../../../README.md#montyhazard_codes)                                                             | Fixed as tropical cyclone    | Always `['MH0057', 'nat-met-sto-tro', 'TC']` for codes                                                 |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#keywords)                  | NAME                         | Keywords should include the cyclone name                                                               |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                  | Constructed URL              | Link to the IBTrACS data source                                                                        |

## Collection: `ibtracs-hazards`

A STAC collection holds all the IBTrACS hazards. An example of the IBTrACS hazards collection is [here](../../../examples/ibtracs-hazards/ibtracs-hazards.json).

### Hazard Items

An IBTrACS tropical cyclone will produce **MULTIPLE** [**hazard STAC items**](../../../README.md#hazard), one for each position in the storm track. Each hazard item represents the cumulative track of the storm up to that point in time.

#### Implementation Approach

For each position in the IBTrACS data:
1. Create a new hazard item
2. Include all previous positions of the storm in the geometry (as a LineString)
3. Set the datetime to the current position's time
4. Update the hazard details with the current intensity information

This approach allows for tracking the evolution of the storm over time, with each hazard item representing the complete track history up to that specific moment. This is particularly valuable for monitoring ongoing storms and understanding their development.

#### Hazard Item Mapping

Here is a table with the STAC fields that are mapped from the IBTrACS data to each STAC hazard item:

| STAC field                                                                                                             | IBTrACS field                          | Description                                                                      |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| [id](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#id)                                  | SID + `-hazard-` + timestamp           | Unique identifier for the hazard including the timestamp of the current position |
| [bbox](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox)                              | Derived from track positions           | Bounding box of the storm track up to the current position                       |
| [geometry](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#geometry)                      | LAT, LON                               | LineString geometry of the storm track up to the current position                |
| [collection](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#collection)                  | `ibtracs-hazards`                      | The collection for IBTrACS hazards                                               |
| [title](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                       | NAME                                   | Name of the storm if available                                                   |
| [description](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#basics)                 | Derived                                | Description of the hazard including basin, season, and current intensity         |
| [datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time)             | ISO_TIME (current position)            | Time of the current observation in UTC ISO 8601 format                           |
| [start_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range) | ISO_TIME (first position)              | Start time of the storm in UTC ISO 8601 format                                   |
| [end_datetime](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#date-and-time-range)   | ISO_TIME (current position)            | End time (current time) of the hazard in UTC ISO 8601 format                     |
| [monty:country_codes](../../../README.md#montycountry_codes)                                                           | Derived from track positions           | ISO3 codes of countries affected by the storm track up to the current position   |
| [monty:hazard_codes](../../../README.md#montyhazard_codes)                                                             | Fixed as tropical cyclone              | Always `['MH0057', 'nat-met-sto-tro', 'TC']` for codes                           |
| [keywords](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#keywords)                  | NAME                                   | Keywords should include the cyclone name                                         |
| [`via` link](https://github.com/radiantearth/stac-spec/blob/master/commons/assets.md)                                  | Constructed URL                        | Link to the IBTrACS data source                                                  |
| [monty:hazard_detail](../../../README.md#montyhazard_detail)                                                           | USA_WIND, WMO_WIND, USA_PRES, WMO_PRES | Detailed description of the hazard at the current position                       |

#### Hazard Detail

The [monty:hazard_detail](../../../README.md#montyhazard_detail) field contains detailed information about the tropical cyclone at the current position:

| Field          | IBTrACS field        | Description                                                            |
| -------------- | -------------------- | ---------------------------------------------------------------------- |
| clusters       | Fixed value          | Always `nat-met-sto-tro` (EM-DAT classification for tropical cyclones) |
| severity_value | USA_WIND or WMO_WIND | Current maximum sustained wind speed in knots                          |
| severity_unit  | Fixed value          | Always `knots`                                                         |
| pressure       | USA_PRES or WMO_PRES | Current minimum central pressure in millibars                          |
| pressure_unit  | Fixed value          | Always `mb`                                                            |

#### Example Sequence

For a tropical cyclone with positions at times T1, T2, T3, ..., Tn:

1. At time T1: Create hazard item with geometry containing only position P1
2. At time T2: Create hazard item with geometry containing positions P1 and P2
3. At time T3: Create hazard item with geometry containing positions P1, P2, and P3
...and so on.

This creates a sequence of hazard items that show the progressive development of the storm track over time.

### Important Caveats

1. **Wind Speed Reporting Differences**: Wind speeds are reported differently by various international agencies. Some use 1-minute averaging periods (US agencies), while others use 10-minute periods (most other agencies). There is no simple global conversion between these wind speeds.

2. **Position Uncertainty**: Storm positions are generally reported at a resolution of 0.1 degrees (~10 km). The uncertainty varies with storm intensity and observation methods.

3. **Storm Count Uncertainty**: Users should exercise care when counting storms in IBTrACS due to various issues:
   - Tropical depressions may not be uniformly counted in space or time
   - Sub-tropical storms may be included in some years but not others
   - Some storms may have been missed, especially before satellite monitoring
   - Storm spurs (alternate positions) should be ignored when counting storms

4. **Historical Data Limitations**: Early storm tracks (prior to 1920) were often rescued by digitizing positions from atlases that sometimes lacked precise dates, resulting in potential duplication.

5. **Observation System Changes**: The methods for observing tropical cyclones have evolved significantly over time:
   - Surface reports (1800s-present)
   - Aircraft reconnaissance (late 1940s-present, but only in North Atlantic since 1987)
   - Satellite observations (1960s-present)
   - Microwave satellites (late 1980s-present)
