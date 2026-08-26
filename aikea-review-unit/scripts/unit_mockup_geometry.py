"""Scope: Turn one flat tall-storage specification into visible panel boxes."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from unit_mockup import MockupPart, UnitMockupInputError


class UnitMockupGeometry:
    """Lay out the visible cabinet envelope without manufacturing features."""

    _CARCASS = (0.78, 0.69, 0.55, 1.0)
    _BACK = (0.67, 0.58, 0.46, 1.0)
    _DOOR = (0.91, 0.86, 0.77, 1.0)

    def build(self, spec: Any) -> tuple[MockupPart, ...]:
        parts = {part.part_id: part for part in spec.parts}
        required = {"left_side", "right_side", "back_panel", "door_panel", "top_panel_01"}
        missing = sorted(required - parts.keys())
        if missing:
            raise UnitMockupInputError(["missing visual parts: " + ", ".join(missing)])
        left = self._dimensions(parts["left_side"])
        right = self._dimensions(parts["right_side"])
        back = self._dimensions(parts["back_panel"])
        door = self._dimensions(parts["door_panel"])
        top = self._dimensions(parts["top_panel_01"])
        if left["height"] != right["height"]:
            raise UnitMockupInputError(["the first mock-up slice requires a level cabinet top"])
        if door["left_height"] != door["right_height"]:
            raise UnitMockupInputError(["the first mock-up slice requires a level door top"])
        base_height = door["left_height"] - left["height"]
        width = float(spec.width_mm)
        depth = float(spec.depth_mm)
        door_x = (width - float(spec.door_width_mm)) / 2.0
        carcass_top = base_height + left["height"]
        return (
            self._box("left_side", 0, 0, base_height, left["thickness"], depth, carcass_top, self._CARCASS),
            self._box("right_side", width - right["thickness"], 0, base_height, width, depth, carcass_top, self._CARCASS),
            self._box("back_panel", 0, depth - back["thickness"], base_height, width, depth, carcass_top, self._BACK),
            self._box("door_panel", door_x, -door["thickness"], 0, door_x + spec.door_width_mm, 0, door["left_height"], self._DOOR),
            self._box("top_panel_01", 0, 0, carcass_top - top["thickness"], width, depth, carcass_top, self._CARCASS),
        )

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}

    def _box(
        self,
        name: str,
        x0: float,
        y0: float,
        z0: float,
        x1: float,
        y1: float,
        z1: float,
        color: tuple[float, float, float, float],
    ) -> MockupPart:
        solid = (
            cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=(False, False, False))
            .translate((x0, y0, z0))
        )
        return MockupPart(name, solid, color)
