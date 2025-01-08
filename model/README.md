<!-- remark-ignore -->

# Monty Model

The [Monty model](./Montandon_Schema_V1-00.json) is maintained in the [GDBC repository](https://github.com/IFRCGo/GCDB)
and is used to generate the Monty model documentation. 
This JSON schema is the authoritative source for the Monty model and is used to build the STAC model.

## eoAPI risk

The STAC extension aims to provide a way to include Montandon data in STAC items and collections.
eoAPI risk is a flavor of [eoAPI](https://eoapi.dev/) dedicated to risk data.
The Monty model is transformed into a STAC model that is assimilable by the eoAPI data store.

## Model Normalization

The first step in the process is to normalize the Monty model.
This is done by converting the Monty model into a format that is easier to work with and compliant with the STAC specifications model.
The normalized model must keep all the information from the Monty model and cover the applications intented that will use the eoAPI risk data.

### Data Overview

The Monty model is based on **Event** data type that consititutes the core of the model.
In STAC, they will be represented as an item. Then for each event,
3 kinds of data are collected:

- **Hazard**: The type of hazard, its location and the intensity
- **Impact**: All type of impact affecting the population, the infrastructure, the environment, etc
  in terms of number of people affected, financial loss, dmaage to infrastructure, etc.
- **Response**: Anticipatory measures and actions taken in response to the event

![GCDB](gcdb.png)

The original Monty model is a relational model with a lot of redundant taxonomy attributes in various forms (e.g. country code + name). 
In the STAC model, we try to use unambiguous and normalized attributes as much as possible
but keeping the capacity to query the data with the original taxonomy.
For example, the country code is used as a normalized attribute in a specific field but the country name is kept as a keyword for free text search.

The following classs diagram shows the relationships between the different classes in the Monty model and their high-level attributes.

<style>
  .invisible {
    display: none;
  }
</style>

``` mermaid
---
title: Montandon STAC Model
---
classDiagram
    direction TD
    linkStyle default interpolate basis

    class Item["STAC Item"] {
        +id: string
        +title: string
        +geometry: GeoJson geometry
        +datetime: datetime
        +start_datetime: datetime
        +end_datetime: datetime
        +keywords: string[]
    }

    class Event {
        +country_codes: string[]
        +hazard_codes: string[]
    }

    Item <|-- Event

    class Data {
        +ref_event_id: string
        +source_event_id: string
        +source: string
    }

    Item <|-- Data

    class ReferenceEvent["Reference Event"] {
    }

    class SourceEvent["Source Event"] {
        +correlation_id: string
    }

    Data "0..*" --> "1" ReferenceEvent : is related to
    Data "0..*" --> "0" SourceEvent : is associated with

    Event <|-- ReferenceEvent
    Event <|-- SourceEvent
    SourceEvent "1..*" --> "1" ReferenceEvent : is paired with

    class Hazard {
        +hazard_detail: HazardDetail[]
    }

    Hazard --|> Data

    class Impact {
        +impact_detail: ImpactDetail[]
    }

    Impact --|> Data
    Impact "0..*" --> "1" Hazard : is the effect of

    class Response {
    }

    Response --|> Data
    
    class HazardDetail {
        +codes: string[]
        +max_value: number
        +max_unit: string
        +estimate_type: string
    }

    HazardDetail --* Hazard
    
    class HazardProfile["UNDRR-ISC 2020\nHazard Information Profiles"] {
        +code: string
        +name: string
        +type: string
        +cluster: string
    }

    Event "*" --> "*" HazardProfile : has
    HazardDetail "*" --> "*" HazardProfile : is defined by

    link HazardProfile "https://www.preventionweb.net/drr-glossary/hips"

    class ac["&ZeroWidthSpace;"] ::: invisible
    Hazard "0..*" -- ac : is concurrent with
    Hazard "0..*" <-- ac

    ac .. Occurence
    class Occurence {
        +type: string
        +prob: string
        +probdef: string
    }

    class ImpactDetail {
        +category: string
        +value: number
        +type: string
        +unit: string
        +date: datetime
        +estimate_type: string
    }

    ImpactDetail --* Impact

    
```

### Event

The event class is the core of the Monty model. It represents a disaster event that has occured or is forecasted to occur.
The global crisis data bank records multiple instances of events that are related to a single event:

- One unique reference event that is used to "pair" all the instances of the event
- Multiple instances of the event that are recorded for different sources

The event class has the following attributes:

- **id**: A unique identifier for the event. Preferably, the identifier assigned by the issuer (source) of the event.
  - The reference event uses a [?](./questions.md) generated by the Monty system
  - The source events use the identifier assigned by the source (issuer) of the event
  
  Generated by the Monty system (currently [this method](https://github.com/IFRCGo/Monty-IFRC/blob/main/API/helpers/DREF_forecasting.R#L13)). The event pairing page describes the algorithm used to generate the event id and the convention to follow.
  This identifier is used as the correlation id for all the sources events registered in the Monty system.
- **title**: The name of the event assigned by the issuer (source) of the event.
- **geometry** (GeoJSON geometry): The location of the event in the form of a GeoJSON geometry.
  It is recommanded to use a point geometry for the event so that it can be easily searched, displayed and clustered on a map.
  More geometries can be used for the hazard, impact and response data to represent the affected area.
- **datetime**: The date and time when the event occurred.
  For forecasted events, it is the date and time when the event is forecasted to occur.
- **start_datetime**: The date and time when the event started.
  For forecasted events, it is the date and time when the event is forecasted to start. **OPTIONAL**
- **end_datetime**: The date and time when the event ended.
  For forecasted events, it is the date and time when the event is forecasted to end. **OPTIONAL**
- **country_codes**: The country codes of the countries affected by the event.
  The country codes are based on the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard.
- **hazard_codes**: The hazard codes of the hazards affecting the event.
  The hazard codes are based on the [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips). [See hazard codes in the taxonomy](https://github.com/IFRCGo/monty-stac-extension/blob/main/model/taxonomy.md#hazard)
- **correlation_id**: The unique identifier assigned by the Monty system to the reference event.
  It is used to "pair" all the instances of the event.
- **keywords**: A list of keywords that describe the event. This list includes the human-readable names of
  - the countries affected by the event
  - the hazard types affecting the event

### Hazard

The hazard class represents a process, phenomenon or human activity that may cause loss of life, injury or other health impacts, property damage, social and economic disruption or environmental degradation. UNDRR - https://www.undrr.org/terminology/hazard.
In the Monty model, a hazard is always linked to an event and as per event, every hazard is recorded from multiple sources.

The hazard class has the following attributes:

- **id**: A unique identifier for the hazard. Preferably, the identifier assigned by the issuer (source) of the hazard. If not available, an identifier can be generated and should be prefixed with the related event id.
- **title**: The name of the hazard assigned by the issuer (source) of the hazard.
- **geometry** (GeoJSON geometry): The location of the hazard in the form of a GeoJSON geometry.
- **datetime**: The date and time when the hazard occurrs or is forecasted to occur.
- **start_datetime**: The date and time when the hazard started or is forecasted to start. **OPTIONAL**
- **end_datetime**: The date and time when the hazard ended or is forecasted to end. **OPTIONAL**
- **ref_event_id**: The identifier of the reference event to which is associated the hazard.
- **source_event_id**: The identifier of the source event to which is associated the hazard. **OPTIONAL**
- **source**: Information about the organization and the database capturing, producing, processing, hosting or publishing this data.
- **hazard_detail**: A detailed description of the hazard including:
  - **codes**: The hazard codes defining the hazard.
  - **max_value**: The estimated maximum hazard intensity/magnitude/severity value, as a number, without the units.
  - **max_unit**: The unit of the estimated maximum hazard intensity/magnitude/severity value.
  - **estimate_type**: The type of data source that was used to create this hazard intensity/magnitude/severity estimate:
    - Primary data
    - Secondary data
    - Modelled data: estimated without any event-specific data

Hazards may be linked between each others. This linkage is called "concurrent hazard" and is linking the observed and potentially unobserved hazards together with a specific relationship:

- **Triggers**: as the current hazard triggers the linked hazard. For example, an earthquake triggers a landslide.
- **Triggered by**: as the current hazard is triggered by the linked hazard. For example, a landslide is triggered by an earthquake.
- **Concurrent**: For hazards that do not necessarily trigger one-another, but occur together. For example, thunderstorms can occur together with windstorms or cyclones, thus, we would use 'concurrent'.
- **Complex**: When the relationship between two hazards is complex.

The link has also specific occurence attributes:

- **occurence_type**: the linked hazard actually observed to have occurred with the main hazard, or is this link only a potential link. Montandon allows for hazards to be linked together by actual observed occurrences, or the possibility that the linked hazard occurred with the principal hazard. This is especially useful when handling hazards such as tropical cyclones, whereby more than half of all deaths from cyclones in the US were actually caused by inland flooding.
- **occurence_prob** of the linked hazard occurring with the main hazard. This is a subjective probability, and is not a statistical probability. It is a qualitative assessment of the likelihood of the linked hazard occurring with the main hazard.
- **occurenece_probdef**: definition of occurrence probability is for the hazard relationship. For example, if the probability is 'high', where is 'high' defined?

### Impact

Impact data represent an estimate of the effect, including negative effects (e.g., economic losses) and positive effects (e.g., economic gains), of a hazardous event or a disaster. The term includes economic, human and environmental impacts, and may include death, injuries, disease and other negative effects on human physical, mental and social well-being'. UNDRR - https://www.undrr.org/terminology/disaster

The impact class has the following attributes:

- **id**: A unique identifier for the impact. Preferably, the identifier assigned by the issuer (source) of the impact estimate data. If not available, an identifier can be generated and should be prefixed with the related event id.
- **title**: The name of the impact assigned by the issuer (source) of the impact estimate data.
- **geometry** (GeoJSON geometry): The location of the impact in the form of a GeoJSON geometry.
- **datetime**: The date and time periods of the impact estimates.
- **start_datetime**: The date and time when the impact estimate started or is forecasted to start. **OPTIONAL**
- **end_datetime**: The date and time when the impact estimate ended or is forecasted to end. **OPTIONAL**
- **ref_event_id**: The identifier of the reference event to which is associated the impact.
- **source_event_id**: The identifier of the source event to which is associated the impact. **OPTIONAL**
- **hazard_id**: The identifier of the hazard to which is associated the impact. **OPTIONAL**
- **source**: Information about the organization and the database capturing, producing, processing, hosting or publishing this estimate impact data.
- **impact_detail**: A detailed description of the impact including:
  - **category**: The category of impact, which is the specific asset or population demographic that has been impacted by the hazard.
  - **value**: The estimated value of the impact, as a number, without the units. For example, for an estimate of 1000 people displaced, you would enter 1000.
  - **type**: The estimated value type of the impact. For example, for an estimate of 1000 people displaced, the value type is people displaced, thus you would enter 'imptypedisp'. [Refer to the taxonomy](https://github.com/IFRCGo/monty-stac-extension/blob/main/model/taxonomy.md#impact-type) for all possible impact types.
  - **unit**: The units of the impact estimate. For example, 10 deaths would be a count value, thus 'unitscountnum' should be used.
  - **date**: If the impact estimate is a cost, provide the date that the estimate was made on, to adjust for currency value and inflation. If no value is provided, imp_sdate will be used.  **OPTIONAL**
  - **estimate_type**: The type of data source that was used to create this impact estimate:
    - Primary data
    - Secondary data
    - Modelled data: estimated without any event-specific data

