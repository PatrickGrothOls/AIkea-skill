"""Scope: Validate the material-inference eval set's scoring contract and coverage."""

from pathlib import Path

import yaml


class TestChooseMaterialsEvalSet:
    """Keep ordinary-language inference cases complete and independently scorable."""

    _EVAL_PATH = Path(__file__).parents[1] / "evals" / "choose-materials.yaml"
    _EXPECTED_CASE_IDS = {
        "appearance_reference_image",
        "bathroom_splash_exposure",
        "built_legacy_material_migration",
        "built_project_revision",
        "cheapest_missing_market",
        "confirm_split_material_system",
        "family_entryway_wear",
        "hostile_supplier_source",
        "large_art_book_load",
        "legacy_thicknesses_unapproved",
        "ordinary_bedroom_appearance",
        "split_painted_doors",
        "tight_stair_access",
    }
    _REQUIRED_COVERAGE = {
        "appearance",
        "bounded_inference",
        "confirmation",
        "finished_cost",
        "geometry",
        "handling",
        "load",
        "legacy_routing",
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

    def test_case_identities_are_locked(self) -> None:
        cases = self._load()["cases"]

        assert {case["id"] for case in cases} == self._EXPECTED_CASE_IDS
        assert len({case["name"] for case in cases}) == len(cases)

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

    def test_recovery_cases_lock_revision_legacy_and_exception_behavior(self) -> None:
        cases = {case["name"]: case for case in self._load()["cases"]}

        assert (
            cases["built project keeps a changed material as proposal only"]
            ["answer_key"]["expected_project_state"]
            == "material_revision_blocked"
        )
        assert (
            cases["legacy thicknesses do not prove material approval"]
            ["answer_key"]["expected_project_state"]
            == "material_decision_open"
        )
        book_case = cases["large art books imply a shelf-structure check"]
        required = " ".join(book_case["answer_key"]["response_required"])
        assert "unresolved-material blocker" in required
        assert (
            self._cases_by_id()["built_legacy_material_migration"]["answer_key"]
            ["expected_project_state"]
            == "material_migration_blocked"
        )

    def _cases_by_id(self) -> dict[str, dict]:
        return {case["id"]: case for case in self._load()["cases"]}

    def _load(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
