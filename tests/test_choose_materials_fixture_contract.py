"""Scope: Validate material-eval fixtures and their expected project lifecycle."""

from pathlib import Path

import pytest
import yaml

from overall_wardrobe_inputs import OverallWardrobeInputReader


class OracleFixtureBoundary:
    """Resolve an expected output only when copied fixtures cannot expose it."""

    def __init__(self, eval_dir: Path) -> None:
        self.eval_dir = eval_dir

    def expected_path(self, relative_path: str) -> Path:
        fixture_root = (self.eval_dir / "fixtures" / "choose-materials").resolve()
        expected_path = (self.eval_dir / relative_path).resolve()
        if fixture_root in expected_path.parents:
            raise ValueError("expected output must be outside copied fixtures")
        return expected_path


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
                expected_path = OracleFixtureBoundary(self._EVAL_DIR).expected_path(
                    expected
                )
                yaml.safe_load(expected_path.read_text(encoding="utf-8"))
            for evidence in setup.get("evidence_files", []):
                assert (self._EVAL_DIR / evidence["source"]).is_file()
            for attachment in setup.get("attachments", []):
                assert (self._EVAL_DIR / attachment).is_file()

    def test_oracle_path_cannot_traverse_into_fixture_tree(self) -> None:
        boundary = OracleFixtureBoundary(self._EVAL_DIR)

        with pytest.raises(ValueError, match="outside copied fixtures"):
            boundary.expected_path(
                "expected/../fixtures/choose-materials/unapproved/aikea.yaml"
            )

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
