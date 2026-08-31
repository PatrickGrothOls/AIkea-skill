"""Scope: Preserve legacy posed additions while wardrobe review becomes tree-based."""

from __future__ import annotations

from typing import Any

from base_mockup_geometry import BaseMockupGeometry
from cabinet_review_geometry import CabinetReviewGeometry
from project_part_placer import ProjectPartPlacer


class WardrobeAdditionReviewGeometry:
    """Place explicitly posed additions through their owning cabinet frame."""

    def __init__(self) -> None:
        self.base = BaseMockupGeometry()
        self.cabinets = CabinetReviewGeometry()
        self.placer = ProjectPartPlacer()

    def build(
        self,
        built_base: Any,
        built_cabinets: tuple[Any, ...],
        door_states: dict[str, Any],
        additions: dict[str, Any],
    ) -> tuple[Any, ...]:
        project_left_mm = float(built_base.spec.global_left_mm)
        parts = self.placer.place(
            built_base.spec.assembly_id,
            project_left_mm,
            project_left_mm,
            self.base.build(built_base),
        )
        for cabinet in built_cabinets:
            addition = additions.get(cabinet.spec.assembly_id)
            local_parts = self.cabinets.build(
                cabinet,
                door_states[cabinet.spec.assembly_id],
            ) + (addition.review_parts if addition else ())
            parts += self.placer.place(
                cabinet.spec.assembly_id,
                float(cabinet.spec.global_left_mm),
                project_left_mm,
                local_parts,
            )
        return parts


__all__ = ["WardrobeAdditionReviewGeometry"]
