"""Scope: Verify manual overall-wardrobe eval cases and calculated answer keys."""

from pathlib import Path

import pytest
import yaml

from overall_wardrobe_calculator import OverallWardrobeCalculator
from overall_wardrobe_inputs import OverallWardrobeInputReader


class TestOverallWardrobeEvalSet:
    """Keep model-eval cases complete and calculated answers aligned."""

    _EVAL_PATH = (
        Path(__file__).parents[1]
        / "evals"
        / "overall-wardrobe-measurements-and-settings.yaml"
    )
    def test_every_case_has_a_complete_final_answer(self) -> None:
        eval_set = self._load_eval_set()
        assert len(eval_set["cases"]) == 9
        for case in eval_set["cases"]:
            final_answer = case["turns"][-1]["answer_key"]
            assert final_answer["expected_aikea_yaml"]
            assert final_answer["expected_calculated"]

    def test_scoring_requires_numbered_named_client_questions(self) -> None:
        scoring = self._load_eval_set()["scoring"]
        pass_rules = " ".join(scoring["pass_when"])
        forbidden_rules = " ".join(scoring["always_forbidden"])

        assert "numbered line" in pass_rules
        assert "numbered choices" in pass_rules
        assert "plain name in parentheses" in pass_rules
        assert "ASCII guide" in pass_rules
        assert "description, colon, and where to measure" in pass_rules
        assert "one concrete next action" in pass_rules
        assert "only when their answer can change the design" in pass_rules
        assert "physical-design task" in pass_rules
        assert "why its result matters" in pass_rules
        assert "bare edge letter" in forbidden_rules
        assert "pretend value fields" in forbidden_rules
        assert "ready when you are" in forbidden_rules
        assert "AIkea skill or workflow" in forbidden_rules
        assert "canned example wording" in forbidden_rules

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

    def test_staged_case_labels_shape_before_asking_how_it_fits(self) -> None:
        eval_set = self._load_eval_set()
        case = next(
            case
            for case in eval_set["cases"]
            if case["name"] == "flat three-bay wardrobe supplied one topic at a time"
        )

        assert "centimetres, millimetres, and inches" in case["turns"][0][
            "answer_key"
        ]["response_required"][1]
        assert "shape of the available space" in case["turns"][1]["answer_key"][
            "response_required"
        ][1]
        assert "labelled clockwise" in case["turns"][2]["answer_key"][
            "response_required"
        ][0]
        assert "one question" in case["turns"][2]["answer_key"]["response_required"][
            1
        ]
        assert "finish flush" in case["turns"][3]["answer_key"]["response_required"][1]
        assert "labelled side edges A and C" in case["turns"][4]["answer_key"][
            "response_required"
        ][1]
        assert "same two walls" in case["turns"][4]["answer_key"][
            "response_required"
        ][2]
        assert "labelled location" in case["turns"][5]["answer_key"][
            "response_required"
        ][1]
        assert "floor edge D to top edge B" in case["turns"][6]["answer_key"][
            "response_required"
        ][1]
        final_yaml = case["turns"][-1]["answer_key"]["expected_aikea_yaml"]
        assert final_yaml["measured_space"]["depth_measurements"] == {"single": 620}

    def test_every_case_uses_the_depth_count_required_by_its_flush_line(self) -> None:
        for case in self._load_eval_set()["cases"]:
            final_yaml = case["turns"][-1]["answer_key"]["expected_aikea_yaml"]
            assert set(final_yaml["design_settings"]["fitted_dimensions"]) == {
                "width",
                "depth",
                "height",
            }
            expected_positions = (
                {"left", "middle", "right"}
                if final_yaml["design_settings"]["fitted_dimensions"]["depth"]
                else {"single"}
            )
            assert set(final_yaml["measured_space"]["depth_measurements"]) == (
                expected_positions
            )

    def test_flat_variation_case_uses_one_limiting_height(self) -> None:
        case = next(
            case
            for case in self._load_eval_set()["cases"]
            if case["name"] == "flat fitted ceiling with small measurement variation"
        )
        answer = case["turns"][-1]["answer_key"]

        assert answer["expected_aikea_yaml"]["measured_space"]["top_boundary"] == "flat"
        assert {
            cabinet["left_height_mm"]
            for cabinet in answer["expected_calculated"]["cabinets"]
        } == {2284}
        assert {
            cabinet["right_height_mm"]
            for cabinet in answer["expected_calculated"]["cabinets"]
        } == {2284}

    def _load_eval_set(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
