"""Scope: Verify one cabinet owns its generated drawer layout and child modules."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import json

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
        self.assertTrue((parent / "drawers/feature.py").is_file())
        self.assertTrue((parent / "with_drawers_builder.py").is_file())
        self.assertTrue((parent / "complete_builder.py").is_file())
        compile(
            (parent / "drawers/feature.py").read_text(encoding="utf-8"),
            "drawers/feature.py",
            "exec",
        )
        self.assertEqual(source.read_text(encoding="utf-8"), original_source)
        self.assertEqual(result.plan.runner.product_code, "760H5000S")
        self.assertEqual(result.plan.drawer.box.outside_width_mm, 695.0)
        self.assertEqual(result.plan.drawer.box.outside_depth_mm, 520.0)
        self.assertEqual(result.plan.origin_in_parent_mm, (24.0, 18.0, 456.0))
        feature_manifest = json.loads((parent / "features.json").read_text())
        self.assertEqual(
            feature_manifest["features"],
            [
                {
                    "module": "drawers.feature",
                    "order": 10,
                    "affected_manufactured_part_paths": [
                        "drawer_01/left_side",
                        "drawer_01/right_side",
                        "drawer_01/front",
                        "drawer_01/back",
                        "drawer_01/bottom",
                    ],
                }
            ],
        )

        layout = yaml.safe_load((parent / "drawer-layout.yaml").read_text())
        drawer = layout["drawers"][0]
        self.assertEqual(drawer["box"]["side_length_mm"], 490.0)
        self.assertEqual(drawer["box"]["outside_depth_mm"], 520.0)
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
