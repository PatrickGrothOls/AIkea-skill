"""Scope: Verify generated local frames and the first Cabineo joint definition."""

from __future__ import annotations

from types import SimpleNamespace

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabineo_connector_layout import CabineoConnectorLayout
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

        assert left.local_size_mm == (564, 2280, 18)
        assert left.inside_face == ">Z"
        assert joints == {
            "left_side_to_back_panel": ("left_side", "back_panel", ">Z", ">X"),
            "right_side_to_back_panel": ("right_side", "back_panel", ">Z", "<X"),
            "left_side_to_top": ("left_side", "top_panel_01", ">Z", ">Y"),
            "right_side_to_top": ("right_side", "top_panel_01", ">Z", ">Y"),
            "top_panel_01_to_back_panel": (
                "top_panel_01",
                "back_panel",
                "<Z",
                ">Y",
            ),
        }


class TestCabineoConnectorLayout:
    """Keep every connector run within the agreed structural distances."""

    def setup_method(self) -> None:
        self.layout = CabineoConnectorLayout()
        self.joint = SimpleNamespace(
            connector_layout="bounded_spacing",
            source_face=">Z",
            source_edge=">X",
        )

    def test_long_edge_uses_the_minimum_count_that_meets_every_limit(self) -> None:
        positions = self._positions(2284.0)

        assert len(positions) == 8
        assert positions[0] <= 200.0
        assert 2284.0 - positions[-1] <= 200.0
        assert max(right - left for left, right in zip(positions, positions[1:])) <= 300.0

    def test_short_edge_still_uses_two_connectors(self) -> None:
        assert self._positions(356.0) == (89.0, 267.0)

    def test_existing_generated_layout_receives_the_same_safe_distribution(self) -> None:
        legacy_joint = SimpleNamespace(
            connector_layout="two_quarter_points",
            source_face=">Z",
            source_edge=">X",
        )
        part = SimpleNamespace(local_size_mm=(18.0, 2284.0, 18.0))

        assert self.layout.positions(legacy_joint, part) == self._positions(2284.0)

    def _positions(self, length_mm: float) -> tuple[float, ...]:
        part = SimpleNamespace(local_size_mm=(18.0, length_mm, 18.0))
        return self.layout.positions(self.joint, part)
