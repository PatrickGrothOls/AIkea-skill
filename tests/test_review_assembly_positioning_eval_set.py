"""Scope: Verify exact answers for the assembly-positioning model eval set."""

from pathlib import Path

import yaml


class TestReviewAssemblyPositioningEvalSet:
    """Keep the model-scoring case aligned with the checked physical result."""

    _EVAL_PATH = (
        Path(__file__).parents[1] / "evals" / "review-assembly-positioning.yaml"
    )

    def test_case_records_exact_local_and_global_positions(self) -> None:
        answer = self._load()["cases"][0]["answer_key"]

        assert answer["expected_status"] == "valid"
        assert answer["expected_assembly_positions"]["base_01"] == {
            "local_zero_mm": [0, 0, 0],
            "global_zero_mm": [10, 0, 0],
            "global_x_bounds_mm": [10, 2988],
            "global_z_bounds_mm": [0, 100],
        }
        assert answer["expected_assembly_positions"]["tall_storage_01"] == {
            "local_zero_mm": [0, 0, 0],
            "global_zero_mm": [10, 0, 0],
            "global_x_bounds_mm": [10, 1001.333333],
            "carcass_z_bounds_mm": [100, 2384],
        }
        assert answer["expected_relationships"] == {
            "base_top_z_mm": 100,
            "cabinet_side_bottom_z_mm": 100,
            "door_bottom": "plinth",
            "door_bottom_z_mm": 82,
            "plinth_front": "recessed",
            "plinth_recess_mm": 60,
            "plinth_front_y_mm": 60,
            "base_deck_bottom_z_mm": 82,
            "first_cabinet_right_x_global_mm": 1001.333333,
            "first_base_module_end_x_global_mm": 1002.333333,
            "first_base_module_projection_into_gap_mm": 1,
            "review_base_right_x_global_mm": 1002.333333,
            "next_cabinet_gap_mm": 2,
        }
        assert "brace_02_01" in answer["expected_absent_combined_nodes"]
        assert answer["expected_part_position"] == {
            "assembly_id": "tall_storage_01",
            "part_id": "left_side",
            "local_zero_mm": [0, 0, 0],
            "assembly_zero_mm": [0, 0, 100],
            "global_zero_mm": [10, 0, 100],
            "local_axes_in_assembly": {
                "x": [0, 1, 0],
                "y": [0, 0, 1],
                "z": [1, 0, 0],
            },
        }

    def test_scoring_requires_geometry_evidence_before_a_verdict(self) -> None:
        eval_set = self._load()
        pass_rules = " ".join(eval_set["scoring"]["pass_when"])
        forbidden = " ".join(eval_set["scoring"]["always_forbidden"])

        assert "deterministic assembly position check" in pass_rules
        assert "local zero" in pass_rules
        assert "axis directions" in pass_rules
        assert "width, depth, height, contact, and material overlap" in pass_rules
        assert "only the base module supporting the first cabinet" in pass_rules
        assert "neighbouring-module part" in pass_rules
        assert "screenshot alone" in forbidden
        assert "open-door review pose" in forbidden

        required = " ".join(eval_set["cases"][0]["answer_key"]["response_required"])
        assert "brace_02_01" in required
        assert "1 mm into the 2 mm cabinet gap" in required

    def _load(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
