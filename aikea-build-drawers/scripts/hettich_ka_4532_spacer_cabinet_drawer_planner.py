"""Scope: Resolve one exact KA 4532 and 13952 drawer inside a cabinet."""

from __future__ import annotations

from typing import Any

from cabinet_drawer_fit_checker import CabinetDrawerFitChecker
from cabinet_drawer_plan import DrawerLayout
from drawer_assembly_spec import DrawerAssemblySpec
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening
from hettich_ka_4532_spacer_cabinet_drawer_plan import (
    HettichKa4532SpacerCabinetDrawerPlan,
)
from hettich_ka_4532_spacer_drawer_box_profile import (
    HettichKa4532SpacerDrawerBoxProfileAdapter,
)
from hettich_ka_4532_spacer_hardware_reservations import (
    HettichKa4532SpacerHardwareReservations,
)
from hettich_ka_4532_spacer_fixing_alignment_checker import (
    HettichKa4532SpacerFixingAlignmentChecker,
)
from hettich_ka_4532_spacer_mounting_planner import (
    HettichKa4532SpacerMountingPlanner,
)
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952
from panel_hardware_reservation import (
    PanelHardwareReservation,
    PanelHardwareReservationPlan,
)

MACHINING_AUTHORITY_BLOCKED = "blocked_missing_longer_screw_and_cabinet_pilot"
SOURCE_CAD_PLACED = "exact_source_cad_placed"


class HettichKa4532SpacerCabinetDrawerPlanner:
    """Compose sourced product rules without inferring spacer machining."""

    def __init__(self) -> None:
        self.box_profile = HettichKa4532SpacerDrawerBoxProfileAdapter()
        self.box_planner = DrawerBoxPlanner()
        self.mounting = HettichKa4532SpacerMountingPlanner()
        self.fixing_alignment = HettichKa4532SpacerFixingAlignmentChecker()
        self.reservations = HettichKa4532SpacerHardwareReservations()
        self.compatibility = PanelHardwareReservationPlan()
        self.fit = CabinetDrawerFitChecker()

    def plan(
        self,
        cabinet: Any,
        layout: DrawerLayout,
        hardware_step: Any,
        existing_reservations: tuple[PanelHardwareReservation, ...] = (),
        *,
        cabinet_front_mm: float,
        drawer_front_mm: float,
    ) -> HettichKa4532SpacerCabinetDrawerPlan:
        profile = HETTICH_KA_4532_500_WITH_13952
        self._require_product_fit(cabinet, layout, profile)
        drawer_bottom_mm = float(cabinet.base_height_mm) + layout.bottom_height_mm
        mounting = self.mounting.plan(
            cabinet,
            hardware_step,
            cabinet_front_mm=cabinet_front_mm,
            drawer_front_mm=drawer_front_mm,
            drawer_bottom_mm=drawer_bottom_mm,
            hardware=profile,
        )
        fixing_alignment = self.fixing_alignment.verify(hardware_step, mounting)
        opening = CabinetDrawerOpening(
            clear_width_mm=(
                mounting.drawer_outside_width_mm
                + 2.0 * profile.hardware_width_per_side_mm
            ),
            inside_depth_mm=float(cabinet.inside_depth_mm),
        )
        sizing = self.box_profile.build(
            profile,
            side_thickness_mm=layout.side_thickness_mm,
            front_back_thickness_mm=layout.front_back_thickness_mm,
            bottom_thickness_mm=layout.bottom_thickness_mm,
            bottom_underside_recess_mm=layout.bottom_underside_recess_mm,
            box_height_mm=layout.box_height_mm,
        )
        box = self.box_planner.plan(opening, sizing)
        if abs(box.outside_width_mm - mounting.drawer_outside_width_mm) > 1e-6:
            raise ValueError("drawer box and exact hardware resolve different widths")
        self.fit.require_fit(
            cabinet,
            box,
            profile.minimum_cabinet_depth_mm,
            mounting.drawer_origin_mm,
        )
        reservations = self._reservations(
            existing_reservations,
            layout.drawer_id,
            mounting,
            hardware_step,
        )
        drawer = DrawerAssemblySpec(
            assembly_id=layout.drawer_id,
            purpose="drawer",
            runner_product_code=profile.runner_product_code,
            runner_item_number=profile.runner_item_number,
            hardware_geometry_state=SOURCE_CAD_PLACED,
            box=box,
        )
        return HettichKa4532SpacerCabinetDrawerPlan(
            cabinet.assembly_id,
            profile,
            drawer,
            mounting.drawer_origin_mm,
            mounting,
            fixing_alignment,
            hardware_step,
            reservations,
            MACHINING_AUTHORITY_BLOCKED,
        )

    def _require_product_fit(self, cabinet, layout, profile) -> None:
        requested = layout.box_depth_mm or profile.nominal_runner_length_mm
        if abs(requested - profile.nominal_runner_length_mm) > 1e-6:
            raise ValueError("KA 4532 article 9114276 requires the exact 500 mm depth")
        if float(cabinet.inside_depth_mm) < profile.minimum_cabinet_depth_mm:
            raise ValueError("KA 4532 article 9114276 requires 504 mm cabinet depth")

    def _reservations(self, existing, drawer_id, mounting, hardware_step):
        owner_ids = {
            self.reservations.owner_id(drawer_id, side)
            for side in ("left", "right")
        }
        retained = tuple(item for item in existing if item.owner_id not in owner_ids)
        if any(
            item.hardware_kind == self.reservations.HARDWARE_KIND
            for item in retained
        ):
            raise ValueError("KA 4532 spacer repetition remains disabled before first proof")
        candidates = self.reservations.build(drawer_id, mounting, hardware_step)
        accepted = list(retained)
        for candidate in candidates:
            self.compatibility.require_compatible(candidate, tuple(accepted))
            accepted.append(candidate)
        return tuple(accepted)


__all__ = [
    "HettichKa4532SpacerCabinetDrawerPlanner",
    "MACHINING_AUTHORITY_BLOCKED",
    "SOURCE_CAD_PLACED",
]
