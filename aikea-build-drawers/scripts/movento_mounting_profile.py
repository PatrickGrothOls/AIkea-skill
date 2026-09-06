"""Scope: Define the proven native-CAD mounting datums for one MOVENTO set."""

from __future__ import annotations

from dataclasses import dataclass

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class MoventoMountingProfile:
    """Map one manufacturer's hardware frame into an AIkea owner frame."""

    drawer_front_to_manufacturer_origin_mm: float
    drawer_bottom_to_manufacturer_origin_mm: float
    native_x_in_owner: Vector3D
    native_y_in_owner: Vector3D
    native_z_in_owner: Vector3D
    runner_screw_native_z_mm: tuple[float, ...]

    def __post_init__(self) -> None:
        if min(
            self.drawer_front_to_manufacturer_origin_mm,
            self.drawer_bottom_to_manufacturer_origin_mm,
        ) <= 0.0:
            raise ValueError("MOVENTO mounting offsets must be greater than zero")
        if not self.runner_screw_native_z_mm:
            raise ValueError("MOVENTO mounting requires at least one runner fixing")


MOVENTO_760H5000S_MOUNTING = MoventoMountingProfile(
    drawer_front_to_manufacturer_origin_mm=37.0,
    drawer_bottom_to_manufacturer_origin_mm=9.575,
    native_x_in_owner=(1.0, 0.0, 0.0),
    native_y_in_owner=(0.0, 0.0, 1.0),
    native_z_in_owner=(0.0, -1.0, 0.0),
    runner_screw_native_z_mm=(0.0, -256.0),
)


__all__ = [
    "MOVENTO_760H5000S_MOUNTING",
    "MoventoMountingProfile",
    "Vector3D",
]
