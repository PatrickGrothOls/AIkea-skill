# Shared surface pockets

## Scope and current state

Branch `feat/shared-surface-pockets`, based on `71e605b`. Add only the reusable
rounded rectangular pocket needed by the applied-frame recipe. Reuse the groove's
frame, dimension validation and entry-face checks, then the common operation
dispatch, material/cut checks and output verification. Implemented and independently reviewed locally.

## Work package and tasks

- [x] Add explicit pocket radius and common operation dispatch.
- [x] Share rectangular cutter dimensions and surface-entry validation with grooves.
- [x] Verify independent rounded-opening geometry, through and blind depths,
      changed-input detection, entry/depth/radius failures and earlier-cut clashes.
- [x] Verify groove and drilling compatibility.
- [x] Review inherited public contract scope and complete the review skill.

## Audit log

1. The existing applied-frame helper cuts a rounded rectangle directly. Reuse that
   shape as an explicit pocket operation, so its removed material is accounted for
   by the same foundation used by standard recipes and custom parts.
2. A through-opening uses the actual panel thickness; blind pockets use a smaller
   depth. Radius zero remains a geometric square opening with unresolved corner
   finishing, not a claim that a round CNC tool cuts square internal corners.
   Cutter access, hold-down, tooling and minimum remaining wall are still actual
   project/fabrication requirements; this operation invents none of those policies.

## Validation and review

52 focused tests passed across pockets, grooves, surface drilling and hole reuse;
all nine skill packages validate. Rounded pockets match independent boxes/cylinders
and analytic removed area for top/bottom entry and blind/through depth. Changed
radius, invalid radius, buried/clipped entry, excessive depth and prior-hole clashes
are rejected at the shared boundary.

The review skill's independent testing review is clean. A 40×8×6 mm pocket with
2 mm radii on a slanted triangular-panel edge matches independent geometry after
parent rotation/translation (zero symmetric difference; 1899.398223686 mm³ removed).
Both building and independently validating raw output reject a buried entry,
overlap with prior drilling, a claimed drilling-reuse allowance and absent machining.

The inherited public specification file is 152 lines. Its required independent
scope review found one coherent immutable-value/reexport contract; pocket execution
remains in its own builder. All four machining annotations agree, existing field
order/defaults are preserved and no circular dependency was added. No refactor is
needed for this slice. A shared type alias is optional future cleanup.

3. Closed this dependency after geometry, existing-operation compatibility and
   independent review passed. Migrate the applied-frame recipe next; no framed
   front or adhesive installation is declared fabrication-ready by this operation.
