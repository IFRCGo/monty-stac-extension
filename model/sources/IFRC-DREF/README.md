# IFRC DREF & EA

API: https://alpha-1-api.ifrc-go.dev.datafriendlyspace.org/api/v2/appeal/?limit=50&offset=0&ordering=-id&format=json
Note: Always include the filter `limit` and `format=json` to prevent source crash

## Collection: `ifrc-dref-events`
Collection: ifrc-dref-events
A STAC collection hold all the GIDD events.

Name: Disaster Relief Emergency Fund and Emergency Appeals

Code: DREF & EA

Source organisation: Internation Federation of Red Cross and Red Crescent Societies

Source code: IFRC

Source URL: https://go.ifrc.org/

Source for: event, impact


## Example:
Here `atype=0` represents DREF data while `atype=1` represents Emergency Appeals.

```

      "aid": "3550",
      "name": "Mozambique - Floods & Cyclones",
      "dtype": {
        "id": 12,
        "summary": "",
        "name": "Flood",
        "translation_module_original_language": "en"
      },
      "atype": 1,
      "atype_display": "Emergency Appeal",
      "status": 1,
      "status_display": "Closed",
      "code": "MDRMZ002",
      "sector": "Country cluster for Mozambique and Angola",
      "num_beneficiaries": 117235,
      "amount_requested": 20633392.0,
      "amount_funded": 8513236.83,
      "start_date": "2007-01-19T00:00:00Z",
      "end_date": "2007-08-16T00:00:00Z",
      "real_data_update": "2023-01-03 10:45:02+00:00",
      "created_at": "2018-02-22 04:43:28.710144+00:00",
      "modified_at": "2024-09-09 02:46:05.663711+00:00",
      "event": 1200,
      "needs_confirmation": false,
      "country": {
        "iso": "MZ",
        "iso3": "MOZ",
        "id": 120,
        "record_type": 1,
        "record_type_display": "Country",
        "region": 0,
        "independent": true,
        "is_deprecated": false,
        "fdrs": "DMZ001",
        "average_household_size": null,
        "name": "Mozambique",
        "society_name": "Mozambique Red Cross Society",
        "translation_module_original_language": "en"
      }
```

### Data
The International Federation of Red Cross and Red Crescent Societies’ Disaster Response Emergency Fund (IFRC-DREF) is an efficient, fast, transparent, and localized way of getting funding directly to local humanitarian actors – both before and after crisis hits. 

### IFRC DREF & EA Events

| STAC field             | IBTrACS Field                        | Remarks                                           |
| ---------------------- | ------------------------------------ | ------------------------------------------------- |
| id                     | id                                   |                                                   |
| collection             | `ifrc-dref-events`                   | Collection name for STAC                          |
| title                  | name                                 |                                                   |
| geometry               | polygon to be extracted from country |                                                   |
| start_datetime         | start_date                           |                                                   |
| end_datetime           | end_date                             |                                                   |
| monty:country_codes[0] | country.iso3                         |                                                   |
| monty:hazard_codes     | to be derived from `dtype.name`      |                                                   |

### IFRC DREF & EA Impact

| STAC field             | IBTrACS Field                        | Remarks                  |
| ---------------------- | ------------------------------------ | ------------------------ |
| id                     | id                                   |                          |
| collection             | `ifrc-dref-impacts`                  | Collection name for STAC |
| title                  | name + atype_display                 |                          |
| geometry               | polygon to be extracted from country |                          |
| start_datetime         | start_date                           |                          |
| end_datetime           | end_date                             |                          |
| monty:country_codes[0] | country.iso3                         |                          |
| monty:hazard_codes     | to be derived from `dtype.name`      |                          |
