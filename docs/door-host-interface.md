# Explicit door mounting hosts

## Scope and current state

WP5c host slice on `feat/door-host-interface`, based on `2bb1737`.
Implementation, focused checks and independent review pass. One upright front and its mounting support are
identified explicitly; machining, exact hardware placement, reservations and
opening geometry use their actual frames. Standard names stay in one adapter.

## Work package and tasks

- [x] Define owned door/support references and supported upright face orientation.
- [x] Resolve dimensions, overlay and positions from actual local frames.
- [x] Retain references in saved plans, machining, purchases and feature scope.
- [x] Route preview cuts through the common machining implementation.
- [x] Verify translated, renamed and inset hosts for both hands, with actual cuts.
- [x] Verify generic closed/open review, compatibility and regeneration behavior.
- [x] Run the review skill and fix/recheck findings.

## Audit log

1. The host is a reference to existing parts, not a second assembly. Reuse the
   existing HardwarePlacement transform; no new coordinate engine is introduced.
2. This NC70 recipe supports an upright front with the back on local Z=0 and an
   upright support with an inside broad face pointing into the selected opening.
   Other orientations require a focused profile/host extension with evidence.
3. Standard shelf obstacles retain the existing adapter. Custom callers must
   supply relevant hardware/contact reservations and complete spatial checks.
4. The retained mass calculation is an estimate using the pre-existing plywood
   density. It is not material-specific load evidence or a new hardware rating.

5. Primary review identified stale plan centers as a risk when one support moves.
   The recipe now verifies current dimensions, overlay, profile and paired world
   heights before writing files. The legacy metadata fixture now describes an
   aligned pair while preserving its exact hardware ownership assertions.
6. The existing panel preview renderer no longer demands five cabinet part names.
   It renders the parts already validated at the official builder boundary using
   their declared frames; ordinary cabinet colors and locators remain unchanged.

7. The scope review identified neutral frame ownership in a drawer-specific file.
   Move the unchanged HardwarePlacement/Vector3D implementation into shared build
   tools, retain the drawer import as a compatibility re-export, and import the
   shared class in both hosts. This removes cross-component ownership coupling
   without creating a second transform engine.

8. Independent review found inset plates incorrectly claiming nodes on the front
   System 32 column. Only a plate at the actual front reference now reserves those
   nodes; all plates still reserve their physical envelopes. New cases retain real
   nearby interference while allowing a separated inset fitting at the same height.

9. Primary review found review hiding based on the entire NC70 hardware family.
   Open/removed states now affect only the saved plan's exact purchased IDs and
   door ID. A different NC70 purchase in the same owner remains visible. Overlay
   selection uses exact owned names rather than a source-CAD substring.

## Validation

- 21 focused door/host/standard alignment tests passed before the final review fixes.
- The neutral-frame move passed 15 drawer, MOVENTO and custom-door checks.
- Fourteen existing review/geometry tests and four subtests passed.
- After the inset correction, 15 custom-host/reservation tests passed. After the
  ownership correction, all ten custom-host cases passed; two additional sloped
  edge-height/count cases then passed.
- Independent review checked all four hand/support-face combinations with different
  door/support bottom origins and an inset. Plate axes and paired world heights
  matched. It verified unchanged transform code and legacy import identity.
- Independent review confirmed an authored builder that omits a declared panel
  still fails at the official build boundary before the general renderer runs.
- The ordinary CompleteAssemblyReviewGenerator generated closed/open/removed GLBs
  for both custom hands using the three checksum-verified registered Riex STEP files.
  Each build has two panels, six operation records, three hinges and three plates;
  generic closed/open views contain eight items and removed views retain one support.
  Evidence is in `/private/tmp/aikea-door-host-source-proof-20260912`, including
  `generic-review-result.json` and checksum-bound review reports. This was run on
  this candidate source; it is not a historical frozen project or substituted CAD.
- All nine skill packages and links validate. `git diff --check` passes. Review
  findings and the [scope improvement](reviews/door-host-interface-scope.md) are
  fixed and independently rechecked; no findings remain open.

The software flow supports rectangular and sloped slab fronts. Multi-part framed
front attachment, full parent opening sweep/clearance, pilot/screw suitability and
material-specific load evidence remain distinct applicable checks. The exact-CAD
exports prove delivery and placements; they are not workshop or strength approval.
