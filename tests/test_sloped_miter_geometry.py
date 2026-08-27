"""Scope: Prove generated sloped panels meet through physical paired miters."""

from __future__ import annotations

from dataclasses import replace
from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestSlopedMiterGeometry(unittest.TestCase):
    """Check both seams created by one arbitrary flat-then-slope cabinet."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "sloped-miter-aikea.yaml"

    def setUp(self) -> None:
        from assembly_part_locator import AssemblyPartLocator
        from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        taxonomy = AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.spec = taxonomy.assemblies[0]
        self.built = GeneratedAssemblyBuilderLoader().load_first(
            self.project_root,
            self.project,
        )
        self.locator = AssemblyPartLocator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_spec_preserves_the_chosen_flat_run_and_right_height(self) -> None:
        self.assertEqual(
            tuple((point.x_mm, point.height_mm) for point in self.spec.top),
            ((0.0, 2300.0), (420.0, 2300.0), (1000.0, 1800.0)),
        )

    def test_both_required_seams_are_equal_thickness_miters(self) -> None:
        joint_types = {joint.joint_id: joint.joint_type for joint in self.spec.joints}
        self.assertEqual(
            joint_types["top_panel_01_to_top_panel_02"],
            "equal_thickness_miter",
        )
        self.assertEqual(joint_types["right_side_to_top"], "equal_thickness_miter")

    def test_each_miter_cuts_both_participants_without_gap_or_overlap(self) -> None:
        built_parts = {part.spec.part_id: part for part in self.built.parts}
        cuts_by_joint: dict[str, list] = {}
        for cut in self.built.cuts:
            cuts_by_joint.setdefault(cut.joint_id, []).append(cut)

        expected_participants = {
            "top_panel_01_to_top_panel_02": {"top_panel_01", "top_panel_02"},
            "right_side_to_top": {"top_panel_02", "right_side"},
        }
        for joint_id, participant_ids in expected_participants.items():
            self.assertEqual(
                {cut.part_id for cut in cuts_by_joint[joint_id]},
                participant_ids,
            )
            first_id, second_id = sorted(participant_ids)
            first = self._placed(built_parts[first_id])
            second = self._placed(built_parts[second_id])
            self.assertAlmostEqual(first.intersect(second).Volume(), 0.0, places=5)
            self.assertAlmostEqual(first.distance(second), 0.0, places=5)

    def test_miter_rejects_unequal_sheet_thicknesses(self) -> None:
        from equal_thickness_miter_joint import EqualThicknessMiterJoint
        from part_construction_error import PartConstructionError

        part_a = self.built.spec.part("top_panel_01")
        part_b = self.built.spec.part("top_panel_02")
        unequal_part_b = replace(
            part_b,
            local_size_mm=(part_b.local_size_mm[0], part_b.local_size_mm[1], 19.0),
        )
        joint = next(
            item
            for item in self.built.spec.joints
            if item.joint_id == "top_panel_01_to_top_panel_02"
        )
        with self.assertRaisesRegex(PartConstructionError, "require equal thickness"):
            EqualThicknessMiterJoint().build(
                joint,
                part_a,
                unequal_part_b,
                self.locator.locate(part_a, self.built.spec, self.built.spec.base_height_mm),
                self.locator.locate(
                    unequal_part_b,
                    self.built.spec,
                    self.built.spec.base_height_mm,
                ),
            )

    def _placed(self, built_part):
        location = self.locator.locate(
            built_part.spec,
            self.built.spec,
            float(self.built.spec.base_height_mm),
        )
        return built_part.solid.val().located(location)


if __name__ == "__main__":
    unittest.main()
