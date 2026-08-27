"""Scope: Verify the unit-taxonomy command's file and JSON boundary."""

from __future__ import annotations

import json
from pathlib import Path
from shutil import copyfile

from generate_unit_taxonomy import UnitTaxonomyCommand


class TestGenerateUnitTaxonomyCommand:
    """Run the same command used by the build-units skill."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "flat-assembly-run-aikea.yaml"

    def test_valid_project_generates_units_and_reports_paths(
        self, tmp_path, capsys
    ) -> None:
        project_file = tmp_path / "aikea.yaml"
        copyfile(self._FIXTURE, project_file)

        status = UnitTaxonomyCommand().run(project_file)
        output = json.loads(capsys.readouterr().out)

        assert status == 0
        assert output == {
            "status": "generated",
            "assemblies": [
                {"id": f"tall_storage_{index:02d}", "path": f"assemblies/tall_storage_{index:02d}"}
                for index in range(1, 4)
            ] + [{"id": "base_01", "path": "assemblies/base_01"}],
        }
        assert (tmp_path / "assemblies" / "tall_storage_03" / "builder.py").is_file()
        assert (tmp_path / "assemblies" / "base_01" / "builder.py").is_file()
