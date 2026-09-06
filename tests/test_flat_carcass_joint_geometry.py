"""Scope: Prove every square flat-carcass seam has matching blind machining."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestFlatCarcassJointGeometry(unittest.TestCase):
    """Verify the complete Cabinet 2 square-joint construction pattern."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"
    _JOINT_IDS = {
        "left_side_to_back_panel",
        "right_side_to_back_panel",
        "left_side_to_top",
        "right_side_to_top",
        "top_panel_01_to_back_panel",
    }

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

    def test_every_square_seam_applies_its_complete_layout_to_both_parts(self) -> None:
        for joint_id in self._JOINT_IDS:
            with self.subTest(joint_id=joint_id):
                joint = next(joint for joint in self.built.joints if joint.joint_id == joint_id)
                cuts = [cut for cut in self.built.cuts if cut.joint_id == joint_id]
                source = self.built.spec.part(joint.source_part_id)
                connector_count = len(self.layout.positions(joint, source))
                self.assertGreaterEqual(connector_count, 2)
                self.assertEqual(len(cuts), connector_count * 2)
                self.assertEqual(
                    {cut.part_id for cut in cuts},
                    {joint.source_part_id, joint.target_part_id},
                )

    def test_every_receiver_is_blind_and_uncut_parts_only_touch(self) -> None:
        for joint_id in self._JOINT_IDS:
            with self.subTest(joint_id=joint_id):
                joint = next(joint for joint in self.built.joints if joint.joint_id == joint_id)
                source = self.built.spec.part(joint.source_part_id)
                target = self.built.spec.part(joint.target_part_id)
                source_blank = self.blank_builder.build(source).val()
                target_blank = self.blank_builder.build(target).val()
                source_placed = source_blank.located(self._location(source))
                target_placed = target_blank.located(self._location(target))
                self.assertAlmostEqual(source_placed.intersect(target_placed).Volume(), 0.0)
                self.assertAlmostEqual(source_placed.distance(target_placed), 0.0)

                receivers = [
                    cut
                    for cut in self.built.cuts
                    if cut.joint_id == joint_id and cut.part_id == target.part_id
                ]
                for receiver_cut in receivers:
                    receiver = target_blank.intersect(
                        receiver_cut.cutter.located(receiver_cut.location)
                    )
                    self.assertGreater(receiver.Volume(), 0.0)
                    self.assertLess(receiver.BoundingBox().zlen, target.local_size_mm[2])

    def test_thin_back_is_rejected_before_connector_geometry_is_applied(self) -> None:
        from part_construction_error import PartConstructionError
        from unit_mockup_generator import UnitMockupGenerator

        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        project["design_settings"]["materials"]["back_panel_thickness"] = 0.6
        with TemporaryDirectory() as project_root:
            AssemblyTaxonomyGenerator().generate(project, Path(project_root))
            with self.assertRaisesRegex(PartConstructionError, "back_panel is 6 mm"):
                UnitMockupGenerator().loader.load_first(Path(project_root), project)

    def _location(self, part):
        return self.locator.locate(
            part,
            self.built.spec,
            float(self.built.spec.base_height_mm),
        )


if __name__ == "__main__":
    unittest.main()
