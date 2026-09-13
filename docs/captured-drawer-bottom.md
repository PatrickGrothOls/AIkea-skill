# Captured drawer bottom

## Scope and current state

Correct the inspected eight-drawer dresser through the shared MOVENTO recipe.
The user requires a bottom captured in recesses in the four walls, retained when
the walls are joined. Corner Cabineos remain flush to their joining edges and
accessible above the floor. Preserve the exact runners/clips and one broad CNC
face per panel. Implemented, independently reviewed and shown in the live viewer.
All eight floors pass capture/clearance checks; all 59 panels have a compatible
chosen CNC face. The follow-up material-removal audit also passes for all 59
CNC panels, with six new focused tests and an independent review. This remains an inspection candidate: the full report correctly
retains source, stock, fit/load, finishing and fabrication qualifications.

Branch `codex/captured-drawer-bottom` starts at `2ad43cc`; refreshed main is an
ancestor. Preserve the earlier project and evidence; rebuild a local copy.

The user's 6 mm HDF choice is applied to all eight bottoms and shown in a new
live inspection model. The 35 focused tests, all 59-panel capture/setup and
material-removal checks, stock inventory assertion and skill-package validation
pass. Independent review found no issues. Exact HDF product, load, stock fit and
existing hardware/finishing/CAM qualifications remain open.

## Work packages

### WP1 — Shared captured construction

- [x] Replace bottom-to-wall Cabineos with four actual retaining grooves.
- [x] Keep wall pockets above the floor; prove no intersections/access blockage.
- [x] Retain clip mounting plane with a lower support; keep rear hook axes.
- [x] Verify actual solid fit, retained material and one machining face.
- [x] Review the change with the review skill and independent reviewer.

### WP2 — Complete dresser proof

- [x] Rebuild the same eight drawers in a copied project with current shared code.
- [x] Reconcile parts, connector pairs, purchased runners and clips.
- [x] Check the full tree and show actual assembled/exploded drawer screenshots.
- [x] Update skill guidance and record remaining fabrication qualifications.
- [x] Review the final diff and commit a coherent local checkpoint.

### WP3 — Complete material-removal proof (2026-09-13 follow-up)

- [x] Add independent blank-versus-finished checks for every drawer panel,
  rebuilding expected cuts from declarations and comparing both volume and shape.
- [x] Add analytic groove/drilling volumes and negative cases for extra cuts,
  equal-volume misplaced cuts, added stock and overlapping cutters.
- [x] Run the new tests and audit the actual dresser CNC tree: six tests pass;
  all 59 CNC panels match expected removed material in volume and shape.
- [x] Review the added proof using the review skill and independent testing
  specialist: no code findings; generator/load/hardware/CAM limits retained.

### WP4 — User-selected 6 mm HDF bottoms

- [x] Save bottom thickness/material independently; retain existing caller defaults.
- [x] Apply 6 mm HDF to all eight drawers and derive 6.2 mm grooves.
- [x] Recheck capture, edge-flush Cabineos, one-face machining and removed material.
- [x] Refresh the full inspection model and review this slice using the review skill.
- [x] Record the actual results and commit the coherent local change.

## Construction candidate and qualifications

The user also questioned the lower brace and 16 mm floor. The brace is the front
locking-device screw support for the existing one-face construction, not an
independently specified anti-sag brace. The floor's 16 mm thickness was retained
from the previous candidate; Blum's 16 mm planning limit concerns the sides.
A 9 mm plywood floor was discussed as an alternative. The user then selected
6 mm HDF; actual HDF grade, load and stock fit need qualification. The choice is
HDF, not the Fibralux high-density MDF used as a price comparator.

Use a 6 mm HDF floor with 5.8 mm engagement in 6 mm deep wall grooves,
6.2 mm groove width and a 14.5 mm bottom recess (inside the saved Blum 12–15 mm
planning range). The floor grows into all four grooves. The visible structural
front has a stopped, rounded pocket; its ends extend beyond the bottom corners.
The bottom rests on the groove floors; the 0.2 mm upper/end allowances are proposed
fit clearances requiring a stock/tool coupon, not manufacturer dimensions.

The front clip support becomes 14.5 mm finished thickness below the floor; clip
mounting plane and axes stay fixed. A prepared strip can be faced from thicker
stock in the same underside setup, but stock preparation/CAM remain explicit
qualifications. Do not relabel old 29 mm stock as finished 14.5 mm material.
Rear hook bores retain their centres and diameter but become through-holes from
the inner face, so the rear groove and bores share one setup. That extension is a
construction proposal, not the source's nominal blind-hole specification.

## Audit log

- 2026-09-13 — User identified the floor covering drawer connectors and specified
  capture by all four walls. Reuse the shared construction path rather than
  changing only a displayed mesh.
- 2026-09-13 — Inspection confirmed the old bottom was joined by Cabineos and
  stopped behind a 29 mm clip support. A full floor requires lowering that support.
  A 14.5 mm recess also keeps the groove above the unchanged Ø6 rear hook axes.
  These are reviewable implementation choices for the requested correction;
  stock, pilot, source-fit and production approvals remain outstanding.
- 2026-09-13 — Independent review caught a regression above 372 mm drawer height:
  two fixed corner positions exceeded the shared maximum spacing. Extracted a
  bounded interval method from the existing Cabineo allocator and used it for
  both old layouts and the new clear region. Actual 100/400/1000 mm builds pass.
- 2026-09-13 — Twenty focused construction/allocator tests pass. Independent
  exact-source checks found no overlap between either old/new floor and each
  handed runner/clip. This does not clear their existing mating discrepancies.
- 2026-09-13 — The copied dresser's eight CNC drawers pass four-edge capture,
  zero wood overlaps and edge-flush wall pockets at least 10 mm above the floor.
  All 59 panels have a compatible broad machining face. Inventory retains 40
  purchased components and now reconciles 156 Cabineos with 156 brass inserts;
  removing the bottom joints removes 32 pairs from the previous 188.
- 2026-09-13 — Full finished geometry has 99 valid solids, no positive-volume
  overlaps or envelope violations and the same 88 uncertain source intersections.
  Its requirement check exposed an incorrect operations-coverage claim for the
  unmachined bottom. Separate joined-wall/support operations from an explicit
  captured-floor stock-fit/load qualification. Do not invent a bottom operation
  or call the captured floor loose to clear the gate. This changes evidence
  declarations only; rerun the complete check after this correction.
- 2026-09-13 — Final refresh completed: applied operations and product identities
  pass; no `panel_connections` errors remain. All eight `captured_floor_fit`
  qualifications intentionally remain open. There are 12 unresolved extension
  qualifications and 59 requirement issues across the complete candidate.
  The geometry still has no invalid solids, overlaps or envelope violations,
  and retains the same 88 uncertain manufacturer-body intersections. Exit 2 is
  the correct non-fabrication-ready result, not a failed model generation.
- 2026-09-13 — Independently reviewed the current reports and all 99 unique
  GLB inspection identities. All 16 runners and 16 locking clips resolve to
  existing physical mounting owners. The final report has no unresolved code
  finding; physical production qualifications remain explicitly separate.
- 2026-09-13 — Opened a fresh snapshot of the final GLB, inspected the drawer
  exploded and assembled, saved new screenshots and left the drawer at 65%
  separation. The earlier project/view remain preserved. Local commits:
  `427f797` shared construction and `cf3dc2f` correct requirement coverage.

- 2026-09-13 — User approved closing the complete material-removal test gap and
  asked why the lower brace and 16 mm floor are present. Add focused independent
  tests and a saved-tree audit; keep the thickness alternative a proposal.
  This is verification of CNC wood geometry, not a change to fabrication approval.

- 2026-09-13 — WP3 completed: six tests passed in 13.90 seconds; independent
  review repeated them in 19.42 seconds with no findings. All 59 saved dresser
  CNC panels pass the volume and removed-shape comparison, including all eight
  drawers and their pull holes. Overlapping cutters are unioned and clipped to
  stock; unmachined floors must retain the full blank. Expected cutters are
  rebuilt from declarations using production generators, with seven independent
  analytic groove/drilling volume checks. This does not independently validate
  every declared dimension or certify the generators, stock, load or CAM.

- 2026-09-14 — User selected "6mm hdf it is then". Apply that choice to this
  dresser while preserving saved projects that omitted separate bottom stock.
  Derive the groove from the same thickness so the thinner floor is captured;
  keep the support, hardware datums and edge-flush joints in place. Verification
  and a new inspection export are required before declaring this slice complete.

- 2026-09-14 — WP4 complete: 35 tests pass in 398.93 seconds. The saved CNC
  dresser has eight HDF bottoms at 630.6 × 485.6 × 6 mm; all 59 panels retain a
  compatible chosen face, all floors remain captured, and wall pockets stay flush
  to their edges above the floor. Inventory remains 59 wood parts, 40 hardware
  components, 156 Cabineos and 156 matching inserts. Removed material matches all
  59 declarations: maximum volume difference 2.1780579118058085e-08 mm3, with
  zero missing cuts, extra cuts or material added outside stock. An initial test
  compared fresh dataclass types across isolated project loads; it now compares
  their complete values. No physical change was needed to address that failure.
- 2026-09-14 — Final model contains 99 valid solids, no positive-volume overlaps
  or envelope violations and the same 88 unresolved source intersections, 12
  extension qualifications and 59 requirement issues. Exit 2 remains correct
  for this non-fabrication-ready inspection model. Independent review found no
  issues and 11 skill packages/links validate. Opened the new model and inspected
  left drawer 01 at 65% separation; saved an actual screenshot. The thinner
  floor retains its underside datum, providing 10 mm more internal height.

## Local evidence

- `local-evidence/regression-tests.log`: 21 passing tests after the final fix.
- `local-evidence/complete-bottom-proof.json`: complete CNC-tree face audit,
  actual eight-drawer retention/access checks and physical inventory.
- `local-evidence/project`: a copied design with a corrected prepared-support
  material label; the original project and model are unchanged.
- Skill-package validation: 11 local skills and links pass.
- All changed code files remain below 150 lines.
- `local-evidence/dresser-captured-bottom.geometry-check.json`: final combined
  report, construction hash
  `5de1279c35968061e871f18583f3505ab5ea31c86056848bc1cc16f6205a50d7`.
- `local-evidence/dresser-captured-bottom.glb`: final 99-piece inspection model;
  SHA-256 `6928c36fa2ae494b40051d9e36479bd9e7f7d3461969fb075dd4f5b649d95ef3`.
- `local-evidence/captured-bottom-review.md`: independent WP1/WP2 review.
- `local-evidence/drawer-grooves-exploded.png` and
  `local-evidence/drawer-bottom-assembled.png`: actual final-model screenshots.
- Live viewer: `http://127.0.0.1:63938/` (drawer selected through the inspection
  controls); the server retains the final immutable model snapshot.

- `local-evidence/material-removal-tests.log`: six new passing tests.
- `local-evidence/material-removal-proof.json`: every panel's expected/actual
  removed volume, missing cut, extra cut and added material, at 1e-5 mm3 tolerance.
- `local-evidence/audit_material_removal.py`: reproducible saved-CNC-tree audit.
- `local-evidence/material-removal-review.md`: core and independent review.

### 6 mm HDF evidence (current inspection candidate)

- `local-evidence/hdf-regression.log`: 35 passing tests; old 16 mm callers included.
- `local-evidence/hdf-bottom-proof.json`: all eight floors, 59 machining setups and inventory.
- `local-evidence/hdf-stock-proof.json`: eight actual HDF material/dimension records.
- `local-evidence/hdf-material-removal-proof.json`: all 59 panels match in volume and shape.
- `local-evidence/hdf-review.md`: core and independent review, no issues.
- `local-evidence/dresser-hdf-bottom.geometry-check.json`: qualifications remain explicit.
- `local-evidence/dresser-hdf-bottom.glb`: current 99-piece model.
- `local-evidence/hdf-drawer-exploded.png`: actual new-model drawer screenshot.
- Live viewer: `http://127.0.0.1:51296/`; drawer 01, 65% separation.
- Construction SHA-256: `d1170b4ff461fa50beade888630aa3d686cb171bbe37dae4cbdd15b69eedb5bd`.
- GLB SHA-256: `1ffc399da9eb230609b13c0b3d55b5399b66024dcd7932f758825aee7f35c34d`.
