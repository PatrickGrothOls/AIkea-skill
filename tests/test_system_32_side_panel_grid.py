"""Scope: Prove the shared System 32 side-panel grid aligns and remains blind."""

from __future__ import annotations

from importlib.util import find_spec
from math import pi
from types import SimpleNamespace
import unittest

from system_32_side_panel_grid import System32SidePanelGrid


class TestSystem32SidePanelGrid(unittest.TestCase):
    """Protect the cabinet-owned hardware grid used by multiple fittings."""

    def setUp(self) -> None:
        self.grid = System32SidePanelGrid()

    def test_rows_share_one_bottom_reference_on_unequal_height_panels(self) -> None:
        shorter_rows = self.grid.row_heights_mm(2011.0)
        taller_rows = self.grid.row_heights_mm(2295.0)

        self.assertEqual(taller_rows[: len(shorter_rows)], shorter_rows)
        self.assertEqual(shorter_rows[0], 100.0)
        self.assertEqual(shorter_rows[1] - shorter_rows[0], 32.0)
        self.assertLessEqual(shorter_rows[-1], 2011.0 - 100.0)

    def test_adjacent_pair_matches_system_32_mounting_plate(self) -> None:
        first_pair = self.grid.adjacent_row_pairs_mm(2295.0)[0]

        self.assertEqual(first_pair, (100.0, 132.0))

    def test_columns_use_fixed_system_32_setbacks_at_every_depth(self) -> None:
        self.assertEqual(self.grid.column_positions_mm(356.0), (37.0, 319.0))
        self.assertEqual(self.grid.column_positions_mm(564.0), (37.0, 527.0))

    @unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
    def test_generated_side_builder_applies_blind_holes_automatically(self) -> None:
        from part_blank_builder import PartBlankBuilder
        from sheet_part_builder import SheetPartBuilder

        part = SimpleNamespace(
            role="side_panel",
            dimensions_mm=(("depth", 356.0), ("height", 2295.0), ("thickness", 18.0)),
            outline_mm=(),
            inside_face=">Z",
        )
        blank = PartBlankBuilder().build(part)
        machined = SheetPartBuilder().build(part, ())
        removed = blank.val().cut(machined.val())
        expected_holes = len(self.grid.row_heights_mm(2295.0)) * 2
        expected_volume = expected_holes * pi * (2.5**2) * 13.0

        self.assertTrue(machined.val().isValid())
        self.assertAlmostEqual(blank.val().Volume() - machined.val().Volume(), expected_volume, places=3)
        self.assertAlmostEqual(removed.BoundingBox().zmin, 5.0, places=5)
        self.assertAlmostEqual(removed.BoundingBox().zmax, 18.0, places=5)


if __name__ == "__main__":
    unittest.main()
