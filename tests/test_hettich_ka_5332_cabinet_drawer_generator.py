"""Scope: Verify the approved KA 5332 prototype becomes a saved drawer child."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from cadquery import Vector
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from hettich_ka_5332_cabinet_drawer_generator import (
    HettichKa5332CabinetDrawerGenerator,
)
from hettich_ka_5332_saved_plan_loader import HettichKa5332SavedPlanLoader
from hettich_ka_5332_test_support import (
    HettichKa5332StepAssemblyLoaderTestDouble,
    TEST_HETTICH_HARDWARE_DIRECTORY,
)


class TestHettichKa5332CabinetDrawerGenerator(unittest.TestCase):
    """Protect child ownership, source identity, and approved local frames."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        self.source = self.project_root / "aikea.yaml"
        self.source.write_text(
            yaml.safe_dump(project, sort_keys=False),
            encoding="utf-8",
        )
        self.original_source = self.source.read_text(encoding="utf-8")
        AssemblyTaxonomyGenerator().generate(project, self.project_root)
        self.result = HettichKa5332CabinetDrawerGenerator(
            HettichKa5332StepAssemblyLoaderTestDouble()
        ).generate(
            self.project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=356.0),
            hardware_directory=TEST_HETTICH_HARDWARE_DIRECTORY,
        )

    def tearDown(self) -> None:
        self._remove_generated_modules()
        self.temporary_directory.cleanup()

    def test_saves_the_approved_drawer_without_blocking_on_width_advice(self) -> None:
        parent = self.project_root / "assemblies/tall_storage_01"

        self.assertTrue((parent / "drawer-layout.yaml").is_file())
        self.assertTrue((parent / "drawers/drawer_01/spec.py").is_file())
        self.assertTrue((parent / "drawers/drawer_01/builder.py").is_file())
        self.assertTrue((parent / "with_drawers_builder.py").is_file())
        self.assertEqual(self.source.read_text(encoding="utf-8"), self.original_source)
        self.assertAlmostEqual(self.result.plan.drawer.box.outside_width_mm, 681.6)
        self.assertEqual(self.result.plan.drawer.box.outside_depth_mm, 530.0)
        self.assertEqual(
            self.result.plan.origin_in_parent_mm,
            (30.7, 0.0, 465.0),
        )
        self.assertEqual(
            self.result.plan.hardware_mounting.system_32_row_height_mm,
            388.0,
        )
        self.assertFalse(self.result.plan.hardware_mounting.recommended_width_met)
        self.assertTrue(self.result.plan.hardware_mounting.minimum_depth_met)

    def test_records_the_exact_pair_and_both_native_side_placements(self) -> None:
        parent = self.project_root / "assemblies/tall_storage_01"
        layout = yaml.safe_load((parent / "drawer-layout.yaml").read_text())
        drawer = layout["drawers"][0]
        runner = drawer["runner"]

        self.assertEqual(drawer["box"]["side_length_mm"], 500.0)
        self.assertEqual(drawer["box"]["outside_depth_mm"], 530.0)
        self.assertEqual(runner["manufacturer"], "Hettich")
        self.assertEqual(runner["item_number"], "9057405")
        self.assertEqual(runner["source"]["filename"], "9057405.stp")
        self.assertEqual(runner["source"]["solid_count"], 6)
        self.assertEqual(
            runner["side_placements"]["left"],
            {"x": 25.95, "y": 37.0, "z": 488.0},
        )
        self.assertEqual(
            runner["side_placements"]["right"],
            {"x": 531.95, "y": 37.0, "z": 488.0},
        )

    def test_composed_builder_owns_one_pair_and_one_wooden_child(self) -> None:
        self._remove_generated_modules()
        sys.path.insert(0, str(self.project_root))
        try:
            installation = importlib.import_module(
                "assemblies.tall_storage_01.drawer_installation"
            )
            drawer_spec = importlib.import_module(
                "assemblies.tall_storage_01.drawers.drawer_01.spec"
            ).SPEC
            built = importlib.import_module(
                "assemblies.tall_storage_01.with_drawers_builder"
            ).BUILDER.build()
        finally:
            sys.path.remove(str(self.project_root))

        self.assertEqual(len(installation.PURCHASED_HARDWARE), 2)
        left, right = installation.PURCHASED_HARDWARE
        self.assertEqual(left.hardware_id, "drawer_01_runner_left")
        self.assertEqual(right.hardware_id, "drawer_01_runner_right")
        self.assertEqual(left.hardware_asset_id, "hettich-ka-5332-500-runner-pair")
        self.assertEqual((left.geometry_selector, right.geometry_selector), ("left", "right"))
        self.assertIsNotNone(left.local_to_parent)
        self.assertEqual(drawer_spec.purchased_hardware, ())
        self.assertEqual(len(built.child_assemblies), 1)
        self.assertEqual(len(built.child_assemblies[0].assembly.parts), 5)
        self.assertEqual(len(built.purchased_hardware), 2)
        cabinet_side = next(part for part in built.parts if part.spec.part_id == "left_side")
        drawer_side = built.child_assemblies[0].assembly.parts[0]
        self.assertFalse(cabinet_side.solid.val().isInside(Vector(128.0, 388.0, 17.0)))
        self.assertFalse(drawer_side.solid.val().isInside(Vector(372.0, 23.0, 14.0)))
        saved_plan = HettichKa5332SavedPlanLoader().load(
            self.project_root,
            "tall_storage_01",
            built,
        )
        self.assertEqual(saved_plan.drawer_origin_mm, (30.7, 0.0, 465.0))
        self.assertEqual(
            saved_plan.left_runner_translation_mm,
            (25.95, 37.0, 488.0),
        )

    def _remove_generated_modules(self) -> None:
        for name in tuple(sys.modules):
            if name == "assemblies" or name.startswith("assemblies."):
                sys.modules.pop(name)


if __name__ == "__main__":
    unittest.main()
