"""Scope: Test overall measurement and shared-setting input handling."""

import pytest

from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputReader
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestOverallWardrobeInputs:
    def setup_method(self) -> None:
        self.project = OverallWardrobeTestProject()

    def test_missing_values_are_reported_together(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["width_measurements"]["bottom"] = None
        data["design_settings"]["base"]["height"] = None
        with pytest.raises(OverallWardrobeInputError) as raised:
            OverallWardrobeInputReader().read(data)
        assert (
            "measured_space.width_measurements.bottom is required and must be numeric"
            in raised.value.problems
        )
        assert "design_settings.base.height is required and must be numeric" in raised.value.problems

    def test_open_depth_requires_one_single_measurement(self) -> None:
        data = self.project.load_flat()
        del data["measured_space"]["depth_measurements"]["single"]
        with pytest.raises(OverallWardrobeInputError) as raised:
            OverallWardrobeInputReader().read(data)
        assert (
            "measured_space.depth_measurements.single is required and must be numeric"
            in raised.value.problems
        )

    def test_height_measurements_must_cover_the_usable_width(self) -> None:
        data = self.project.load_flat()
        data["measured_space"]["height_measurements"][-1]["distance_from_left"] = 2997
        with pytest.raises(OverallWardrobeInputError, match="cover the usable width"):
            OverallWardrobeInputReader().read(data)

    def test_top_boundary_kind_is_required(self) -> None:
        data = self.project.load_flat()
        del data["measured_space"]["top_boundary"]

        with pytest.raises(OverallWardrobeInputError, match="top_boundary"):
            OverallWardrobeInputReader().read(data)

    def test_each_fitted_dimension_must_be_confirmed(self) -> None:
        data = self.project.load_flat()
        data["design_settings"]["fitted_dimensions"]["width"] = None
        with pytest.raises(OverallWardrobeInputError) as raised:
            OverallWardrobeInputReader().read(data)
        assert (
            "design_settings.fitted_dimensions.width is required and must be true or false"
            in raised.value.problems
        )

    def test_centimetres_are_normalized_to_millimetres(self) -> None:
        data = self.project.load_flat()
        data["units"] = "cm"
        data["measured_space"]["width_measurements"] = dict.fromkeys(
            ("bottom", "middle", "top"), 300
        )
        data["measured_space"]["depth_measurements"] = {"single": 60}
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 240},
            {"distance_from_left": 150, "height_from_floor": 240},
            {"distance_from_left": 300, "height_from_floor": 240},
        ]
        data["design_settings"]["fit_allowance"] = 0.2
        for section, field in (("base", "height"), ("doors", "gap")):
            data["design_settings"][section][field] /= 10
        for field in (
            "left_clearance",
            "right_clearance",
            "cabinet_gap",
            "ceiling_clearance",
        ):
            data["design_settings"]["cabinet_run"][field] /= 10
        for field in data["design_settings"]["materials"]:
            data["design_settings"]["materials"][field] /= 10

        inputs = OverallWardrobeInputReader().read(data)

        assert inputs.space.width_measurements_mm == (3000.0, 3000.0, 3000.0)
        assert inputs.space.depth_measurements_mm == (600.0,)
        assert inputs.space.top_boundary.measurements[1].distance_from_left_mm == 1500.0
        assert inputs.settings.fit_allowance_mm == 2.0

    def test_client_statement_is_preserved_as_design_decision_evidence(self) -> None:
        data = self.project.load_flat()
        data["design_decisions"].append(
            {
                "subject": "front_outline.edge_C",
                "decision": "straight",
                "design_effect": "use_measured_endpoints",
                "client_statement": "Edge C is straight; use its endpoints.",
            }
        )

        inputs = OverallWardrobeInputReader().read(data)

        decision = next(
            item
            for item in inputs.design_decisions
            if item.subject == "front_outline.edge_C"
        )
        assert decision.subject == "front_outline.edge_C"
        assert decision.decision == "straight"
        assert decision.design_effect == "use_measured_endpoints"
        assert decision.client_statement == "Edge C is straight; use its endpoints."

    def test_design_decision_requires_a_client_statement(self) -> None:
        data = self.project.load_flat()
        data["design_decisions"].insert(
            0,
            {
                "subject": "front_outline.edge_C",
                "decision": "straight",
                "design_effect": "use_measured_endpoints",
            }
        )

        with pytest.raises(OverallWardrobeInputError) as raised:
            OverallWardrobeInputReader().read(data)

        assert (
            "design_decisions[0].client_statement is required and must be non-empty text"
            in raised.value.problems
        )
