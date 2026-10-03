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

        self.assertEqual(len(parts), 4)
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

    def test_kickboard_meets_deck_and_base_owns_adjustable_feet(self):
        built = self.generator.loader.load_assembly(self.project_root,"base_01")
        parts = self.generator.base_geometry.build(built)
        front = next(p for p in parts if p.name == "kickboard_01")
        deck = next(p for p in parts if p.name == "deck_01")
        self.assertAlmostEqual(front.placed_shape().BoundingBox().zmax,deck.placed_shape().BoundingBox().zmin)
        self.assertGreater(len(built.purchased_hardware),0)
        self.assertEqual({p.spec.product_code for p in built.purchased_hardware},{"61854","70151"})

    def _bounding_overlap_volume(self, left, right) -> float:
        lengths = (
            max(0.0, min(left.xmax, right.xmax) - max(left.xmin, right.xmin)),
            max(0.0, min(left.ymax, right.ymax) - max(left.ymin, right.ymin)),
            max(0.0, min(left.zmax, right.zmax) - max(left.zmin, right.zmin)),
        )
        return lengths[0] * lengths[1] * lengths[2]
