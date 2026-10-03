"""Scope: Place every already-built first-unit part for visual review."""

from __future__ import annotations

from cabinet_assembly_geometry import CabinetAssemblyGeometry
from review_part_locator import ReviewPartLocator


class UnitMockupGeometry(CabinetAssemblyGeometry):
    """Choose the open-door pose used for one-cabinet visual review."""

    def __init__(self) -> None:
        super().__init__(ReviewPartLocator())
