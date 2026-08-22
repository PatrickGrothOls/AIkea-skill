"""Scope: Test overall input validation, normalization, and recalculation."""

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from overall_wardrobe_calculator import OverallWardrobeCalculator, OverallWardrobeResult
from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputReader


class TestOverallWardrobe:
    def test_flat_ceiling_produces_equal_cabinet_heights(self) -> None:
        result = self._calculate(self._flat_project())
        assert [cabinet.width_mm for cabinet in result.cabinets] == [1495.0, 1495.0]
        assert [cabinet.left_height_mm for cabinet in result.cabinets] == [2300.0, 2300.0]
        assert [cabinet.right_height_mm for cabinet in result.cabinets] == [2300.0, 2300.0]

    def test_piecewise_ceiling_is_sampled_at_cabinet_boundaries(self) -> None:
        project = self._flat_project()
        project["measured_space"]["ceiling_points"] = [
            {"distance_from_left": 0, "height_from_floor": 2400},
            {"distance_from_left": 1000, "height_from_floor": 2400},
            {"distance_from_left": 3000, "height_from_floor": 1200},
        ]
        result = self._calculate(project)
        assert result.cabinets[0].left_height_mm == 2300.0
        assert result.cabinets[0].right_height_mm == 2000.0
        assert result.cabinets[1].right_height_mm == 1103.0

    def test_missing_values_are_reported_together(self) -> None:
        project = self._flat_project()
        project["measured_space"]["width"] = None
        project["design_settings"]["base"]["height"] = None
        with pytest.raises(OverallWardrobeInputError) as raised:
            OverallWardrobeInputReader().read(project)
        assert "measured_space.width is required and must be numeric" in raised.value.problems
        assert "design_settings.base.height is required and must be numeric" in raised.value.problems

    def test_contradictory_width_inputs_are_rejected(self) -> None:
        project = self._flat_project()
        project["design_settings"]["cabinet_run"]["left_clearance"] = 2995
        with pytest.raises(OverallWardrobeInputError, match="leave no width"):
            self._calculate(project)

    def test_ceiling_points_must_cover_the_full_width(self) -> None:
        project = self._flat_project()
        project["measured_space"]["ceiling_points"][-1]["distance_from_left"] = 2999
        with pytest.raises(OverallWardrobeInputError, match="end at measured_space.width"):
            OverallWardrobeInputReader().read(project)

    def test_unequal_width_shares_still_close_the_available_width(self) -> None:
        project = self._flat_project()
        run = project["design_settings"]["cabinet_run"]
        run["cabinet_width_shares"] = [1.8, 0.2]
        result = self._calculate(project)
        assert [cabinet.width_mm for cabinet in result.cabinets] == [2691.0, 299.0]
        assert result.cabinets[-1].right_position_mm == 2995.0

    def test_centimetres_are_normalized_to_millimetres(self) -> None:
        project = self._flat_project()
        project["units"] = "cm"
        project["measured_space"]["width"] = 300
        project["measured_space"]["depth"] = 60
        project["measured_space"]["ceiling_points"] = [
            {"distance_from_left": 0, "height_from_floor": 240},
            {"distance_from_left": 300, "height_from_floor": 240},
        ]
        for section, field in (("base", "height"), ("doors", "gap")):
            project["design_settings"][section][field] /= 10
        run = project["design_settings"]["cabinet_run"]
        for field in (
            "left_clearance",
            "right_clearance",
            "cabinet_gap",
            "ceiling_clearance",
        ):
            run[field] /= 10
        for field in project["design_settings"]["materials"]:
            project["design_settings"]["materials"][field] /= 10
        result = self._calculate(project)
        assert result.width_mm == 3000.0
        assert result.finished_depth_mm == 600.0
        assert result.cabinets[0].left_height_mm == 2300.0

    def test_one_width_change_recalculates_every_cabinet(self) -> None:
        original = self._flat_project()
        wider = deepcopy(original)
        wider["measured_space"]["width"] = 3600
        wider["measured_space"]["ceiling_points"][-1]["distance_from_left"] = 3600
        original_result = self._calculate(original)
        wider_result = self._calculate(wider)
        assert [cabinet.width_mm for cabinet in original_result.cabinets] == [1495.0, 1495.0]
        assert [cabinet.width_mm for cabinet in wider_result.cabinets] == [1795.0, 1795.0]
        assert wider_result.cabinets[-1].right_position_mm == 3595.0

    def _calculate(self, project: dict) -> OverallWardrobeResult:
        inputs = OverallWardrobeInputReader().read(project)
        return OverallWardrobeCalculator().calculate(inputs)

    def _flat_project(self) -> dict:
        path = Path(__file__).parent / "fixtures" / "flat-aikea.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))
