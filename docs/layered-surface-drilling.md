# Drilling across physical panel layers

## Scope and current state

This component dependency resolves one dimensioned surface pattern into normal
part-local drilling requests. It keeps every piece independent in construction
and inventory. Branch `feat/layered-surface-drilling`, based on `fe3d76d`. Implementation,
focused verification and independent review are complete.

## Work package and tasks

- [x] Resolve a shared datum into parallel physical panel broad faces.
- [x] Split depths at real part boundaries; require continuous material.
- [x] Reuse surface drilling and common material/earlier-cut validation.
- [x] Verify independent cutter parity, frames, reversed entry, gaps and openings.
- [x] Complete review skill and close findings.

## Audit log

1. A hinge cup can cross backing and frame layers. Reuse this as a construction
   recipe for any dimensioned hole pattern across contacting parallel panels;
   neither duplicate hinge tooling nor create a combined physical sheet.
2. Restrict this recipe to parallel broad faces with a complete cylindrical
   section in each participating piece. Edge-spanning bores, nonparallel entries,
   unsupported depths and physical gaps require another qualified operation.
   Adhesive, screw engagement and material/load suitability remain unresolved.

## Validation and review

33 focused tests passed in 286.77 seconds across layer drilling, framed geometry,
hinge construction and surface drilling. Ten skill packages validate. All new code
is below 150 lines, with drilling splitting separate from execution and evidence.

The review skill's independent testing specialist found no issues. Three 4/9/5 mm
layers with mixed rotated/reversed local frames, a rotated/translated owner and
shuffled part order matched independent full-depth cylinders for holes stopping at
3/11/18 mm, from both directions (zero symmetric difference in every part).
Common output validation passed. Empty/duplicate participants, missing material,
over-depth, clipped circles, buried entry and nonparallel faces reject. A prior
opening in the middle layer rejects when the common machining feature applies it.
Evidence: `/private/tmp/layered-drilling-review-mzp1v6a9`.
