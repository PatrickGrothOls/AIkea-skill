"""Scope: Verify one cabinet owns its generated drawer layout and child modules."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_generator import CabinetDrawerGenerator
from cabinet_drawer_plan import DrawerLayout


class TestCabinetDrawerGenerator(unittest.TestCase):
    """Protect local ownership and the 500 mm runner selection for cabinet one."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_generates_a_child_under_the_existing_first_cabinet(self) -> None:
        temporary_directory = TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        project_root = Path(temporary_directory.name)
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        source = project_root / "aikea.yaml"
        source.write_text(yaml.safe_dump(project, sort_keys=False), encoding="utf-8")
        original_source = source.read_text(encoding="utf-8")
        AssemblyTaxonomyGenerator().generate(project, project_root)

        result = CabinetDrawerGenerator().generate(
            project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=356.0),
        )

        parent = project_root / "assemblies/tall_storage_01"
        self.assertTrue((parent / "drawer-layout.yaml").is_file())
        self.assertTrue((parent / "drawers/drawer_01/spec.py").is_file())
        self.assertTrue((parent / "drawers/drawer_01/builder.py").is_file())
        self.assertTrue((parent / "with_drawers_builder.py").is_file())
        self.assertEqual(source.read_text(encoding="utf-8"), original_source)
        self.assertEqual(result.plan.runner.product_code, "760H5000S")
        self.assertEqual(result.plan.drawer.box.outside_width_mm, 695.0)
        self.assertEqual(result.plan.origin_in_parent_mm, (24.0, 18.0, 456.0))

        layout = yaml.safe_load((parent / "drawer-layout.yaml").read_text())
        drawer = layout["drawers"][0]
        self.assertEqual(drawer["runner"]["product_code"], "760H5000S")
        self.assertEqual(drawer["runner"]["geometry"], "omitted_until_verified")
        self.assertEqual(
            drawer["local_frame"]["origin_in_parent_mm"],
            {"x": 24.0, "y": 18.0, "z": 456.0},
        )
