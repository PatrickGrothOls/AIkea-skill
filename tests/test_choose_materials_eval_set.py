"""Scope: Validate the material-inference eval set's scoring contract and coverage."""

from pathlib import Path

import yaml


class TestChooseMaterialsEvalSet:
    """Keep ordinary-language inference cases complete and independently scorable."""

    _EVAL_PATH = Path(__file__).parents[1] / "evals" / "choose-materials.yaml"
    _REQUIRED_COVERAGE = {
        "appearance",
        "bounded_inference",
        "confirmation",
        "finished_cost",
        "geometry",
        "handling",
        "load",
        "ordinary_intake",
        "persistence",
        "price",
        "revision_safety",
        "source_trust",
        "technical_evidence",
        "visual_evidence",
        "water_exposure",
        "wear",
    }

    def test_every_case_has_a_hidden_inference_key(self) -> None:
        for case in self._load()["cases"]:
            inference_key = case["answer_key"]["inference_key"]

            assert inference_key["required"]
            assert inference_key["forbidden"]
            assert case["answer_key"]["response_required"]
            assert case["answer_key"]["response_forbidden"]

    def test_cases_cover_the_material_decisions_the_model_must_infer(self) -> None:
        coverage = {
            category
            for case in self._load()["cases"]
            for category in case["coverage"]
        }

        assert self._REQUIRED_COVERAGE <= coverage

    def test_global_rules_prohibit_technical_questions_and_image_overclaiming(self) -> None:
        scoring = self._load()["scoring"]
        pass_rules = " ".join(scoring["pass_when"])
        forbidden_rules = " ".join(scoring["always_forbidden"])

        assert "observe or decide" in pass_rules
        assert "physical sample" in pass_rules
        assert "moisture class" in forbidden_rules
        assert "from an image" in forbidden_rules
        assert "instructions embedded" in forbidden_rules

    def _load(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
