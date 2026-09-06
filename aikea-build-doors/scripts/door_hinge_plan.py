"""Scope: Resolve one cabinet door's hinge quantity, positions, and fit status."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from door_hinge_compatibility import DoorHingeCompatibilityChecker
from door_hinge_side import DoorHingeSide
from riex_nc70_hinge_profile import RiexNc70HingeProfile
from system_32_hinge_placement_resolver import System32HingePlacementResolver
from panel_hardware_reservation import PanelHardwareReservation


@dataclass(frozen=True, slots=True)
class DoorHingePlacement:
    """Name one shared vertical center for door and cabinet machining."""

    hinge_id: str
    door_height_mm: float
    cabinet_height_mm: float
    cabinet_fixing_rows_mm: tuple[float, float]


@dataclass(frozen=True, slots=True)
class DoorHingePlan:
    """Carry the complete deterministic result for one hinged door."""

    assembly_id: str
    profile_id: str
    relationship: str
    hinge_side: DoorHingeSide
    door_width_mm: float
    door_height_mm: float
    door_thickness_mm: float
    door_mass_kg: float
    overlay_mm: float
    placements: tuple[DoorHingePlacement, ...]
    compatibility_issues: tuple[str, ...]

    @property
    def fabrication_ready(self) -> bool:
        return not self.compatibility_issues

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        values = asdict(self)
        values["fabrication_ready"] = self.fabrication_ready
        path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def read(cls, path: Path) -> "DoorHingePlan":
        values = json.loads(path.read_text(encoding="utf-8"))
        values.pop("fabrication_ready", None)
        values["hinge_side"] = DoorHingeSide(values["hinge_side"])
        values["placements"] = tuple(
            DoorHingePlacement(
                item["hinge_id"],
                float(item["door_height_mm"]),
                float(item["cabinet_height_mm"]),
                tuple(float(value) for value in item["cabinet_fixing_rows_mm"]),
            )
            for item in values["placements"]
        )
        values["compatibility_issues"] = tuple(values["compatibility_issues"])
        return cls(**values)


class DoorHingePlanner:
    """Fit the manufacturer quantity around this cabinet's owned features."""

    _PLYWOOD_DENSITY_KG_PER_M3 = 650.0

    def __init__(self) -> None:
        self.compatibility = DoorHingeCompatibilityChecker()
        self.placement_resolver = System32HingePlacementResolver()

    def plan(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
        blocked_reservations: tuple[PanelHardwareReservation, ...] = (),
    ) -> DoorHingePlan:
        door = assembly.part("door_panel")
        side = assembly.part(hinge_side.side_part_id)
        dimensions = self._dimensions(door)
        side_dimensions = self._dimensions(side)
        height_mm = dimensions[hinge_side.door_height_dimension]
        count = profile.hinge_count(height_mm)
        positions = self.placement_resolver.resolve(
            assembly,
            count,
            hinge_side,
            profile,
            blocked_reservations,
        )
        edge_gap_mm = (float(assembly.width_mm) - dimensions["width"]) / 2.0
        overlay_mm = side_dimensions["thickness"] - edge_gap_mm
        issues = self.compatibility.check(dimensions, overlay_mm, profile)
        return DoorHingePlan(
            assembly_id=assembly.assembly_id,
            profile_id=profile.profile_id,
            relationship=profile.relationship,
            hinge_side=hinge_side,
            door_width_mm=dimensions["width"],
            door_height_mm=height_mm,
            door_thickness_mm=dimensions["thickness"],
            door_mass_kg=self._door_mass(dimensions),
            overlay_mm=overlay_mm,
            placements=tuple(
                DoorHingePlacement(
                    f"hinge_{index:02d}",
                    position.door_center_mm,
                    position.cabinet_center_mm,
                    position.cabinet_fixing_rows_mm,
                )
                for index, position in enumerate(positions, start=1)
            ),
            compatibility_issues=issues,
        )

    def _door_mass(self, dimensions: dict[str, float]) -> float:
        volume_m3 = (
            dimensions["width"]
            * dimensions["left_height"]
            * dimensions["thickness"]
            / 1_000_000_000.0
        )
        return round(volume_m3 * self._PLYWOOD_DENSITY_KG_PER_M3, 2)

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["DoorHingePlacement", "DoorHingePlan", "DoorHingePlanner"]
