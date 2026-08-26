"""Scope: Verify generated local frames and the first Cabineo joint definition."""

from __future__ import annotations

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestCabineoJointTaxonomy:
    """Keep Cabinet 2's proven face-and-edge choices deterministic."""

    def test_flat_carcass_has_complete_cabineo_definitions(self, tmp_path) -> None:
        data = OverallWardrobeTestProject().load_flat()
        data["design_settings"]["materials"]["back_panel_thickness"] = 18
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

        assembly = AssemblyTaxonomyGenerator().generate(data, tmp_path).assemblies[0]
        left = next(part for part in assembly.parts if part.part_id == "left_side")
        joints = {
            joint.joint_id: (
                joint.source_part_id,
                joint.target_part_id,
                joint.source_face,
                joint.source_edge,
            )
            for joint in assembly.joints
            if joint.joint_type == "cabineo"
        }

        assert left.local_size_mm == (564, 2298, 18)
        assert left.inside_face == ">Z"
        assert joints == {
            "left_side_to_back_panel": ("left_side", "back_panel", ">Z", ">X"),
            "right_side_to_back_panel": ("right_side", "back_panel", ">Z", "<X"),
            "left_side_to_top": ("top_panel_01", "left_side", "<Z", "<X"),
            "right_side_to_top": ("top_panel_01", "right_side", "<Z", ">X"),
            "top_panel_01_to_back_panel": (
                "top_panel_01",
                "back_panel",
                "<Z",
                ">Y",
            ),
        }
