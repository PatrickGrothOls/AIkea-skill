"""Scope: Verify one planned drawer builds as five correctly placed sheet blanks."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import (
    CabinetDrawerOpening,
    DrawerBoxSizingProfile,
)
from generated_assembly_spec_loader import GeneratedAssemblySpecLoader


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestDrawerBoxGeometry(unittest.TestCase):
    """Use the generated four-cabinet opening as the drawer source of truth."""

    FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def setUp(self) -> None:
        from drawer_box_builder import DrawerBoxBuilder
        from drawer_box_fit_checker import DrawerBoxFitChecker

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        project = yaml.safe_load(self.FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, self.project_root)
        cabinet = GeneratedAssemblySpecLoader().load(
            self.project_root,
            "tall_storage_01",
        )
        self.opening = CabinetDrawerOpening.from_assembly_spec(cabinet)
        self.drawer = DrawerBoxPlanner().plan(
            self.opening,
            DrawerBoxSizingProfile(runner_length_mm=500.0),
        )
        self.built = DrawerBoxBuilder().build(self.drawer)
        self.fit_checker = DrawerBoxFitChecker()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_reads_the_first_generated_cabinet_opening(self) -> None:
        self.assertAlmostEqual(self.opening.clear_width_mm, 707.0)
        self.assertAlmostEqual(self.opening.inside_depth_mm, 564.0)
        self.assertAlmostEqual(self.drawer.clear_inside_width_mm, 665.0)
        self.assertAlmostEqual(self.drawer.outside_width_mm, 695.0)
        self.assertAlmostEqual(self.drawer.side_length_mm, 490.0)
        self.assertAlmostEqual(self.drawer.outside_depth_mm, 520.0)
        self.assertAlmostEqual(self.drawer.clear_inside_depth_mm, 490.0)

    def test_every_part_starts_in_its_canonical_manufacturing_frame(self) -> None:
        expected_sizes = {
            "left_side": (490.0, 160.0, 15.0),
            "right_side": (490.0, 160.0, 15.0),
            "front": (695.0, 160.0, 15.0),
            "back": (695.0, 160.0, 15.0),
            "bottom": (665.0, 490.0, 9.0),
        }
        for part in self.built.parts:
            bounds = part.solid.val().BoundingBox()
            width_mm, height_mm, thickness_mm = expected_sizes[part.spec.part_id]
            self.assert_bounds(
                bounds,
                (0.0, width_mm, 0.0, height_mm, 0.0, thickness_mm),
            )
            self.assertTrue(part.solid.val().isValid())

    def test_explicit_placements_close_the_box_without_material_overlap(self) -> None:
        expected_bounds = {
            "left_side": (0.0, 15.0, 15.0, 505.0, 0.0, 160.0),
            "right_side": (680.0, 695.0, 15.0, 505.0, 0.0, 160.0),
            "front": (0.0, 695.0, 0.0, 15.0, 0.0, 160.0),
            "back": (0.0, 695.0, 505.0, 520.0, 0.0, 160.0),
            "bottom": (15.0, 680.0, 15.0, 505.0, 13.0, 22.0),
        }
        for part in self.built.parts:
            self.assert_bounds(
                part.placed_shape().BoundingBox(),
                expected_bounds[part.spec.part_id],
            )

        report = self.fit_checker.check(self.built)
        self.assertTrue(report.passed)
        self.assertEqual(len(report.intended_contacts), 8)
        self.assertEqual(report.missing_contacts, ())
        self.assertEqual(report.overlapping_parts, ())

    def test_the_same_calculation_accepts_a_550_millimetre_runner_in_depth(self) -> None:
        drawer = DrawerBoxPlanner().plan(
            CabinetDrawerOpening(
                clear_width_mm=self.opening.clear_width_mm,
                inside_depth_mm=600.0,
            ),
            DrawerBoxSizingProfile(runner_length_mm=550.0),
        )

        self.assertAlmostEqual(drawer.side_length_mm, 540.0)
        self.assertAlmostEqual(drawer.outside_depth_mm, 570.0)
        self.assertAlmostEqual(drawer.clear_inside_depth_mm, 540.0)

    def assert_bounds(self, bounds, expected: tuple[float, ...]) -> None:
        actual = (
            bounds.xmin,
            bounds.xmax,
            bounds.ymin,
            bounds.ymax,
            bounds.zmin,
            bounds.zmax,
        )
        for value, target in zip(actual, expected):
            self.assertAlmostEqual(value, target, places=5)


if __name__ == "__main__":
    unittest.main()
