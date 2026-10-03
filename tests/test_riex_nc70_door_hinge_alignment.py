"""Scope: Lock left- and right-hand Riex door CAD to matching cup machining."""

from __future__ import annotations

from importlib.util import find_spec
import unittest

CADQUERY_AVAILABLE = find_spec("cadquery") is not None

if CADQUERY_AVAILABLE:
    from concealed_hinge_machining import ConcealedHingeMachining
    from door_hinge_side import DoorHingeSide
    from riex_nc70_alignment_test_case import RiexNc70AlignmentTestCase
else:
    RiexNc70AlignmentTestCase = unittest.TestCase


@unittest.skipUnless(CADQUERY_AVAILABLE, "requires the project's CadQuery environment")
class TestRiexNc70DoorHingeAlignment(RiexNc70AlignmentTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.machining = ConcealedHingeMachining()

    def test_left_hardware_axes_match_cup_and_fixing_holes(self) -> None:
        source_axes = self._source_axes(DoorHingeSide.LEFT)

        self.assertEqual(self.profile.cup_center_from_edge_mm, 23.5)
        self.assertEqual(self.profile.cup_fixing_line_from_edge_mm, 33.0)
        self.assertEqual(self.profile.native_door_surface_x_mm, -68.6)
        self.assert_axes_match(
            self.sort_axes(source_axes),
            self.sort_axes(self._door_machining_axes(DoorHingeSide.LEFT)),
        )

    def test_right_hardware_axes_match_right_edge_machining(self) -> None:
        self.assert_axes_match(
            self.sort_axes(self._source_axes(DoorHingeSide.RIGHT)),
            self.sort_axes(self._door_machining_axes(DoorHingeSide.RIGHT)),
        )

    def _source_axes(
        self,
        hinge_side: DoorHingeSide,
    ) -> tuple[tuple[float, float, float], ...]:
        location = self.placement.hinge_location(
            self.assembly,
            self.profile,
            self.HINGE_CENTER_Z_MM,
            hinge_side,
        )
        return (
            self.global_point(
                location,
                self.profile.native_door_surface_x_mm,
                self.profile.native_cup_center_y_mm,
                0.0,
            ),
            *(
                self.global_point(
                    location,
                    self.profile.native_door_surface_x_mm,
                    self.profile.native_fixing_center_y_mm,
                    z_mm,
                )
                for z_mm in (-22.5, 22.5)
            ),
        )

    def _door_machining_axes(
        self,
        hinge_side: DoorHingeSide,
    ) -> tuple[tuple[float, float, float], ...]:
        cutter = self.machining._door_cutter(
            self.HINGE_CENTER_Z_MM,
            self.profile,
            hinge_side,
            self.assembly.door_width_mm,
        )
        cylinders = tuple(
            face._geomAdaptor().Cylinder()
            for face in cutter.val().Faces()
            if face.geomType() == "CYLINDER"
        )
        cup = next(item for item in cylinders if item.Radius() == 17.5)
        fixings = tuple(item for item in cylinders if item.Radius() == 1.25)
        left_gap_mm = (
            self.assembly.width_mm - self.assembly.door_width_mm
        ) / 2.0
        return tuple(
            (
                left_gap_mm + item.Axis().Location().X(),
                0.0,
                item.Axis().Location().Y(),
            )
            for item in (cup, *fixings)
        )


if __name__ == "__main__":
    unittest.main()
