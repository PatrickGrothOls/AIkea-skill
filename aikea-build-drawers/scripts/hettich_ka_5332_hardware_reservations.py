"""Scope: Map one KA 5332 runner pair onto shared cabinet hardware space."""

from __future__ import annotations

from panel_hardware_reservation import PanelHardwareReservation
from hettich_ka_5332_runner_profile import HettichKa5332RunnerProfile


class HettichKa5332HardwareReservations:
    """Reserve one front System 32 node and the full rail envelope per side."""

    def build(
        self,
        drawer_id: str,
        row_height_mm: float,
        runner: HettichKa5332RunnerProfile,
    ) -> tuple[PanelHardwareReservation, ...]:
        half_height_mm = runner.installation_envelope_height_mm / 2.0
        depth_interval_mm = (
            runner.runner_front_from_drawer_front_mm,
            runner.runner_front_from_drawer_front_mm + runner.nominal_length_mm,
        )
        return tuple(
            PanelHardwareReservation(
                owner_id=f"{drawer_id}_{side}_runner",
                hardware_kind="drawer_runner",
                side_part_id=f"{side}_side",
                system_32_node_rows_mm=(row_height_mm,),
                depth_interval_mm=depth_interval_mm,
                height_interval_mm=(
                    row_height_mm - half_height_mm,
                    row_height_mm + half_height_mm,
                ),
            )
            for side in ("left", "right")
        )


__all__ = ["HettichKa5332HardwareReservations"]
