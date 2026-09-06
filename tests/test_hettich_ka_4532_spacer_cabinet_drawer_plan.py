"""Scope: Verify one exact KA 4532 spacer drawer planning gate."""

from importlib.util import find_spec

import pytest

pytestmark = pytest.mark.skipif(find_spec("cadquery") is None, reason="requires CadQuery")

from cabinet_drawer_plan import DrawerLayout
if find_spec("cadquery") is not None:
    from hettich_ka_4532_spacer_cabinet_drawer_planner import (
        HettichKa4532SpacerCabinetDrawerPlanner,
        MACHINING_AUTHORITY_BLOCKED,
    )
from hettich_ka_4532_spacer_mounting_test_support import (
    HettichKa4532SpacerMountingTestSupport,
)
from panel_hardware_reservation import PanelHardwareReservation


class TestHettichKa4532SpacerCabinetDrawerPlan:
    """Protect exact-product fit, placement, and first-proof limits."""

    _FIXTURE = HettichKa4532SpacerMountingTestSupport()

    def test_resolves_one_exact_drawer_and_keeps_machining_blocked(self) -> None:
        plan = self._plan()

        assert plan.parent_assembly_id == "tall_storage_01"
        assert plan.origin_in_parent_mm == (55.7, 18.0, 177.0)
        assert plan.drawer.box.outside_width_mm == pytest.approx(483.6)
        assert plan.drawer.box.outside_depth_mm == 530.0
        assert plan.hardware.runner_item_number == "9114276"
        assert plan.hardware.spacer_item_number == "13952"
        assert plan.hardware.combined_load_capacity_kg == 20.0
        assert plan.fixing_alignment.cabinet_depth_axes_mm == (
            37.0,
            165.0,
            261.0,
            325.0,
        )
        assert plan.machining_authority == MACHINING_AUTHORITY_BLOCKED
        assert tuple(item.hardware_kind for item in plan.hardware_reservations) == (
            "drawer_runner_with_spacer",
            "drawer_runner_with_spacer",
        )

    def test_rejects_unregistered_depth_and_shallow_cabinet(self) -> None:
        with pytest.raises(ValueError, match="exact 500 mm"):
            self._plan(layout=DrawerLayout("drawer_01", 77.0, box_depth_mm=450.0))

        cabinet = self._FIXTURE.cabinet()
        cabinet.inside_depth_mm = 503.0
        with pytest.raises(ValueError, match="requires 504 mm"):
            self._plan(cabinet=cabinet)

    def test_rejects_repetition_before_the_first_real_cabinet_proof(self) -> None:
        existing = self._plan(
            layout=DrawerLayout("drawer_02", 300.0, box_depth_mm=500.0)
        ).hardware_reservations

        with pytest.raises(ValueError, match="repetition remains disabled"):
            self._plan(existing=existing)

    def test_rejects_an_overlapping_hinge_reservation(self) -> None:
        hinge = PanelHardwareReservation(
            owner_id="hinge_01",
            hardware_kind="hinge_plate",
            side_part_id="left_side",
            system_32_node_rows_mm=(132.0, 164.0),
            depth_interval_mm=(19.0, 64.0),
            height_interval_mm=(150.0, 202.0),
        )

        with pytest.raises(ValueError, match="conflicts with hinge_01"):
            self._plan(existing=(hinge,))

    def _plan(self, cabinet=None, layout=None, existing=()):
        return HettichKa4532SpacerCabinetDrawerPlanner().plan(
            cabinet or self._FIXTURE.cabinet(),
            layout or DrawerLayout("drawer_01", 77.0, box_depth_mm=500.0),
            self._FIXTURE.step_set(),
            existing,
            cabinet_front_mm=0.0,
            drawer_front_mm=18.0,
        )


__all__ = ["TestHettichKa4532SpacerCabinetDrawerPlan"]
