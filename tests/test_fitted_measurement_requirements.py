"""Scope: Test measurement counts selected from the installation arrangement."""

import pytest

from overall_wardrobe_inputs import (
    OverallWardrobeInputError,
    OverallWardrobeInputReader,
)
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestFittedMeasurementRequirements:
    def setup_method(self) -> None:
        self.project = OverallWardrobeTestProject()

    def test_open_dimensions_accept_one_measurement_each(self) -> None:
        data = self.project.load_flat()
        data["design_settings"]["fitted_dimensions"] = {
            "width": False,
            "depth": False,
            "height": False,
        }
        data["measured_space"]["width_measurements"] = {"single": 3000}
        data["measured_space"]["depth_measurements"] = {"single": 600}
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400}
        ]

        inputs = OverallWardrobeInputReader().read(data)

        assert inputs.space.width_measurements_mm == (3000.0,)
        assert inputs.space.depth_measurements_mm == (600.0,)
        assert len(inputs.space.top_boundary.measurements) == 1

    def test_fitted_width_requires_three_measurements(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["width_measurements"] = {"single": 3000}

        with pytest.raises(OverallWardrobeInputError, match="width_measurements.bottom"):
            OverallWardrobeInputReader().read(data)

    def test_fitted_height_requires_three_measurements(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400}
        ]

        with pytest.raises(OverallWardrobeInputError, match="at least three"):
            OverallWardrobeInputReader().read(data)

    def test_flush_depth_requires_three_measurements(self) -> None:
        data = self.project.load_flat()
        data["design_settings"]["fitted_dimensions"]["depth"] = True

        with pytest.raises(OverallWardrobeInputError, match="depth_measurements.left"):
            OverallWardrobeInputReader().read(data)

    def test_inches_are_normalized_to_millimetres(self) -> None:
        data = self.project.load_flat()
        data["units"] = "in"
        scale = 25.4
        data["measured_space"]["width_measurements"] = dict.fromkeys(
            ("bottom", "middle", "top"), 3000 / scale
        )
        data["measured_space"]["depth_measurements"] = {"single": 600 / scale}
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400 / scale},
            {"distance_from_left": 1500 / scale, "height_from_floor": 2400 / scale},
            {"distance_from_left": 3000 / scale, "height_from_floor": 2400 / scale},
        ]
        data["design_settings"]["fit_allowance"] = 2 / scale
        for section, field in (("base", "height"), ("doors", "gap")):
            data["design_settings"][section][field] /= scale
        for field in (
            "left_clearance",
            "right_clearance",
            "cabinet_gap",
            "ceiling_clearance",
        ):
            data["design_settings"]["cabinet_run"][field] /= scale
        for field in data["design_settings"]["materials"]:
            data["design_settings"]["materials"][field] /= scale

        inputs = OverallWardrobeInputReader().read(data)

        assert inputs.space.minimum_width_mm == pytest.approx(3000)
        assert inputs.space.minimum_depth_mm == pytest.approx(600)
        assert inputs.settings.fit_allowance_mm == pytest.approx(2)
