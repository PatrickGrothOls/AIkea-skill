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
the panel, actually remove material and remain clear of prior operations. Multiple
holes form one local operation whose complete dimensions and frame are retained
in the source fingerprint. The cut record stores that frame separately from its
surface-local cutter, preserving the same placement convention as paired joints.

When a mounting interface uses an existing System 32 hole, reference and verify
that hole in the component's mounting evidence. Emit drilling only for missing
holes. Do not add a duplicate overlapping operation or enlarge an old hole to
make a new hardware profile appear compatible. An incompatible interface remains
an explicit requirement until the appropriate operation is available.

The hardware configurator owns product selection, fixing dimensions, mounting
participants and applicable motion/clearance checks. The shared drilling tool
does not infer a screw, material pilot size or hardware purchase from a hole.
