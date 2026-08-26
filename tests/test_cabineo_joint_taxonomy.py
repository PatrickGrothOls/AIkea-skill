"""Scope: Verify generated local frames and the first Cabineo joint definition."""

from __future__ import annotations

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestCabineoJointTaxonomy:
    """Keep face-and-edge choices in deterministic unit construction."""

    def test_left_side_to_top_has_one_complete_local_definition(self, tmp_path) -> None:
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

        assembly = AssemblyTaxonomyGenerator().generate(data, tmp_path).assemblies[0]
        left = next(part for part in assembly.parts if part.part_id == "left_side")
        joint = next(item for item in assembly.joints if item.joint_id == "left_side_to_top")

        assert left.local_size_mm == (582, 2298, 18)
        assert left.inside_face == ">Z"
        assert joint.source_part_id == "left_side"
        assert joint.target_part_id == "top_panel_01"
        assert (joint.source_face, joint.source_edge) == (">Z", ">Y")
        assert joint.connector_layout == "two_quarter_points"
