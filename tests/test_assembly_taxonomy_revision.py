"""Scope: Verify safe regeneration when a project changes its unit count."""

from __future__ import annotations

from hashlib import sha256
import json

import pytest

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from generated_file_record import GeneratedFileRecord, GeneratedFileRecordError
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestAssemblyTaxonomyRevision:
    """Refresh untouched generated files while preserving local edits."""

    def setup_method(self) -> None:
        self.generator = AssemblyTaxonomyGenerator()
        self.projects = OverallWardrobeTestProject()

    def test_three_units_can_be_recalculated_as_four(self, tmp_path) -> None:
        self.generator.generate(self._project(3), tmp_path)
        first_spec = tmp_path / "assemblies/tall_storage_01/spec.py"
        previous_spec = first_spec.read_text(encoding="utf-8")

        result = self.generator.generate(self._project(4), tmp_path)

        assert [assembly.assembly_id for assembly in result.assemblies] == [
            "tall_storage_01",
            "tall_storage_02",
            "tall_storage_03",
            "tall_storage_04",
            "base_01",
        ]
        assert first_spec.read_text(encoding="utf-8") != previous_spec
        assert result.assemblies[0].width_mm == 747
        assert result.assemblies[3].global_right_mm == 2993
        assert (tmp_path / "assemblies/tall_storage_04/builder.py").is_file()
        base = result.assemblies[-1]
        assert [(module.start_x_mm, module.end_x_mm) for module in base.modules] == [
            (0, 1494),
            (1494, 2988),
        ]
        self._assert_record_matches(first_spec, tmp_path)

    def test_local_edit_blocks_the_complete_revision(self, tmp_path) -> None:
        self.generator.generate(self._project(3), tmp_path)
        record_path = tmp_path / GeneratedFileRecord.PATH
        previous_record = record_path.read_text(encoding="utf-8")
        local_spec = tmp_path / "assemblies/tall_storage_01/spec.py"
        local_spec.write_text("# client-owned local change\n", encoding="utf-8")

        with pytest.raises(AssemblyTaxonomyConflict, match="tall_storage_01/spec.py"):
            self.generator.generate(self._project(4), tmp_path)

        assert local_spec.read_text(encoding="utf-8") == "# client-owned local change\n"
        assert not (tmp_path / "assemblies/tall_storage_04").exists()
        assert record_path.read_text(encoding="utf-8") == previous_record

    def test_invalid_generated_file_record_stops_before_writing(self, tmp_path) -> None:
        record_path = tmp_path / GeneratedFileRecord.PATH
        record_path.parent.mkdir(parents=True)
        record_path.write_text("[]\n", encoding="utf-8")

        with pytest.raises(GeneratedFileRecordError, match="invalid object"):
            self.generator.generate(self._project(3), tmp_path)

        assert not (tmp_path / "assemblies/tall_storage_01").exists()

    def _project(self, unit_count: int) -> dict:
        data = self.projects.load_flat()
        run = data["design_settings"].pop("cabinet_run")
        data["design_settings"]["assembly_run"] = {
            "left_clearance": run["left_clearance"],
            "right_clearance": run["right_clearance"],
            "gap": run["cabinet_gap"],
            "ceiling_clearance": run["ceiling_clearance"],
            "assemblies": [
                {
                    "id": f"tall_storage_{index:02d}",
                    "purpose": "tall_storage",
                    "width_share": 1,
                }
                for index in range(1, unit_count + 1)
            ],
        }
        return data

    def _assert_record_matches(self, path, project_root) -> None:
        data = json.loads(
            (project_root / GeneratedFileRecord.PATH).read_text(encoding="utf-8")
        )
        relative = path.relative_to(project_root).as_posix()
        assert data["schema_version"] == 1
        assert data["files"][relative] == sha256(path.read_bytes()).hexdigest()
