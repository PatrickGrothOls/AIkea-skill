"""Scope: Verify deterministic local unit taxonomy generation."""

from __future__ import annotations

import importlib
import sys

import pytest

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestAssemblyTaxonomyGenerator:
    """Generate populated unit folders from one checked assembly run."""

    def setup_method(self) -> None:
        self.generator = AssemblyTaxonomyGenerator()
        self.project = OverallWardrobeTestProject()

    def test_three_units_receive_complete_local_taxonomies(self, tmp_path) -> None:
        result = self.generator.generate(self._three_unit_project(), tmp_path)

        assert [item.assembly_id for item in result.assemblies] == [
            "tall_storage_01",
            "tall_storage_02",
            "tall_storage_03",
            "base_01",
        ]
        assert result.assemblies[0].global_left_mm == 5
        assert result.assemblies[0].global_right_mm == 1001
        assert result.assemblies[0].width_mm == 996
        assert [(point.x_mm, point.height_mm) for point in result.assemblies[0].top] == [
            (0, 2298),
            (996, 2298),
        ]

        unit = tmp_path / "assemblies" / "tall_storage_01"
        expected_files = {
            unit / "spec.py",
            unit / "builder.py",
            unit / "joints" / "spec.py",
        }
        for part_id in (
            "left_side",
            "right_side",
            "back_panel",
            "door_panel",
            "shelf_01",
            "shelf_02",
            "shelf_03",
            "top_panel_01",
        ):
            expected_files.add(unit / "parts" / part_id / "spec.py")
            expected_files.add(unit / "parts" / part_id / "builder.py")
        assert all(path.is_file() for path in expected_files)

        spec = self._load_generated_spec(tmp_path, "tall_storage_01")
        assert spec.assembly_id == "tall_storage_01"
        door = spec.part("door_panel")
        assert dict(door.dimensions_mm)["left_height"] == 2398
        assert spec.base_height_mm == 100
        assert [(point.x_mm, point.height_mm) for point in door.outline_mm] == [
            (0, 0),
            (994, 0),
            (994, 2398),
            (0, 2398),
        ]
        assert spec.joints
        part_builder = (
            unit / "parts" / "left_side" / "builder.py"
        ).read_text(encoding="utf-8")
        assembly_builder = (unit / "builder.py").read_text(encoding="utf-8")
        assert "SheetPartBuilder().build(SPEC, cuts)" in part_builder
        assert "LEFT_SIDE_BUILDER.build(cuts.for_part('left_side'))" in assembly_builder
        assert "BuiltAssembly" in assembly_builder

        base = result.assemblies[-1]
        assert base.width_mm == 2988
        assert len(base.modules) == 2
        base_root = tmp_path / "assemblies" / "base_01"
        assert (base_root / "spec.py").is_file()
        assert (base_root / "builder.py").is_file()
        assert all(
            (base_root / "parts" / part.part_id / "spec.py").is_file()
            and (base_root / "parts" / part.part_id / "builder.py").is_file()
            for part in base.parts
        )

    def test_local_boundary_preserves_a_change_inside_one_unit(self, tmp_path) -> None:
        data = self._three_unit_project()
        data["measured_space"]["top_boundary"] = "measured_profile"
        data["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 2400},
            {"distance_from_left": 750, "height_from_floor": 2400},
            {"distance_from_left": 3000, "height_from_floor": 1800},
        ]

        result = self.generator.generate(data, tmp_path)

        first = result.assemblies[0]
        assert [(point.x_mm, point.height_mm) for point in first.top] == [
            (0, 2298),
            (745, 2298),
            (996, pytest.approx(2231.066667)),
        ]
        door = next(part for part in first.parts if part.part_id == "door_panel")
        assert [(point.x_mm, point.height_mm) for point in door.outline_mm] == [
            (0, 0),
            (994, 0),
            (994, pytest.approx(2331.333333)),
            (744, 2398),
            (0, 2398),
        ]
        assert (tmp_path / "assemblies" / "tall_storage_01" / "parts" / "top_panel_02").is_dir()

    def test_changed_generated_file_is_reported_without_overwriting(self, tmp_path) -> None:
        data = self._three_unit_project()
        self.generator.generate(data, tmp_path)
        local_spec = tmp_path / "assemblies" / "tall_storage_01" / "spec.py"
        local_spec.write_text("# client-owned local change\n", encoding="utf-8")

        with pytest.raises(AssemblyTaxonomyConflict, match="tall_storage_01/spec.py"):
            self.generator.generate(data, tmp_path)

        assert local_spec.read_text(encoding="utf-8") == "# client-owned local change\n"

    def test_identical_generated_taxonomy_can_be_checked_again(self, tmp_path) -> None:
        data = self._three_unit_project()

        first = self.generator.generate(data, tmp_path)
        second = self.generator.generate(data, tmp_path)

        assert second == first

    def _three_unit_project(self) -> dict:
        data = self.project.load_flat()
        run = data["design_settings"].pop("cabinet_run")
        data["design_settings"]["assembly_run"] = {
            "left_clearance": run["left_clearance"],
            "right_clearance": run["right_clearance"],
            "gap": run["cabinet_gap"],
            "ceiling_clearance": run["ceiling_clearance"],
            "assemblies": [
                {"id": f"tall_storage_{index:02d}", "purpose": "tall_storage", "width_share": 1}
                for index in range(1, 4)
            ],
        }
        return data

    def _load_generated_spec(self, project_root, assembly_id: str):
        sys.path.insert(0, str(project_root))
        try:
            module = importlib.import_module(f"assemblies.{assembly_id}.spec")
            return module.SPEC
        finally:
            sys.path.remove(str(project_root))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
