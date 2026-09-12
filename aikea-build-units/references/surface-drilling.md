# Explicit surface drilling

Use `SurfaceDrillingSpec` in an assembly's `machining` when an exact hardware
adapter or verified construction requires dimensioned holes. It shares the same
execution, cut ownership and independent result checks as System 32 requests.

```python
from assemblies.specification import SurfaceDrillingSpec, IDENTITY_LOCAL_TO_PARENT
from surface_hole_pattern import SurfaceHole

request = SurfaceDrillingSpec(
    "mounting_pattern", "panel", IDENTITY_LOCAL_TO_PARENT,
    (SurfaceHole("fixing_1", 25, 25, 4, 8),),
)
```

These dimensions illustrate the contract; choose actual holes from the selected
product and material evidence. The frame is an existing `LocalToParentPlacement`
from the drilling surface into the part. Local X/Y locate the holes and positive
local Z points into the material. The depth is measured from that surface. A
hole entering the opposite face therefore needs the corresponding rotated frame;
it is not selected by a panel's label or its place in a wardrobe.

Each complete hole-entry disk must lie on a real planar face of the blank;
an internal datum that creates a sealed cavity is rejected during construction
and again when validating a raw builder result. The shared operation adds no entry
overrun. A through-hole ends at the opposite
surface; a blind hole ends at its declared depth. Every cutter must fit inside
the panel and remove material or explicitly reuse an exact existing hole. Multiple
holes form one local operation whose complete dimensions and frame are retained
in the source fingerprint. Individual holes within a pattern must not overlap
or duplicate one another; a slot or merged opening needs an appropriate separate
operation. The cut record stores that frame separately from its
surface-local cutter, preserving the same placement convention as paired joints.

When a mounting interface uses existing holes, set `reuse_machining_ids` on its
`SurfaceDrillingSpec` to the earlier local operations providing them, for example
`("side_grid",)`. Keep the complete mounting pattern in `holes`. Construction
and independent output validation verify the same part, earlier execution and
exact whole-hole geometry, including depth and diameter. New holes remove new
material; matching holes retain both operation records without double removal.
Missing sources, shifted or partially overlapping holes, different depths and
unused reuse references fail. Other overlaps remain errors. This also applies to
a mounting pattern made entirely from existing holes. Product compatibility and
installed mounting evidence are still the component's responsibility.

The hardware configurator owns product selection, fixing dimensions, mounting
participants and applicable motion/clearance checks. The shared drilling tool
does not infer a screw, material pilot size or hardware purchase from a hole.

For a removable component applied after the base build, use
`PanelMachiningFeature().apply(built_assembly, machining, requirements)` with the
same explicit requests. It cuts the current parts using the shared applicator,
preserves prior geometry and ownership, and validates the complete result. Build
again from the base with only the retained features to remove a component; do
not try to fill old cuts back in. If the parent's requirements are still
unassessed, adding a feature retains that unresolved state.

## Drilling through contacting layers

`LayeredSurfaceDrilling().build(id, parts, surface_to_owner, holes)` emits ordinary
`SurfaceDrillingSpec` requests for explicit panels whose broad faces are parallel
to the drilling datum. It splits each depth at actual material boundaries and
rejects gaps, overlaps, over-depth and clipped circular sections. Apply its result
through `PanelMachiningFeature` so earlier openings and machining remain checked.
Each part keeps its own local solid, cuts, material and inventory identity. A
partial hole crossing an edge between neighboring pieces is outside this recipe.
This is drilling geometry, not adhesive or screw-engagement approval.
