"""Scope: Verify exact answers for the four-unit revision model eval case."""

from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


class TestFourUnitRevisionEvalSet:
    """Keep the revision answer aligned with safe deterministic generation."""

    EVAL_PATH = Path(__file__).parents[1] / "evals/build-unit-taxonomy.yaml"

    def test_three_generated_units_revise_to_exact_four_unit_answer(
        self, tmp_path
    ) -> None:
        case = yaml.safe_load(self.EVAL_PATH.read_text(encoding="utf-8"))["cases"][1]
        project = case["starting_project"]["aikea_yaml"]
        answer = case["answer_key"]
        generator = AssemblyTaxonomyGenerator()
        generator.generate(project, tmp_path)
        previous_spec = (
            tmp_path / "assemblies/tall_storage_01/spec.py"
        ).read_text(encoding="utf-8")
        project["design_settings"]["assembly_run"]["assemblies"] = answer[
            "expected_assembly_run"
        ]

        result = generator.generate(project, tmp_path)

        storage = result.assemblies[:-1]
        assert [assembly.assembly_id for assembly in storage] == [
            item["id"] for item in answer["expected_storage_assemblies"]
        ]
        for assembly, expected in zip(
            storage, answer["expected_storage_assemblies"], strict=True
        ):
            assert assembly.global_left_mm == pytest.approx(expected["left_mm"])
            assert assembly.global_right_mm == pytest.approx(expected["right_mm"])
            assert assembly.width_mm == pytest.approx(expected["width_mm"])
        first_spec = tmp_path / "assemblies/tall_storage_01/spec.py"
        assert first_spec.read_text(encoding="utf-8") != previous_spec
        assert (tmp_path / "assemblies/tall_storage_04/builder.py").is_file()
        self._assert_base(result.assemblies[-1], answer["expected_base"])
        assert (tmp_path / answer["expected_generated_record"]).is_file()

    def _assert_base(self, base, expected) -> None:
        assert base.width_mm == expected["width_mm"]
        assert [(module.start_x_mm, module.end_x_mm) for module in base.modules] == [
            (pytest.approx(start), pytest.approx(end))
            for start, end in expected["module_spans_mm"]
        ]
        roles = [part.role for part in base.parts]
        assert roles.count("base_deck") == expected["deck_count"]
        assert roles.count("base_rail") == expected["rail_count"]
        assert roles.count("base_brace") == expected["brace_count"]
