"""Scope: Verify one built drawer appears in its cabinet and four-unit wardrobe."""

from __future__ import annotations

from importlib.util import find_spec
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_generator import CabinetDrawerGenerator
from cabinet_drawer_plan import DrawerLayout
from test_unit_mockup_generator import GlbTestDocument


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestDrawerWardrobeReview(unittest.TestCase):
    """Protect the project-owned child, position evidence, and both GLBs."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def setUp(self) -> None:
        from drawer_wardrobe_review_generator import DrawerWardrobeReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        CabinetDrawerGenerator().generate(
            self.project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=356.0),
        )
        self.generator = DrawerWardrobeReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_exports_the_built_child_in_closeup_and_existing_full_run(self) -> None:
        result = self.generator.generate(
            self.project_root,
            self.project,
            "tall_storage_01",
        )
        report = json.loads(
            result.drawer_position_report_path.read_text(encoding="utf-8")
        )
        full_report = json.loads(
            result.full_position_report_path.read_text(encoding="utf-8")
        )
        closeup_nodes = GlbTestDocument(result.closeup_glb_path).node_names
        full_nodes = GlbTestDocument(result.full_wardrobe_glb_path).node_names

        self.assertEqual(result.runner_product_code, "760H5000S")
        self.assertIn("drawer_01__left_side", closeup_nodes)
        self.assertNotIn("door_panel", closeup_nodes)
        self.assertIn("tall_storage_01__drawer_01__left_side", full_nodes)
        self.assertNotIn("tall_storage_01__door_panel", full_nodes)
        self.assertIn("tall_storage_02__door_panel", full_nodes)
        self.assertEqual(report["status"], "valid")
        self.assertEqual(full_report["status"], "valid")
        relationships = report["relationships"]
        self.assertEqual(
            relationships["drawer_local_zero_in_cabinet_mm"],
            [24.0, 18.0, 456.0],
        )
        self.assertEqual(relationships["runner_required_depth_mm"], 518.0)
        self.assertEqual(
            relationships["hardware_geometry"],
            "omitted_until_verified",
        )
        self.assertEqual(
            relationships["closed_clearances_mm"],
            {
                "left": 6.0,
                "right": 6.0,
                "front": 18.0,
                "rear": 56.0,
                "below": 356.0,
                "above": 98.5,
            },
        )
        self.assertEqual(
            report["assemblies"]["drawer_01"]["global_zero_mm"],
            [34.0, 18.0, 456.0],
        )
