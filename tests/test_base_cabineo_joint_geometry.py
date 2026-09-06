"""Scope: Prove every structural-base brace has matching blind rail machining."""

from __future__ import annotations

from importlib.util import find_spec
import math
import unittest

from base_review_test_case import BaseReviewTestCase


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBaseCabineoJointGeometry(BaseReviewTestCase):
    """Verify paired connector geometry across every brace-to-rail seam."""

    def setUp(self) -> None:
        from base_part_locator import BasePartLocator
        from cabineo_connector_layout import CabineoConnectorLayout
        from part_blank_builder import PartBlankBuilder

        super().setUp()
        self.built = self.generator.loader.load_assembly(self.project_root, "base_01")
        self.locator = BasePartLocator()
        self.layout = CabineoConnectorLayout()
        self.blank_builder = PartBlankBuilder()

    def test_every_joint_applies_one_shared_layout_to_both_parts(self) -> None:
        joints = self._frame_joints()

        self.assertEqual(len(joints), 26)
        for joint in joints:
            with self.subTest(joint_id=joint.joint_id):
                source = self.built.spec.part(joint.source_part_id)
                expected_positions = self.layout.positions(joint, source)
                source_cuts = self._cuts(joint.joint_id, joint.source_part_id)
                target_cuts = self._cuts(joint.joint_id, joint.target_part_id)

                self.assertEqual(expected_positions, (20.5, 61.5))
                self.assertEqual(len(source_cuts), len(expected_positions))
                self.assertEqual(len(target_cuts), len(expected_positions))
                source_location = self.locator.locate(source, self.built.spec)
                target = self.built.spec.part(joint.target_part_id)
                target_location = self.locator.locate(target, self.built.spec)
                for source_cut, target_cut in zip(source_cuts, target_cuts):
                    self.assertIs(source_cut.cutter, target_cut.cutter)
                    self._assert_same_transform(
                        source_location * source_cut.location,
                        target_location * target_cut.location,
                    )

    def test_every_joint_is_blind_and_its_uncut_parts_meet(self) -> None:
        for joint in self._frame_joints():
            with self.subTest(joint_id=joint.joint_id):
                source = self.built.spec.part(joint.source_part_id)
                target = self.built.spec.part(joint.target_part_id)
                source_blank = self.blank_builder.build(source).val()
                target_blank = self.blank_builder.build(target).val()
                source_placed = source_blank.located(
                    self.locator.locate(source, self.built.spec)
                )
                target_placed = target_blank.located(
                    self.locator.locate(target, self.built.spec)
                )

                self.assertAlmostEqual(source_placed.intersect(target_placed).Volume(), 0.0)
                self.assertAlmostEqual(source_placed.distance(target_placed), 0.0)
                for part, blank in ((source, source_blank), (target, target_blank)):
                    for cut in self._cuts(joint.joint_id, part.part_id):
                        removed = blank.intersect(cut.cutter.located(cut.location))
                        self.assertGreater(removed.Volume(), 0.0)
                        self.assertLess(
                            removed.BoundingBox().zlen,
                            part.local_size_mm[2],
                        )

    def test_generated_braces_and_rails_contain_their_machining(self) -> None:
        machined_parts = [
            part
            for part in self.built.parts
            if part.spec.role in {"base_brace", "base_rail"}
        ]

        self.assertEqual(len(machined_parts), 17)
        for part in machined_parts:
            self.assertLess(
                part.solid.val().Volume(),
                math.prod(part.spec.local_size_mm),
            )

    def test_rejects_base_braces_too_short_for_the_connector_layout(self) -> None:
        import cadquery as cq

        from base_taxonomy_builder import BaseTaxonomyBuilder
        from cabineo_joint import CabineoJoint
        from part_construction_error import PartConstructionError

        base = BaseTaxonomyBuilder().build(
            cabinet_spans_mm=((10.0, 1001.3),),
            depth_mm=582.0,
            height_mm=30.0,
            panel_thickness_mm=18.0,
            plinth_front="recessed",
            plinth_recess_mm=60.0,
        )
        joint = next(
            joint for joint in base.joints if joint.purpose == "base_frame_corner"
        )
        parts_by_id = {part.part_id: part for part in base.parts}
        source = parts_by_id[joint.source_part_id]
        target = parts_by_id[joint.target_part_id]

        with self.assertRaisesRegex(PartConstructionError, "too short"):
            CabineoJoint().build(
                joint,
                source,
                target,
                cq.Location(),
                cq.Location(),
            )

    def _frame_joints(self):
        return tuple(
            joint
            for joint in self.built.joints
            if joint.purpose == "base_frame_corner"
        )

    def _cuts(self, joint_id: str, part_id: str):
        return tuple(
            cut
            for cut in self.built.cuts
            if cut.joint_id == joint_id and cut.part_id == part_id
        )

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
