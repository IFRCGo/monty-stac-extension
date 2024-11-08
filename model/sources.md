# Sources

This page identifies the sources of data used for Monty. This has been initiated from the [GCDB excel source sheet](https://github.com/IFRCGo/GCDB/blob/main/Taxonomies/Monty_DataSources.xlsx).

Each section is a source reference to extract data from.

## GLIDE

Since the beginning of 2004, GLobal IDEntifier numbers (GLIDE) are produced by this website (GLIDEnumber.net) for all new disaster events reported by partner institutions and those discovered by ADRC.
The components of a GLIDE number consist of two letters to identify the disaster type (e.g. EQ - earthquake); the year of the disaster; a six-digit, sequential disaster number; and the three-letter ISO code for country of occurrence. So, for example, the GLIDE number for West-India Earthquake in India is: EQ-2001-000033-IND.

### Metadata

* Name: GLobal IDEntifier numbers (GLIDE)
* Code: GLIDE
* Source organisation: Asian Disaster Reduction Center (ADRC)
* Source code: ADRC
* Source Type: Regional Intergovernmental Organisation
* Source organization email: gliderep@adrc.asia
* Source URL: https://glidenumber.net
* Source Data license: unknown
* Source for: event, hazard, *impact*

* implementation (R): https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGLIDEnumber.R

### Data

Accessible data is a set of glide number entries. Each entry is a disaster event. The data is available in the form of a json file via the API endpoint `https://www.glidenumber.net/glide/jsonglideset.jsp?level1=CHN&fromyear=2008&events=EQ&number=2008-000062`.

#### Data conversion

* A glide entry will **ALWAYS** produce an event STAC item as in the example [EQ-2008-000062-CHN](../examples/glide-events/EQ-2008-000062-CHN.json)
* A glide entry will **ALWAYS** produce an hazard STAC item as in the example [EQ-2008-000062-CHN](../examples/glide-hazards/EQ-2008-000062-CHN.json)
* A glide entry *MAY* produce a Impact STAC item if any of the fields `homeless`, `killed`, `affected` or `injured` are set to a number different from zero.

Refer to the existing R code for a baseline implementation.

## GDACS

GDACS is a cooperation framework between the United Nations, the European Commission and disaster managers worldwide to improve alerts, information exchange and coordination in the first phase after major sudden-onset disasters.

### Metadata

* Name: Global Disaster Alert and Coordination System (GDACS)
* Code: GDACS
* Source organisation: European Commission - Joint Research Centre (JRC)
* Source code: EC-JRC
* Source Type: Regional Intergovernmental Organisation
* Source organization email: coordination@gdacs.org
* Source URL: https://www.gdacs.org
* Source Data license: MIT License
* Source for: event, hazard, impact

* implementation (R): https://github.com/IFRCGo/GCDB/blob/main/RCode/MainlyHazardData/GetGDACS.R

### Data

Accessible data is a set of GDACS entries. Each entry is a disaster event. The data is available in the form of a geojson collections via the API endpoint `https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?`.
Individual events can be accessed via the API endpoint `https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype=FL&eventid=1102983`.

* Documentation: https://www.gdacs.org/floodmerge/data_v2.aspx
* Python lib: https://github.com/Kamparia/gdacs-api

### Event

A GDACS event will **ALWAYS** produce an event STAC item as in the example [GDACS-2021-000001-IND](../examples/gdacs-events/GDACS-2021-000001-IND.json).

Here is a table with the fields that are mapped from the GDACS event to the STAC event:

| GDACS field          | STAC field         | Description                                                                             |
| -------------------- | ------------------ | --------------------------------------------------------------------------------------- |
| bbox                 | bbox               | Bounding box of the event                                                               |
| geometry             | geometry           | Geometry of the event                                                                   |
| properties.eventtype | monty:hazard_codes | List of hazard codes converted following the GDACS event type to Hazard profile mapping |
| properties.eventid   | id                 | Unique identifier for the event                                                         |


