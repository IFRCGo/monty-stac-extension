# Plan: Research Response/Action Taxonomies (issue #12)

## Context

This task addresses [developmentseed/esa-montandon#12](https://github.com/developmentseed/esa-montandon/issues/12), a sub-issue of the epic [#7](https://github.com/developmentseed/esa-montandon/issues/7) — "Define and implement the Response data model in the Monty STAC extension". The work is part of the ESA contract (issue-one#39) to integrate EO-based response products (Charter Mapper, CEMS, UNOSAT) into Montandon.

The Monty STAC extension currently has Hazard and Impact fully defined, but Response is empty (only `ID_linkage`, no taxonomy, no STAC fields). Before designing the Response STAC fields, we need a grounded taxonomy. This deliverable (D1.1) is due at KO+4m (July 2026).

**Key design constraints (from Epic #7):**

- Response items will be separate STAC items linked via `monty:corr_id`
- Taxonomy must be open/extensible; EO types go in first
- Anticipatory actions are out of scope but the model must not preclude them
- Response = action taken / product produced (not the impact itself)

## Deliverable

Create `docs/model/response-taxonomy.md` in the `IFRCGo/monty-stac-extension` repository, published via PR on a new branch. This is an iterative working document — first iteration covers the framework survey and selection rationale.

## Implementation Steps

### Step 1 — Framework research (web search per framework)

Fetch and summarise each of the 7 candidate frameworks listed in issue #12:

| Framework | What to capture |
| --- | --- |
| **OCHA 3W/4W** | Activity category list used in Who-does-What-Where-When tracking |
| **Sendai Framework monitoring** | Indicator categories for response/recovery actions (Targets E/F/G) |
| **IFRC EPoA / DREF** | Standard response sectors (shelter, health, WASH, livelihoods, protection, cash, etc.) |
| **IASC Cluster system** | 11 clusters + their sub-sectors |
| **International Charter** | Activation types, product types (Reference Map, Delineation, Grading) |
| **CEMS rapid mapping** | First Estimate Product, Delineation, Grading, Reference Product |
| **PDNA framework (WB/EU/UN)** | Post-disaster needs assessment sector categories |

For each: capture category hierarchy depth, whether machine-readable codes exist, and how well it maps to the Monty use-case (EO products + humanitarian response data).

### Step 2 — Selection and crosswalk analysis

After surveying all frameworks, assess them against Monty-specific criteria:

- **Coverage**: Does it address EO products? Humanitarian sectors? Financial response?
- **Hierarchy depth**: Is it flat, 2-level, 3-level?
- **Code availability**: Are there existing stable codes we can reuse or crosswalk?
- **Adoption**: Is it actively used in data systems we ingest (CEMS, Charter, IFRC GO)?
- **Extensibility**: Can the structure accommodate future response types (anticipatory action, PDNA)?

Produce a crosswalk summary table mapping concepts across frameworks, and a shortlist of frameworks to adopt vs. reference only.

### Step 3 — Taxonomy structure recommendation

Based on the analysis, propose and justify:

- **Hierarchy**: flat list vs. group → type (2-level) vs. deeper — mirroring the hazard taxonomy if appropriate
- **Code format**: informed by which frameworks contribute codes and whether crosswalk IDs are needed
- **Scope boundary**: what counts as "Response" vs. "Impact" in Monty's model

This section will likely require iteration and review with the team before finalising codes.

### Step 4 — Proposed initial response type codes

Only after the structure is validated, propose the initial code list, prioritising:

1. EO response products (Charter, CEMS, UNOSAT) — first entries per Epic #7
2. Humanitarian placeholder groups — to be expanded in future issues

### Step 5 — Publish working document

- Branch: `feat/response-taxonomy`
- File: `docs/model/response-taxonomy.md`
- PR to `IFRCGo/monty-stac-extension` main
- Reference developmentseed/esa-montandon#12 in PR description
- Mark clearly as "working document / first iteration" — codes in Step 4 are proposals pending team review

## Document Structure

```markdown
# Response Taxonomy (Working Document — v0.1)

## 1. Purpose and Scope

## 2. Framework Survey
   ### 2.1 OCHA 3W/4W
   ### 2.2 Sendai Framework
   ### 2.3 IFRC EPoA / DREF
   ### 2.4 IASC Cluster System
   ### 2.5 International Charter
   ### 2.6 Copernicus EMS (CEMS)
   ### 2.7 PDNA Framework
   ### 2.8 Crosswalk Summary & Selection Rationale

## 3. Taxonomy Design Recommendation
   - Chosen structure + justification
   - Code format proposal (derived from analysis)
   - Scope boundary definition

## 4. Proposed Response Type Codes (EO-first)
   - EO response products
   - Humanitarian placeholder groups

## 5. Open Questions & Next Steps
```

## Critical Files

| File | Role |
| --- | --- |
| [docs/model/taxonomy.md](docs/model/taxonomy.md) | Existing hazard + impact taxonomy — format and code convention reference |
| [docs/model/README.md](docs/model/README.md) | Model overview — Response class currently empty |
| [README.md](README.md) | STAC extension spec — Response section marked "still needs to be defined" |

## Verification

1. All 7 frameworks surveyed with category lists and applicability notes
2. Crosswalk table covers all frameworks, identifying overlaps and gaps
3. Selection rationale documented (which frameworks inform the taxonomy and why)
4. Taxonomy structure recommendation justified with comparison of alternatives
5. Initial EO code proposals flow logically from the analysis (not assumed upfront)
6. Document accepted as working document in `docs/model/` and referenced from the PR
