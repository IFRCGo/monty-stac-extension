# CEMS Rapid Mapping — API & Data Model Familiarisation

Hands-on exploration of the live CEMS Rapid Mapping API. Public, no auth. Sample
activations captured in this folder: **EMSR847** (storm, rich), **EMSR842** (wildfire,
minimal), **EMSR871** (flood, has FEP), plus list pages.

## 1. Endpoints & access

| Endpoint | Purpose |
|---|---|
| `GET rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/?limit=&offset=` | RM activation **list** (224 activations). DRF pagination: `{count,next,previous,results}`. |
| `GET rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR847` | **Rich activation detail** — AOIs, products, images, stats, cross-refs. **The ETL entry point.** Returns `{count,next,previous,results:[{...}]}` (single result). |
| `GET mapping.emergency.copernicus.eu/activations/api/activations/?limit=&offset=` | Unified list (RM + Risk&Recovery). Different shape (`category` is an object `{slug,name}`, has `drmPhase`, `search_snippet`). Discovery only. |

- Pagination: `limit`/`offset`; list `count=224`. No auth, no obvious rate limit hit during exploration.
- Licence: Copernicus — free & open, attribution "© European Union, Copernicus Emergency Management Service".

## 2. Activation payload (detail endpoint → `results[0]`)

Fields: `code` (EMSR847), `name`, `reason` (free-text description), `category` (Storm),
`subCategory` (Tropical cyclone…), `sensitive` (bool), **`reportLink`** (ArcGIS StoryMap URL
= the **Situational Report**), `activator`, `eventTime`, `activationTime`, `closed` (bool),
**`gdacsId`** (e.g. `TC1001230`), `continent`, `countries` (`[{name}]`), **`aois`** (list),
`centroid` (WKT POINT), `infobulletins`, **`stats`** (aggregated damage figures),
**`charterNumber`** + **`charterUrl`** (Charter co-activation), `extent` (WKT POLYGON),
`aws_bucket`, `productsPath`, `relatedevents`.

Activation-level `stats` = aggregated thematic figures, e.g.
`{"Roads [km]":206.4,"Built-up [ha]":19.5,"Built-up [No.]":48253,"Population [No.]":13030,"max_extent":8552.7}`.

### AOI (`results[0].aois[i]`)
`{name, extent (WKT POLYGON), number, activationCode, products:[...], blpPath}`.

### Product (`aois[i].products[j]`) — maps to Monty **Response**
`{id, type, monitoring (bool), monitoringNumber (int), feasible (bool), images:[...],
stats, mapsCount, activationCode, aoiName, aoiNumber, extent (WKT), expectedDelivery,
layers:[...], downloadPath, version:{...}}`

- **`type`** observed: `REF`, `FEP`, `DEL`, `GRA` (all four RM map products). **`SR` is NOT a product** — it is the activation-level `reportLink` StoryMap.
- **`version`** = `{uuid, number, reason, deliveryTime, statusCode}`. **`statusCode`** observed: `F` (final/produced), `N` (not produced / not feasible). Status lives on `version`, not the product root.
- **`monitoring`/`monitoringNumber`**: base = 0; monitoring iterations = 1, 2, … (EMSR847: monitoringNumber ∈ {0,1,2}).
- **`images[]`** (the acquisition): `{uuid, new, sensorType (sar/optical), sensorName (ICEYE…), resolutionClass (VHR2…), acquisitionTime, fileName}`.
- **`layers[]`** (web/COG assets): `{name, format (cog)}` — ArcGIS/COG raster layers.
- **`downloadPath`**: per-product ZIP, e.g. `…/backend/EMSR847/AOI01/GRA_PRODUCT/EMSR847_AOI01_GRA_PRODUCT_v1.zip`.

### GRA product `stats` — the **Impact** source
Nested `{thematic_class: {sub_class: {unit, total, affected}}}`, e.g.
`{"Landslide":{"None":{"unit":"","total":"NA","affected":1}},"Estimated population":{"None":{"total":84000}}}`.
`total` may be `"NA"`. Only GRA carries per-product stats (REF/DEL/FEP: `stats:null`).

## 3. Validation against the merged taxonomy (`response-taxonomy.md`, `response-best-practices.md`)

- ✅ Product→type-code crosswalk holds: `REF→eo-ref`, `FEP→eo-fep`, `DEL→eo-del`, `GRA→eo-gra`, `SR→eo-sr`.
- ✅ `monitoring`/`monitoringNumber` → `monty:response_detail.monitoring_number` (set only when `monitoring=true`).
- ✅ `statusCode` → `monty:response_detail.status` (need enum mapping: `F`→published/finished, `N`→no-impact/withdrawn; confirm other codes exist historically).
- ✅ `resolutionClass` (on `images[]`) → carried on the linked acquisition, not the Response root.
- 🟢 `eventTime` vs `activationTime` — two distinct timestamps (event onset vs Charter/CEMS activation). Onset = `eventTime`.
- ❓ `eo-sr` is **resolved as Response** in the taxonomy; structurally the SR is a StoryMap URL (`reportLink`), a produced report — consistent with Response. No geospatial asset; model as a Response item whose asset is the StoryMap link.

### 3b. Cross-source linkage — derive `related` links, not just a shared `corr_id`

The activation carries hard cross-references to sibling sources. Beyond co-referencing
via a shared `monty:corr_id`, the ETL **SHOULD derive the target source's Monty item id
and emit an explicit `rel: related` link** (with the appropriate `roles`). This makes the
graph navigable directly (`related`) instead of only query-joinable (`corr_id`).

| CEMS field | Example | Target Monty item id (derivation) | Link to emit |
|---|---|---|---|
| `gdacsId` | `TC1001230` | GDACS uses `{eventtype}` + `{eventid}`; Monty id = `{eventid}-{episodeid}` in collection `gdacs-events` (e.g. `1001230-1`). Split `TC`/`1001230`; resolve/assume episode (default `1`, or link at event level). | `rel: related`, `roles: ["event"]` → GDACS **Event** |
| `charterNumber` (+ `charterUrl`) | `996` | Charter Monty Event id = `charter-event-{activation_id}` → `charter-event-996` (collection `charter-events`); Charter VAP/eo-dat Responses under `charter-response`. | `rel: related`, `roles: ["event"]` → Charter **Event** (and optionally `roles: ["response"]` to Charter VAP Responses) |

Notes (all resolved in the analysis doc — see [`README.md`](./README.md)):

- **Episode ambiguity for GDACS**: `gdacsId` gives eventtype+eventid but not the episode; decide whether to link the latest episode, all episodes, or the event without episode.
- **Existence**: the target item may not yet be ingested in Montandon; emit the `related`
  link by convention regardless (id is deterministic), or gate on presence — a #21 decision.
- **Generalise**: treat this as a reusable pattern — any source cross-ref field that yields a
  deterministic source-item id (GLIDE, Charter, GDACS, EMSR↔EMSR `relatedevents`) becomes a
  typed `related` link, keeping `corr_id` as the fallback join.
- Same idea applies **outward**: the Charter source doc already links a VAP to sibling
  Responses via `related`/`response` — the CEMS↔Charter edge should be reciprocal.

## 4. Data access patterns

- **Detail endpoint is the ETL unit**: one call per activation code yields everything (AOIs → products → images/stats/layers/downloads).
- Discover codes via the list endpoint (paginated, 224 RM activations; `category` values seen: Flood, Wildfire, Storm, Earthquake, Other).
- Assets: per-product `downloadPath` (ZIP of vector+raster), `layers[]` (COG), `images[].fileName` (source imagery). `aws_bucket` + `productsPath` give S3/backend roots.
- Cross-source keys on the activation: `gdacsId` (GDACS), `charterNumber`/`charterUrl` (Charter).

## 5. Open items to carry into the analysis (historical — now resolved)

> **Superseded.** These were the open questions at familiarisation time. They are **all
> resolved** in the analysis doc — see [`README.md` → Decisions (resolved)](./README.md#decisions-resolved).
> This section is retained only as a record of the original exploration; do **not** treat it
> as open work.

1. Full **`statusCode` enum** (only `F`,`N` seen) and its `monty:response_detail.status` mapping.
2. **FEP/REF** field completeness (fewer samples) — confirm images/assets shape.
3. **Category → `monty:hazard_codes`** crosswalk (CEMS `category`/`subCategory` → UNDRR-ISC) — needs a table like Charter's.
4. **Monitoring lineage**: how to link monitoring iteration *n* to *n-1* (`rel: prev`?) — `version.number` vs `monitoringNumber`.
5. **AOI → geometry**: model per-AOI (like Charter Area→Hazard) or per-product extent.
6. **RSS feeds** (WP2 trigger) not yet explored — listed in the epic but out of WP1 ETL scope.
7. Reference activations for tests: **EMSR847** (storm, Charter+GDACS cross-refs, monitoring, 67 products), **EMSR871** (flood, has FEP), **EMSR842** (wildfire, minimal, 2 GRA).
