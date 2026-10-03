"""Scope: Verify cabinet-to-base contact and reported coordinate transforms."""

from __future__ import annotations

from importlib.util import find_spec
import json
import unittest

from base_review_test_case import BaseReviewTestCase


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBaseAssemblyPositions(BaseReviewTestCase):
    """Protect physical contact and the local-to-global position contract."""

    def test_cabinet_sides_bear_on_the_base_deck(self) -> None:
        built_base = self.generator.loader.load_assembly(self.project_root, "base_01")
        base_parts = self.generator.base_geometry.build(built_base)
        built_cabinet = self.generator.loader.load_first(self.project_root, self.project)
        cabinet_parts = self.generator.cabinet_geometry.build(built_cabinet)
        deck_top_mm = max(
            part.placed_shape().BoundingBox().zmax
            for part in base_parts
            if part.name.startswith("deck_")
        )

        for side_id in ("left_side", "right_side"):
            side = next(part for part in cabinet_parts if part.name == side_id)
            self.assertAlmostEqual(side.placed_shape().BoundingBox().zmin, deck_top_mm)

    def test_writes_checked_local_and_global_positions(self) -> None:
        result = self.generator.generate(self.project_root, self.project)
        report = json.loads(result.position_report_path.read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "valid")
        self.assertEqual(
            report["assemblies"]["base_01"]["global_zero_mm"],
            [10.0, 0.0, 0.0],
        )
        self.assertEqual(
            report["assemblies"]["tall_storage_01"]["global_zero_mm"],
            [10.0, 0.0, 0.0],
        )
        relationships = report["relationships"]
        self.assertEqual(relationships["base_top_z_mm"], 100.0)
        self.assertEqual(relationships["cabinet_side_bottom_z_mm"], 100.0)
        self.assertEqual(relationships["door_bottom"], "plinth")
        self.assertEqual(relationships["door_bottom_z_mm"], 82.0)
        self.assertEqual(relationships["plinth_front"], "recessed")
        self.assertEqual(relationships["plinth_recess_mm"], 60.0)
        self.assertEqual(relationships["plinth_front_y_mm"], 60.0)
        self.assertAlmostEqual(
            relationships["first_base_module_projection_into_gap_mm"],
            1.0,
        )
        self.assertAlmostEqual(
            relationships["review_base_right_x_global_mm"],
            1002.3333333333334,
        )
        left_side = report["assemblies"]["tall_storage_01"]["part_positions"][
            "left_side"
        ]
        self.assertEqual(left_side["assembly_zero_mm"], [0.0, 0.0, 100.0])
        self.assertEqual(left_side["global_zero_mm"], [10.0, 0.0, 100.0])
        self.assertEqual(
            left_side["local_axes_in_assembly"],
            {
                "x": [0.0, 1.0, 0.0],
                "y": [0.0, 0.0, 1.0],
                "z": [1.0, 0.0, 0.0],
            },
        )
        self.assertTrue(all(check["passed"] for check in report["checks"]))
