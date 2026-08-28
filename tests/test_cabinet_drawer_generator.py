"""Scope: Verify one cabinet owns its generated drawer layout and child modules."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_generator import CabinetDrawerGenerator
from cabinet_drawer_plan import DrawerLayout
from drawer_hardware_test_support import (
    DrawerHardwareSetVerifierFactoryTestDouble,
    TEST_HARDWARE_DIRECTORY,
)
from hardware_asset_resolver import HardwareAssetError


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

        result = CabinetDrawerGenerator(
            DrawerHardwareSetVerifierFactoryTestDouble()
        ).generate(
            project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=356.0),
            hardware_directory=TEST_HARDWARE_DIRECTORY,
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
        self.assertEqual(
            drawer["runner"]["geometry"],
            "source_cad_mounting_plan_saved",
        )
        self.assertEqual(
            drawer["runner"]["fixed_mounting_frames"]["left"]["origin_mm"],
            {"x": 18.0, "y": 55.0, "z": 465.575},
        )
        self.assertEqual(
            drawer["runner"]["fixed_mounting_frames"]["right"]["origin_mm"],
            {"x": 725.0, "y": 55.0, "z": 465.575},
        )
        self.assertEqual(
            drawer["local_frame"]["origin_in_parent_mm"],
            {"x": 24.0, "y": 18.0, "z": 456.0},
        )

    def test_rejects_drawer_ids_that_cannot_be_stable_python_children(self) -> None:
        invalid_ids = (
            "drawer-01",
            "Drawer_01",
            "1_drawer_01",
            "drawer_1",
            "class",
        )

        for drawer_id in invalid_ids:
            with self.subTest(drawer_id=drawer_id):
                with self.assertRaisesRegex(ValueError, "stable lowercase"):
                    DrawerLayout(drawer_id, bottom_height_mm=356.0)

    def test_missing_source_cad_stops_before_any_drawer_file_is_written(self) -> None:
        temporary_directory = TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        project_root = Path(temporary_directory.name)
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, project_root)
        hardware_directory = project_root / "empty-hardware"
        hardware_directory.mkdir()

        with self.assertRaisesRegex(HardwareAssetError, "STEP file is missing"):
            CabinetDrawerGenerator().generate(
                project_root,
                "tall_storage_01",
                DrawerLayout("drawer_01", bottom_height_mm=356.0),
                hardware_directory=hardware_directory,
            )

        parent = project_root / "assemblies/tall_storage_01"
        self.assertFalse((parent / "drawer-layout.yaml").exists())
        self.assertFalse((parent / "drawers").exists())

    def test_rejects_traversal_before_rendering_outside_the_drawers_root(self) -> None:
        temporary_directory = TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        project_root = Path(temporary_directory.name)
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, project_root)

        with self.assertRaisesRegex(ValueError, "stable lowercase"):
            CabinetDrawerGenerator(
                DrawerHardwareSetVerifierFactoryTestDouble()
            ).generate(
                project_root,
                "tall_storage_01",
                DrawerLayout("../escaped_01", bottom_height_mm=356.0),
                hardware_directory=TEST_HARDWARE_DIRECTORY,
            )

        parent = project_root / "assemblies/tall_storage_01"
        self.assertFalse((parent / "escaped_01").exists())
        self.assertFalse((parent / "drawers").exists())
