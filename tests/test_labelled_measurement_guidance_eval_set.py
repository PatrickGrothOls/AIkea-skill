"""Scope: Verify labelled-measurement guidance eval cases and answer keys."""

from pathlib import Path

import yaml


class TestLabelledMeasurementGuidanceEvalSet:
    """Keep adaptive measurement guidance cases complete and scoreable."""

    _EVAL_PATH = (
        Path(__file__).parents[1]
        / "evals"
        / "labelled-measurement-guidance.yaml"
    )

    def test_cases_define_useful_next_questions(self) -> None:
        eval_set = self._load_eval_set()

        assert len(eval_set["cases"]) == 5
        for case in eval_set["cases"]:
            assert case["established_outline"]
            assert case["chat_history"]
            assert case["next_user_message"]
            assert case["answer_key"]["response_required"]
            assert case["answer_key"]["response_forbidden"]
            assert all(
                label in case["established_outline"]
                for label in ("A (", "B (", "C (", "D (")
            )

    def test_measurement_cases_require_numbered_named_lines(self) -> None:
        measurement_cases = self._load_eval_set()["cases"][:3]

        for case in measurement_cases:
            required = " ".join(case["answer_key"]["response_required"])
            assert "numbered" in required
            assert "(" in required and ")" in required
            assert "reply with the item numbers" in required
            assert "headline" in required
            assert "ASCII guide" in required
            assert "colon, and where to measure" in required

    def test_measurement_prompts_forbid_fake_value_fields(self) -> None:
        forbidden = " ".join(self._load_eval_set()["scoring"]["always_forbidden"])

        assert "pretend value fields" in forbidden
        assert "Mix width, height, and depth" in forbidden

    def test_width_choice_case_requires_numbered_reply_options(self) -> None:
        width_choice = next(
            case
            for case in self._load_eval_set()["cases"]
            if case["name"] == "offer numbered cabinet-width choices"
        )

        required = " ".join(width_choice["answer_key"]["response_required"])
        assert "numbered choices" in required
        assert "reply with only the option number" in required

    def test_confirmed_slope_has_a_design_decision_answer(self) -> None:
        confirmed_slope = next(
            case
            for case in self._load_eval_set()["cases"]
            if case["name"] == "accept a client-confirmed straight slope"
        )

        assert confirmed_slope["answer_key"]["expected_design_decision"] == {
            "subject": "front_outline.edge_C",
            "decision": "straight",
            "design_effect": "use_measured_endpoints",
            "client_statement": (
                "Edge C is straight. Use its endpoints; another reading there would "
                "be impractical."
            ),
        }

    def _load_eval_set(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
