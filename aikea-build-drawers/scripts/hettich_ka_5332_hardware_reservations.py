"""Scope: Map one KA 5332 runner pair onto shared cabinet hardware space."""

from __future__ import annotations

from panel_hardware_reservation import PanelHardwareReservation
from hettich_ka_5332_runner_profile import HettichKa5332RunnerProfile
from system_32_side_panel_grid import System32SidePanelGrid


class HettichKa5332HardwareReservations:
    """Reserve one front System 32 node and the full rail envelope per side."""

    def build(
        self,
        drawer_id: str,
        row_height_mm: float,
        runner: HettichKa5332RunnerProfile,
        *, host=None,
    ) -> tuple[PanelHardwareReservation, ...]:
        half_height_mm = runner.installation_envelope_height_mm / 2.0
        depth_interval_mm = (
            runner.runner_front_from_drawer_front_mm,
            runner.runner_front_from_drawer_front_mm + runner.nominal_length_mm,
        )
        reservations = tuple(
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
        if host is None:
            return reservations
        from dataclasses import replace
        world_height = host.frame("left").origin_mm[2] + row_height_mm
        resolved = []
        for side, reservation in zip(("left", "right"), reservations):
            frame = host.frame(side)
            panel_front = min(frame.origin_mm[1], frame.to_owner((host.part(side).local_size_mm[0], 0, 0))[1])
            front_offset = host.spec.front_mm - panel_front
            row = host.row_in_part(side, world_height)
            front_column = System32SidePanelGrid().column_positions_mm(host.part(side).local_size_mm[0])[0]
            uses_node = any(abs(value+front_offset-front_column) < 1e-6
                            for value in runner.cabinet_fixing_positions_from_front_mm)
            resolved.append(replace(reservation, side_part_id=host.part(side).part_id,
                system_32_node_rows_mm=(row,) if uses_node else (),
                depth_interval_mm=tuple(value+front_offset for value in depth_interval_mm),
                height_interval_mm=(row-half_height_mm, row+half_height_mm)))
        return tuple(resolved)


__all__ = ["HettichKa5332HardwareReservations"]
