# Shared panel construction

Use shared construction inputs for an authored assembly or the editable output
of a component configurator. Each part has explicit local geometry and placement;
its role is a label, not a request to drill holes. Current template generation
still has a compatibility path until its configurator migration is complete.

Initialise contracts with `scripts/init_furniture_design.py <project>` using the
active CadQuery environment. Author local inputs and a root builder that returns
the existing complete `BuiltAssembly` tree. Keep project measurements authoritative.

```python
from assemblies.panel_assembly import PanelAssemblyBuilder, PanelAssemblySpec, PartMachiningSpec
from assemblies.specification import PartSpec, IDENTITY_LOCAL_TO_PARENT

board = PartSpec(
    "partition", "partition", (), IDENTITY_LOCAL_TO_PARENT,
    local_size_mm=(400, 700, 16), inside_face=">Z", material_id="mdf",
)
spec = PanelAssemblySpec(
    "component_01", "authored component", parts=(board,),
    machining=(PartMachiningSpec("shelf_grid", "partition", "system_32"),),
)
BUILDER = PanelAssemblyBuilder(spec)
```

The dimensions above demonstrate the contract; they are not project defaults.
Leaving `machining=()` produces an undrilled blank. Use explicit `CabineoJointSpec`
or a supported miter joint to join actual panels. Joint tools derive both cuts
from their participants' frames. Unknown operations, incorrect ownership and
cutters that miss a participant fail construction. The current explicit local
operation (System 32) requires each blind bore to fit completely inside the
remaining material; clipped holes or collisions with earlier cuts fail. Geometry checks do not establish
loads, omitted design requirements or fabrication readiness.

Existing operations live in `assembly_joint_machining_builder.py`,
`panel_machining_builder.py`, `cabineo_joint.py` and `equal_thickness_miter_joint.py`.
Inspect their contracts before creating a new operation. A custom blank/joint
builder uses the same single-shape and participant-cut checks. Shape-specific
extensions remain possible; standard machining should be reused.

For whole-assembly review, a root `assemblies/<id>/builder.py` exports `BUILDER`
and a CadQuery `ENVELOPE`. Run
`aikea-review-unit/scripts/build_furniture_design.py <project> --assembly <id>`.
Its GLB and geometry report remain prototype evidence; use the existing fabrication
gate for manufacturing claims. Build the complete root, including bought hardware.

When exact purchased connector geometry is included, link its `HardwarePurchaseSpec`
to `ConnectionPurchaseSpec(joint_id, connector_index, component)`. `component` is
`"connector"` or `"insert"` for a Cabineo connection; the index is one-based and
comes from the declared layout's paired cuts. The reference is relative to the
purchase owner (including `owner_levels_up`). Inventory reconciles that explicit
installed purchase with the machining occurrence instead of adding it twice.
Unlinked hardware is never matched by name or shape. Supplier packs and unverified
product compatibility are not inferred from this link.
