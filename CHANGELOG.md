# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

- Updated taxonomy for 2025 UNDRR-ISC Hazard Information Profiles [#32](https://github.com/IFRCGo/monty-stac-extension/pull/32)

### Fixed

- Mandatory severity_value and severity_unit fields in hazard_detail reflected in json schema [#32](https://github.com/IFRCGo/monty-stac-extension/pull/32)

### Removed

- Removed cluster code from hazard detail as we have chapeau hazard codes now [#32](https://github.com/IFRCGo/monty-stac-extension/pull/32)

## [1.0.0] - 2025-05-27

Initial release of the Monty STAC Extension specification.

### Added

- Core STAC extension specification for Monty (Global Crisis Data Bank)
  - Field definitions for Items and Collections
  - Relation type specifications
  - Link attribute definitions

- Comprehensive data model documentation
  - Event object specification
  - Hazard object specification
  - Impact object specification
  - Source analysis templates and guidelines

- Integration with major disaster data sources:
  - DesInventar - National disaster loss database
  - EM-DAT - International disaster database
  - GDACS - Global Disaster Alert and Coordination System
  - GFD - Global Flood Database
  - GLIDE - Global unique disaster identifier
  - IBTrACS - International Best Track Archive for Climate Stewardship
  - IDMC - Internal Displacement Monitoring Centre
  - IFRC-DREF - Disaster Relief Emergency Fund
  - PDC - Pacific Disaster Center
  - USGS - United States Geological Survey

- Common taxonomy and classification systems
  - Standardized hazard codes
  - Impact types and categories
  - Country code normalization
  - Cross-classification mappings

- Reference implementations
  - Example collections for all supported sources
  - Event correlation examples
  - Impact aggregation examples

- Developer tools and documentation
  - JSON Schema for validation
  - Documentation website using MkDocs
  - Source integration guidelines
  - Querying capabilities documentation

### Supported Features

- Event correlation across multiple sources
- Hazard classification standardization
- Impact data aggregation
- Spatial and temporal querying
- STAC API integration support
- Collection-level metadata
- Source-specific field mappings

### Notes

- This is the initial release for evaluation and feedback
- The specification is currently in proposal status
- Some features may be subject to change based on community feedback
- Additional sources may be added in future releases

[1.0.0]: https://github.com/IFRCGo/monty-stac-extension/releases/tag/v1.0.0
