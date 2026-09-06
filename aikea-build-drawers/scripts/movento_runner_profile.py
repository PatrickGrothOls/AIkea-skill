"""Scope: Define sourced planning values and CAD ownership for one MOVENTO pair."""

from __future__ import annotations

from dataclasses import dataclass

from movento_mounting_profile import MoventoMountingProfile


@dataclass(frozen=True, slots=True)
class DrawerInsideWidthLimits:
    """Describe the permitted drawer-inside width from one cabinet opening."""

    minimum_mm: float
    maximum_mm: float


@dataclass(frozen=True, slots=True)
class MoventoHardwareAssetIdentity:
    """Name one exact handed component in a depth-matched hardware set."""

    asset_id: str
    component_type: str
    product_code: str
    item_number: str
    handedness: str


@dataclass(frozen=True, slots=True)
class MoventoHardwareAssetSet:
    """Keep the fixed runners and moving locking devices matched together."""

    runner_left: MoventoHardwareAssetIdentity
    runner_right: MoventoHardwareAssetIdentity
    locking_device_left: MoventoHardwareAssetIdentity
    locking_device_right: MoventoHardwareAssetIdentity

    def identities(self) -> tuple[MoventoHardwareAssetIdentity, ...]:
        return (
            self.runner_left,
            self.runner_right,
            self.locking_device_left,
            self.locking_device_right,
        )


@dataclass(frozen=True, slots=True)
class MoventoRunnerProfile:
    """Keep one official runner product's planning values together."""

    product_code: str
    item_number: str
    nominal_length_mm: float
    maximum_load_kg: float
    hardware_asset_set: MoventoHardwareAssetSet | None
    mounting_profile: MoventoMountingProfile | None = None
    drawer_inside_width_deduction_mm: float = 42.0
    drawer_inside_width_negative_tolerance_mm: float = 1.5
    drawer_side_length_deduction_mm: float = 10.0
    maximum_drawer_side_thickness_mm: float = 16.0
    drawer_bottom_recess_minimum_mm: float = 12.0
    drawer_bottom_recess_maximum_mm: float = 15.0
    cabinet_depth_clearance_mm: float = 3.0
    mounting_width_mm: float | None = None
    runner_bearing_height_mm: float | None = None
    cabinet_profile_width_mm: float | None = None

    def __post_init__(self) -> None:
        positive_values = (
            self.nominal_length_mm,
            self.maximum_load_kg,
            self.drawer_inside_width_deduction_mm,
            self.drawer_side_length_deduction_mm,
            self.maximum_drawer_side_thickness_mm,
            self.cabinet_depth_clearance_mm,
        )
        if any(value <= 0.0 for value in positive_values):
            raise ValueError("MOVENTO planning dimensions must be greater than zero")
        if self.drawer_inside_width_negative_tolerance_mm < 0.0:
            raise ValueError("drawer width tolerance cannot be negative")
        if self.drawer_bottom_recess_minimum_mm > self.drawer_bottom_recess_maximum_mm:
            raise ValueError("drawer bottom recess limits are reversed")

    def drawer_inside_width_limits(
        self,
        cabinet_clear_width_mm: float,
    ) -> DrawerInsideWidthLimits:
        maximum_mm = cabinet_clear_width_mm - self.drawer_inside_width_deduction_mm
        return DrawerInsideWidthLimits(
            minimum_mm=maximum_mm - self.drawer_inside_width_negative_tolerance_mm,
            maximum_mm=maximum_mm,
        )

    @property
    def drawer_side_length_mm(self) -> float:
        return self.nominal_length_mm - self.drawer_side_length_deduction_mm

    def required_inside_depth_mm(self, inner_front_thickness_mm: float = 0.0) -> float:
        if inner_front_thickness_mm < 0.0:
            raise ValueError("inner front thickness cannot be negative")
        return (
            self.nominal_length_mm
            + inner_front_thickness_mm
            + self.cabinet_depth_clearance_mm
        )

    def require_hardware_asset_set(self) -> MoventoHardwareAssetSet:
        if self.hardware_asset_set is None:
            raise ValueError(
                f"selected runner {self.product_code} has no complete hardware CAD set"
            )
        return self.hardware_asset_set

    def require_mounting_profile(self) -> MoventoMountingProfile:
        if self.mounting_profile is None:
            raise ValueError(
                f"selected runner {self.product_code} has no verified mounting profile"
            )
        return self.mounting_profile


__all__ = [
    "DrawerInsideWidthLimits",
    "MoventoHardwareAssetIdentity",
    "MoventoHardwareAssetSet",
    "MoventoRunnerProfile",
]
