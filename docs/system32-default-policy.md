# System 32 cabinet default

## Scope
Make Patrick's full-height System 32 choice explicit across standard and custom
cabinet design skills. Keep the shared machining executor role-independent.

## Current state
The skill contract is updated. The displayed Vilja geometry is unchanged: its
custom CabinetRecipe omits grid machining, and CabinetBuilder adds only five
support rows per shelf at offsets -64, -32, 0, 32 and 64 mm. This is a design
omission, not a viewer visibility bug. Installed main-branch skills are unchanged.

## Work packages
### WP1 — Find the omission
- [x] Read the actual cabinet recipe and support feature.
- [x] Identify instruction allowing custom arrangements to omit grid machining.
### WP2 — Correct the reusable default
- [x] Require the grid in both skill entrypoints and the construction contract.
- [x] Require deliberate per-panel overrides with a reason and replacement arrangement.
- [x] Cover shelf setbacks, lighting, shared partitions and sloped retained stock.
- [x] Require expected-pattern reconciliation, actual removal and inside-face checks.
- [x] Validate both skill packages and review cross-references (all local targets exist).
### WP3 — Correct and verify the Vilja model
- [ ] Add complete grid declarations and requirements to its custom recipe.
- [ ] Reconcile the recessed shelves, hinge positions, lighting and structural cuts.
- [ ] Rebuild and check expected versus actual holes, material removal and one-face machining.
- [ ] Regenerate inspection and presentation assets, then replace the current viewer.

## Audit log
1. Patrick explicitly confirmed the 32 mm hole system is a default design choice
   that may only be deliberately overridden. This authorizes the contract change.
2. Source inspection found no system_32 operation in the custom cabinet recipe.
   The shelf feature adds only short adjustment groups. Do not claim a render fix
   or a repaired model from this documentation change.
3. Retain explicit machining inputs: putting automatic role-based cuts in the
   common executor would violate the established shared-construction architecture.
   The skill must declare the grid and its requirement before building.

4. Both skill validators pass; reviewed changed guidance and verified local links.
   This checks packaging, not a new cold-start build or regenerated geometry.
