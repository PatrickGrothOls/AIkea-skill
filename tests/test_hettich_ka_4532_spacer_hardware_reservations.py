"""Scope: Verify exact placed KA 4532 and 13952 panel reservations."""

from importlib.util import find_spec
from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.skipif(find_spec("cadquery") is None, reason="requires CadQuery")

if find_spec("cadquery") is not None:
    import cadquery as cq

from drawer_hardware_mounting_plan import HardwarePlacement
from hettich_ka_4532_spacer_mounting_plan import HettichKa4532SpacerMountingPlan
from panel_hardware_reservation import PanelHardwareReservation
from hettich_ka_4532_spacer_hardware_reservations import (
    HettichKa4532SpacerHardwareReservations,
)


class TestHettichKa4532SpacerHardwareReservations:
    """Protect exact combined envelopes without inferring fixing holes."""

    def test_reserves_exact_combined_non_system32_envelope_per_side(self) -> None:
        reservations = HettichKa4532SpacerHardwareReservations().build(
            "drawer_01",
            self._mounting(),
            self._step_set(),
        )

        assert tuple(item.owner_id for item in reservations) == (
            "drawer_01_left_ka_4532_with_13952",
            "drawer_01_right_ka_4532_with_13952",
        )
        assert tuple(item.side_part_id for item in reservations) == (
            "left_side",
            "right_side",
        )
        assert all(
            item.hardware_kind == "drawer_runner_with_spacer"
            and item.system_32_node_rows_mm == ()
            and item.depth_interval_mm == pytest.approx((1.99, 525.05))
            and item.height_interval_mm == pytest.approx((97.99, 148.01))
            for item in reservations
        )

    def test_normalizes_exact_bounds_to_the_cabinet_front(self) -> None:
        reservations = HettichKa4532SpacerHardwareReservations().build(
            "drawer_01",
            self._mounting(cabinet_front_mm=50.0, drawer_front_mm=68.0),
            self._step_set(),
        )

        assert all(
            item.depth_interval_mm == pytest.approx((1.99, 525.05))
            for item in reservations
        )

    def test_exact_trailing_edge_conflicts_with_hinge_space(self) -> None:
        runner = HettichKa4532SpacerHardwareReservations().build(
            "drawer_01",
            self._mounting(),
            self._step_set(),
        )[0]
        hinge = PanelHardwareReservation(
            owner_id="hinge_01",
            hardware_kind="hinge_plate",
            side_part_id="left_side",
            system_32_node_rows_mm=(),
            depth_interval_mm=(520.0, 530.0),
            height_interval_mm=(120.0, 172.0),
        )

        assert runner.conflicts_with(hinge)

    def _mounting(
        self,
        cabinet_front_mm: float = 0.0,
        drawer_front_mm: float = 18.0,
    ) -> HettichKa4532SpacerMountingPlan:
        fixed = self._placement((0.0, cabinet_front_mm + 11.5, 123.0))
        moving = self._placement((0.0, 11.5, 23.0))
        left_spacer = self._placement((18.0, cabinet_front_mm + 10.0, 98.0))
        right_spacer = HardwarePlacement(
            (577.0, cabinet_front_mm + 10.0, 148.0),
            (-1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, -1.0),
        )
        return HettichKa4532SpacerMountingPlan(
            cabinet_front_mm=cabinet_front_mm,
            drawer_front_mm=drawer_front_mm,
            drawer_origin_mm=(55.7, drawer_front_mm, 100.0),
            drawer_outside_width_mm=483.6,
            spacer_left_in_cabinet=left_spacer,
            spacer_right_in_cabinet=right_spacer,
            fixed_runner_left_in_cabinet=fixed,
            fixed_runner_right_in_cabinet=fixed,
            moving_runner_left_in_drawer=moving,
            moving_runner_right_in_drawer=moving,
        )

    def _step_set(self):
        fixed = self._box(12.7, 502.483917, 45.7, (0.0, -9.5, -22.85))
        moving = self._box(12.7, 505.04, 45.7, (0.0, -9.5, -22.85))
        spacer = self._box(25.0, 486.0, 50.0, (0.0, 0.0, 0.0))
        return SimpleNamespace(
            runner_left=SimpleNamespace(fixed_member=fixed, moving_member=moving),
            runner_right=SimpleNamespace(fixed_member=fixed, moving_member=moving),
            spacer_solid=spacer,
        )

    def _box(self, x_mm, y_mm, z_mm, origin_mm):
        return cq.Solid.makeBox(x_mm, y_mm, z_mm, cq.Vector(*origin_mm))

    def _placement(self, origin_mm):
        return HardwarePlacement(
            origin_mm,
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )
