# Authored assembly contract

## Start a project

Run with the active Python/CadQuery environment:

```sh
python <package>/aikea-build-units/scripts/init_furniture_design.py <project>
```

This copies the existing assembly contracts plus `panel_assembly.py`; it chooses
no furniture layout and preserves differing local files. Existing project facts
remain authoritative. Author a requirements/input file, local specifications,
and a root `assemblies/furniture_01/builder.py`. Use IDs ending `_01`, `_02`, etc.
as required by the shared loader. IDs and purpose text do not select a template.

The root module exports:

- `BUILDER`: an object whose `build()` returns the existing `BuiltAssembly` tree.
- `ENVELOPE`: a CadQuery Workplane containing the allowed solid volume in the root
  frame. Derive it from the client's envelope and exclusions. It may be stepped,
  sloped or contain obstacle cutouts; it need not be a rectangular cabinet box.

Every returned Workplane must contain one Shape. To represent several solids as
one physical item, wrap them in a `cq.Compound.makeCompound(solids)` and return
`cq.Workplane("XY").newObject([compound])`. A Workplane with multiple separate
values is rejected, because the shared exporter would otherwise take only its
first value. Use the same single-Shape contract for the envelope.

Keep input dimensions in the local specification. Rebuild from them instead of
editing exported geometry. All physical items, including bought hardware, must
appear in the root tree; a list of separate preview files is not a whole design.

## Panels and explicit machining

Use the project `PartSpec` contract:

```python
PartSpec(
    part_id="seat", role="seat",
    dimensions_mm=(("width", width), ("depth", depth), ("thickness", thickness)),
    local_to_parent=placement,
    local_size_mm=(width, depth, thickness),
)
```

The blank lies in local XY, extruded through positive Z. Any semantic role is
allowed. `outline_mm` optionally supplies polygon vertices as `BoundaryPoint(x,y)`;
here `height_mm` is simply the existing contract's name for local Y. Keep
`local_size_mm` consistent with the outline bounds. An `inside_face` such as
`>Z` is required when the chosen machining operation uses that datum.

`PanelAssemblySpec(id, purpose, parts, joints, child_assemblies, purchased_hardware)`
owns arbitrary panels and composition. It provides `.part(id)` for joint tools.
`PanelAssemblyBuilder(spec, children=(), hardware=())` resolves paired cuts and
builds actual panels. Pass built children/hardware in the exact declared order.
Use `BuiltChildAssembly(child_spec, child_builder.build())` to nest a unit.

The default joint builder implements Cabineo and equal-thickness miter. Unknown
or unresolved joints fail explicitly. Its cutters must remove material from each
participant. That check catches a misplaced receiver; it does not establish a
safe fastening design by itself.

For new operations, inject `blank_builder` (with `.build(part)` returning the
local Workplane) or `joint_builder` (with `.build(spec, joints)` returning
`AssemblyCuts` of `PartCut` values). Every declared machining joint must return
cuts for each of its participants; unknown part/joint IDs and omitted
participants are rejected. A custom builder can also implement the
existing `BuiltAssembly` contract directly. This is the extension point for
nonrectangular parts, machining and mechanisms, without editing a purpose registry.

Keep a cut's coordinate transform in `PartCut.location`. For a cutter authored
in assembly space, that is the inverse of the participant's local-to-assembly
placement. A joint spanning children must resolve both participants in a common
frame and return machining to their actual owners; do not duplicate physical
panels to make a connection appear local.

## Build and inspect the whole design

```sh
python <package>/aikea-review-unit/scripts/build_furniture_design.py <project>
python <package>/aikea-review-unit/scripts/serve_unit_review.py <project>/reviews/furniture_01.glb
```

The build command executes the authored tree, accumulates its placements, exports
real GLB geometry and saves `furniture_01.geometry-check.json`. It reports invalid
solids, volume outside the envelope and exact volumetric overlaps after a bounding
box filter. Touching faces are allowed. Invalid geometry returns exit 2; a GLB may
still be exported for diagnosis. Fix the source and rebuild.

This is a closed-geometry check. It deliberately keeps `fabrication_ready:false`:
review the requirement checklist, joint participation, hardware provenance and
ratings, retained material, assembly method, moving states and actual installed
constraints separately. Record design omissions visibly and return from any
component probe to the full root assembly before claiming completion.
