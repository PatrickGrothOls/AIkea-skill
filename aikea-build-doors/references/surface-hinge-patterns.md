# Place a hardware pattern on a surface

Use this operation when laying out drilling or fitting hardware to a custom
construction. It requires a planar mounting datum, not a cabinet, a named door
part, a thickness or a door-style selection. A pattern can be laid out before
any receiving solid exists. Material suitability is a separate assessment.

## Pattern and placement

`aikea-build-units/scripts/surface_hole_pattern.py` provides:

- `SurfaceHole(hole_id, x_mm, y_mm, diameter_mm, depth_mm)` in millimetres.
- `SurfaceHolePattern(holes).place(surface, entry_clearance_mm=0.1)` returning
  named `PlacedSurfaceHole` values with the original specification and real
  CadQuery cutter solids.

The supplied `cq.Plane` defines the mounting datum: its origin locates the
pattern, its X/Y axes orient the hole offsets, and its normal points **into the
receiving material**. Depth is measured from that surface. Entry clearance
extends cutters outside it without increasing the specified drilling depth.
Choose a machining datum for a nonplanar part; this helper does not project
holes onto a curved face.

The existing NC70 hardware adapter exposes its cup and two fixing holes through
`aikea-build-doors/scripts/riex_nc70_cup_pattern.py`. In the active AIkea runtime:

```python
import cadquery as cq
from riex_nc70_cup_pattern import RiexNc70CupPattern

# Inputs come from the selected hardware, fasteners and saved mounting datum.
pattern = RiexNc70CupPattern(
    selected_profile,
    pilot_diameter_mm=chosen_pilot_diameter_mm,
    pilot_depth_mm=chosen_pilot_depth_mm,
).build()
surface = cq.Plane(origin=cup_centre, xDir=fixing_direction, normal=into_material)
placed_holes = pattern.place(surface)
```

For this adapter, local `(0, 0)` is the cup centre; +X points from the cup towards
the fixing line and the two fixings are symmetric along Y. Edge distance belongs
to the caller's placement decision. Pilot diameter and depth are explicit inputs:
choose them for the actual screw and substrate. A different product can construct
its own `SurfaceHolePattern` without implementing a door template or joining a
style registry. The shared primitive has no NC70-specific knowledge.

## Return machining to the receiving parts

The owning assembly places the pattern once in a shared frame and identifies
the actual receiving parts. Transform each cutter into each receiving part's
manufacturing frame using its inverse placement. Preserve machining with the
existing `PartCut`/`AssemblyCuts` contract; see
[construction tools](../../aikea-design-furniture/references/construction-tools.md).
Only parts intersected by the pattern receive material-removing cuts. Do not
trim the pattern to conceal a missing receiver or insufficient material.

The same cup can intersect a backing and a separate frame. Keep both parts and
their cuts distinct. Their combined occupied volume can help check containment,
but does not prove that a glued interface supports a screw or transfers load.
After layout, assess the cup pocket, remaining material, screw engagement, nearby
openings and the actual fastening method. Carry every leaf-owned piece with the
hinge's movement. A valid pattern alone does not establish a fitted mechanism.

## Existing complete-door workflow

`ConcealedHingeMachining` remains an adapter for the existing saved cabinet/slab
plan. It derives a datum from that plan, calls the surface operation and leaves
the cabinet-owned System 32 grid unchanged. Its historical 2.5 mm by 10 mm cup
fixing pilots are preserved, not newly certified for every material or screw.

Custom leaves use the surface operation directly and compose their receiving
parts and hardware placements. The legacy planner, `door_panel` lookup and open
review adapter are not generalized by this extraction. Exact paired cup/plate
placement, purchased CAD, motion and whole-assembly collision checks remain
necessary when the task is a complete fitted door.
