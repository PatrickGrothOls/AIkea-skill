"""Scope: Validate material-eval fixtures and their expected project lifecycle."""

from pathlib import Path

import yaml

from overall_wardrobe_inputs import OverallWardrobeInputReader


class TestChooseMaterialsFixtureContract:
    """Keep material eval seeds isolated, valid, and reproducible."""

    _EVAL_DIR = Path(__file__).parents[1] / "evals"
    _EVAL_PATH = _EVAL_DIR / "choose-materials.yaml"

    def test_every_case_has_replayable_inputs(self) -> None:
        for case in self._load()["cases"]:
            assert "starting_project" not in case
            setup = case["setup"]
            project = self._EVAL_DIR / setup["project_fixture"]
            assert project.is_dir()
            project_data = yaml.safe_load(
                (project / "aikea.yaml").read_text(encoding="utf-8")
            )
            assert "cabinet_run" in project_data["design_settings"]
            assert "assembly_run" not in project_data["design_settings"]

            expected = setup["expected_aikea_yaml"]
            if expected != "unchanged":
                fixture_root = self._EVAL_DIR / "fixtures" / "choose-materials"
                assert fixture_root not in (self._EVAL_DIR / expected).parents
                yaml.safe_load(
                    (self._EVAL_DIR / expected).read_text(encoding="utf-8")
                )
            for evidence in setup.get("evidence_files", []):
                assert (self._EVAL_DIR / evidence["source"]).is_file()
            for attachment in setup.get("attachments", []):
                assert (self._EVAL_DIR / attachment).is_file()

    def test_confirmation_case_locks_exact_supported_materials(self) -> None:
        case = self._cases_by_id()["confirm_split_material_system"]
        expected_path = self._EVAL_DIR / case["setup"]["expected_aikea_yaml"]
        expected = yaml.safe_load(expected_path.read_text(encoding="utf-8"))
        OverallWardrobeInputReader().read(expected)

        assert [
            decision["subject"] for decision in expected["design_decisions"]
        ] == [
            "cabinet_carcass_material",
            "door_front_material",
            "back_panel_material",
        ]
        assert expected["design_settings"]["materials"] == {
            "cabinet_panel_thickness": 18,
            "door_thickness": 19,
            "back_panel_thickness": 9,
        }

    def _cases_by_id(self) -> dict[str, dict]:
        return {case["id"]: case for case in self._load()["cases"]}

    def _load(self) -> dict:
        return yaml.safe_load(self._EVAL_PATH.read_text(encoding="utf-8"))
