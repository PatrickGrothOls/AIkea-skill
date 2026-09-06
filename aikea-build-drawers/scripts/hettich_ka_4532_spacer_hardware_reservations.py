"""Scope: Reserve the exact placed KA 4532 and 13952 envelope per hand."""

from __future__ import annotations

from typing import Any

from hettich_ka_4532_spacer_mounting_plan import HettichKa4532SpacerMountingPlan
from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSet
from panel_hardware_reservation import PanelHardwareReservation


class HettichKa4532SpacerHardwareReservations:
    """Keep paired runner-spacer envelopes distinct from inferred machining."""

    HARDWARE_KIND = "drawer_runner_with_spacer"
    _SIDES = ("left", "right")
    _PLACEMENT_TOLERANCE_MM = 0.01

    def build(
        self,
        drawer_id: str,
        mounting: HettichKa4532SpacerMountingPlan,
        step_set: HettichKa4532SpacerStepSet,
    ) -> tuple[PanelHardwareReservation, ...]:
        return tuple(
            self._reservation(drawer_id, side, mounting, step_set)
            for side in self._SIDES
        )

    def owner_id(self, drawer_id: str, side: str) -> str:
        return f"{drawer_id}_{side}_ka_4532_with_13952"

    def _reservation(
        self,
        drawer_id: str,
        side: str,
        mounting: HettichKa4532SpacerMountingPlan,
        step_set: HettichKa4532SpacerStepSet,
    ) -> PanelHardwareReservation:
        bounds = self._side_bounds(side, mounting, step_set)
        return PanelHardwareReservation(
            owner_id=self.owner_id(drawer_id, side),
            hardware_kind=self.HARDWARE_KIND,
            side_part_id=f"{side}_side",
            system_32_node_rows_mm=(),
            depth_interval_mm=self._interval(
                bounds,
                "ymin",
                "ymax",
                -mounting.cabinet_front_mm,
            ),
            height_interval_mm=self._interval(bounds, "zmin", "zmax"),
        )

    def _side_bounds(
        self,
        side: str,
        mounting: HettichKa4532SpacerMountingPlan,
        step_set: HettichKa4532SpacerStepSet,
    ) -> tuple[Any, ...]:
        runner = getattr(step_set, f"runner_{side}")
        drawer_origin = mounting.drawer_origin_mm
        return (
            self._placed_bounds(
                step_set.spacer_solid,
                getattr(mounting, f"spacer_{side}_in_cabinet"),
            ),
            self._placed_bounds(
                runner.fixed_member,
                getattr(mounting, f"fixed_runner_{side}_in_cabinet"),
            ),
            self._placed_bounds(
                runner.moving_member,
                getattr(mounting, f"moving_runner_{side}_in_drawer"),
                drawer_origin,
            ),
        )

    def _placed_bounds(
        self,
        shape: Any,
        placement: Any,
        owner_origin_mm: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Any:
        import cadquery as cq

        owner = cq.Location(cq.Vector(*owner_origin_mm))
        local = cq.Location(
            cq.Plane(
                origin=placement.origin_mm,
                xDir=placement.local_x_in_owner,
                normal=placement.local_z_in_owner,
            )
        )
        return shape.located(cq.Location()).located(
            owner * local * shape.location()
        ).BoundingBox()

    def _interval(
        self,
        bounds: tuple[Any, ...],
        minimum_name: str,
        maximum_name: str,
        offset_mm: float = 0.0,
    ) -> tuple[float, float]:
        return (
            min(getattr(bound, minimum_name) for bound in bounds)
            + offset_mm
            - self._PLACEMENT_TOLERANCE_MM,
            max(getattr(bound, maximum_name) for bound in bounds)
            + offset_mm
            + self._PLACEMENT_TOLERANCE_MM,
        )


__all__ = ["HettichKa4532SpacerHardwareReservations"]
