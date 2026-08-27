"""Scope: Locate one structural-base part inside its owning base assembly."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from part_construction_error import PartConstructionError


class BasePartLocator:
    """Place decks, front and back rails, and braces from their local specs."""

    ROLES = frozenset({"base_deck", "base_rail", "base_brace"})

    def locate(self, part: Any, base: Any) -> cq.Location:
        module = self._module(part, base)
        dimensions = self._dimensions(part)
        locations = {
            "base_deck": self._deck_location,
            "base_rail": self._rail_location,
            "base_brace": self._brace_location,
        }
        locator = locations.get(part.role)
        if locator is None:
            raise PartConstructionError(f"unsupported base part role: {part.role}")
        return locator(part, base, module, dimensions)

    def _deck_location(self, _part, base, module, dimensions) -> cq.Location:
        return cq.Location(
            cq.Vector(
                module.start_x_mm,
                0.0,
                base.height_mm - dimensions["thickness"],
            )
        )

    def _rail_location(self, part, base, module, dimensions) -> cq.Location:
        origin_y_mm = float(base.plinth_recess_mm) + dimensions["thickness"]
        if part.part_id.startswith("back_rail_"):
            origin_y_mm = base.depth_mm
        return cq.Location(
            cq.Plane(
                origin=(module.start_x_mm, origin_y_mm, 0.0),
                xDir=(1.0, 0.0, 0.0),
                normal=(0.0, -1.0, 0.0),
            )
        )

    def _brace_location(self, part, base, module, dimensions) -> cq.Location:
        front_rail = base.part(f"front_rail_{self._module_suffix(part)}")
        front_thickness_mm = self._dimensions(front_rail)["thickness"]
        front_inside_y_mm = float(base.plinth_recess_mm) + front_thickness_mm
        start_x_mm = (
            module.start_x_mm
            + dimensions["center_x"]
            - (dimensions["thickness"] / 2.0)
        )
        return cq.Location(
            cq.Plane(
                origin=(start_x_mm, front_inside_y_mm, 0.0),
                xDir=(0.0, 1.0, 0.0),
                normal=(1.0, 0.0, 0.0),
            )
        )

    def _module(self, part: Any, base: Any) -> Any:
        module_id = f"base_module_{self._module_suffix(part)}"
        return next(module for module in base.modules if module.module_id == module_id)

    def _module_suffix(self, part: Any) -> str:
        fields = part.part_id.split("_")
        return fields[-2] if part.role == "base_brace" else fields[-1]

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["BasePartLocator"]
