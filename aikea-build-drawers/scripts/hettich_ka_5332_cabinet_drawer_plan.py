"""Scope: Resolve one KA 5332 drawer child from an existing cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cabinet_drawer_fit_checker import CabinetDrawerFitChecker
from cabinet_drawer_plan import DrawerLayout
from drawer_assembly_spec import DrawerAssemblySpec
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening
from hettich_ka_5332_drawer_box_profile import (
    HettichKa5332DrawerBoxProfileAdapter,
)
from hettich_ka_5332_mounting_plan import (
    HettichKa5332MountingPlan,
    HettichKa5332MountingPlanner,
)
from hettich_ka_5332_runner_catalog import (
    HETTICH_KA_5332_RUNNER_CATALOG,
    HettichKa5332RunnerCatalog,
)
from hettich_ka_5332_runner_profile import (
    HettichKa5332RunnerProfile,
)
from hettich_ka_5332_hardware_reservations import (
    HettichKa5332HardwareReservations,
)
from hettich_ka_5332_system_32_row_resolver import (
    HettichKa5332System32RowResolver,
)
from hettich_ka_5332_step_assembly import HettichKa5332StepAssembly
from panel_hardware_reservation import PanelHardwareReservation

SOURCE_CAD_MOUNTING_PLAN_SAVED = "source_cad_mounting_plan_saved"


@dataclass(frozen=True, slots=True)
class HettichKa5332CabinetDrawerPlan:
    """Keep the wooden child and exact paired-runner placement together."""

    parent_assembly_id: str
    layout: DrawerLayout
    runner: HettichKa5332RunnerProfile
    drawer: DrawerAssemblySpec
    origin_in_parent_mm: tuple[float, float, float]
    hardware_mounting: HettichKa5332MountingPlan
    hardware_step: HettichKa5332StepAssembly
    hardware_reservations: tuple[PanelHardwareReservation, ...]


class HettichKa5332CabinetDrawerPlanner:
    """Promote the approved visual prototype calculations into project data."""

    def __init__(
        self,
        runner_catalog: HettichKa5332RunnerCatalog = (
            HETTICH_KA_5332_RUNNER_CATALOG
        ),
    ) -> None:
        self.runner_catalog = runner_catalog
        self.box_profile = HettichKa5332DrawerBoxProfileAdapter()
        self.box_planner = DrawerBoxPlanner()
        self.mounting_planner = HettichKa5332MountingPlanner()
        self.row_resolver = HettichKa5332System32RowResolver()
        self.hardware_reservations = HettichKa5332HardwareReservations()
        self.fit_checker = CabinetDrawerFitChecker()

    def plan(
        self,
        cabinet: Any,
        layout: DrawerLayout,
        hardware_step: HettichKa5332StepAssembly,
        blocked_reservations: tuple[PanelHardwareReservation, ...] = (),
    ) -> HettichKa5332CabinetDrawerPlan:
        opening = CabinetDrawerOpening.from_assembly_spec(cabinet)
        runner = self.runner_catalog.select(
            layout.box_depth_mm,
            opening.inside_depth_mm,
        )
        sizing = self.box_profile.build(
            runner,
            side_thickness_mm=layout.side_thickness_mm,
            front_back_thickness_mm=layout.front_back_thickness_mm,
            bottom_thickness_mm=layout.bottom_thickness_mm,
            bottom_underside_recess_mm=layout.bottom_underside_recess_mm,
            box_height_mm=layout.box_height_mm,
        )
        box = self.box_planner.plan(opening, sizing)
        system_32_row_mm = self.row_resolver.resolve(
            cabinet,
            layout.drawer_id,
            layout.bottom_height_mm,
            runner,
            blocked_reservations,
        )
        cabinet_opening_front_mm = 0.0
        drawer_bottom_mm = float(cabinet.base_height_mm) + (
            system_32_row_mm - runner.runner_center_from_drawer_bottom_mm
        )
        mounting = self.mounting_planner.plan(
            cabinet,
            hardware_step,
            runner,
            drawer_front_mm=cabinet_opening_front_mm,
            drawer_bottom_mm=drawer_bottom_mm,
            system_32_row_height_mm=system_32_row_mm,
        )
        if abs(box.outside_width_mm - mounting.drawer_outside_width_mm) > 1e-6:
            raise ValueError("drawer box and runner placement resolve different widths")
        self.fit_checker.require_fit(
            cabinet,
            box,
            runner.minimum_cabinet_depth_mm,
            mounting.drawer_origin_mm,
        )
        drawer = DrawerAssemblySpec(
            assembly_id=layout.drawer_id,
            purpose="drawer",
            runner_product_code=runner.product_code,
            runner_item_number=runner.item_number,
            hardware_geometry_state=SOURCE_CAD_MOUNTING_PLAN_SAVED,
            box=box,
        )
        reservations = self.hardware_reservations.build(
            layout.drawer_id,
            system_32_row_mm,
            runner,
        )
        return HettichKa5332CabinetDrawerPlan(
            parent_assembly_id=cabinet.assembly_id,
            layout=layout,
            runner=runner,
            drawer=drawer,
            origin_in_parent_mm=mounting.drawer_origin_mm,
            hardware_mounting=mounting,
            hardware_step=hardware_step,
            hardware_reservations=reservations,
        )


__all__ = [
    "HettichKa5332CabinetDrawerPlan",
    "HettichKa5332CabinetDrawerPlanner",
    "SOURCE_CAD_MOUNTING_PLAN_SAVED",
]
