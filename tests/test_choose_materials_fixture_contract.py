"""Scope: Validate material-eval fixtures and their expected project lifecycle."""

from pathlib import Path

import pytest
import yaml

from overall_wardrobe_inputs import OverallWardrobeInputReader


class OracleFixtureBoundary:
    """Resolve only expected outputs kept in the isolated expected directory."""

    def __init__(self, eval_dir: Path) -> None:
        self.eval_dir = eval_dir

    def expected_path(self, relative_path: str) -> Path:
        relative = Path(relative_path)
        expected_entry_root = self.eval_dir.resolve() / "expected"
        expected_root = expected_entry_root.resolve()
        target_path = (self.eval_dir / relative).resolve()
        if (
            relative.is_absolute()
            or relative.parts[:1] != ("expected",)
            or ".." in relative.parts
            or expected_entry_root != expected_root
            or expected_root not in target_path.parents
        ):
            raise ValueError("expected output must stay inside the expected directory")
        return target_path


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

        with pytest.raises(ValueError, match="inside the expected directory"):
            boundary.expected_path(
                "expected/../fixtures/choose-materials/unapproved/aikea.yaml"
            )

    def test_oracle_symlink_entry_cannot_live_in_fixture_tree(self, tmp_path) -> None:
        eval_dir = tmp_path / "evals"
        fixture = eval_dir / "fixtures" / "choose-materials" / "confirmation"
        expected = eval_dir / "expected.yaml"
        fixture.mkdir(parents=True)
        expected.write_text("status: hidden\n", encoding="utf-8")
        (fixture / "oracle-link.yaml").symlink_to(expected)

        with pytest.raises(ValueError, match="inside the expected directory"):
            OracleFixtureBoundary(eval_dir).expected_path(
                "fixtures/choose-materials/confirmation/oracle-link.yaml"
            )

    def test_oracle_path_rejects_case_insensitive_fixture_alias(self) -> None:
        boundary = OracleFixtureBoundary(self._EVAL_DIR)

        with pytest.raises(ValueError, match="inside the expected directory"):
            boundary.expected_path(
                "FIXTURES/choose-materials/confirmation/oracle-case.yaml"
            )

    def test_oracle_symlink_cannot_leave_expected_directory(self, tmp_path) -> None:
        eval_dir = tmp_path / "evals"
        expected_dir = eval_dir / "expected"
        fixture = eval_dir / "fixtures" / "choose-materials" / "oracle.yaml"
        expected_dir.mkdir(parents=True)
        fixture.parent.mkdir(parents=True)
        fixture.write_text("status: hidden\n", encoding="utf-8")
        (expected_dir / "oracle-link.yaml").symlink_to(fixture)

        with pytest.raises(ValueError, match="inside the expected directory"):
            OracleFixtureBoundary(eval_dir).expected_path(
                "expected/oracle-link.yaml"
            )

    def test_expected_directory_cannot_alias_fixture_tree(self, tmp_path) -> None:
        eval_dir = tmp_path / "evals"
        fixture = eval_dir / "fixtures" / "choose-materials" / "confirmation"
        fixture.mkdir(parents=True)
        (fixture / "oracle.yaml").write_text("status: hidden\n", encoding="utf-8")
        (eval_dir / "expected").symlink_to(fixture, target_is_directory=True)

        with pytest.raises(ValueError, match="inside the expected directory"):
            OracleFixtureBoundary(eval_dir).expected_path("expected/oracle.yaml")

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
