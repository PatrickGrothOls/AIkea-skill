"""Scope: Expose fixed cabinet parts as side-panel hardware obstacles."""

from __future__ import annotations

from typing import Any

from panel_hardware_reservation import PanelHardwareReservation


class CabinetFeatureReservations:
    """Map shelf contacts into the same physical contract as purchased hardware."""

    def for_side(
        self,
        assembly: Any,
        side_part_id: str,
    ) -> tuple[PanelHardwareReservation, ...]:
        return tuple(
            self._shelf(part, side_part_id)
            for part in assembly.parts
            if part.role == "shelf_panel"
        )

    def _shelf(
        self,
        part: Any,
        side_part_id: str,
    ) -> PanelHardwareReservation:
        dimensions = {
            name: float(value) for name, value in part.dimensions_mm
        }
        bottom_mm = dimensions["bottom_height"]
        return PanelHardwareReservation(
            owner_id=part.part_id,
            hardware_kind="cabinet_shelf",
            side_part_id=side_part_id,
            system_32_node_rows_mm=(),
            depth_interval_mm=(
                dimensions["assembly_y"],
                dimensions["assembly_y"] + dimensions["depth"],
            ),
            height_interval_mm=(
                bottom_mm,
                bottom_mm + dimensions["thickness"],
            ),
        )


__all__ = ["CabinetFeatureReservations"]
