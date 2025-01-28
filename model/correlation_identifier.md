# Correlation Identifier

This page describes the algorithm used to generate the correlation identifier for the items for the Monty system.

## Context

*The elements of context below are based on the article [Connecting the dots: the importance of recognising multi-hazard events in disaster reporting](https://www.preventionweb.net/news/connecting-dots-importance-recognising-multi-hazard-events-disaster-reporting).

In the past year, the world has experienced numerous severe disasters caused by multiple overlapping hazards. In February 2023, two severe earthquakes struck Syria and Turkey in quick succession, followed by two more powerful earthquakes and over a hundred aftershocks in the subsequent weeks. This disaster resulted in over 48,000 fatalities, with many people still missing. Similarly, in June 2022, Afghanistan was hit by an earthquake while already grappling with a multi-year drought, which was then followed by extreme rainfall and flooding in August. Pakistan also faced a series of unfortunate events throughout 2022. After a period of drought, a heatwave-induced glacier melt combined with a heavy rain season led to devastating flooding, landslides, and disease outbreaks. Additionally, the country contended with severe wildfires in May and June 2022.

The [United Nations Office for Disaster Risk Reduction](https://www.preventionweb.net/) defines such complex events as multi-hazard events involving the simultaneous or sequential occurrence of two or more hazards and their potentially interrelated impacts. For example, the flash floods in Pakistan were likely exacerbated by the wildfires in other regions. Due to connections and feedback between multiple events, the combined impact of a multi-hazard event can be different from the sum of the impacts of multiple individual disasters.

This requires a shift from a fragmented to a more comprehensive approach to disaster reporting, including more frequent and consistent use of multi-risk terminology and adopting a broader definition of multi-hazard events. Improved recognition of multi-hazard events in disaster reporting will provide a more accurate representation of such complex disasters and their impacts, enhancing public awareness and understanding of multi-hazard events. Additionally, more attention to interconnected natural hazards in the reporting of official disaster data can support disaster risk science and management efforts.

Monty is a system that aims to address this challenge by providing a comprehensive and consistent approach to disaster data collection, management, and reporting. As such, the model used by Monty is designed to support the identification and tracking events, hazards, impacts, and responses from various sources. Its model must be flexible enough to cope with the heterogeneity of the data sources and the different representations of the disaster data.

## Monty Approach: correlation identifier

**The Monty system uses a correlation identifier to link the items in the system**. This identifier is generated based on the metadata collected from the data sources.

Monty database collects 4 types of items that cover most of the disaster data from various sources:

- **Event item**: A document that represents a disaster event that has occured or is forecasted to occur. This document contains the information about the event, such as the date and time and location. It also contains the information about the hazards that affected the event by referencing [hazard codes](./taxonomy.md#hazards) and linking to the related hazard items.
- **Hazard item**: A document that represents a process, phenomenon or human activity that may cause loss of life, injury or other health impacts. This document contains the information about the hazard, such as the name, description, a unique [hazard code](./taxonomy.md#hazards) and severity level or magnitude.
- **Impact item**: A document that represents the impact of a hazard on an event. This document contains the information about the impact, such as the number of fatalities, injuries, and affected people.
- **Response item**: *TBD*

> [!IMPORTANT]
> Every source produces at least event items. They are necessary to provide the context for the other items. As described in the next section, the correlation identifier is generated based on the event item.

### Event Pairing Algorithm

For any type of item, there is a link to an event that represents the context of the item. The event pairing algorithm is used to generate a correlation identifier for the items based on the event metadata. The correlation identifier is used to link the items in the system.

The event pairing algorithm is a function that takes the following parameters:

- Hazards codes: An array with the codes of the event hazards based on different [hazard classification systems](./taxonomy.md#hazards). According to the combination of the hazard codes, the algorithm selects a group code that represents the cluster of the main hazards of the event.
- Country code: The country code of the related event in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) format.
- Date and Time: The date and time of the related event.

The algorithm returns a string with the event id. The event id is a string with the following format:

```console
{datetime}-{country_code}-{hazard_cluster_code}-{episode_number}-GDBC
```

Where:

- `{datetime}`: The date and time of the event in the format `YYYYMMDDThhmmssZ` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)).
- `{country_code}`: The country code of the related event in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) format.
- `{hazard_cluster_code}`: A code that represents the cluster of the main hazards of the event. This code represents the cluster in the [UNDRR-ISC 2020 Hazard Information Profiles](./taxonomy.md#undrr-isc-2020-hazard-information-profiles). The cluster is slected based on the order of the hazards codes provided.
- `{episode_number}`: A number that represents the episode of the event. This number is used to differentiate between events that have the same date, country, and hazard cluster. The episode number starts at 1 and is incremented by 1 for each new event with the same date, country, and hazard cluster.

A reference implementation is provided with the pystac.monty module. *TBD*
