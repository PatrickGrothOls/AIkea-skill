"""Scope: Test safe overall wardrobe geometry and recalculation."""

from copy import deepcopy

import pytest

from overall_wardrobe_inputs import OverallWardrobeInputError
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestOverallWardrobeCalculator:
    def setup_method(self) -> None:
        self.project = OverallWardrobeTestProject()

    def test_flat_ceiling_produces_equal_cabinet_heights(self) -> None:
        result = self.project.calculate(self.project.load_flat())
        assert [cabinet.width_mm for cabinet in result.cabinets] == [1494.0, 1494.0]
        assert [cabinet.left_height_mm for cabinet in result.cabinets] == [2298.0, 2298.0]
        assert [cabinet.right_height_mm for cabinet in result.cabinets] == [2298.0, 2298.0]

    def test_piecewise_ceiling_is_sampled_at_cabinet_boundaries(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400},
            {"distance_from_left": 1000, "height_from_floor": 2400},
            {"distance_from_left": 3000, "height_from_floor": 1200},
        ]
        result = self.project.calculate(data)
        assert result.cabinets[0].left_height_mm == 2298.0
        assert result.cabinets[0].right_height_mm == pytest.approx(1998.6)
        assert result.cabinets[1].right_height_mm == pytest.approx(1102.2)

    def test_contradictory_width_inputs_are_rejected(self) -> None:
        data = self.project.load_flat()
        data["design_settings"]["cabinet_run"]["left_clearance"] = 2995
        with pytest.raises(OverallWardrobeInputError, match="leave no width"):
            self.project.calculate(data)

    def test_unequal_width_shares_still_close_the_available_width(self) -> None:
        data = self.project.load_flat()
        data["design_settings"]["cabinet_run"]["cabinet_width_shares"] = [1.8, 0.2]
        result = self.project.calculate(data)
        assert [cabinet.width_mm for cabinet in result.cabinets] == pytest.approx(
            [2689.2, 298.8]
        )
        assert result.cabinets[-1].right_position_mm == pytest.approx(2993.0)

    def test_one_width_change_recalculates_every_cabinet(self) -> None:
        original = self.project.load_flat()
        wider = deepcopy(original)
        wider["measured_space"]["width_measurements"] = dict.fromkeys(
            ("bottom", "middle", "top"), 3600
        )
        wider["measured_space"]["height_measurements"][1]["distance_from_left"] = 1800
        wider["measured_space"]["height_measurements"][-1]["distance_from_left"] = 3600
        original_result = self.project.calculate(original)
        wider_result = self.project.calculate(wider)
        assert [cabinet.width_mm for cabinet in original_result.cabinets] == [1494.0, 1494.0]
        assert [cabinet.width_mm for cabinet in wider_result.cabinets] == [1794.0, 1794.0]
        assert wider_result.cabinets[-1].right_position_mm == 3593.0

    def test_smallest_site_readings_receive_the_fit_allowance(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["width_measurements"] = {
            "bottom": 3000,
            "middle": 2998,
            "top": 2996,
        }
        data["measured_space"]["depth_measurements"] = {
            "left": 600,
            "middle": 598,
            "right": 599,
        }
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400},
            {"distance_from_left": 1498, "height_from_floor": 2398},
            {"distance_from_left": 2996, "height_from_floor": 2396},
        ]
        result = self.project.calculate(data)
        assert result.minimum_measured_width_mm == 2996.0
        assert result.minimum_measured_depth_mm == 598.0
        assert result.fit_allowance_mm == 2.0
        assert result.usable_width_mm == 2994.0
        assert result.usable_depth_mm == 596.0
        assert result.cabinets[0].left_height_mm == pytest.approx(2297.9933)
