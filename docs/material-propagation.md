# Material propagation

## Scope

Carry saved material choices into generated manufacturing part specifications.
Use existing group defaults and preserve explicit overrides. Do not invent
supplier products, alter dimensions, or weaken fabrication checks.

## Current state

The standard wardrobe now transfers all three saved material decisions into
PartSpec. Twenty-three targeted tests pass, including generated specifications,
inventory, identity checking, material-only regeneration and protected local edits.
Authored drawers already carry separate wall/front/bottom identities; these are
kept outside the standard wardrobe group resolver. Seven existing drawer stock
input tests, 15 sheet-planning tests and all nine CAD inventory checks pass.
All 11 skill-link checks pass. Changes are committed on
`codex/material-propagation`, not merged or included in the public release.

## Work packages

### WP1: Standard panels
- [x] Trace confirmed decisions, taxonomy, generated specifications and checker.
- [x] Propagate carcass/shelf/base, door and back material choices.
- [x] Test generated specifications, inventory and identity validation.

### WP2: Preserve drawer material ownership
- [x] Inspect drawer material rendering and independent bottom selection.
- [x] Verify existing authored drawer stock tests without changing geometry.

### WP3: Documentation and review
- [x] Update skill instructions and remove the now-obsolete README limitation.
- [x] Review files exceeding 150 lines and the final diff.
- [x] Run affected tests and package validation; commit coherent changes.

## Audit log

- 2026-09-21: User explicitly asks the skill to handle material identity using
  existing defaults. Reuse saved decisions; users must not type internal IDs.
  Material names identify selected stock without asserting supplier verification.
  Product qualification and all other manufacturing checks remain independent.
- 2026-09-21: Scope review confirms material identity belongs in PartTaxonomy;
  selection mapping belongs in a small dedicated resolver. Geometry and rendering
  responsibilities remain unchanged. Both existing files remain below 150 lines.
- 2026-09-21: Drawer recipes have a separate material contract, including HDF
  bottoms. Do not assign the global door choice to drawer fronts or assume the
  carcass stock is suitable when drawer wall thickness differs. The legacy box
  planner is a geometry primitive with caller-supplied materials; its unresolved
  inputs must still fail readiness. This change fixes the standard generator's
  dropped selections and preserves authored per-part selections.
- 2026-09-21: Independent scope and diff review found an older unrecorded-source
  upgrade gap. Preserve exact pre-material source variants; file-equality checks
  continue protecting local edits. The added historical upgrade test passes.
  The mixed inventory test remains coherently scoped despite exceeding 150 lines:
  one expensive fixture validates counting, evidence rejection and sheet grouping.
- 2026-09-21: CAD inventory confirmed 37 standard panels now have material
  identities; ten legacy drawer panels remain explicitly unspecified. Eight
  inventory tests passed initially; the old thickness-only nesting assertion
  failed because it collapsed three different 18 mm stock groups. Updated it to
  check material plus thickness and reran that test with a fresh CAD build: pass.
  All 54 selected checks now pass across the targeted runs. This does not claim
  a full-suite CI run, a new public installer release or fabrication approval.
