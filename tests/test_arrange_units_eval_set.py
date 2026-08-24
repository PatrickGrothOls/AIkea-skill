"""Scope: Verify arrange-units eval cases and exact assembly-run answers."""

from pathlib import Path

import yaml


class TestArrangeUnitsEvalSet:
    """Keep unit-arrangement model scoring complete and unambiguous."""

    _EVAL_PATH = Path(__file__).parents[1] / "evals" / "arrange-units.yaml"

    def test_cases_cover_complete_missing_and_revision_behaviour(self) -> None:
        cases = self._load_eval_set()["cases"]

        assert len(cases) == 6
        assert {case["name"] for case in cases} == {
            "three equal tall-storage units",
            "bench between matching tall-storage units",
            "mixed arrangement beneath a sloped room boundary",
            "ask only for the missing width relationship",
            "revise one width relationship without replacing stable IDs",
            "acknowledgement continues a completed arrangement",
        }

    def test_complete_cases_have_exact_valid_assembly_runs(self) -> None:
        complete_cases = [
            case
            for case in self._load_eval_set()["cases"]
            if "expected_assembly_run" in case["answer_key"]
        ]

        assert len(complete_cases) == 5
        for case in complete_cases:
            assembly_run = case["answer_key"]["expected_assembly_run"]
            assemblies = assembly_run["assemblies"]
            assert set(assembly_run) == {
                "left_clearance",
                "right_clearance",
                "gap",
                "ceiling_clearance",
                "assemblies",
            }
            assert len({assembly["id"] for assembly in assemblies}) == len(assemblies)
            for assembly in assemblies:
                assert set(assembly) == {"id", "purpose", "width_share"}
                assert assembly["id"]
                assert assembly["purpose"]
                assert assembly["width_share"] > 0

    def test_eval_forbids_internal_and_later_stage_questions(self) -> None:
        forbidden = " ".join(self._load_eval_set()["scoring"]["always_forbidden"])

        for required_phrase in (
            "internal IDs",
            "width shares",
            "bench height",
            "Cabineos",
            "assembly folders",
            "cabinet_run",
            "ready when you are",
        ):
            assert required_phrase in forbidden

    def test_revision_preserves_stable_ids(self) -> None:
        revision = next(
            case
            for case in self._load_eval_set()["cases"]
            if case["name"]
            == "revise one width relationship without replacing stable IDs"
        )
        before = revision["starting_project"]["design_settings"]["assembly_run"]
        after = revision["answer_key"]["expected_assembly_run"]

        assert [item["id"] for item in before["assemblies"]] == [
            item["id"] for item in after["assemblies"]
        ]
        assert [item["purpose"] for item in before["assemblies"]] == [
            item["purpose"] for item in after["assemblies"]
        ]
        assert [item["width_share"] for item in before["assemblies"]] == [1, 0.5, 1]
        assert [item["width_share"] for item in after["assemblies"]] == [1, 1, 1]

    def test_acknowledgement_case_requires_an_actionable_handoff(self) -> None:
        acknowledgement = next(
            case
            for case in self._load_eval_set()["cases"]
            if case["name"] == "acknowledgement continues a completed arrangement"
        )
        required = " ".join(acknowledgement["answer_key"]["response_required"])
        forbidden = " ".join(acknowledgement["answer_key"]["response_forbidden"])

        assert "permission to continue" in required
        assert "left unit" in required
        assert "what it needs to store" in required
        assert "ready when you are" in forbidden

    def _load_eval_set(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
