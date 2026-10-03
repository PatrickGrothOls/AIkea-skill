"""Scope: Resolve an exact or grid-snapped KA 5332 runner height with reservations."""

from __future__ import annotations

from typing import Any

from hettich_ka_5332_hardware_reservations import (
    HettichKa5332HardwareReservations,
)
from hettich_ka_5332_runner_profile import HettichKa5332RunnerProfile
from panel_hardware_reservation import (
    PanelHardwareConflictError,
    PanelHardwareReservation,
    PanelHardwareReservationPlan,
)
from system_32_side_panel_grid import System32SidePanelGrid
from drawer_host import DrawerHost


class HettichKa5332System32RowError(ValueError):
    """Report that no common side-panel row can accept the runner pair."""


class HettichKa5332System32RowResolver:
    """Snap requested drawer height to the nearest compatible shared row."""

    def __init__(self) -> None:
        self.grid = System32SidePanelGrid()
        self.reservations = HettichKa5332HardwareReservations()
        self.compatibility = PanelHardwareReservationPlan()

    def resolve(
        self,
        cabinet: Any,
        drawer_id: str,
        requested_bottom_height_mm: float,
        runner: HettichKa5332RunnerProfile,
        blocked: tuple[PanelHardwareReservation, ...] = (),
    ) -> float:
        host = DrawerHost.resolve(cabinet)
        world_rows = [{round(host.frame(side).origin_mm[2] + row, 6)
                       for row in self.grid.row_heights_mm(host.part(side).local_size_mm[1])}
                      for side in ("left", "right")]
        requested = host.spec.bottom_mm + requested_bottom_height_mm + runner.runner_center_from_drawer_bottom_mm
        for height in sorted(world_rows[0] & world_rows[1], key=lambda row: (abs(row-requested), row)):
            if height - runner.runner_center_from_drawer_bottom_mm < host.spec.bottom_mm:
                continue
            row_mm = host.row_in_part("left", height)
            candidates = self.reservations.build(drawer_id, row_mm, runner, host=host)
            try:
                for candidate in candidates:
                    self.compatibility.require_compatible(candidate, blocked)
            except PanelHardwareConflictError:
                continue
            return row_mm
        raise HettichKa5332System32RowError(
            f"no collision-free System 32 row remains for {drawer_id}"
        )

    def resolve_exact(self, cabinet, drawer_id, requested_bottom_height_mm,
                      runner, blocked=()) -> float:
        """Preserve the planned bottom; reject conflicts instead of moving a drawer."""
        host = DrawerHost.resolve(cabinet)
        world_height = (host.spec.bottom_mm + requested_bottom_height_mm
                        + runner.runner_center_from_drawer_bottom_mm)
        row = host.row_in_part("left", world_height)
        for reservation in self.reservations.build(drawer_id, row, runner, host=host):
            self.compatibility.require_compatible(reservation, blocked)
        return row


__all__ = [
    "HettichKa5332System32RowError",
    "HettichKa5332System32RowResolver",
]
