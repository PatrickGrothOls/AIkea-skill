# Construction tools

Inspect the relevant implementation and reference before choosing or extending it.
Repository paths below are relative to the skill package root. Installed project
contracts under `assemblies/` import these shared runtimes; do not freeze a copy.

| Need | Input and implementation | Output/check boundary |
| --- | --- | --- |
| Rectangular or polygonal physical panel | `PartSpec` with material, local frame and explicit `local_size_mm`/`outline_mm`; `aikea-build-units/scripts/panel_blank_builder.py` | One local solid; role does not select drilling. |
| Configured or authored construction | `PanelAssemblySpec`; project `assemblies/panel_assembly.py` | `PanelAssemblyBuilder` applies the same declared joints and machining to either route. |
| Add machining to current parts | `aikea-build-units/scripts/panel_machining_feature.py` | Preserves earlier operations, children and hardware; checks actual subtraction and clipping. |
| Rigid placement and nesting | Project `assembly_placement.py`, `assembly_composition.py`, `assembly_tree.py` | One declared/built tree, accumulated right-handed frames, unique physical ownership. |
| Cabineo connection | `CabineoJointSpec`; `cabineo_joint.py`, `cabineo_connector_layout.py` | Paired source/receiver cuts and explicit occurrences. Check actual faces, edge, thickness and receiver; spacing is not load evidence. |
| Equal-thickness miter | `equal_thickness_miter_joint.py` | Both participant frames determine paired machining; apply its actual geometric limits. |
| Shelf/hardware grid | `PartMachiningSpec(id, part, "system_32")` | Explicit common machining; labels never activate a grid. |
| Dimensioned surface holes | `SurfaceDrillingSpec`, `SurfaceHole`; [surface drilling](../../aikea-build-units/references/surface-drilling.md) | Whole openings/depth must fit actual remaining material. Only explicitly matched whole holes may be reused. |
| Drilling through contacting layers | `LayeredSurfaceDrilling` in `aikea-build-units/scripts` | Emits ordinary requests per physical layer; rejects gaps/overlaps/partial circles. Apply through the common feature to catch earlier openings. |
| Rectangular groove or rounded pocket | `SurfaceGrooveSpec` / `SurfacePocketSpec`; [panel construction](../../aikea-build-units/references/panel-construction.md) | Explicit datum, dimensions, depth and optional pocket radius; actual surface entry and subtraction are checked. |
| Secondary edge rounding | `PanelEdgeFinishSpec`, `EdgeRound`, `PanelEdgeFinishCutBuilder` in `aikea-build-units/scripts/panel_edge_finish.py`; apply through `PanelMachiningFeature` | Explicit edges/radii on existing machined solids, recorded as secondary finishing cuts. This does not qualify router setup, retained joint strength or a single-face CNC process. Keep the CNC-stage audit separate; the complete face audit must still flag this unqualified operation. |
| Purchased identity | `PurchasedHardwareSpec`, `HardwarePurchaseSpec`, optional `ConnectionPurchaseSpec` | Physical geometry and installed purchase units remain distinct; explicit connection links prevent duplicate Cabineo purchases. Set `mounting_part_id` to the real mounting panel in the same owning assembly so exploded inspection preserves that attachment. |
| Required work and scoped evidence | `ConstructionRequirementSpec`; [shared contract](../../aikea-build-units/references/shared-construction.md) | Missing/unrelated operations, unassessed materials and stale qualification remain visible. |
| One broad machining face per part | `aikea-review-unit/scripts/check_panel_setups.py <project> --assembly <root-id>` | Audits declared Cabineo/surface-operation entry faces through the whole tree. Opposing blind demands and edge/unknown operations fail; through openings can share either face. This does not approve missing hardware holes, actual subtraction, tooling, workholding or CAM. |
| A new operation | Shared blank/joint extension contract, `PartCut` and `AssemblyCuts` | Actual per-part cuts plus focused qualification evidence. A direct `BuiltAssembly` return does not bypass official checks. |
| Whole-tree review and inventory | [project contract](authored-assemblies.md), [physical counting](../../aikea-review-unit/references/physical-item-counting.md) | Same tree feeds geometry, purchases and sheet inputs. Scenarios do not regenerate the actual design. |

For ordinary construction, begin with the [shared input example](../../aikea-build-units/references/shared-construction.md).
The frame, material, local operations and independent requirements remain editable
after a configurator produces them. Read a tool's concrete limits rather than
treating the table as a universal engineering approval.
