# Hazard-code verification procedure

The hazard crosswalk in a source doc maps the source's own classification to Monty
hazard codes. Getting a code *wrong but syntactically valid* is the failure this
procedure prevents: `get_canonical_hazard_codes()` in `pystac-monty` preserves any
valid UNDRR-ISC 2025 code without checking it is the **right** one for the class,
so a wrong code passes canonicalisation and silently breaks the dynamic
`a_overlaps(monty:hazard_codes, …)` correlation the spec relies on. The mapping
must be correct **at the source**.

`docs/model/taxonomy.md` is canonical. Do not map from memory, from another
source's crosswalk, or from a superseded profile.

## For each source class you map

1. **Find the intended hazard in `docs/model/taxonomy.md`.** Search the
   **Complete 2025 Hazard List** and the **Cross-Classification Mapping** table for
   the phenomenon by name — not by a code you assume. Confirm the UNDRR-ISC 2025
   code's description actually matches the source class (e.g. a tropical cyclone is
   `MH0306`, not `MH0403`, which is *Blizzard*).

2. **Pick exactly one UNDRR-ISC 2025 code per Hazard item.** The schema requires
   it. For a multi-hazard source object, emit one Hazard item per code rather than
   stacking codes on one item.

3. **Add the recommended GLIDE and EM-DAT codes** from the same row of the
   Cross-Classification Mapping table. Match the convention already used by the
   documented sources (e.g. landslide → the `GH0300` chapeau, matching
   GDACS/EM-DAT/GLIDE) so cross-source `a_overlaps` stays discoverable.

4. **Prefer the chapeau code unless the source is specific.** Map to the general
   (chapeau) code when the source only gives a broad class; refine to a
   sub-type code only when the source data justifies it.

5. **Never invent or guess a code.** If no taxonomy code fits, mark the row for
   **manual review** in the doc rather than shipping a plausible-looking code. An
   unmapped class is an honest gap; a wrong code is a silent bug.

## Then let CI confirm it

`scripts/check_hazard_codes.py` (run by `npm test`) validates every
`monty:hazard_codes` value in `examples/` against the GLIDE, EM-DAT, and
UNDRR-ISC 2025 tables in `taxonomy.md`. It catches codes that resolve to nothing,
but it **cannot** catch a valid-but-wrong code — that is what steps 1–5 are for.
Add a worked example exercising each mapped class so the checker sees the codes.
