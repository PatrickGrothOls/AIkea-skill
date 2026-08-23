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

        assert len(eval_set["cases"]) == 4
        for case in eval_set["cases"]:
            assert case["established_outline"]
            assert case["chat_history"]
            assert case["next_user_message"]
            assert case["answer_key"]["response_required"]
            assert case["answer_key"]["response_forbidden"]
            scored_text = " ".join(
                case["answer_key"]["response_required"]
                + case["answer_key"]["response_forbidden"]
            )
            assert any(label in scored_text for label in ("A", "B", "C", "D", "E"))

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
