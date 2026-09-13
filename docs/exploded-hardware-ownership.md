# Mounted hardware in hierarchical exploded views

## Scope

The user requires hardware to remain with the physical part carrying it while
exploding the complete dresser. Drawer-side members and locking clips must stay
with the drawer too. Individual fittings separate only during deeper inspection
of their drawer or mounting panel. This is a shared viewing rule, not a change
to furniture geometry, fixing holes, source CAD, or manufacturing approval.

Branch `fix/exploded-hardware-ownership` is stacked on the completed fresh-run
record `01acb3f`. Refreshed `origin/main`, confirmed ancestry and created an
isolated worktree with the existing virtual environment.

## Current state

Implemented and verified on the complete 99-piece fresh dresser. All 16 runner
units follow their real supports; all 16 locking clips stay with their drawer's
rail. The full dresser keeps drawers together, drawer inspection separates its
panels, and selecting the rail separates its two clips while retaining the rail.
The live packaged viewer was checked at all three levels and reset to all 99
pieces. Actual screenshots are saved under `local-evidence/`.

Existing source runner units remain intact. The shared contract supports an
independently represented drawer-side runner member, tested with a separate
fixture; this dresser's source CAD does not gain an invented moving-member split.
Source fit, articulated travel and previous fabrication gaps remain unresolved.

## Work packages

### WP1 — Carry physical ownership into the review

- [x] Inspect the active complete dresser and shared exporter/viewer.
- [x] Add optional explicit mounting-panel ownership to purchased components.
- [x] Populate the known MOVENTO support/clip-rail relationships.
- [x] Export structured inspection paths without changing physical identities.
- [x] Verify mounting metadata, compatibility and geometry preservation.

### WP2 — Respect the selected explosion level

- [x] Group mounted fittings with their carrier at higher inspection levels.
- [x] Include the carrier itself when focusing its panel and separating fittings.
- [x] Preserve existing child grouping, hidden parts and exact reset.
- [x] Add regressions for fixed and drawer-mounted members, repeated drawers,
  one-panel focus and GLTF surface primitives.
- [x] Update the review skill's inspection instructions.

### WP3 — Show the corrected dresser

- [x] Export the full fresh dresser through the shared path.
- [x] Check the whole dresser, drawer and mounted-panel inspection levels.
- [x] Save actual screenshots for mobile and preserve the live viewer.
- [x] Review the work package, update this record and commit the coherent fix.

## Verification and evidence

- WP1: 26 focused Python checks passed across metadata, MOVENTO installation,
  complete-tree review, native placement, doors and existing spacer ownership.
  After the saved-contract compatibility fix, all 5 metadata checks passed again.
- WP2: all 41 viewer tests passed. The production bundle was rebuilt after the
  final path-codec change. Skill-package validation passed for all 11 skills.
- Independent review applied the installed review skill/checklist to both work
  packages. It found two compatibility gaps: older saved hardware specs without
  the new field and valid IDs containing double underscores. Both were fixed
  and independently rechecked; no findings remain. Report:
  `local-evidence/attachment-review.md`.
- WP3: `actual-dresser-attachment-proof.json` records all 99 parts, 16 runner
  attachments, 16 clip attachments and exact transform reset. Whole-model
  separation was checked at 25% and 65%; drawer and rail focus were also checked
  through the real GLTF loader and production presentation class.
- The new CAD export preserves all item names and placements. Bounds differ by
  at most 4.5e-16 mm; three rounded fronts were tessellated with different vertex
  counts. Separate CAD exports are therefore not claimed to be byte-identical.
  The annotation-only test proves that adding inspection metadata preserves
  binary geometry bytes, node names and transforms exactly.
- Live packaged viewer verified 99 pieces in the dresser, 9 in the selected
  drawer, 3 in its clip rail, and 99 again after Restore assembly. Screenshots:
  `dresser-exploded-attached.png`, `drawer-exploded-attached.png`, and
  `clip-rail-exploded.png` under `local-evidence/`.
- All touched authored code files remain below 150 lines; largest is
  `PlywoodSurface.js` at 143. Diff review found no unrelated changes.

## Follow-up — exact Cabineo and runner-recess calculation

The user's visual check prompted a direct calculation of the existing geometry
and the previously suggested shift along the rail's 64 mm front-to-back depth
(16 to 20 mm and 52 to 44 mm). The existing layout does **not**
intersect the shallow runner recess. Only the hypothetical move does.

- [x] Rebuild the unchanged `dresser_cnc_01` through the shared project loader.
- [x] Measure actual current rail-local cutters in all eight drawers.
- [x] Measure hypothetical positions 20/44 mm with the same shared Cabineo
  cutter and participant transforms, without editing the design.
- [x] Cross-check the solid intersections with an independent circle formula.
- [x] Record the distinction between cut overlap and physical hardware fit.

The 619 x 64 x 29 mm rail has four Cabineo pockets, two shallow runner recesses
and four clip pilot holes. Each cut was located in the same part-local frame and
clipped to the original wooden blank. Exact solid intersection volume and nearest
surface distance were measured against both complete drilling patterns. There
were 32 current pockets and 32 hypothetical pockets across eight rails.

| Layout | Pocket position along rail depth | Gap to runner recess | Intersection volume per pocket |
| --- | ---: | ---: | ---: |
| Current | 16 mm | 3.500074532 mm | 0 mm³ |
| Current | 52 mm | 5.500066687 mm | 0 mm³ |
| Hypothetical | 20 mm | 0 mm | 0.604837274 mm³ |
| Hypothetical | 44 mm | 0 mm | 6.600067590 mm³ |

Results repeat on both sides of all eight drawers. Clip screw pilot holes do not
overlap a Cabineo pocket in either layout. Their minimum pocket-to-hole distance
is 0.602194509 mm in the current layout and 4.556522541 mm in the hypothetical
layout. These are distances between the modeled cuts, not qualification of the
wood web or the physical screw threads.

Independent check: the relevant Cabineo bore radius is 7.5 mm and its centre is
X=25.5-2*sqrt(7.5²-5²)=14.319660113 mm, Y=the connector position. The recess has
radius 6 mm, centre (14.37,33) mm and depth 0.5 mm. Its centre distance is
`d=sqrt((14.37-14.319660113)^2+(33-Y)^2)`. The signed separation is `d-13.5`.
For intersecting circles, the standard two-circle lens area multiplied by the
common 0.5 mm depth gives the overlap volume. It agrees with the actual full
Cabineo cutter intersections within 1e-8 mm³ for all 64 comparisons.

Raw results: `local-evidence/rail-cut-intersections.json`. No design dimensions,
joint positions or cuts were changed. Overlapping removal volumes are not by
themselves a collision between physical hardware or proof of joint failure.
The existing end-distance and fixing qualification questions remain separate.

## Acceptance boundary

At full-dresser separation, a mounted fitting and its host must have identical
world displacement. Drawer-side hardware must also remain in its drawer's group.
At drawer separation, mounted fittings may remain with their individual panel;
selecting that panel explicitly can reveal separate fittings. Restoring the
assembly must reproduce every original transform and geometry buffer exactly.
Legacy files without explicit mounting ownership retain their existing grouping;
missing source-member identity must not be guessed from proximity or product names.

## Audit log

- 2026-09-13 — User clarified both sides of the attachment rule, including the
  drawer-side hardware. This authorizes the ownership-aware viewer change and
  a new full-dresser screenshot. Existing fabrication gaps remain unchanged.
- 2026-09-13 — Selected a small optional mounting-part reference in the shared
  hardware contract and structured GLB inspection paths. This reuses known
  installation inputs, keeps physical/source IDs intact and avoids dresser-only
  naming rules or guessed spatial attachment. Existing complete runner source
  bodies remain complete; only independently represented members receive their
  own physical mounting owner.
- 2026-09-13 — Independent review reproduced two compatibility failures. Kept
  older project-owned contracts working at the export boundary and encoded path
  segments separately from their display labels. Added focused regressions and
  rebuilt the packaged viewer after both fixes.
- 2026-09-13 — Verified actual dresser attachments, panel-level detachment and
  exact reset; captured the full dresser, drawer underside and separated clip
  rail. This completes the requested viewing change locally without changing
  furniture dimensions, drilling geometry or manufacturing approval.
- 2026-09-13 — At the user's request, calculated actual rail cut intersections
  across all eight drawers and cross-checked them analytically. Confirmed the
  current 16/52 layout has no runner-recess or clip-pilot overlap. The suggested
  20/44 move alone creates shallow overlap. This corrects the earlier ambiguous
  wording; it does not change the design or establish physical hardware fit.
- 2026-09-13 — Clarified the ambiguous word "inward": the hypothetical movement
  is along the rail's 64 mm front-to-back depth toward its midpoint, not a change
  in cut depth or a move across the drawer width. No movement was applied.
