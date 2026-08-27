"""Scope: Verify a generated four-unit project builds as one physical wardrobe."""

from __future__ import annotations

from dataclasses import replace
from importlib.util import find_spec
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from test_unit_mockup_generator import GlbTestDocument


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestFourUnitFullWardrobeReview(unittest.TestCase):
    """Build one four-cabinet slope and prove every generated miter closes."""

    FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def setUp(self) -> None:
        from full_wardrobe_review_generator import FullWardrobeReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self.FIXTURE.read_text(encoding="utf-8"))
        self.taxonomy = AssemblyTaxonomyGenerator().generate(
            self.project,
            self.project_root,
        )
        self.generator = FullWardrobeReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_exports_four_cabinets_on_the_complete_base(self) -> None:
        from door_review_state import DoorReviewState
        from full_wardrobe_door_plan import FullWardrobeDoorPlan

        door_plan = FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.REMOVED,
            ("tall_storage_01=open",),
        )
        result = self.generator.generate(self.project_root, self.project, door_plan)
        report = json.loads(result.position_report_path.read_text(encoding="utf-8"))
        nodes = GlbTestDocument(result.glb_path).node_names

        self.assertEqual(
            result.assembly_ids,
            tuple(f"tall_storage_{index:02d}" for index in range(1, 5)),
        )
        self.assertTrue(
            {
                "base_01__deck_01",
                "base_01__deck_02",
                "tall_storage_01__door_panel",
            }.issubset(nodes)
        )
        self.assertFalse(
            {
                "tall_storage_02__door_panel",
                "tall_storage_03__door_panel",
                "tall_storage_04__door_panel",
            }
            & nodes
        )
        self.assertEqual(report["status"], "valid")
        self.assertEqual(report["relationships"]["cabinet_gaps_mm"], [2.0] * 3)
        last_maximum = report["assemblies"]["tall_storage_04"]["global_bounds"][
            "maximum_mm"
        ]
        for actual, expected in zip(last_maximum, (2988.0, 582.0, 2097.722222222222)):
            self.assertAlmostEqual(actual, expected)
        self.assertTrue(all(check["passed"] for check in report["checks"]))

    def test_overall_profile_becomes_six_physical_local_miters(self) -> None:
        from assembly_part_locator import AssemblyPartLocator

        assemblies = {
            assembly.assembly_id: assembly
            for assembly in self.taxonomy.assemblies
            if assembly.purpose == "tall_storage"
        }
        self.assertEqual(
            tuple((point.x_mm, point.height_mm) for point in assemblies["tall_storage_02"].top),
            ((0.0, 2288.0), (445.0, 2288.0), (743.0, 2205.222222222222)),
        )
        expected_counts = (0, 2, 2, 2)
        locator = AssemblyPartLocator()
        for index, expected_count in enumerate(expected_counts, start=1):
            assembly_id = f"tall_storage_{index:02d}"
            built = self.generator.loader.load_assembly(self.project_root, assembly_id)
            miters = tuple(
                joint for joint in built.joints
                if joint.joint_type == "equal_thickness_miter"
            )
            self.assertEqual(len(miters), expected_count)
            for joint in miters:
                self._assert_closed_miter(built, joint, locator)

    def test_rejects_unequal_material_at_a_miter(self) -> None:
        from assembly_part_locator import AssemblyPartLocator
        from equal_thickness_miter_joint import EqualThicknessMiterJoint
        from part_construction_error import PartConstructionError

        built = self.generator.loader.load_assembly(self.project_root, "tall_storage_02")
        joint = next(item for item in built.joints if item.joint_type == "equal_thickness_miter")
        part_a = built.spec.part(joint.participant_ids[0])
        part_b = built.spec.part(joint.participant_ids[1])
        unequal_part_b = replace(
            part_b,
            local_size_mm=(*part_b.local_size_mm[:2], 19.0),
        )
        locator = AssemblyPartLocator()
        with self.assertRaisesRegex(PartConstructionError, "require equal thickness"):
            EqualThicknessMiterJoint().build(
                joint,
                part_a,
                unequal_part_b,
                locator.locate(part_a, built.spec, 100.0),
                locator.locate(unequal_part_b, built.spec, 100.0),
            )

    def _assert_closed_miter(self, built, joint, locator) -> None:
        cuts = tuple(cut for cut in built.cuts if cut.joint_id == joint.joint_id)
        self.assertEqual({cut.part_id for cut in cuts}, set(joint.participant_ids))
        placed = []
        for part_id in joint.participant_ids:
            part = next(item for item in built.parts if item.spec.part_id == part_id)
            location = locator.locate(part.spec, built.spec, built.spec.base_height_mm)
            placed.append(part.solid.val().located(location))
        self.assertAlmostEqual(placed[0].intersect(placed[1]).Volume(), 0.0, places=5)
        self.assertAlmostEqual(placed[0].distance(placed[1]), 0.0, places=5)
