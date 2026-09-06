# Full-width drawer fronts and backs

## Scope

Make the reusable AIkea drawer box use front and back panels across its complete
outside width, with the side panels captured between them.

## Workpackages and tasks

### WP1 - Construction geometry

- [x] Preserve the runner-authoritative side-panel length.
- [x] Calculate complete outside depth from the side, front, and back panels.
- [x] Resize and relocate all five drawer sheets without overlap.

### WP2 - Saved specifications and checks

- [x] Record both side-panel length and complete outside depth.
- [x] Make cabinet and review bounds check the complete drawer depth.
- [x] Run focused geometry and generator verification.

### WP3 - Visual approval

- [x] Rebuild the existing three-drawer cabinet.
- [x] Capture the revised drawer construction for the maintainer's approval.

### WP4 - Cabinet-front placement

- [x] Trace the drawer, runner, and cabinet-front coordinate relationship.
- [x] Remove the accidental panel-thickness setback from the drawer origin.
- [ ] Regenerate the cabinet for the maintainer's visual approval.
- [x] Update the focused regression expectations for the corrected front frame.
- [ ] Record the maintainer's visual approval of the corrected placement.

## Current state

The reusable drawer now uses full-width front and back panels. The traced front
coordinate exposed an unrelated 18 mm setback caused by using cabinet-panel
thickness as a position. That production calculation and its focused regression
expectations are corrected. The versioned checkpoint does not replace the maintainer's
remaining visual approval.

## Audit log

- 2026-08-31: the maintainer chose full-width front and back panels. The sides therefore
  fit between them, while the runner-defined side length remains unchanged so the
  selected hardware relationship stays authoritative.
- 2026-08-31: The existing three-drawer cabinet was rebuilt and captured after
  the physical geometry and generated layout passed their focused checks.
- 2026-08-31: the maintainer identified that the drawers did not meet the cabinet-front
  opening. The front plane is the cabinet-local zero; panel thickness does not
  define a setback. The remaining unused depth belongs behind the drawer.
- 2026-08-31: the maintainer requested that every outstanding branch change be committed
  for durable history. The corrected front placement is therefore code-checked
  and versioned before its still-required visual approval.
