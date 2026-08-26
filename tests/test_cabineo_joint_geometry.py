"""Scope: Prove one Cabineo joint cuts both panels from identical geometry."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestCabineoJointGeometry(unittest.TestCase):
    """Verify source pockets and receiver cuts coincide in assembly space."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"
    _EVAL_SET = Path(__file__).parents[1] / "evals" / "build-unit-taxonomy.yaml"

    def setUp(self) -> None:
        from assembly_part_locator import AssemblyPartLocator
        from part_blank_builder import PartBlankBuilder
        from unit_mockup_generator import UnitMockupGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        eval_set = yaml.safe_load(self._EVAL_SET.read_text(encoding="utf-8"))
        self.expected_joint = eval_set["cases"][0]["answer_key"]["expected_first_joint"]
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.built = UnitMockupGenerator().loader.load_first(
            self.project_root,
            self.project,
        )
        self.locator = AssemblyPartLocator()
        self.blank_builder = PartBlankBuilder()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_two_source_pockets_share_geometry_with_two_receiver_cuts(self) -> None:
        cuts = [
            cut
            for cut in self.built.cuts
            if cut.joint_id == "left_side_to_top"
        ]
        source_cuts = [cut for cut in cuts if cut.part_id == "left_side"]
        target_cuts = [cut for cut in cuts if cut.part_id == "top_panel_01"]

        self.assertEqual(len(source_cuts), self.expected_joint["connectors"])
        self.assertEqual(len(target_cuts), self.expected_joint["connectors"])
        self.assertEqual(
            len(cuts),
            self.expected_joint["connectors"]
            * self.expected_joint["cuts_per_connector"],
        )
        self.assertEqual(
            [self._x_center(cut.cutter) for cut in source_cuts],
            [145.5, 436.5],
        )
        source_location = self._location("left_side")
        target_location = self._location("top_panel_01")
        for source, target in zip(source_cuts, target_cuts):
            self.assertIs(source.cutter, target.cutter)
            self._assert_same_transform(
                source_location * source.location,
                target_location * target.location,
            )

    def test_generated_part_builders_apply_both_sides_of_the_joint(self) -> None:
        left = self._built_part("left_side").solid.val()
        top = self._built_part("top_panel_01").solid.val()
        spec = self.built.spec

        self.assertTrue(left.isValid())
        self.assertTrue(top.isValid())
        self.assertLess(left.Volume(), 582.0 * 2266.0 * 18.0)
        self.assertLess(top.Volume(), spec.width_mm * 582.0 * 18.0)

    def test_receiver_is_blind_and_mating_panels_do_not_overlap(self) -> None:
        """Prove the target receives a blind hole at a zero-volume contact seam."""
        source_spec = self.built.spec.part("left_side")
        target_spec = self.built.spec.part("top_panel_01")
        source_blank = self.blank_builder.build(source_spec).val()
        target_blank = self.blank_builder.build(target_spec).val()
        source_location = self._location("left_side")
        target_location = self._location("top_panel_01")
        source_placed = source_blank.located(source_location)
        target_placed = target_blank.located(target_location)

        self.assertAlmostEqual(source_placed.intersect(target_placed).Volume(), 0.0)
        self.assertAlmostEqual(source_placed.distance(target_placed), 0.0)

        receiver_cut = next(
            cut
            for cut in self.built.cuts
            if cut.joint_id == "left_side_to_top"
            and cut.part_id == "top_panel_01"
        )
        receiver = target_blank.intersect(
            receiver_cut.cutter.located(receiver_cut.location)
        )
        self.assertLess(receiver.BoundingBox().zlen, target_spec.local_size_mm[2])

    def _built_part(self, part_id: str):
        return next(part for part in self.built.parts if part.spec.part_id == part_id)

    def _location(self, part_id: str):
        part = self.built.spec.part(part_id)
        return self.locator.locate(
            part,
            self.built.spec,
            float(self.built.spec.base_height_mm),
        )

    def _x_center(self, shape) -> float:
        bounds = shape.BoundingBox()
        return (bounds.xmin + bounds.xmax) / 2.0

    def _assert_same_transform(self, source, target) -> None:
        source_transform = source.wrapped.Transformation()
        target_transform = target.wrapped.Transformation()
        for row in range(1, 4):
            for column in range(1, 5):
                self.assertAlmostEqual(
                    source_transform.Value(row, column),
                    target_transform.Value(row, column),
                )


if __name__ == "__main__":
    unittest.main()
