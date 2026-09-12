"""Scope: Exercise public startup commands without pytest's global module paths."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml


class TestConstructionStartupCommands:
    ROOT = Path(__file__).resolve().parents[1]

    def _run(self, *arguments):
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        return subprocess.run([sys.executable, "-B", *map(str, arguments)],
                              env=environment, capture_output=True, text=True, timeout=90)

    @pytest.mark.parametrize("fixture,count", (
        ("four-unit-review-aikea.yaml", 4), ("review-unit-aikea.yaml", 3)))
    def test_overall_cli_accepts_saved_run_without_rewriting_it(self, tmp_path, fixture, count):
        source = self.ROOT / "tests/fixtures" / fixture
        target = tmp_path / "aikea.yaml"
        target.write_bytes(source.read_bytes())
        result = self._run(self.ROOT / "aikea/scripts/calculate_overall_wardrobe.py", target)
        assert result.returncode == 0, result.stdout + result.stderr
        assert len(json.loads(result.stdout)["calculated"]["cabinets"]) == count
        assert target.read_bytes() == source.read_bytes()

    def test_invalid_assembly_run_reports_its_real_problem(self, tmp_path):
        project = yaml.safe_load((self.ROOT / "tests/fixtures/four-unit-review-aikea.yaml").read_text())
        run = project["design_settings"]["assembly_run"]
        run["assemblies"][1]["id"] = run["assemblies"][0]["id"]
        target = tmp_path / "aikea.yaml"
        target.write_text(yaml.safe_dump(project))
        result = self._run(self.ROOT / "aikea/scripts/calculate_overall_wardrobe.py", target)
        assert result.returncode == 2
        assert "assembly_run assembly ids must be unique" in json.loads(result.stdout)["problems"]

    def test_door_and_full_review_bootstrap_their_own_dependencies(self):
        for script, module, expression in (
            ("aikea-build-doors/scripts/generate_door_hinge_review.py",
             "cabinet_door_hinge_review_generator", "CabinetDoorHingeReviewGenerator()"),
            ("aikea-review-unit/scripts/generate_full_wardrobe_review.py",
             "full_wardrobe_review_generator", "FullWardrobeReviewGenerator()"),
        ):
            code = (f"import runpy, sys; sys.path.insert(0, {str((self.ROOT / script).parent)!r}); "
                    f"runpy.run_path({str(self.ROOT / script)!r}); "
                    f"from {module} import {expression.split('(')[0]}; {expression}")
            result = self._run("-c", code)
            assert result.returncode == 0, result.stdout + result.stderr
