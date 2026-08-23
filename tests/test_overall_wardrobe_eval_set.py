"""Scope: Verify that manual overall-wardrobe eval answers are complete and calculable."""

from pathlib import Path

import pytest
import yaml

from overall_wardrobe_calculator import OverallWardrobeCalculator
from overall_wardrobe_inputs import OverallWardrobeInputReader


class TestOverallWardrobeEvalSet:
    """Keep manual model-eval answer keys aligned with deterministic calculations."""

    _EVAL_PATH = (
        Path(__file__).parents[1]
        / "evals"
        / "overall-wardrobe-measurements-and-settings.yaml"
    )

    def test_every_case_has_a_complete_final_answer(self) -> None:
        eval_set = self._load_eval_set()
        assert len(eval_set["cases"]) == 8
        for case in eval_set["cases"]:
            final_answer = case["turns"][-1]["answer_key"]
            assert final_answer["expected_aikea_yaml"]
            assert final_answer["expected_calculated"]

    def test_every_final_answer_matches_the_calculator(self) -> None:
        eval_set = self._load_eval_set()
        for case in eval_set["cases"]:
            answer = case["turns"][-1]["answer_key"]
            inputs = OverallWardrobeInputReader().read(answer["expected_aikea_yaml"])
            actual = OverallWardrobeCalculator().calculate(inputs).as_dict()
            expected = answer["expected_calculated"]
            for field in (
                "minimum_measured_width_mm",
                "minimum_measured_depth_mm",
                "width_fitting_allowance_mm",
                "depth_fitting_allowance_mm",
                "height_fitting_allowance_mm",
                "usable_width_mm",
                "usable_depth_mm",
                "cabinet_depth_mm",
                "inside_depth_mm",
            ):
                assert actual[field] == pytest.approx(expected[field]), case["name"]
            assert len(actual["cabinets"]) == len(expected["cabinets"])
            for actual_cabinet, expected_cabinet in zip(
                actual["cabinets"], expected["cabinets"], strict=True
            ):
                assert actual_cabinet.keys() == expected_cabinet.keys()
                for field, value in actual_cabinet.items():
                    assert value == pytest.approx(expected_cabinet[field]), (
                        case["name"],
                        field,
                    )

    def test_staged_case_learns_the_installation_before_dimensions(self) -> None:
        eval_set = self._load_eval_set()
        case = next(
            case
            for case in eval_set["cases"]
            if case["name"] == "flat three-bay wardrobe supplied one topic at a time"
        )

        assert "centimetres, millimetres, and inches" in case["turns"][0][
            "answer_key"
        ]["response_required"][1]
        assert "fixed walls" in case["turns"][1]["answer_key"]["response_required"][1]
        assert "reaches the ceiling" in case["turns"][2]["answer_key"][
            "response_required"
        ][1]
        assert "open at the front" in case["turns"][3]["answer_key"][
            "response_required"
        ][1]
        assert "one depth" in case["turns"][5]["answer_key"]["response_required"][
            1
        ]
        final_yaml = case["turns"][-1]["answer_key"]["expected_aikea_yaml"]
        assert final_yaml["measured_space"]["depth_measurements"] == {"single": 620}

    def _load_eval_set(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
