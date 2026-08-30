"""Scope: Supply reusable measured-room fixtures for door-opening tests."""

from __future__ import annotations

from dataclasses import dataclass

from height_measurements import HeightMeasurement
from installation_boundaries import InstallationBoundaries
from top_boundary import TopBoundary, TopBoundaryKind


@dataclass(frozen=True, slots=True)
class DoorOutlinePoint:
    x_mm: float
    height_mm: float


@dataclass(frozen=True, slots=True)
class DoorPart:
    part_id: str
    dimensions_mm: tuple[tuple[str, float], ...]
    outline_mm: tuple[DoorOutlinePoint, ...] = ()


class DoorOpeningAssembly:
    """Represent one fitted door in global wardrobe coordinates."""

    assembly_id = "tall_storage_01"
    width_mm = 600.0
    door_width_mm = 598.0
    global_left_mm = 200.0
    global_right_mm = 800.0
    door_bottom_mm = 100.0

    def __init__(self, left_height_mm: float, right_height_mm: float) -> None:
        self.door = DoorPart(
            "door_panel",
            (
                ("width", self.door_width_mm),
                ("left_height", left_height_mm),
                ("right_height", right_height_mm),
                ("thickness", 18.0),
            ),
            (
                DoorOutlinePoint(0.0, 0.0),
                DoorOutlinePoint(self.door_width_mm, 0.0),
                DoorOutlinePoint(self.door_width_mm, right_height_mm),
                DoorOutlinePoint(0.0, left_height_mm),
            ),
        )

    def part(self, part_id: str) -> DoorPart:
        if part_id != "door_panel":
            raise KeyError(part_id)
        return self.door


@dataclass(frozen=True, slots=True)
class MeasuredSpace:
    minimum_width_mm: float
    top_boundary: TopBoundary


@dataclass(frozen=True, slots=True)
class DesignSettings:
    installation_boundaries: InstallationBoundaries


@dataclass(frozen=True, slots=True)
class DoorOpeningInputs:
    space: MeasuredSpace
    settings: DesignSettings


class DoorOpeningFixture:
    """Build flat or sloped room inputs from explicit measurements."""

    def flat_inputs(self, height_mm: float) -> DoorOpeningInputs:
        return self._inputs(
            (
                HeightMeasurement(0.0, height_mm),
                HeightMeasurement(1000.0, height_mm),
            ),
            TopBoundaryKind.FLAT,
        )

    def sloped_inputs(
        self,
        left_mm: float,
        right_mm: float,
    ) -> DoorOpeningInputs:
        return self._inputs(
            (
                HeightMeasurement(0.0, left_mm),
                HeightMeasurement(1000.0, right_mm),
            ),
            TopBoundaryKind.MEASURED_PROFILE,
        )

    def _inputs(
        self,
        heights: tuple[HeightMeasurement, ...],
        kind: TopBoundaryKind,
    ) -> DoorOpeningInputs:
        return DoorOpeningInputs(
            MeasuredSpace(1000.0, TopBoundary(kind, heights)),
            DesignSettings(InstallationBoundaries(True, True, True)),
        )


__all__ = ["DoorOpeningAssembly", "DoorOpeningFixture"]
