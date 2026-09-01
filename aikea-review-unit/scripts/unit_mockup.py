"""Scope: Define the immutable values used by one visual cabinet mock-up."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


class UnitMockupInputError(ValueError):
    """Report a local specification that cannot produce this review slice."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = tuple(problems)
        super().__init__("; ".join(problems))


@dataclass(frozen=True)
class MockupPart:
    name: str
    solid: Any
    location: Any
    color: tuple[float, float, float, float]
    source_hardware_asset_id: str | None = None
    source_geometry_selector: str | None = None

    def placed_shape(self) -> Any:
        """Return this local part transformed into assembly coordinates."""
        return self.solid.val().located(self.location)


@dataclass(frozen=True)
class UnitMockupResult:
    assembly_id: str
    glb_path: Path
