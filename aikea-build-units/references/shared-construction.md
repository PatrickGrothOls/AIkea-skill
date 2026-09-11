# Shared panel construction

Use shared construction inputs for an authored assembly or the editable output
of a component configurator. Each part has explicit local geometry and placement;
its role is a label, not a request to drill holes. The tall-storage configurator
and [structural-base recipes](base-recipe.md) emit those inputs and use this
builder. Older saved builders need explicit conflict-preserving migration.

Initialise contracts with `scripts/init_furniture_design.py <project>` using the
active CadQuery environment. Author local inputs and a root builder that returns
the existing complete `BuiltAssembly` tree. Keep project measurements authoritative.

```python
from assemblies.panel_assembly import PanelAssemblyBuilder, PanelAssemblySpec, PartMachiningSpec
from assemblies.specification import ConstructionRequirementSpec, PartSpec, IDENTITY_LOCAL_TO_PARENT

board = PartSpec(
    "partition", "partition", (), IDENTITY_LOCAL_TO_PARENT,
    local_size_mm=(400, 700, 16), inside_face=">Z", material_id="mdf",
)
spec = PanelAssemblySpec(
    "component_01", "authored component", parts=(board,),
    machining=(PartMachiningSpec("shelf_grid", "partition", "system_32"),),
    requirements=(ConstructionRequirementSpec(
        "partition_attachment", "Resolve how the partition is supported and attached",
        ("part:partition",),
    ),),
)
BUILDER = PanelAssemblyBuilder(spec)
```

The dimensions above demonstrate the contract; they are not project defaults.
Leaving `machining=()` produces an undrilled blank. Use explicit `CabineoJointSpec`
or a supported miter joint to join actual panels. Joint tools derive both cuts
from their participants' frames. Unknown operations, incorrect ownership and
cutters that miss a participant fail construction. Explicit local operations
(System 32 and [surface drilling](surface-drilling.md)) require their cutters to
fit completely inside the remaining material; clipped holes or collisions with
earlier cuts fail. Geometry checks do not establish
loads, omitted design requirements or fabrication readiness.

## Adapting a standard recipe

`generate_unit_taxonomy.py` retains the standard cabinet calculations and writes
editable parts, joints and `machining` into `assemblies/<id>/spec.py`. Cabinet
metadata remains available to existing fitted-door and drawer tools. The generated
builder executes that specification directly through `PanelAssemblyBuilder`;
individual part entry points read the result of that same complete build.

Use `dataclasses.replace` to adapt the saved parts or construct a `PanelAssemblySpec`
from `SPEC.parts`, `SPEC.joints`, `SPEC.machining` and `SPEC.requirements`. Keep child and purchase
declarations too when present. Explicit System 32 requests remain independent of
part names and roles. Update outlines, local sizes, placements and dependent joint
references together. For a shared panel between adjacent components, give it one
physical owner and define both connections in that owner's combined assembly;
do not include the same board in two child inventories.

Generated-file hashes distinguish untouched recipe output from authored changes.
Regeneration updates untouched files and stops before writing if an authored file
conflicts. Preserve those edits and deliberately reconcile them with the new
dimensions; never remove the record or overwrite the edit to force regeneration.
Older unrecorded files that cannot be identified exactly also require reconciliation.
Dimension edits require a fresh build/review; previous approval is not permission
to manufacture the revised assembly.

An unfinished preview can explicitly use `allow_unresolved=True`. Only joints
declared with `joint_type="unresolved"` omit machining, and they remain in the
built tree and draft inventory. Missing participants and unsupported named tools
still fail. The standard recipe uses this mode for unselected attachments; finish
those requirements through the relevant feature tools before fabrication review.

Existing operations live in `assembly_joint_machining_builder.py`,
`panel_machining_builder.py`, `surface_hole_pattern.py`, `cabineo_joint.py` and `equal_thickness_miter_joint.py`.
Inspect their contracts before creating a new operation. A custom blank/joint
builder uses the same single-shape and participant-cut checks. Shape-specific
extensions remain possible; standard machining should be reused.

For whole-assembly review, a root `assemblies/<id>/builder.py` exports `BUILDER`
and a CadQuery `ENVELOPE`. Run
`aikea-review-unit/scripts/build_furniture_design.py <project> --assembly <id>`.
Its GLB and geometry report remain prototype evidence; use the existing fabrication
gate for manufacturing claims. Build the complete root, including bought hardware.

Official review loaders also verify the returned tree independently of the chosen
builder: declared participants/occurrences, selected built-in cutter geometry,
actual subtraction and valid manufactured solids. A direct `BuiltAssembly` return
does not bypass these checks. `build_furniture_design.py` honors an existing
`complete_builder.py`, records construction checks alongside geometry, and revokes
the previous success report before rebuilding. An old GLB left after a failed
build is not fresh evidence; the new invalid report contains no GLB reference.
Run `check_fabrication_readiness.py <project>/aikea.yaml --assembly <root-id>` for
that same tree. Novel operation types still need separate qualification evidence;
passing participant and shape checks alone does not provide it.
For complete position records, bounded contact declarations and a fabrication
review on any root, follow the [closed position protocol](../../aikea-review-unit/references/construction-position.md).

## Requirements and extension evidence

Keep `requirements` separate from executed joints. The standard recipe writes
editable declarations for its connections and leaves unassigned support unresolved.
Removing a joint must not silently remove the requirement it was meant to satisfy.
`None` means the assembly has not been assessed; an empty tuple means it has no
local obligations, but every physical item still needs coverage from its owner or
an ancestor. Describe the brief's support, attachment, motion and material needs;
the checker cannot discover an omitted requirement from a model's appearance.

Each `ConstructionRequirementSpec` has a stable ID, description, owner-relative
`subject_paths` such as `part:side`, `drawer_01/part:front` or `hardware:hinge`,
and a disposition. `operations` references exact `joint:<id>`, `machining:<id>`
or `feature:<module>` paths; nested references use the same child path prefixes.
Every subject must be covered by those operations. `loose` and `floor_contact`
require a written `basis` and cannot claim machining or hardware installation.
Leave unsupported load, motion and product suitability questions `unresolved`.
Operation coverage alone does not prove those engineering requirements.

A custom joint still implements `AssemblyCuts` and `PartCut` for every participant.
For qualification, register its owning feature and exact affected manufactured
paths in `features.json`, including `qualified_joint_ids`. The feature's existing
manufacturing report must contain the same joint IDs, passed applicable checks,
current STEP checksums and `construction_sha256` from
`ConstructionInputFingerprinter().build(project_root, visits)` after the final
build/export inputs are saved. Test the new operation's coordinate registration,
machining and applicable limits independently; do not manufacture a passing
report from geometry success. The report is an evidence contract, not a sandbox
against arbitrary authored Python or invented test results.

For installed hardware, register exact `affected_purchased_hardware_paths` alongside
the machined parts through `CabinetFeatureManifest.register`. Include those full
physical paths as `purchased_hardware_paths` in the evidence record. The requirement
can then reference `feature:<module>` for both its panels and installed hardware;
the current input hash also binds that evidence to the selected product. Paths
are ordered as registered, and omitted or unrelated hardware cannot be covered.

The fabrication gate qualifies only joints whose complete participant set lies
inside that valid current feature scope. Missing participants/cuts still fail the
independent output check. Changed material, dimensions, selected products,
requirements or project source invalidate qualification and visual approval, even
when the GLB bytes happen to stay the same. Existing unbound approvals need a new
review; there is no extra approval workflow.

When exact purchased connector geometry is included, link its `HardwarePurchaseSpec`
to `ConnectionPurchaseSpec(joint_id, connector_index, component)`. `component` is
`"connector"` or `"insert"` for a Cabineo connection; the index is one-based and
comes from the declared layout's paired cuts. The reference is relative to the
purchase owner (including `owner_levels_up`). Inventory reconciles that explicit
installed purchase with the machining occurrence instead of adding it twice.
Unlinked hardware is never matched by name or shape. Supplier packs and unverified
product compatibility are not inferred from this link.
