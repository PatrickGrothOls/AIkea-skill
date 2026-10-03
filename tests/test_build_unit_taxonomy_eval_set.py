"""Scope: Verify the build-unit taxonomy eval answer contract."""

from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from system_32_side_panel_grid import System32SidePanelGrid


class TestBuildUnitTaxonomyEvalSet:
    """Keep the manual eval answer aligned with generated project files."""

    _EVAL_PATH = (
        Path(__file__).parents[1] / "evals" / "build-unit-taxonomy.yaml"
    )

    def test_case_has_exact_paths_and_local_values(self, tmp_path) -> None:
        eval_set = yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
        case = eval_set["cases"][0]
        answer = case["answer_key"]
        project = case["starting_project"]["aikea_yaml"]

        assert answer["expected_paths_per_storage_assembly"]
        assert answer["expected_next_stage"] == "aikea-review-unit"
        result = AssemblyTaxonomyGenerator().generate(project, tmp_path)
        expected = answer["expected_first_assembly"]
        first = result.assemblies[0]

        assert first.global_left_mm == expected["global_left_mm"]
        assert first.global_right_mm == pytest.approx(expected["global_right_mm"])
        assert first.width_mm == pytest.approx(expected["width_mm"])
        assert [(point.x_mm, point.height_mm) for point in first.top] == [
            (pytest.approx(x), pytest.approx(height)) for x, height in expected["top"]
        ]
        assert first.depth_mm == expected["depth_mm"]
        assert first.inside_depth_mm == expected["inside_depth_mm"]
        door = next(part for part in first.parts if part.part_id == "door_panel")
        left_side = next(part for part in first.parts if part.part_id == "left_side")
        top_panel = next(part for part in first.parts if part.part_id == "top_panel_01")
        assert dict(door.dimensions_mm)["left_height"] == expected["door_height_mm"]
        assert dict(left_side.dimensions_mm)["height"] == expected["side_panel_height_mm"]
        assert dict(top_panel.dimensions_mm)["length"] == pytest.approx(
            expected["top_panel_width_mm"]
        )
        shelves = [part for part in first.parts if part.role == "shelf_panel"]
        assert len(shelves) == expected["shelf_count"]
        assert all(
            dict(shelf.dimensions_mm)["width"]
            == pytest.approx(expected["shelf_width_mm"])
            for shelf in shelves
        )
        assert [
            dict(shelf.dimensions_mm)["support_row_height"] for shelf in shelves
        ] == expected["shelf_support_rows_mm"]
        assert list(
            System32SidePanelGrid().column_positions_mm(first.inside_depth_mm)
        ) == expected["side_hole_columns_mm"]
        self._assert_first_joint(first, answer["expected_first_joint"])
        for assembly in result.assemblies[:-1]:
            root = tmp_path / "assemblies" / assembly.assembly_id
            assert all(
                (root / relative).is_file()
                for relative in answer["expected_paths_per_storage_assembly"]
            )
        self._assert_base(result.assemblies[-1], answer["expected_base"], tmp_path)

    def _assert_base(self, base, expected, project_root) -> None:
        assert base.assembly_id == expected["assembly_id"]
        assert base.width_mm == expected["width_mm"]
        assert base.depth_mm == expected["depth_mm"]
        assert base.height_mm == expected["height_mm"]
        assert [
            (module.start_x_mm, module.end_x_mm) for module in base.modules
        ] == [
            (pytest.approx(start), pytest.approx(end))
            for start, end in expected["module_spans_mm"]
        ]
        roles = [part.role for part in base.parts]
        assert roles.count("base_deck") == expected["deck_count"]
        assert roles.count("base_rail") == expected["rail_count"]
        assert roles.count("base_brace") == expected["brace_count"]
        root = project_root / "assemblies" / base.assembly_id
        assert all((root / relative).is_file() for relative in expected["paths"])
        assert all(
            (root / "parts" / part.part_id / "spec.py").is_file()
            and (root / "parts" / part.part_id / "builder.py").is_file()
            for part in base.parts
        )

    def _assert_first_joint(self, assembly, expected) -> None:
        joint = next(
            item for item in assembly.joints if item.joint_id == expected["joint_id"]
        )
        assert joint.joint_type == expected["joint_type"]
        assert joint.source_part_id == expected["source_part_id"]
        assert joint.target_part_id == expected["target_part_id"]
        assert joint.source_face == expected["source_face"]
        assert joint.source_edge == expected["source_edge"]
        assert joint.connector_layout == expected["connector_layout"]
