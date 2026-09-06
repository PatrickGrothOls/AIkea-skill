"""Scope: Verify generated cabinet and base specs own every part placement."""

from __future__ import annotations

import importlib

from assembly_composition_test_case import AssemblyCompositionTestCase
from assembly_taxonomy import BaseAssemblyTaxonomy, LocalAssemblyTaxonomy
from assembly_taxonomy_resolver import AssemblyTaxonomyResolver
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestPartPlacementTaxonomy(AssemblyCompositionTestCase):
    """Protect the physical frames migrated from the legacy review locators."""

    def test_storage_taxonomy_contains_canonical_part_frames(self) -> None:
        project = AssemblyTaxonomyResolver().resolve(self._project())
        cabinet = next(
            item for item in project.assemblies if isinstance(item, LocalAssemblyTaxonomy)
        )

        left = self._part(cabinet, "left_side").local_to_parent
        right = self._part(cabinet, "right_side").local_to_parent
        door = self._part(cabinet, "door_panel").local_to_parent
        shelf = self._part(cabinet, "shelf_01").local_to_parent

        assert left.origin_in_parent_mm == (0.0, 0.0, cabinet.base_height_mm)
        assert left.local_x_in_parent == (0.0, 1.0, 0.0)
        assert left.local_y_in_parent == (0.0, 0.0, 1.0)
        assert right.origin_in_parent_mm == (
            cabinet.width_mm,
            cabinet.inside_depth_mm,
            cabinet.base_height_mm,
        )
        assert right.local_z_in_parent == (-1.0, 0.0, 0.0)
        assert door.origin_in_parent_mm[2] == cabinet.door_bottom_mm
        assert shelf.origin_in_parent_mm[0] == 18.0
        assert shelf.local_z_in_parent == (0.0, 0.0, 1.0)

    def test_base_taxonomy_contains_module_relative_part_frames(self) -> None:
        project = AssemblyTaxonomyResolver().resolve(self._project())
        base = next(
            item for item in project.assemblies if isinstance(item, BaseAssemblyTaxonomy)
        )

        deck = self._part(base, "deck_01").local_to_parent
        front = self._part(base, "front_rail_01").local_to_parent
        back = self._part(base, "back_rail_01").local_to_parent
        brace = self._part(base, "brace_01_01").local_to_parent

        assert deck.origin_in_parent_mm == (0.0, 0.0, base.height_mm - 18.0)
        assert front.origin_in_parent_mm[1] == base.plinth_recess_mm + 18.0
        assert back.origin_in_parent_mm[1] == base.depth_mm
        assert brace.local_x_in_parent == (0.0, 1.0, 0.0)
        assert brace.local_z_in_parent == (1.0, 0.0, 0.0)

    def test_generated_spec_builds_a_complete_walkable_part_tree(
        self, generated_values
    ) -> None:
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        spec = importlib.import_module("assemblies.tall_storage_01.spec").SPEC
        parts = tuple(values.BuiltPart(part, object()) for part in spec.parts)
        built = values.BuiltAssembly(spec, parts, spec.joints)

        visits = tree.AssemblyTreeWalker().walk(built)

        assert len(visits) == len(spec.parts) + 1
        assert all(part.local_to_parent is not None for part in spec.parts)
        assert visits[1].local_to_root == spec.parts[0].local_to_parent

    def _part(self, assembly, part_id: str):
        return next(part for part in assembly.parts if part.part_id == part_id)

    def _project(self) -> dict:
        data = OverallWardrobeTestProject().load_flat()
        run = data["design_settings"].pop("cabinet_run")
        data["design_settings"]["assembly_run"] = {
            "left_clearance": run["left_clearance"],
            "right_clearance": run["right_clearance"],
            "gap": run["cabinet_gap"],
            "ceiling_clearance": run["ceiling_clearance"],
            "assemblies": [
                {
                    "id": "tall_storage_01",
                    "purpose": "tall_storage",
                    "width_share": 1,
                }
            ],
        }
        return data
