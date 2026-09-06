"""Scope: Place every built base part for visual inspection."""

from __future__ import annotations

from typing import Any

from base_part_locator import BasePartLocator
from unit_mockup import MockupPart, UnitMockupInputError


class BaseMockupGeometry:
    """Turn generated local base parts into one reviewable physical arrangement."""

    _DECK = (0.82, 0.74, 0.61, 1.0)
    _FRAME = (0.67, 0.58, 0.46, 1.0)
    _REQUIRED_ROLES = {"base_deck", "base_rail", "base_brace"}

    def __init__(self) -> None:
        self.locator = BasePartLocator()

    def build(self, built_base: Any) -> tuple[MockupPart, ...]:
        roles = {part.spec.role for part in built_base.parts}
        missing = sorted(self._REQUIRED_ROLES - roles)
        if missing:
            raise UnitMockupInputError(["missing base roles: " + ", ".join(missing)])
        return tuple(
            MockupPart(
                part.spec.part_id,
                part.solid,
                self.locator.locate(part.spec, built_base.spec),
                self._color(part.spec.role),
            )
            for part in built_base.parts
        )

    def _color(self, role: str) -> tuple[float, float, float, float]:
        return self._DECK if role == "base_deck" else self._FRAME


__all__ = ["BaseMockupGeometry"]
