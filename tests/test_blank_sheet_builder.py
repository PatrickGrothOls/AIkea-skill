"""Scope: Verify the review skill's BlankSheetBuilder creates its local workpiece."""

from __future__ import annotations

from importlib.util import find_spec
import unittest


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBlankSheetBuilder(unittest.TestCase):
    """Prove diverse calculated flat outlines become valid sheet solids."""

    def test_builds_the_calculated_shape_families(self) -> None:
        from blank_sheet_builder import BlankSheetBuilder

        shapes = {
            "rectangle": ((0, 0), (582, 0), (582, 2284), (0, 2284)),
            "sloped": ((0, 0), (1000, 0), (1000, 1800), (0, 2284)),
            "flat_to_slope": (
                (0, 0),
                (1500, 0),
                (1500, 1200),
                (700, 2284),
                (0, 2284),
            ),
            "stepped": (
                (0, 0),
                (1200, 0),
                (1200, 900),
                (800, 900),
                (800, 1700),
                (0, 1700),
            ),
            "concave": (
                (0, 0),
                (1200, 0),
                (1200, 1700),
                (700, 1700),
                (700, 800),
                (400, 800),
                (400, 1700),
                (0, 1700),
            ),
            "reversed": ((0, 2284), (582, 2284), (582, 0), (0, 0)),
        }

        for name, outline in shapes.items():
            with self.subTest(shape=name):
                self._assert_outline(BlankSheetBuilder, outline, 18.0)

    def test_rectangle_short_form_uses_the_same_outline_contract(self) -> None:
        from blank_sheet_builder import BlankSheetBuilder

        outline = ((0.0, 0.0), (582.0, 0.0), (582.0, 2284.0), (0.0, 2284.0))
        blank = BlankSheetBuilder.rectangle(582.0, 2284.0, 18.0).build().val()
        outlined = BlankSheetBuilder(outline, 18.0).build().val()

        self.assertAlmostEqual(blank.Volume(), 582.0 * 2284.0 * 18.0)
        self.assertAlmostEqual(blank.cut(outlined).Volume(), 0.0)
        self.assertAlmostEqual(outlined.cut(blank).Volume(), 0.0)
        self.assertTrue(blank.isValid())

    def _assert_outline(self, builder_class, outline, thickness_mm: float) -> None:
        solid = builder_class(tuple(outline), thickness_mm).build().val()
        bounds = solid.BoundingBox()
        x_values = [point[0] for point in outline]
        y_values = [point[1] for point in outline]

        self.assertAlmostEqual(bounds.xmin, min(x_values))
        self.assertAlmostEqual(bounds.xmax, max(x_values))
        self.assertAlmostEqual(bounds.ymin, min(y_values))
        self.assertAlmostEqual(bounds.ymax, max(y_values))
        self.assertAlmostEqual(bounds.zmin, 0.0)
        self.assertAlmostEqual(bounds.zmax, thickness_mm)
        self.assertAlmostEqual(solid.Volume(), self._outline_area(outline) * thickness_mm)
        self.assertEqual(len(solid.Solids()), 1)
        self.assertTrue(solid.isValid())

    def _outline_area(self, outline) -> float:
        paired = zip(outline, outline[1:] + outline[:1])
        signed_twice_area = sum(
            start[0] * end[1] - end[0] * start[1]
            for start, end in paired
        )
        return abs(signed_twice_area) / 2.0


if __name__ == "__main__":
    unittest.main()
