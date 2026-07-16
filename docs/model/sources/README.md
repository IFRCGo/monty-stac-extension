# Data Sources

This documentation identifies the sources of data used for Monty. This has been initiated from the [GCDB excel source sheet](https://github.com/IFRCGo/GCDB/blob/main/Taxonomies/Monty_DataSources.xlsx).

Sources are declared in [`sources.yml`](./sources.yml), the single source of
truth this section and [`docs/sources.json`](../../sources.json) are generated
from — see [`scripts/gen_sources_index.py`](https://github.com/IFRCGo/monty-stac-extension/blob/main/scripts/gen_sources_index.py).
Run it after editing `sources.yml`; CI runs it with `--check` and fails on drift.

<!-- gen_sources_index.py: BEGIN available-sources -->
## Available Sources

| Source | Organisation | Status |
|---|---|---|
| AlertHub | — | undocumented |
| [Copernicus Emergency Management Service — Rapid Mapping](./CEMS/README.md) | Copernicus Emergency Management Service (CEMS) | etl |
| [International Charter on Space and Major Disasters](./Charter/README.md) | International Charter on Space and Major Disasters | etl |
| [DesInventar](./DesInventar/README.md) | United Nations Office for Disaster Risk Reduction (UNDRR) | production |
| [EM-DAT](./EM-DAT/README.md) | Centre for Research on the Epidemiology of Disasters (CRED) | production |
| [GDACS](./GDACS/README.md) | European Commission - Joint Research Centre (JRC) | production |
| [Global Flood Database (GFD)](./GFD/README.md) | Cloud to Street | production |
| [GLIDE](./GLIDE/README.md) | Asian Disaster Reduction Center (ADRC) | production |
| [IBTrACS](./IBTrACS/README.md) | National Oceanic and Atmospheric Administration (NOAA) | production |
| [IDMC — Global Internal Displacement Database (GIDD)](./IDMC/README.md) | Internal Displacement Monitoring Centre (IDMC) | production |
| [IDMC — Internal Displacement Updates (IDU)](./IDU/README.md) | Internal Displacement Monitoring Centre (IDMC) | production |
| [IFRC DREF](./IFRC-DREF/README.md) | International Federation of Red Cross and Red Crescent Societies (IFRC) | production |
| [Pacific Disaster Center (PDC)](./PDC/README.md) | Pacific Disaster Center | production |
| Reference Events | — | undocumented |
| [USGS Earthquake Catalog](./USGS/README.md) | United States Geological Survey (USGS) | production |
<!-- gen_sources_index.py: END available-sources -->

<!-- gen_sources_index.py: BEGIN data-types-by-source -->
## Data Types by Source

| Source | Events | Hazards | Impacts | Response |
|---|---|---|---|---|
| AlertHub | ✓ | ✓ | - | - |
| [Copernicus Emergency Management Service — Rapid Mapping](./CEMS/README.md) | ✓ | ✓ | ✓ | ✓ |
| [International Charter on Space and Major Disasters](./Charter/README.md) | ✓ | ✓ | - | ✓ |
| [DesInventar](./DesInventar/README.md) | ✓ | - | ✓ | - |
| [EM-DAT](./EM-DAT/README.md) | ✓ | ✓ | ✓ | - |
| [GDACS](./GDACS/README.md) | ✓ | ✓ | ✓ | - |
| [Global Flood Database (GFD)](./GFD/README.md) | ✓ | ✓ | ✓ | - |
| [GLIDE](./GLIDE/README.md) | ✓ | ✓ | - | - |
| [IBTrACS](./IBTrACS/README.md) | ✓ | ✓ | - | - |
| [IDMC — Global Internal Displacement Database (GIDD)](./IDMC/README.md) | ✓ | - | ✓ | - |
| [IDMC — Internal Displacement Updates (IDU)](./IDU/README.md) | ✓ | - | ✓ | - |
| [IFRC DREF](./IFRC-DREF/README.md) | ✓ | ✓ | ✓ | - |
| [Pacific Disaster Center (PDC)](./PDC/README.md) | ✓ | ✓ | ✓ | - |
| Reference Events | ✓ | - | - | - |
| [USGS Earthquake Catalog](./USGS/README.md) | ✓ | ✓ | ✓ | - |
<!-- gen_sources_index.py: END data-types-by-source -->

## Source Characteristics

Each source has specific characteristics that determine how their data is used in Monty:

- **Update Frequency**: Ranges from near real-time (GDACS, USGS) to annual updates (EM-DAT)
- **Geographic Coverage**: Global vs. regional focus
- **Data Types**: Events, hazards, and impacts coverage
- **Access Methods**: API, file downloads, or direct database access
- **Data Format**: Various formats including JSON, CSV, XML, and GeoJSON

For detailed information about each source, including specific data structures and integration methods, visit the respective source documentation pages linked above.

## Role Conventions

Use the following role conventions consistently in source mappings:

- Item `properties.roles` should include the data type role plus `source` for source-derived items:
    - event item: include `event` and `source`
    - hazard item: include `hazard` and `source`
    - impact item: include `impact` and `source`
- For cross-item relationships using link `rel="related"`, link `roles` should contain exactly one target type value: `event`, `hazard`, or `impact`.

Role order in arrays is not semantically significant.

## Source Analysis Process

Each source in the Monty system follows a standard documentation template to ensure consistent analysis and integration. Below is the structure that should be followed when documenting a new source:

### 1. Source Description

- Brief overview of the source
- Type of organization (e.g., International Organization, Government Agency)
- Primary focus and expertise
- Data coverage (temporal and geographical)

### 2. Collection Metadata

- Name of the collection
- Collection code/identifier
- Source organization details
    - Organization name
    - Contact information
    - Website/URL
- License information
- Source category (event, hazard, impact)
- API or documentation links

### 3. Data Sourcing

- API endpoints (if available)
    - Base URL
    - Authentication requirements
    - Rate limits
- Data download options
    - File formats
    - Update frequency
    - Access restrictions
- Data retrieval process
    - Methods (API calls, file downloads, etc.)
    - Required preprocessing steps

### 4. Data Structure

- Data model description
- Key fields and their definitions
- Data format specifications
- Quality control measures
- Known limitations or caveats

### 5. Item Mapping

Detailed mapping of source fields to STAC items for:

#### Event Items
- Required fields mapping
- Optional fields mapping
- Special handling requirements
- Examples

#### Hazard Items (if applicable)
- Hazard classification mapping
- Required fields mapping
- Optional fields mapping
- Examples

#### Impact Items (if applicable)
- Impact classification mapping
- Required fields mapping
- Optional fields mapping
- Examples

See [IDMC documentation](./IDMC/README.md) for a comprehensive example of this documentation structure.
