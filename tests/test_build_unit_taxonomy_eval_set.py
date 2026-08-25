"""Scope: Verify the build-unit taxonomy eval answer contract."""

from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


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

        assert answer["expected_paths_per_assembly"]
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
        assert dict(door.dimensions_mm)["left_height"] == expected["door_height_mm"]
        for assembly in result.assemblies:
            root = tmp_path / "assemblies" / assembly.assembly_id
            assert all((root / relative).is_file() for relative in answer["expected_paths_per_assembly"])
