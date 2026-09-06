"""Scope: Protect exact two-sided KA 4532 and 13952 mounting transforms."""

from importlib.util import find_spec

import pytest

pytestmark = pytest.mark.skipif(find_spec("cadquery") is None, reason="requires CadQuery")

if find_spec("cadquery") is not None:
    from hettich_ka_4532_spacer_mounting_planner import (
        HettichKa4532SpacerMountingPlanner,
    )
from hettich_ka_4532_spacer_mounting_test_support import (
    HettichKa4532SpacerMountingTestSupport,
)


class TestHettichKa4532SpacerMountingPlan:
    """Verify cabinet-face datums without generated replacement geometry."""

    _FIXTURE = HettichKa4532SpacerMountingTestSupport()

    def test_places_the_same_spacer_frame_on_both_inside_faces(self) -> None:
        plan = self._plan()
        left = plan.spacer_left_in_cabinet
        right = plan.spacer_right_in_cabinet

        assert left.origin_mm == (18.0, 10.0, 98.0)
        assert right.origin_mm == (577.0, 10.0, 148.0)
        assert self._axes(left) == self._identity_axes()
        assert self._axes(right) == (
            (-1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, -1.0),
        )
        assert self._determinant(self._axes(right)) == 1.0

    def test_aligns_runner_contacts_and_separate_front_datums(self) -> None:
        plan = self._plan()
        left_fixed = plan.fixed_runner_left_in_cabinet
        right_fixed = plan.fixed_runner_right_in_cabinet
        left_moving = plan.moving_runner_left_in_drawer
        right_moving = plan.moving_runner_right_in_drawer

        assert plan.drawer_origin_mm == (55.7, 18.0, 100.0)
        assert plan.drawer_outside_width_mm == pytest.approx(483.6)
        assert left_fixed.origin_mm == (43.0, 11.5, 123.0)
        assert right_fixed.origin_mm == (351.0, 11.5, 123.0)
        assert left_moving.origin_mm == pytest.approx((-12.7, 11.5, 23.0))
        assert right_moving.origin_mm == pytest.approx((295.3, 11.5, 23.0))
        assert left_fixed.origin_mm[0] + 0.0 == 43.0
        assert right_fixed.origin_mm[0] + 201.0 == 552.0
        assert plan.drawer_origin_mm[1] + left_moving.origin_mm[1] - 9.5 == 20.0
        assert plan.drawer_origin_mm[1] + right_moving.origin_mm[1] - 9.5 == 20.0

    def test_keeps_the_cabinet_and_drawer_front_datums_independent(self) -> None:
        plan = self._plan(drawer_front_mm=30.0)

        assert plan.drawer_origin_mm[1] == 30.0
        assert plan.spacer_left_in_cabinet.origin_mm[1] == 10.0
        assert plan.fixed_runner_left_in_cabinet.origin_mm[1] == 11.5
        assert (
            plan.drawer_origin_mm[1]
            + plan.moving_runner_left_in_drawer.origin_mm[1]
            - 9.5
        ) == 32.0

    def test_changed_side_part_frames_move_every_inside_face_datum(self) -> None:
        plan = self._plan(cabinet=self._FIXTURE.cabinet(7.0, 612.0))

        assert plan.spacer_left_in_cabinet.origin_mm[0] == 25.0
        assert plan.spacer_right_in_cabinet.origin_mm[0] == 594.0
        assert plan.fixed_runner_left_in_cabinet.origin_mm[0] == 50.0
        assert plan.fixed_runner_right_in_cabinet.origin_mm[0] == 368.0
        assert plan.drawer_origin_mm[0] == 62.7
        assert plan.drawer_outside_width_mm == pytest.approx(493.6)

    def _plan(self, drawer_front_mm: float = 18.0, cabinet=None):
        return HettichKa4532SpacerMountingPlanner().plan(
            cabinet or self._FIXTURE.cabinet(),
            self._FIXTURE.step_set(),
            cabinet_front_mm=0.0,
            drawer_front_mm=drawer_front_mm,
            drawer_bottom_mm=100.0,
        )

    def _axes(self, placement):
        return (
            placement.local_x_in_owner,
            placement.local_y_in_owner,
            placement.local_z_in_owner,
        )

    def _identity_axes(self):
        return (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

    def _determinant(self, axes):
        x_axis, y_axis, z_axis = axes
        return (
            x_axis[0] * (y_axis[1] * z_axis[2] - y_axis[2] * z_axis[1])
            - x_axis[1] * (y_axis[0] * z_axis[2] - y_axis[2] * z_axis[0])
            + x_axis[2] * (y_axis[0] * z_axis[1] - y_axis[1] * z_axis[0])
        )
