# Monty STAC Extension Examples

This directory contains example STAC collections and items that demonstrate the implementation of the Monty STAC extension. These examples serve as reference implementations for various disaster data sources and showcase the proper structure and usage of the extension.

## Directory Structure

The examples are organized by data source and collection type:

### Event Collections

Collections that define disaster events from various sources:

- **[desinventar-events/](desinventar-events/)** - DesInventar disaster events
- **[emdat-events/](emdat-events/)** - EM-DAT disaster events  
- **[gdacs-events/](gdacs-events/)** - GDACS disaster events
- **[gfd-events/](gfd-events/)** - Global Flood Database events
- **[glide-events/](glide-events/)** - GLIDE disaster events
- **[ibtracs-events/](ibtracs-events/)** - IBTrACS tropical cyclone events
- **[idmc-gidd-events/](idmc-gidd-events/)** - IDMC GIDD displacement events
- **[idmc-idu-events/](idmc-idu-events/)** - IDMC IDU displacement events
- **[ifrcevent-events/](ifrcevent-events/)** - IFRC event data
- **[pdc-events/](pdc-events/)** - Pacific Disaster Center events
- **[reference-events/](reference-events/)** - Reference canonical events
- **[usgs-events/](usgs-events/)** - USGS earthquake events

### Hazard Collections

Collections that contain hazard-specific data and characteristics:

- **[emdat-hazards/](emdat-hazards/)** - EM-DAT hazard data
- **[gdacs-hazards/](gdacs-hazards/)** - GDACS hazard information
- **[gfd-hazards/](gfd-hazards/)** - Global Flood Database hazard data
- **[glide-hazards/](glide-hazards/)** - GLIDE hazard classifications
- **[ibtracs-hazards/](ibtracs-hazards/)** - IBTrACS tropical cyclone hazard data
- **[ifrcevent-hazards/](ifrcevent-hazards/)** - IFRC hazard data
- **[pdc-hazards/](pdc-hazards/)** - Pacific Disaster Center hazard data
- **[usgs-hazards/](usgs-hazards/)** - USGS earthquake hazard data

### Impact Collections

Collections that document the effects and impacts of disasters:

- **[desinventar-impacts/](desinventar-impacts/)** - DesInventar impact data
- **[emdat-impacts/](emdat-impacts/)** - EM-DAT impact statistics
- **[gdacs-impacts/](gdacs-impacts/)** - GDACS impact assessments
- **[gfd-impacts/](gfd-impacts/)** - Global Flood Database impact data
- **[idmc-gidd-impacts/](idmc-gidd-impacts/)** - IDMC GIDD displacement impacts
- **[idmc-idu-impacts/](idmc-idu-impacts/)** - IDMC IDU displacement impacts
- **[ifrcevent-impacts/](ifrcevent-impacts/)** - IFRC impact data
- **[pdc-impacts/](pdc-impacts/)** - Pacific Disaster Center impact data
- **[usgs-impacts/](usgs-impacts/)** - USGS earthquake impact data

## Usage

These examples demonstrate:

1. **Proper STAC Collection Structure** - How to structure collections according to the STAC specification
2. **Monty Extension Implementation** - Correct usage of Monty extension fields and properties
3. **Data Source Integration** - How different disaster data sources can be represented in STAC
4. **Relationship Modeling** - How events, hazards, and impacts relate to each other
5. **Taxonomy Usage** - Implementation of standardized disaster taxonomies

## Collection Types

### Events

Event collections represent discrete disaster occurrences with temporal and spatial bounds. They typically include:

- Event identification and classification
- Temporal information (start/end dates)
- Spatial information (affected areas)
- Links to related hazards and impacts

### Hazards

Hazard collections contain data about the physical phenomena that can cause disasters:

- Hazard type and classification
- Intensity and severity measures
- Temporal evolution
- Spatial extent and characteristics

### Impacts

Impact collections document the consequences of disasters:

- Human impacts (casualties, displacement)
- Economic impacts (damages, losses)
- Social and environmental impacts
- Recovery and response metrics

## Validation

All examples in this directory are validated against:

- [STAC Specification](https://stacspec.org/)
- [Monty STAC Extension Schema](../json-schema/schema.json)
- Taxonomy requirements defined in the [model documentation](../docs/model/)

## Contributing

When adding new examples:

1. Follow the existing directory structure
2. Ensure compliance with the Monty extension schema
3. Include both collection and item examples where applicable
4. Update this index file to reference new examples
5. Validate examples using the provided schema

For more information about the Monty extension and its usage, see the [documentation](../docs/).
