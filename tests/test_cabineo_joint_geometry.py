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

    def setUp(self) -> None:
        from assembly_part_locator import AssemblyPartLocator
        from cabineo_connector_layout import CabineoConnectorLayout
        from part_blank_builder import PartBlankBuilder
        from unit_mockup_generator import UnitMockupGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.built = UnitMockupGenerator().loader.load_first(
            self.project_root,
            self.project,
        )
        self.locator = AssemblyPartLocator()
        self.layout = CabineoConnectorLayout()
        self.blank_builder = PartBlankBuilder()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_source_pockets_share_geometry_with_receiver_cuts(self) -> None:
        joint = next(
            joint
            for joint in self.built.joints
            if joint.joint_id == "left_side_to_top"
        )
        source_part = self.built.spec.part(joint.source_part_id)
        expected_positions = self.layout.positions(joint, source_part)
        cuts = [
            cut
            for cut in self.built.cuts
            if cut.joint_id == "left_side_to_top"
        ]
        source_cuts = [
            cut for cut in cuts if cut.part_id == joint.source_part_id
        ]
        target_cuts = [
            cut for cut in cuts if cut.part_id == joint.target_part_id
        ]

        self.assertEqual(len(source_cuts), len(expected_positions))
        self.assertEqual(len(target_cuts), len(expected_positions))
        self.assertEqual(len(cuts), len(expected_positions) * 2)
        self.assertEqual(
            [self._slide_center(cut.cutter, joint) for cut in source_cuts],
            list(expected_positions),
        )
        source_location = self._location(joint.source_part_id)
        target_location = self._location(joint.target_part_id)
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
        left_size = spec.part("left_side").local_size_mm
        top_size = spec.part("top_panel_01").local_size_mm
        self.assertLess(left.Volume(), left_size[0] * left_size[1] * left_size[2])
        self.assertLess(top.Volume(), top_size[0] * top_size[1] * top_size[2])

    def test_receiver_is_blind_and_mating_panels_do_not_overlap(self) -> None:
        """Prove the target receives a blind hole at a zero-volume contact seam."""
        joint = next(
            joint
            for joint in self.built.joints
            if joint.joint_id == "left_side_to_top"
        )
        source_spec = self.built.spec.part(joint.source_part_id)
        target_spec = self.built.spec.part(joint.target_part_id)
        source_blank = self.blank_builder.build(source_spec).val()
        target_blank = self.blank_builder.build(target_spec).val()
        source_location = self._location(joint.source_part_id)
        target_location = self._location(joint.target_part_id)
        source_placed = source_blank.located(source_location)
        target_placed = target_blank.located(target_location)

        self.assertAlmostEqual(source_placed.intersect(target_placed).Volume(), 0.0)
        self.assertAlmostEqual(source_placed.distance(target_placed), 0.0)

        receiver_cut = next(
            cut
            for cut in self.built.cuts
            if cut.joint_id == "left_side_to_top"
            and cut.part_id == joint.target_part_id
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

    def _slide_center(self, shape, joint) -> float:
        bounds = shape.BoundingBox()
        slide_axis = self.layout.slide_axis(joint.source_face, joint.source_edge)
        minimum = getattr(bounds, f"{slide_axis.lower()}min")
        maximum = getattr(bounds, f"{slide_axis.lower()}max")
        return (minimum + maximum) / 2.0

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
