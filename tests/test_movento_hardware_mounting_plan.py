"""Scope: Verify MOVENTO native frames resolve from cabinet and drawer datums."""

from types import SimpleNamespace

from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening, DrawerBoxSizingProfile
from movento_hardware_mounting_planner import MoventoHardwareMountingPlanner
from movento_mounting_profile import MOVENTO_760H5000S_MOUNTING


class TestMoventoHardwareMountingPlan:
    """Protect the shared handed frame and the 21 mm inside-face relationship."""

    def test_aligns_runner_and_lock_origins_after_child_placement(self) -> None:
        drawer = DrawerBoxPlanner().plan(
            CabinetDrawerOpening(707.0, 564.0),
            DrawerBoxSizingProfile(runner_length_mm=500.0),
        )
        cabinet = SimpleNamespace(
            width_mm=743.0,
            part=lambda part_id: SimpleNamespace(local_size_mm=(0.0, 0.0, 18.0)),
        )
        child_origin = (24.0, 18.0, 456.0)

        plan = MoventoHardwareMountingPlanner().plan(
            cabinet,
            drawer,
            child_origin,
            MOVENTO_760H5000S_MOUNTING,
        )

        self._assert_same_parent_origin(
            plan.runner_left_in_cabinet.origin_mm,
            child_origin,
            plan.locking_device_left_in_drawer.origin_mm,
        )
        self._assert_same_parent_origin(
            plan.runner_right_in_cabinet.origin_mm,
            child_origin,
            plan.locking_device_right_in_drawer.origin_mm,
        )
        assert plan.locking_device_left_in_drawer.origin_mm[0] == -6.0
        assert plan.locking_device_right_in_drawer.origin_mm[0] == 701.0

    def test_maps_native_depth_and_height_into_aikea_axes(self) -> None:
        profile = MOVENTO_760H5000S_MOUNTING

        assert profile.native_x_in_owner == (1.0, 0.0, 0.0)
        assert profile.native_y_in_owner == (0.0, 0.0, 1.0)
        assert profile.native_z_in_owner == (0.0, -1.0, 0.0)
        assert profile.runner_screw_native_z_mm == (0.0, -256.0)
        assert profile.drawer_front_to_manufacturer_origin_mm == 37.0
        assert profile.drawer_bottom_to_manufacturer_origin_mm == 9.575

    def _assert_same_parent_origin(self, runner, child, locking_device) -> None:
        composed = tuple(parent + local for parent, local in zip(child, locking_device))
        assert composed == runner
