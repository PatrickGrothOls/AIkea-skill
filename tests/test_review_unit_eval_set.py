"""Scope: Verify the first-unit visual review eval has exact artifact answers."""

from pathlib import Path

import yaml


class TestReviewUnitEvalSet:
    """Keep visual approval separate from repeated cabinet production."""

    _EVAL_PATH = Path(__file__).parents[1] / "evals" / "review-unit.yaml"

    def test_case_names_exact_first_assembly_artifacts(self) -> None:
        case = self._load()["cases"][0]
        answer = case["answer_key"]

        assert answer["expected_state"] == "awaiting_visual_approval"
        assert answer["expected_glb"] == (
            "assemblies/tall_storage_01/tall_storage_01.glb"
        )
        assert answer["expected_nodes"] == [
            "left_side",
            "right_side",
            "back_panel",
            "door_panel",
            "shelf_01",
            "shelf_02",
            "shelf_03",
            "top_panel_01",
        ]
        assert answer["expected_cadquery_bounds_mm"] == {
            "minimum": [-17, -989.333333, 0],
            "maximum": [991.333333, 582, 2384],
        }
        assert len(answer["expected_absent_glbs"]) == 2

    def test_scoring_requires_visual_decision_without_hidden_details(self) -> None:
        eval_set = self._load()
        pass_rules = " ".join(eval_set["scoring"]["pass_when"])
        forbidden = " ".join(eval_set["scoring"]["always_forbidden"])

        assert "one concrete visual-review question" in pass_rules
        assert "door is open" in pass_rules
        assert "Standard construction details remain internal" in pass_rules
        assert "remaining units before the first unit is visually approved" in forbidden
        assert "Cabineos" in forbidden

    def _load(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
