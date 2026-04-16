# Response Taxonomy (Working Document — v0.1)

> **Status:** Working document. Framework survey (including existing STAC extensions) and crosswalk are complete; taxonomy structure recommendation and initial code proposals are pending team review.
>
> **Relates to:** [developmentseed/esa-montandon#12](https://github.com/developmentseed/esa-montandon/issues/12) · Contributes to D1.1 (KO+4m)

---

## 1. Purpose and Scope

The Monty STAC extension currently covers Hazard and Impact data constructs. The Response construct is defined in the Montandon base schema but contains only an `ID_linkage` field — no taxonomy, no detail fields, and no STAC representation.

This document surveys existing disaster response classification frameworks to inform the design of a Response taxonomy for Monty. The taxonomy will be:

- **Action-oriented**: a Response item represents an action taken or a product produced (a CEMS Delineation map, a DREF operation), not an impact estimate
- **EO-first**: Earth Observation response products (Charter, CEMS, UNOSAT) are the primary use case for this contract; humanitarian sectors are secondary but the model must not preclude them
- **Extensible**: structured to accommodate future response types (anticipatory action, field assessments, PDNA, financial appeals) without breaking existing items
- **Separate items**: Response items are separate STAC items linked to their event and impact items via `monty:corr_id` and explicit STAC relation links

The scope boundary with Impact is: **Response = action taken / product produced; Impact = estimated effect on people or assets.** A CEMS Grading Product is a Response that *informs* Impact items; it is not itself an impact.

---

## 2. Framework Survey

### 2.1 OCHA 3W / 4W / 5W

**What it is:** OCHA's *Who does What, Where* (and optionally *When* / *for Whom*) tool collects basic operational presence data from humanitarian actors during emergencies.

**Category structure:**

- No fixed activity taxonomy — activities are free text or drawn from the country-level Humanitarian Response Plan (HRP) activity list
- Organized around **IASC cluster/sector names** as the primary axis (see §2.4)
- Activity status: `planned` / `implemented` / `completed`
- Supplemented by the **Humanitarian Exchange Language (HXL)** hashtag standard (`#sector`, `#activity`, `#org+type`) for machine-readability, but the sector vocabulary is cluster-name-based, not coded

**Hierarchy depth:** 2 levels (cluster → activity), but activity list varies by country context

**Machine-readable codes:** Partial. OCHA maintains a vocabulary service but sector codes are cluster names, not stable short codes.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Not covered |
| Humanitarian sectors | Yes — but only as cluster labels, not an action taxonomy |
| Financial response | No |
| Codes available | Weak (cluster names, not stable codes) |
| Adoption in Monty data | Indirect (IFRC GO uses cluster categories) |

**Verdict:** Reference only. The cluster structure is the organizing principle for 3W data but delegates the actual activity vocabulary to each HRP/context. The IASC cluster system (§2.4) is the better canonical reference for the sector layer.

---

### 2.2 Sendai Framework Monitoring

**What it is:** The Sendai Framework for Disaster Risk Reduction 2015–2030 defines 7 global targets tracked by 38 indicators via the Sendai Monitor.

**Targets:**

| Target | Focus |
| --- | --- |
| A | Substantially reduce global disaster mortality (by 2030) |
| B | Substantially reduce the number of affected people |
| C | Reduce direct disaster economic loss relative to GDP |
| D | Substantially reduce disaster damage to critical infrastructure and disruption of services |
| E | Substantially increase the number of countries with national and local DRR strategies (by 2020) |
| F | Substantially enhance international cooperation to developing countries |
| G | Substantially increase availability and access to multi-hazard early warning systems |

**Action/response relevance:** Targets D, E, F, G deal with infrastructure resilience, DRR strategies, cooperation, and early warning — but **all seven targets are outcome metrics**, not action categories. The framework describes *what to achieve*, not *what actions to take*. There is no action taxonomy in Sendai.

**Hierarchy depth:** Flat (7 targets × 38 indicators; no action type hierarchy)

**Machine-readable codes:** Yes — indicator codes (e.g., C-2, G-1) are used in the monitor. But these are monitoring KPIs, not response action identifiers.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Not covered |
| Humanitarian action taxonomy | Not applicable (outcome metrics only) |
| Codes available | Yes, but wrong semantic layer |
| Adoption in Monty data | No |

**Verdict:** Not suitable as a source taxonomy. Useful for crosswalk annotations (e.g., noting which response types contribute to which Sendai target), but should not drive the taxonomy structure.

---

### 2.3 IFRC Emergency Plan of Action (EPoA) / DREF

**What it is:** The IFRC Disaster Response Emergency Fund (DREF) funds National Society responses through Emergency Plans of Action (EPoA). Each EPoA uses a standard sector structure that is the closest thing IFRC has to an operational response taxonomy.

**Response sectors used in DREF/EPoA operations:**

| Sector | Description |
| --- | --- |
| Shelter and settlements | Temporary/transitional shelter, NFI distribution |
| Health | Emergency health services, epidemic response, psychosocial support |
| WASH | Water, sanitation and hygiene |
| Livelihoods and basic needs | Food, cash and voucher assistance (CVA), multipurpose cash |
| Protection, Gender and Inclusion (PGI) | Mainstreamed across sectors; includes GBV, child protection |
| Community Engagement and Accountability (CEA) | Mainstreamed; feedback mechanisms, communication |
| Disaster Risk Reduction (DRR) | Preparedness, risk reduction actions |
| Education in Emergencies | Schools, learning continuity |
| Migration | Cross-border displacement support |
| Early Recovery | Transitional recovery actions |
| Anticipatory Action (AA) | Pre-crisis triggers and early action protocols (separate DREF pillar) |

**Hierarchy depth:** Flat (sector names, no formal codes)

**Machine-readable codes:** None. Sectors are named strings in EPoA documents. IFRC GO (the operational database) uses internal IDs but these are not published as a stable taxonomy.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Not covered |
| Humanitarian sectors | Yes — comprehensive and IFRC-native |
| Financial response | Partial (DREF funding is tracked; appeal amounts are in impact data) |
| Codes available | No stable public codes |
| Adoption in Monty data | Yes — DREF is a Monty data source |

**Verdict:** High applicability for the humanitarian sector layer. The sector list should map directly to Monty response types for DREF-sourced items. Requires assigning stable codes.

---

### 2.4 IASC Cluster System

**What it is:** The Inter-Agency Standing Committee (IASC) Cluster Approach organizes humanitarian response into 11 global clusters, each led by a designated UN agency. Used in all major international responses.

**11 Global Clusters:**

| Cluster | Lead Agency |
| --- | --- |
| Camp Coordination and Camp Management (CCCM) | UNHCR / IOM |
| Early Recovery | UNDP |
| Education | UNICEF / Save the Children |
| Emergency Telecommunications (ETC) | WFP |
| Food Security | WFP / FAO |
| Health | WHO |
| Logistics | WFP |
| Nutrition | UNICEF |
| Protection | UNHCR |
| Shelter / Non-Food Items (NFI) | UNHCR / IFRC |
| Water, Sanitation and Hygiene (WASH) | UNICEF |

**Protection Areas of Responsibility (AoRs):**

| AoR | Lead |
| --- | --- |
| Gender-Based Violence (GBV) | UNFPA |
| Child Protection | UNICEF |
| Mine Action | UNMAS |
| Housing, Land and Property (HLP) | NRC / UN-Habitat |

**Hierarchy depth:** 2 levels (cluster → AoR, currently only for Protection)

**Machine-readable codes:** No stable short codes. Cluster names are the identifiers used in 3W, HRP, and IATI data.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Not covered |
| Humanitarian sectors | Yes — comprehensive, internationally recognised |
| Codes available | No (cluster names only) |
| Adoption in Monty data | Indirect (IFRC GO uses cluster-aligned sectors) |

**Verdict:** The cluster list is the de facto international standard for humanitarian sector categorization. The IFRC EPoA sectors (§2.3) largely map to clusters. Together they provide the humanitarian response layer. Short codes need to be assigned.

---

### 2.5 International Charter "Space and Major Disasters"

**What it is:** A worldwide collaboration between space agencies providing satellite-derived data and products to support disaster response. Activated within 10 days of fast-onset disasters.

**Activation conditions:** Fast-onset natural or technological disasters (floods, earthquakes, cyclones, wildfires, oil spills, landslides, tsunamis, volcanic eruptions, etc.)

**Activation channels:**

| Channel | Description |
| --- | --- |
| Direct (Authorized User) | National civil protection, UN agencies, authorized organizations call On-Duty Operator |
| UN channel | UN agencies activate via designated UN pathway |
| Asia Pacific | Via Sentinel Asia / Asian Disaster Reduction Centre |

**STAC data model: Terradue `disaster:` extension**

The Charter Mapper system ([charter.esa.int/mapper](https://charter.esa.int/mapper)) uses the **Terradue `disaster:` STAC extension** (`https://terradue.github.io/stac-extensions-disaster/v1.1.0/schema.json`) as its data model. This is the authoritative machine-readable schema for Charter items and must be used — not just referenced — in any Monty integration of Charter data.

**Object model** (defined by `disaster:class`):

```text
Activation  (disaster:class = activation)
  └── Call  (collection — resource mobilization request)
        ├── Acquisition  (disaster:class = acquisition)   ← raw satellite data
        └── VAP          (disaster:class = vap)           ← processed product / map
  └── Area  (disaster:class = area)                       ← affected geographic zone
```

**Fields defined by the `disaster:` extension:**

| Field | Type | Controlled vocabulary | Notes |
| --- | --- | --- | --- |
| `disaster:class` | string (REQUIRED) | `activation`, `area`, `acquisition`, `vap` | Object type in the Charter workflow |
| `disaster:activation_id` | integer | — | Numeric ID of the activation |
| `disaster:call_ids` | [integer] | — | IDs of resource mobilization calls within the activation |
| `disaster:types` | [string] | `fire`, `earthquake`, `volcano`, `storm_hurricane`, `flood`, `cyclone`, `tsunami`, `snow_hazard`, `landslide`, `ice`, `oil_spill`, `explosive_event`, `other` | Hazard type — overlaps with `monty:hazard_codes` |
| `disaster:country` | string | ISO 3166-1 alpha-3 | Overlaps with `monty:country_codes` |
| `disaster:regions` | [string] | Free text | Sub-national regions |
| `disaster:activation_status` | string | `open`, `closed`, `archived` | Activation lifecycle state |
| `disaster:resolution_class` | string | `VLR`, `LR`, `MR`, `HR`, `VHR` | Spatial resolution class of acquisition items |

**Product types** (expressed via `disaster:class = vap`):

The `disaster:` extension classifies all processed Charter outputs as `vap` (Value-Added Product). The specific product type within the VAP (reference map, delineation, grading) is not further differentiated by the extension — this is the gap that Monty response type codes fill.

| Monty product concept | `disaster:class` | Analogous CEMS type | Notes |
| --- | --- | --- | --- |
| Activation record | `activation` | — | Event-level record; consider modelling as Monty Event, not Response item |
| Satellite acquisition | `acquisition` | — | Source imagery; not a Response item; carries `sar:` / `eo:` / `sat:` fields |
| Reference map | `vap` | `REF` | Pre-event basemap |
| Delineation map | `vap` | `DEL` | Affected area extent |
| Grading map | `vap` | `GRA` | Damage intensity |
| Value-added analysis | `vap` | — | Population exposure, sectoral damage |

**Imagery types delivered:** Optical (Landsat, SPOT, Pleiades) and SAR (TerraSAR-X, TanDEM-X, RADARSAT)

**Machine-readable codes:** The `disaster:` extension provides object-type codes (`activation`, `area`, `acquisition`, `vap`) and hazard-type codes, but **not** product-type codes distinguishing delineation from grading. Monty response type codes (`eo-charter-del`, `eo-charter-gra`, etc.) are needed to fill this gap.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Yes — core use case; `disaster:` extension is the live data model |
| Humanitarian sectors | No |
| STAC extension exists | Yes — `disaster:` (Proposal, owned by @emmanuelmathot) |
| Codes available | Partial — `disaster:class` classifies object type; response product type codes still needed |
| Adoption in Monty data | Target for integration (SW1.2); `disaster:` must be declared alongside `monty:` |

**Verdict:** High applicability. Monty Charter Response items (`vap` objects) must declare both `monty:` and `disaster:` extensions. The `disaster:` extension covers object identity and Charter workflow fields; `monty:response_detail` adds the response type code and Monty-specific semantics. Fields already in `disaster:` (`activation_id`, `activation_status`, `resolution_class`) must not be duplicated in `response_detail`.

---

### 2.6 Copernicus Emergency Management Service (CEMS) Rapid Mapping

**What it is:** EU-funded satellite mapping service for emergency response activated by eligible requestors (civil protection authorities, UN, humanitarian organizations). The most formally specified EO product taxonomy of all frameworks surveyed.

**5 Product Types:**

| Code | Name | Timing | Description |
| --- | --- | --- | --- |
| `REF` | Reference Product | Pre-event | Baseline knowledge of territory and assets prior to the emergency. Only for activations outside Europe. |
| `FEP` | First Estimate Product | Post-event, immediate | Extremely fast (~hours) rough assessment of most affected locations. Used to orient response or decide on further product requests. |
| `DEL` | Delineation Product | Post-event | Event impact extent and affected area. Can be updated (Monitoring). Derived from imagery acquired immediately after the emergency. |
| `GRA` | Grading Product | Post-event | Damage grade, its spatial distribution and extent. Superset of DEL; only available if delineation was previously requested. Can be updated (Monitoring). |
| `SR` | Situational Report | Cross-cutting | Online report presenting the event and activation in a visual and informative way. Starts within 4 hours of activation; regularly updated. |

**Monitoring updates:** DEL and GRA products can have monitoring iterations (`DEL-MON`, `GRA-MON`) to track evolving events.

**Hierarchy depth:** Flat (5 product types + monitoring variants)

**Machine-readable codes:** Yes — 3-letter uppercase codes (REF, FEP, DEL, GRA, SR) are stable, published, and used in CEMS metadata. The most code-ready system of all frameworks surveyed.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Yes — directly applicable, codes ready to use |
| Humanitarian sectors | No |
| Codes available | Yes — best code readiness of all frameworks |
| Adoption in Monty data | Target for integration (SW1.2) |

**Verdict:** Primary source for EO response product codes. CEMS codes should be the basis for the `eo` domain of the Monty response taxonomy, extended with Charter and UNOSAT mappings.

---

### 2.7 UNOSAT Rapid Mapping

**What it is:** UNITAR's satellite analysis service producing humanitarian mapping products, primarily for UN agencies and humanitarian organizations. Largest focus: floods (61% of activations).

**Service phases and product types:**

| Phase | Timeframe | Products |
| --- | --- | --- |
| Phase 0 — Pre-Crisis | Before event | Baseline / preparedness maps |
| Phase 1 — Preliminary Situation Awareness | ~24 hours post-event | Preliminary flood/damage extent, affected area overview |
| Phase 2 — Impact/Damage Assessment | ~72 hours | Damage density maps, sectoral assessments (shelter, agriculture, health/education), population exposure |
| Phase 3 — Ongoing Analysis | 2+ weeks | Flood monitoring, cumulative flood extent, time-series analysis, AI-assisted mapping |

**Product categories (within phases):**

- Flood extent (SAR-based, Sentinel-1)
- Damage assessment (shelter, agriculture, infrastructure)
- Population exposure analysis
- Sectoral damage assessment
- Cumulative / monitoring flood extent
- Statistical reports and data downloads (GIS-ready)

**Machine-readable codes:** No. UNOSAT uses descriptive names and no published code vocabulary.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | Yes — core use case |
| Humanitarian sectors | No |
| Codes available | No — needs code assignment |
| Adoption in Monty data | Target for integration |

**Verdict:** High applicability. The UNOSAT phase/product structure is more granular than CEMS but lacks formal codes. The product types partially overlap with CEMS (e.g., Phase 1 ≈ FEP, Phase 2 ≈ DEL/GRA). A crosswalk and code assignment is needed.

---

### 2.8 PDNA Framework (World Bank / EU / UN)

**What it is:** The Post-Disaster Needs Assessment (PDNA) is a joint WB/EU/UN methodology for assessing disaster impacts and defining recovery strategies, including financial resource requirements.

**Sector groups and sub-sectors:**

| Group | Sub-sectors |
| --- | --- |
| **Social Sectors** | Housing and Settlements; Education; Health; Culture; Nutrition |
| **Productive Sectors** | Agriculture, livestock, fisheries, forestry; Industry, commerce and trade; Tourism |
| **Infrastructure Sectors** | Water, Sanitation and Hygiene (WASH); Community Infrastructure; Energy and Electricity |
| **Cross-cutting Themes** | Employment and Livelihoods; Disaster Risk Reduction (DRR); Governance; Environment; Gender; HIV/AIDS and Age |

**Relationship to Response:** PDNA is a **post-disaster assessment methodology** conducted weeks to months after a disaster, focused on recovery planning and financial needs estimation. It is not an operational response taxonomy.

**Machine-readable codes:** None.

**Applicability to Monty:**

| Aspect | Assessment |
| --- | --- |
| EO products | No |
| Humanitarian action taxonomy | No (assessment/planning, not operational action) |
| Financial response | Yes — recovery cost estimation |
| Codes available | No |
| Adoption in Monty data | No |

**Verdict:** Out of scope for the initial taxonomy. The PDNA sector list overlaps with IASC clusters but is recovery-planning oriented. It should be documented as a future extension possibility, not a primary source.

---

### 2.9 Existing STAC Extensions

Before proposing new fields, we surveyed existing STAC extensions that model disaster response or EO product metadata.

#### 2.9.1 Terradue Disaster Charter Extension (`disaster:`)

The `disaster:` extension is the live data model powering the Charter Mapper system and is analysed in full as part of §2.5 (International Charter). See §2.5 for the complete field list, object model, and implications for Monty.

**Summary:** Charter VAP items must declare both `monty:` and `disaster:` extensions. Fields already defined in `disaster:` (`activation_id`, `activation_status`, `resolution_class`) must not be duplicated in `monty:response_detail`.

#### 2.9.2 CEMS Rapid Mapping — No STAC Extension Exists

CEMS provides a proprietary REST API (OpenAPI) rather than a STAC catalog. There is no published STAC extension for CEMS Rapid Mapping products. The Copernicus Data Space Ecosystem (CDSE) has a general STAC catalog for Sentinel satellite imagery but it does not cover CEMS emergency mapping products.

**Key API fields that should inform Monty `response_detail`:**

| API field | Type | Description | Monty mapping candidate |
| --- | --- | --- | --- |
| `code` | string | Activation identifier (EMSR-XXXX) | `response_detail.source_id` |
| `category` / `subCategory` | string | Hazard event category | Already in `monty:hazard_codes` |
| Product `type` | string | `REF`, `FEP`, `DEL`, `GRA`, `SR` | Response type code |
| Product `monitoring` | boolean | Whether this is a monitoring update | `response_detail.monitoring` |
| Product `monitoringNumber` | integer | Monitoring sequence number | `response_detail.monitoring_number` |
| Product `statusCode` | string | `F`=Finished, `N`=No impact, `W`=Waiting, `I`=In production | `response_detail.status` |
| Image `sensorType` | string | `optical` or `radar` | `response_detail.sensor_type` (or via `eo:`/`sar:` extensions) |
| Image `resolutionClass` | string | `VHR1`, `HR`, etc. | `disaster:resolution_class` (reuse Terradue field) |
| `charterNumber` | string | If Charter co-activation exists | `disaster:activation_id` |
| Stats (`affected`, `total` per thematic) | object | Damage/exposure stats by theme | → Impact items, not Response |

**Gap:** A Monty-aligned STAC extension (or profile) for CEMS Rapid Mapping products is a deliverable of this contract (SW1.1). It should build on the existing CEMS API field semantics while expressing them in STAC.

#### 2.9.3 UNOSAT — No STAC Extension Exists

No STAC extension or catalog for UNOSAT rapid mapping products has been found. UNOSAT distributes products via HDX (Humanitarian Data Exchange) in GIS formats with HTML metadata pages. There is no structured machine-readable schema equivalent to the CEMS API or the Charter extension.

**Implication:** UNOSAT product metadata will need to be mapped to Monty Response fields without an existing STAC anchor. The phase-based structure (PSA / Damage Assessment / Population Exposure / Monitoring) and the CEMS crosswalk proposed in §4 are the primary structuring reference.

#### 2.9.4 Other Relevant STAC Extensions

| Extension | URL | Relevance to Response items |
| --- | --- | --- |
| `sar:` | [stac-extensions/sar](https://github.com/stac-extensions/sar) | For SAR-derived flood/damage products (UNOSAT Sentinel-1 based) |
| `eo:` | [stac-extensions/eo](https://github.com/stac-extensions/eo) | For optical imagery products (Charter acquisitions) |
| `sat:` | [stac-extensions/sat](https://github.com/stac-extensions/sat) | Satellite orbit/platform metadata for acquisition items |
| `eq:` (earthquake) | [stac-extensions/earthquake](https://github.com/stac-extensions/earthquake) | Structural pattern for hazard-type-specific fields; same owners (@emmanuelmathot) |
| `processing:` | [stac-extensions/processing](https://github.com/stac-extensions/processing) | Processing chain metadata — relevant for derived EO products |

These extensions apply to the **acquisition/source imagery layer**, not to the Response product layer. A Monty Response STAC item for a CEMS Grading Product would link to acquisition items (via `derived_from`) that carry the `sar:`, `eo:`, and `sat:` fields.

### 2.10 Crosswalk Summary

The table below maps response concepts across frameworks and assesses readiness for Monty integration.

| Response concept | OCHA 3W | Sendai | IFRC EPoA | IASC Cluster | Int'l Charter | CEMS | UNOSAT | PDNA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Satellite imagery / EO product | — | — | — | — | ✓ | ✓ (codes) | ✓ | — |
| Pre-event reference mapping | — | — | — | — | Reference map | `REF` | Phase 0 | — |
| Rapid damage extent mapping | — | — | — | — | Delineation map | `FEP`, `DEL` | Phase 1, 2 | — |
| Damage intensity/grading | — | — | — | — | Grading map | `GRA` | Phase 2 | — |
| Population exposure analysis | — | — | — | — | Value-added | — | Phase 2 | — |
| Shelter response | Shelter cluster | — | Shelter | Shelter/NFI | — | — | — | Housing |
| Health response | Health cluster | — | Health | Health (WHO) | — | — | — | Health |
| WASH | WASH cluster | — | WASH | WASH (UNICEF) | — | — | — | WASH |
| Food security / livelihoods | Food Security | — | Livelihoods | Food Security | — | — | — | Agriculture |
| Protection | Protection cluster | — | PGI | Protection + AoRs | — | — | — | — |
| Early warning / preparedness | — | Target G | DRR | — | — | — | Phase 0 | DRR |
| Financial / appeal | — | — | DREF/EA | — | — | — | — | — |
| Recovery planning | Early Recovery | — | Early Recovery | Early Recovery | — | — | — | ✓ (all sectors) |
| Anticipatory action | — | — | AA Pillar | — | — | — | — | — |

**Code availability summary:**

| Framework | Stable machine-readable codes? | Existing STAC extension? | Readiness |
| --- | --- | --- | --- |
| CEMS Rapid Mapping | Yes (`REF`, `FEP`, `DEL`, `GRA`, `SR`) | No — REST API only | Immediate (codes), gap (STAC) |
| International Charter | No | Yes — `disaster:` (Terradue) | Adopt `disaster:` extension + add Monty response type codes |
| UNOSAT | No | No | Crosswalk to CEMS phases; no STAC anchor |
| IFRC EPoA | No (names only) | No | Needs code assignment |
| IASC Cluster | No (names only) | No | Needs code assignment |
| OCHA 3W | Partial (HXL cluster names) | No | Needs code assignment |
| Sendai Framework | Yes (indicator codes) | No | Wrong semantic layer |
| PDNA | No | No | Out of scope (v1) |

---

## 3. Taxonomy Design Recommendation

> **Note:** This section presents a structural recommendation derived from the framework survey. The specific code values in §4 are proposals for team discussion — they are not final.

### 3.1 Relationship to Existing STAC Extensions

The survey (§2.9) revealed one directly relevant existing STAC extension: the Terradue `disaster:` extension for International Charter items. This changes the design approach: **Monty Response items should declare multiple STAC extensions** rather than trying to replicate all fields under the `monty:` prefix.

**Extension layering strategy:**

| Item type | Extensions to declare | Notes |
| --- | --- | --- |
| Charter activation / VAP | `monty:` + `disaster:` | Reuse `disaster:class`, `disaster:activation_id`, `disaster:activation_status`, `disaster:resolution_class` |
| CEMS rapid mapping product | `monty:` + `processing:` | No CEMS-specific STAC extension exists; `processing:` covers provenance chain |
| UNOSAT product | `monty:` + `processing:` | No UNOSAT STAC extension exists |
| Charter / CEMS acquisition (source imagery) | `disaster:` + `sar:` / `eo:` + `sat:` | These are linked via `derived_from`, not Monty Response items themselves |

The `monty:response_detail` field (analogous to `hazard_detail` and `impact_detail`) remains the primary place for the **response type code** and Monty-specific metadata. Fields already covered by `disaster:` or `processing:` should not be duplicated in `response_detail`.

### 3.2 Hierarchy: Two-level (domain → type)

**Recommendation:** A **two-level hierarchy** — `domain → type` — is the appropriate structure for the Monty response taxonomy at this stage.

**Rationale:**

- The hazard taxonomy uses UNDRR's 4-level structure (type → cluster → specific hazard → variant) because there are 281 hazards requiring fine-grained disambiguation. The response space is much smaller and less settled.
- The impact taxonomy uses a flat structure (category × type matrix). Response is closer to impact in complexity but has a domain axis (EO vs. humanitarian vs. financial) that warrants one grouping level.
- A 3-level structure would be premature: the second level can always be split later without breaking existing codes.
- All frameworks surveyed use either flat or 2-level structures; the `disaster:class` vocabulary (`activation` / `area` / `acquisition` / `vap`) is itself 1-level flat.

**Structure:**

```
domain      type
  eo          cems-ref
  eo          cems-fep
  eo          cems-del
  eo          cems-gra
  eo          charter-vap
  hum         shelter
  hum         health
  ...
```

### 3.3 Code Format

**Recommendation:** Lowercase hyphenated slugs in the format `{domain}-{type}`.

**Design principles:**

- Two segments for simple types; three segments when disambiguation requires a sub-group (e.g., `eo-cems-del` vs `eo-unosat-del`)
- All lowercase, ASCII, hyphen-separated — consistent with EM-DAT codes (`nat-hyd-flo-fla`) and IFRC GO conventions
- No numeric suffixes unless truly needed (prefer descriptive slugs)
- EO types use source-prefixed sub-group (`cems`, `charter`, `unosat`) since the same logical product type exists across sources
- Avoid redundancy with fields already covered by `disaster:` — e.g., do not encode `disaster:activation_status` into the type code

**Domain codes:**

| Domain | Prefix | Covers |
| --- | --- | --- |
| Earth Observation | `eo` | Satellite-derived products (CEMS, Charter, UNOSAT) |
| Humanitarian | `hum` | Cluster-based operational response |
| Financial | `fin` | Appeals, funds, assessment budgets |

### 3.4 Scope Boundary

The following rule governs what belongs in Response vs. Impact:

| Construct | Definition | Examples |
| --- | --- | --- |
| **Response** | An action taken or product produced in response to a disaster | CEMS Grading map, DREF operation, IFRC shelter distribution |
| **Impact** | An estimated effect on people, assets, or the environment | 1000 people displaced, 500 buildings destroyed, CHF 2M economic loss |

A CEMS Grading Product is a **Response** item. The damage statistics it contains may inform **Impact** items, which are separate STAC items linked via `monty:corr_id`.

---

## 4. Proposed Response Type Codes

> **Status:** Proposals for team review. Not yet final.

### 4.1 EO Response Products

EO response products are the primary use case for this contract. Codes use the `eo-{source}-{type}` pattern to preserve the product source in the code itself (since the same logical type — e.g., "delineation" — exists across CEMS, Charter, and UNOSAT with different semantics and metadata).

#### 4.1.1 CEMS Rapid Mapping

Directly derived from CEMS published 3-letter codes (REF, FEP, DEL, GRA, SR).

| Code | Name | Description | Monitoring variant |
| --- | --- | --- | --- |
| `eo-cems-ref` | CEMS Reference Product | Pre-event baseline mapping of territory and assets | — |
| `eo-cems-fep` | CEMS First Estimate Product | Fast, rough post-event affected area assessment (~hours) | — |
| `eo-cems-del` | CEMS Delineation Product | Event impact extent and affected area | `eo-cems-del-mon` |
| `eo-cems-gra` | CEMS Grading Product | Damage grade, spatial distribution and extent | `eo-cems-gra-mon` |
| `eo-cems-sr` | CEMS Situational Report | Online report with event overview; updated throughout activation | — |

#### 4.1.2 International Charter

Product types aligned with CEMS where possible. The Charter does not publish formal product codes, so the codes below are Monty-assigned.

| Code | Name | Description | CEMS crosswalk |
| --- | --- | --- | --- |
| `eo-charter-act` | Charter Activation | Formal activation record with event metadata | — |
| `eo-charter-ref` | Charter Reference Map | Pre-event baseline map | `eo-cems-ref` |
| `eo-charter-del` | Charter Delineation Map | Affected area extent map | `eo-cems-del` |
| `eo-charter-gra` | Charter Grading Map | Damage intensity map | `eo-cems-gra` |
| `eo-charter-vap` | Charter Value-Added Product | Derived analysis (population exposure, sectoral damage) | — |

#### 4.1.3 UNOSAT Rapid Mapping

UNOSAT's phase-based structure mapped to Monty product types.

| Code | Name | Description | UNOSAT phase | CEMS crosswalk |
| --- | --- | --- | --- | --- |
| `eo-unosat-psa` | UNOSAT Preliminary Situation Awareness | Early flood/damage extent (~24h) | Phase 1 | `eo-cems-fep` |
| `eo-unosat-dam` | UNOSAT Damage Assessment | Damage density, sectoral damage (shelter/agriculture/health) | Phase 2 | `eo-cems-gra` |
| `eo-unosat-pop` | UNOSAT Population Exposure | Population in affected area analysis | Phase 2 | — |
| `eo-unosat-mon` | UNOSAT Flood Monitoring | Ongoing monitoring, cumulative flood extent | Phase 3 | `eo-cems-del-mon` |

### 4.2 Humanitarian Response (Placeholder Groups)

Humanitarian response types are placeholders for future issues (outside this contract scope). Codes follow the `hum-{cluster}` pattern aligned with IASC cluster names and IFRC EPoA sectors.

| Code | Name | IASC Cluster | IFRC EPoA Sector |
| --- | --- | --- | --- |
| `hum-shelter` | Shelter and NFI | Shelter / NFI | Shelter and settlements |
| `hum-health` | Health Response | Health | Health |
| `hum-wash` | WASH | WASH | WASH |
| `hum-food` | Food Security and Livelihoods | Food Security | Livelihoods and basic needs |
| `hum-nutrition` | Nutrition | Nutrition | — |
| `hum-protection` | Protection | Protection | PGI |
| `hum-education` | Education in Emergencies | Education | Education in Emergencies |
| `hum-cccm` | Camp Coordination and Management | CCCM | — |
| `hum-early-recovery` | Early Recovery | Early Recovery | Early Recovery |
| `hum-logistics` | Logistics and Coordination | Logistics | — |
| `hum-telecom` | Emergency Telecommunications | ETC | — |
| `hum-drr` | Disaster Risk Reduction | — | DRR |

### 4.3 Financial Response (Placeholder)

| Code | Name | Description |
| --- | --- | --- |
| `fin-dref` | IFRC DREF Operation | IFRC Disaster Response Emergency Fund allocation |
| `fin-ea` | IFRC Emergency Appeal | IFRC Emergency Appeal operation |
| `fin-aa` | IFRC Anticipatory Action | IFRC Anticipatory Action allocation (pre-crisis) |
| `fin-pdna` | PDNA Assessment | Post-Disaster Needs Assessment (WB/EU/UN) |

---

## 5. Open Questions and Next Steps

### 5.1 Open Questions

1. **`disaster:` extension adoption**: Should Monty Charter Response items declare the Terradue `disaster:` extension (`https://terradue.github.io/stac-extensions-disaster/v1.1.0/schema.json`) alongside `monty:`? This would reuse `disaster:class`, `disaster:activation_id`, `disaster:activation_status`, and `disaster:resolution_class` without duplicating them in `response_detail`. The extension is currently a Proposal and has the same owners — coordination is feasible.

2. **`disaster:class` vs. `monty:response_type`**: The `disaster:class` vocabulary (`activation` / `area` / `acquisition` / `vap`) classifies *what kind of Charter object* this item is, not what kind of *response action* it represents. A `vap` is always a response product, but `monty:response_type` (`eo-charter-del`, `eo-charter-gra`, etc.) carries the semantic meaning for querying. Both are needed; they are complementary, not redundant.

3. **Monitoring variants**: Should `eo-cems-del-mon` be a separate type code or a property on `eo-cems-del` items? The CEMS API already models this as `monitoring: boolean` + `monitoringNumber: integer` — replicating these as `response_detail` properties (avoiding code proliferation) is more consistent with how CEMS itself represents this.

4. **Charter activation record modelling**: Is a Charter activation (`disaster:class = activation`) a Monty Response item or a Monty Event? An activation bundles multiple VAP deliveries — it may be better modelled as a Collection or Event rather than a single Response item.

5. **UNOSAT vs. CEMS code collapse**: Should UNOSAT codes (`eo-unosat-psa`, `eo-unosat-dam`, etc.) be kept separate or collapsed into CEMS codes with a source field in `response_detail`? Separate codes make queries like "all delineation products" harder; a source field plus shared type codes makes them easier. Decision depends on whether UNOSAT and CEMS delineations are semantically equivalent enough to share a code.

6. **CEMS STAC extension gap**: CEMS currently has no STAC extension — only a REST API. SW1.1 may include drafting a `cems:` STAC extension (or a Monty CEMS profile) to express CEMS activation and product metadata as STAC fields. Should this be a separate extension repository (like `disaster:`) or part of the Monty extension?

7. **Humanitarian code granularity**: The `hum-*` placeholders are coarse (cluster level). Should Protection sub-types (GBV, Child Protection, Mine Action, HLP) be first-class codes now or deferred?

8. **Sendai crosswalk fields**: Should response items carry an optional field indicating which Sendai target(s) the response contributes to? This would enable monitoring/reporting use cases without encoding Sendai into the taxonomy itself.

### 5.2 Next Steps

- [ ] Team review of the proposed taxonomy structure and code format (§3)
- [ ] Team review of EO product codes (§4.1) — validate against Charter Mapper metadata and CEMS API field names
- [ ] Decide on open questions 1–4 before finalising EO codes (these directly unblock SW1.1 and SW1.2)
- [ ] Determine whether to propose updates to the `disaster:` extension or adopt it as-is for Charter items
- [ ] Prototype a `response_detail` object schema analogous to `hazard_detail` and `impact_detail`, incorporating reusable fields from `disaster:` and CEMS API
- [ ] Draft example STAC items for a CEMS activation (one per product type: REF, FEP, DEL, GRA, SR)
- [ ] Draft example STAC items for a Charter activation (activation record + VAP)
- [ ] Integrate response taxonomy into the main `taxonomy.md` once codes are finalised
- [ ] Publish as v1.0 of this document at D1.1 (KO+4m, July 2026)

---

*Document history:*
*v0.1 — 2026-04-16 — Initial framework survey and structural proposal (Emmanuel Mathot)*
*v0.2 — 2026-04-16 — Added STAC extensions survey (§2.9); updated crosswalk and taxonomy recommendation to incorporate `disaster:` extension reuse strategy (Emmanuel Mathot)*
