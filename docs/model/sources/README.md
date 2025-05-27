# Data Sources

This documentation identifies the sources of data used for Monty. This has been initiated from the [GCDB excel source sheet](https://github.com/IFRCGo/GCDB/blob/main/Taxonomies/Monty_DataSources.xlsx).

## Available Sources

### Global Disaster Databases

- [DesInventar](./DesInventar/README.md) - National disaster loss database system collecting detailed disaster-related damage and loss data.
- [EM-DAT](./EM-DAT/README.md) - The Emergency Events Database, containing worldwide data on the occurrence and effects of disasters.
- [GDACS](./GDACS/README.md) - Global Disaster Alert and Coordination System, providing near real-time alerts about natural disasters.
- [GLIDE](./GLIDE/README.md) - GLobal IDEntifier number, assigning unique identifiers to disasters worldwide.

### Specialized Systems

- [GFD](./GFD/README.md) - Global Flood Database, providing information about flood events and their impacts.
- [IBTrACS](./IBTrACS/README.md) - International Best Track Archive for Climate Stewardship, tracking tropical cyclone data.
- [IDMC](./IDMC/README.md) - Internal Displacement Monitoring Centre, focusing on internal displacement data.
- [PDC](./PDC/README.md) - Pacific Disaster Center, offering disaster monitoring and early warning capabilities.
- [USGS](./USGS/README.md) - United States Geological Survey, providing earthquake and other geological hazard data.

### IFRC Sources

- [IFRC-DREF](./IFRC-DREF/README.md) - Disaster Relief Emergency Fund operations data from the International Federation of Red Cross and Red Crescent Societies.

## Data Types by Source

| Source | Events | Hazards | Impacts |
|--------|---------|----------|----------|
| DesInventar | ✓ | - | ✓ |
| EM-DAT | ✓ | ✓ | ✓ |
| GDACS | ✓ | ✓ | ✓ |
| GFD | ✓ | ✓ | ✓ |
| GLIDE | ✓ | ✓ | - |
| IBTrACS | ✓ | ✓ | - |
| IDMC | ✓ | - | ✓ |
| IFRC-DREF | ✓ | - | ✓ |
| PDC | ✓ | ✓ | ✓ |
| USGS | ✓ | ✓ | ✓ |

## Source Characteristics

Each source has specific characteristics that determine how their data is used in Monty:

- **Update Frequency**: Ranges from near real-time (GDACS, USGS) to annual updates (EM-DAT)
- **Geographic Coverage**: Global vs. regional focus
- **Data Types**: Events, hazards, and impacts coverage
- **Access Methods**: API, file downloads, or direct database access
- **Data Format**: Various formats including JSON, CSV, XML, and GeoJSON

For detailed information about each source, including specific data structures and integration methods, visit the respective source documentation pages linked above.

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
