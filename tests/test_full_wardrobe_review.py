"""Scope: Verify the complete generated wardrobe is positioned and exported."""

from __future__ import annotations

from importlib.util import find_spec
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from test_unit_mockup_generator import GlbTestDocument


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestFullWardrobeReview(unittest.TestCase):
    """Protect the full run's GLB nodes and local-to-project position report."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def setUp(self) -> None:
        from full_wardrobe_review_generator import FullWardrobeReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.generator = FullWardrobeReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_exports_all_three_closed_cabinets_on_the_complete_base(self) -> None:
        result = self.generator.generate(self.project_root, self.project)
        report = json.loads(result.position_report_path.read_text(encoding="utf-8"))
        nodes = GlbTestDocument(result.glb_path).node_names

        self.assertEqual(
            result.assembly_ids,
            ("tall_storage_01", "tall_storage_02", "tall_storage_03"),
        )
        self.assertEqual(
            result.door_states,
            {
                "tall_storage_01": "closed",
                "tall_storage_02": "closed",
                "tall_storage_03": "closed",
            },
        )
        self.assertEqual(result.glb_path.name, "full_wardrobe_review.glb")
        self.assertFalse(
            (self.project_root / "reviews/fabrication-assembly.json").exists()
        )
        self.assertTrue(
            {
                "base_01__deck_01",
                "tall_storage_01__door_panel",
                "tall_storage_02__door_panel",
                "tall_storage_03__door_panel",
            }.issubset(nodes)
        )
        self.assertEqual(report["status"], "valid")
        self.assertEqual(report["relationships"]["cabinet_gaps_mm"], [2.0, 2.0])
        self.assertEqual(
            report["relationships"]["door_bottoms_z_mm"],
            {
                "tall_storage_01": 82.0,
                "tall_storage_02": 82.0,
                "tall_storage_03": 82.0,
            },
        )
        self.assertEqual(
            report["assemblies"]["tall_storage_03"]["global_bounds"]["maximum_mm"],
            [2988.0, 582.0, 2384.0],
        )
        door = report["assemblies"]["tall_storage_02"]["part_positions"][
            "door_panel"
        ]
        self.assertEqual(door["assembly_bounds"]["minimum_mm"][1:], [-18.0, 82.0])
        self.assertTrue(all(check["passed"] for check in report["checks"]))

    def test_exports_all_three_doors_open_without_changing_fit_evidence(self) -> None:
        from door_review_state import DoorReviewState
        from full_wardrobe_door_plan import FullWardrobeDoorPlan

        result = self.generator.generate(
            self.project_root,
            self.project,
            FullWardrobeDoorPlan.uniform(DoorReviewState.OPEN),
        )
        report = json.loads(result.position_report_path.read_text(encoding="utf-8"))
        nodes = GlbTestDocument(result.glb_path).node_names

        self.assertEqual(set(result.door_states.values()), {"open"})
        self.assertEqual(result.glb_path.name, "full_wardrobe_open_review.glb")
        self.assertTrue(
            {
                "tall_storage_01__door_panel",
                "tall_storage_02__door_panel",
                "tall_storage_03__door_panel",
            }.issubset(nodes)
        )
        self.assertEqual(report["status"], "valid")
        physical_door = report["assemblies"]["tall_storage_01"]["part_positions"][
            "door_panel"
        ]
        self.assertEqual(
            physical_door["assembly_bounds"]["minimum_mm"][1:],
            [-18.0, 82.0],
        )

        built = self.generator.loader.load_assembly(
            self.project_root,
            "tall_storage_01",
        )
        open_parts = self.generator.cabinet_geometry.build(built, DoorReviewState.OPEN)
        open_door = next(part for part in open_parts if part.name == "door_panel")
        bounds = open_door.placed_shape().BoundingBox()
        self.assertAlmostEqual(bounds.xmin, -17.0)
        self.assertAlmostEqual(bounds.xmax, 1.0)
        self.assertAlmostEqual(bounds.ymin, -989.3333333333334)
        self.assertAlmostEqual(bounds.ymax, 0.0)

    def test_exports_one_open_door_and_removes_the_other_two_from_review(self) -> None:
        from door_review_state import DoorReviewState
        from full_wardrobe_door_plan import FullWardrobeDoorPlan

        plan = FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.CLOSED,
            (
                "tall_storage_01=open",
                "tall_storage_02=removed",
                "tall_storage_03=removed",
            ),
        )
        result = self.generator.generate(self.project_root, self.project, plan)
        report = json.loads(result.position_report_path.read_text(encoding="utf-8"))
        nodes = GlbTestDocument(result.glb_path).node_names

        self.assertEqual(
            result.door_states,
            {
                "tall_storage_01": "open",
                "tall_storage_02": "removed",
                "tall_storage_03": "removed",
            },
        )
        self.assertEqual(
            result.glb_path.name,
            "full_wardrobe_door_states_review.glb",
        )
        self.assertIn("tall_storage_01__door_panel", nodes)
        self.assertNotIn("tall_storage_02__door_panel", nodes)
        self.assertNotIn("tall_storage_03__door_panel", nodes)
        self.assertIn(
            "door_panel",
            report["assemblies"]["tall_storage_02"]["part_positions"],
        )
        self.assertEqual(report["status"], "valid")

    def test_tree_placement_closes_the_complete_run_bounds(self) -> None:
        from door_review_state import DoorReviewState

        wardrobe = self.generator.loader.load_assembly(
            self.project_root,
            "wardrobe_01",
        )
        visits = self.generator.loader.walk(self.project_root, wardrobe)
        all_parts = self.generator.tree_geometry.build(
            visits,
            {"tall_storage_03": DoorReviewState.CLOSED},
        )
        placed = tuple(
            part
            for part in all_parts
            if part.name.startswith("tall_storage_03__")
        )
        bounds = [part.placed_shape().BoundingBox() for part in placed]

        self.assertAlmostEqual(max(bound.xmax for bound in bounds), 2978.0)
        self.assertAlmostEqual(min(bound.ymin for bound in bounds), -18.0)
        self.assertAlmostEqual(min(bound.zmin for bound in bounds), 82.0)
        self.assertAlmostEqual(max(bound.zmax for bound in bounds), 2384.0)
