# Vilja v3 — provisional full-width wardrobe

Four 618.75 mm bays across 2475 mm; four 616.75 mm leaves, six complete drawers, thirteen shelves, two base decks and sixteen foot/plate pairs. No filler strips. The six fronts are single structural panels, centered with equal side reveals and 3 mm floor/stack/cap clearances. Neutral-white recessed lighting is included.

**Baked appearance verified:** all four geometry/coverage/export checks pass. Output SHA256 `f9968c556ea28dac14f9faebddebf6e77ac80894942c43f9f6628517114f05ad`; matching inspection SHA256 `ebd4013871b0a1376ee38ade83ee532e0d5a42b3ea753184f48e87b0c350941f`. Visual acceptance remains pending.

The six centered front and box widths are468.75 mm, with59 mm equal side reveals and46.3 mm supports.

## Review files

- Assembled baked appearance: `../../reviews/presentation-grass-v3-01/assembled.glb`.
- Matching live inspection model: `../../reviews/grass-v3-materials-packed.glb`.
- Native full assembly: `../../reviews/furniture_01-grass-closed-provisional-v3.step`.
- Actual manufactured-part solids: `manufacturing/parts/` (84 STEP files).
- Blank outlines: same directory (84 DXF files). These are **perimeters only**, not drilling drawings or CNC toolpaths.
- Draft part/inventory data: `manufacturing/part-manifest.json` and `manufacturing/item-counts.json`.
- Declared machining-face audit: `reviews/panel-setup-audit.json`.
- Unresolved declared requirements: `reviews/unresolved-requirements.json`.

## Verified scope

The corrected closed GRASS hardware has no positive overlap with the 84 machined wood parts across 59 exact candidate intersections. All 12 assembly nodes pass declared broad-face access. The baked appearance retains 743 item identities, covers all 775,824 panel triangles at tested UV centroids and stays within 0.000784 mm export rounding. Its complete source, coverage and geometry reports accompany the model.

## Remaining qualifications

This is a provisional design and draft inventory, **not fabrication-ready**. The accepted full-width leaves remain outside the chart’s 600 mm reference condition; actual finished masses and supplier/trial-fit load qualification remain open. Complete door/hinge/drawer motion is not established by a closed-position model. The inferred native hinge/plate clip overlap requires source interpretation. Fixing seating/holding, calibrated support stock, anchoring, kickboard attachments, electrical routing, connection evidence, machining tool reach and workholding remain unresolved. Selected pins, connector bodies and screws contain labelled dimensional illustrations.

Use the matching inspection model when hiding doors or exploding parts; assembled baked shadows are valid only for the assembled pose. Material products/coatings remain representative. The v3 whole-tree report is `../../reviews/grass-v3-whole-tree-position.json`:725 valid solids,zero outside-envelope or uncertain intersections. No wood/wood, runner/front, pin/wood or support-fixing/rail collision remains.275 source engagement and illustrative screw contacts remain unqualified. The complete-tree status is therefore invalid, not fabrication-approved.
