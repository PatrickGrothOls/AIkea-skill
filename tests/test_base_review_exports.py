"""Scope: Verify named structural base GLBs contain only the intended module."""

from __future__ import annotations

from importlib.util import find_spec
import unittest

from base_review_test_case import BaseReviewTestCase
from test_unit_mockup_generator import GlbTestDocument


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBaseReviewExports(BaseReviewTestCase):
    """Protect the complete-base and first-cabinet review exports."""

    def test_exports_named_base_and_combined_glbs(self) -> None:
        result = self.generator.generate(self.project_root, self.project)
        base_nodes = GlbTestDocument(result.base_glb_path).node_names
        combined_nodes = GlbTestDocument(result.cabinet_with_base_glb_path).node_names

        self.assertTrue({"deck_01", "front_rail_01", "brace_02_08"}.issubset(base_nodes))
        self.assertTrue(
            {"deck_01", "front_rail_01", "brace_01_05"}.issubset(combined_nodes)
        )
        self.assertNotIn("deck_02", combined_nodes)
        self.assertNotIn("brace_02_01", combined_nodes)
        self.assertTrue(
            {"left_side", "right_side", "door_panel"}.issubset(combined_nodes)
        )
