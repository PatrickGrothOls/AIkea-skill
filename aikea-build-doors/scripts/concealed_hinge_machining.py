"""Scope: Adapt the existing slab-door plan to surface-based hinge drilling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cadquery as cq

from door_hinge_plan import DoorHingePlan
from door_hinge_side import DoorHingeSide
from riex_nc70_hinge_profile import RiexNc70HingeProfile
from riex_nc70_cup_pattern import RiexNc70CupPattern
from panel_machining_feature import PanelMachiningFeature
from riex_nc70_machining_recipe import RiexNc70MachiningRecipe


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
        requests = RiexNc70MachiningRecipe().build(built_assembly.spec, plan, profile)
        machined = PanelMachiningFeature().apply(built_assembly, requests)
        parts = {part.spec.part_id: part for part in machined.parts}
        return HingedPanelSet(door=parts[plan.door_part_id].solid,
                              cabinet_side=parts[plan.support_part_id].solid)

    def _door_cutter(
        self,
        center_height_mm: float,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
        door_width_mm: float = 0.0,
    ) -> cq.Workplane:
        left = hinge_side is DoorHingeSide.LEFT
        cup_x = (profile.cup_center_from_edge_mm if left else
                 door_width_mm-profile.cup_center_from_edge_mm)
        surface = cq.Plane(origin=(cup_x, center_height_mm, 0),
                           xDir=(1 if left else -1, 0, 0), normal=(0, 0, 1))
        pattern = RiexNc70CupPattern(profile, self._PILOT_DIAMETER_MM,
                                     self._PILOT_DEPTH_MM).build()
        holes = pattern.place(surface)
        return cq.Workplane(obj=cq.Compound.makeCompound([hole.cutter for hole in holes]))

__all__ = ["ConcealedHingeMachining", "HingedPanelSet"]
