"""Scope: Carry one exact KA 4532 and 13952 cabinet drawer proof."""

from __future__ import annotations

from dataclasses import dataclass

from drawer_assembly_spec import DrawerAssemblySpec
from hettich_ka_4532_spacer_mounting_plan import (
    HettichKa4532SpacerMountingPlan,
)
from hettich_ka_4532_spacer_fixing_alignment import (
    HettichKa4532SpacerFixingAlignment,
)
from hettich_ka_4532_spacer_profile import HettichKa4532SpacerProfile
from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSet
from panel_hardware_reservation import PanelHardwareReservation


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerCabinetDrawerPlan:
    """Keep the wooden child, exact hardware, and fabrication boundary together."""

    parent_assembly_id: str
    hardware: HettichKa4532SpacerProfile
    drawer: DrawerAssemblySpec
    origin_in_parent_mm: tuple[float, float, float]
    hardware_mounting: HettichKa4532SpacerMountingPlan
    fixing_alignment: HettichKa4532SpacerFixingAlignment
    hardware_step: HettichKa4532SpacerStepSet
    hardware_reservations: tuple[PanelHardwareReservation, ...]
    machining_authority: str


__all__ = ["HettichKa4532SpacerCabinetDrawerPlan"]
