# Native shape placement in review

## Scope and current state

Branch `fix/review-native-placement` makes placed-geometry reporting and checking
compose the shape's native location with its assembly frame, matching the exported
model. Implementation, focused regression and independent review are complete.

## Work package and tasks

- [x] Reproduce the open-door report versus raw GLB vertex discrepancy.
- [x] Verify the intrinsic location already exists before the exporter runs.
- [x] Compose native and parent locations in the shared MockupPart placed shape.
- [x] Verify analytic translated/rotated parents, fit/collision and the real door.
- [x] Review the slice using the review skill before checkpointing.

## Audit log

1. The fresh-model standard trial's open door appears upright in the actual GLB
   (82–1488 mm Z), but its report puts that 1406 mm span in Y. Independent raw
   vertex decoding and a before/after-export probe isolate replacement of the
   existing native location by `located`, not an exporter mutation.
2. Preserve the existing GLB and compose through `moved` for placed geometry.
   This changes no declared design dimensions or parent frames. Cutter placement
   semantics are a separate concern and are unchanged in this bounded fix.
3. The independently reproduced hinge Boolean inconsistency also occurs on
   identity-located source shapes; it is a separate subsequent slice.


## Validation

Twenty-six focused tests passed, including translated/rotated native frames,
placed-volume collision checks, review reports and existing door-host behavior.
Independent review found no issues. A fresh copied real prototype exports 20
parts; raw GLB positions plus node transforms match the corrected report within
0.00001914 mm, with the open door's Z range at 82–1488 mm. All 20 before/after
vertex arrays are unchanged (maximum delta 0 mm), and source geometry/location
are not mutated. The fix changes the report/check placement, not the design or
the already correct visual model. Diff whitespace checks pass.
