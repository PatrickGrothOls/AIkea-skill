"""Scope: Verify known generated metadata builders upgrade without data loss."""

from __future__ import annotations

from pathlib import Path

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestAssemblyTaxonomyUpgrade:
    """Upgrade only the exact earlier generated builder scaffold."""

    def setup_method(self) -> None:
        self.generator = AssemblyTaxonomyGenerator()
        self.project = OverallWardrobeTestProject()

    def test_metadata_builders_upgrade_to_executable_builders(self, tmp_path) -> None:
        data = self._one_unit_project()
        taxonomy = self.generator.generate(data, tmp_path)
        metadata_files = self.generator.renderer.render_metadata_scaffold(taxonomy)
        for relative, content in metadata_files.items():
            (tmp_path / relative).write_text(content, encoding="utf-8")

        self.generator.generate(data, tmp_path)

        part_builder = (
            tmp_path
            / "assemblies/tall_storage_01/parts/left_side/builder.py"
        ).read_text(encoding="utf-8")
        specification = (
            tmp_path / "assemblies/specification.py"
        ).read_text(encoding="utf-8")
        assert "SheetPartBuilder().build(SPEC, cuts)" in part_builder
        assert "BuiltPart," in specification
        assert "class PartBuildPlan" not in specification

    def test_untouched_pre_shelf_taxonomy_receives_generated_shelf_parts(
        self, tmp_path
    ) -> None:
        data = self._one_unit_project()
        taxonomy = self.generator.resolver.resolve(data)
        previous_files = self.generator.renderer.render_without_adjustable_shelves(
            taxonomy
        )
        self._write(tmp_path, previous_files)

        self.generator.generate(data, tmp_path)

        spec = (tmp_path / "assemblies/tall_storage_01/spec.py").read_text(
            encoding="utf-8"
        )
        assert "part_id='shelf_01'" in spec
        assert (
            tmp_path / "assemblies/tall_storage_01/parts/shelf_03/builder.py"
        ).is_file()

    def _write(self, root: Path, files: dict[Path, str]) -> None:
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def _one_unit_project(self) -> dict:
        data = self.project.load_flat()
        run = data["design_settings"].pop("cabinet_run")
        data["design_settings"]["assembly_run"] = {
            "left_clearance": run["left_clearance"],
            "right_clearance": run["right_clearance"],
            "gap": run["cabinet_gap"],
            "ceiling_clearance": run["ceiling_clearance"],
            "assemblies": [
                {
                    "id": "tall_storage_01",
                    "purpose": "tall_storage",
                    "width_share": 1,
                }
            ],
        }
        return data
