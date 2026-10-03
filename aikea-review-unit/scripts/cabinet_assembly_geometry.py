"""Scope: Place every already-built cabinet part with one assembly locator."""

from __future__ import annotations

from typing import Any

from unit_mockup import MockupPart


class CabinetAssemblyGeometry:
    """Place and color generated cabinet parts without choosing their pose."""

    _CARCASS = (0.78, 0.69, 0.55, 1.0)
    _BACK = (0.67, 0.58, 0.46, 1.0)
    _DOOR = (0.91, 0.86, 0.77, 1.0)

    def __init__(self, locator: Any) -> None:
        self.locator = locator

    def build(self, built_assembly: Any) -> tuple[MockupPart, ...]:
        spec = built_assembly.spec
        base_height_mm = float(getattr(spec, "base_height_mm", 0.0))
        return tuple(
            MockupPart(
                built_part.spec.part_id,
                built_part.solid,
                self.locator.locate(built_part.spec, spec, base_height_mm),
                self._color(built_part.spec.role),
            )
            for built_part in built_assembly.parts
        )

    def _color(self, role: str) -> tuple[float, float, float, float]:
        return {
            "back_panel": self._BACK,
            "door_panel": self._DOOR,
        }.get(role, self._CARCASS)


__all__ = ["CabinetAssemblyGeometry"]
