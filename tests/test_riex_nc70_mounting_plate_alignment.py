"""Scope: Lock left- and right-hand Riex plates to the cabinet System 32 grid."""

from __future__ import annotations

from importlib.util import find_spec
import unittest

CADQUERY_AVAILABLE = find_spec("cadquery") is not None

if CADQUERY_AVAILABLE:
    from door_hinge_side import DoorHingeSide
    from riex_nc70_alignment_test_case import RiexNc70AlignmentTestCase
    from system_32_side_panel_grid import System32SidePanelGrid
else:
    RiexNc70AlignmentTestCase = unittest.TestCase


@unittest.skipUnless(CADQUERY_AVAILABLE, "requires the project's CadQuery environment")
class TestRiexNc70MountingPlateAlignment(RiexNc70AlignmentTestCase):
    def test_left_plate_axes_match_the_system_32_pair(self) -> None:
        source_axes = self._source_axes(DoorHingeSide.LEFT)
        rows = System32SidePanelGrid().adjacent_row_pairs_mm(1000.0)[12]
        expected = tuple((18.0, 37.0, row_mm) for row_mm in rows)

        self.assertEqual(rows, (484.0, 516.0))
        self.assert_axes_match(self.sort_axes(source_axes), expected)

    def test_right_plate_axes_match_the_right_system_32_pair(self) -> None:
        source_axes = self._source_axes(DoorHingeSide.RIGHT)
        expected = ((982.0, 37.0, 484.0), (982.0, 37.0, 516.0))

        self.assert_axes_match(self.sort_axes(source_axes), expected)

    def _source_axes(
        self,
        hinge_side: DoorHingeSide,
    ) -> tuple[tuple[float, float, float], ...]:
        location = self.placement.plate_location(
            self.assembly,
            self.profile,
            self.HINGE_CENTER_Z_MM,
            hinge_side,
        )
        return tuple(
            self.global_point(
                location,
                source_x_mm,
                self.profile.plate_native_panel_face_y_mm,
                self.profile.plate_native_fixing_axis_z_mm,
            )
            for source_x_mm in (8.693877, 40.693877)
        )


if __name__ == "__main__":
    unittest.main()
