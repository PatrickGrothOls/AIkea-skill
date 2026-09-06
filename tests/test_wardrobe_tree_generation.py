"""Scope: Verify one generated wardrobe root owns every complete assembly."""

from __future__ import annotations

import importlib

from assembly_composition_test_case import AssemblyCompositionTestCase
from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestWardrobeTreeGeneration(AssemblyCompositionTestCase):
    """Protect base-first ownership and saved left-to-right cabinet frames."""

    def test_four_cabinet_taxonomy_has_one_ordered_root(self, tmp_path) -> None:
        project = self._project(4)

        taxonomy = AssemblyTaxonomyGenerator().generate(project, tmp_path)

        wardrobe = taxonomy.wardrobe
        assert wardrobe is not None
        assert [child.assembly_id for child in wardrobe.child_assemblies] == [
            "base_01",
            "tall_storage_01",
            "tall_storage_02",
            "tall_storage_03",
            "tall_storage_04",
        ]
        base = taxonomy.assemblies[-1]
        expected_x = [
            assembly.global_left_mm - base.global_left_mm
            for assembly in (base, *taxonomy.assemblies[:-1])
        ]
        assert [
            child.local_to_parent.origin_in_parent_mm[0]
            for child in wardrobe.child_assemblies
        ] == expected_x
        root = tmp_path / "assemblies/wardrobe_01"
        assert (root / "spec.py").is_file()
        assert (root / "builder.py").is_file()
        assert (root / "complete_builder.py").is_file()
        source = (root / "builder.py").read_text(encoding="utf-8")
        assert "tall_storage_04.complete_builder" in source
        assert "zip(" in source and "strict=True" in source

    def test_tree_walker_accumulates_generated_root_child_frames(
        self, generated_values
    ) -> None:
        specification, project_root = generated_values
        wardrobe_spec = importlib.import_module("assemblies.wardrobe_01.spec").SPEC
        children = tuple(
            specification.BuiltChildAssembly(
                child,
                specification.BuiltAssembly(
                    self.fixture_assembly_spec(
                        child.assembly_id,
                        child.purpose,
                        (),
                        (),
                    ),
                    (),
                    (),
                ),
            )
            for child in wardrobe_spec.child_assemblies
        )
        wardrobe = specification.BuiltAssembly(
            wardrobe_spec,
            (),
            (),
            child_assemblies=children,
        )

        visits = GeneratedAssemblyBuilderLoader().walk(project_root, wardrobe)

        assemblies = [
            item for item in visits if type(item).__name__ == "AssemblyTreeAssembly"
        ]
        assert [item.assembly.spec.assembly_id for item in assemblies] == [
            "wardrobe_01",
            "base_01",
            "tall_storage_01",
        ]
        cabinet_x = assemblies[-1].local_to_root.origin_in_parent.x_mm
        saved_cabinet_x = (
            wardrobe_spec.child_assemblies[-1]
            .local_to_parent.origin_in_parent.x_mm
        )
        assert cabinet_x == saved_cabinet_x
        assert project_root.joinpath("assemblies/wardrobe_01/spec.py").is_file()

    def _project(self, cabinet_count: int) -> dict:
        data = OverallWardrobeTestProject().load_flat()
        run = data["design_settings"].pop("cabinet_run")
        data["design_settings"]["assembly_run"] = {
            "left_clearance": run["left_clearance"],
            "right_clearance": run["right_clearance"],
            "gap": run["cabinet_gap"],
            "ceiling_clearance": run["ceiling_clearance"],
            "assemblies": [
                {
                    "id": f"tall_storage_{index:02d}",
                    "purpose": "tall_storage",
                    "width_share": 1,
                }
                for index in range(1, cabinet_count + 1)
            ],
        }
        return data
