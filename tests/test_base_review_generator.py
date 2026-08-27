"""Scope: Verify the structural base and first cabinet export as physical GLBs."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from test_unit_mockup_generator import GlbTestDocument


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBaseReviewGenerator(unittest.TestCase):
    """Protect base placement, cabinet contact, and named review exports."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def setUp(self) -> None:
        from base_review_generator import BaseReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.generator = BaseReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_base_parts_close_the_complete_base_bounds_without_overlap(self) -> None:
        built_base = self.generator.loader.load_assembly(self.project_root, "base_01")
        parts = self.generator.base_geometry.build(built_base)
        bounds = [part.placed_shape().BoundingBox() for part in parts]

        self.assertEqual(len(parts), 19)
        self.assertAlmostEqual(min(bound.xmin for bound in bounds), 0.0)
        self.assertAlmostEqual(max(bound.xmax for bound in bounds), 2978.0)
        self.assertAlmostEqual(min(bound.ymin for bound in bounds), 0.0)
        self.assertAlmostEqual(max(bound.ymax for bound in bounds), 582.0)
        self.assertAlmostEqual(min(bound.zmin for bound in bounds), 0.0)
        self.assertAlmostEqual(max(bound.zmax for bound in bounds), 100.0)
        for index, left in enumerate(parts):
            for right in parts[index + 1:]:
                self.assertAlmostEqual(
                    self._bounding_overlap_volume(
                        left.placed_shape().BoundingBox(),
                        right.placed_shape().BoundingBox(),
                    ),
                    0.0,
                )

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

    def test_braces_close_between_both_rails_and_bear_the_deck(self) -> None:
        built_base = self.generator.loader.load_assembly(self.project_root, "base_01")
        parts = self.generator.base_geometry.build(built_base)
        front = next(part for part in parts if part.name == "front_rail_01")
        back = next(part for part in parts if part.name == "back_rail_01")
        brace = next(part for part in parts if part.name == "brace_01_03")
        deck = next(part for part in parts if part.name == "deck_01")
        front_bounds = front.placed_shape().BoundingBox()
        back_bounds = back.placed_shape().BoundingBox()
        brace_bounds = brace.placed_shape().BoundingBox()
        deck_bounds = deck.placed_shape().BoundingBox()

        self.assertAlmostEqual(front_bounds.ymax, brace_bounds.ymin)
        self.assertAlmostEqual(brace_bounds.ymax, back_bounds.ymin)
        self.assertAlmostEqual(brace_bounds.zmax, deck_bounds.zmin)

    def test_exports_named_base_and_combined_glbs(self) -> None:
        result = self.generator.generate(self.project_root, self.project)
        base_nodes = GlbTestDocument(result.base_glb_path).node_names
        combined_nodes = GlbTestDocument(result.cabinet_with_base_glb_path).node_names

        self.assertTrue({"deck_01", "front_rail_01", "brace_02_08"}.issubset(base_nodes))
        self.assertTrue(
            {"deck_01", "front_rail_01", "brace_01_05"}.issubset(combined_nodes)
        )
        self.assertNotIn("deck_02", combined_nodes)
        self.assertTrue(
            {"left_side", "right_side", "door_panel"}.issubset(combined_nodes)
        )

    def _bounding_overlap_volume(self, left, right) -> float:
        lengths = (
            max(0.0, min(left.xmax, right.xmax) - max(left.xmin, right.xmin)),
            max(0.0, min(left.ymax, right.ymax) - max(left.ymin, right.ymin)),
            max(0.0, min(left.zmax, right.zmax) - max(left.zmin, right.zmin)),
        )
        return lengths[0] * lengths[1] * lengths[2]


if __name__ == "__main__":
    unittest.main()
