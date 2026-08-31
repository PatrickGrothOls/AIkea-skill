"""Scope: Define the measured opening and resolved wooden drawer-box values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from drawer_part_locator import DrawerPartPlacement


@dataclass(frozen=True, slots=True)
class CabinetDrawerOpening:
    """Describe the clear cabinet space available to one drawer."""

    clear_width_mm: float
    inside_depth_mm: float

    @classmethod
    def from_assembly_spec(cls, assembly: Any) -> "CabinetDrawerOpening":
        """Read the clear opening from one generated cabinet specification."""
        left_side = assembly.part("left_side")
        right_side = assembly.part("right_side")
        left_thickness_mm = float(left_side.local_size_mm[2])
        right_thickness_mm = float(right_side.local_size_mm[2])
        return cls(
            clear_width_mm=(
                float(assembly.width_mm)
                - left_thickness_mm
                - right_thickness_mm
            ),
            inside_depth_mm=float(assembly.inside_depth_mm),
        )


@dataclass(frozen=True, slots=True)
class DrawerBoxSizingProfile:
    """Hold the construction values that determine one wooden drawer box."""

    runner_length_mm: float
    drawer_inside_width_reduction_mm: float = 42.0
    runner_to_side_length_reduction_mm: float = 10.0
    side_thickness_mm: float = 15.0
    front_back_thickness_mm: float = 15.0
    bottom_thickness_mm: float = 9.0
    bottom_underside_recess_mm: float = 13.0
    box_height_mm: float = 160.0


@dataclass(frozen=True, slots=True)
class DrawerPartSpec:
    """Describe one unmachined sheet part in its manufacturing frame."""

    part_id: str
    role: str
    width_mm: float
    height_mm: float
    thickness_mm: float
    local_to_parent: DrawerPartPlacement | None = None

    @property
    def local_size_mm(self) -> tuple[float, float, float]:
        return self.width_mm, self.height_mm, self.thickness_mm


@dataclass(frozen=True, slots=True)
class DrawerBoxSpec:
    """Own every calculated dimension and sheet part for one drawer box."""

    opening: CabinetDrawerOpening
    sizing: DrawerBoxSizingProfile
    clear_inside_width_mm: float
    outside_width_mm: float
    side_length_mm: float
    outside_depth_mm: float
    clear_inside_depth_mm: float
    parts: tuple[DrawerPartSpec, ...]

    def part(self, part_id: str) -> DrawerPartSpec:
        return next(part for part in self.parts if part.part_id == part_id)


__all__ = [
    "CabinetDrawerOpening",
    "DrawerBoxSizingProfile",
    "DrawerBoxSpec",
    "DrawerPartSpec",
]
