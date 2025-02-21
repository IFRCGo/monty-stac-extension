{
  "stac_version": "1.0.0",
  "stac_extensions": [
    "https://ifrcgo.github.io/monty/v0.1.0/schema.json"
  ],
  "type": "Collection",
  "id": "idmc-gidd-events",
  "title": "IDMC GIDD Source Events",
  "description": "Global Internal Displacement Database (GIDD) Events",
  "license": "TBD",
  "roles": [
    "event",
    "source"
  ],
  "providers": [
    {
      "name": "Internal Displacement Monitoring Centre",
      "roles": [
        "producer"
      ],
      "url": "https://www.internal-displacement.org/database",
      "email": "info@idmc.ch"
    }
  ],
  "extent": {
    "spatial": {
      "bbox": [
        [
          -180,
          -90,
          180,
          90
        ]
      ]
    },
    "temporal": {
      "interval": [
        [
          "2008-01-01T00:00:00Z",
          null
        ]
      ]
    }
  },
  "summaries": {
    "datetime": {
      "minimum": "2008-01-01T00:00:00Z",
      "maximum": "2025-01-23T00:00:00Z"
    },
    "roles": [
      "event",
      "source"
    ],
    "monty:country_codes": [
      "IDN"
    ],
    "monty:hazard_codes": [
      "nat-met-sto-tro"
    ]
  },
  "links": [
    {
      "href": "idmc-gidd-events.json",
      "rel": "self"
    }
  ]
}
