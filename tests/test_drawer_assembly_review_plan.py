"""Scope: Verify drawer review overlays replace only drawer-owned hardware."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from drawer_assembly_review_plan import DrawerAssemblyReviewPlanBuilder
from drawer_review_state import DrawerReviewState


class TestDrawerAssemblyReviewPlan:
    """Keep door and lighting hardware visible beside drawer review geometry."""

    @pytest.mark.parametrize(
        "state",
        (
            DrawerReviewState.CLOSED,
            DrawerReviewState.OPEN,
            DrawerReviewState.REMOVED,
        ),
    )
    def test_hides_only_hardware_replaced_by_the_drawer_overlay(self, state) -> None:
        plan = DrawerAssemblyReviewPlanBuilder().build(
            self._cabinet(),
            state,
            ("drawer overlay",),
        )
        cabinet = ("wardrobe_01", "cabinet_01")
        drawer = cabinet + ("drawer_01",)

        assert plan.hides(cabinet + ("hardware:runner_left",))
        assert plan.hides(cabinet + ("hardware:runner_right",))
        assert plan.hides(drawer + ("hardware:locking_device_left",))
        assert plan.hides(drawer + ("hardware:locking_device_right",))
        assert not plan.hides(cabinet + ("hardware:door_hinge_left",))
        assert not plan.hides(cabinet + ("hardware:light_driver",))
        assert plan.hides(drawer + ("hardware:drawer_sensor",)) is (
            state is DrawerReviewState.REMOVED
        )

    def _cabinet(self):
        drawer = SimpleNamespace(
            spec=SimpleNamespace(
                assembly_id="drawer_01",
                purpose="drawer",
            ),
            assembly=SimpleNamespace(
                spec=SimpleNamespace(
                    box=SimpleNamespace(side_length_mm=500.0),
                ),
                purchased_hardware=self._hardware(
                    "locking_device_left",
                    "locking_device_right",
                    "drawer_sensor",
                ),
            ),
        )
        return SimpleNamespace(
            spec=SimpleNamespace(assembly_id="cabinet_01"),
            child_assemblies=(drawer,),
            purchased_hardware=self._hardware(
                "runner_left",
                "runner_right",
                "door_hinge_left",
                "light_driver",
            ),
        )

    def _hardware(self, *hardware_ids):
        return tuple(
            SimpleNamespace(spec=SimpleNamespace(hardware_id=hardware_id))
            for hardware_id in hardware_ids
        )


__all__ = ["TestDrawerAssemblyReviewPlan"]
