"""Scope: Verify exact structural-base eval answers against deterministic output."""

from pathlib import Path

import yaml

from base_taxonomy_builder import BaseTaxonomyBuilder


class TestBuildStructuralBaseEvalSet:
    """Keep current and oversize base answers aligned with the planner."""

    _EVAL_PATH = Path(__file__).parents[1] / "evals" / "build-structural-base.yaml"

    def test_every_case_matches_its_exact_answer(self) -> None:
        eval_set = yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
        for case in eval_set["cases"]:
            inputs = case["resolved_input"]
            answer = case["answer_key"]
            base = BaseTaxonomyBuilder().build(
                tuple(tuple(span) for span in inputs["cabinet_spans_mm"]),
                inputs["depth_mm"],
                inputs["height_mm"],
                inputs["panel_thickness_mm"],
                "flush",
                0.0,
            )
            assert base.width_mm == answer["width_mm"]
            self._assert_modules(base, answer["modules"])
            self._assert_parts(base, answer)

    def _assert_modules(self, base, expected_modules: list[dict]) -> None:
        assert [
            (module.module_id, module.start_x_mm, module.end_x_mm)
            for module in base.modules
        ] == [
            (item["id"], item["start_x_mm"], item["end_x_mm"])
            for item in expected_modules
        ]

    def _assert_parts(self, base, answer: dict) -> None:
        roles = [part.role for part in base.parts]
        assert roles.count("base_deck") == answer["deck_count"]
        assert roles.count("base_rail") == answer["rail_count"]
        if "brace_count" in answer:
            assert roles.count("base_brace") == answer["brace_count"]
        assert {
            part.local_size_mm[1]
            for part in base.parts
            if part.role in {"base_rail", "base_brace"}
        } == {answer["support_height_mm"]}
        assert {
            part.local_size_mm[0]
            for part in base.parts
            if part.role == "base_brace"
        } == {answer["clear_depth_mm"]}
        assert len(
            [joint for joint in base.joints if joint.purpose == "base_module_seam"]
        ) == answer["module_seam_count"]
