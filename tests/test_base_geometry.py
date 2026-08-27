"""Scope: Verify the structural base closes its bounds without collisions."""

from __future__ import annotations

from importlib.util import find_spec
import unittest

from base_review_test_case import BaseReviewTestCase


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBaseGeometry(BaseReviewTestCase):
    """Protect the base's physical bounds and part-to-part contact."""

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

    def _bounding_overlap_volume(self, left, right) -> float:
        lengths = (
            max(0.0, min(left.xmax, right.xmax) - max(left.xmin, right.xmin)),
            max(0.0, min(left.ymax, right.ymax) - max(left.ymin, right.ymin)),
            max(0.0, min(left.zmax, right.zmax) - max(left.zmin, right.zmin)),
        )
        return lengths[0] * lengths[1] * lengths[2]
