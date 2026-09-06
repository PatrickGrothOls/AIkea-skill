"""Scope: Resolve one local drawer child from its cabinet and layout choices."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from drawer_assembly_spec import DrawerAssemblySpec
from cabinet_drawer_fit_checker import CabinetDrawerFitChecker
from drawer_hardware_mounting_plan import DrawerHardwareMountingPlan
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening
from movento_drawer_box_profile import MoventoDrawerBoxProfileAdapter
from movento_hardware_mounting_planner import MoventoHardwareMountingPlanner
from movento_runner_catalog import MOVENTO_RUNNER_CATALOG
from movento_runner_profile import MoventoRunnerProfile

Vector3D = tuple[float, float, float]


class DrawerLayoutError(ValueError):
    """Report a drawer layout that cannot own a stable generated child."""


@dataclass(frozen=True, slots=True)
class DrawerLayout:
    """Record the local choices for one drawer inside one cabinet."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    drawer_id: str
    bottom_height_mm: float
    side_thickness_mm: float = 15.0
    front_back_thickness_mm: float = 15.0
    bottom_thickness_mm: float = 9.0
    bottom_underside_recess_mm: float = 13.0
    box_height_mm: float = 160.0
    box_depth_mm: float | None = None

    def __post_init__(self) -> None:
        if not self._ID_PATTERN.fullmatch(self.drawer_id):
            raise DrawerLayoutError(
                "drawer_id must be a stable lowercase Python identifier "
                "with a two-digit suffix"
            )
        if self.bottom_height_mm < 0.0:
            raise DrawerLayoutError("drawer bottom height cannot be negative")
        if self.box_height_mm <= 0.0:
            raise DrawerLayoutError("drawer box height must be positive")
        if self.box_depth_mm is not None and self.box_depth_mm <= 0.0:
            raise DrawerLayoutError("drawer box depth must be positive")


@dataclass(frozen=True, slots=True)
class CabinetDrawerPlan:
    """Keep the resolved child and its explicit cabinet-local zero together."""

    parent_assembly_id: str
    layout: DrawerLayout
    runner: MoventoRunnerProfile
    drawer: DrawerAssemblySpec
    origin_in_parent_mm: Vector3D
    hardware_mounting: DrawerHardwareMountingPlan


class CabinetDrawerPlanner:
    """Calculate one drawer child without changing the overall project spec."""

    def __init__(self) -> None:
        self.profile_adapter = MoventoDrawerBoxProfileAdapter()
        self.box_planner = DrawerBoxPlanner()
        self.fit_checker = CabinetDrawerFitChecker()
        self.hardware_mounting_planner = MoventoHardwareMountingPlanner()

    def plan(self, cabinet: Any, layout: DrawerLayout) -> CabinetDrawerPlan:
        opening = CabinetDrawerOpening.from_assembly_spec(cabinet)
        runner = MOVENTO_RUNNER_CATALOG.select_for_depth(
            opening.inside_depth_mm,
            layout.front_back_thickness_mm,
        )
        sizing = self.profile_adapter.build(
            runner,
            side_thickness_mm=layout.side_thickness_mm,
            front_back_thickness_mm=layout.front_back_thickness_mm,
            bottom_thickness_mm=layout.bottom_thickness_mm,
            bottom_underside_recess_mm=layout.bottom_underside_recess_mm,
            box_height_mm=layout.box_height_mm,
        )
        box = self.box_planner.plan(opening, sizing)
        left_thickness_mm = float(cabinet.part("left_side").local_size_mm[2])
        side_clearance_mm = (opening.clear_width_mm - box.outside_width_mm) / 2.0
        origin = (
            left_thickness_mm + side_clearance_mm,
            layout.front_back_thickness_mm + runner.cabinet_depth_clearance_mm,
            float(cabinet.base_height_mm) + layout.bottom_height_mm,
        )
        self.fit_checker.require_fit(
            cabinet,
            box,
            runner.required_inside_depth_mm(layout.front_back_thickness_mm),
            origin,
        )
        drawer = DrawerAssemblySpec(
            assembly_id=layout.drawer_id,
            purpose="drawer",
            runner_product_code=runner.product_code,
            runner_item_number=runner.item_number,
            hardware_geometry_state="source_cad_verification_required",
            box=box,
        )
        hardware_mounting = self.hardware_mounting_planner.plan(
            cabinet,
            box,
            origin,
            runner.require_mounting_profile(),
        )
        return CabinetDrawerPlan(
            parent_assembly_id=cabinet.assembly_id,
            layout=layout,
            runner=runner,
            drawer=drawer,
            origin_in_parent_mm=origin,
            hardware_mounting=hardware_mounting,
        )

__all__ = [
    "CabinetDrawerPlan",
    "CabinetDrawerPlanner",
    "DrawerLayout",
    "DrawerLayoutError",
    "Vector3D",
]
