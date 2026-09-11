# Shared surface drilling

## Scope and current state

WP5b prerequisite on `feat/shared-surface-drilling`, based on reviewed base
migration `ae595c0`. Implementation and review are complete. Reuse the previously implemented
surface-hole geometry to declare hardware drilling through the same local-operation
contract used by cabinet grids. Product-specific fixing selection stays in its
component adapter; this slice does not choose new screws or hole dimensions.

## Work package and tasks

- [x] Reuse `surface_hole_pattern.py` from `c08f1b0` with source provenance.
- [x] Add a focused typed drilling request using the existing local-to-parent frame.
- [x] Execute and independently verify the request through the common builder.
- [x] Test opposite faces, rotated frames, changed patterns, clipped holes,
  omitted cuts and duplicate/invalid hole declarations.
- [x] Document how a hardware adapter reuses this operation and existing holes.
- [x] Run the review skill, fix/recheck findings and commit the slice.

## Validation

- The first opposite-face test caught a frame reset caused by storing the frame
  in the cutter instead of `PartCut.location`. The cut now carries the frame in
  the existing explicit location field; independent cylinder comparison passes.
- 23 drilling, output-validation and construction-specification tests passed.
- 17 fresh custom CLI, extension and requirement tests passed.
- Independent review found an accepted buried drilling datum. The shared operation
  now checks the entire entry disk against actual blank faces. The builder and raw
  output validator reject the cavity; valid opposite-face and edge drilling pass.
  The 23-test drilling/output regression passed after this correction.
- Independent review reproduced the corrected buried-datum rejection and matched
  bottom, top and edge drilling to separate cylinders. No findings remained.
- All nine skill packages and reference links verified. No new purchased fixing,
  material compatibility or fabrication claim is implied by these geometry checks.

## Audit log

1. The drawer audit found successful subtractions without corresponding declared
   local operations/cuts. The shared hole-pattern implementation already exists
   on the hinge-pattern branch (`c08f1b0`), so reuse it as a narrow dependency for
   drawer, hinge and mounting-interface migrations instead of copying their cutters.
2. `SurfaceDrillingSpec` carries the existing surface-to-part frame and dimensioned
   holes. Pattern coordinates use local positive Z into the material. This follows
   the existing surface-pattern convention and introduces no new furniture policy.
