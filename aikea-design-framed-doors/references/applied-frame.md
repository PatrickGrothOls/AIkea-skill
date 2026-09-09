# Optional applied-frame construction

Use this helper for a flat rectangular backing with a continuous frame glued
onto its face. It also works for framed drawer fronts and fixed decorative
panels. It is one available operation, not the contract for every door style.

## Install into the active project

```sh
python <skill>/scripts/init_framed_door_design.py <project>
```

Run through the active environment (`direnv exec .` in this repository). The
initializer reuses the shared authored-assembly contracts and adds
`assemblies/framed_front_spec.py` and `assemblies/applied_frame_front.py`.
Repeated initialization preserves identical files and rejects differing files;
inspect and deliberately reconcile a local customization instead of overwriting it.
Existing `aikea.yaml` and the furniture layout are not replaced.

## Use the helper

The following values illustrate the API only. Derive all real values from the
current front and the selected stock; there are no default door dimensions.

```python
from assemblies.framed_front_spec import FrameBorders, FramedFrontSpec
from assemblies.applied_frame_front import FramedFrontBuilder

front = FramedFrontSpec(
    assembly_id="door_01",
    width_mm=520,
    height_mm=760,
    backing_thickness_mm=12,
    frame_thickness_mm=6,
    borders=FrameBorders(left_mm=60, right_mm=60, bottom_mm=75, top_mm=60),
    opening_corner_radius_mm=4,
)
child = FramedFrontBuilder(front).child(door_local_to_cabinet)
# Declare child.spec in the owning assembly and return this same built child.
```

`.build()` returns the leaf in its own local frame. The backing occupies
`Z=0..backing_thickness`; the frame occupies
`Z=backing_thickness..total_thickness`. X is width, Y is height and +Z points
towards the visible face. Use the complete leaf's existing parent placement;
do not apply a second orientation correction when exporting it.

The returned parts are `backing` and `frame`. The frame is one continuous solid,
with its opening cut through its full thickness. The saved `face_glue` joint
names both participants and has no machining cutters. `adhesive_product` is
optional source information; `strength_verified` remains false. A zero-thickness
glue interface is a nominal geometry assumption, not an adhesive specification.

Borders can differ on all four edges. A positive opening radius represents the
remaining inside corners from routing; choose it with the intended cutter.
Radius zero models square corners and needs an explicit corner-finishing method.
The helper does not invent toolpaths or make a square internal corner cuttable
with a round bit. Curved outlines, multiple openings, profiled rails or other
joinery can use a custom builder with the same `BuiltAssembly` contract.

## Check the result in its parent

Build the complete furniture using
`aikea-review-unit/scripts/build_furniture_design.py <project>`. The helper checks
the default shop's blank footprint before construction; the complete-tree check
also checks every manufactured part, placement, collision and envelope. Keep the
frame's full outside blank in cut planning, including material removed later.

For a split of an existing routed front, compare the union of both placed parts
against the original solid, and require no volume overlap and full intended glue
contact. Check the opening and any changed corner radius explicitly. Give each
piece its own cut-list row, material/thickness record and manufacturing work.

For a useful separated view, move only the frame's saved presentation placement;
reuse its actual solid. Keep the assembled leaf as the fitting reference and
move both pieces together for a hinge-open view. Keep gap and exploded-position
changes out of the physical joint specification.

## Hardware and finishing

Select material products and adhesive for the actual substrates. A 12+6 mm
combination is an example, not a strength rating or a universal 18 mm requirement.
Keep the centre's factory surface when the selected construction permits it;
plan glue removal, pressing and finishing of the perimeter seam.

Check hinge cups and screws against the actual layers and nearby frame opening.
A nominal total thickness alone does not prove adequate retained material or
screw engagement. Supply the hinge operation with a mounting surface and datum;
it places the hardware's pattern there. The owning assembly distributes the cuts
to the real backing/frame solids. The pattern does not depend on a door style or
assume the surface belongs to one slab. Tall-door flatness, weight, hinge support
and glue strength remain separate from the closed-solid review.
