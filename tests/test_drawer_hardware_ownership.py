"""Scope: Verify fixed and moving drawer hardware remain with their owners."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys
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
from hardware_asset_manifest import HardwareAssetManifest


class TestDrawerHardwareOwnership(unittest.TestCase):
    """Protect hardware identity without inventing unresolved CAD geometry."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"
    _MANIFEST = (
        Path(__file__).parents[1]
        / "aikea-build-drawers/assets/blum/movento/hardware-assets.json"
    )

    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, self.project_root)
        CabinetDrawerGenerator(
            DrawerHardwareSetVerifierFactoryTestDouble()
        ).generate(
            self.project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=356.0),
            hardware_directory=TEST_HARDWARE_DIRECTORY,
        )
        self._remove_generated_modules()
        sys.path.insert(0, str(self.project_root))
        self.specification = importlib.import_module("assemblies.specification")
        self.installation = importlib.import_module(
            "assemblies.tall_storage_01.drawer_installation"
        )
        self.drawer_spec = importlib.import_module(
            "assemblies.tall_storage_01.drawers.drawer_01.spec"
        ).SPEC

    def tearDown(self) -> None:
        sys.path.remove(str(self.project_root))
        self._remove_generated_modules()
        self.temporary_directory.cleanup()

    def test_fixed_runners_belong_to_the_cabinet(self) -> None:
        runners = self.installation.FIXED_RUNNERS

        self.assertEqual(
            [runner.hardware_id for runner in runners],
            ["runner_left", "runner_right"],
        )
        self.assertTrue(all(runner.product_code == "760H5000S" for runner in runners))
        self.assertEqual(
            [runner.hardware_asset_id for runner in runners],
            [
                "movento-760h5000s-runner-left",
                "movento-760h5000s-runner-right",
            ],
        )
        self.assertTrue(all(runner.local_to_parent is None for runner in runners))

    def test_locking_devices_belong_to_the_moving_drawer(self) -> None:
        locks = self.drawer_spec.purchased_hardware

        self.assertEqual(
            [lock.hardware_id for lock in locks],
            ["locking_device_left", "locking_device_right"],
        )
        self.assertEqual(
            [lock.hardware_asset_id for lock in locks],
            [
                "t51-7601-left-locking-device",
                "t51-7601-right-locking-device",
            ],
        )
        self.assertTrue(all(lock.local_to_parent is None for lock in locks))

    def test_every_identity_resolves_through_the_manifest_without_geometry(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST)
        hardware = (
            *self.installation.FIXED_RUNNERS,
            *self.drawer_spec.purchased_hardware,
        )

        for item in hardware:
            self.assertEqual(manifest.asset(item.hardware_asset_id).asset_id, item.hardware_asset_id)
            built = self.specification.BuiltPurchasedHardware(item, None)
            self.assertFalse(built.has_geometry)

    def _remove_generated_modules(self) -> None:
        for name in tuple(sys.modules):
            if name == "assemblies" or name.startswith("assemblies."):
                sys.modules.pop(name)


if __name__ == "__main__":
    unittest.main()
