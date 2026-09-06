"""Scope: Verify exact answers for the full-wardrobe model eval set."""

from pathlib import Path

import yaml


class TestReviewFullWardrobeEvalSet:
    """Keep the manual scoring answer aligned with the generated full run."""

    _EVAL = Path(__file__).parents[1] / "evals" / "review-full-wardrobe.yaml"

    def test_case_records_the_complete_position_answer(self) -> None:
        answer = self._load()["cases"][0]["answer_key"]

        assert answer["expected_status"] == "valid"
        assert answer["expected_base_global_x_mm"] == [10, 2988]
        assert [item["id"] for item in answer["expected_cabinets"]] == [
            "tall_storage_01",
            "tall_storage_02",
            "tall_storage_03",
        ]
        assert answer["expected_gaps_mm"] == [2, 2]
        assert answer["expected_plinth"] == {
            "front": "recessed",
            "recess_mm": 60,
            "top_z_mm": 100,
        }

    def test_scoring_requires_generated_builders_and_position_evidence(self) -> None:
        scoring = self._load()["scoring"]
        passing = " ".join(scoring["pass_when"])
        forbidden = " ".join(scoring["always_forbidden"])

        assert "every generated cabinet builder" in passing
        assert "doors closed" in passing
        assert "position report" in passing
        assert "simplified cabinet boxes" in forbidden
        assert "guessed positions" in forbidden

    def test_open_door_case_preserves_the_physical_position_report(self) -> None:
        answer = self._load()["cases"][1]["answer_key"]

        assert answer["expected_artifact"] == (
            "assemblies/full_wardrobe_open_review.glb"
        )
        assert answer["expected_report"] == (
            "assemblies/full-wardrobe-position-check.json"
        )
        assert answer["expected_door_state"] == "open"
        assert answer["expected_open_doors"] == [
            "tall_storage_01__door_panel",
            "tall_storage_02__door_panel",
            "tall_storage_03__door_panel",
        ]

    def test_independent_door_case_has_exact_module_states(self) -> None:
        answer = self._load()["cases"][2]["answer_key"]

        assert answer["expected_artifact"] == (
            "assemblies/full_wardrobe_door_states_review.glb"
        )
        assert answer["expected_door_states"] == {
            "tall_storage_01": "open",
            "tall_storage_02": "removed",
            "tall_storage_03": "removed",
        }
        assert answer["expected_visible_doors"] == [
            "tall_storage_01__door_panel"
        ]

    def _load(self) -> dict:
        return yaml.safe_load(self._EVAL.read_text(encoding="utf-8"))
