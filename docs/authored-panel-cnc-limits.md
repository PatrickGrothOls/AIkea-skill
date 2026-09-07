# Enforce CNC limits in authored furniture

## Scope

Patrick requires every panel to stay at or below 2490 mm for the 2500 mm CNC.
Preserve the complete wardrobe envelope by splitting oversized panels into real
supported, joined components. Apply the same check to future authored designs.

## Current state

The authored route previously checked only room-envelope fit and solid overlaps.
It omitted the existing CNC tools, and the supplied CNC profile subtracted only
one cutter radius, permitting 2496 mm. The original wardrobe contains six
oversized panels: four at 3940 mm and two at approximately 2618.67 mm.

All 33 focused CNC, segmentation, authored geometry and base tests pass. The old
wardrobe now exits 2, lists all six oversized parts and produces no GLB at its
new diagnostic output path. Evidence is saved in
`/private/tmp/aikea-cnc-limit-evidence/rejected-original.geometry-check.json`.
The revised closed design passes with 113 parts and a longest blank of 1994 mm.
Its 98-part interior view also passes. Six lap pairs reproduce their original
panel volumes without gaps/overlap, with 9 mm retained halves in the 18 mm panels
and 3.25 mm in the 6.5 mm back. The corrected whole model was inspected in a fresh
viewer on port 8776; its screenshot is saved in the revised project's reviews.

## Work packages

- [x] Identify omitted CNC validation and inspect the existing profile/planner.
- [x] Correct the supplied profile to 2490 × 1990 mm usable blank dimensions.
- [x] Check actual local part geometry and declared blanks throughout the tree.
- [x] Route the design skill to existing segmentation and construction guidance.
- [x] Verify boundary sizes, nested/custom parts and the real original rejection.
- [x] Rebuild all six oversized wardrobe parts with actual supported joints.
- [x] Verify corrected closed/interior models, inspect and capture the result.
- [x] Review changes and make a coherent local commit.

## Audit log

1. Patrick explicitly set a hard 2490 mm panel maximum to preserve cutter space.
   The existing 8 mm tool profile now reserves a full cutter diameter plus 1 mm
   extra on each edge, giving the requested 2490 mm X and consistent 1990 mm Y.
2. Keep room fit and CNC fit as separate checks in one required build result.
   Inspect part-local solids and blank dimensions instead of assembly bounds or
   role names, so rotated/nested/custom parts cannot evade the check.
3. Preserve the previous prototype as failure evidence. Revise a separate copy
   in `/private/tmp/aikea-full-pdf-cnc-test`; the subagent owns its joins and parts.
   Shared hardware, strength and other unfinished construction gates remain open.
4. The revised prototype uses six support-aligned half-lap joints. Check actual
   blank extents including overlap material; the joined furniture remains
   3940 × 465 × 2597 mm even though its individual blanks now fit the machine.
5. Independent review found that a malformed two-value local-size tuple could
   truncate actual bounds through `zip`. Reject incomplete/non-finite/non-positive
   dimensions at the authored boundary and always compare all three actual axes.
   Regression includes a direct custom builder with a 3000 mm omitted third axis.
6. Independent reviewer reran the malformed-builder reproduction and confirmed
   its explicit rejection, with no remaining blocker in this scoped change.
   The branch remains local; the installed main-based skills are unchanged.
