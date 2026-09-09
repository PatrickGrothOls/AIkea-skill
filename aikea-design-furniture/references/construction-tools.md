# Discover construction tools by operation

Read the referenced implementation or feature reference when using that operation.
All paths below are relative to the skill package root, not a client project.

| Need | Existing tool and contract |
| --- | --- |
| Rectangular or polygonal panel | `aikea-build-units/scripts/blank_sheet_builder.py`: `BlankSheetBuilder.rectangle(w, h, t)` or `BlankSheetBuilder(outline, t)`, then `.build()`. Returns a real local CadQuery solid, Z=0..thickness. |
| Semantic-free panel assembly | Project `assemblies/panel_assembly.py`: `PanelAssemblySpec` and `PanelAssemblyBuilder`; geometry comes from `PartSpec.local_size_mm` or its outline. No implicit drilling from a role. |
| CNC limits and oversized spans | `aikea-build-units/scripts/cnc_work_area.py` owns usable blank size; `panel_segment_planner.py` proposes segments with preferred support boundaries. Read `aikea-build-units/references/panel-construction.md`. Design the real joins and include their extensions; the planner only divides intervals. |
| Rigid placement | Project `assemblies/assembly_placement.py`: `LocalToParentPlacement`, `Point3D`, right-handed `AxisBasis`; `local_to_parent_location.py` converts it to CadQuery. |
| Nested units and purchased items | Project `assemblies/assembly_composition.py` and `assembly_tree.py`: `ChildAssemblySpec`, `BuiltChildAssembly`, `PurchasedHardwareSpec`, `BuiltPurchasedHardware`, `BuiltAssembly`, and accumulated tree placements. |
| Cabineo pocket and receiver together | `aikea-build-units/scripts/cabineo_joint.py` and `cabineo_connector_layout.py`; `CabineoJointSpec` selects the source face, source edge and connector spacing. Verify the actual receiving panel, material thickness and cutter reach. |
| Paired equal-thickness miter | `aikea-build-units/scripts/equal_thickness_miter_joint.py` and `part_outside_face_plane.py`; explicit placements and inside-face orientation determine the shared cut. |
| Return machining to its owners | `aikea-build-units/scripts/part_cut.py`: `PartCut(joint_id, part_id, connector_index, cutter, location)` and `AssemblyCuts`. The location maps the cutter into that part's local frame. |
| A new groove, rebate, drilling pattern or connection | Author a focused blank/machining or joint builder from CadQuery operations. Return the existing part/cut contracts. For a mating connection derive both sides from one joint. Check retained material, intersection, fit and manufacture; don't add a furniture-type template. |
| System 32 grid when wanted | `aikea-build-units/scripts/system_32_side_panel_grid.py`; request its machining explicitly and satisfy its panel-local dimension/inside-face contract. |
| Wooden drawer and runners | `$aikea-build-drawers`, especially its `references/runner-selection.md` and `scripts/drawer_box_planner.py`. Discover suitable products from available space and load. Exact new products need their machining, placement and motion integration. |
| Door and hinges | `$aikea-build-doors` and `references/door-and-hinge-construction.md`; reused templates need matching host-panel and opening contracts. Custom orientations still need paired cup/plate machining and exact closed/open evidence. |
| Optional framed front | [$aikea-design-framed-doors](../../aikea-design-framed-doors/SKILL.md) installs a configurable backing-and-applied-frame helper. Other outlines, joinery and door styles remain model-authored through the existing primitives. |
| Lighting | `$aikea-add-lighting`; host-local run drives both groove and purchased luminaire. |
| Generic built-tree review | `aikea-review-unit/scripts/build_furniture_design.py`; uses the existing tree walker, review geometry and GLB exporter. No cabinet-purpose lookup. |

The feature scripts expose concrete product and host contracts; they are not
universal mechanisms merely because their skill names are broad. Read and adapt
the smallest relevant owner. When no template matches, continue designing with
the underlying tools and add the missing operation rather than changing the
client's furniture to fit a template.
