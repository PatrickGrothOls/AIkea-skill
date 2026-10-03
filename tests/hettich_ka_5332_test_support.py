"""Scope: Supply exact-shape bounds without importing vendor CAD in unit tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

from hettich_ka_5332_step_assembly import (
    HettichKa5332SideStepParts,
    HettichKa5332StepAssembly,
)


@dataclass(frozen=True, slots=True)
class HardwareBoundingBoxStub:
    """Expose the X bounds consumed by the mounting planner."""

    xmin: float
    xmax: float


class HardwareShapeStub:
    """Stand in for one imported solid while preserving native X bounds."""

    def __init__(self, xmin: float, xmax: float) -> None:
        self.bounds = HardwareBoundingBoxStub(xmin, xmax)

    def BoundingBox(self) -> HardwareBoundingBoxStub:
        return self.bounds


class HettichKa5332StepAssemblyLoaderTestDouble:
    """Return the recorded six-member source structure for generator tests."""

    sha256 = "a" * 64

    def load(self, hardware_directory: Path) -> HettichKa5332StepAssembly:
        source = SimpleNamespace(
            asset=SimpleNamespace(
                path=hardware_directory / "9057405.stp",
                sha256=self.sha256,
            ),
            solid_count=6,
        )
        left = HettichKa5332SideStepParts(
            cabinet_member=HardwareShapeStub(-7.95, -1.0),
            middle_member=HardwareShapeStub(-7.0, -2.0),
            drawer_member=HardwareShapeStub(-6.0, -3.0),
        )
        right = HettichKa5332SideStepParts(
            cabinet_member=HardwareShapeStub(187.0, 193.05),
            middle_member=HardwareShapeStub(188.0, 192.0),
            drawer_member=HardwareShapeStub(189.0, 191.0),
        )
        return HettichKa5332StepAssembly(source, left, right)


TEST_HETTICH_HARDWARE_DIRECTORY = Path("test-hettich-hardware")


__all__ = [
    "HettichKa5332StepAssemblyLoaderTestDouble",
    "TEST_HETTICH_HARDWARE_DIRECTORY",
]
