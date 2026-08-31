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
from drawer_hardware_test_support import (
    DrawerHardwareSetVerifierFactoryTestDouble,
    TEST_HARDWARE_DIRECTORY,
)
from drawer_hardware_review_test_support import DrawerHardwareReviewBuilderTestDouble
from drawer_review_state import DrawerReviewState
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
        CabinetDrawerGenerator(
            DrawerHardwareSetVerifierFactoryTestDouble()
        ).generate(
            self.project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=356.0),
            hardware_directory=TEST_HARDWARE_DIRECTORY,
        )
        self.generator = DrawerWardrobeReviewGenerator(
            DrawerHardwareReviewBuilderTestDouble()
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_exports_three_drawer_states_and_removed_mounting_zones(self) -> None:
        results = {
            state: self.generator.generate(
                self.project_root,
                self.project,
                "tall_storage_01",
                TEST_HARDWARE_DIRECTORY,
                state,
            )
            for state in DrawerReviewState
        }
        documents = {
            state: (
                GlbTestDocument(result.closeup_glb_path),
                GlbTestDocument(result.full_wardrobe_glb_path),
            )
            for state, result in results.items()
        }
        runner_nodes = {"runner_left__source_cad", "runner_right__source_cad"}
        preview_nodes = {
            f"review_only__runner_{hand}__{part}"
            for hand in ("left", "right")
            for part in ("fixed_path", "drawer_side_guide")
        }
        lock_nodes = {
            "drawer_01__locking_device_left__source_cad",
            "drawer_01__locking_device_right__source_cad",
        }
        for state, (closeup, full) in documents.items():
            runner_is_visible = runner_nodes.issubset(closeup.node_names)
            full_runner_is_visible = {
                f"tall_storage_01__{name}" for name in runner_nodes
            }.issubset(full.node_names)
            exact_is_expected = state is not DrawerReviewState.OPEN
            self.assertEqual(runner_is_visible, exact_is_expected)
            self.assertEqual(full_runner_is_visible, exact_is_expected)
            self.assertEqual(
                preview_nodes.issubset(closeup.node_names),
                state is DrawerReviewState.OPEN,
            )
            locks_are_visible = lock_nodes.issubset(closeup.node_names)
            full_locks_are_visible = {
                f"tall_storage_01__{name}" for name in lock_nodes
            }.issubset(full.node_names)
            expected_lock_visibility = state is not DrawerReviewState.REMOVED
            self.assertEqual(locks_are_visible, expected_lock_visibility)
            self.assertEqual(full_locks_are_visible, expected_lock_visibility)
            drawer_is_visible = "drawer_01__left_side" in closeup.node_names
            self.assertEqual(drawer_is_visible, state is not DrawerReviewState.REMOVED)
            self.assertEqual(results[state].drawer_state, state.value)
            self.assertEqual(
                results[state].runner_review_representation,
                (
                    "review_only_runner_movement"
                    if state is DrawerReviewState.OPEN
                    else "source_cad_mounted_and_position_checked"
                ),
            )
        self.assertEqual(
            len({result.full_wardrobe_glb_path for result in results.values()}),
            3,
        )
        result = results[DrawerReviewState.OPEN]
        report = json.loads(
            result.drawer_position_report_path.read_text(encoding="utf-8")
        )
        full_report = json.loads(
            result.full_position_report_path.read_text(encoding="utf-8")
        )
        hardware_report = json.loads(
            result.hardware_position_report_path.read_text(encoding="utf-8")
        )
        movement_report = json.loads(
            result.runner_movement_report_path.read_text(encoding="utf-8")
        )
        closeup_nodes = documents[DrawerReviewState.OPEN][0].node_names
        full_nodes = documents[DrawerReviewState.OPEN][1].node_names

        self.assertEqual(result.runner_product_code, "760H5000S")
        self.assertIn("drawer_01__left_side", closeup_nodes)
        self.assertNotIn("door_panel", closeup_nodes)
        self.assertIn("tall_storage_01__drawer_01__left_side", full_nodes)
        self.assertNotIn("tall_storage_01__door_panel", full_nodes)
        self.assertIn("tall_storage_02__door_panel", full_nodes)
        self.assertEqual(report["status"], "valid")
        self.assertEqual(full_report["status"], "valid")
        self.assertEqual(hardware_report["status"], "valid")
        self.assertEqual(movement_report["status"], "valid")
        self.assertFalse(movement_report["manufacturing_authority"])
        relationships = report["relationships"]
        self.assertEqual(
            relationships["drawer_local_zero_in_cabinet_mm"],
            [24.0, 18.0, 456.0],
        )
        self.assertEqual(relationships["runner_required_depth_mm"], 518.0)
        self.assertEqual(
            relationships["hardware_geometry"],
            "source_cad_mounting_plan_saved",
        )
        self.assertEqual(
            relationships["closed_clearances_mm"],
            {
                "left": 6.0,
                "right": 6.0,
                "front": 18.0,
                "rear": 26.0,
                "below": 356.0,
                "above": 98.5,
            },
        )
        self.assertEqual(
            report["assemblies"]["drawer_01"]["global_zero_mm"],
            [34.0, 18.0, 456.0],
        )
