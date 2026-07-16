# Response Best Practices — STAC Extension Combinations

> **Status:** Initial best-practices document accompanying the v1.3 introduction of `monty:response_detail`.

This document specifies which STAC extensions Monty Response items SHOULD or MUST declare, per response type and per source system. The governing principle is **extension layering over duplication**: where a suitable third-party STAC extension exists, Response items declare it alongside `monty:` rather than copying its fields into `monty:response_detail`.

---

## 1. Governing principles

1. **Extension layering over duplication.** When a third-party STAC extension covers a concept (e.g., Terradue `disaster:` for International Charter items, `processing:` for derived EO products, `eo:` / `sar:` / `sat:` for source imagery), Response items SHOULD declare that extension and use its fields directly. Do NOT replicate those fields under `monty:response_detail`.
2. **Acquisition vs. Response layer separation.** `sat:`, `eo:`, `sar:`, `view:` extensions describe the **acquisition / source imagery** that the Response product is derived from. They apply to the linked acquisition items reached via `derived_from`, **not** to the Response product item itself. A Monty Response item for a CEMS Grading Product is a derived product — its STAC extensions describe its provenance and classification, not the raw imagery. **Exception:** an `eo-dat` Response item *is* the delivered dataset, so it carries the imagery-layer extensions directly (see §2 and §4.4).
3. **`monty:` is always declared.** Every Response item declares the Monty extension and carries at least `monty:response_detail.type`, `monty:corr_id`, `monty:country_codes`, `monty:hazard_codes`, and the `response` role.
4. **`monty:response_detail` is the residual carrier.** It carries the response type code and Monty-specific metadata that is not already expressed by another declared extension on the same item.
5. **Statistical figures go to Impact items.** Damage / exposure statistics that EO products may carry (e.g., CEMS `affected` / `total` per thematic) are **not** part of `response_detail` — they belong to separate Monty Impact items linked via `monty:corr_id`.

---

## 2. Extension combinations per response type

| Response type (`monty:response_detail.type`) | Extensions to declare on the Response item | Notes |
| --- | --- | --- |
| `eo-dat` *(satellite imagery dataset delivered as the response deliverable)* | `monty:` **+** `eo:` / `sar:` / `sat:` *(the item IS the imagery)* **+** `disaster:` *(MANDATORY for Charter acquisitions, with `disaster:class = acquisition`)* | The most basic EO response, and the one case where the Response item and the acquisition item **coincide**: the deliverable is the dataset itself (e.g., a Charter `acquisition`, a UNOSAT GIS-ready download). Each delivered dataset is an `eo-dat` Response item. For the Charter, an acquisition is recorded at several ETL stages — keep only the **last, calibrated stage** (the dataset responders use to build VAPs); earlier-stage records are intermediate artifacts, not separate Response items. The imagery-layer extensions (`eo:` / `sar:` / `sat:`) are declared **on** the Response item; because the calibrated dataset is itself a Response item, derived VAP Response items reference it as a **sibling Response** (`rel: related`, `roles: ["response"]`), not via `derived_from`. See the acquisition row below and [taxonomy §2.1](./response-taxonomy.md#21-eo-response-products). |
| `eo-ref`, `eo-fep`, `eo-del`, `eo-gra`, `eo-pop`, `eo-mon`, `eo-sr`, `eo-vap` *(CEMS-sourced)* | `monty:` **+** `processing:` *(recommended)* | No CEMS-specific STAC extension exists. CEMS `statusCode` and `monitoringNumber` are carried under `monty:response_detail` (as `status` and `monitoring_number`). `resolutionClass` is carried on the linked acquisition items (not on the Response item). `charterNumber` is modelled as a `rel: related` link (with `roles: ["response"]`) to the corresponding Charter VAP Response item. |
| `eo-ref`, `eo-del`, `eo-gra`, `eo-pop`, `eo-vap` *(International Charter VAPs)* | `monty:` **+** `disaster:` *(MANDATORY)* **+** `processing:` *(recommended)* | Reuse `disaster:class = vap`, `disaster:activation_id`, `disaster:call_ids`, `disaster:activation_status`, `disaster:resolution_class`, `disaster:types`. Do NOT duplicate these under `monty:response_detail`. |
| `eo-fep`, `eo-del`, `eo-gra`, `eo-pop`, `eo-mon` *(UNOSAT-sourced)* | `monty:` **+** `processing:` *(recommended)* | No UNOSAT STAC extension exists. |
| `hum-*` *(IFRC / cluster-based humanitarian)* | `monty:` *(only)* | No directly relevant third-party extension. Sectors carried in `monty:response_detail.sectors`. |
| `fin-*` *(IFRC DREF / EA / AA / PDNA)* | `monty:` *(only)* | Financial-amount fields are not yet part of `monty:response_detail`; tracked as a proposal in the [response taxonomy](response-taxonomy.md) and out of scope for v1. |
| *(Acquisition / source imagery — linked via `derived_from`)* | `sat:`, `eo:`, `sar:`, `view:`, `disaster:` *(for Charter acquisitions, with `disaster:class = acquisition`)*, `processing:` | These are **not** Monty Response items themselves; they are upstream items referenced by Response items via `rel: derived_from`. (Contrast `eo-dat` above: the final calibrated dataset the Charter delivers *is* kept as a Response item; earlier ETL-stage acquisition records and other non-delivered source imagery remain upstream-only and are referenced via `derived_from`.) |

> The Response item's `stac_extensions` array MUST contain `https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json` (or newer). The relative ordering of extension URLs is not significant.

---

## 3. Field carriage by source — what goes where

The tables below show which field carries which concept on each source's Response items. Use this to decide whether to populate a `monty:response_detail.*` field or rely on another extension's field on the same item.

### 3.1 CEMS Rapid Mapping

CEMS Response items declare `monty:` (+ optionally `processing:`). They do **not** declare `disaster:`.

| Concept | CEMS API field | Carried on Monty Response item as |
| --- | --- | --- |
| Activation code | `code` (e.g., `EMSR744`) | `monty:response_detail.source_id` |
| Product type | `type` (`REF` / `FEP` / `DEL` / `GRA` / `SR`) | `monty:response_detail.type` (mapped per [taxonomy §2.1](./response-taxonomy.md#21-eo-response-products)) |
| Monitoring iteration | `monitoring`, `monitoringNumber` | `monty:response_detail.monitoring_number` (set only on monitoring updates; absent on the initial product) |
| Product status | `statusCode` (`F` / `N` / `W` / `I`) | `monty:response_detail.status` (mapped: `F→finished`, `N→no-impact`, `W→planned`, `I→in-production`) |
| Resolution class | `resolutionClass` | Carried on the linked acquisition items (via `eo:gsd` / `sat:` / `disaster:resolution_class` where applicable) — not on the Response item itself |
| Charter co-activation | `charterNumber` | `rel: related` link (with `roles: ["response"]`) to the corresponding Charter VAP Response item; the Charter VAP item itself carries `disaster:activation_id` |
| Producer | (provider metadata) | `monty:response_detail.producer` (typically `JRC` or contracted VAP provider) |
| Methodology | (implicit) | `monty:response_detail.methodology` (typically `human_interpreted` or `semi_automated`) |
| Sendai targets | — | `monty:response_detail.sendai_targets` (see [taxonomy §5](./response-taxonomy.md#5-sendai-framework-crosswalk)) |
| Damage statistics | `affected` / `total` per thematic | **NOT** in `response_detail` — emit as separate Monty Impact items linked via `monty:corr_id` |

### 3.2 International Charter

Charter VAP Response items declare `monty:` **+** `disaster:` (+ optionally `processing:`). Fields already covered by `disaster:` MUST be carried on `disaster:` and MUST NOT be duplicated under `monty:response_detail`.

| Concept | Carried on Monty Response item as |
| --- | --- |
| Charter object type | `disaster:class = vap` |
| Activation id | `disaster:activation_id` |
| Call id(s) | `disaster:call_ids` |
| Activation status | `disaster:activation_status` |
| Resolution class | `disaster:resolution_class` |
| Hazard types | `disaster:types` (and `monty:hazard_codes` for Monty / UNDRR-ISC interoperability) |
| Country | `disaster:country` (and `monty:country_codes`) |
| Product type code | `monty:response_detail.type` (best-effort: `eo-del` / `eo-gra` / `eo-pop` / `eo-vap` fallback) |
| Charter-provided VAP id | `monty:response_detail.source_id` (e.g., `1144-1` — `{call_id}-{vap_number}`; activation id is on `disaster:activation_id`) |
| Source landing page | STAC `rel: derived_from` link to the source-system product page (`href` = canonical URL) |
| Producer (VAP provider) | `monty:response_detail.producer` |
| Methodology | `monty:response_detail.methodology` |

> **Charter activations themselves** (`disaster:class = activation`) are modelled as Monty **Event** items, not Response items. **VAPs** and **calibrated acquisition datasets** become Monty Response items (`eo-del` / `eo-gra` / … and `eo-dat` respectively). See [Charter source mapping](sources/Charter/README.md).

### 3.3 UNOSAT Rapid Mapping

UNOSAT Response items declare `monty:` (+ optionally `processing:`). No UNOSAT STAC extension exists.

| Concept | UNOSAT field / convention | Carried on Monty Response item as |
| --- | --- | --- |
| Product identifier | UNOSAT product code (e.g., `FL20240926ESP`) | `monty:response_detail.source_id` and item `id` |
| Phase | Phase 0 / 1 / 2 / 3 | Mapped to `monty:response_detail.type` per [taxonomy §3.1](./response-taxonomy.md#31-choosing-a-code) classification guidance (`Phase 1 → eo-fep`, flood extent `→ eo-del`, damage density `→ eo-gra`, population exposure `→ eo-pop`, monitoring `→ eo-mon`) |
| Producer | (typically `UNOSAT`) | `monty:response_detail.producer` |
| Methodology | (varies) | `monty:response_detail.methodology` |
| Sensor / acquisition | Sentinel-1 / Sentinel-2 / ... | Carried on linked acquisition items via `sar:` / `eo:` / `sat:` — **not** on the Response item itself |
| Resolution class | (varies) | Carried on the linked acquisition items, not on the Response item itself |

---

## 4. Worked extension-stack examples

### 4.1 CEMS Delineation product (`eo-del`)

```jsonc
{
  "stac_extensions": [
    "https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json",
    "https://stac-extensions.github.io/processing/v1.2.0/schema.json"
  ],
  "properties": {
    "monty:response_detail": {
      "type": "eo-del",
      "source_id": "EMSR744",
      "status": "published",
      "producer": "JRC",
      "methodology": "human_interpreted",
      "sendai_targets": ["D", "G"]
    },
    "processing:level": "L3",
    "processing:lineage": "Sentinel-1 GRD → flood-mask classifier → vector cleanup"
  },
  "links": [
    {
      "rel": "derived_from",
      "href": "https://emergency.copernicus.eu/mapping/list-of-components/EMSR744",
      "type": "text/html",
      "title": "CEMS EMSR744 activation page"
    }
  ]
}
```

### 4.2 International Charter VAP (`eo-vap`)

```jsonc
{
  "stac_extensions": [
    "https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json",
    "https://terradue.github.io/stac-extensions-disaster/v1.1.0/schema.json"
  ],
  "properties": {
    "disaster:class": "vap",
    "disaster:activation_id": 849,
    "disaster:call_ids": [1421],
    "disaster:activation_status": "open",
    "disaster:resolution_class": "VHR",
    "disaster:types": ["flood"],
    "disaster:country": "ESP",
    "monty:response_detail": {
      "type": "eo-vap",
      "source_id": "1421-1",
      "producer": "Airbus",
      "methodology": "human_interpreted",
      "sendai_targets": ["D", "G"]
    }
  },
  "links": [
    {
      "rel": "related",
      "href": "../charter-events/charter-event-849.json",
      "type": "application/geo+json",
      "roles": ["event"]
    },
    {
      "rel": "derived_from",
      "href": "https://disasterscharter.org/web/guest/activations/-/article/...",
      "type": "text/html",
      "title": "International Charter activation Act-849"
    }
  ]
}
```

Note the absence of `monty:response_detail.status` — it is carried via `disaster:activation_status` on the same item.

### 4.3 UNOSAT damage assessment (`eo-gra`)

```jsonc
{
  "stac_extensions": [
    "https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json",
    "https://stac-extensions.github.io/processing/v1.2.0/schema.json"
  ],
  "properties": {
    "monty:response_detail": {
      "type": "eo-gra",
      "source_id": "FL20240926ESP",
      "status": "published",
      "producer": "UNOSAT",
      "methodology": "human_interpreted",
      "sendai_targets": ["C", "D"]
    },
    "processing:level": "L3",
    "processing:lineage": "Pleiades VHR optical → manual building damage interpretation"
  }
}
```

### 4.4 Charter raw acquisition delivered to responders (`eo-dat`)

Here the response deliverable is the satellite dataset itself, so the Response item and the acquisition item coincide: the imagery-layer extensions (`sat:` / `eo:`) and `disaster:class = acquisition` are carried directly on the Response item. This is the **last, calibrated** ETL stage of the acquisition — the dataset responders use to build VAPs; because the calibrated dataset is itself an `eo-dat` Response item, the derived VAP Response items reference it as a **sibling Response** (`rel: related`, `roles: ["response"]`), not via `derived_from`.

```jsonc
{
  "stac_extensions": [
    "https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json",
    "https://terradue.github.io/stac-extensions-disaster/v1.1.0/schema.json",
    "https://stac-extensions.github.io/eo/v1.1.0/schema.json",
    "https://stac-extensions.github.io/sat/v1.0.0/schema.json"
  ],
  "properties": {
    "disaster:class": "acquisition",
    "disaster:activation_id": 849,
    "disaster:call_ids": [1421],
    "disaster:resolution_class": "VHR",
    "disaster:types": ["flood"],
    "disaster:country": "ESP",
    "eo:cloud_cover": 12,
    "sat:platform_international_designator": "2018-014A",
    "monty:response_detail": {
      "type": "eo-dat",
      "source_id": "ACT-849",
      "producer": "Airbus",
      "sendai_targets": ["D", "G"]
    }
  },
  "links": [
    {
      "rel": "derived_from",
      "href": "https://disasterscharter.org/web/guest/activations/-/article/...",
      "type": "text/html",
      "title": "International Charter activation ACT-849"
    }
  ]
}
```

---

## 5. Anti-patterns

The following patterns SHOULD be avoided:

- **Duplicating `disaster:` fields under `monty:response_detail`** on Charter items — e.g., adding a parallel `monty:response_detail` field for any concept already covered by `disaster:activation_id`, `disaster:activation_status`, `disaster:resolution_class`, etc. On Charter items declaring `disaster:`, the `disaster:` field is canonical.
- **Carrying `sar:` / `eo:` / `sat:` fields on the Response product item.** For *derived* products (`eo-del`, `eo-gra`, `eo-pop`, …) those describe the source imagery, which lives in separate acquisition items linked via `derived_from`. The sole exception is `eo-dat`, where the dataset *is* the deliverable and the Response item and acquisition item coincide (see §4.4).
- **Stuffing damage statistics into `response_detail`.** Damage counts, affected populations, building destruction counts MUST become Monty Impact items (separate STAC items, `roles: ["impact"]`) linked to the Response via `monty:corr_id` (and optionally `rel: related` with `roles: ["impact"]`). See [Response ↔ Impact Boundary Rules](response-impact-boundary.md) for the data-pattern catalogue and the decision tree that resolves, per attribute, whether something stays on the Response item or becomes a paired Impact item.
- **Mixing source code into the type code.** Use `eo-del` (source-agnostic) rather than `eo-cems-del` or `eo-charter-del`. Source provenance lives in `monty:response_detail.source_id`, `monty:response_detail.producer`, and `derived_from` links.
- **Creating multiple `eo-del-mon-N` codes for monitoring iterations.** Use a single `monty:response_detail.monitoring_number = N` field on the monitoring item, mirroring the CEMS API.

---

## 6. Linkage summary

> For the algorithm that decides **when** to split a source record into a Response item plus paired Impact items, the exact `derived_from` link block to emit, the idempotent `corr_id` / id conventions, and the CQL2 queries that re-pair the two halves, see [Response ↔ Impact Boundary Rules](response-impact-boundary.md).

A Monty Response item typically participates in the following links:

| `rel` | Target | `roles` (on link) | Purpose |
| --- | --- | --- | --- |
| `self` | this item | — | Standard STAC self link |
| `collection` | parent collection | — | Standard STAC parent link |
| `reference-event` | the Monty reference event | — | Ties the response to the canonical Monty event (cross-catalog) |
| `source-event` | the source-system event item | — | Ties the response to the source-side event (cross-catalog) |
| `related` | Event item | `["event"]` | Within a source collection, ties the response to its parent Event (typed link per Monty schema) |
| `related` | another Response item | `["response"]` | Cross-reference to a sibling response (e.g., a CEMS Grading product references a prior Delineation product on the same activation) |
| `related` | Hazard item(s) | `["hazard"]` | Indicates which hazard(s) the response addresses |
| `related` | Impact item(s) | `["impact"]` | Optional back-reference to Impact items this response informs. The canonical provenance edge runs the **other way**: each derived Impact item carries a `rel: derived_from` link pointing to this Response item. |
| `derived_from` | Source-system product page (canonical URL) | — | The Monty Response item is derived from this published source product (e.g., the CEMS activation page, the Charter activation page, the UNOSAT product page). Use this rather than embedding the URL in `monty:response_detail`. |
| `derived_from` | Acquisition / source imagery item(s) | — | Provenance chain to the raw imagery the response is derived from (those items carry `sat:` / `eo:` / `sar:`) |
| `prev` | A prior Response item | — | When the current item is a monitoring update of a prior response product (mirrors `monty:response_detail.monitoring_number`) |
| `via` | Source-system landing page (alternative to `derived_from`) | — | When the source-system endpoint is a generic landing or API URL rather than a published product the Monty item was derived from |
