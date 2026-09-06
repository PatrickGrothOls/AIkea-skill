"""Scope: Cut door-side hinge preparation while preserving the cabinet-owned grid."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cadquery as cq

from door_hinge_plan import DoorHingePlan
from door_hinge_side import DoorHingeSide
from riex_nc70_hinge_profile import RiexNc70HingeProfile


@dataclass(frozen=True, slots=True)
class HingedPanelSet:
    """Carry the two machined panel solids that participate in the joint."""

    door: cq.Workplane
    cabinet_side: cq.Workplane


class ConcealedHingeMachining:
    """Machine the door and leave grid-mounted cabinet preparation unchanged."""

    _PILOT_DIAMETER_MM = 2.5
    _PILOT_DEPTH_MM = 10.0

    def apply(
        self,
        built_assembly: Any,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
    ) -> HingedPanelSet:
        parts = {part.spec.part_id: part for part in built_assembly.parts}
        door = parts["door_panel"].solid
        side = parts[plan.hinge_side.side_part_id].solid
        for placement in plan.placements:
            door = door.cut(
                self._door_cutter(
                    placement.door_height_mm,
                    profile,
                    plan.hinge_side,
                    plan.door_width_mm,
                )
            )
        return HingedPanelSet(door=door, cabinet_side=side)

    def _door_cutter(
        self,
        center_height_mm: float,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
        door_width_mm: float = 0.0,
    ) -> cq.Workplane:
        cup_center_mm = self._edge_position(
            profile.cup_center_from_edge_mm,
            hinge_side,
            door_width_mm,
        )
        fixing_line_mm = self._edge_position(
            profile.cup_fixing_line_from_edge_mm,
            hinge_side,
            door_width_mm,
        )
        cup = (
            cq.Workplane("XY", origin=(0.0, 0.0, -0.1))
            .center(cup_center_mm, center_height_mm)
            .circle(profile.cup_diameter_mm / 2.0)
            .extrude(profile.cup_depth_mm + 0.1)
        )
        fixing_centers = (
            center_height_mm - profile.cup_fixing_spacing_mm / 2.0,
            center_height_mm + profile.cup_fixing_spacing_mm / 2.0,
        )
        return cup.union(
            self._pilot_cylinders(
                fixing_line_mm,
                fixing_centers,
                -0.1,
                self._PILOT_DEPTH_MM + 0.1,
            )
        )

    def _edge_position(
        self,
        distance_from_edge_mm: float,
        hinge_side: DoorHingeSide,
        door_width_mm: float,
    ) -> float:
        if hinge_side is DoorHingeSide.LEFT:
            return distance_from_edge_mm
        return door_width_mm - distance_from_edge_mm

    def _pilot_cylinders(
        self,
        x_mm: float,
        y_values_mm: tuple[float, float],
        origin_z_mm: float,
        depth_mm: float,
    ) -> cq.Workplane:
        return (
            cq.Workplane("XY", origin=(0.0, 0.0, origin_z_mm))
            .pushPoints(tuple((x_mm, y_mm) for y_mm in y_values_mm))
            .circle(self._PILOT_DIAMETER_MM / 2.0)
            .extrude(depth_mm)
        )

__all__ = ["ConcealedHingeMachining", "HingedPanelSet"]
