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
    """Protect hardware identity, ownership, and saved mounting frames."""

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
        self.assertEqual(
            [self._origin(runner) for runner in runners],
            [(18.0, 55.0, 465.575), (725.0, 55.0, 465.575)],
        )
        self.assertTrue(all(self._axes(runner) == self._hardware_axes() for runner in runners))

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
        self.assertEqual(
            [self._origin(lock) for lock in locks],
            [(-6.0, 37.0, 9.575), (701.0, 37.0, 9.575)],
        )
        self.assertTrue(all(self._axes(lock) == self._hardware_axes() for lock in locks))

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

    def test_drawer_parts_are_directly_walkable_from_their_saved_frames(self) -> None:
        tree = importlib.import_module("assemblies.assembly_tree")
        built_parts = tuple(
            self.specification.BuiltPart(part, object())
            for part in self.drawer_spec.parts
        )
        built_hardware = tuple(
            self.specification.BuiltPurchasedHardware(item, None)
            for item in self.drawer_spec.purchased_hardware
        )
        drawer = self.specification.BuiltAssembly(
            self.drawer_spec,
            built_parts,
            (),
            purchased_hardware=built_hardware,
        )

        visits = tree.AssemblyTreeWalker().walk(drawer)

        part_visits = [item for item in visits if type(item).__name__ == "AssemblyTreePart"]
        self.assertEqual(len(part_visits), 5)
        self.assertEqual(
            part_visits[0].local_to_root.origin_in_parent,
            self.specification.Point3D(15.0, 505.0, 0.0),
        )

    def _remove_generated_modules(self) -> None:
        for name in tuple(sys.modules):
            if name == "assemblies" or name.startswith("assemblies."):
                sys.modules.pop(name)

    def _origin(self, hardware) -> tuple[float, float, float]:
        origin = hardware.local_to_parent.origin_in_parent
        return origin.x_mm, origin.y_mm, origin.z_mm

    def _axes(self, hardware) -> tuple[tuple[float, float, float], ...]:
        basis = hardware.local_to_parent.axis_basis
        return tuple(
            (axis.x, axis.y, axis.z)
            for axis in (
                basis.local_x_in_parent,
                basis.local_y_in_parent,
                basis.local_z_in_parent,
            )
        )

    def _hardware_axes(self) -> tuple[tuple[float, float, float], ...]:
        return (
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
            (0.0, -1.0, 0.0),
        )


if __name__ == "__main__":
    unittest.main()
