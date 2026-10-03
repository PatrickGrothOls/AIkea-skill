"""Scope: Read the versioned local-CAD requirements for drawer hardware."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Any


class HardwareAssetState(str, Enum):
    """Distinguish build-approved CAD from incomplete inspection material."""

    READY = "ready"
    REQUIRES_USER_DOWNLOAD = "requires-user-download"
    INSPECTION_ONLY = "inspection-only"


@dataclass(frozen=True, slots=True)
class NativeStepBounds:
    """Record the unchanged bounds observed in a manufacturer's STEP frame."""

    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "NativeStepBounds":
        return cls(**{key: float(value) for key, value in values.items()})

    def values(self) -> tuple[float, ...]:
        return self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax


@dataclass(frozen=True, slots=True)
class NativeStepObservation:
    """Lock a verified STEP file to its native solid count and bounds."""

    solid_count: int
    bounds_mm: NativeStepBounds

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "NativeStepObservation":
        return cls(
            solid_count=int(values["solid_count"]),
            bounds_mm=NativeStepBounds.from_mapping(values["bounds_mm"]),
        )


@dataclass(frozen=True, slots=True)
class HardwareAssetRecord:
    """Describe one locally supplied CAD file without carrying its bytes."""

    asset_id: str
    component_type: str
    product_code: str
    catalog_item_number: str | None
    local_filename: str
    download_filename: str | None
    expected_sha256: str | None
    state: HardwareAssetState
    embedded_product_codes: tuple[str, ...]
    handedness: str | None
    handedness_basis: str | None
    unresolved_reason: str | None
    native_step_observation: NativeStepObservation | None

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "HardwareAssetRecord":
        observation = values.get("native_step_observation")
        return cls(
            asset_id=values["asset_id"],
            component_type=values["component_type"],
            product_code=values["product_code"],
            catalog_item_number=values.get("catalog_item_number"),
            local_filename=values["local_filename"],
            download_filename=values.get("download_filename"),
            expected_sha256=values.get("expected_sha256"),
            state=HardwareAssetState(values["state"]),
            embedded_product_codes=tuple(values.get("embedded_product_codes", ())),
            handedness=values.get("handedness"),
            handedness_basis=values.get("handedness_basis"),
            unresolved_reason=values.get("unresolved_reason"),
            native_step_observation=(
                NativeStepObservation.from_mapping(observation)
                if observation
                else None
            ),
        )


@dataclass(frozen=True, slots=True)
class HardwareAssetManifest:
    """Own product provenance and all registered local hardware assets."""

    schema_version: int
    vendor: str
    source_urls: tuple[str, ...]
    assets: tuple[HardwareAssetRecord, ...]

    @classmethod
    def load(cls, path: Path) -> "HardwareAssetManifest":
        values = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            schema_version=int(values["schema_version"]),
            vendor=values["vendor"],
            source_urls=tuple(values["source_urls"]),
            assets=tuple(
                HardwareAssetRecord.from_mapping(asset)
                for asset in values["assets"]
            ),
        )

    def asset(self, asset_id: str) -> HardwareAssetRecord:
        try:
            return next(asset for asset in self.assets if asset.asset_id == asset_id)
        except StopIteration as error:
            raise KeyError(f"hardware asset is not registered: {asset_id}") from error


__all__ = [
    "HardwareAssetManifest",
    "HardwareAssetRecord",
    "HardwareAssetState",
    "NativeStepBounds",
    "NativeStepObservation",
]
