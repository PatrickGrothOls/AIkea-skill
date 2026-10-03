# Optional applied-frame recipe

Use a rectangular backing with a continuous applied frame when that is the
selected construction. A slab, routed front or separate rails and stiles can use
the same shared construction tools without adopting this recipe.

Run `python <skill>/scripts/init_framed_door_design.py <project>` in the active
environment. It installs the shared project contracts plus `framed_front_spec.py`
and `applied_frame_front.py`. Identical files are retained; changed local files
raise a conflict instead of being overwritten.

```python
from assemblies.framed_front_spec import FrameBorders, FramedFrontSpec
from assemblies.applied_frame_front import FramedFrontBuilder

front = FramedFrontSpec(
    assembly_id="door_01", width_mm=520, height_mm=760,
    backing_thickness_mm=12, frame_thickness_mm=6,
    borders=FrameBorders(60, 60, 75, 60), opening_corner_radius_mm=4,
    backing_material_id="selected-backing-product",
    frame_material_id="selected-frame-product",
)
recipe = FramedFrontBuilder(front).recipe()
child = FramedFrontBuilder(front).child(door_local_to_cabinet)
# Declare child.spec in the parent and return this same built child.
```

Values illustrate the API, not stock, dimensions or material defaults. Empty
material identity remains unresolved. The backing is Z=0..backing_thickness;
the frame is Z=backing_thickness..total_thickness. X is width, Y is height and +Z
points toward the visible face. The complete leaf inherits one parent placement.

`recipe()` returns editable `PanelAssemblySpec`: two real panels, one shared
`SurfacePocketSpec` through the frame and explicit opening, attachment and parent
mounting requirements. `build()` uses `PanelAssemblyBuilder`; there is no private
cutting engine. The adhesive requirement names both pieces, records an optional
product choice and stays unresolved. No zero-cut machining or glue strength is
invented. Nonzero glue thickness requires an explicit revised placement.

Change the recipe with `dataclasses.replace` and rebuild through the same builder.
Each part retains its material, blank, frame and cut-list identity. Count the full
frame blank in sheet planning. Borders may differ; radius zero needs explicit
corner finishing because a round CNC cutter cannot cut square internal corners.
The configured CNC footprint is checked before building. Cutter access, hold-down,
remaining wall, adhesive compatibility and stiffness require project evidence.

Review the complete parent through the ordinary full-tree review command. For a
construction replacement, compare placed volume, contact and fitting gaps with
the approved front. Physical layers must move together. A separated presentation
is not a changed physical joint.

Hinge machining must resolve the actual mounting surface into each intersected
layer and check retained material near the opening. Nominal combined thickness
alone proves neither cup fit nor screw engagement. Use the [whole-front hinge interface](../../aikea-build-doors/references/assembly-fronts.md)
for the supported flat layered case. Do not substitute one layer as a slab.
