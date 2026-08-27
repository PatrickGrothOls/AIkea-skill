"""Scope: Verify exact answers for the modular door-and-plinth eval set."""

from pathlib import Path

import yaml

from assembly_taxonomy_resolver import AssemblyTaxonomyResolver


class TestConfigureDoorAndPlinthEvalSet:
    """Keep all four design combinations aligned with deterministic taxonomy."""

    _EVAL = Path(__file__).parents[1] / "evals" / "configure-door-and-plinth-design.yaml"
    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def test_every_case_matches_its_exact_geometry_answer(self) -> None:
        eval_set = yaml.safe_load(self._EVAL.read_text(encoding="utf-8"))
        for case in eval_set["cases"]:
            project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
            inputs = case["resolved_input"]
            project["design_settings"]["doors"]["bottom"] = inputs["door_bottom"]
            project["design_settings"]["base"].update(
                {
                    "front": inputs["plinth_front"],
                    "recess": inputs["plinth_recess_mm"] / 10,
                }
            )

            taxonomy = AssemblyTaxonomyResolver().resolve(project)
            cabinet, base = taxonomy.assemblies[0], taxonomy.assemblies[-1]
            door = next(part for part in cabinet.parts if part.part_id == "door_panel")
            brace = next(part for part in base.parts if part.role == "base_brace")
            answer = case["answer_key"]

            assert cabinet.door_bottom_mm == answer["door_bottom_mm"]
            assert door.local_size_mm[1] == answer["door_height_mm"]
            assert base.plinth_recess_mm == answer["plinth_front_y_mm"]
            assert brace.local_size_mm[0] == answer["brace_depth_mm"]

    def test_scoring_preserves_independent_choices_and_full_depth_deck(self) -> None:
        scoring = yaml.safe_load(self._EVAL.read_text(encoding="utf-8"))["scoring"]
        passing = " ".join(scoring["pass_when"])
        forbidden = " ".join(scoring["always_forbidden"])

        assert "independent choices" in passing
        assert "overall project specification" in passing
        assert "full cabinet depth" in passing
        assert "Couple full-length doors" in forbidden
