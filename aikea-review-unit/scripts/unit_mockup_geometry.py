"""Scope: Assemble every first-unit panel blank for visual review."""

from __future__ import annotations

from typing import Any

from assembly_part_locator import AssemblyPartLocator
from unit_mockup import MockupPart, UnitMockupInputError
from unit_part_blank_builder import UnitPartBlankBuilder


class UnitMockupGeometry:
    """Build and place all generated panel blanks without machining them."""

    _CARCASS = (0.78, 0.69, 0.55, 1.0)
    _BACK = (0.67, 0.58, 0.46, 1.0)
    _DOOR = (0.91, 0.86, 0.77, 1.0)

    def __init__(self) -> None:
        self.blank_builder = UnitPartBlankBuilder()
        self.locator = AssemblyPartLocator()

    def build(self, spec: Any) -> tuple[MockupPart, ...]:
        parts = {part.part_id: part for part in spec.parts}
        required = {"left_side", "right_side", "back_panel", "door_panel", "top_panel_01"}
        missing = sorted(required - parts.keys())
        if missing:
            raise UnitMockupInputError(["missing visual parts: " + ", ".join(missing)])
        base_height_mm = self._base_height(spec, parts)
        return tuple(
            MockupPart(
                part.part_id,
                self.blank_builder.build(part),
                self.locator.locate(part, spec, base_height_mm),
                self._color(part.role),
            )
            for part in spec.parts
        )

    def _base_height(self, spec: Any, parts: dict[str, Any]) -> float:
        if hasattr(spec, "base_height_mm"):
            return float(spec.base_height_mm)
        left = self._dimensions(parts["left_side"])
        door = self._dimensions(parts["door_panel"])
        return door["left_height"] - left["height"]

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}

    def _color(self, role: str) -> tuple[float, float, float, float]:
        return {
            "back_panel": self._BACK,
            "door_panel": self._DOOR,
        }.get(role, self._CARCASS)
