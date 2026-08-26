"""Scope: Verify the review skill's BlankSheetBuilder creates its local workpiece."""

from __future__ import annotations

from importlib.util import find_spec
import unittest


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBlankSheetBuilder(unittest.TestCase):
    """Keep the skill's first panel step deterministic and locally anchored."""

    def test_builds_the_calculated_rectangular_workpiece(self) -> None:
        from blank_sheet_builder import BlankSheetBuilder

        width_mm = 582.0
        height_mm = 2284.0
        thickness_mm = 18.0
        blank = BlankSheetBuilder(width_mm, height_mm, thickness_mm).build().val()
        bounds = blank.BoundingBox()

        self.assertAlmostEqual(bounds.xmin, 0.0)
        self.assertAlmostEqual(bounds.xmax, width_mm)
        self.assertAlmostEqual(bounds.ymin, 0.0)
        self.assertAlmostEqual(bounds.ymax, height_mm)
        self.assertAlmostEqual(bounds.zmin, 0.0)
        self.assertAlmostEqual(bounds.zmax, thickness_mm)
        self.assertAlmostEqual(blank.Volume(), width_mm * height_mm * thickness_mm)
        self.assertTrue(blank.isValid())


if __name__ == "__main__":
    unittest.main()
