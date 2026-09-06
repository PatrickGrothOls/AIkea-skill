"""Scope: Map assembly-local review parts into one project coordinate frame."""

from __future__ import annotations

import cadquery as cq

from unit_mockup import MockupPart


class ProjectPartPlacer:
    """Position and uniquely name one assembly's parts in the full project."""

    def place(
        self,
        assembly_id: str,
        assembly_global_left_mm: float,
        project_global_left_mm: float,
        parts: tuple[MockupPart, ...],
    ) -> tuple[MockupPart, ...]:
        project_offset = cq.Location(
            cq.Vector(assembly_global_left_mm - project_global_left_mm, 0.0, 0.0)
        )
        return tuple(
            MockupPart(
                f"{assembly_id}__{part.name}",
                part.solid,
                project_offset * part.location,
                part.color,
            )
            for part in parts
        )


__all__ = ["ProjectPartPlacer"]
