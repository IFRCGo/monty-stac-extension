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

## [GDACS](GDACS)
