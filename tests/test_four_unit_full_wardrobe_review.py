"""Scope: Verify a generated four-unit project builds as one physical wardrobe."""

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
class TestFourUnitFullWardrobeReview(unittest.TestCase):
    """Build four generated cabinets and their base through the real builders."""

    FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def setUp(self) -> None:
        from full_wardrobe_review_generator import FullWardrobeReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self.FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.generator = FullWardrobeReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_exports_four_cabinets_on_the_complete_base(self) -> None:
        result = self.generator.generate(self.project_root, self.project)
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
                "tall_storage_02__door_panel",
                "tall_storage_03__door_panel",
                "tall_storage_04__door_panel",
            }.issubset(nodes)
        )
        self.assertEqual(report["status"], "valid")
        self.assertEqual(report["relationships"]["cabinet_gaps_mm"], [2.0] * 3)
        self.assertEqual(
            report["assemblies"]["tall_storage_04"]["global_bounds"]["maximum_mm"],
            [2988.0, 582.0, 2384.0],
        )
        self.assertTrue(all(check["passed"] for check in report["checks"]))
