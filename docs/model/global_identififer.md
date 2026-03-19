# Uniquely Identifiable ID [GUID]

The `guid` within the monty extension projects the idea of uniquely identifying a group of items belonging to a same event originating from a particular source. This means, for the similar events originating from different sources, this `guid` will be different as the `Source Name` is used in its construction. It is an extension to the correlation identifier but with a different purpose of uniquely identifying items of an event across all the sources used in Montandon. The identifier is applicable and applied to all the types of Items described within the Montandon ecosystem (Event Item, Hazard Item, Impact Item).

The algorithm returns a string with the event id. The event id is a string with the following format:

```console
{datetime}-{country_code}-{block_id}-{hazard_code}-GCDB-{source_name}-{event_id}-{episode_number}
```

Where:

- `{datetime}`: The date and time of the event in the format `YYYYMMDD` or `YYYYMMDDThhmmssZ` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)).
- `{country_code}`: The country code of the related event in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) format.
- `{block_id}`: The Earth is partitioned into several blocks of size 0.2 degrees latitude/longitude and each block is given unique value. The block id refers to id of that chunk.
- `{hazard_code}`: The primary hazard code from the [2025 UNDRR-ISC Hazard Information Profiles](./taxonomy.md#2025-update) (e.g., `MH0600` for River Flood, `GH0101` for Earthquake). For multi-hazard events, the first hazard code in the array is used. Legacy codes may use simplified forms (e.g., `FL` for flood).
- `{source_name}`: Name of the data source
- `{event_id}`: The event id refers to the unique id of the event set by the data source.
- `{episode_number}`: A number that represents the episode of the event. This number is used to differentiate between events that have the same date, country, and hazard code. The episode number starts at 1 and is incremented by 1 for each new event with the same date, country, and hazard.
