"""Scope: Import local hardware STEP geometry without moving or scaling it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hardware_asset_manifest import NativeStepBounds
from hardware_asset_resolver import ResolvedHardwareAsset

Vector3D = tuple[float, float, float]


class HardwareStepImportError(ValueError):
    """Report STEP geometry that differs from its recorded native observation."""


@dataclass(frozen=True, slots=True)
class ManufacturerFrame:
    """Name the unchanged coordinate system embedded in a vendor STEP file."""

    frame_id: str
    units: str
    origin: Vector3D
    x_axis: Vector3D
    y_axis: Vector3D
    z_axis: Vector3D


STEP_NATIVE_MILLIMETRE_FRAME = ManufacturerFrame(
    frame_id="step-native-mm",
    units="mm",
    origin=(0.0, 0.0, 0.0),
    x_axis=(1.0, 0.0, 0.0),
    y_axis=(0.0, 1.0, 0.0),
    z_axis=(0.0, 0.0, 1.0),
)


@dataclass(frozen=True, slots=True)
class ImportedHardwareStep:
    """Wrap untouched vendor geometry in consistent source and frame metadata."""

    asset: ResolvedHardwareAsset
    shape: Any
    manufacturer_frame: ManufacturerFrame
    solid_count: int
    bounds_mm: NativeStepBounds


class HardwareStepImporter:
    """Import one verified STEP while preserving its manufacturer coordinates."""

    _BOUND_TOLERANCE_MM = 1e-4

    def import_unchanged(
        self,
        asset: ResolvedHardwareAsset,
    ) -> ImportedHardwareStep:
        import cadquery as cq

        shape = cq.importers.importStep(str(asset.path)).val()
        bounding_box = shape.BoundingBox()
        bounds = NativeStepBounds(
            xmin=bounding_box.xmin,
            xmax=bounding_box.xmax,
            ymin=bounding_box.ymin,
            ymax=bounding_box.ymax,
            zmin=bounding_box.zmin,
            zmax=bounding_box.zmax,
        )
        solid_count = len(shape.Solids())
        self._verify_native_observation(asset, solid_count, bounds)
        return ImportedHardwareStep(
            asset=asset,
            shape=shape,
            manufacturer_frame=STEP_NATIVE_MILLIMETRE_FRAME,
            solid_count=solid_count,
            bounds_mm=bounds,
        )

    def _verify_native_observation(
        self,
        asset: ResolvedHardwareAsset,
        solid_count: int,
        bounds: NativeStepBounds,
    ) -> None:
        expected = asset.record.native_step_observation
        if expected is None:
            return
        bounds_match = all(
            abs(actual - recorded) <= self._BOUND_TOLERANCE_MM
            for actual, recorded in zip(bounds.values(), expected.bounds_mm.values())
        )
        if solid_count != expected.solid_count or not bounds_match:
            raise HardwareStepImportError(
                f"native STEP geometry differs from {asset.record.asset_id}"
            )


__all__ = [
    "HardwareStepImporter",
    "HardwareStepImportError",
    "ImportedHardwareStep",
    "ManufacturerFrame",
    "STEP_NATIVE_MILLIMETRE_FRAME",
    "Vector3D",
]
