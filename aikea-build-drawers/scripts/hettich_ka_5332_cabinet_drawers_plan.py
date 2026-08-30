"""Scope: Validate any number of KA 5332 drawer children in one cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cabinet_drawer_plan import DrawerLayout
from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
    HettichKa5332CabinetDrawerPlanner,
)
from hettich_ka_5332_step_assembly import HettichKa5332StepAssembly
from panel_hardware_reservation import PanelHardwareReservation


class HettichKa5332CabinetDrawersPlanError(ValueError):
    """Report drawer children that cannot coexist in their cabinet."""


@dataclass(frozen=True, slots=True)
class HettichKa5332CabinetDrawersPlan:
    """Keep an arbitrary cabinet-owned drawer collection together."""

    parent_assembly_id: str
    drawers: tuple[HettichKa5332CabinetDrawerPlan, ...]
    hardware_reservations: tuple[PanelHardwareReservation, ...]


class HettichKa5332CabinetDrawersPlanner:
    """Resolve independent drawer layouts and reject duplicate or overlapping children."""

    def __init__(
        self,
        drawer_planner: HettichKa5332CabinetDrawerPlanner | None = None,
    ) -> None:
        self.drawer_planner = drawer_planner or HettichKa5332CabinetDrawerPlanner()

    def plan(
        self,
        cabinet: Any,
        layouts: tuple[DrawerLayout, ...],
        hardware_step: HettichKa5332StepAssembly,
        blocked_reservations: tuple[PanelHardwareReservation, ...] = (),
    ) -> HettichKa5332CabinetDrawersPlan:
        if not layouts:
            raise HettichKa5332CabinetDrawersPlanError(
                "a cabinet drawer collection cannot be empty"
            )
        drawer_ids = tuple(layout.drawer_id for layout in layouts)
        if len(set(drawer_ids)) != len(drawer_ids):
            raise HettichKa5332CabinetDrawersPlanError(
                "drawer IDs must be unique inside one cabinet"
            )
        drawers: list[HettichKa5332CabinetDrawerPlan] = []
        reservations = list(blocked_reservations)
        for layout in layouts:
            drawer = self.drawer_planner.plan(
                cabinet,
                layout,
                hardware_step,
                tuple(reservations),
            )
            drawers.append(drawer)
            reservations.extend(drawer.hardware_reservations)
        resolved_drawers = tuple(drawers)
        self._require_separate_vertical_spans(resolved_drawers)
        return HettichKa5332CabinetDrawersPlan(
            cabinet.assembly_id,
            resolved_drawers,
            tuple(reservations),
        )

    def _require_separate_vertical_spans(
        self,
        drawers: tuple[HettichKa5332CabinetDrawerPlan, ...],
    ) -> None:
        ordered = sorted(drawers, key=lambda plan: plan.origin_in_parent_mm[2])
        for lower, upper in zip(ordered, ordered[1:]):
            lower_top_mm = (
                lower.origin_in_parent_mm[2]
                + lower.drawer.box.sizing.box_height_mm
            )
            if lower_top_mm > upper.origin_in_parent_mm[2]:
                raise HettichKa5332CabinetDrawersPlanError(
                    f"{lower.drawer.assembly_id} overlaps {upper.drawer.assembly_id}"
                )


__all__ = [
    "HettichKa5332CabinetDrawersPlan",
    "HettichKa5332CabinetDrawersPlanError",
    "HettichKa5332CabinetDrawersPlanner",
]
