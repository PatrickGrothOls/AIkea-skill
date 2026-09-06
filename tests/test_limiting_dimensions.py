"""Scope: Test limiting width, depth, and flat-height calculations."""

from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestLimitingDimensions:
    """Keep measurement variation out of square and level wardrobe geometry."""

    def setup_method(self) -> None:
        self.project = OverallWardrobeTestProject()

    def test_width_uses_smallest_reading_for_one_square_run(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["width_measurements"] = {
            "bottom": 3000,
            "middle": 2998,
            "top": 2996,
        }

        result = self.project.calculate(data)

        assert result.minimum_measured_width_mm == 2996
        assert [cabinet.width_mm for cabinet in result.cabinets] == [1492, 1492]

    def test_flush_depth_uses_smallest_reading_for_one_depth(self) -> None:
        data = self.project.load_flat()
        data["design_settings"]["fitted_dimensions"]["depth"] = True
        data["measured_space"]["depth_measurements"] = {
            "left": 600,
            "middle": 598,
            "right": 599,
        }

        result = self.project.calculate(data)

        assert result.minimum_measured_depth_mm == 598
        assert result.cabinet_depth_mm == 578
        assert result.inside_depth_mm == 572

    def test_flat_top_uses_smallest_reading_for_every_unit_edge(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400},
            {"distance_from_left": 1500, "height_from_floor": 2398},
            {"distance_from_left": 3000, "height_from_floor": 2396},
        ]

        result = self.project.calculate(data)

        assert [cabinet.left_height_mm for cabinet in result.cabinets] == [2294, 2294]
        assert [cabinet.right_height_mm for cabinet in result.cabinets] == [2294, 2294]
