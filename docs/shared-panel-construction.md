# WP2: Shared panel and operation execution

## Scope and current state

Branch `feat/shared-panel-construction`, parent `4ab87a7` (reviewed WP1).
Reuse the generic panel runtime from `5b744f4`, with the shared WP1 inputs,
explicit local machining and traceable connector purchases. Existing template
callers remain compatible; their migration is WP3.

- [x] Reuse explicit panel/placement construction and existing joint tools.
- [x] Add explicit System 32 requests and shared operation-accounting checks.
- [x] Reject unsupported requests, missing participants and misplaced cutters.
- [x] Keep modeled connection purchases from duplicating machining-derived items.
- [x] Provide an initializer, documented build command and prototype geometry report.
- [x] Complete geometry/inventory regressions and the per-WP `review` skill.

## Implementation

`PanelAssemblyBuilder` consumes `PanelAssemblySpec` for both recipe output and
authored panels. `PanelBlankBuilder` uses explicit dimensions and outlines.
`ConstructionCutValidator` checks operation IDs, ownership and returned cuts.
`PanelMachiningBuilder` resolves the first explicit operation, System 32, through
the existing grid implementation. Joint-specific rules remain in Cabineo/miter
tools. No new furniture type or engineering standard has been added.

The shared initializer installs current contracts without overwriting different
local files. The generic build/review entry was reused from the old composition
branch; it exports actual geometry and always keeps fabrication readiness false.
Shared strict dispatch is used by the panel builder; legacy generator migration
has not yet happened, so this WP does not claim both old and new entry points
already share every check.

The new `ConnectionPurchaseSpec` identifies a joint occurrence and connector or
insert inside the purchase owner. Inventory suppresses only the corresponding
implicit installation requirement, and only after a complete one-piece purchase
reconciles. Wrong, duplicate or supplier-pack claims remain unresolved. Supplier
identity/compatibility still needs the actual selected product evidence.

## Verification and review

The `review` skill's full-diff, scope and critical/informational passes completed.
The independent testing specialist found three issues, all fixed and rechecked:

- A partial receiver cut could pass per-panel coverage: now the complete Cabineo
  occurrence/participant matrix is checked; a missing second receiver cut fails.
- A local grid could clip a slanted outline: every current local cutter must be
  fully contained in remaining material; the slanted-outline regression fails as expected.
- A legacy fixture silently stopped replacing its old purchase class: its import
  match and installed legacy class are now asserted, and compatibility runs again.

The combined regression before fixes passed 73 tests and 62 subtests; after fixes,
31 affected tests passed, with the independent reviewer verifying the four precise
closure cases. The final combined run passed **75 tests and 62 subtests** on the reviewed code. Skill validation
and whitespace checks passed. All changed code remains under 150 lines.

No findings remain. Geometry output remains prototype evidence; existing
fabrication gates and actual product/strength requirements are not bypassed.

## Audit log

1. 2026-09-11 — Started WP2 after WP1's clean skill review and commit `4ab87a7`.
2. 2026-09-11 — Retained the existing paired cutters and generic tree. Explicit
   System 32 requests remove role dependence in the new path; old template
   behavior remains until WP3's compatibility proof.
3. 2026-09-11 — Added an explicit purchase-to-occurrence reference because the
   counter otherwise adds modeled connectors to the same machining-derived
   requirements. No matching by product names or CAD solids was introduced.

4. 2026-09-11 — Fixed all three review findings and added targeted regressions.
   Independent closure review reports no remaining findings.
