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

    def test_project_placement_closes_the_complete_run_bounds(self) -> None:
        built = self.generator.loader.load_assembly(self.project_root, "tall_storage_03")
        local_parts = self.generator.cabinet_geometry.build(built)
        placed = self.generator.part_placer.place(
            built.spec.assembly_id,
            built.spec.global_left_mm,
            10.0,
            local_parts,
        )
        bounds = [part.placed_shape().BoundingBox() for part in placed]

        self.assertAlmostEqual(max(bound.xmax for bound in bounds), 2978.0)
        self.assertAlmostEqual(min(bound.ymin for bound in bounds), -18.0)
        self.assertAlmostEqual(min(bound.zmin for bound in bounds), 82.0)
        self.assertAlmostEqual(max(bound.zmax for bound in bounds), 2384.0)
