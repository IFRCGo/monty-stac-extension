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

- Two segments: `{domain}-{type}` — e.g., `eo-del`, `hum-shelter`
- All lowercase, ASCII, hyphen-separated — consistent with EM-DAT codes (`nat-hyd-flo-fla`) and IFRC GO conventions
- **Source-agnostic**: codes classify *what kind of product* was produced, not *who produced it*. A delineation map is `eo-del` whether it comes from CEMS, Charter, or UNOSAT. Source provenance is preserved through `monty:source`, `disaster:activation_id`, `derived_from` links, and the item `id` — not encoded in the type code.
- **Generic fallback for unclassifiable products**: `eo-vap` serves as the fallback when the specific product type cannot be determined (e.g., Charter VAPs where the source does not distinguish delineation from grading). Best-effort classification to a more specific code is always preferred.
- Avoid redundancy with fields already covered by `disaster:` — do not encode `disaster:activation_status` or source identity into the type code

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

EO response products are the primary use case for this contract. Codes are **source-agnostic**: a delineation product is `eo-del` regardless of whether it was produced by CEMS, the International Charter, or UNOSAT. Source provenance is preserved through `monty:source`, `disaster:` extension fields, and `derived_from` / `source-event` relation links — not encoded in the type code.

**Charter activation note:** A Charter activation (`disaster:class = activation`) is not a Response item — it is more naturally modelled as a Monty **Event** linked to the initiating call, since it bundles multiple subsequent VAP deliveries. Only the VAPs themselves (`disaster:class = vap`) become Monty Response items.

| Code | Name | Description | CEMS equivalent | Charter mapping | UNOSAT mapping |
| --- | --- | --- | --- | --- | --- |
| `eo-ref` | Reference Product | Pre-event baseline mapping of territory and assets | `REF` | Reference map VAP | Phase 0 basemap |
| `eo-fep` | First Estimate Product | Fast, rough post-event extent assessment (~hours) | `FEP` | Best-effort from early VAPs | Phase 1 PSA |
| `eo-del` | Delineation Product | Affected area extent and event impact mapping | `DEL` | Delineation VAP (best effort) | Phase 2 flood extent |
| `eo-gra` | Grading Product | Damage grade, intensity and spatial distribution | `GRA` | Grading VAP (best effort) | Phase 2 damage assessment |
| `eo-pop` | Population Exposure | Population in affected area analysis | — (derived) | Population exposure VAP | Phase 2 population analysis |
| `eo-mon` | Monitoring Update | Iterative update of a previous delineation or grading product | `DEL-MON`, `GRA-MON` | — | Phase 3 flood monitoring |
| `eo-sr` | Situational Report | Event overview report updated throughout the response | `SR` | — | — |
| `eo-vap` | Value-Added Product | Generic EO product — used when specific type cannot be determined | — | Charter VAP (fallback) | — |

**Classification guidance:**

- **CEMS products**: always classifiable — use the CEMS product type code directly (`REF`→`eo-ref`, `FEP`→`eo-fep`, `DEL`→`eo-del`, `GRA`→`eo-gra`, `SR`→`eo-sr`). Monitoring updates use `eo-mon` with `response_detail.monitoring_number` to distinguish iterations.
- **Charter VAPs**: classify as specifically as the Charter Mapper metadata allows. If delineation/grading intent is discernible from the VAP title or description, use `eo-del` / `eo-gra`. If the product type cannot be determined, fall back to `eo-vap`. Do not force classification where the source does not support it.
- **UNOSAT products**: classify by phase and product description. Phase 1 → `eo-fep`; flood extent → `eo-del`; damage density → `eo-gra`; population exposure → `eo-pop`; monitoring → `eo-mon`.
- **Monitoring variants**: expressed as `eo-mon` type code with a `response_detail.monitoring_number` integer, not as separate codes per source (`eo-cems-del-mon`, etc.). This mirrors the CEMS API model (`monitoring: true`, `monitoringNumber: int`).

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

### 4.4 Sendai Framework Crosswalk

The Sendai Framework 2015–2030 defines 7 global targets (A–G) tracked by 38 indicators. Although Sendai targets are outcome metrics (not a response action taxonomy — see §2.2), they are highly valuable for monitoring and reporting: annotating response items with the targets they contribute to enables policy-level aggregation without encoding Sendai into the taxonomy itself.

**Proposed integration:** An optional `monty:sendai_targets` array field on Response items (or inside `response_detail`) carrying one or more target letter codes. The crosswalk below provides default mappings per response type code; items may override or supplement these defaults.

**Sendai targets:**

| Target | Summary |
| --- | --- |
| A | Substantially reduce global disaster mortality |
| B | Substantially reduce the number of affected people |
| C | Reduce direct disaster economic loss relative to GDP |
| D | Reduce disaster damage to critical infrastructure and services |
| E | Increase countries with national/local DRR strategies |
| F | Enhance international cooperation to developing countries |
| G | Increase availability and access to multi-hazard early warning systems and EO data |

**Default crosswalk — EO response products:**

| Code | Sendai targets | Rationale |
| --- | --- | --- |
| `eo-ref` | G | Provides pre-event baseline — supports EO/early warning access |
| `eo-fep` | D, G | Rapid post-event extent informs infrastructure damage response and EO data access |
| `eo-del` | D, G | Affected area delineation supports critical infrastructure damage assessment |
| `eo-gra` | C, D | Damage grade products directly inform economic loss (C) and infrastructure damage (D) estimates |
| `eo-pop` | B | Population exposure analysis directly supports reduction of affected people (B) |
| `eo-mon` | D, G | Ongoing monitoring supports infrastructure resilience tracking and EO access |
| `eo-sr` | G | Situational reports support EO data access and dissemination |
| `eo-vap` | D, G | Generic; specific targets depend on product content |

**Default crosswalk — Humanitarian response (placeholder):**

| Code | Sendai targets | Rationale |
| --- | --- | --- |
| `hum-shelter` | A, B | Reduces mortality (A) and people affected (B) |
| `hum-health` | A, B | Direct mortality reduction (A) |
| `hum-wash` | A, B | Reduces disease mortality and affected people |
| `hum-food` | A, B | Reduces mortality from starvation and malnutrition |
| `hum-nutrition` | A, B | Direct mortality and affected people |
| `hum-protection` | A, B | Reduces mortality and harm to affected people |
| `hum-education` | B | Supports affected populations |
| `hum-cccm` | B | Supports displaced/affected populations |
| `hum-early-recovery` | A, B, C | Addresses mortality, affected people, and economic recovery |
| `hum-logistics` | D | Supports critical infrastructure and service continuity |
| `hum-telecom` | D, G | Emergency telecom supports infrastructure (D) and early warning (G) |
| `hum-drr` | D, E | Reduces infrastructure damage (D) and contributes to DRR strategies (E) |

**Default crosswalk — Financial response (placeholder):**

| Code | Sendai targets | Rationale |
| --- | --- | --- |
| `fin-dref` | A, B, F | DREF reduces mortality and affected people; funded via international cooperation (F) |
| `fin-ea` | A, B, F | Emergency Appeals have same profile as DREF |
| `fin-aa` | A, B, G | Anticipatory action reduces mortality and affected people; linked to early warning (G) |
| `fin-pdna` | C, D | PDNA quantifies economic loss (C) and infrastructure damage (D) |

> **Note:** These defaults are a starting point — they capture the primary contribution of each response type and should be reviewed against the Sendai Monitor indicator definitions before integration into the schema.

---

## 5. Open Questions and Next Steps

### 5.1 Open Questions

**Resolved decisions:**

| # | Question | Decision |
| --- | --- | --- |
| 1 | Charter VAP best-effort classification — how reliably can `eo-del`/`eo-gra` be determined from Charter Mapper metadata? | Tracked in [developmentseed/esa-montandon#9](https://github.com/developmentseed/esa-montandon/issues/9) (Charter Data Source Analysis) |
| 2 | `eo-vap` fallback scope — Charter-only or also for novel EO product types? | Same — resolved in [developmentseed/esa-montandon#9](https://github.com/developmentseed/esa-montandon/issues/9) |
| 3 | `eo-sr` (Situational Report) — assess whether it should be modelled as a Hazard item rather than a Response item for CEMS | Needs a sub-task under [developmentseed/esa-montandon#6](https://github.com/developmentseed/esa-montandon/issues/6) (Epic: Copernicus EMS) |
| 4 | `disaster:class = vap` and `monty:response_type = eo-del` are complementary, not redundant | **Accepted** — document explicitly in `response_detail` schema |
| 5 | Should a separate `cems:` STAC extension be created? | **No** — CEMS-specific fields go in `monty:response_detail`; no separate extension |
| 6 | Protection sub-types (GBV, Child Protection, Mine Action, HLP) as first-class codes? | **Deferred** — coarse `hum-protection` code sufficient for v1 |

**Open:**

1. **Sendai Framework integration** — Sendai target annotations are considered high value for monitoring and reporting. See the design proposal in §4.4 below.

### 5.2 Next Steps

- [ ] Team review of the source-agnostic EO code set (§4.1) and classification guidance
- [ ] Charter VAP field mapping — determine which Charter Mapper API fields enable best-effort classification ([developmentseed/esa-montandon#9](https://github.com/developmentseed/esa-montandon/issues/9))
- [ ] Assess whether `eo-sr` (CEMS Situational Report) should be modelled as a Hazard item — sub-task of [developmentseed/esa-montandon#6](https://github.com/developmentseed/esa-montandon/issues/6)
- [ ] Prototype a `response_detail` object schema analogous to `hazard_detail` and `impact_detail`; include `monitoring_number`, `status`, and optionally `sendai_targets`
- [ ] Validate Sendai target crosswalk (§4.4) against the [Sendai Monitor indicator definitions](https://sendaimonitor.undrr.org/) before integrating into the schema
- [ ] Draft example STAC items for a CEMS activation (one per product type: `eo-ref`, `eo-fep`, `eo-del`, `eo-gra`, `eo-sr`)
- [ ] Draft example STAC items for a Charter activation (Event item + VAP Response item with `disaster:` + `monty:`)
- [ ] Integrate response type codes and Sendai crosswalk into the main `taxonomy.md` once finalised
- [ ] Publish as v1.0 of this document at D1.1 (KO+4m, July 2026)

---

*Document history:*
*v0.1 — 2026-04-16 — Initial framework survey and structural proposal (Emmanuel Mathot)*
*v0.2 — 2026-04-16 — Added STAC extensions survey (§2.9); updated crosswalk and taxonomy recommendation to incorporate `disaster:` extension reuse strategy (Emmanuel Mathot)*
*v0.3 — 2026-04-16 — Revised §4.1 to source-agnostic EO codes (`eo-del` not `eo-cems-del`); Charter activation mapped to Event not Response; `eo-vap` fallback for unclassifiable Charter VAPs; open questions updated to reflect resolved decisions (Emmanuel Mathot)*
*v0.4 — 2026-04-16 — Closed open questions 1–6 with explicit decisions and issue cross-references; added §4.4 Sendai Framework crosswalk with default target mappings per response type code (Emmanuel Mathot)*
