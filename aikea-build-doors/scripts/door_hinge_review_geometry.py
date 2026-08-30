"""Scope: Present one machined cabinet door with exact closed or open hinge CAD."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from assembly_part_locator import AssemblyPartLocator
from cabinet_assembly_geometry import CabinetAssemblyGeometry
from concealed_hinge_machining import HingedPanelSet
from door_hinge_plan import DoorHingePlan
from riex_nc70_hardware_loader import RiexNc70HardwareSet
from riex_nc70_hardware_placement import RiexNc70HardwarePlacement
from riex_nc70_hinge_profile import RiexNc70HingeProfile
from unit_mockup import MockupPart


class DoorHingeReviewGeometry:
    """Keep manufactured panel frames and purchased-hardware frames explicit."""

    def __init__(self) -> None:
        self.closed_cabinet = CabinetAssemblyGeometry(AssemblyPartLocator())
        self.hardware_placement = RiexNc70HardwarePlacement()

    def build(
        self,
        built_assembly: Any,
        machined: HingedPanelSet,
        hardware: RiexNc70HardwareSet,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
        opened: bool,
    ) -> tuple[MockupPart, ...]:
        cabinet_parts = self._machined_cabinet_parts(
            built_assembly,
            machined,
            plan,
            profile,
            opened,
        )
        return cabinet_parts + self.hardware_placement.parts(
            built_assembly.spec,
            hardware,
            plan,
            profile,
            opened,
        )

    def _machined_cabinet_parts(
        self,
        built_assembly: Any,
        machined: HingedPanelSet,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
        opened: bool,
    ) -> tuple[MockupPart, ...]:
        replacements = {
            plan.hinge_side.side_part_id: machined.cabinet_side,
            "door_panel": machined.door,
        }
        parts = tuple(
            MockupPart(
                part.name,
                replacements.get(part.name, part.solid),
                part.location,
                part.color,
            )
            for part in self.closed_cabinet.build(built_assembly)
        )
        if not opened:
            return parts
        pivot_x_mm, pivot_y_mm = self.hardware_placement.pivot(
            built_assembly.spec,
            profile,
            plan.hinge_side,
        )
        angle_degrees = plan.hinge_side.opening_angle_degrees(
            profile.open_angle_degrees
        )
        return tuple(
            self._open_door(part, pivot_x_mm, pivot_y_mm, angle_degrees)
            if part.name == "door_panel"
            else part
            for part in parts
        )

    def _open_door(
        self,
        part: MockupPart,
        pivot_x_mm: float,
        pivot_y_mm: float,
        angle_degrees: float,
    ) -> MockupPart:
        placed = part.solid.val().located(part.location)
        opened = placed.rotate(
            cq.Vector(pivot_x_mm, pivot_y_mm, 0.0),
            cq.Vector(pivot_x_mm, pivot_y_mm, 1.0),
            angle_degrees,
        )
        return MockupPart(
            part.name,
            cq.Workplane(obj=opened),
            cq.Location(cq.Vector(0.0, 0.0, 0.0)),
            part.color,
        )

__all__ = ["DoorHingeReviewGeometry"]
