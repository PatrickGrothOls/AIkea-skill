# Captured drawer bottom

## Scope and current state

Correct the inspected eight-drawer dresser through the shared MOVENTO recipe.
The user requires a bottom captured in recesses in the four walls, retained when
the walls are joined. Corner Cabineos remain flush to their joining edges and
accessible above the floor. Preserve the exact runners/clips and one broad CNC
face per panel. Shared construction and the complete CNC-tree checks pass. The
finished full-tree source/position check and visual delivery are in progress.

Branch `codex/captured-drawer-bottom` starts at `2ad43cc`; refreshed main is an
ancestor. Preserve the earlier project and evidence; rebuild a local copy.

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
- [ ] Check the full tree and show actual assembled/exploded drawer screenshots.
- [x] Update skill guidance and record remaining fabrication qualifications.
- [ ] Review the final diff and commit a coherent local checkpoint.

## Construction candidate and qualifications

Use the existing 16 mm floor with 5.8 mm engagement in 6 mm deep wall grooves,
16.2 mm groove width and a 14.5 mm bottom recess (inside the saved Blum 12–15 mm
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

## Local evidence

- `local-evidence/regression-tests.log`: 20 passing tests.
- `local-evidence/complete-bottom-proof.json`: complete CNC-tree face audit,
  actual eight-drawer retention/access checks and physical inventory.
- `local-evidence/project`: a copied design with a corrected prepared-support
  material label; the original project and model are unchanged.
- Skill-package validation: 11 local skills and links pass.
- All changed code files remain below 150 lines.
