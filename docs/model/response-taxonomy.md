# Response Taxonomy

This is the canonical Monty **Response** taxonomy reference for the v1.3.0 extension. It is the Response counterpart to the hazard [Taxonomy](taxonomy.md): it defines the controlled vocabulary of **response type codes**, the rules for classifying a response, the `monty:response_detail` field reference, and the Sendai Framework crosswalk.

For the extension-layering rules (which STAC extensions a Response item declares per source system) and worked example combinations, see [Response Best Practices](response-best-practices.md). The Response vs Impact boundary is summarised in §3.3.

The framework survey that informed this taxonomy is retained as [Appendix A](#appendix-a--source-framework-survey) for background.

---

## 1. Scope

The Monty STAC extension covers Hazard, Impact, and Response constructs. A **Response** item represents an *action taken or a product produced* in response to a disaster — a CEMS Delineation map, a Charter Value-Added Product, a DREF operation — as a STAC item linked to its event and impact items via `monty:corr_id` and explicit STAC relation links.

The taxonomy is:

- **Action-oriented**: a Response item represents an action or product, not an impact estimate.
- **EO-first**: Earth Observation response products (International Charter, Copernicus EMS, UNOSAT) are the primary use case; humanitarian and financial response are modelled but secondary.
- **Source-agnostic**: codes classify *what kind of product* was produced, not *who produced it* — a delineation map is `eo-del` whether it comes from CEMS, the Charter, or UNOSAT.
- **Extensible**: structured to accommodate future response types without breaking existing codes.

The scope boundary with Impact is: **Response = action taken / product produced; Impact = estimated effect on people or assets.** A CEMS Grading Product is a Response that *informs* Impact items; it is not itself an impact. See §3.3 for the boundary rule.

---

## 2. Response Type Codes

Response type codes use a **two-level `{domain}-{type}` hierarchy**:

- All lowercase, ASCII, hyphen-separated — consistent with EM-DAT codes (`nat-hyd-flo-fla`) and IFRC GO conventions, and matched by the schema pattern `^(eo|hum|fin)-[a-z0-9]+(-[a-z0-9]+)*$`.
- The **domain** (first segment) is derivable from the code; it groups responses into Earth Observation, humanitarian, and financial.
- Codes are **source-agnostic**. Source provenance is preserved through `monty:source`, the `disaster:` extension fields (for Charter items), `derived_from` / `source-event` links, and the item `id` — not encoded in the type code.

| Domain | Prefix | Covers |
| --- | --- | --- |
| Earth Observation | `eo` | Satellite-derived products (Copernicus EMS, International Charter, UNOSAT) |
| Humanitarian | `hum` | Cluster-based operational response |
| Financial | `fin` | Appeals, funds, assessment budgets |

### 2.1 EO Response Products

EO response products are the primary use case. Codes are source-agnostic: a delineation product is `eo-del` regardless of producer.

| Code | Name | Description | CEMS equivalent | Charter mapping | UNOSAT mapping |
| --- | --- | --- | --- | --- | --- |
| `eo-dat` | Data Product | Satellite imagery dataset delivered as the response deliverable itself — typically a calibrated acquisition or a GIS-ready data download | — (raw imagery, not a CEMS product type) | Acquisition (`disaster:class = acquisition`, calibrated stage) | GIS-ready data download |
| `eo-ref` | Reference Product | Pre-event baseline mapping of territory and assets | `REF` | Reference map VAP | Phase 0 basemap |
| `eo-fep` | First Estimate Product | Fast, rough post-event extent assessment (~hours) | `FEP` | Best-effort from early VAPs | Phase 1 PSA |
| `eo-del` | Delineation Product | Affected area extent and event impact mapping | `DEL` | Delineation VAP (best effort) | Phase 2 flood extent |
| `eo-gra` | Grading Product | Damage grade, intensity and spatial distribution | `GRA` | Grading VAP (best effort) | Phase 2 damage assessment |
| `eo-pop` | Population Exposure | Population in affected area analysis | — (derived) | Population exposure VAP | Phase 2 population analysis |
| `eo-mon` | Monitoring Update | Iterative update of a previous delineation or grading product | `DEL-MON`, `GRA-MON` | — | Phase 3 flood monitoring |
| `eo-sr` | Situational Report | Event overview report updated throughout the response | `SR` | — | — |
| `eo-vap` | Value-Added Product | Generic EO product — used when the specific type cannot be determined | — | Charter VAP (fallback) | — |

> A Charter activation (`disaster:class = activation`) is **not** a Response item — it is modelled as a Monty **Event** because it bundles multiple subsequent deliveries.
>
> Both Charter **VAPs** (`disaster:class = vap`) and Charter **acquisitions** (`disaster:class = acquisition`) become Monty Response items: VAPs map to the EO product codes above (`eo-del`, `eo-gra`, `eo-vap`, …), and each delivered acquisition dataset maps to `eo-dat`. **ETL subtlety:** the Charter records an acquisition at several stages of its own processing pipeline; keep only the **last, calibrated stage** as the `eo-dat` Response item — that is the dataset responders use to derive value-added products. Earlier-stage records of the same acquisition are intermediate processing artifacts, not separate Response items. Each VAP Response item links to the calibrated acquisition it was produced from via `derived_from`.

### 2.2 Humanitarian Response

Humanitarian response codes follow the `hum-{cluster}` pattern aligned with IASC cluster names and IFRC EPoA sectors. Detailed humanitarian modelling is the subject of future work; these codes are stable for use now.

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

For humanitarian items, the specific clusters / sectors covered are carried in `monty:response_detail.sectors` (a multi-cluster operation carries several).

### 2.3 Financial Response

| Code | Name | Description |
| --- | --- | --- |
| `fin-dref` | IFRC DREF Operation | IFRC Disaster Response Emergency Fund allocation |
| `fin-ea` | IFRC Emergency Appeal | IFRC Emergency Appeal operation |
| `fin-aa` | IFRC Anticipatory Action | IFRC Anticipatory Action allocation (pre-crisis) |
| `fin-pdna` | PDNA Assessment | Post-Disaster Needs Assessment (WB/EU/UN) |

---

## 3. Classification Rules

### 3.1 Choosing a code

Classify a response as specifically as the source metadata supports, preferring a specific code over the `eo-vap` fallback.

- **Data products** (`eo-dat`) are the most basic EO response — the deliverable is the satellite imagery dataset itself, not a derived map. Each delivered dataset is a Response item (e.g., every Charter acquisition, `disaster:class = acquisition`; a UNOSAT GIS-ready download). For the Charter, mind the ETL subtlety: an acquisition is recorded at several processing stages, and only the **last, calibrated stage** is kept as the `eo-dat` Response item — that is the dataset responders use to build VAPs; earlier-stage records are intermediate artifacts, not separate Response items. Because the `eo-dat` item *is* the dataset, it carries `eo:` / `sar:` / `sat:` (and `disaster:class = acquisition` for Charter) directly, and derived VAP Response items reference it via `derived_from`.
- **CEMS products** are always classifiable — map the CEMS product type directly: `REF`→`eo-ref`, `FEP`→`eo-fep`, `DEL`→`eo-del`, `GRA`→`eo-gra`, `SR`→`eo-sr`. Monitoring iterations use the underlying product code with `response_detail.monitoring_number` set (see §4).
- **Charter VAPs**: classify by the VAP title/description where delineation or grading intent is discernible (`eo-del` / `eo-gra`); otherwise fall back to `eo-vap`. Do not force a classification the source does not support.
- **UNOSAT products**: classify by phase and product description — Phase 1 → `eo-fep`; flood extent → `eo-del`; damage density → `eo-gra`; population exposure → `eo-pop`; monitoring → `eo-mon`.
- **`eo-vap` fallback** is for EO products whose specific type cannot be determined; best-effort classification to a more specific code is always preferred.

### 3.2 Monitoring updates

Monitoring iterations are **not** separate codes per source (no `eo-cems-del-mon`). They use the underlying product type code (typically `eo-mon`, or the product's own code) with the `monty:response_detail.monitoring_number` integer set. The presence of `monitoring_number` marks the item as a monitoring update; the prior iteration it monitors SHOULD be referenced with a STAC `rel="prev"` link. This mirrors the CEMS API model (`monitoring: true`, `monitoringNumber: int`).

### 3.3 Response vs Impact boundary

| Construct | Definition | Examples |
| --- | --- | --- |
| **Response** | An action taken or product produced in response to a disaster | CEMS Grading map, DREF operation, IFRC shelter distribution |
| **Impact** | An estimated effect on people, assets, or the environment | 1000 people displaced, 500 buildings destroyed, CHF 2M economic loss |

Statistical / damage figures contained in an EO product (e.g., CEMS `affected` / `total` per thematic) are **not** part of `response_detail` — they belong to separate Monty Impact items linked via `monty:corr_id` (see the boundary rule in §3.3).

### 3.4 Extension layering

Before adding a field to `response_detail`, check whether it is already defined by another STAC extension declared on the same item (`disaster:`, `processing:`, `sar:`, `eo:`, `sat:`). If so, use that extension's field rather than duplicating it. The per-source extension combinations are specified in [Response Best Practices](response-best-practices.md) — notably that International Charter VAP items MUST declare the Terradue `disaster:` extension alongside `monty:`.

---

## 4. `monty:response_detail` field reference

`monty:response_detail` is the Monty-specific object attached to a Response item, analogous to `monty:hazard_detail` and `monty:impact_detail`. It carries the **response type code** and the minimal additional metadata not already expressed by another declared extension on the same item. `type` is the only required field.

| Field | Type | Req. | Allowed values / format | Description |
| --- | --- | --- | --- | --- |
| `type` | string | **R** | `^(eo\|hum\|fin)-[a-z0-9]+(-[a-z0-9]+)*$` (a code from §2) | Response type code from this taxonomy. The domain is derivable from the prefix. |
| `source_id` | string | O | Free string, min length 1 (e.g., `EMSR744`, `1144-1`, `FL20240926ESP`) | Native identifier of the response in the source system (CEMS activation code, Charter VAP id `{call_id}-{n}` or dataset id, UNOSAT product code, DREF operation id). |
| `status` | string | O | `planned`, `in-production`, `published`, `finished`, `no-impact`, `withdrawn` | Lifecycle status. Harmonises CEMS `statusCode` (`F`/`N`/`W`/`I`) and Charter `disaster:activation_status`. |
| `monitoring_number` | integer | O | ≥ 1 | Iteration number for monitoring updates (mirrors CEMS `monitoringNumber`). Its presence marks the item as a monitoring update; reference the prior iteration via a `rel="prev"` link. |
| `producer` | string | O | Free string / org name | Organisation that produced the response (e.g., `JRC`, `UNOSAT`, `Airbus`, `IFRC`). |
| `methodology` | string | O | `human_interpreted`, `semi_automated`, `automated`, `modelled` | Type of analysis used to produce the response. |
| `sendai_targets` | [string] | O | Subset of `["A","B","C","D","E","F","G"]`, unique | Sendai Framework targets this response contributes to (defaults in §5). |
| `sectors` | [string] | O | IASC cluster / IFRC EPoA sector slugs (e.g., `shelter`, `health`, `wash`), unique | For humanitarian (`hum-*`) items, the sectors covered. |

The object does not permit additional properties (`additionalProperties: false`).

**What does NOT belong in `response_detail`:**

- **Source landing page / product URL** — expressed as a STAC `rel: derived_from` link, not a property.
- **Spatial resolution, sensor, orbit** — for derived products, carried on linked acquisition items (`sar:` / `eo:` / `sat:`) reached via `derived_from`. Exception: `eo-dat` items carry these extensions directly because the dataset is the deliverable.
- **Charter activation/call/resolution fields** — carried by the `disaster:` extension on Charter VAP items (`disaster:activation_id`, `disaster:activation_status`, `disaster:resolution_class`, …).
- **Damage / exposure statistics** — emitted as separate Monty Impact items linked via `monty:corr_id` (see §3.3).

**Minimal example — CEMS Delineation product:**

```json
{
  "monty:response_detail": {
    "type": "eo-del",
    "source_id": "EMSR744",
    "status": "published",
    "producer": "JRC",
    "methodology": "human_interpreted",
    "sendai_targets": ["D", "G"]
  }
}
```

**Minimal example — Charter VAP (item also declares `disaster:`):**

```json
{
  "monty:response_detail": {
    "type": "eo-vap",
    "source_id": "1144-1",
    "producer": "Airbus",
    "sendai_targets": ["D", "G"]
  }
}
```

(Note the absence of resolution, status, and activation fields — those come from the `disaster:` extension on the same item.)

---

## 5. Sendai Framework Crosswalk

The Sendai Framework for Disaster Risk Reduction 2015–2030 defines 7 global targets (A–G) tracked by 38 indicators. Sendai targets are outcome metrics, not a response action taxonomy (see [Appendix A](#a2-sendai-framework-monitoring)), but annotating response items with the targets they contribute to enables policy-level aggregation. The optional `monty:response_detail.sendai_targets` array carries one or more target letter codes; the defaults below capture the primary contribution of each response type and may be overridden or supplemented per item.

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
| `eo-dat` | D, G | Data products (e.g., raw imagery) support infrastructure assessment and EO access |
| `eo-ref` | G | Provides pre-event baseline — supports EO/early warning access |
| `eo-fep` | D, G | Rapid post-event extent informs infrastructure damage response and EO data access |
| `eo-del` | D, G | Affected area delineation supports critical infrastructure damage assessment |
| `eo-gra` | C, D | Damage grade products inform economic loss (C) and infrastructure damage (D) estimates |
| `eo-pop` | B | Population exposure analysis supports reduction of affected people (B) |
| `eo-mon` | D, G | Ongoing monitoring supports infrastructure resilience tracking and EO access |
| `eo-sr` | G | Situational reports support EO data access and dissemination |
| `eo-vap` | D, G | Generic; specific targets depend on product content |

**Default crosswalk — humanitarian response:**

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

**Default crosswalk — financial response:**

| Code | Sendai targets | Rationale |
| --- | --- | --- |
| `fin-dref` | A, B, F | DREF reduces mortality and affected people; funded via international cooperation (F) |
| `fin-ea` | A, B, F | Emergency Appeals have the same profile as DREF |
| `fin-aa` | A, B, G | Anticipatory action reduces mortality and affected people; linked to early warning (G) |
| `fin-pdna` | C, D | PDNA quantifies economic loss (C) and infrastructure damage (D) |

---

## Appendix A — Source Framework Survey

This appendix retains the survey of disaster-response classification frameworks that informed the taxonomy above. It is background material; the adopted vocabulary is §2 and the classification rules are §3.

### A.1 Frameworks surveyed

| Framework | What it contributes | Codes available? | STAC extension? | Role in Monty |
| --- | --- | --- | --- | --- |
| **Copernicus EMS Rapid Mapping** | 5 product types: `REF`, `FEP`, `DEL`, `GRA`, `SR` (+ monitoring variants) — the most formally specified EO product taxonomy surveyed | Yes — stable 3-letter codes | No — REST API only | **Primary source** for the `eo` code set |
| **International Charter "Space and Major Disasters"** | Object model via Terradue `disaster:` extension (`activation` / `area` / `acquisition` / `vap`) | Object-type codes only; not product-type codes | Yes — `disaster:` (Terradue) | EO codes + `disaster:` extension reuse (see [Best Practices](response-best-practices.md)) |
| **UNOSAT Rapid Mapping** | Phase-based products (Phase 0–3), strong flood focus | No published codes | No | Crosswalk to CEMS phases; no STAC anchor |
| **IFRC EPoA / DREF** | IFRC-native humanitarian sector structure; DREF is a Monty data source | No public codes | No | Humanitarian (`hum-*`) and financial (`fin-*`) layers |
| **IASC Cluster System** | 11 global clusters — de facto international standard for humanitarian sectors | Cluster names only | No | Basis for `hum-*` cluster alignment |
| **OCHA 3W / 4W / 5W** | Operational presence data organised by cluster | Partial (HXL cluster names) | No | Reference only |
| **Sendai Framework** | 7 outcome targets (A–G), 38 indicators | Yes (indicator codes) | No | Crosswalk annotation (§5), not a code source |
| **PDNA** | Post-disaster recovery needs assessment by sector | No | No | `fin-pdna`; otherwise out of scope (v1) |

### A.2 Sendai Framework Monitoring

The Sendai Framework defines 7 global targets tracked by the Sendai Monitor. All seven targets are **outcome metrics** (what to achieve), not action categories — there is no action taxonomy in Sendai. The targets are therefore used only as crosswalk annotations on Response items (§5), not as a structuring axis of the taxonomy. Target definitions are listed in §5.

### A.3 EO product crosswalk

| Response concept | International Charter | Copernicus EMS | UNOSAT | Monty code |
| --- | --- | --- | --- | --- |
| Satellite imagery dataset | Acquisition (calibrated, `disaster:class = acquisition`) | — | GIS-ready data download | `eo-dat` |
| Pre-event reference mapping | Reference map | `REF` | Phase 0 | `eo-ref` |
| Rapid first estimate | Best-effort early VAP | `FEP` | Phase 1 (PSA) | `eo-fep` |
| Affected-area delineation | Delineation map | `DEL` | Phase 2 flood extent | `eo-del` |
| Damage intensity / grading | Grading map | `GRA` | Phase 2 damage density | `eo-gra` |
| Population exposure analysis | Value-added | — (derived) | Phase 2 population | `eo-pop` |
| Ongoing monitoring | — | `DEL-MON`, `GRA-MON` | Phase 3 monitoring | `eo-mon` |
| Situational report | — | `SR` | — | `eo-sr` |
| Generic / unclassifiable EO product | Charter VAP (fallback) | — | — | `eo-vap` |

### A.4 Relevant STAC extensions

| Extension | Relevance to Response items |
| --- | --- |
| `disaster:` ([Terradue](https://terradue.github.io/stac-extensions-disaster/v1.1.0/schema.json)) | The live data model for International Charter items; Charter VAP Response items MUST declare it alongside `monty:`. Covers `disaster:class`, `disaster:activation_id`, `disaster:activation_status`, `disaster:resolution_class`, etc. |
| `processing:` ([stac-extensions/processing](https://github.com/stac-extensions/processing)) | Processing-chain provenance for derived EO products (CEMS, UNOSAT). |
| `sar:` / `eo:` / `sat:` | Describe the **acquisition / source imagery** layer reached via `derived_from`, not the Response product item itself. The sole exception is `eo-dat`, where the delivered dataset *is* the Response item and these extensions are declared on it directly. |

The per-source extension combinations are specified in [Response Best Practices](response-best-practices.md). Neither CEMS nor UNOSAT publishes a STAC extension; their source-specific values are carried under `monty:response_detail` or on linked acquisition items.

---

*This page was promoted from a working document to the canonical Monty Response taxonomy reference with the v1.3.0 extension release. The `monty:response_detail` object is defined in [`json-schema/schema.json`](../../json-schema/schema.json).*
